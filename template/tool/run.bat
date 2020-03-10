@echo off && setlocal enabledelayedexpansion

REM 初始化默认环境变量
set pyexe=python
set mainfile=main.py
set buildfile=build.py

REM 读取环境配置
for /f "tokens=1,2 delims==" %%i in (_tool.env) do (
    if "%%i"=="pyexe" set pyexe=%%j
    if "%%i"=="mainfile" set mainfile=%%j
    if "%%i"=="buildfile" set buildfile=%%j
)

echo %pyexe% %buildfile% %mainfile%

REM 进入资源层
cd .\assets

REM 校验模块
%pyexe% %buildfile% %pyexe%

REM 运行程序
%pyexe% %mainfile% %pyexe%

REM 运行结束后保留cmd窗口
REM pause