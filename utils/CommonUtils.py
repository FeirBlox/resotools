'''
Author: Achetair
Date: 2024-03-03 17:03:45
LastEditors: Achetair
Description: 
'''
#-*- config:utf-8 -*-
# python 3.11
import os
import stat
import sys
from resotools.utils.UserLog import obj_log as log
import threading
import ctypes
import inspect
import time
import json
import datetime
import shutil
import re
from collections import Counter

def getPhraseRepchar(phraselist:list)->dict:
    ret_info = {}
    # 计算每个短语的代表字
    representative_chars = []
    for phrase in phraselist:
        # 统计短语中每个字的出现频率
        char_count = Counter(phrase)
        # 选择出现频率最高的字作为代表字
        representative_char = char_count.most_common(1)[0][0]
        representative_chars.append(representative_char)
        
        ret_info[representative_char] = phrase
    return ret_info

def getNowTime():
    return time.time()

def getNowTimeFormat(format="%Y-%m-%d %H:%M:%S", offhours=0):
    # 获取当前时间
    current_time = datetime.datetime.now()
    time_difference = datetime.timedelta(hours=offhours)
    new_time = current_time + time_difference
    # 将时间格式化为年月日时分秒格式
    formatted_time = new_time.strftime(format)    
    return formatted_time
    

def load_json(file_path):
    """
    加载JSON文件

    Parameters:
        file_path (str): JSON文件的路径

    Returns:
        dict: 包含文件内容的字典对象
    """
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data

def save_as_json(data, file_path):
    """
    将数据保存为JSON文件

    Parameters:
        data (dict): 要保存的数据，必须是一个字典类型
        file_path (str): JSON文件的路径

    Returns:
        None
    """
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)

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
    try:
        async_raise(thread.ident, SystemExit)
    except ValueError:
        # log.debug()
        return 
   
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
        self.white_list = []
        
        self.timeThreadInfo = {}
        
    def __checkOtherThread(self):
        for k,v in self.threadsinfo.items():
            if k not in self.white_list:
                self.killTthread(k)
                
    def startNewTimeThread(self, tn, func, recordName, *args):
        # self.__checkOtherThread()
        newThread = threading.Timer(tn, func, args=args)
        self.timeThreadInfo[recordName] = newThread
        newThread.daemon = True
        newThread.start()        
    
    def startNewThread(self, func, recordName, *args):
        self.__checkOtherThread()
        newThread = threading.Thread(
            target=func, args=args
        )
        self.threadsinfo[recordName] = newThread
        newThread.daemon = True
        newThread.start()
        
    def setWhiteList(self, name):
        if name not in self.white_list:
            self.white_list.append(name)
                    
    def killThreads(self):
        for k,v in self.threadsinfo.items():
            stop_thread(v)
            log.info("终止进程 {} ".format(k))
            
    def killTthread(self, rname):
        stateth = self.threadsinfo.get(rname)
        if stateth is None:
            # 在其他进程已经被杀死
            return False        
        if stateth.is_alive():
            stop_thread(self.threadsinfo[rname])
            log.info("终止进程 {} ".format(rname))
            return True
        else:
            return False

def makedirs(dir_path:str):
    if not os.path.exists(dir_path):
        # 创建目录及其所有子目录
        os.makedirs(dir_path)
    else:
        log.error("目录:{} 已存在".format(dir_path))
        
if __name__ == "__main__":
    text = r'剩余行程：90km'
    getTextNumber(text)