#-*- config:utf-8 -*-
# python 3.11
import os
import sys
from .UserLog import obj_log as log
import threading
import ctypes
import inspect
import time
import gc
import datetime

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
        async_raise(self.threadsinfo[rname])
        log.info("终止进程 {} ".format(rname))


def makedirs(dir_path:str):
    if not os.path.exists(dir_path):
        # 创建目录及其所有子目录
        os.makedirs(dir_path)
    else:
        log.error("目录:{} 已存在".format(dir_path))