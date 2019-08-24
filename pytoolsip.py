# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 19:05:42
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-04-20 00:00:41

import os,re,subprocess,json;

# 无日志打印运行命令
def runCmd(cmd, cwd=os.getcwd(), funcName="call"):
    startupinfo = subprocess.STARTUPINFO();
    startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW;
    startupinfo.wShowWindow = subprocess.SW_HIDE;
    return getattr(subprocess, funcName)(cmd, cwd = cwd, startupinfo = startupinfo);

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

# 获取依赖模块数据
def getDependMapJson():
    dependJsonPath = os.path.join("data", "depend_map.json");
    if os.path.exists(dependJsonPath):
        with open(dependJsonPath, "r") as f:
            return json.loads(f.read());
    return {};

# 设置依赖模块数据
def setDependMapJson(dependMap):
    dependJsonPath = os.path.join("data", "depend_map.json");
    with open(dependJsonPath, "w") as f:
        f.write(json.dumps(dependMap));

# 获取依赖模块列表
def checkDependMapJson(assetsPath):
    isChange, dependMap = False, getDependMapJson();
    for mod in getDependMods(assetsPath):
        if mod not in dependMap:
            dependMap[mod] = 1;
            isChange = True;
    if isChange:
        setDependMapJson(dependMap);
    return dependMap;

# 获取已安装模块
def getInstalledMods(pyExe):
    modList = [];
    ret = runCmd(f"{pyExe} -m pip freeze", funcName = "check_output");
    for line in ret.decode().split("\n"):
        line = line.strip();
        if line:
            modList.append(line.split("==")[0]);
    return modList;

# 获取未安装模块
def getUninstalledMods(pyExe, assetsPath):
    modList = getInstalledMods(pyExe); # 获取已安装模块
    unInstallMods = [];
    for mod in checkDependMapJson(assetsPath):
        if mod not in modList:
            unInstallMods.append(mod);
    return unInstallMods;

# 安装模块
def installMods(pyExe, mods):
    failedMods = [];
    for mod in mods:
        if subprocess.call(f"{pyExe} -m pip install {mod}") != 0:
            failedMods.append(mod);
    return failedMods;

# 安装依赖模块
def installDepends(pyExe, assetsPath):
    # 获取未安装模块
    unInstallMods = getUninstalledMods(pyExe, assetsPath);
    # 安装未安装模块
    failedMods = installMods(pyExe, unInstallMods);
    if len(failedMods) > 0:
        print(f"{pipPath} install {failedMods} failed!");

# 获取主函数文件
def getMainFile(assetsPath):
    for name in os.listdir(assetsPath):
        fPath = os.path.join(assetsPath, name);
        if os.path.isfile(fPath) and re.search("main\.?.*\.pyc", name):
            return name;
    return "main.py";

# 获取资源路径
def getAssetsPath():
    updatePath = os.path.abspath(os.path.join(os.getcwd(), "data", "update", "pytoolsip"));
    if os.path.exists(updatePath):
        return updatePath;
    return os.path.abspath(os.path.join(os.getcwd(), "assets"));

if __name__ == '__main__':
    # 获取python依赖路径
    pyExe = os.path.abspath(os.path.join(os.getcwd(), "include", "python", "python.exe"));
    # 获取资源路径
    assetsPath = getAssetsPath();
    # 安装依赖模块
    installDepends(pyExe, assetsPath);
    # 运行main文件
    runPath = os.path.abspath(os.path.join(os.getcwd(), "run"));
    runCmd(" ".join([os.path.join(runPath, "run.bat"), pyExe, assetsPath, getMainFile(assetsPath), os.getcwd()]), os.getcwd());