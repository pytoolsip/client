# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-05-31 11:23:44
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-31 17:25:29
import os, sys;
import shutil;

# 获取json数据
def getJsonData(filePath):
	config = {};
	with open(filePath, "rb") as f:
		config = json.loads(f.read().decode("utf-8", "ignore"));
		f.close();
	return config;

# 根据目录获取md5列表
def getMd5Map(dirPath):
	filePath = os.path.join(dirPath, "update", "fileMd5Info.json");
	if os.path.exist(filePath):
		cfg = getJsonData(filePath);
		return cfg.get("md5Map", {});
	return {};

# 根据目录处理文件
def dealFileByPaths(srcPath, tarPath):
	srcMd5Map, tarMd5Map = getMd5Map(srcPath), getMd5Map(tarPath);
	for k,v in srcMd5Map.items():
		if k not in tarMd5Map:
			# 移除不需要的文件
			if os.path.exist(os.path.join(srcPath, k)):
				os.remove(os.path.join(srcPath, k));
		elif tarMd5Map[k] == v:
			tarMd5Map.pop(k);
	# 拷贝并覆盖
	copyFileList(srcPath, tarPath, fileList = tarMd5Map.keys());

# 拷贝文件列表
def copyFileList(srcPath, tarPath, fileList = []):
	for path in fileList:
		if os.path.exist(os.path.join(tarPath, path)):
			shutil.copyfile(os.path.join(tarPath, path), os.path.join(srcPath, path));

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		return;
	# 根据md5数据处理文件
	srcPath, tarPath = sys.argv[1], sys.argv[2];
	dealFileByPaths(srcPath, tarPath);
	# 拷贝扩展文件
	exFileList = [];
	if len(sys.argv) > 2:
		exFileList = json.loads(sys.argv[3]);
	copyFileList(srcPath, tarPath, fileList = exFileList);