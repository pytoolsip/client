# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-12-08 13:41:18
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-01-12 09:45:17

import wx;

from _Global import _GG;
from function.base import *;

class LauncherGaugeViewUI(wx.Panel):
	"""docstring for LauncherGaugeViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(LauncherGaugeViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self.className_ = LauncherGaugeViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_NONE,
			"fgColour" : wx.Colour(0,0,0),
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self.curPath + "***View"); # , parent = self, params = {}
		self.createGauge();
		self.createInfoText();
		pass;
		
	def initViewLayout(self):
		vbox = wx.BoxSizer(wx.VERTICAL);
		vbox.Add(self.text);
		vbox.Add(self.gauge, flag = wx.ALIGN_CENTER);
		self.SetSizer(vbox);
		pass;

	def updateView(self, data):
		if "text" in data:
			self.text.SetLabel(data["text"]);
		if "textColor" in data:
			self.text.SetForegroundColour(data["textColor"]);
		if "gauge" in data:
			self.gauge.SetValue(data["gauge"] * self.gauge.GetRange());
		if "isReset" in data:
			self.resetView(data);

	def createGauge(self):
		self.gauge = wx.Gauge(self, size = (self.GetSize()[0], 20), style = wx.GA_SMOOTH);

	def createInfoText(self):
		self.text = wx.StaticText(self, label = "正在启动...", style = wx.ALIGN_LEFT);

	def resetView(self, data = {}):
		self.updateView({
			"text" : "",
			"textColor" : self.__params["fgColour"],
			"gauge" : 0,
		});