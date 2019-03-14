# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-09 21:32:27
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 17:41:46

import os;
import wx;
from _Global import _GG;
from function.base import *;

class LauncherLoader(object):
	def __init__(self):
		super(LauncherLoader, self).__init__();
		self.className_ = LauncherLoader.__name__;
		self.curPath = _GG("g_AssetsPath") + "launcher/";
		self.createFunc = None;
		self.runFunc = None;

	def load(self, createFunc, runFunc):
		self.createFunc = createFunc;
		self.runFunc = runFunc;
		self.createWindow();
		self.runWindow();
		self.launch();

	def createWindow(self):
		self.windowCtr = CreateCtr(self.curPath + "window/LauncherWindow", None);

	def runWindow(self):
		self.windowCtr.getUI().Centre();
		self.windowCtr.getUI().Show(True);

	def closeWindow(self):
		self.windowCtr.getUI().Close(True);

	def launch(self):
		# 校验工程
		self.windowCtr.verifyProject();
		# 处理启动事件
		self.windowCtr.handleLauncherEvent(callbackInfo = {"callback" : self.onLaunch});

	def onLaunch(self):
		# 延迟1s后调用启动后的逻辑
		wx.CallLater(1000, self.afterLaunch);

	def afterLaunch(self):
		# 调用主界面的创建函数
		if callable(self.createFunc):
			wx.CallAfter(self.createFunc);
		# 调用主界面的运行函数
		if callable(self.runFunc):
			wx.CallAfter(self.runFunc);
		# 关闭启动窗口
		self.closeWindow();
