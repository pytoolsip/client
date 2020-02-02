@echo off && setlocal enabledelayedexpansion

set pyexe=%1
set updatefile=%2
set version=%3
set projectpath=%4
set updatepath=%5
set runpath=%6

start /d %runpath% update.vbs %pyexe% %updatefile% %version% %projectpath% %updatepath%