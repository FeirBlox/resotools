'''
Author: Achetair
Date: 2024-03-08 23:29:25
LastEditors: Achetair
LastEditTime: 2024-03-17 21:43:08
Description: 
'''
#-*- config:utf-8 -*-
# python 3.11
import pywinctl as pwc 
import pyautogui 
import os
import time

from resotools.utils.GameExceptions import *
from resotools.utils.CommonUtils import *
from resotools.utils.UserLog import obj_log as log
from resotools.utils.cvTools import *
from resotools.connection.adb import ADB


DATA_TMP_DIR = "tmp"
CHOME_PNG_DIR = "pngdata/chrome"

class ABSobj():
    def __init__(self, title="unknow") -> None:
        self.moudle_name = "ABSobj"
        self.store_pic_path = ""
        self.window = pwc.getWindowsWithTitle(title)
        if not self.window:
            raise WindowNotStartException("你的{}打开失败".format(title))
        self.hwndwindow = self.window[0]
        self.left = self.hwndwindow.left
        self.top = self.hwndwindow.top
        self.height = self.hwndwindow.height
        self.width = self.hwndwindow.width
        self.bottom = self.hwndwindow.bottom
        self.right = self.hwndwindow.right
        
        self.center_pos = (self.left+self.width/2, self.top+self.height/2)
        
        log.info("标题：{dtitle} 的坐标信息 left={dleft}, top={dtop}, right={dright}, bottom={dbottom}, width={dwidth}, height={dheight}".format(dtitle=title, dleft=self.left, dtop=self.top, dright=self.right, dbottom=self.bottom, dwidth=self.width, dheight=self.bottom))
        
    # 获取标签页的截图
    def takeTabShoot(self):
        tabshoot_path = os.path.join(DATA_TMP_DIR, self.moudle_name+"tabshoot.png")
        pyautogui.screenshot(tabshoot_path, region=(self.left, self.top, self.width, self.height))
    
    # 定位图片
    def locateTpicture(self, picname):
        assert self.store_pic_path != ""
        pic_path = os.path.join(self.store_pic_path, picname)
        objshoot_png = os.path.join(DATA_TMP_DIR, self.moudle_name+"tabshoot.png")
        try:
            xPoints = cvLocatPng(objshoot_png, pic_path)
        except ChromeLocatePngNotFound as e:
            log.error("图片 {} 在 图片 {} 中没有发现".format(pic_path, objshoot_png))
            return None
        
        x = xPoints[0] + self.left 
        y = xPoints[1] + self.top

        picPoints = (x, y)
        log.info("{} 的坐标：x={}, y={}".format(picname ,picPoints[0], picPoints[1])) 
        return picPoints     
    
class ABSadbObj():
    def __init__(self, title="") -> None:
        self.title = title
        self.moudle_name = "ABSadbObj"
        self.adb_path = None
        self.adb_obj = None
        self.store_pic_path = None
    
    def setAdbInfo(self, ip, port, adb_path, tmpstore_path):
        self.adb_path = adb_path
        self.adb_obj= ADB(ip, port, adb_path)
        # 设置adb的信息
        self.adb_obj.setModuleName(self.moudle_name)
        self.adb_obj.setScreenShoot(tmpstore_path)
        self.tmpstore_path = tmpstore_path
        
    def takeTabShoot(self):
        self.adb_obj.takeScreenShoot()
        
    # 快照测试用的文件    
    def takeTestTabShoot(self, nname):
        self.adb_obj.takeScreenShoot()
        tpath_dir = os.path.join(self.tmpstore_path, "test-{}".format(self.moudle_name))
        tpath = os.path.join(tpath_dir, nname)
        makedirs(tpath_dir)
        os.rename(self.adb_obj.screenshoot_path, tpath)
        
    def cutPartPic(self, shapeA, picname=""):
        crop_file_path = crop_image(shapeA, self.adb_obj.screenshoot_path)
        if picname != "":
            tmp_pth = os.path.join(self.tmpstore_path, "{}.png".format(picname))
            copy_and_rename_file(crop_file_path, tmp_pth)
            crop_file_path = tmp_pth
        return crop_file_path
        
        
    def locateTpicture(self, picname):
        assert self.store_pic_path != ""
        pic_path = os.path.join(self.store_pic_path, picname)
        objshoot_png = self.adb_obj.screenshoot_path
        # print(objshoot_png + "    " + pic_path)
        try:
            xPoints = cvLocatPng(objshoot_png, pic_path)
        except ChromeLocatePngNotFound as e:
            # log.error("图片 {} 在 图片 {} 中没有发现".format(pic_path, objshoot_png))
            return None
        
        log.debug("{} 的坐标：x={}, y={}".format(picname ,xPoints[0], xPoints[1])) 
        return xPoints
    
    '''
    description: 
    param {*} self
    param {*} picname
    param {*} name
    param {*} num:重复检测的次数
    return {*}
    '''
    def clickPictureEvent(self, picname, name="", num=3):
        pPoints = None
        for i in range(num):
            self.takeTabShoot()
            pPoints = self.locateTpicture(picname)
            if pPoints is not None:
                if name == "":
                    log.info("检测到【{}】 在 {}, 执行点击".format(picname, pPoints))
                else:
                    log.info("检测到【{}】 在 {}, 执行点击".format(name, pPoints))  
                self.adb_obj.clickPosition(pPoints) 
                return pPoints
            time.sleep(1)
        return None

        

        
                   