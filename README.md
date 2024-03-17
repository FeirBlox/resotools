<!--
 * @Author: Achetair
 * @Date: 2024-03-11 22:12:32
 * @LastEditors: Achetair
 * @LastEditTime: 2024-03-15 01:40:21
 * @Description: 
-->
# resotools
 
雷索纳斯游戏小助手，禁止商用，自用脚本。

# 部署环境

* python 3.11.8
* 在python的环境的Lib\site-packages下面添加mypath.pth，并写入项目的父目录(运行不需要，改功能需要)
* 安装相关依赖 
* 运行 <code>python mainApp.py</code>

# 更新计划

* 随缘

# 打包

nuitka --mingw64 --windows-disable-console --standalone --enable-plugin=tk-inter mainApp.py

nuitka --mingw64 --windows-disable-console --enable-plugin=tk-inter ResoToolsUI.py