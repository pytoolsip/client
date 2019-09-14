# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-10-09 22:41:23
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-03-16 13:46:29

import wx;

from _Global import _GG;
from function.base import *;

class LauncherWindowUI(wx.Frame):
	"""docstring for LauncherWindowUI"""
	def __init__(self, parent, id = -1, title = "", pos = (0,0), size = (0,0), style = wx.DEFAULT_FRAME_STYLE, curPath = "", windowCtr = None):
		super(LauncherWindowUI, self).__init__(parent, id, title = title, pos = pos, size = size, style = style);
		self._className_ = LauncherWindowUI.__name__;
		self._curPath = curPath;
		self.__windowCtr = windowCtr;

	def getCtr(self):
		return self.__windowCtr;

	def initWindow(self):
		self.initIcon();
		self.createViewCtrs();
		self.initWindowLayout();
		self.Centre();
		self.Show(True);
		pass;

	def initIcon(self):
		self.SetIcon(wx.Icon(_GG("g_CommonPath")+"res/img/dzjh.ico", wx.BITMAP_TYPE_ICO));

	def createViewCtrs(self):
		self.getCtr().createCtrByKey("LauncherGaugeView", _GG("g_AssetsPath") + "launcher/view/LauncherGaugeView", params = {"size" : (self.GetSize()[0], -1)}); # , parent = self, params = {}
		self.createTitle();
		self.createReverifyButton();
		self.createDetailTextCtrl();
		self.createCopyrightInfo();
		pass;

	def initWindowLayout(self):
		hbox = wx.BoxSizer(wx.HORIZONTAL);
		vbox = wx.BoxSizer(wx.VERTICAL);
		vbox.Add(self.title, 0, wx.ALIGN_CENTER|wx.TOP, 40);
		vbox.Add(self.reverifyButton, 0, wx.ALIGN_CENTER|wx.TOP, 40)
		vbox.Add(self.getCtr().getUIByKey("LauncherGaugeView"), 0, wx.ALIGN_CENTER);
		vbox.Add(self.detailTextCtrl, 0, wx.ALIGN_CENTER|wx.TOP, 10)
		vbox.Add(self.copyrightInfo, 0, wx.ALIGN_CENTER|wx.TOP, 4);
		hbox.Add(vbox, 0, wx.ALIGN_TOP|wx.LEFT|wx.RIGHT, 20);
		self.SetSizer(hbox);
		pass;

	def updateWindow(self, data):
		pass;

	def createTitle(self):
		self.title = wx.StaticText(self, label = _GG("AppConfig")["AppTitle"], style = wx.ALIGN_CENTER);
		font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD);
		self.title.SetFont(font);

	def createReverifyButton(self):
		self.reverifyButton = wx.Button(self, label = u"重新校验", size = (-1, 32));
		self.reverifyButton.Bind(event = wx.EVT_BUTTON, handler = self.getCtr().onReverifyButton);
		wx.CallAfter(self.showReverifyButton, False);

	def createDetailTextCtrl(self):
		self.detailTextCtrl = wx.TextCtrl(self, value = "", size = (self.GetSize().x, 160), style = wx.TE_READONLY|wx.TE_MULTILINE);
		wx.CallAfter(self.showDetailTextCtrl, False);

	def createCopyrightInfo(self):
		self.copyrightInfo = wx.StaticText(self, label = _GG("AppConfig")["CopyrightInfo"], style = wx.ALIGN_CENTER);

	def showReverifyButton(self, isShow = True):
		self.reverifyButton.Show(isShow);

	def showDetailTextCtrl(self, isShow = True, text = "", isReset = False):
		self.detailTextCtrl.Show(isShow);
		if isShow and text != "":
			if isReset:
				self.detailTextCtrl.SetValue(text);
			else:
				if self.detailTextCtrl.GetValue():
					text = "\n" + text;
				self.detailTextCtrl.AppendText(text);
		elif isReset:
			self.detailTextCtrl.SetValue("");