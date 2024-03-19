'''
Author: Achetair
Date: 2024-03-03 17:03:45
LastEditors: Achetair
Description: 
'''
#-*- config:utf-8 -*-
# python 3.11
import os
import sys
from resotools.utils.UserLog import obj_log as log
import threading
import ctypes
import inspect
import time
import gc
import datetime
import shutil
import re

def async_raise(tid, exctype):
   """raises the exception, performs cleanup if needed"""
   tid = ctypes.c_long(tid)
   if not inspect.isclass(exctype):
      exctype = type(exctype)
   res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
   if res == 0:
      raise ValueError("invalid thread id")
   elif res != 1:
      # """if it returns a number greater than one, you're in trouble,  
      # and you should call it again with exc=NULL to revert the effect"""  
      ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
      raise SystemError("PyThreadState_SetAsyncExc failed")
      
def stop_thread(thread):
   async_raise(thread.ident, SystemExit)
   
def copy_and_rename_file(original_filename, new_filename):
    shutil.copyfile(original_filename, new_filename)
   
def dropfixFileName(filep, fix="_cropped"):
    # 分割文件名和扩展名
    filename, extension = os.path.splitext(filep)
    # 构造新的文件名
    new_filename = filename + fix + extension
    # 重命名文件
    # os.rename(filep, new_filename)
    return new_filename    

def getTextNumber(text):
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', text)
    try:
        ret_num = int(numbers[-1])
        return ret_num
    except Exception as e:
        log.error("触发匹配失败：{}".format(text))
        return 500
    
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def distance_from_origin(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5
    
    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def clamp_x(self, min_value=0, max_value=1920):
        self.x= max(min(self.x, max_value), min_value)
        
    def __str__(self) -> str:
        return "({},{})".format(self.x, self.y)
    
    def clamp_y(self, min_value=0, max_value=1080):
        self.y = max(min(self.y , max_value), min_value) 
    
    def clamp(self):
        self.clamp_x()
        self.clamp_y()
      
    def tuple(self):
        return (self.x, self.y)

class threadsManager():
    def __init__(self) -> None:
        self.threadsinfo = {}
    
    def startNewThread(self, func, recordName, *args):
        newThread = threading.Thread(
            target=func, args=args
        )
        self.threadsinfo[recordName] = newThread
        newThread.daemon = True
        newThread.start()
        
        
    def killThreads(self):
        for k,v in self.threadsinfo.items():
            stop_thread(v)
            log.info("终止进程 {} ".format(k))
            
    def killTthread(self, rname):
        stop_thread(self.threadsinfo[rname])
        log.info("终止进程 {} ".format(rname))


def makedirs(dir_path:str):
    if not os.path.exists(dir_path):
        # 创建目录及其所有子目录
        os.makedirs(dir_path)
    else:
        log.error("目录:{} 已存在".format(dir_path))
        
if __name__ == "__main__":
    text = r'剩余行程：90km'
    getTextNumber(text)