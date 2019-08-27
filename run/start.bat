@echo off && setlocal enabledelayedexpansion

set pyexe=%1
set assetspath=%2
set buildfile=%3
set mainfile=%4
set pjpath=%5
set runpath=%6

start /d %runpath% buildAndRun.vbs %pyexe% %assetspath% %buildfile% %mainfile% %pjpath%