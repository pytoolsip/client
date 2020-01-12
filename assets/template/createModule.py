# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-03-29 22:21:00
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-04-20 12:29:21
import os;

from module.ModuleCreator import *;

"""
	参数解析
	modName 所基于生成的模块名
	targetModName 所要生成的模块名
	targetModPath 所要生成的目录
"""
if __name__ == "__main__":
	# assets层的目录
	assetsPath = "";
	# common层的目录
	commonPath = "common";

	# # 创建组件的参数配置 behavior
	# theModule = {
	# 	"modName" : "behavior",
	# 	"targetModName" : "CompilePyBehavior",
	# 	"targetModPath" : commonPath + "/behavior/compileBehavior/",
	# };

	# # 创建视图的参数配置 view
	# theModule = {
	# 	"modName" : "view",
	# 	"targetModName" : "InstallerGaugeView",
	# 	"targetModPath" : assetsPath + "../../installer/view/",
	# };

	# # 创建窗口的参数配置 window
	# theModule = {
	# 	"modName" : "window",
	# 	"targetModName" : "InstallerWindow",
	# 	"targetModPath" : assetsPath + "../../installer/window/",
	# };

	# 创建弹窗的参数配置 dialog
	theModule = {
		"modName" : "dialog",
		"targetModName" : "CreateTemplateDialog",
		"targetModPath" : "test",
	};


	# # 创建module的对象
	CMO = CreateModuleObj();
	# # 创建module
	CMO.createMod(theModule["modName"], theModule["targetModName"], targetPath = theModule["targetModPath"], basePath = os.getcwd());