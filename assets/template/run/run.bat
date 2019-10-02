@REM @Author: JinZhang
@REM @Date:   2018-04-19 17:16:41
@REM @Last Modified by:   JimDreamHeart
@REM Modified time: 2018-11-24 10:44:48

@echo off && setlocal enabledelayedexpansion

set pyexe=%1
set mainfile=%2
set buildfile=%3

cd ..\assets\

%pyexe% %buildfile% %pyexe%

%pyexe% %mainfile% %pyexe%

pause
