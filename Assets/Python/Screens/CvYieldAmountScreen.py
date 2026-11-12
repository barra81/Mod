## WTP: dialog to enter the amount of goods to transfer (shift + transfer). It replaces the spin box popup of the game, which
## can neither be changed by Python nor gets mouse wheel or Page Up / Page Down: this one takes the keys and the mouse wheel.
## The DLL (CvDLLButtonPopup::launchSelectYieldAmountPopup) calls askYieldAmount in CvScreensInterface, the amount is sent back
## with CyGame().sendYieldTransfer.

from CvPythonExtensions import *
import CvUtil
import CvScreenEnums

gc = CyGlobalContext()
localText = CyTranslator()

BTN_MINUS = 40001
BTN_PLUS = 40002
BTN_MAX = 40003
BTN_OK = 40004
BTN_CANCEL = 40005

STEP = 25
STEP_CTRL = 50

# diagnosis of the events (WTP_Yield.log in the game folder): shows which event the mouse wheel sends
def logYield(szText):
	try:
		f = open("WTP_Yield.log", "a")
		f.write(szText + "\n")
		f.close()
	except:
		pass

class CvYieldAmountScreen:
	"Amount of goods to transfer"

	def __init__(self):
		self.SCREEN_NAME = "YieldAmountScreen"
		self.BACKGROUND_ID = "YAMBackground"
		self.W = 380
		self.H = 200
		self.iYield = -1
		self.iUnit = -1
		self.iMax = 0
		self.iData3 = -1
		self.bPlayerAction = False
		self.iFromPlayer = -1
		self.szValue = u""
		self.bSelected = True
		self.bFinished = True
		self.iLog = 0
		self.bHostMain = False
		self.iRefresh = 0
		self.pHost = None # the harbor screen (Europe / Africa / Port Royal) the dialog is drawn on, none: an own screen
		self.OX = 0
		self.OY = 0

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.YIELD_AMOUNT)

	def getKeyId(self, szName):
		iKey = getattr(InputTypes, szName, None)
		if iKey == None:
			return -12345
		return int(iKey)

	def getNotifyId(self, szName):
		iCode = getattr(NotifyCode, szName, None)
		if iCode == None:
			return -12345
		return int(iCode)

	# opens the dialog (1: it is open, 0: the DLL shows its own popup instead)
	def open(self, iYield, iUnit, iMax, iData3, bPlayerAction, iFromPlayer):
		screen = self.getScreen()
		if screen.isActive():
			return 0
		self.iYield = iYield
		self.iUnit = iUnit
		self.iMax = iMax
		self.iData3 = iData3
		self.bPlayerAction = bPlayerAction
		self.iFromPlayer = iFromPlayer # diplomacy: the player whose goods are traded, otherwise -1
		self.szValue = unicode(iMax)
		self.bSelected = True
		self.bFinished = False
		self.iLog = 0

		# a harbor screen (Europe / Africa / Port Royal) that is open would be closed by the game when another screen opens: the
		# dialog is drawn on that screen then (a screen of its own is used everywhere else)
		self.pHost = None
		try:
			import CvScreensInterface
			if CvScreensInterface.europeScreen.getScreen().isActive():
				self.pHost = CvScreensInterface.europeScreen.getScreen()
			elif CvScreensInterface.africaScreen.getScreen().isActive():
				self.pHost = CvScreensInterface.africaScreen.getScreen()
			elif CvScreensInterface.portroyalScreen.getScreen().isActive():
				self.pHost = CvScreensInterface.portroyalScreen.getScreen()
		except:
			self.pHost = None
		# everywhere else (the cities, the map) the dialog is drawn on the main interface: a screen of its own makes the city screen
		# show things that do not belong there (the minimap, the yellow ovals); the diplomacy has an own screen
		self.bHostMain = False
		if self.pHost == None and iFromPlayer < 0:
			self.pHost = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			self.bHostMain = True
			self.iRefresh = 0

		self.dDigits = {}
		for i in range(10):
			self.dDigits[self.getKeyId("KB_" + str(i))] = i
			self.dDigits[self.getKeyId("KB_NUMPAD" + str(i))] = i
		self.iKeyBack = self.getKeyId("KB_BACKSPACE")
		self.aKeyOk = [self.getKeyId("KB_RETURN"), self.getKeyId("KB_NUMPADENTER")]
		self.iKeyEsc = self.getKeyId("KB_ESCAPE")
		self.iKeyUp = self.getKeyId("KB_PGUP")
		self.iKeyDown = self.getKeyId("KB_PGDN")
		self.iKeyArrowUp = self.getKeyId("KB_UP")
		self.iKeyArrowDown = self.getKeyId("KB_DOWN")
		self.iWheelUp = self.getNotifyId("NOTIFY_MOUSEWHEELUP")
		self.iWheelDown = self.getNotifyId("NOTIFY_MOUSEWHEELDOWN")
		self.aWheelUp = [self.iWheelUp, self.getNotifyId("NOTIFY_SCROLL_UP")]
		self.aWheelDown = [self.iWheelDown, self.getNotifyId("NOTIFY_SCROLL_DOWN")]

		iXRes = screen.getXResolution()
		iYRes = screen.getYResolution()
		iX = (iXRes - self.W) / 2
		iY = (iYRes - self.H) / 2
		# where the dialog is drawn: in the diplomacy its bottom is at the lower edge of the portrait, in the cities (and on the map)
		# just above the goods bar, in the harbors it is moved up by more than its height
		if iFromPlayer >= 0:
			iY = int(iYRes * 0.597) - self.H
		if self.pHost == None:
			self.OX = 0
			self.OY = 0
			# (no setRenderInterfaceOnly: it would switch off the 3d views of the city screen; the keys come from CvEventManager.onKbdEvent)
			screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
			screen.setDimensions(iX, iY, self.W, self.H)
			screen.showWindowBackground(False)
		else:
			screen = self.pHost
			self.OX = (screen.getXResolution() - self.W) / 2
			if self.bHostMain:
				# just above the goods bar; in the city screen at the right, up to the golden frame of the panels there
				self.OY = int(screen.getYResolution() * 0.84) - self.H
				if CyInterface().isCityScreenUp():
					self.OX = int(screen.getXResolution() * 0.592) - self.W
			else:
				self.OY = int(screen.getYResolution() * 0.305) # the harbors: a little above the landing stage
		screen.addPanel(self.BACKGROUND_ID, u"", u"", True, False, self.OX, self.OY, self.W, self.H, PanelStyles.PANEL_STYLE_MAIN, WidgetTypes.WIDGET_GENERAL, -1, -1)

		szTitle = localText.getText("TXT_KEY_SELECT_YIELD_POPUP", (gc.getYieldInfo(iYield).getDescription(),))
		screen.setLabelAt("YAMTitle", self.BACKGROUND_ID, u"<font=3>" + szTitle + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W / 2, 24, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel("YAMValueBG", u"", u"", False, False, self.OX + self.W / 2 - 70, self.OY + 44, 140, 36, PanelStyles.PANEL_STYLE_IN, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iButtonW = 86
		iGap = 10
		iRowX = (self.W - 3 * iButtonW - 2 * iGap) / 2
		screen.setButtonGFC("YAMMinus", u"<font=2>-" + unicode(STEP) + u"</font>", "", self.OX + iRowX, self.OY + 92, iButtonW, 26, WidgetTypes.WIDGET_GENERAL, BTN_MINUS, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("YAMPlus", u"<font=2>+" + unicode(STEP) + u"</font>", "", self.OX + iRowX + iButtonW + iGap, self.OY + 92, iButtonW, 26, WidgetTypes.WIDGET_GENERAL, BTN_PLUS, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("YAMMax", u"<font=2>" + localText.getText("TXT_KEY_WTP_YIELD_AMOUNT_MAX", ()) + u"</font>", "", self.OX + iRowX + 2 * (iButtonW + iGap), self.OY + 92, iButtonW, 26, WidgetTypes.WIDGET_GENERAL, BTN_MAX, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		screen.setLabelAt("YAMHintA", self.BACKGROUND_ID, u"<font=2>" + localText.getText("TXT_KEY_WTP_YIELD_AMOUNT_HINT1", ()) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W / 2, 130, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt("YAMHintB", self.BACKGROUND_ID, u"<font=2>" + localText.getText("TXT_KEY_WTP_YIELD_AMOUNT_HINT2", ()) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W / 2, 148, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setButtonGFC("YAMOk", u"<font=2>" + localText.getText("TXT_KEY_MAIN_MENU_OK", ()) + u"</font>", "", self.OX + self.W / 2 - 105, self.OY + self.H - 36, 100, 28, WidgetTypes.WIDGET_GENERAL, BTN_OK, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("YAMCancel", u"<font=2>" + localText.getText("TXT_KEY_POPUP_CANCEL", ()) + u"</font>", "", self.OX + self.W / 2 + 5, self.OY + self.H - 36, 100, 28, WidgetTypes.WIDGET_GENERAL, BTN_CANCEL, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		self.drawValue()
		self.refreshView()
		try:
			CyGame().setWheelCapture(True)
		except:
			pass
		return 1

	def refreshView(self):
		# ask the interface to redraw the parts that show artifacts (minimap, ovals) in the city screen
		if not self.bHostMain:
			return
		# the minimap and the yellow ovals of the city screen are hidden by the hide states of the main interface: apply them again
		try:
			import CvScreensInterface
			CvScreensInterface.mainInterface.updateMiscButtons()
		except:
			pass
		for szBit in ("Minimap_Section_DIRTY_BIT", "MiscButtons_DIRTY_BIT", "Help_DIRTY_BIT", "InfoPane_DIRTY_BIT"):
			try:
				CyInterface().setDirty(getattr(InterfaceDirtyBits, szBit), True)
			except:
				pass

	def getDrawScreen(self):
		if self.pHost != None:
			return self.pHost
		return self.getScreen()

	def isEmbedded(self):
		return self.pHost != None

	def drawValue(self):
		screen = self.getDrawScreen()
		if self.bSelected:
			szText = u"<color=255,220,100>" + self.szValue + u"</color>"
		else:
			szText = u"<color=255,255,255>" + self.szValue + u"</color><color=255,220,100>|</color>"
		screen.setLabelAt("YAMValue", self.BACKGROUND_ID, u"<font=3b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W / 2, 50, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.show("YAMValue")

	def getValue(self):
		if len(self.szValue) == 0:
			return 0
		return int(self.szValue)

	def setValue(self, iValue):
		iValue = max(1, min(self.iMax, iValue))
		self.szValue = unicode(iValue)
		self.bSelected = False
		self.drawValue()

	def step(self, iDirection, bCtrl):
		iStep = STEP
		if bCtrl:
			iStep = STEP_CTRL
		self.setValue(self.getValue() + iDirection * iStep)

	def isOpen(self):
		return not self.bFinished

	def releaseWheel(self):
		try:
			CyGame().setWheelCapture(False)
		except:
			pass

	def finish(self, bOk):
		if self.bFinished:
			return
		self.bFinished = True
		self.releaseWheel()
		if bOk:
			iAmount = max(1, min(self.iMax, self.getValue()))
			try:
				if self.iFromPlayer >= 0:
					gc.getPlayer(self.iFromPlayer).setDiploYieldAmount(self.iYield, iAmount) # (as the popup of the diplomacy did)
				else:
					CyGame().sendYieldTransfer(self.iUnit, self.iData3, self.iYield, iAmount, self.bPlayerAction)
			except:
				import traceback
				logYield(traceback.format_exc())
		if self.pHost == None:
			self.getScreen().hideScreen()
		else:
			# drawn on a harbor screen: the widgets are removed again
			try:
				for szName in ("YAMValue", "YAMTitle", "YAMHintA", "YAMHintB", "YAMValueBG", "YAMMinus", "YAMPlus", "YAMMax", "YAMOk", "YAMCancel", self.BACKGROUND_ID):
					self.pHost.deleteWidget(szName)
			except:
				import traceback
				logYield(traceback.format_exc())
			self.refreshView()
			self.pHost = None

	# a key down event (CvEventManager.onKbdEvent gives them to the dialog while it is open)
	def handleKey(self, iKey, bCtrl):
		if self.dDigits.has_key(iKey):
			if self.bSelected:
				self.szValue = u""
			self.bSelected = False
			self.szValue = self.szValue + unicode(self.dDigits[iKey])
			if self.getValue() > self.iMax:
				self.szValue = unicode(self.iMax)
			self.szValue = unicode(self.getValue())
			if self.szValue == u"0":
				self.szValue = u""
			self.drawValue()
		elif iKey == self.iKeyBack:
			if self.bSelected:
				self.szValue = u""
			else:
				self.szValue = self.szValue[:-1]
			self.bSelected = False
			self.drawValue()
		elif iKey == self.iKeyUp:
			self.step(1, bCtrl)
		elif iKey == self.iKeyDown:
			self.step(-1, bCtrl)
		elif iKey == self.iKeyArrowUp:
			self.setValue(self.getValue() + 1)
		elif iKey == self.iKeyArrowDown:
			self.setValue(self.getValue() - 1)
		elif iKey in self.aKeyOk:
			if len(self.szValue) > 0:
				self.finish(True)
		elif iKey == self.iKeyEsc:
			self.finish(False)

	# the clicks on the buttons of the dialog when it is drawn on a harbor screen (CvScreensInterface.handleInput gives them here);
	# returns 1 if the event was for the dialog
	def handleEmbeddedInput(self, inputClass):
		if int(inputClass.getNotifyCode()) != int(NotifyCode.NOTIFY_CLICKED) or inputClass.getButtonType() != WidgetTypes.WIDGET_GENERAL:
			return 0
		iData = inputClass.getData1()
		if iData < BTN_MINUS or iData > BTN_CANCEL:
			return 0
		self.handleInput(inputClass)
		return 1

	def handleInput(self, inputClass):
		iCode = int(inputClass.getNotifyCode())
		if iCode == int(NotifyCode.NOTIFY_CHARACTER):
			return 0 # (the keys are handled in CvEventManager.onKbdEvent)
		if iCode in self.aWheelUp:
			self.step(1, inputClass.isCtrlKeyDown())
			return 0
		if iCode in self.aWheelDown:
			self.step(-1, inputClass.isCtrlKeyDown())
			return 0
		if iCode == int(NotifyCode.NOTIFY_CLICKED):
			if inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL:
				iData = inputClass.getData1()
				if iData == BTN_MINUS:
					self.step(-1, inputClass.isCtrlKeyDown())
				elif iData == BTN_PLUS:
					self.step(1, inputClass.isCtrlKeyDown())
				elif iData == BTN_MAX:
					self.setValue(self.iMax)
				elif iData == BTN_OK:
					if len(self.szValue) > 0:
						self.finish(True)
				elif iData == BTN_CANCEL:
					self.finish(False)
			return 0
		# the other events are logged (the first ones): this shows what the mouse wheel sends if it is none of the codes above
		if self.iLog < 60 and iCode != int(NotifyCode.NOTIFY_CURSOR_MOVE_ON) and iCode != int(NotifyCode.NOTIFY_CURSOR_MOVE_OFF):
			self.iLog += 1
			logYield("event code %d name '%s' button %d data %d/%d" % (iCode, inputClass.getFunctionName(), int(inputClass.getButtonType()), inputClass.getData1(), inputClass.getData2()))
		return 0

	# the mouse wheel (collected by the DLL while the dialog is open)
	def update(self, fDelta):
		if self.bFinished:
			return 0
		try:
			if self.pHost != None and not self.bHostMain and not self.pHost.isActive():
				self.finish(False) # the harbor screen was closed meanwhile
				return 0
			if self.bHostMain and self.iRefresh < 6:
				# the engine shows the minimap again a moment after the dialog was drawn: hide it again for a few updates
				self.iRefresh += 1
				self.refreshView()
			iNotches = CyGame().takeWheelNotches()
			if iNotches != 0:
				bCtrl = CyGame().isCtrlKeyPressed()
				if self.iLog < 60:
					self.iLog += 1
					logYield("wheel notches %d" % iNotches)
				for i in range(abs(iNotches)):
					if iNotches > 0:
						self.step(1, bCtrl)
					else:
						self.step(-1, bCtrl)
		except:
			pass
		return 0

	def onClose(self):
		self.bFinished = True
		self.releaseWheel()
		return 0
