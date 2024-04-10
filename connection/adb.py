'''
Author: Achetair
Date: 2024-03-08 22:12:54
LastEditors: Achetair
LastEditTime: 2024-04-09 22:48:42
Description: 
'''
#-*- config:utf-8 -*-
# python 3.11

from subprocess import DEVNULL, run, Popen
import os

class ADB():
    def __init__(self, ip="127.0.0.1", port="16384", adb_path="adb.exe") -> None:
        self.module_name = "adb"
        self.ip_addr = "{}:{}".format(ip, port)
        self.adb_path = adb_path
        self.screenshoot_path = None
        
        # 创建连接
        msg = self.__connect()
        # print(msg)
        
    '''
    description: 
    param {*} store_path
    return 截图的名字
    '''
    def setScreenShoot(self, store_path)->str:
        # 返回
        assert os.path.exists(store_path)
        self.screenshoot_path = os.path.join(store_path, self.module_name+"tabshoot.png")
        return self.screenshoot_path
    
    def setModuleName(self, module_name):
        self.module_name = module_name
        
    # 获取分辨率
    def getScreenSize(self):
        shell_cmd = [self.adb_path, "shell ", "wm", "size"]
        result = run(shell_cmd,capture_output=True, text=True)
        output = result.stdout.strip()
        resolution_str = output.split()[-1]  # 获取分辨率信息
        width_str, height_str = resolution_str.split('x')  # 分割长和宽
        width = int(width_str)
        height = int(height_str)
        return width, height
        
    def __connect(self):
        shell_cmd = [self.adb_path, "connect", self.ip_addr]
        # print(shell_cmd)
        result = run(shell_cmd, shell=True, capture_output=True)
        return result.stdout
    
    def reconnect(self):
        shell_cmd = [self.adb_path, "connect", self.ip_addr]
        # print(shell_cmd)
        result = run(shell_cmd, shell=True, capture_output=True)
        return result.stdout        
    
    def disconnect(self):
        shell = [self.adb_path, "kill-server"]
        run(shell, shell=True, stdout=DEVNULL)
        
    def takeScreenShoot(self):
        assert self.screenshoot_path is not None
        shell_cmd = [self.adb_path, "-s", self.ip_addr, "exec-out", "screencap", "-p", ">", self.screenshoot_path]
        # print(" ".join(shell_cmd))
        takeShootrun = Popen(shell_cmd, shell=True)
        takeShootrun.wait()
        # print("模拟器 截图完成")
        
    def clickPosition(self, point=(0,0), off=(0,0)):
        x = point[0] + off[0]
        y = point[1] + off[1]
        
        # 点击坐标
        shell_cmd = [self.adb_path, "-s", self.ip_addr, "shell", "input", "tap", str(x), str(y)]
        # print(" ".join(shell_cmd))
        # log.info()
        run(shell_cmd, shell=True) 
    
    # 从结束移动到开始
    def swipePosition(self, srcpoint=(0,0), dstpoint=(0,0), time:int=100):
        shell_cmd = [self.adb_path, "-s", self.ip_addr, "shell", "input", "swipe", str(srcpoint[0]), str(srcpoint[1]), str(dstpoint[0]), str(dstpoint[1]), str(int(time))]
        # print(" ".join(shell_cmd))
        run(shell_cmd, shell=True) 
        
        

if __name__ == "__main__":
    A = ADB()
    shoot_dir = "../tmp"
    shoot_path = A.setScreenShoot(shoot_dir)
    A.takeScreenShoot()