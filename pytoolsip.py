# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 19:05:42
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-04-20 00:00:41

import os,re,subprocess;

# 无日志打印运行命令
def runCmd(cmd, cwd=os.getcwd(), funcName="call"):
    startupinfo = subprocess.STARTUPINFO();
    startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW;
    startupinfo.wShowWindow = subprocess.SW_HIDE;
    return getattr(subprocess, funcName)(cmd, cwd = cwd, startupinfo = startupinfo);

# 获取依赖模块表
def getDependMods():
    modList = [];
    if not os.path.exists("depends.mod"):
        return modList;
    with open("depends.mod", "r") as f:
        for line in f.readlines():
            mod = line.strip();
            if mod not in modList:
                modList.append(mod);
    return modList;

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
def getUninstalledMods(pyExe):
    modList = getInstalledMods(pyExe); # 获取已安装模块
    unInstallMods = [];
    for mod in getDependMods():
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
def installDepends(pyExe):
    # 获取未安装模块
    unInstallMods = getUninstalledMods(pyExe);
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

if __name__ == '__main__':
    # 获取python依赖路径
    pyExe = os.path.abspath(os.path.join(os.getcwd(), "include", "python", "python.exe"));
    # 安装依赖模块
    installDepends(pyExe);
    # 运行main文件
    assetsPath = os.path.abspath(os.path.join(os.getcwd(), "assets"));
    runPath = os.path.abspath(os.path.join(os.getcwd(), "run"));
    runCmd(" ".join([os.path.join(runPath, "run.bat"), pyExe, assetsPath, getMainFile(assetsPath)]), os.getcwd());