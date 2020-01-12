# -*- coding: utf-8 -*-
# @Author: JimDreamHeart
# @Date:   2018-04-05 13:08:49
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-03-15 16:09:34


import linecache;
import getpass;
import time;
import os;
import re;

# 当前文件位置
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__));

class CreateModuleObj(object):
	"""docstring for CreateModuleObj"""
	def __init__(self):
		super(CreateModuleObj, self).__init__();
		self.__modulePath = CURRENT_PATH;
		self.__userName = self.getUserName();
		self.__fileHeadConfig = self.initFileHeadConfig();
		self.__moduleName = "";

	def createMod(self, moduleName, targetName, targetPath = "", basePath = ""):
		if moduleName and targetPath:
			self.__moduleName = moduleName;
			isCreateFile,targetFilePath = self.checkAndCreateFilePath(targetPath, targetName, basePath);
			if isCreateFile == True:
				modFullName = self.getModuleFullName();
				if not os.path.exists(os.path.join(self.__modulePath, modFullName)):
					return False, "invalid";
				self.createFilesByRecursion(targetFilePath, targetName, self.__modulePath, modFullName);
			return isCreateFile, targetFilePath;
		return False, "";

	def initFileHeadConfig(self):
		return {
			"@Author" : "getUserName",
			"@Date" : "getNowDate",
			"@Last Modified by" : "getUserName",
			"@Last Modified time" : "getNowDate",
		};

	def getFileHeadReplacedContent(self, line):
		for Key,Func in self.__fileHeadConfig.items():
			if re.search(r""+Key, line):
				return False, self.getReplacedStr(Key, getattr(self, Func)(), line);
		if re.search("^[def,class].*", line):
			return True, line;
		return False, line;

	def getReplacedStr(self, findStr, replaceStr, content):
		regStr = re.compile(".*"+findStr+"[:]\s*(.+)\s*$");
		findRet = re.findall(regStr, content);
		return re.sub(r""+findRet[0], r""+replaceStr, content);

	def getUserName(self):
		if hasattr(self, "userName"):
			return self.__userName;
		return getpass.getuser();

	def getNowDate(self):
		return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()));

	def getPathByRelativePath(self, path, basePath = ""):
		if not basePath:
			return path;
		basePath = re.sub(r"\\", r"/", basePath);
		basePathList = basePath.split("/");
		path = re.sub(r"\\", r"/", path);
		pathList = path.split("/");
		while len(pathList) > 0:
			if pathList[0] == "..":
				basePathList.pop();
				pathList.pop(0);
			else:
				basePathList.extend(pathList);
				break;
		return "/".join(basePathList).strip();

	def getModuleFullName(self):
		if os.path.isdir(os.path.join(self.__modulePath, self.__moduleName)):
			return self.__moduleName;
		else:
			return self.__moduleName + ".py";

	def checkAndCreateFilePath(self, targetPath, targetName, basePath):
		# 检测目标文件是否已存在
		targetModPath = self.getPathByRelativePath(targetPath, basePath);
		targetFileFulName = os.path.join(targetModPath, targetName);
		if not os.path.isdir(os.path.join(self.__modulePath, self.__moduleName)):
			targetFileFulName += ".py";
		if os.path.exists(targetFileFulName):
			if not self.isCoverExistedMod():
				return False, "existed";
		# 若文件所在路径不存在，则创建相应路径
		if not os.path.exists(targetModPath):
			os.makedirs(targetModPath);
		return True, targetModPath;

	def createFilesByRecursion(self, targetFilePath, targetFileName, moduleFilePath, moduleFileName):
		modulePath = os.path.join(moduleFilePath, moduleFileName);
		if os.path.isdir(modulePath):
			newTargetFilePath = self.checkAndCreateFolderByModule(targetFilePath, moduleFileName, targetFileName);
			for fileName in os.listdir(modulePath):
				self.createFilesByRecursion(newTargetFilePath, targetFileName, modulePath, fileName);
		else:
			self.createFileByModule(targetFilePath, targetFileName, moduleFilePath, moduleFileName);
			pass;

	def checkAndCreateFolderByModule(self, baseFilePath, filePathName, targetFileName):
		newFilePathName = re.sub(r""+self.__moduleName, r""+targetFileName, filePathName);
		targetFullPath = os.path.join(baseFilePath, newFilePathName);
		if not os.path.exists(targetFullPath):
			os.makedirs(targetFullPath);
		return targetFullPath;

	def createFileByModule(self, targetFilePath, targetFileName, moduleFilePath, moduleFileName):
		# 获取目标文件内容
		data = "";
		isInitedFileHead = False;
		newModuleName = self.__moduleName.capitalize();
		for line in linecache.getlines(os.path.join(moduleFilePath, moduleFileName)):
			newLine = line;
			if not isInitedFileHead:
				isInitedFileHead, newLine = self.getFileHeadReplacedContent(line);
				pass;
			if isInitedFileHead:
				if re.search(r"Template" + newModuleName, line):
					newLine = re.sub(r"Template" + newModuleName, r""+targetFileName, line);
					pass;
			data += newLine;
		# 写入目标文件
		targetFileFullName = os.path.join(targetFilePath, re.sub(r""+self.__moduleName, r""+targetFileName, moduleFileName));
		try:
			with open(targetFileFullName, "w+", encoding = "utf-8") as f:
				f.writelines(data);
		except Exception:
			with open(targetFileFullName, "wb+") as f:
				f.writelines(data);
		print("It is finish to create \"{0}\" by module named \"{1}\".".format(targetFileName, moduleFileName));
		pass;

	def isCoverExistedMod(self):
		return False;