# -*- coding:utf-8 -*-
# python 3.7
'''
Author: achetair
Date: 2021-06-12 17:00:14
LastEditTime: 2021-06-12 17:21:39
Description: Do not edit
'''
import os
import re
import sys
import time
from loguru import logger


MAX_KB = 3 * 1024 * 1024 # 3MB
VERSION = "v1.0.0"
LOG_DIR = "logs"

message = ""

class FileFilter:
    def __init__(self, file):
        self.file = file

    def __call__(self, record):
        return record["extra"].get("file") == self.file

obj_path_log = os.path.join(LOG_DIR, 'resotoolss.log')
obj_log = logger.bind(file=obj_path_log)
obj_log.add(obj_path_log,
            format="{time:HH:mm:ss} - "
                    "{level}\t| "
                    "{module}.{function}:{line} - "+f"<cyan>{VERSION}</cyan> - "+" {message}",
            rotation="1 days", enqueue=True, serialize=False, encoding="utf-8", retention="10 days",filter=FileFilter(obj_path_log))

# 自定义日志记录
class Userlog:
    def __init__(self, projectname: "str", isCreate=False):
        # 初始化一些变量
        self.num = 0
        self.root = "./log/"
        self.proname = projectname
        self.init()

        # 配置一些基本的变量
        self.log_name = self._getLogFileName()
         # 日志的名称和路径
        #  创建相关的文件夹
        self.checkPathExist(self.log_name, isCreate=False)

        try:
            self.log = open(self.log_name, "a", encoding="utf-8")
        except Exception() as e:
            print(e)
            exit(1)

    def _getLogFileName(self):
        return self.root + self.proname + "_" + str(self.num) + ".log"


    # 检测路径的同时，顺便将文件也创建了
    def checkPathExist(self, file_path, isCreate=False):
        # 如果路径存在就不再进行检测了
        if os.path.exists(file_path):
            return True

        # 检测文件是否存在，并循环创建父级目录
        if os.path.isdir(file_path):
            os.makedirs(file_path)
            return True
        else:
            # 文件的话需要先获取父级目录
            parent_dir = os.path.dirname(file_path)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
            if isCreate:
                f = open(file_path, "wb")
                f.close()
                return True
            else:
                return False

    # 检测日志的目录，获取日志的数量
    def init(self):
        self.checkPathExist(self.root)
        files = os.listdir(self.root)
        # 计算已有日志文件的数目
        self.num = 0
        for f in files:
            if f[0 : len(self.proname)] == self.proname:
                self.num += 1
        # self.num = len(files)
        if self.num != 0:
            self.num = self.num - 1

    def __file_split(self):
        max_kb = MAX_KB
        # 获取文件的大小
        self.log.flush()
        size = os.path.getsize(self.log_name)
        if size > max_kb:
            # 关闭之前的文件，开启新的文件
            self.log.close()
            self.log = None
            # 开启新的日志文件
            self.num = self.num + 1
            self.log_name = self._getLogFileName()
            self.log = open(self.log_name, "a", encoding="utf-8")

    # 获取目前的时间
    def Gtime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 完整日期，时间，星期，时区

    # 对打印的日志信息进行分类
    def info(self, msg, *args):
        self.__file_split()
        msg = str(msg)
        if args:
            msg += " "
            msg += " ".join([str(x) for x in args])
        self.log.write(
            self.Gtime()
            + " INFO : "
            + msg.encode("utf-8", "ignore").decode("utf-8", "ignore")
            + "\n"
        )

    def debug(self, msg, *args):
        self.__file_split()
        msg = str(msg)
        if args:
            msg += " "
            msg += " ".join([str(x) for x in args])

        self.log.write(
            self.Gtime()
            + " DEBUG : "
            + msg.encode("utf-8", "ignore").decode("utf-8", "ignore")
            + "\n"
        )

    def warning(self, msg, *args):
        self.__file_split()
        msg = str(msg)
        if args:
            msg += " "
            msg += " ".join([str(x) for x in args])
        self.log.write(
            self.Gtime()
            + " WARNING : "
            + msg.encode("utf-8", "ignore").decode("utf-8", "ignore")
            + "\n"
        )

    def error(self, msg, isExit=True, *args):
        self.__file_split()
        msg = str(msg)
        if args:
            msg += " "
            msg += " ".join([str(x) for x in args])
        self.log.write(
            self.Gtime()
            + " ERROR : "
            + msg.encode("utf-8", "ignore").decode("utf-8", "ignore")
            + "\n"
        )
        # 出现错误的日志，程序必须终止
        if isExit:
            exit(1)
