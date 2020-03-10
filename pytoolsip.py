# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 19:05:42
# @Last Modified by:   JimZhang
# @Last Modified time: 2020-02-03 17:00:25

import sys,os,re,subprocess;

# 无日志打印运行命令
def runCmd(cmd, cwd=os.getcwd(), funcName="call", argDict = {}):
    startupinfo = subprocess.STARTUPINFO();
    startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW;
    startupinfo.wShowWindow = subprocess.SW_HIDE;
    return getattr(subprocess, funcName)(cmd, cwd = cwd, startupinfo = startupinfo, **argDict);

# 获取对应名称的脚本
def getFile(assetsPath, name):
    for fn in os.listdir(assetsPath):
        fPath = os.path.join(assetsPath, fn);
        if os.path.isfile(fPath) and re.search(f"^{name}\.?.*\.pyc", fn):
            return fn;
    return f"{name}.py";

# 运行pytoolsip程序
def runExeByPath(cwd):
    exeName = "pytoolsip.exe";
    ptipPath =os.path.abspath(os.path.join(cwd, "data", "update", "pytoolsip"));
    if os.path.exists(os.path.join(ptipPath, exeName)):
        runCmd(" ".join([exeName, cwd]), cwd = ptipPath);
        return True;
    return False;

# 获取依赖路径
def getDependPath(cwd, path):
    # 判断是否存在更新时的temp文件夹【存在表示更新失败，不能使用更新文件】
    if not os.path.exists(os.path.join(cwd, "data", "update", "temp_pytoolsip")):
        updatePath = os.path.abspath(os.path.join(cwd, "data", "update", "pytoolsip"));
        if os.path.exists(updatePath):
            dependPath = os.path.abspath(os.path.join(updatePath, path));
            if os.path.exists(dependPath):
                return dependPath;
    return os.path.abspath(os.path.join(cwd, path));

if __name__ == '__main__':
    cwd = os.getcwd();
    if not runExeByPath(cwd):
        # 获取工程路径
        if len(sys.argv) >= 2:
            if os.path.exists(sys.argv[1]):
                cwd = sys.argv[1];
        # 获取python依赖路径
        pyExe = os.path.abspath(getDependPath(cwd, "include/python/python.exe"));
        # 获取资源路径
        assetsPath = getDependPath(cwd, "assets");
        # 运行start.bat文件
        runPath = os.path.abspath(getDependPath(cwd, "run"));
        startBat = os.path.join(runPath, "start.bat");
        runCmd(" ".join([startBat, pyExe, assetsPath, getFile(assetsPath, "build"), getFile(assetsPath, "main"), cwd, runPath]));