# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-04-19 11:59:45
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-10 20:17:24
import sys,os;
# 当前文件位置
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));
# 添加搜索路径
if CURRENT_PATH not in sys.path:
	sys.path.append(CURRENT_PATH);

# 导入加载模块
from common._load import Loader;
from launcher._load import LauncherLoader;

# 获取工程路径
pjPath = os.path.dirname(os.getcwd());
if len(sys.argv) > 1:
	pjPath = sys.argv[1];

# 初始化窗口加载器
Loader = Loader(os.getcwd(), pjPath);
Loader.loadGlobalInfo();
Loader.initGlobalClass();
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