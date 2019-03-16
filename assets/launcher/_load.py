# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-09 21:32:27
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:46:25

import os;
import wx;
from _Global import _GG;
from function.base import *;

class LauncherLoader(object):
	def __init__(self):
		super(LauncherLoader, self).__init__();
		self._className_ = LauncherLoader.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.createFunc = None;
		self.runFunc = None;
		self.bindBehavior();

	def load(self, createFunc, runFunc):
		self.createFunc = createFunc;
		self.runFunc = runFunc;
		self.createWindow();
		self.runWindow();
		self.launch();

	def createWindow(self):
		self.__windowCtr = CreateCtr(self._curPath + "window/LauncherWindow", None);

	def runWindow(self):
		self.__windowCtr.getUI().Centre();
		self.__windowCtr.getUI().Show(True);

	def closeWindow(self):
		self.__windowCtr.getUI().Close(True);

	def launch(self):
		# 校验工程
		self.__windowCtr.verifyProject();
		# 处理启动事件
		self.__windowCtr.handleLauncherEvent(callbackInfo = {"callback" : self.onLaunch});

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
		# 自动登录
		wx.CallAfter(self.autoLogin);

	def bindBehavior(self):
		_GG("BehaviorManager").bindBehavior(self, {"path" : "serviceBehavior/ServiceBehavior", "basePath" : _GG("g_CommonPath") + "behavior/"});

	# 自动登录
	def autoLogin(self):
		# 绑定serviceBehavior/ServiceBehavior组件
		if hasattr(self, "autoLoginIP"):
			_GG("Log").i("Auto login IP ...");
			self.autoLoginIP();