# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-10-08 20:56:43
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 23:42:01
import sys,os;
# 当前文件位置
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
# 添加搜索路径
if CURRENT_PATH not in sys.path:
	sys.path.append(CURRENT_PATH);

from common._load import Loader;
from MainWindowLoader import MainWindowLoader;

# 初始化窗口加载器
Loader = Loader(CURRENT_PATH, os.path.dirname(CURRENT_PATH));
Loader.loadGlobalInfo();
if len(sys.argv) > 1:
	Loader.updatePyPath(os.path.dirname(sys.argv[1])); # 更新python路径
Loader.lockGlobal();
Loader.verifyDefaultData();
WindowLoader = MainWindowLoader(); # Loader.getWindowLoader();

# 创建工程窗口
def createWindow():
	WindowLoader.createWindows(); # 创建窗口
	WindowLoader.initWindowMethods(); # 初始化窗口函数
	WindowLoader.initWindowEvent(); # 初始化窗口事件
	WindowLoader.createViews(); # 创建视图

# 运行工程窗口
def runWindow():
	WindowLoader.runWindows(); # 运行窗口
	WindowLoader.runApp(); # 运行App

if __name__ == '__main__':
	createWindow();
	runWindow();