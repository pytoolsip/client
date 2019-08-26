
@echo off && setlocal enabledelayedexpansion

set pyexe=%1
set mainpath=%2
set mainfile=%3
set pjpath=%4

start /d %mainpath% %pyexe% %mainfile% %pjpath%