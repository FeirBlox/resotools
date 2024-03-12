'''
Author: Achetair
Date: 2024-03-03 17:25:58
LastEditors: Achetair
LastEditTime: 2024-03-11 22:51:24
Description: 
'''
#-*- config:utf-8 -*-
# python 3.11

import imp
import pyautogui 
import cv2 as cv
from resotools.utils.UserLog import obj_log as log
from resotools.utils.GameExceptions import *

def getCurMousePosition():
    currentMouseX, currentMouseY = pyautogui.position() 
    log.info("鼠标位置：x={}, y={}".format(currentMouseX, currentMouseY))

def cvLocatPng(allscreen, tpng):
    # log.info("在 {} 中 定位 {}".format(allscreen, tpng))
    srcimg = cv.imread(allscreen)
    srcimgray = cv.cvtColor(srcimg, cv.COLOR_BGR2RGB)
    timg = cv.imread(tpng)
    timgray = cv.cvtColor(timg, cv.COLOR_BGR2RGB)
    
    # sift = cv.SIFT()
    # result = cv.xfeatures2d.SIFT_create(srcimg, srcimg, cv.TM_CCORR_NORMED)
    result = cv.matchTemplate(srcimgray, timgray, cv.TM_CCORR_NORMED)
    
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    # print(max_val)
    if max_val < 0.98:
        raise ChromeLocatePngNotFound
    log.debug("min_val={}, max_val={}, min_loc={}, max_loc={}".format(min_val, max_val, min_loc, max_loc))
    
    # 如果匹配上了，返回图片的位置
    # show img
    # (startX, startY) = max_loc
    # endX = startX + timg.shape[1]
    # endY = startY + timg.shape[0]
    # cv.rectangle(srcimg, (startX, startY), (endX, endY), (255, 0, 0), 3)
    # cv.imshow("output", srcimg)
    # cv.waitKey(0)
    # exit(1)
    return (max_loc[0] + timg.shape[1]/2, max_loc[1] + timg.shape[0]/2)
    
    # return result