' 校验参数个数
if WScript.Arguments.Count < 2 Then
    MsgBox "Error Arguments!"
End If

' 获取参数
Dim pyexe,mainfile
pyexe = " " + WScript.Arguments(0)
mainfile = " " + WScript.Arguments(1)

' 获取Wscript脚本对象
Set ws = CreateObject("Wscript.Shell")
' 启动运行程序
ws.run "cmd /c run.bat"+pyexe+mainfile