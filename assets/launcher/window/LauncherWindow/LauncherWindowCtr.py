# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-09 22:41:23
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-14 19:04:02

import wx;
import threading;
import copy;

from _Global import _GG;
from _Global import isExist_G;

from LauncherWindowUI import *;

def getRegisterEventMap(G_EVENT):
	return {
		G_EVENT.ADD_LAUNCHER_EVENT : "addLauncherEvent",
	};

class LauncherWindowCtr(object):
	"""docstring for LauncherWindowCtr"""
	def __init__(self, parent = None, params = {}):
		super(LauncherWindowCtr, self).__init__();
		self.className_ = LauncherWindowCtr.__name__;
		self._curPath = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") + "/";
		self.__CtrMap = {}; # 所创建的控制器
		self.initUI(parent);
		self.registerEventMap(); # 注册事件
		self.bindBehaviors(); # 绑定组件
		self.scheduleTaskList = []; # 调度任务列表

	def __del__(self):
		self.__dest__();

	def __dest__(self):
		if not hasattr(self, "_unloaded_"):
			self._unloaded_ = True;
			self.__unload__();

	def __unload__(self):
		if isExist_G(): # window控制类中的析构函数，涉及到全局变量时，要判断全局变量是否存在
			self.unregisterEventMap(); # 注销事件
			self.unbindBehaviors(); # 解绑组件
		self.delCtrMap(); # 銷毀控制器列表

	def delCtrMap(self):
		for key in self.__CtrMap:
			DelCtr(self.__CtrMap[key]);
		self.__CtrMap.clear();

	def initUI(self, parent = None):
		# 创建视图UI类
		windowTitle = _GG("AppConfig")["AppTitle"];
		windowSize = (640,420); # _GG("AppConfig")["AppSize"];
		windowStyle = wx.DEFAULT_FRAME_STYLE^(wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU);
		self.__ui = LauncherWindowUI(parent, id = -1, title = windowTitle, size = windowSize, style = windowStyle, curPath = self._curPath, windowCtr = self);
		self.__ui.SetBackgroundColour(wx.Colour(250,250,250));
		self.__ui.initWindow();

	def getUI(self):
		return self.__ui;
		
	"""
		key : 索引所创建控制类的key值
		path : 所创建控制类的路径
		parent : 所创建控制类的UI的父节点，默认为本UI
		params : 扩展参数
	"""
	def createCtrByKey(self, key, path, parent = None, params = {}):
		if not parent:
			parent = self.getUI();
		self.__CtrMap[key] = CreateCtr(path, parent, params = params);

	def getCtrByKey(self, key):
		return self.__CtrMap.get(key, None);

	def getUIByKey(self, key):
		ctr = self.getCtrByKey(key);
		if ctr:
			return ctr.getUI();
		return None;
		
	def registerEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").register(eventId, self, callbackName);

	def unregisterEventMap(self):
		eventMap = getRegisterEventMap(_GG("EVENT_ID"));
		for eventId, callbackName in eventMap.items():
			_GG("EventDispatcher").unregister(eventId, self, callbackName);
			
	def updateWindow(self, data):
		self.__ui.updateWindow(data);

	def bindBehaviors(self):
		_GG("BehaviorManager").bindBehavior(self.getUI(), {"path" : _GG("g_AssetsPath") + "launcher/behavior/VerifyProjectBehavior"});
		pass;
		
	def unbindBehaviors(self):
		pass;

	# 重新校验按钮回调
	def onReverifyButton(self, event = None):
		self.getUI().showReverifyButton(isShow = False);
		self.getUI().showDetailTextCtrl(isShow = False, isReset = True);
		self.handleLauncherEvent();

	def addLauncherEvent(self, data):
		self.addScheduleTask(data);

	def addScheduleTask(self, data):
		if callable(data.get("scheduleTask")):
			# 添加到任务列表
			self.scheduleTaskList.append({
				"task" : data["scheduleTask"],
				"text" : data.get("text", "正在启动"),
				"args" : data.get("args", {}),
				"failInfo" : data.get("failInfo", {}),
			});

	def handleLauncherEvent(self, callbackInfo = {}, failCallbackInfo = {}):
		# 保存回调函数信息
		if callable(callbackInfo.get("callback")):
			self.launcherCallbackInfo = {
				"callback" : callbackInfo.get("callback"),
				"args": callbackInfo.get("args", {}),
				"failCallback" : failCallbackInfo.get("callback"),
				"failArgs" : failCallbackInfo.get("args", {}),
			};
		# 重置加载进度视图
		self.getCtrByKey("LauncherGaugeView").updateView({"isReset" : True});
		# 处理调度任务列表
		self.handleScheduleTaskList(copy.copy(self.scheduleTaskList));

	def handleScheduleTaskList(self, scheduleTaskList = []):
		if len(scheduleTaskList) > 0:
			taskInfo = scheduleTaskList.pop(0);
			self.getCtrByKey("LauncherGaugeView").updateView({
				"text" : taskInfo["text"],
				"gauge" : 1 - (len(scheduleTaskList) + 1)/len(self.scheduleTaskList),
			});
			# 启动线程
			threading.Thread(target = self.handleScheduleTask, args = (taskInfo, scheduleTaskList, )).start();
		else:
			self.getCtrByKey("LauncherGaugeView").updateView({
				"text" : "完成启动，正在打开主界面...",
				"gauge" : 1,
			});
			if hasattr(self, "launcherCallbackInfo"):
				self.launcherCallbackInfo["callback"](*self.launcherCallbackInfo["args"].get("list", []), **self.launcherCallbackInfo["args"].get("dict", {}));

	def handleScheduleTask(self, taskInfo, scheduleTaskList = []):
		isContinue, taskResult = self.handleScheduleTaskInfo(taskInfo);
		if not isContinue:
			# 显示重新校验按钮
			wx.CallAfter(self.getUI().showReverifyButton);
			# 调用校验失败后的相关回调函数
			failInfo = taskInfo.get("failInfo", {});
			wx.CallAfter(self.getCtrByKey("LauncherGaugeView").updateView, {
				"text" : failInfo.get("text", "启动失败！"),
				"textColor" : failInfo.get("textColor", wx.Colour(255, 0, 0)),
			});
			failCallback = None;
			failArgs = {};
			if isinstance(taskResult, tuple) and len(taskResult) > 0:
				failCallback = taskResult[0];
				if len(taskResult) > 1:
					failArgs["list"] = taskResult[1:];
			if not callable(failCallback) and callable(failInfo.get("failCallback")):
				failCallback = failInfo.get("failCallback");
				failArgs = failInfo.get("failArgs", {});
			if callable(failCallback):
				def failCallbackFunc():
					if failCallback(*failArgs.get("list", []), **failArgs.get("dict", {})):
						self.getCtrByKey("LauncherGaugeView").updateView({"textColor" : wx.Colour(0, 0, 0)})
						# 继续执行任务列表中的任务
						scheduleTaskList.insert(0, taskInfo);
						self.handleScheduleTaskList(scheduleTaskList);
				wx.CallAfter(failCallbackFunc);
			else:
				# 调用校验失败后的回调函数
				if hasattr(self, "launcherCallbackInfo") and callable(self.launcherCallbackInfo.get("failCallback")):
					failArgs = self.launcherCallbackInfo.get("failArgs", {});
					wx.CallAfter(self.launcherCallbackInfo.get("failCallback"), *failArgs.get("list", []), **failArgs.get("dict", {}));
			return; # 不执行以下逻辑
		# 继续执行任务列表中的任务
		wx.CallAfter(self.handleScheduleTaskList, scheduleTaskList);

	def handleScheduleTaskInfo(self, taskInfo = {}):
		isContinue, taskResult = True, None;
		if callable(taskInfo.get("task")):
			args = taskInfo.get("args", {});
			result = taskInfo.get("task")(*args.get("list", []), **args.get("dict", {}));
			if isinstance(result, tuple) and len(result) > 0:
				isContinue = result[0];
				if len(result) > 1:
					taskResult = result[1:];
			else:
				isContinue = result;
		return isContinue, taskResult;

	# 校验工程
	def verifyProject(self):
		self.addLauncherEvent({
			"scheduleTask" : self.getUI().verifyPythonEnv,
			"text" : "正在校验python环境",
			"failInfo" : {
				"text" : "校验python环境失败！",
				# "failCallback" : self.getUI().showEntryPyPathDialog,
			},
		});
		self.addLauncherEvent({
			"scheduleTask" : self.getUI().verifyPipEnv,
			"text" : "正在校验pip环境",
			"failInfo" : {
				"text" : "校验pip环境失败！",
				# "failCallback" : self.getUI().showInstallPipMsgDialog,
			},
		});
		self.addLauncherEvent({
			"scheduleTask" : self.getUI().verifyModuleMap,
			"text" : "正在校验工程所需模块",
			"failInfo" : {
				"text" : "校验工程所需模块失败！",
				# "failCallback" : self.getUI().showInstallModMsgDialog,
			},
		});
		self.addLauncherEvent({
			"scheduleTask" : self.getUI().verifyCommonVersion,
			"text" : "正在校验Common版本",
		});