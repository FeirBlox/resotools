'''
Author: Achetair
Date: 2024-03-11 22:18:12
LastEditors: Achetair
LastEditTime: 2024-03-11 22:18:15
Description: 
'''

import sys
import os
import subprocess
import time
import pywinctl as pwc 
import pyautogui 
import cv2 as cv

from utils.UserLog import obj_log as log
from utils.CommonUtils import *
from utils.GameExceptions import *
from utils.cvTools import *

DATA_TMP_DIR = "tmp"
CHOME_PNG_DIR = "pngdata/chrome"

# chrome test
def createChromeWindow():
    chrome_path = '\"C:/Program Files/Google/Chrome/Application/chrome.exe\" '
    args = ["--profile-directory=\"Profile 2\""]
    command = chrome_path + " ".join(args)
    print(command)
    subobj = subprocess.Popen(command)
    return subobj


class ChomeWindowObj():
    def __init__(self, title="新标签页 - Google Chrome") -> None:
        self.moudle_name = "ChomeWindowObj"
        self.window = pwc.getWindowsWithTitle(title)
        if not self.window:
            raise WindowNotStartException("你的Chrome打开失败")
        self.hwndwindow = self.window[0]
        self.left = self.hwndwindow.left
        self.top = self.hwndwindow.top
        self.height = self.hwndwindow.height
        self.width = self.hwndwindow.width
        self.bottom = self.hwndwindow.bottom
        self.right = self.hwndwindow.right
        log.info("标题：{dtitle} 的坐标信息 left={dleft}, top={dtop}, right={dright}, bottom={dbottom}, width={dwidth}, height={dheight}".format(dtitle=title, dleft=self.left, dtop=self.top, dright=self.right, dbottom=self.bottom, dwidth=self.width, dheight=self.bottom))
        
        self.takeTabShoot()
        self.__locateGoogleBlank()
        # pyautogui.rightClick(self.right, self.top)
        
    # 获取标签页的截图
    def takeTabShoot(self):
        tabshoot_path = os.path.join(DATA_TMP_DIR, self.moudle_name+"tabshoot.png")
        pyautogui.screenshot(tabshoot_path, region=(self.left, self.top, self.width, self.height))
        
    def closeChome(self):
        pyautogui.leftClick(self.right-self.width*0.01, self.top+self.height*0.01)
    
    # 定位google的搜索栏目
    def __locateGoogleBlank(self):
        googlesearch_png = os.path.join(CHOME_PNG_DIR, "googlesearch.png")
        # googlesearch_png = "pngdata/chrome/googlesearch.png"
        # assert os.path.exists(googlesearch_png)
        # try:
        # x, y = pyautogui.locateCenterOnScreen(googlesearch_png)
        objshoot_png = os.path.join(DATA_TMP_DIR, self.moudle_name+"tabshoot.png")
        try:
            xPoints = cvLocatPng(objshoot_png, googlesearch_png)
        except ChromeLocatePngNotFound as e:
            log.error("图片 {} 在 图片 {} 中没有发现".format(googlesearch_png, objshoot_png))
            exit(1)
        # print(bbb)
        
        x = xPoints[0] + self.left + self.width/2
        y = xPoints[1] + self.top

        self.googlsearch_pos = (x, y)
        log.info("google搜索栏目的坐标：x={}, y={}".format(self.googlsearch_pos[0], self.googlsearch_pos[1]))
        # pyautogui.leftClick(self.googlsearch_pos[0], self.googlsearch_pos[1])
        
    def __clearSearchBlank(self):
        time.sleep(1)
        pyautogui.leftClick(self.googlsearch_pos[0], self.googlsearch_pos[1])
        pyautogui.hotkey("ctrl", "a")
        pyautogui.press("back")
    
    # 进入指定的网址
    def enterChromUrl(self, url:str):
        time.sleep(1)
        self.__clearSearchBlank()
        log.info("访问网址： {}".format(url))
        pyautogui.typewrite(url)
        pyautogui.press("enter", presses=2, interval=0.25)
        
