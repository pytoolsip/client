# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 19:05:42
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-04-20 00:00:41

import os,re;

def getPyexe(configPath):
    if os.path.exists(configPath):
        isHasEnv = False;
        with open(configPath, "r") as f:
            for line in f.readlines():
                if re.search("[.*]", line):
                    if line.find("[env]"):
                        isHasEnv = True;
                    else:
                        isHasEnv = False;
                if isHasEnv:
                    matchObj = re.match("python\s*=\s*(.*)$", line);
                    if matchObj:
                        return os.path.abspath(os.path.join(matchObj.groups()[0], "python.exe"));
    return "python";

def getDepends(dependPath):
    if os.path.exists(dependPath):
        dependList = [];
        with open(dependPath, "r") as f:
            for line in f.readlines():
                dependList.append(line.strip());
    return " ".join(dependList);

def getMainFile(assetsPath):
    for name in os.listdir(assetsPath):
        fPath = os.path.join(assetsPath, name);
        if os.path.isfile(name) and re.search("main\.?.*\.pyc", name):
            return name;
    return "main.py";

def getBuildFile(assetsPath):
    for name in os.listdir(assetsPath):
        fPath = os.path.join(assetsPath, name);
        if os.path.isfile(name) and re.search("build\.?.*\.pyc", name):
            return name;
    return "build.py";

if __name__ == '__main__':
    # 获取python运行程序
    configIniPath = os.path.abspath(os.path.join(os.getcwd(), "assets\common\config\ini\config.ini"));
    pyExe = getPyexe(configIniPath);
    # 获取依赖组件
    dependsPath = os.path.abspath(os.path.join(os.getcwd(), "depend.mod"));
    depends = getDepends(dependsPath);
    assetsPath = os.path.abspath(os.path.join(os.getcwd(), "assets"));
    # 安装依赖模块
    os.system(" ".join(["cd assets&", pyExe, getBuildFile(assetsPath), pyExe, depends]));
    # 运行main文件
    os.system(" ".join(["cd assets&", pyExe, getMainFile(assetsPath)]));