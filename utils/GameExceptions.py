'''
Author: Achetair
Date: 2024-03-08 23:30:48
LastEditors: Achetair
LastEditTime: 2024-03-09 00:36:16
Description: 
'''
#-*- config:utf-8 -*-
# python 3.11

class WindowNotStartException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    def __str__(self) -> str:
        # log.error("Chrome not Start. The program will exit in 1s")
        exit(1)
        return super().__str__()
    
class WaitForContinue(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
class ChromeLocatePngNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
 
    