#-*- config:utf-8 -*-
# python 3.11
import os

from .UserLog import obj_log as log

def makedirs(dir_path:str):
    if not os.path.exists(dir_path):
        # 创建目录及其所有子目录
        os.makedirs(dir_path)
    else:
        log.error("目录:{} 已存在".format(dir_path))