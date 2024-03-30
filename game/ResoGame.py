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
import stat
import time
import datetime
from tkinter import NO
import numpy as np
from cnocr import CnOcr

from resotools.game.ABSObj import *
from resotools.utils.cvTools import *
from resotools.utils.ocrtools import Ocr_tools
from scipy.fft import dst

    
    
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
        self.ocr = Ocr_tools()
        self.__classValueInit()
    
    def __classValueInit(self):
        self.pos_data = {
            "自动战斗":[311, 32, 389, 98],
            "自动巡航":[920.0, 164.0, 1040.0, 205.0],
            # "弹丸图标":[1588, 978, 1640, 1027],
            "弹丸数量":[1585, 1036, 1645, 1058],
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
    
    def __gameFlagRefresh(self):
        for k,v in self.pos_data.items():
            # if k in self.gameFlag:
            #     continue
            # else:
            #     self.gameFlag[k] = False
            self.gameFlag[k] = False

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

                
    def autoDetectExcute(self):
        # 持续性对界面进行文字识别
        repeat_num = 0
        while(True):
            self.takeTabShoot()
            ocrinfos = self.ocr.ocr_img(self.adb_obj.screenshoot_path)
            # print(ocrinfos)
            findinfos = self.findKeyWord(ocrinfos)
            if findinfos is None:
                self.dispatchImgCenter()
                if repeat_num == 0:
                    log.info("待机中，(+.+)(-.-)(_ _) ..zzZZ")
                time.sleep(5)
                repeat_num += 1
                continue
            else:
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
        
    def _ocr_tabshoot(self, characs, isStrict=False):

        self.takeTabShoot()
        if isStrict:
            return self.ocr.ocr_characters_strict(self.adb_obj.screenshoot_path, characs)
        else:
            return self.ocr.ocr_characters(self.adb_obj.screenshoot_path, characs)
            
                    
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
        while(True):
            self.takeTabShoot()
            state = self.locateTpicture("zuozhan.png")
            if state is not None:
                self.adb_obj.clickPosition(state)
                time.sleep(1)
                self.waitMissionEnd()
                count = 0
            else:
                count += 1
            time.sleep(1)
            if count >= 2:
                log.info("铁安局清理完成！")
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
                    log.info("加速弹丸数量剩余：{}/6".format(state))
                    continue
                    
            state = self.clickPictureEvent("huweiduiyingji.png", name="护卫队袭击", num=1)
            if state is not None:
                log.info("(ｷ｀ﾟДﾟ´)!! 被野怪袭击！！！干他！！！")
                repeat_num = 0
                self.waitMissionEnd()

            state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "到站")
            if state is not None:
                log.info("列车已经到站，请下车！！")
                return
                
            repeat_num += 1
            if repeat_num >=num:
                state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "自动巡航")
                if state is None:
                    log.info("意外，退出自动巡航的状态")
                    return
                repeat_num = 0
                
    def fightFloatTree(self, funm=0):
        if funm:
            log.info("混响浮标战斗次数：{}".format(funm))
        else:
            log.info("混响浮标持续战斗..........")
        repeat_count = 0
        while(True):  
            time.sleep(1)
            self.takeTabShoot()
            state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "开始作战")
            if state is not None:
                self.adb_obj.clickPosition(state[1])
                time.sleep(2)
            self.waitMissionEnd()
            repeat_count += 1
            log.info("混响浮标第{}次战斗结束。".format(repeat_count))
            time.sleep(3)
            if repeat_count == funm:
                break
        
    def strengthLess(self):
        state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "澄明度不足")
        if state is None:
            log.error("澄明度充足，出现了误报")
            return
        log.info("澄明度不足,将补充一次...")
        state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "确认")
        if state is None:
            pass
        # 先尝试棒棒糖
        pass
    
    def stepToCity(self):
        # 通过图标进入城市
        self.takeTabShoot()
        state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "到站")
        if state is None:
            return 
        self.takeTabShoot()
        state = self.clickPictureEvent("jinruzhandian.png", name="进入站点")
        time.sleep(3)
        self.takeTabShoot()
        state = self.clickPictureEvent("fangwenchengshi.png", name="访问城市")
        # assert self.tmpcityDes != ""
        log.info("进入城市：【{}】".format(self.tmpcityDes))
        
                
    def waitMissionEnd(self,num=5):
        # self.clickPictureEvent("zuozhan.png", "作战")
        ffight = False
        log.info("开始作战！！！")
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
                log.info("出现意外退出循环")   
                break
        log.info("作战结束")
                    

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