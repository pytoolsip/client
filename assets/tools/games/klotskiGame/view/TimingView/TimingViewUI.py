# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-12-22 09:09:43
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 19:00:52

import wx;
import math;
from datetime import datetime;

from _Global import _GG;
from function.base import *;

class TimingViewUI(wx.Panel):
	"""docstring for TimingViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(TimingViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self.className_ = TimingViewUI.__name__;
		self._curPath = curPath;
		self.__viewCtr = viewCtr;
		self.__startTime = None;
		self.tryStopTimer = False;
		self.createTimer(); # 创建定时器

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		self.stopAllTimer(isDestroy = True); # 停止定时器

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (-1,-1),
			"style" : wx.BORDER_THEME,
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.__viewCtr;

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self._curPath + "***View"); # , parent = self, params = {}
		self.createTimingText();
		pass;
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.timingText, flag = wx.ALIGN_CENTER);
		self.SetSizer(box);
		if self.GetSize().x < self.timingText.GetSize().x:
			self.Fit();

	def updateView(self, data):
		pass;

	def restartTime(self):
		self.__startTime = datetime.now();

	def createTimer(self):
		self.m_timer = _GG("TimerManager").createTimer(self, callback = self.onTimerEvent);

	def stopAllTimer(self, isDestroy = False):
		if hasattr(self, "m_timer") and self.m_timer.IsRunning():
			self.m_timer.Stop();
			if isDestroy:
				_GG("TimerManager").deleteTimer(self.m_timer);

	def onTimerEvent(self, event = None):
		if self.__startTime:
			diffDataTime = datetime.now() - self.__startTime;
			days, diffSeconds = diffDataTime.days, diffDataTime.seconds;
			hours = math.floor(diffSeconds / (60 * 60)) % 24;
			minutes = math.floor(diffSeconds / 60) % 60;
			seconds = diffSeconds % 60;
			if days > 0:
				self.timingText.SetLabel("{}D ".format(days) + ":".join(["%02d"%hours, "%02d"%minutes, "%02d"%seconds]));
			else:
				self.timingText.SetLabel(":".join(["%02d"%hours, "%02d"%minutes, "%02d"%seconds]));
			self.checkStopTimer();

	def createTimingText(self):
		self.timingText = wx.StaticText(self, label = "--:--:--");

	def startTimer(self):
		self.restartTime();
		self.onTimerEvent();
		if hasattr(self, "m_timer") and not self.m_timer.IsRunning():
			self.m_timer.Start(1000);

	def stopTimer(self):
		self.tryStopTimer = True;

	def checkStopTimer(self):
		if self.tryStopTimer:
			self.stopTimer();
			self.tryStopTimer = False;