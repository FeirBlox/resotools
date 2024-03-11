'''
Author: Achetair
Date: 2024-03-08 23:46:19
LastEditors: Achetair
Description: 
'''
#-*- config:utf-8 -*-
# python 3.11


import stat
import time
from tkinter import NO
import numpy as np
from cnocr import CnOcr

from resotools.game.ABSObj import*

MODEL_ROOT = "D:/work/resotools"

class Ocr_tools():
    def __init__(self,det_model_name="ch_PP-OCRv3_det", rec_model_name= "densenet_lite_114-fc", det_root="model/cnstd", rec_root="model/cnocr", number=False, start=True) -> None:
        det_root, rec_root = os.path.join(MODEL_ROOT, det_root), os.path.join(MODEL_ROOT, rec_root)
        
        print("det_root: {}, rec_root:{}".format(det_root, rec_root))
        rec_vocab_path = os.path.join(MODEL_ROOT, "model/cnocr/label_cn.txt")
        self.ocr = CnOcr(det_model_name=det_model_name, rec_model_name=rec_model_name, rec_vocab_fp=rec_vocab_path, det_root=det_root, rec_root=rec_root) 
        self.number_ocr = CnOcr(det_model_name=det_model_name, rec_model_name="en_number_mobile_v2.0", det_root=det_root, rec_root=rec_root, cand_alphabet='0123456789.+%')
        
    def ocr_characters(self, img_path, charac):
        ocr_list = self.ocr.ocr(img_path)
        for vd in ocr_list:
            msg = vd["text"]
            if charac in msg:
                return (msg, self.ocr_center_pos(vd["position"]))
        return None
    
    def ocr_img(self, img_path):
        return self.ocr.ocr(img_path)
    
    def ocr_center_pos(self, ocr_array):
        position = np.mean(ocr_array, axis=0)
        return position.tolist()



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
        self.text_funcaction_dict = {
            "进入游戏":"click",
            "自动巡航":self.zidongxunhang,
            "下一步":"click",
        }
        self.img_funcact_dict={
            "fighting.png":self.waitMissionEnd,
            
        }
                 
    def dispatchOcrCenter(self):
        # 持续性对界面进行文字识别
        while(True):
            self.takeTabShoot()
            ocrinfos = self.ocr.ocr_img(self.adb_obj.screenshoot_path)
            findinfos = self.findKeyWord(ocrinfos)
            if findinfos is None:
                self.dispatchImgCenter()
                log.info("没有找到关键字，休息。。。。。")
                time.sleep(5)
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
                    
    def zidongxunhang(self, num=5):
        # 自动巡航的状态
        log.info("列车进入自动巡航的状态！")
        repeat_num = 0
        while(True):
            self.takeTabShoot()
            
            # 检测弹丸加速
            state = self.clickPictureEvent("jiasudanwan.png", name="加速弹丸", num=2)
            if state is None:
                # log.info("没有检测到加速弹丸，可能会发生遇袭事件")
                log.info("亲，列车正在加速中~~~~~~~~")
            else:
                repeat_num = 0
                state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "列车已经到站")
                if state is not None:
                    log.info("列车已经到站，请下车！！")
                    return
                continue
            
            state = self.clickPictureEvent("huweiduiyingji.png", name="护卫队袭击", num=1)
            if state is not None:
                repeat_num = 0
                log.info("(ｷ｀ﾟДﾟ´)!! 被野怪袭击！！！干他！！！")
                self.waitMissionEnd()
            repeat_num += 1
            if repeat_num >=num:
                state = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "自动巡航")
                if state is None:
                    log.info("意外，退出自动巡航的状态")
                    return
                repeat_num = 0
                
    def waitMissionEnd(self):
        # self.clickPictureEvent("zuozhan.png", "作战")
        log.info("开始作战！！！")
        for i in range(2):
            state = self.clickPictureEvent("kaishizuozhan.png", "开始作战", num=3)
            time.sleep(2)
            if state is not None:
                time.sleep(7)
                break
        repeat_count = 0
        while(True):
            self.takeTabShoot()
            state = self.locateTpicture("fighting.png")
            if state is not None:
                log.info("游戏还没有结束请等待......")
                time.sleep(10)
                repeat_count += 1
                continue
            
            break
        endp = self.ocr.ocr_characters(self.adb_obj.screenshoot_path, "下一步")
        if endp is not None:
            repeat_count = 0
            log.info("检测到[{}], 点击{}".format(endp[0], endp[1]))
            self.adb_obj.clickPosition(endp[1])       
        else:
            log.info("出现意外退出循环")     
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
    A.setAdbInfo("127.0.0.1", "16384", "D:/work/resotools/connection/adb.exe", "D:/work/resotools/tmp" )
    A.dispatchOcrCenter()
    # A.locateTpicture("zidongxunhang.png")
    # print(A.locateTpicture.__name__)
    # A.takeTestTabShoot("xiaohongdian.png")
    # A.gotoMission()
    # img_path = "D:/work/resotools/tmp/test-ResoadbObj/kaishijiemian.png"
    # B = Ocr_tools()
    # # rrr = B.ocr.ocr(img_path)
    # rrr = B.ocr_characters(img_path, "进入游戏")
    # print(rrr)