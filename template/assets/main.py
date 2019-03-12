# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-10-08 20:56:43
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2018-12-02 12:21:10

import os;

from common._load import Loader;
from MainWindowLoader import MainWindowLoader;

if __name__ == '__main__':
	Loader = Loader(os.getcwd());
	Loader.loadGlobalInfo();
	WindowLoader = MainWindowLoader(); # Loader.getWindowLoader();
	WindowLoader.createWindows(); # 创建窗口
	WindowLoader.initWindowMethods(); # 初始化窗口函数
	WindowLoader.initWindowEvent(); # 初始化窗口事件
	WindowLoader.createViews(); # 创建视图
	WindowLoader.runWindows();