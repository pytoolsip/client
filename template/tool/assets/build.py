import sys,os,subprocess,json,re;

# 无日志打印运行命令
def runCmd(cmd, cwd=os.getcwd(), funcName="call", argDict = {}):
    startupinfo = subprocess.STARTUPINFO();
    startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW;
    startupinfo.wShowWindow = subprocess.SW_HIDE;
    return getattr(subprocess, funcName)(cmd, cwd = cwd, startupinfo = startupinfo, **argDict);

# 分割等号
def splitEqualSign(modstr):
    modstr = modstr.strip();
    if modstr.find("=") != -1:
        if modstr.find("==") != -1:
            return tuple(modstr.split("=="));
        return tuple(modstr.split("="));
    return (modstr, "");

# 获取依赖模块表
def getDependMods():
    modList, modFileList = [], ["tool/depends.mod", "common/depends.mod"];
    for modFile in modFileList:
        if not os.path.exists(modFile):
            continue;
        with open(modFile, "r") as f:
            for line in f.readlines():
                mod = splitEqualSign(line.strip());
                if mod not in modList:
                    modList.append(mod);
    return modList;

# 获取已安装模块
def getInstalledModMap(pyExe):
    modMap = {};
    if os.path.isfile(pyExe):
        pyExe = os.path.abspath(pyExe);
    ret = runCmd(f"{pyExe} -m pip freeze", funcName = "check_output");
    for line in ret.decode().split("\n"):
        line = line.strip();
        if line:
            mod = splitEqualSign(line);
            modMap[mod[0]] = mod[1];
    return modMap;

# 获取未安装模块
def getUninstalledMods(pyExe):
    modMap = getInstalledModMap(pyExe); # 获取已安装模块
    unInstallMods = [];
    for mod, ver in getDependMods():
        if mod not in modMap:
            unInstallMods.append((mod, ver));
        elif ver and ver != modMap[mod]:
            print(f"Mismatched version requirements: mod[{mod}], installed[{modMap[mod]}], required[{ver}]!");
    return unInstallMods;

# 安装模块
def installMods(pyExe, mods, pii = ""):
    failedMods = [];
    for mod in mods:
        cmd = getPipInstallCmd(pyExe, mod, pii);
        if subprocess.call(cmd) != 0:
            failedMods.append(mod);
    return failedMods;

# 获取pip安装命令
def getPipInstallCmd(pyExe, mod, pii = ""):
    if os.path.isfile(pyExe):
        pyExe = os.path.abspath(pyExe);
    cmd = f"{pyExe} -m pip install {mod[0]}";
    if mod[1]: # 安装版本号
        cmd += f"=={mod[1]}";
    # 处理镜像
    if pii:
        cmd += f" -i {pii}";
        mtObj = re.match("^https?://(.*)/.*$", pii);
        if mtObj:
            host = mtObj.group(1);
            cmd += f" --trusted-host {host}";
    return cmd;

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1); # 参数错误，直接退出
    pyExe = sys.argv[1]; # python程序
    pii = ""; # pip安装镜像
    if len(sys.argv) > 2:
        pii = sys.argv[2];
    # 获取未安装模块
    unInstallMods = getUninstalledMods(pyExe);
    # 安装未安装模块
    if len(unInstallMods) > 0:
        print(f"Start installing dependent modules -> {unInstallMods}...");
        failedMods = installMods(pyExe, unInstallMods, pii);
        if len(failedMods) > 0:
            print(f"{pyExe} -m pip install {failedMods} failed!");
    pass;