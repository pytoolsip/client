import sys,os,subprocess,json;

# 无日志打印运行命令
def runCmd(cmd, cwd=os.getcwd(), funcName="call", argDict = {}):
    startupinfo = subprocess.STARTUPINFO();
    startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW;
    startupinfo.wShowWindow = subprocess.SW_HIDE;
    return getattr(subprocess, funcName)(cmd, cwd = cwd, startupinfo = startupinfo, **argDict);

# 获取依赖模块表
def getDependMods():
    modList, modFile = [], "depends.mod";
    if not os.path.exists(modFile):
        return modList;
    with open(modFile, "r") as f:
        for line in f.readlines():
            mod = line.strip();
            if mod not in modList:
                modList.append(mod);
    return modList;

# 初始化依赖信息文件
def initDependMap(pjPath):
    dirPath = os.path.join(pjPath, "data");
    filePath = os.path.join(dirPath, "depend_map.json");
    if not os.path.exists(dirPath):
        os.makedirs(dirPath);
    if not os.path.exists(filePath):
        dependMap = {};
        for mod in getDependMods():
            dependMap[mod] = 1;
        with open(filePath, "w") as f:
            f.write(json.dumps(dependMap));

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

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1); # 参数错误，直接退出
    pyExe, pjPath, isCheck = sys.argv[1], sys.argv[2], False;
    if len(sys.argv) > 3:
        isCheck = sys.argv[3]=="-check";
    # 初始化依赖信息文件
    initDependMap(pjPath);
    # 获取未安装模块
    unInstallMods = getUninstalledMods(pyExe);
    if isCheck and len(unInstallMods) > 0:
        sys.exit(2); # 有未安装模块
    # 安装未安装模块
    failedMods = installMods(pyExe, unInstallMods);
    if len(failedMods) > 0:
        print(f"{pyExe} -m pip install {failedMods} failed!");