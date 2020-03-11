import sys,os,subprocess,json,re;

# 无日志打印运行命令
def runCmd(cmd, cwd=os.getcwd(), funcName="call", argDict = {}):
    startupinfo = subprocess.STARTUPINFO();
    startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW;
    startupinfo.wShowWindow = subprocess.SW_HIDE;
    return getattr(subprocess, funcName)(cmd, cwd = cwd, startupinfo = startupinfo, **argDict);

# 获取依赖模块表
def getDependMods():
    modList, modFileList = [], ["depends.mod", "common/depends.mod"];
    for modFile in modFileList:
        if not os.path.exists(modFile):
            continue;
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
    if os.path.isfile(pyExe):
        pyExe = os.path.abspath(pyExe);
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
def installMods(pyExe, mods, pjPath):
    failedMods = [];
    pii = getPipInstallImage(pjPath);
    for mod in mods:
        cmd = getPipInstallCmd(pyExe, mod, pii);
        if subprocess.call(cmd) != 0:
            failedMods.append(mod);
    return failedMods;

# 获取pip安装镜像
def getPipInstallImage(pjPath):
    settingCfg = {};
    cfgPath = os.path.join(pjPath, "data", "config", "setting_cfg.json");
    if os.path.exists(cfgPath):
        with open(cfgPath, "rb") as f:
            settingCfg = json.loads(f.read().decode("utf-8"));
    return settingCfg.get("pip_install_image", "");

# 获取pip安装命令
def getPipInstallCmd(pyExe, mod, pii):
    if os.path.isfile(pyExe):
        pyExe = os.path.abspath(pyExe);
    cmd = f"{pyExe} -m pip install {mod}";
    # 处理镜像
    if pii:
        cmd += f" -i {pii}";
        mtObj = re.match("^https?://(.*)/.*$", pii);
        if mtObj:
            host = mtObj.group(1);
            cmd += f" --trusted-host {host}";
    return cmd;

# 升级pip安装命令
def upgradePip(pyExe, pjPath):
    pii = getPipInstallImage(pjPath);
    cmd = getPipInstallCmd(pyExe, "--upgrade pip", pii);
    runCmd(cmd);

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
        upgradePip(pyExe, pjPath); # 静默升级pip
        sys.exit(2); # 有未安装模块
    # 安装未安装模块
    if len(unInstallMods) > 0:
        print(f"Start installing dependent modules -> {unInstallMods}...");
        failedMods = installMods(pyExe, unInstallMods, pjPath);
        if len(failedMods) > 0:
            print(f"{pyExe} -m pip install {failedMods} failed!");
    pass;