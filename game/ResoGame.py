'''
Author: Achetair
Date: 2024-03-08 23:46:19
LastEditors: Achetair
Description: 
'''
#-*- config:utf-8 -*-
# python 3.11

from enum import auto
from re import L
import time
import datetime
from tkinter import NO
import numpy as np
from cnocr import CnOcr

from resotools.game.ABSObj import *
from resotools.utils.cvTools import *
from resotools.utils.ocrtools import Ocr_tools

from game.ResoGoodsCal import City

    
    
class ResoCityGraph():
    def __init__(self) -> None:
        # 制作城市地图
        map_size = 2640
        self.citymap = [[0 for _ in range(map_size)] for _ in range(map_size)]
        
        # 城市的坐标点
        self.cityPosInfo = {
            "汇流塔":(49,1824),
            "海角城":(420,1825),
            "阿妮塔能源研究所":(580,1053),
            "7号自由港":(651,430),
            "阿妮塔战备工厂":(884,548),
            "澄明数据中心":(1184,107),
            "修格里城":(1578,274),
            "铁盟哨站":(1882,272),
            "荒原站":(2223,271),
            "曼德矿场":(2019,551),
            "贡露城":(1346,1422),
            "淘金乐园":(2158,941),
        }
        
        
        
        for k,v in self.cityPosInfo.items():
            self.citymap[v[0]][v[1]] = 1
    
    def getCitys(self):
        return list(self.cityPosInfo.keys())
    
    def getCityDistance(self, srccity:str, dstcity:str, per=1):
        log.info("城市1 {} , 城市2： {}".format(srccity, dstcity))
        assert srccity in self.cityPosInfo.keys()
        assert dstcity in self.cityPosInfo.keys()
        src_pos = self.cityPosInfo[srccity]
        dst_pos = self.cityPosInfo[dstcity]
        
        x = int((src_pos[0] - dst_pos[0])/per)
        y = int((src_pos[1] - dst_pos[1])/per)
        return (x,y)
    
    
    
class ResoadbObj(ABSadbObj):
    def __init__(self, title="MuMu模拟器12") -> None:
        super().__init__(title)
        self.moudle_name = "ResoadbObj"
        self.store_pic_path = "D:/work/resotools/pngdata/leisuonasi"
        self.store_json_path = os.path.join(os.getcwd(), "json")
        self.ocr = Ocr_tools()
        self.__classValueInit()
    
    def __classValueInit(self):
        self.commerce_city = ["7号自由港", "澄明数据中心", "修格里城", "曼德矿场"]
        
        self.can_add_strength = False
        self.is_strenth_less = False
        
        
        
        self.pos_data = {
            "自动战斗":[311, 32, 389, 98],
            "自动巡航":[920.0, 164.0, 1040.0, 205.0],
            # "弹丸图标":[1588, 978, 1640, 1027],
            "弹丸数量":[1585, 1036, 1645, 1058],
            "商会城市名称":[1345.0, 335.0, 1688.0, 369.0],
            "载货量":[1758.0, 581.0, 1810.0, 608.0],
            "卖出":[1500.0, 945.0, 1642.0, 998.0]
        }
        self.gameFlag = {
            "自动战斗":False,
        }
        self.__gameFlagRefresh()
        
        self.text_funcaction_dict = {
            "触碰":"click",
            "进入游戏":"click",
            "自动巡航":self.autoCruise,
            "下一步":"click",
        }
        self.img_funcact_dict={
            "fighting.png":self.waitMissionEnd,
            "huweiduiyingji.png":self.autoCruise,
            "fighting.png":self.waitMissionEnd,
            "jinruzhandian.png":self.stepToCity,
            "fangwenchengshi.png":"click",
        }       
        
        self.resograph = ResoCityGraph()
        
        # 一些类的信息
        # self.city_list = ["曼德矿场","阿妮塔能源研究所","7号自由港", "澄明数据中心","修格里城"]
        self.city_list = self.resograph.getCitys()
        self.tmpcityDes = "" # 临时城市目的地
        
        self.file_daily_info = None
        self.daily_info = None
        
    def __checkDailyInfo(self):
        if self.daily_info is not None:
            return True
        # 检测日常文件是否存在
        if self.tmpstore_path is None:
            raise Exception
        self.file_daily_info = os.path.join(self.store_json_path, "dailyinfo.json")
        if not os.path.exists(self.file_daily_info) or os.stat(self.file_daily_info).st_size == 0:
            self.daily_info = {}
            for city in self.city_list:
                self.daily_info[city] = {}   
        else:  
            self.daily_info =  load_json(self.file_daily_info)
        return True
    
    def __isCityDailyComplete(self, xm="commerce"):
        # 获取当前城市
        if self.tmpcityDes != "":
            if self.daily_info.get(self.tmpcityDes) != None:
                xminfo = self.daily_info[self.tmpcityDes].get(xm)
                if xminfo is not None:
                    nowtime = getNowTimeFormat("%Y-%m-%d", -5)
                    cityfinishTime = xminfo.get("finish_time")
                    if cityfinishTime == nowtime:
                        # log.info("城市 {} 的商会任务已经领取".format(self.tmpcityDes))
                        return True
        return False
           
    def dailyChamberOfCommerce(self):
        # 检测商会任务是否已经完成了
        self.__checkDailyInfo()

        if self.__isCityDailyComplete("commerce"):
            return 

        self.backToCityHome()
        
        # 获取商会截图
        log.info("获取城市：{} 的商会任务".format(self.tmpcityDes))
        for i in range(3):
            self.takeTabShoot()
            state = self._ocr_offclick("商会")
            if state is None:
                srcpos = (767, 506)
                dstpos = (926, 847)
                self.adb_obj.swipePosition(srcpos, dstpos)
            else:
                break
                # raise Exception
        if state is None:
            return 
    
        # 获取城市名称
        while True:
            self.takeTabShoot()
            xm_name = "商会城市名称"
            part_pic = self.cutPartPic(self.pos_data[xm_name])
            state = self.ocr.ocr_singleline(part_pic)
            if state is not None:
                # print(state)
                city_uniqname = getPhraseRepchar(self.city_list)
                for repchar, cityname in city_uniqname.items():
                    if repchar in state:
                        self.tmpcityDes = cityname
                        break
                if self.tmpcityDes == "":
                    continue
                break            
        log.info("访问城市：{}".format(self.tmpcityDes))
        if self.__isCityDailyComplete("commerce"):
            self.backToCityHome()
            return 
        # 点击运输订单
        self.takeTabShoot()
        state = self.clickPictureEvent("yunshudingdan.png", name="运输订单")
        # 统计订单数量
        srcpos = (804, 807)
        dstpos = (804, 465)
        order_count = 0
        while(True):
            self.takeTabShoot()
            state = self._ocr_tabshoot("接取", True)
            if state is None:
                state = self._ocr_tabshoot("追加")
                if state is not None:
                    break
            else:
                for ooo in state:
                    self.adb_obj.clickPosition(ooo[1])
                    self.takeTabShoot()
                    tstate = self._ocr_tabshoot("接取")
                    if tstate is not None:
                        self.adb_obj.clickPosition(tstate[1])
                    time.sleep(1)
                    order_count += 1
            self.adb_obj.swipePosition(srcpos, dstpos)
            time.sleep(2)
        log.info("获取[{}]订单数量：{} 个".format(self.tmpcityDes, order_count))
        
        # 保存商会信息
        nowTime = getNowTimeFormat("%Y-%m-%d", -5)
        citycommerceinfo = {
            "order_count":order_count,
            "finish_time":nowTime
        }
        self.daily_info[self.tmpcityDes]["commerce"] = citycommerceinfo
        save_as_json(self.daily_info, self.file_daily_info)
        
        self.backToCityHome()
    
    def __gameFlagRefresh(self):
        for k,v in self.pos_data.items():
            # if k in self.gameFlag:
            #     continue
            # else:
            #     self.gameFlag[k] = False
            self.gameFlag[k] = False
            
    def dailyCenter(self):
        state = self.locateTpicture("cityhomepage.png")
        if state is not None:
            if self.tmpcityDes != "":
                if self.tmpcityDes not in self.commerce_city:
                    return
            self.dailyChamberOfCommerce()
            self.autoIronSecurity()
            self.dailyRest()    
            
    def dealExceptionCenter(self):
        self.takeTabShoot()    
        if not self.dispatchWordCenter():
            self.dispatchImgCenter()

    def dispatchImgCenter(self):
        gameStates = self.img_funcact_dict.keys()
        for gs in gameStates:
            self.takeTabShoot()
            dPos = self.locateTpicture(gs)
            if dPos is None:
                continue
            else:
                # 进入对应的状态
                state = self.img_funcact_dict[gs]
                if state == "click":
                    self.clickPictureEvent(gs)
                else:
                    state()
                    return True
        return False
            
    def dailyRest(self):
        self.__checkDailyInfo()
        xm = "restcore"
        if self.__isCityDailyComplete(xm):
            return
        
        failed_count = 0
        while(True):
            self.takeTabShoot()
            state = self._ocr_offclick("休息区")
            if state is None:
                failed_count += 1
                if failed_count % 3 == 2:
                    self.backToCityHome()
                    continue
                if failed_count >= 7:
                    raise Exception
                srcpos = (1132, 467)
                dstpos = (1036, 545)
                self.adb_obj.swipePosition(srcpos, dstpos)
                continue
            failed_count = 0
            break
        
        self.takeTabShoot(2)
        state = self.clickPictureEvent("heyibei.png")
        if state is None:
            return
        
        self.takeTabShoot()
        state = self.locateTpicture("yinzhi.png")
        if state is not None:
            self._ocr_click("取消")
            
            nowTime = getNowTimeFormat("%Y-%m-%d", -5)
            restinfo = {
                "finish_time":nowTime
            }
            self.saveDailyInfo(xm ,restinfo)
            
            self.backToCityHome()
            return    
        
        self.takeTabShoot()
        state = self.clickPictureEvent("heyibei.png")
        if state is None:
            return 
         
        lf = 0
        rc = 0
        while(True):
            self.takeTabShoot(1)
            if lf & 1 != 1:
                state = self.clickPictureEvent("blackcheksymbol.png")
                if state is not None:
                    lf = lf | 1
                    continue
            if lf & 2 != 2:
                state = self._ocr_click("skip")
                if state is not None:
                    lf = lf | 2
                    continue
            state = self._ocr_click("确定")
            if state is not None:
                break
            rc += 1
            if rc >=4:
                break
        nowTime = getNowTimeFormat("%Y-%m-%d", -5)
        restinfo = {
            "finish_time":nowTime
        }
        self.saveDailyInfo(xm ,restinfo)

        
        self.takeTabShoot()
        self.backToCityHome()
        
    def saveDailyInfo(self, xm, infodata):
        self.daily_info[self.tmpcityDes][xm] = infodata
        save_as_json(self.daily_info, self.file_daily_info)        
            
    def dispatchWordCenter(self):
        # self.takeTabShoot()
        ocrinfos = self.ocr.ocr_img(self.adb_obj.screenshoot_path)
        # print(ocrinfos)
        findinfos = self.findKeyWord(ocrinfos)
        if findinfos is not None:                    
            nkey = findinfos["nkey"]
            msg = findinfos["text"]
            pos = findinfos["pos"]
            log.info("通过 【{}】 发现信息：【{}】，位置{}".format(nkey,msg,pos))
            if self.text_funcaction_dict[nkey] == "click":
                log.info("执行[{}]的操作[{}]".format(nkey, "click"))
                self.adb_obj.clickPosition(pos)
            else:
                log.info("执行[{}]的操作[{}]".format(nkey, self.text_funcaction_dict[nkey].__name__))
                self.text_funcaction_dict[nkey]()
            return True
        else:
            return False        
                
    def autoDetectExcute(self):
        # 持续性对界面进行文字识别
        repeat_num = 0
        while(True):
            self.takeTabShoot()
            if self.dispatchWordCenter():
                continue
            else:
                if not self.dispatchImgCenter():
                    self.dailyCenter()
                if repeat_num == 0:
                    log.info("待机中，(+.+)(-.-)(_ _) ..zzZZ")
                time.sleep(5)
                repeat_num += 1
                continue                 

                    
    def _setTmpcity(self, cityname):
        assert cityname in self.city_list
        self.tmpcityDes = cityname
        
    def searchTargetCity(self, tocity):
        centPoint = Point(860, 540)
        # 点击地图
        self.takeTabShoot()
        self.clickPictureEvent("cityhomepage.png", "启程页面")
        # time.sleep(1)
        self.takeTabShoot()
        state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "启程")
        # print(state)
        if state is not None:
            self.adb_obj.clickPosition(state[1])
        else:
            raise Exception
        log.info("启程：开始选择搜索本次旅途目的地：{}".format(tocity))
        
        self.takeTabShoot()
        state = self.locateTpicture("pilaotubiao.png")
        if state is None:
            # log.error("未知错误")
            raise Exception
        # 进入地图开始查找相关的数据
        dis = self.resograph.getCityDistance(self.tmpcityDes, tocity, 1)
        endPoint = centPoint + Point(*dis)
        # endPoint.clamp()
        log.info("开始位置:{}, 结束位置：{}".format(centPoint, endPoint))
        count = 0
        while(True):
            # 滑动屏幕寻找目的地
            self.adb_obj.swipePosition(centPoint.tuple(), endPoint.tuple())
            
            self.takeTabShoot()
            state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, tocity)       
            if state is not None:
                self.adb_obj.clickPosition(state[1])
                break
            count += 1
            if count >= 4:
                raise ResoDesCityNotFound
            
        time.sleep(1)
        for i in range(3):
            self.takeTabShoot()
            state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "前往目的")
            if state is not None:
                pos = state[1]
                pos[0] = pos[0] - 80
                self.adb_obj.clickPosition(pos)
                return

        raise Exception
        
    
    def _sell(self):
        self.takeTabShoot()
        state = self.clickPictureEvent("sell.png", "我要卖")
        time.sleep(2)
        
        # 检查载货量
        xm_name = "载货量"
        self.takeTabShoot()
        part_pic = self.cutPartPic(self.pos_data[xm_name])
        state = self.ocr.ocr_number(part_pic)
        if state is None:
            raise ResoNoBankFound
        if (state <= 20):
            log.info("当前货量：{}， 货物已经卖出，开始买！".format(state))
            return  
        log.info("目前载货量：{}/530， 开始卖货".format(state))
        
        state = self._ocr_tabshoot("全部")
        if state is None:
            raise Exception
        self.adb_obj.clickPosition(state[1])
        time.sleep(1)
        state = self._ocr_tabshoot("卖出", True)[-1]


        self.adb_obj.clickPosition(state[1])
        time.sleep(3)
        self._clickBlank()

        
    def _clickBlank(self):
        center = (983, 1014)
        self.adb_obj.clickPosition(center)
    
    def _buy(self):
        # state = self.clickPictureEvent("fanhui.png","返回")
        # if state is None:
        #     raise Exception
        log.info("我要买！买！买！买！")
        repeat_num = 0
        while(True):
            self.takeTabShoot()
            state = self.locateTpicture("buy.png")
            if state is None:
                # 重新进入交易所
                if repeat_num == 0:
                    state = self.clickPictureEvent("fanhui.png","返回")
                if repeat_num >= 1:
                    log.info("未发现买入图片，重新进入城市进行查找")
                    # 重新进入城市
                    time.sleep(1)
                    self.backToCityHome()
                    time.sleep(1)
                    # 重新进入交易所
                    self.stepToBusiness()

                if repeat_num >= 3:
                    raise Exception
                repeat_num += 1
            else:
                self.adb_obj.clickPosition(state)
                break
                    
        time.sleep(2)       
        
        # 检查载货量
        xm_name = "载货量"
        self.takeTabShoot()
        part_pic = self.cutPartPic(self.pos_data[xm_name])
        state = self.ocr.ocr_number(part_pic)
        if state is None:
            state = 0
        if (state >= 200):
            log.info("卖货不成功！")
            raise Exception
        repeat_num = 1

        state = self._ocr_tabshoot("全部")
        if state is None:
            raise Exception
        self.adb_obj.clickPosition(state[1])
        time.sleep(1)        
        state = self._ocr_tabshoot("买入", True)[-1]
        self.adb_obj.clickPosition(state[1]) 

        time.sleep(3)
        self._clickBlank()
        
    
    def stepToBusiness(self):
        log.info("交易所，I'm coming ~~~~~~~")
        time.sleep(2)
        repeat_num = 0
        while(True):
            self.takeTabShoot()
            state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "交易所")
            if state is not None:
                pos = state[1]
                x = pos[0] - 5
                y = pos[1] + 120
                self.adb_obj.clickPosition((x,y))
                break
            else:
                # 刷新重新进入
                self.backToCityHome()
                repeat_num += 1
            if repeat_num >= 1:
                time.sleep(1)
                for i in range(repeat_num):
                    # 进行拖拽的操作
                    bPos = (1199,434)
                    ePos = (903,436)
                    self.adb_obj.swipePosition(bPos,ePos)
            if repeat_num >= 4:
                log.error("没有发现交易所")
                raise ResoNoBankFound        
        
    def buyandsell(self):
        self.stepToBusiness()
        time.sleep(1)
        self._sell()
        time.sleep(1)
        self._buy()
        
    def _ocr_tabshoot(self, characs, isStrict=False, picName=None):
        if picName is None:
            picName = self.adb_obj.screenshoot_path
        # self.takeTabShoot()
        if isStrict:
            return self.ocr.ocr_characters_strict(picName, characs)
        else:
            return self.ocr.ocr_characters(picName, characs)
        
    def _ocr_offclick(self, chara, isStrict=False):
        state = self._ocr_tabshoot(chara)
        if state is not None:
            pos = state[1]
            x = pos[0] - 5
            y = pos[1] + 120
            self.adb_obj.clickPosition((x,y))
        return state
    
    def _ocr_click(self, chara, isStrict=False): 
        state = self._ocr_tabshoot(chara)
        if state is not None:
            pos = state[1]
            self.adb_obj.clickPosition(pos)
        return state            
                    
    def autoRunningBusiness(self, city1, city2, current_level = 8):
         # 判断当前所在的城市
        if self.tmpcityDes == "":
            self.tmpcityDes = city1
            
        dstcity = ""
        if self.tmpcityDes == city1:
            # 当前城市是 city1
            dstcity = city2
        else:
            dstcity = city1
            assert self.tmpcityDes == city2
            
        srccity = self.tmpcityDes
        while(True):
            try:
                if current_level >= 7:
                    self.searchTargetCity(dstcity)
                if current_level >= 5:
                    self.autoCruise()
                    self.stepToCity() 
                # 进入城市,交易所
                if current_level >= 3:
                    self.buyandsell()
                # 交换目的地和开始位置
                dstcity = srccity
                srccity = self.tmpcityDes
                current_level = 8
            except ResoDesCityNotFound as e:
                log.error("目的地：{} 没有找到".format(dstcity))
                continue
            except ResoNoBankFound as e:
                log.error("城市：{} 未找到交易所".format(self.tmpcityDes))
                self.backToCityHome()
                current_level = 4
                continue
            
    
    def _clickGameGraph(self):
        # 点击游戏的地图
        game_map_pos = (158,170)
        self.takeTabShoot()
        log.info("进入游戏地图")
        self.adb_obj.clickPosition(game_map_pos)
    
    # 返回城市的首页
    def backToCityHome(self):
        log.info("城市：{} 首页".format(self.tmpcityDes))
        self.takeTabShoot()
        state = self.locateTpicture("cityhomepage.png")
        if state is not None:
            self.adb_obj.clickPosition(state)
        time.sleep(1)
        
        self.takeTabShoot()
        state = self.clickPictureEvent("fangwenchengshi.png")
        return 
    
    def autoIronSecurity(self):
        self.__checkDailyInfo()
        xm = "ironsecure"
        if self.__isCityDailyComplete(xm) or self.is_strenth_less:
            return 
        
        log.info("自动化清理铁安局日常")
        self.backToCityHome()

        # 点击铁安局，自动战斗
        self.takeTabShoot()
        state = self._ocr_tabshoot("铁安局")
        # time.sleep(1)
        # self.takeTabShoot()
        # state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "铁安局")
        if state is not None:
            pos = state[1]
            x = pos[0] - 5
            y = pos[1] + 120
            self.adb_obj.clickPosition((x,y))
        time.sleep(1)
        # 点击悬赏任务
        self.takeTabShoot()
        self.clickPictureEvent("xuanshangrenwu.png", name="悬赏任务")
        count = 0
        iron_count = 0
        while(True):
            self.takeTabShoot()
            state = self.locateTpicture("zuozhan.png")
            if state is not None:
                self.adb_obj.clickPosition(state)
                time.sleep(1)
                try:
                    self.waitMissionEnd()
                except FightUnexpectException:
                    if self.isStrengthLess():
                        return
                iron_count += 1
                count = 0
            else:
                count += 1
            time.sleep(1)
            if count >= 2:
                log.info("铁安局清理完成！")
                
                # 记录信息
                nowTime = getNowTimeFormat("%Y-%m-%d", -5)
                ironinfo = {
                    "count":iron_count,
                    "finish_time":nowTime
                }
                self.daily_info[self.tmpcityDes][xm] = ironinfo
                save_as_json(self.daily_info, self.file_daily_info)   
                             
                self.backToCityHome()
                return 
    
    # 自动巡航   
    def autoCruise(self, num=5):
        # 自动巡航的状态
        log.info("列车进入自动巡航的状态！")
        repeat_num = 0 
        isDisCertain = False
        distance = 1000
        destination = ""
         
        while(True):
            time.sleep(1)
            self.takeTabShoot()
            # 获取剩余里程，目的地
            state = self.ocr.ocr_mutitext(self.adb_obj.screenshoot_path, ["剩余行程", "目的地"])

            if state is not None:
                if state.get("剩余行程") is not None:
                    tmpdis = state["剩余行程"]["text"]
                    # tdis = 
                    distance = getTextNumber(tmpdis)
                # print("距离")
                if not isDisCertain and state.get("目的地") is not None:
                    destination = state["目的地"]["text"].split("：")[-1]
                    if destination in self.city_list:
                        self.tmpcityDes = destination
                        isDisCertain = True
                log.info("距离[{}]还有[{}]km".format(destination, distance))
                
            xm_name = "自动巡航"
            part_pic = self.cutPartPic(self.pos_data[xm_name])
            state = self.ocr.ocr_characters(part_pic, xm_name)
            # state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "自动巡航")

            if state is not None:
                # 还在自动巡航中
                repeat_num = 0
                xm_name = "弹丸数量"
                self.takeTabShoot()
                part_pic = self.cutPartPic(self.pos_data[xm_name])
                state = self.ocr.ocr_number(part_pic)
                if state is None:
                    # 正在加速中
                    state = self.ocr.ocr_characters(part_pic, "加速")
                    if state is not None:
                        log.info("亲，列车正在加速中~～(￣▽￣～)(～￣▽￣)～~")
                        time.sleep(3)
                        continue
                else:
                    # 点击加速弹丸
                    if distance >= 50 and state != 0:
                        self.clickPictureEvent("jiasudanwan.png",name="加速弹丸", num=1)
                    else:
                        log.info("距离[{}]太近，停止使用加速弹丸".format(destination))
                    log.info("加速弹丸数量剩余：{}/7".format(state))
                    continue
                    
            state = self.clickPictureEvent("huweiduiyingji.png", name="护卫队袭击", num=1)
            if state is not None:
                log.info("(ｷ｀ﾟДﾟ´)!! 被野怪袭击！！！干他！！！")
                repeat_num = 0
                self.waitMissionEnd()

            state = self.locateTpicture("jinruzhandian.png")
            if state is not None:
                log.info("列车已经到站，请下车！！")
                self.stepToCity()
                return
                
            repeat_num += 1
            if repeat_num >=num:
                state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "自动巡航")
                if state is None:
                    log.info("意外，退出自动巡航的状态")
                    return
                repeat_num = 0
                
    def fightFloatTree(self, funm=5):
        if funm:
            log.info("混响浮标战斗次数：{}".format(funm))
        else:
            log.info("混响浮标持续战斗..........")

        s_start_time = getNowTime()
        s_end_time = getNowTime()
        fight_list = []
        avg_fight_time = 300        
        
        repeat_count = 0
        while(True):  
            time.sleep(1)
            self.takeTabShoot()
            state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "开始作战")
            if state is not None:
                s_start_time = getNowTime()
                self.adb_obj.clickPosition(state[1])
                time.sleep(2)
            else:
                repeat_count += 1
                if repeat_count == funm:
                    break
                continue
            try:
                self.waitMissionEnd()
            except FightUnexpectException:
                self._clickBlank()
                self.dealExceptionCenter()
                
            s_end_time = getNowTime()
            fight_list.append(s_end_time-s_start_time)
            
            if len(fight_list) > 3:
                avg_fight_time = sum(fight_list) / len(fight_list)
                log.info("混响浮标第{}次战斗结束，平均时间{}s".format(len(fight_list), avg_fight_time))
            else:
                log.info("混响浮标第{}次战斗结束。".format(len(fight_list)))
            time.sleep(3)

        
    def isStrengthLess(self):
        self.takeTabShoot()
        state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "澄明度不足")
        if state is None:
            log.error("澄明度充足，出现了误报")
            return
        log.info("澄明度不足!!!!")
        if not self.can_add_strength:
            self.is_strenth_less = True
            state = self._ocr_click("取消")
            self.backToCityHome()
    
    def stepToCity(self):
        # 通过图标进入城市
        self.takeTabShoot()
        # state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "到站")
        state = self.clickPictureEvent("jinruzhandian.png", name="进入站点")
        if state is None:
            return 
        time.sleep(3)
        self.takeTabShoot()
        state = self.clickPictureEvent("fangwenchengshi.png", name="访问城市")
        # assert self.tmpcityDes != ""
        log.info("进入城市：【{}】".format(self.tmpcityDes))
        
                
    def waitMissionEnd(self,num=5):
        # self.clickPictureEvent("zuozhan.png", "作战")
        ffight = False
        log.info("开始作战！！！")
        
        s_start_time = getNowTime()

        repeat_count = 0
        while(True):
            self.takeTabShoot()
            if not ffight:
                state = self.clickPictureEvent("kaishizuozhan.png", "开始作战", num=2)
                ffight = True
                time.sleep(8)
                continue
                
            state = self.locateTpicture("fighting.png")
            if state is not None:
                # 检测自动战斗是否开启
                if not self.gameFlag["自动战斗"]:
                    # self.locateTpicture("autofighttagwhite.png")
                    cutfile = self.cutPartPic(self.pos_data["自动战斗"])
                    # 检测灰度
                    color = detect_color(cutfile)
                    if color == "grey":
                        log.info("自动战斗开启")
                        self.adb_obj.clickPosition(calcenterpos(self.pos_data["自动战斗"]))
                    self.gameFlag["自动战斗"] = True    
                endTime = getNowTime()
                if int(endTime - s_start_time) % 30 <= 5:         
                    log.info("游戏还没有结束请等待......")
                ffight = True
                time.sleep(5)
                continue
                
            endp = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "下一步")
            if endp is not None:
                repeat_count = 0
                log.info("检测到[{}], 点击{}".format(endp[0], endp[1]))
                self.adb_obj.clickPosition(endp[1]) 
                break 
            
            repeat_count += 1
            if repeat_count >= num:
                time.sleep(1)
                log.info("出现意外退出循环")   
                raise FightUnexpectException
            
        endTime = getNowTime()
        log.info("作战结束, 持续时间 {}s".format(endTime - s_start_time))
        return s_start_time - endTime
                    

    def findKeyWord(self, ocr_result):
        textinfos = self.text_funcaction_dict.keys()
        # 遍历ocr的结果
        for ocrvd in ocr_result:
            ocrtext = ocrvd["text"]
            # 和关键字进行比较
            for tinfo in textinfos:
                if tinfo in ocrtext:
                    return {
                        "nkey":tinfo,
                        "text":ocrtext,
                        "pos":self.ocr.ocr_center_pos(ocrvd["position"])
                    }
        return None
                    
    # def enterGame(self):
        

        
    
if __name__ == "__main__":
    A = ResoadbObj()
    A.setAdbInfo("127.0.0.1", "16384", "connection/adb.exe", "tmp" )
    # A.dispatchOcrCenter()
    A.takeTabShoot()
    A.backToCityHome()
    # rrr = A.ocr.ocr_characters(A.adb_obj.screenshoot_path, "下一步")
    # A.locateTpicture("zidongxunhang.png")
    # print(A.locateTpicture.__name__)
    # A.takeTestTabShoot("xiaohongdian.png")
    # A.gotoMission()
    # img_path = "D:/work/resotools/tmp/test-ResoadbObj/kaishijiemian.png"
    # B = Ocr_tools()
    # # rrr = B.ocr.ocr(img_path)
    # rrr = B.ocr_characters(img_path, "进入游戏")
    # print(rrr)