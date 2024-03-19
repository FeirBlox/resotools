<!--
 * @Author: Achetair
 * @Date: 2024-03-11 22:12:32
 * @LastEditors: Achetair
 * @LastEditTime: 2024-03-20 00:13:42
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

- [x] 自动巡航（虽然官方出了，但是感觉好贵）

- [x] 混响信标：把车子开到树下面，到挑战页面，体力准备好，就可以挂机了

- [x] 自动铁安局

- [ ] 自动跑商:基本已经实现了，还有一些不稳定的小bug，目前需要手动设置始发地和目的地，然后就可以放任循环了

# 运行截图

![](readme/runningui.png)


# 打包

nuitka --mingw64 --windows-disable-console --standalone --enable-plugin=tk-inter mainApp.py

nuitka --mingw64 --windows-disable-console --enable-plugin=tk-inter ResoToolsUI.py