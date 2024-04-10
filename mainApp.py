'''
Author: Achetair
Date: 2024-03-01 22:18:25
LastEditors: Achetair
Description: 
'''
#-*- config:utf-8 -*-
# python 3.11

import sys
import os

from sympy import EX

from game.ResoActivity import ResoActivity0322
sys.path.append(os.path.dirname(os.getcwd()))

import subprocess
import time
import pywinctl as pwc 
import pyautogui 
import cv2 as cv

from utils.UserLog import obj_log as log
from utils.CommonUtils import *
from utils.GameExceptions import *
from utils.cvTools import *

from game.ResoGoodsCal import staticResoGoodCal
from game.ResoGame import ResoadbObj

DATA_TMP_DIR = "tmp"

def systemInit():
    # 创建相关的文件夹
    makedirs(DATA_TMP_DIR)
    

# 获取最上面的窗体信息
def getFrontWindowInfo():
    return pwc.getActiveWindow()


if __name__ == "__main__":
    systemInit()
    # print(os.getcwd())
    
    # global staticResoGoodCal
    


    self = ResoadbObj()
    self.setAdbInfo("127.0.0.1", "16384", os.path.join(os.getcwd(),"connection/adb.exe"), "tmp" )
    # self.takeTestTabShoot("mairujiaoyi2.png")
    # self.takeTabShoot()
    
    # 当前城市
    self.tmpcityDes = "阿妮塔能源研究所"
    # staticResoGoodCal.store_time = getNowTime()
    # staticResoGoodCal.updateInfo()
    # self.tmpbestRunningRoute = staticResoGoodCal.cityGoodsProfitCal()
    # buyinfo = self.tmpbestRunningRoute[1].get(self.tmpcityDes)
    # products = buyinfo[0]
    # book_num = buyinfo[1]
    # self.buyandsell(buyinfo, 1|2)
    # self._buy(products, book_num)
    self.autoRunningBusiness(2)

    
    
     
    
    
            

    