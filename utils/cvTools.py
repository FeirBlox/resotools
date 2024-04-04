'''
Author: Achetair
Date: 2024-03-03 17:25:58
LastEditors: Achetair
LastEditTime: 2024-04-04 11:10:17
Description: 
'''
#-*- config:utf-8 -*-
# python 3.11

import imp
import pyautogui 
import cv2 as cv
from resotools.utils.UserLog import obj_log as log
from resotools.utils.CommonUtils import *
from resotools.utils.GameExceptions import *
from PIL import Image

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
    log.debug("图片 {} max_val={}, max_loc={}, pngshape={}".format(tpng, max_val, max_loc, timg.shape))
    
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

def calcenterpos(shapeA:list):
    assert len(shapeA) ==  4
    x = (shapeA[0]+shapeA[2]) / 2
    y = (shapeA[1]+shapeA[3]) / 2
    return (x,y)

def cvLocatePngShape(allscreen, tpng):
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
    left = max_loc[0]
    right = max_loc[0] + timg.shape[1]
    top =  max_loc[1]
    bottom = max_loc[1] + timg.shape[0]
    return [left, top, right, bottom]
    
def maxlocToShape(maxloc, pngshape):
    left = maxloc[0]
    right = maxloc[0] + pngshape[1]
    top =  maxloc[1]
    bottom = maxloc[1] + pngshape[0]
    return [left, top, right, bottom]
    
# 裁剪图片
def crop_image(imgshape, picpath):
    assert len(imgshape)==4
    # 使用PIL库裁剪截图文件
    img = Image.open(picpath)
    # cropped_img = img.crop((left, top, right, bottom))
    cropped_img = img.crop((imgshape[0], imgshape[1], imgshape[2], imgshape[3]))
    # 裁剪后的图片保存
    cutpicName = dropfixFileName(picpath)
    cropped_img.save(cutpicName)
    return cutpicName
    # return cutpicNam
    
# 检测图片的白色与灰色
def detect_color(image_path):
    # 读取图像
    image = cv.imread(image_path)
    
    # 将图像转换为灰度图像
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    # 计算灰度图像的平均亮度值
    mean_brightness = cv.mean(gray_image)[0]
    log.debug("均度值：{}".format(mean_brightness))
    # print(mean_brightness)
    # 判断图像是白色还是灰色
    if mean_brightness > 100:  # 这里的阈值200可以根据实际情况调整
        return "white"
    else:
        return "grey"
    
if __name__ == "__main__":
    # 定位图片
    # imp_path = r"D:\work\resotools\tmp\test-ResoadbObj\daodamudidi.png"
    # timg = r"D:\work\resotools\tmp\test-ResoadbObj\danwanshuliang.png"
    # cvLocatPng(imp_path, timg)
    
    
    # 裁剪图片
    imp_path = r"D:\work\resotools\tmp\ResoadbObjtabshoot.png"
    shape_l = [1758.0, 581.0, 1810.0, 608.0]
    crop_image(shape_l,imp_path)
    
    # 计算轮廓
    # maxloc = (1588, 978)
    # pngshape=(49, 52, 3)
    # shss = maxlocToShape(maxloc, pngshape)
    # print(shss)
    