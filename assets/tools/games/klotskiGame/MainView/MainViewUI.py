# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-08 21:02:23
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-01-23 14:25:31

import wx;
import time;

from _Global import _GG;
from function.base import *;

class MainViewUI(wx.ScrolledWindow):
	"""docstring for MainViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(MainViewUI, self).__init__(parent, id, size = self.__params["size"], style = self.__params["style"]);
		self.className_ = MainViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;
		self.bindEvents(); # 绑定事件
		self.SetBackgroundColour(self.__params["bgColour"]);
		# 初始化滚动条参数
		self.SetScrollbars(1, 1, self.__params["size"][0] + 20, self.__params["size"][0] + 40);

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
		# 校验大小
		if self.__params["size"][0] < 100:
			self.__params["size"] = (self.__params["size"][0], self.__params["size"][1]);

	def getCtr(self):
		return self.viewCtr;

	def bindEvents(self):
		_GG("WindowObject").BindEventToToolWinSize(self, self.onToolWinSize);

	def unbindEvents(self):
		_GG("WindowObject").UnbindEventToToolWinSize(self);

	def initView(self):
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局
		self.resetScrollbars(); # 重置滚动条

	def createControls(self):
		self.createControlPanel();
		self.createContentPanel();
		self.setGameOverCallback();
		
	def initViewLayout(self):
		box = wx.BoxSizer(wx.HORIZONTAL);
		box.Add(self.controlPanel);
		box.Add(self.contentPanel);
		self.SetSizerAndFit(box);

	def resetScrollbars(self):
		self.SetScrollbars(1, 1, self.GetSizer().GetSize().x, self.GetSizer().GetSize().y);

	def updateView(self, data):
		pass;
		
	def onToolWinSize(self, sizeInfo, event = None):
		self.SetSize(self.GetSize() + sizeInfo["preDiff"]);
		self.Refresh();
		self.Layout();

	def createControlPanel(self):
		self.controlPanel = wx.Panel(self, size = (100, self.GetSize().y), style = wx.BORDER_THEME);
		self.createStartGameBtn(self.controlPanel);
		self.createRestartGameBtn(self.controlPanel);
		self.initControlPanelLayout();

	def initControlPanelLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		box.Add(self.startGameBtn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		box.Add(self.restartGameBtn, flag = wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border = 5);
		self.controlPanel.SetSizerAndFit(box);

	def createContentPanel(self):
		self.contentPanel = wx.Panel(self, size = (self.GetSize().x - 100, self.GetSize().y), style = wx.BORDER_THEME);
		self.createContentViews(self.contentPanel);
		self.updateContentPanelSize();
		self.initContentPanelLayout();
		wx.CallAfter(self.contentPanel.Show, False);

	def updateContentPanelSize(self):
		contentPanelSize = self.contentPanel.GetSize();
		klotskiViewSize = self.getCtr().getUIByKey("KlotskiViewCtr").GetSize();
		timingViewSize = self.getCtr().getUIByKey("TimingViewCtr").GetSize();
		newSizeX = max(contentPanelSize.x, klotskiViewSize.x, timingViewSize.x);
		newSizeY = max(self.controlPanel.GetSize().y, contentPanelSize.y, klotskiViewSize.y + timingViewSize.y);
		self.contentPanel.SetSize(newSizeX, newSizeY);

	def initContentPanelLayout(self):
		box = wx.BoxSizer(wx.VERTICAL);
		topOffset = (self.contentPanel.GetSize().y - self.getCtr().getUIByKey("KlotskiViewCtr").GetSize().y - self.getCtr().getUIByKey("TimingViewCtr").GetSize().y) / 2;
		box.Add(self.getCtr().getUIByKey("TimingViewCtr"), flag = wx.ALIGN_CENTER|wx.TOP, border = topOffset);
		box.Add(self.getCtr().getUIByKey("KlotskiViewCtr"), flag = wx.ALIGN_CENTER);
		self.contentPanel.SetSizer(box);

	def createStartGameBtn(self, parent):
		self.startGameBtn = wx.Button(parent, label = "开始游戏");
		self.startGameBtn.Bind(wx.EVT_BUTTON, self.onStartGame);

	def createRestartGameBtn(self, parent):
		self.restartGameBtn = wx.Button(parent, label = "重新开始");
		self.restartGameBtn.Bind(wx.EVT_BUTTON, self.onRestartGame);

	def onStartGame(self, event = None):
		if not self.contentPanel.IsShown():
			self.contentPanel.Show(True);
			self.getCtr().getUIByKey("TimingViewCtr").startTimer();

	def onRestartGame(self, ecent = None):
		self.onStartGame();
		self.getCtr().getUIByKey("KlotskiViewCtr").resetView();
		self.getCtr().getUIByKey("TimingViewCtr").startTimer();

	def createContentViews(self, parent):
		self.getCtr().createCtrByKey("KlotskiViewCtr", GetPathByRelativePath("../view/KlotskiView", self.curPath), parent = parent); # , parent = self, params = {}
		klotskiViewSize = self.getCtr().getUIByKey("KlotskiViewCtr").GetSize();
		self.getCtr().createCtrByKey("TimingViewCtr", GetPathByRelativePath("../view/TimingView", self.curPath), parent = parent, params = {"size" : (klotskiViewSize.x, -1)}); # , parent = self, params = {}

	def setGameOverCallback(self):
		self.getCtr().getUIByKey("KlotskiViewCtr").onGameOver = self.onGameOver;

	def onGameOver(self):
		self.getCtr().getUIByKey("TimingViewCtr").stopTimer();
