# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2019-03-12 23:49:20
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-10 19:57:05
import os,sys,json;

# 校验依赖模块
def verifyDepends(pyExePath = "", dependList=[]):
	for depend in dependList:
		if os.system(pyExePath + "pip show " + depend) != 0:
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