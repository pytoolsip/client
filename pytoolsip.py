# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-08-11 19:05:42
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-04-20 00:00:41

import os,re;

# 获取对应名称的脚本
def getFile(assetsPath, name):
    for fn in os.listdir(assetsPath):
        fPath = os.path.join(assetsPath, fn);
        if os.path.isfile(fPath) and re.search(f"{name}\.?.*\.pyc", fn):
            return fn;
    return f"{name}.py";

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
    # 运行run.vbs文件
    runPath = os.path.abspath(os.path.join(os.getcwd(), "run"));
    os.system(" ".join(["start /d", runPath, "run.vbs", pyExe, assetsPath, getFile(assetsPath, "build"), getFile(assetsPath, "main"), os.getcwd()]));