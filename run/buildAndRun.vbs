' 校验参数个数
if WScript.Arguments.Count < 5 Then
    MsgBox "Error Arguments!"
End If

' 获取参数
Dim pyexe,assetspath,buildfile,mainfile,pjpath
pyexe = " " + WScript.Arguments(0)
assetspath = " " + WScript.Arguments(1)
buildfile = " " + WScript.Arguments(2)
mainfile = " " + WScript.Arguments(3)
pjpath = " " + WScript.Arguments(4)

' 获取Wscript脚本对象
Set ws = CreateObject("Wscript.Shell")

' 校验依赖模块
Dim args1
args1 = pyexe+assetspath+buildfile
if ws.Run("cmd /c build.bat"+args1+" -check", 0, True) = 2 Then
    ws.run "cmd /c build.bat"+args1, 1, True
End If

' 启动运行程序
Dim args2
args2 = pyexe+assetspath+mainfile+pjpath
ws.run "cmd /c run.bat"+args2,0