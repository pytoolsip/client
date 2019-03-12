# -*- coding: utf-8 -*-
# @Author: JimZhang
# @Date:   2018-12-02 13:33:13
# @Last Modified by:   JimDreamHeart
# @Last Modified time: 2019-01-12 12:00:45

import math;
import wx;
from enum import Enum, unique;

from _Global import _GG;
from function.base import *;

@unique
class Direction(Enum):
	LEFT = 0;
	TOP = 1;
	RIGHT = 2;
	BOTTOM = 3;


class KlotskiViewUI(wx.Panel):
	"""docstring for KlotskiViewUI"""
	def __init__(self, parent, id = -1, curPath = "", viewCtr = None, params = {}):
		self.initParams(params);
		super(KlotskiViewUI, self).__init__(parent, id, pos = self.__params["pos"], size = self.__params["size"], style = self.__params["style"]);
		self.className_ = KlotskiViewUI.__name__;
		self.curPath = curPath;
		self.viewCtr = viewCtr;
		self.__playing, self.curPos, self.curItem = False, None, None;
		self.SetBackgroundColour(self.__params["bgColour"]);

	def initParams(self, params):
		# 初始化参数
		self.__params = {
			"pos" : (0,0),
			"size" : (400,400),
			"style" : wx.BORDER_THEME,
			"matrix" : (4,4),
			"bgColour" : "grey",
			"respDist" : 10, # 移动元素的响应距离
		};
		for k,v in params.items():
			self.__params[k] = v;

	def getCtr(self):
		return self.viewCtr;

	def initView(self):
		self.__playing = True; # 游戏状态标记
		self.createControls(); # 创建控件
		self.initViewLayout(); # 初始化布局

	def createControls(self):
		# self.getCtr().createCtrByKey("key", self.curPath + "***View"); # , parent = self, params = {}
		self.createCaoCao();
		self.createZhangFei();
		self.createZhaoYun();
		self.createGuanYu();
		self.createSoldiers();
		pass;
		
	def initViewLayout(self):
		bagSizer = wx.GridBagSizer(0,0);
		bagSizer.Add(self.ZhangFei, pos = (0,0), span = (2,1));
		bagSizer.Add(self.CaoCao, pos = (0,1), span = (2,2));
		bagSizer.Add(self.ZhaoYun, pos = (0,3), span = (2,1));
		bagSizer.Add(self.GuanYu, pos = (2,1), span = (1,2));
		bagSizer.Add(self.Soldiers[0], pos = (2,0), span = (1,1));
		bagSizer.Add(self.Soldiers[1], pos = (2,3), span = (1,1));
		bagSizer.Add(self.Soldiers[2], pos = (3,0), span = (1,1));
		bagSizer.Add(self.Soldiers[3], pos = (3,3), span = (1,1));
		self.SetSizerAndFit(bagSizer);
		pass;

	def createCaoCao(self):
		self.CaoCao = self.createItem((self.GetSize().x/2, self.GetSize().y/2), "曹操", "white");

	def createZhangFei(self):
		self.ZhangFei = self.createItem((self.GetSize().x/4, self.GetSize().y/2), "张飞", "green");

	def createZhaoYun(self):
		self.ZhaoYun = self.createItem((self.GetSize().x/4, self.GetSize().y/2), "赵云", "yellow");

	def createGuanYu(self):
		self.GuanYu = self.createItem((self.GetSize().x/2, self.GetSize().y/4), "关羽", "red");

	def createSoldiers(self):
		self.Soldiers = [];
		for i in range(0,4):
			soldier = self.createItem((self.GetSize().x/4, self.GetSize().y/4), "兵", "blue");
			self.Soldiers.append(soldier);

	def createItem(self, size, label, colour):
		p = wx.Panel(self, size = size, style = wx.BORDER_THEME);
		p.SetBackgroundColour(colour);
		t = wx.StaticText(p, label = label);
		t.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD));
		b = wx.BoxSizer(wx.VERTICAL);
		b.Add(t, flag = wx.ALIGN_CENTER|wx.TOP, border = (p.GetSize().y - t.GetSize().y) / 2)
		p.SetSizer(b);
		p.Layout();
		# 绑定事件
		self.bindEventToItem(p, t);
		return p;

	def bindEventToItem(self, item, text):
		# 绑定item的相关事件
		item.Bind(wx.EVT_LEFT_DOWN, self.onClick);
		item.Bind(wx.EVT_MOTION, self.onMotion);
		# 绑定text的相关事件
		def onClickText(event):
			self.onClick(event, item);
		text.Bind(wx.EVT_LEFT_DOWN, onClickText);
		text.Bind(wx.EVT_MOTION, self.onMotion);

	def onClick(self, event, item = None):
		if self.__playing:
			self.curPos = event.GetPosition();
			self.curItem = item;
			if not self.curItem:
				self.curItem = event.GetEventObject()
			event.Skip();
		else:
			# 显示游戏结束信息弹窗
			self.showMessageDialog("请重新开始游戏！", "游戏已结束");

	def onMotion(self, event):
		if event.Dragging() and event.LeftIsDown() and self.__playing and self.curPos:
			pos = event.GetPosition() - self.curPos;
			direction = None;
			respDist = self.__params["respDist"];
			fabsX, fabsY = math.fabs(pos.x), math.fabs(pos.y);
			if fabsX > respDist or fabsY > respDist:
				self.curPos = None;
				if fabsX < fabsY:
					direction = pos.y < 0 and Direction.TOP or Direction.BOTTOM;
				else:
					direction = pos.x < 0 and Direction.LEFT or Direction.RIGHT;
				# 移动Item
				self.moveItem(self.curItem, direction);

	def moveItem(self, item, direction):
		try:
			pos = self.GetSizer().GetItemPosition(item);
			span = self.GetSizer().GetItemSpan(item);
			isLayout = False;
			if direction == Direction.LEFT:
				if pos[1] > 0 :
					isLayout = True;
					self.GetSizer().SetItemPosition(item, wx.GBPosition(pos[0], pos[1] - 1));
			elif direction == Direction.TOP:
				if pos[0] > 0 :
					isLayout = True;
					self.GetSizer().SetItemPosition(item, wx.GBPosition(pos[0] - 1, pos[1]));
			elif direction == Direction.RIGHT:
				if pos[1] + span[1] < self.__params["matrix"][1]:
					isLayout = True;
					self.GetSizer().SetItemPosition(item, wx.GBPosition(pos[0], pos[1] + 1));
			elif direction == Direction.BOTTOM:
				if pos[0] + span[0] < self.__params["matrix"][0]:
					isLayout = True;
					self.GetSizer().SetItemPosition(item, wx.GBPosition(pos[0] + 1, pos[1]));
			if isLayout:
				self.GetSizer().Layout();
				self.checkGameOver();
		except Exception:
			pass;

	def resetView(self):
		self.GetSizer().Clear(True);
		self.SetSize(self.__params["size"]);
		self.initView();

	def checkGameOver(self):
		pos = self.GetSizer().GetItemPosition(self.CaoCao);
		span = self.GetSizer().GetItemSpan(self.CaoCao);
		if (pos[0] + span[0] == self.__params["matrix"][0]) and (pos[1] + span[1] == self.__params["matrix"][1] - 1):
			# 回调游戏结束方法
			if hasattr(self, "onGameOver"):
				self.onGameOver();
			# 显示游戏结束信息弹窗
			self.showMessageDialog("恭喜逃出华容道~", "游戏结束");
			# 重置游戏状态
			self.__playing = False;

	def showMessageDialog(self, message, caption):
		msgDialog = wx.MessageDialog(self, message, caption, style = wx.OK|wx.ICON_INFORMATION);
		msgDialog.ShowModal();