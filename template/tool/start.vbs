' 获取Wscript脚本对象
Set ws = CreateObject("Wscript.Shell")
' 启动运行程序
ws.run "cmd /c start.bat",0