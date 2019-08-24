# -*- coding: utf-8 -*-
# @Author: JinZhang
# @Date:   2019-05-31 11:23:44
# @Last Modified by:   JinZhang
# @Last Modified time: 2019-05-31 17:25:29
import os, sys;
import shutil;

# 获取json数据
def getJsonData(filePath):
	if os.path.exists(filePath):
		with open(filePath, "r") as f:
			return json.loads(f.read());
	return {};

# 根据目录获取md5列表
def getMd5Map(tempPath, targetMd5Path):
	tmpMd5, targetMd5 = {}, {};
	fileName = "_file_md5_map_.json";
	filePath = os.path.join(tempPath, fileName);
	if os.path.exist(filePath):
		tmpMd5 = getJsonData(filePath);
	filePath = os.path.join(targetMd5Path, fileName);
	if os.path.exist(filePath):
		targetMd5 = getJsonData(filePath);
	return tmpMd5, targetMd5;

# 根据目录处理文件
def copyFileByMd5s(tempPath, targetMd5Path):
	tmpMd5Map, tgMd5Map = getMd5Map(tempPath, targetMd5Path);
	for k,v in tmpMd5Map.items():
		tmpFile, tgFile = os.path.join(tempPath, k), os.path.join(targetMd5Path, k);
		if os.path.exist(tmpFile) and v == tgMd5Map.get(k, ""):
			continue; # 已存在且md5值一样，则跳过
		if not os.path.exist(tgFile):
			return False; # 不存在目标文件，则更新失败
		shutil.copyfile(tgFile, tmpFile); # 拷贝文件
	return True;

# 获取依赖模块表
def getDependMods(assetsPath):
	modList, modFile = [], os.path.join(assetsPath, "depends.mod");
	if not os.path.exists(modFile):
		return modList;
	with open(modFile, "r") as f:
		for line in f.readlines():
			mod = line.strip();
			if mod not in modList:
				modList.append(mod);
	return modList;

# 获取依赖模块表
def diffDependMods(tempPath, targetMd5Path):
	modList = [];
	tempModList, tgtMd5List = getDependMods(tempPath), getDependMods(targetMd5Path);
	for mod in tempModList:
		if mod not in tgtMd5List:
			modList.append(mod);
	return modList;

# 获取依赖模块列表
def checkDependMapJson(tempPath, targetMd5Path, dependMapFile):
	isChange, dependMap = False, getJsonData(dependMapFile);
	for mod in diffDependMods(tempPath, targetMd5Path):
		if mod not in dependMap:
			dependMap[mod] = 1;
			isChange = True;
	if isChange:
		with open(dependMapFile, "w") as f:
			f.write(json.dumps(dependMap));
	return dependMap;


if __name__ == '__main__':
	if len(sys.argv) <= 4:
		return;
	# 根据md5数据处理文件
	tempPath, targetPath, targetMd5Path, dependMapFile = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4];
	if copyFileByMd5s(tempPath, targetMd5Path):
		checkDependMapJson(tempPath, targetMd5Path, dependMapFile); # 检测依赖模块配置
		shutil.copytree(tempPath, targetPath); # 更新成功，拷贝文件夹
		shutil.rmtree(tempPath); # 删除临时更新文件夹
	else:
		sys.exit(1); # 更新失败，退出程序