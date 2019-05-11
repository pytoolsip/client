
@echo off && setlocal enabledelayedexpansion

set pyexe=%1
set mainpath=%2
set mainfile=%3

cd /d %mainpath%

%pyexe% %mainfile%