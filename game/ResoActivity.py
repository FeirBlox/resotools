'''
Author: Achetair
Date: 2024-03-22 23:33:25
LastEditors: Achetair
Description: 
'''

from resotools.utils.CommonUtils import *
from resotools.game.ResoGame import ResoadbObj
from resotools.utils.UserLog import obj_log as log

# 红茶战争相关的脚本
class ResoActivity0322(ResoadbObj):
    def __init__(self, title="MuMu模拟器12") -> None:
        super().__init__(title)
        
        self.moudle_name = "ResoActivity"
        
        self._blacktea_data = ["混厄石芝"]
        
        
    def blackteaAct(self, mission_name, num=0):
        assert mission_name in self._blacktea_data
        count = 1
        # 检索目标
        while(True):
            state = self._ocr_tabshoot(mission_name)
            if state is None:
                count = count + 1
                continue
            pos = Point(*state[1])
            pos.y += 50
            self.adb_obj.clickPosition(pos.tuple())
            time.sleep(1)
            self.waitMissionEnd()
            
            count = count + 1
            if count > 100:
                break
        
    def activityRun(self):
        self.blackteaAct("混厄石芝")
        
        
        
    
