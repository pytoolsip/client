# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-04-19 11:59:45
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 01:09:34
import sys,os;
from imp import reload;
# 设置默认编码格式
if hasattr(sys, "setdefaultencoding"):
	reload(sys);
	sys.setdefaultencoding('utf-8');

from common._load import Loader;
from launcher._load import LauncherLoader;

# 初始化窗口加载器
Loader = Loader(os.getcwd());
Loader.loadGlobalInfo();
Loader.verifyDefaultData();
WindowLoader = Loader.getWindowLoader();

# 创建工程窗口
def createWindow():
	WindowLoader.createWindows(); # 创建窗口
	WindowLoader.initWindowMethods(); # 初始化窗口函数
	WindowLoader.initWindowEvent(); # 初始化窗口事件
	WindowLoader.createViews(); # 创建视图

# 运行工程窗口
def runWindow():
	WindowLoader.runWindows(); # 运行窗口

if __name__ == '__main__':
	# 加载启动窗口
	LauncherLoader = LauncherLoader();
	LauncherLoader.load(createWindow, runWindow);
	# 运行App
	WindowLoader.runApp();