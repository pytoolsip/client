# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-03-12 23:49:20
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-10 19:57:05
import os,sys,json;

# 获取已通过pip安装的包
def getInstalledPackagesByPip(pyExePath = ""):
	installedPackageDict = {};
	installedPackageReader = os.popen(pyExePath + "pip freeze");
	installedPackageLines = installedPackageReader.read();
	for line in installedPackageLines.splitlines():
		lineArr = line.split("==");
		if len(lineArr) == 2:
			installedPackageDict[lineArr[0]] = lineArr[1];
	installedPackageReader.close();
	return installedPackageDict;

# 校验依赖模块
def verifyDepends(pyExePath = "", dependList=[]):
	pkgDict = getInstalledPackagesByPip(pyExePath);
	for depend in dependList:
		if depend not in pkgDict:
			os.system(pyExePath + "pip install " + depend);

if __name__ == '__main__':
	if len(sys.argv) > 2:
		pyExePath = sys.argv[1];
		dependList = [];
		for i in range(2, len(sys.argv)):
			dependList.append(sys.argv[i]);
		verifyDepends(pyExePath+" -m ", dependList);
	else:
		print("Failed to install depend modules !");