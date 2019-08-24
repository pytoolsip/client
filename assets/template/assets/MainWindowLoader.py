# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-10-08 20:56:43
# @Last Modified by:   JimZhang
# @Last Modified time: 2019-04-19 21:41:37

import wx,json;
from _Global import _GG;
from _Global import isExist_G;
from function.base import *;
from ProjectConfig import ProjectConfig;

from window.WindowLoader import WindowLoader;

class MainWindowLoader(WindowLoader):
	def __init__(self):
		super(MainWindowLoader, self).__init__();
		self._className_ = MainWindowLoader.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__toolWinSizeEventDict = {}; # 窗口大小事件字典
		self.__syncData__(); # 同步数据

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		if isExist_G(): # window加载类中的析构函数，涉及到全局变量时，要判断全局变量是否存在
			self.unregisterEvent(); # 注销事件
		pass;

	def createWindows(self):
		self.createParentWindowCtr();
		self.createMainWindowCtr();
		pass;

	def createParentWindowCtr(self):
		self._parentWindowUI = wx.MDIParentFrame(None, -1, title = ProjectConfig["name"], size = ProjectConfig["winSize"], style = wx.DEFAULT_FRAME_STYLE|wx.FRAME_NO_WINDOW_MENU); # 加载并获取UI
		self._parentWindowUI.Bind(wx.EVT_SIZE, self.onParentWinSize);
		self._parentWindowUI.ClientWindow.Bind(wx.EVT_SIZE, self.onClientWinSize);
		self.__PreWinUISize = self._parentWindowUI.Size; # 初始化self.__PreWinUISize
		self._parentWindowUI.ClientWindow.Size = self._parentWindowUI.Size; # 重置self._parentWindowUI.ClientWindow.Size
		
	def createMainWindowCtr(self):
		self.__MainWindowUI = wx.MDIChildFrame(self._parentWindowUI, -1, title = "", pos = (0,0), size = self._parentWindowUI.ClientWindow.Size, style = wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.CAPTION));
		self.__MainWindowUI.Bind(wx.EVT_SIZE, self.onToolWinSize);
	
	# 初始化窗口对象的公有函数
	def initMainWindowMethods(self):
		_GG("WindowObject").GetToolWinSize = self.getToolWinSize; # 设置获取工具窗口大小的函数
		_GG("WindowObject").BindEventToToolWinSize = self.bindEventToToolWinSize; # 绑定工具窗口大小变化事件
		_GG("WindowObject").UnbindEventToToolWinSize = self.unbindEventToToolWinSize; # 解绑工具窗口大小变化事件
		_GG("WindowObject").GetMainWindowCenterPoint = self.getMainWindowCenterPoint; # 获取主窗口的中心点

	def getToolWinSize(self):
		mainWinSize = self.__MainWindowUI.GetClientSize();
		return wx.Size(mainWinSize.x - 18, mainWinSize.y - 44);

	def onParentWinSize(self, event):
		self._parentWindowUI.ClientWindow.Size = self._parentWindowUI.Size;
		
	def onClientWinSize(self, event):
		preWinUISize = self.__PreWinUISize;
		curSize = self._parentWindowUI.GetSize();
		# 重置__PreWinUISize
		self.__PreWinUISize = curSize;
		# 重置__MainWindowUI Size
		if hasattr(self, "__MainWindowUI"):
			self.__MainWindowUI.SetSize(self.__MainWindowUI.Size[0] + curSize[0] - preWinUISize[0], self.__MainWindowUI.Size[1] + curSize[1] - preWinUISize[1]);	

	def bindEventToToolWinSize(self, obj, func):
		if callable(func):
			objId = id(obj);
			if objId not in self.__toolWinSizeEventDict:
				self.__toolWinSizeEventDict[objId] = {"obj" : obj, "funcDict" : {}};
			self.__toolWinSizeEventDict[objId]["funcDict"][id(func)] = func;

	def unbindEventToToolWinSize(self, obj, func = None):
		objId = id(obj);
		if objId in self.__toolWinSizeEventDict:
			if not func:
				self.__toolWinSizeEventDict.pop(objId);
			elif callable(func):
				funcId = id(func);
				if funcId in self.__toolWinSizeEventDict[objId]["funcDict"]:
					self.__toolWinSizeEventDict[objId]["funcDict"].pop(funcId);

	def onToolWinSize(self, event):
		if not hasattr(self, "OriToolUISize"):
			self.OriToolUISize = self.__MainWindowUI.GetSize();
			self.PreToolUISize = self.__MainWindowUI.GetSize();
		curToolUISize = self.__MainWindowUI.GetSize();
		sizeInfo = {
			"oriDiff" : curToolUISize - self.OriToolUISize,
			"preDiff" : curToolUISize - self.PreToolUISize,
		}
		for objId in self.__toolWinSizeEventDict:
			if self.__toolWinSizeEventDict[objId]["obj"]:
				for funcId in self.__toolWinSizeEventDict[objId]["funcDict"]:
					self.__toolWinSizeEventDict[objId]["funcDict"][funcId](sizeInfo, event = event);
		# 重置PreToolUISize
		self.PreToolUISize = curToolUISize;

	def getMainWindowCenterPoint(self, isToScreen = True):
		pos = self.__MainWindowUI.GetPosition();
		if isToScreen == True:
			pos = self.__MainWindowUI.ClientToScreen(pos);
		return wx.Point(pos[0] + self.__MainWindowUI.GetSize().x/2, pos[1] + self.__MainWindowUI.GetSize().y/2);

	def onCreateViews(self, event = None):
		self.createMainView();

	def createMainView(self):
		self.MainViewCtr = CreateCtr(self._curPath + "/tool/MainView", self.__MainWindowUI);

	def __syncData__(self):
		# 同步ProjectConfig的key、version、changelog到tool.json
		configPath = self._curPath + "tool/tool.json";
		toolConfig = {};
		if os.path.exists(configPath):
			with open(configPath, "r") as f:
				toolConfig = json.loads(f.read());
		# 更新key、version、changelog
		for k in ["key", "version", "changelog"]:
			toolConfig[k] = ProjectConfig.get(k, "null");
		with open(configPath, "w") as f:
			f.write(json.dumps(toolConfig));