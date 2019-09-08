@echo off && setlocal enabledelayedexpansion

set pyexe=%1
set assetspath=%2
set buildfile=%3
set pjpath=%4
set ischeck=%5

cd %assetspath%
%pyexe% %buildfile% %pyexe% %pjpath% %ischeck%

if %errorlevel% neq 0 (
    exit %errorlevel%
)