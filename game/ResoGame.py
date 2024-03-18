'''
Author: Achetair
Date: 2024-03-08 23:46:19
LastEditors: Achetair
Description: 
'''
#-*- config:utf-8 -*-
# python 3.11

import time
import datetime
from tkinter import NO
import numpy as np
from cnocr import CnOcr

from resotools.game.ABSObj import *
from resotools.utils.cvTools import *
from resotools.utils.ocrtools import Ocr_tools


class ResoObj(ABSobj):
    def __init__(self, title="MuMu模拟器12") -> None:
        super().__init__(title)
        self.moudle_name = "ResoObj"
        self.store_pic_path = "pngdata/leisuonasi"
    
    # 点击下一步    
    def clickPictureEvent(self, picname, name=""):
        count = 0
        pPoints = None
        while(1):
            self.takeTabShoot()
            pPoints = self.locateTpicture(picname)
            if pPoints is None:
                count += 1
                time.sleep(3)
                continue
            break
        assert pPoints is not None
        if name == "":
            log.info("检测到【{}】 在 {}, 执行点击".format(picname, pPoints))
        else:
            log.info("检测到【{}】 在 {}, 执行点击".format(name, pPoints))
        pyautogui.leftClick(pPoints[0], pPoints[1])
        
    def dragWindow(self, picname, name=""):
        count = 0
        pPoints = None
        while(1):
            self.takeTabShoot()
            pPoints = self.locateTpicture(picname)
            if pPoints is None:
                count += 1
                time.sleep(3)
                continue
            break
        assert pPoints is not None
        if name == "":
            log.info("检测到【{}】 在 {}, 执行鼠标移动".format(picname, pPoints))
        else:
            log.info("检测到【{}】 在 {}, 执行鼠标移动".format(name, pPoints))
            
        pyautogui.moveTo(pPoints[0], pPoints[1]-20)
        # 执行鼠标拖拽向右
        # pyautogui.mouseDown(button="left")
        # pyautogui.moveTo(pPoints[0]+100, pPoints[1], duration=2)
        # pyautogui.mouseUp(button="left")
        pyautogui.dragTo(pPoints[0]+200, pPoints[1]-20, duration=1, button="left")
        
                
    def reapteTaojin(self):
        repeat_count = 0
        # 检测游戏是否结束
        while(True):
            self.takeTabShoot()
            endp = self.locateTpicture("xiayibu.png")
            if endp is None:
                log.info("游戏还没有结束请等待......")
                time.sleep(10)
                repeat_count += 1
                if repeat_count % 4 == 0:
                    pyautogui.leftClick(self.center_pos[0], self.center_pos[1])
                continue
            repeat_count = 0
            break
        
        self.clickPictureEvent("xiayibu.png", name="下一步")
        while(True):
            self.dragWindow("anquanweituo4.png")
            mission_3_point = self.locateTpicture("3.png")
            if mission_3_point is None:
                continue
            break
        self.clickPictureEvent("3.png", "任务3")
        time.sleep(1)
        self.clickPictureEvent("zuozhan.png", "作战")
        time.sleep(3)
        self.clickPictureEvent("kaishizuozhan.png", "开始作战")
        return 1
    
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
        }
        self.gameFlag = {
            "自动战斗":False,
        }
        self.__gameFlagRefresh()
        
        self.text_funcaction_dict = {
            "进入游戏":"click",
            "自动巡航":self.autoCruise,
            "下一步":"click",
        }
        self.img_funcact_dict={
            "fighting.png":self.waitMissionEnd,
            "huweiduiyingji.png":self.autoCruise,
            "fighting.png":self.waitMissionEnd,
        }       
        
        # 一些类的信息
        self.city_list = ["曼德矿场","阿妮塔能源研究所"]
        self.tmpcityDes = "" # 临时城市目的地
    
    def __gameFlagRefresh(self):
        for k,v in self.pos_data.items():
            # if k in self.gameFlag:
            #     continue
            # else:
            #     self.gameFlag[k] = False
            self.gameFlag[k] = False
                 
    def autoDetectExcute(self):
        # 持续性对界面进行文字识别
        repeat_num = 0
        while(True):
            self.takeTabShoot()
            ocrinfos = self.ocr.ocr_img(self.adb_obj.screenshoot_path)
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
                    
    def autoRunningBusiness(self, city1, city2):
        pass
    
    # 自动巡航   
    def autoCruise(self, num=5):
        # 自动巡航的状态
        log.info("列车进入自动巡航的状态！")
        repeat_num = 0 
        isDisCertain = False
        distance = 1000
        destination = ""
         
        while(True):
            self.takeTabShoot()
            time.sleep(1)
            
            # 获取剩余里程，目的地
            state = self.ocr.ocr_mutitext(self.adb_obj.screenshoot_path, ["剩余行程", "目的地"])

            if state is not None:
                if state.get("剩余行程") is not None:
                    tmpdis = state["剩余行程"]["text"]
                    tdis = getTextNumber(tmpdis)
                    distance = min(tdis, distance)
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
                    if distance >= 50:
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

            state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "列车已经到站")
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
        state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "列车已经到站")
        if state is None:
            return 
        state = self.clickPictureEvent("jinruzhandian.png", name="进入站点")
        time.sleep(4)
        state = self.clickPictureEvent("fangwenchengshi.png", name="访问城市")
        # assert self.tmpcityDes != ""
        log.info("进入城市：【{}】".format(self.tmpcityDes))
        
                
    def waitMissionEnd(self,num=5):
        # self.clickPictureEvent("zuozhan.png", "作战")
        ffight = False
        log.info("开始作战！！！")
        repeat_count = 0
        while(True):
            time.sleep(1)
            self.takeTabShoot()
            if not ffight:
                state = self.clickPictureEvent("kaishizuozhan.png", "开始作战", num=2)
                ffight = True
                time.sleep(8)
                
            state = self.locateTpicture("fighting.png")
            if state is not None:
                # 检测自动战斗是否开启
                if not self.gameFlag["自动战斗"]:
                    # self.locateTpicture("autofighttagwhite.png")
                    cutfile = self.cutPartPic(self.pos_data["自动战斗"])
                    # 检测灰度
                    color = detect_color(cutfile)
                    if color == "grey":
                        self.adb_obj.clickPosition(calcenterpos(self.pos_data["自动战斗"]))
                    log.info("自动战斗已经开启")
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
                    
    def dispatchImgCenter(self):
        gameStates = self.img_funcact_dict.keys()
        for gs in gameStates:
            dPos = self.locateTpicture(gs)
            if dPos is None:
                continue
            else:
                # 进入对应的状态
                self.img_funcact_dict[gs]()
    
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