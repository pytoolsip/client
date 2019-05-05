@REM @Author: JinZhang
@REM @Date:   2018-04-19 17:16:41
@REM @Last Modified by:   JimZhang
@REM Modified time: 2019-05-06 00:33:48

@echo off && setlocal enabledelayedexpansion

set so=
set pypath=

for /f "delims=" %%a in (config.ini) do (
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

if defined pypath (
	%pypath%\python.exe main.py
) else (
	python main.py
)

pause