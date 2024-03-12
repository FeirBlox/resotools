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
    A = ResoadbObj()
    A.setAdbInfo("127.0.0.1", "16384", os.path.join(os.getcwd(),"connection/adb.exe"), "tmp" )
    A.dispatchOcrCenter()
    # A.takeTabShoot()
    # rrr = A.ocr.ocr_characters(A.adb_obj.screenshoot_path, "下一步")
    # A.adb_obj.clickPosition(rrr[1])
    # print(rrr)