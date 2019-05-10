@REM @Author: JinZhang
@REM @Date:   2018-04-19 17:16:41
@REM @Last Modified by:   JinZhang
@REM Modified time: 2019-05-10 17:13:17

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

rem 获取运行文件名
set mainFile="main.pyc"
if exist ..\assets\main.py (
	set mainFile="main.py"
)

rem 获取运行程序
set pythonExe="python"
if defined pypath (
	set pythonExe=%pypath%\python.exe
)

rem 判断是否安装了wxPython
for /f "tokens=2 delims=: " %%i in ('%pythonExe% -m pip show wxPython') do (
	if %%i==wxPython (
		goto existed
	)
)

:installwx
%pythonExe% -m pip install wxPython
for /f "tokens=2 delims=: " %%i in ('%pythonExe% -m pip show wxPython') do (
	if %%i==wxPython (
		goto existed
	)
)
set /p isInstall=Failed to install wxPython, do you try again ?(y/n):
if %isInstall%==y (
	goto installwx
) else (
	echo "Quit to install wxPython !"
	goto endRun
)

:existed
echo "Existed wxPython ."

cd ..\assets\

%pythonExe% %mainFile%

:endRun

pause