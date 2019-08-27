@echo off && setlocal enabledelayedexpansion

set pyexe=%1
set assetspath=%2
set buildfile=%3
set ischeck=%4

cd %assetspath%
%pyexe% %buildfile% %pyexe% %ischeck%

if %errorlevel% neq 0 (
    exit %errorlevel%
)