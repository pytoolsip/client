' 校验参数个数
if WScript.Arguments.Count < 5 Then
    MsgBox "Error Arguments!"
End If

' 获取参数
Dim pyexe,updatefile,version,projectpath,updatepath
pyexe = " " + WScript.Arguments(0)
updatefile = " " + WScript.Arguments(1)
version = " " + WScript.Arguments(2)
projectpath = " " + WScript.Arguments(3)
updatepath = " " + WScript.Arguments(4)

' 获取Wscript脚本对象
Set ws = CreateObject("Wscript.Shell")

' 启动运行程序
Dim args
args = pyexe+updatefile+version+projectpath+updatepath
ws.run "cmd /c update.bat"+args, 0