@REM @Author: JinZhang
@REM @Date:   2018-04-19 17:16:41
@REM @Last Modified by:   JinZhang
@REM Modified time: 2019-05-10 20:11:19

@echo off && setlocal enabledelayedexpansion

rem 获取python路径
set so=
set pypath=
for /f "delims=" %%a in (..\assets\common\config\ini\config.ini) do (
	set v=%%a
	if "!v:~0,1!"=="[" (
		if %%a==[env] (
			set so=1
		) else (
			set so=
		)
	) else (
		if defined so (
			for %%b in (%%a) do (
				if %%b==python (
					set so=2
				) else (
					if !so!==2 (
						set pypath=%%b&&goto readover
					)
				)
			)
		)
	)
)

:readover

cd ..\assets\

rem 获取运行程序
set pythonExe="python"
if defined pypath (
	set pythonExe=%pypath%\python.exe
)

rem 获取运行文件名
set mainFile="main.pyc"
if exist ..\assets\main.py (
	set mainFile="main.py"
)

rem 获取构建依赖文件名
set buildFile="build.pyc"
if exist ..\assets\build.py (
	set buildFile="build.py"
)

:installModules
rem 安装依赖模块
set mods=wxPython grpcio protobuf grpcio-tools
%pythonExe% %buildFile% %pythonExe% %mods%
rem 判断是否安装了依赖模块
set flag=
for %%a in (%mods%) do (
	for /f "tokens=1,2 delims=: " %%i in ('%pythonExe% -m pip show %%a') do (
		if %%i==Name (
			if %%j==%%a (
				set flag=1
			)
		)
	)
	if defined flag (
		set flag=
	) else (
		goto askAgain
	)
)

%pythonExe% %mainFile%
goto endRun

:askAgain
set /p isInstall=Failed to install %mods%, do you try again ?(y/n):
if %isInstall%==y (
	goto installModules
) else (
	echo "Quit to install %mods% !"
)

:endRun

pause