# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-12-17 22:27:40
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-06 09:45:30
import sys;
import os;
import wx;
import json;

from _Global import _GG;
from function.base import *;

def __getExposeData__():
	return {
		# "exposeDataName" : {},
	};

def __getExposeMethod__(DoType):
	return {
		"verifyModuleMap" : DoType.AddToRear,
		"showInstallModMsgDialog" : DoType.AddToRear,
		"verifyIPVersion" : DoType.AddToRear,
	};

def __getDepends__():
	return [
		{
			"path" : "verifyBehavior/VerifyEnvironmentBehavior", 
			"basePath" : _GG("g_CommonPath") + "behavior/",
		},
		{
			"path" : "installBehavior/InstallPythonPackageBehavior", 
			"basePath" : _GG("g_CommonPath") + "behavior/",
		},
		{
			"path" : "serviceBehavior/ServiceBehavior", 
			"basePath" : _GG("g_CommonPath") + "behavior/",
		},
	];

class VerifyProjectBehavior(_GG("BaseBehavior")):
	def __init__(self):
		super(VerifyProjectBehavior, self).__init__(__getDepends__(), __getExposeData__(), __getExposeMethod__, __file__);
		self._className_ = VerifyProjectBehavior.__name__;
		pass;

	# 默认方法【obj为绑定该组件的对象，argList和argDict为可变参数，_retTuple为该组件的前个函数返回值】
	# def defaultFun(self, obj, _retTuple = None, *argList, _retTuple = None, **argDict):
	# 	_GG("Log").i(obj._className_);
	# 	pass;

	# 校验import模块
	def verifyModuleMap(self, obj, _retTuple = None):
		jsonPath = _GG("g_DataPath") + "depend_map.json";
		if os.path.exists(jsonPath):
			modNameList = [];
			uninstallNameList = [];
			# 读取json文件
			with open(jsonPath, "rb") as f:
				moduleMap = json.loads(f.read().decode("utf-8", "ignore"));
				# 校验模块
				installedPkgDict = obj.getInstalledPackagesByPip(pythonPath = _GG("g_PythonPath"));
				for modName,count in moduleMap.items():
					if count > 0:
						if modName not in installedPkgDict:
							modNameList.append(modName);
					else:
						if modName not in installedPkgDict:
							uninstallNameList.append(modName);
			if len(modNameList) == 0:
				if len(uninstallNameList) > 0:
					wx.CallAfter(self.showUninstallModMsgDialog, obj, uninstallNameList);
				return True;
			else:
				return False, obj.showInstallModMsgDialog, modNameList;

	def showInstallModMsgDialog(self, obj, modNameList = [], _retTuple = None):
		messageDialog = wx.MessageDialog(obj, "是否确认安装以下模块？\n" + "\n".join(modNameList), "校验import模块失败！", style = wx.YES_NO|wx.ICON_QUESTION);
		if messageDialog.ShowModal() == wx.ID_YES:
			# 安装模块
			for modName in modNameList:
				obj.showDetailTextCtrl(text = "正在安装" + modName + "模块...\n此过程可能持续10+秒，请耐心等候...");
				obj.installPackageByPip(modName, pythonPath = _GG("g_PythonPath"));
			# 校验是否成功安装
			failedNameList = [];
			installedPkgDict = obj.getInstalledPackagesByPip(pythonPath = _GG("g_PythonPath"));
			for modName in modNameList:
				if modName in installedPkgDict:
					obj.showDetailTextCtrl(text = "安装“{}”模块成功。".format(modName));
				else:
					obj.showDetailTextCtrl(text = "安装“{}”模块失败！".format(modName));
					failedNameList.append(modName);
			return len(failedNameList) == 0;
		return False;

	def showUninstallModMsgDialog(self, obj, modNameList = [], _retTuple = None):
		messageDialog = wx.MessageDialog(obj, "发现有未使用的模块，是否确认卸载以下模块？\n" + "\n".join(modNameList), "校验import模块成功！", style = wx.YES_NO|wx.ICON_QUESTION);
		if messageDialog.ShowModal() == wx.ID_YES:
			obj.showDetailTextCtrl(text = "开始卸载未使用的模块...");
			failedNameList = [];
			for modName in modNameList:
				if obj.uninstallPackageByPip(modName, pythonPath = _GG("g_PythonPath")):
					obj.showDetailTextCtrl(text = "卸载“{}”模块成功。".format(modName));
				else:
					obj.showDetailTextCtrl(text = "卸载“{}”模块失败！".format(modName));
					failedNameList.append(modName);
			return len(failedNameList) == 0;
		return False;

	# 校验Common版本
	def verifyIPVersion(self, obj, _retTuple = None):
		if hasattr(obj, "checkUpdateIP"):
			obj.checkUpdateIP();
		return True;