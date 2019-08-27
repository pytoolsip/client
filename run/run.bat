
@echo off && setlocal enabledelayedexpansion

set pyexe=%1
set assetspath=%2
set mainfile=%3
set pjpath=%4

cd %assetspath%
%pyexe% %mainfile% %pjpath%