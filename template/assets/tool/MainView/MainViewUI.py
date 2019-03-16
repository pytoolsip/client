# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-08 21:02:23
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:46:37

import wx;

from _Global import _GG;
from function.base import *;

class MainViewUI(wx.ScrolledWindow):
	"""docstring for MainViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(MainViewUI, self).__init__(parent, id, size = self.__params["size"]);
		self._className_ = MainViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.bindEvents(); # 绑定事件
		self.SetBackgroundColour(self.__params["bgColour"]);
		# 初始化滚动条参数
		self.SetScrollbars(1, 1, *self.__params["size"]);

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.unbindEvents();

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"size" : _GG("WindowObject").GetToolWinSize(),
			"style" : wx.BORDER_THEME,
			"bgColour" : wx.Colour(255,255,255),
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def bindEvents(self):
		_GG("WindowObject").BindEventToToolWinSize(self, self.onToolWinSize);

	def unbindEvents(self):
		_GG("WindowObject").UnbindEventToToolWinSize(self);

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局
		self.resetScrollbars(); # 重置滚动条

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		self.createTestCtrl();
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.testCtrl);
		self.SetSizerAndFit(box);

	def resetScrollbars(self):
		self.SetScrollbars(1, 1, self.GetSizer().GetSize().x, self.GetSizer().GetSize().y);

	def onToolWinSize(self, sizeInfo, event = None):
		self.SetSize(self.GetSize() + sizeInfo["preDiff"]);
		self.Refresh();
		self.Layout();

	def updateView(self, data):
		pass;

	def createTestCtrl(self):
		self.testCtrl = wx.TextCtrl(self, value = "测试文本控件", size = self.GetSize(), style = wx.TE_MULTILINE);