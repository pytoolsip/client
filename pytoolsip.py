# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 19:05:42
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-04-20 00:00:41

import os,re,subprocess;

def updatePyexe(pyIncludePath, configPath):
    pyexePath = os.path.join(pyIncludePath, "python.exe");
    if os.path.exists(pyexePath):
        content = "";
        isHasEnv = False;
        with open(configPath, "r") as f:
            for line in f.readlines():
                content += line;
                if re.search("[.*]", line):
                    if line.find("[env]"):
                        isHasEnv = True;
                    else:
                        isHasEnv = False;
                if isHasEnv and re.search("python\s*=\s*", line):
                    content += pyexePath;
        with open(configPath, "w") as f:
            f.write(content);
        return pyexePath;
    return "python";

def getPyexe(pyIncludePath, configPath):
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
    return updatePyexe(pyIncludePath, configPath); # 更新python运行程序路径

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
        if os.path.isfile(fPath) and re.search("main\.?.*\.pyc", name):
            return name;
    return "main.py";

def getBuildFile(assetsPath):
    for name in os.listdir(assetsPath):
        fPath = os.path.join(assetsPath, name);
        if os.path.isfile(fPath) and re.search("build\.?.*\.pyc", name):
            return name;
    return "build.py";

def runCmd(cmd, cwd):
    startupinfo = subprocess.STARTUPINFO();
    startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW;
    startupinfo.wShowWindow = subprocess.SW_HIDE;
    subprocess.call(cmd, cwd = cwd, startupinfo = startupinfo);

if __name__ == '__main__':
    # 获取python依赖路径
    pyIncludePath = os.path.abspath(os.path.join(os.getcwd(), "include\python"));
    # 获取python运行程序
    configIniPath = os.path.abspath(os.path.join(os.getcwd(), "assets\common\config\ini\config.ini"));
    pyExe = getPyexe(pyIncludePath, configIniPath);
    # 获取依赖组件
    dependsPath = os.path.abspath(os.path.join(os.getcwd(), "depend.mod"));
    depends = getDepends(dependsPath);
    # 安装依赖模块
    assetsPath = os.path.abspath(os.path.join(os.getcwd(), "assets"));
    subprocess.call(" ".join([pyExe, getBuildFile(assetsPath), pyExe, depends]), cwd = assetsPath);
    # 运行main文件
    runPath = os.path.abspath(os.path.join(os.getcwd(), "run"));
    runCmd(" ".join([os.path.join(runPath, "run.bat"), pyExe, assetsPath, getMainFile(assetsPath)]), os.getcwd());