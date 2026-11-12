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
		self.W = 640
		self.H = 330
		self.iYield = -1
		self.iUnit = -1
		self.iMax = 0
		self.iData3 = -1
		self.bPlayerAction = False
		self.szValue = u""
		self.bSelected = True
		self.bFinished = True
		self.iLog = 0

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
	def open(self, iYield, iUnit, iMax, iData3, bPlayerAction):
		screen = self.getScreen()
		if screen.isActive():
			return 0
		self.iYield = iYield
		self.iUnit = iUnit
		self.iMax = iMax
		self.iData3 = iData3
		self.bPlayerAction = bPlayerAction
		self.szValue = unicode(iMax)
		self.bSelected = True
		self.bFinished = False
		self.iLog = 0

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
		screen.setRenderInterfaceOnly(True) # (as the screens that get keyboard input)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setDimensions(iX, iY, self.W, self.H)
		screen.showWindowBackground(False)
		screen.addPanel(self.BACKGROUND_ID, u"", u"", True, False, 0, 0, self.W, self.H, PanelStyles.PANEL_STYLE_MAIN, WidgetTypes.WIDGET_GENERAL, -1, -1)

		szTitle = localText.getText("TXT_KEY_SELECT_YIELD_POPUP", (gc.getYieldInfo(iYield).getDescription(),))
		screen.setLabelAt("YAMTitle", self.BACKGROUND_ID, u"<font=3b>" + szTitle + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W / 2, 28, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel("YAMValueBG", u"", u"", False, False, self.W / 2 - 120, 62, 240, 60, PanelStyles.PANEL_STYLE_IN, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iButtonW = 130
		iRowX = (self.W - 3 * iButtonW - 2 * 20) / 2
		screen.setButtonGFC("YAMMinus", u"<font=3b>-" + unicode(STEP) + u"</font>", "", iRowX, 140, iButtonW, 34, WidgetTypes.WIDGET_GENERAL, BTN_MINUS, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("YAMPlus", u"<font=3b>+" + unicode(STEP) + u"</font>", "", iRowX + iButtonW + 20, 140, iButtonW, 34, WidgetTypes.WIDGET_GENERAL, BTN_PLUS, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("YAMMax", u"<font=3b>" + localText.getText("TXT_KEY_WTP_YIELD_AMOUNT_MAX", ()) + u"</font>", "", iRowX + 2 * (iButtonW + 20), 140, iButtonW, 34, WidgetTypes.WIDGET_GENERAL, BTN_MAX, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		screen.setLabelAt("YAMHintA", self.BACKGROUND_ID, u"<font=2>" + localText.getText("TXT_KEY_WTP_YIELD_AMOUNT_HINT1", ()) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W / 2, 196, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt("YAMHintB", self.BACKGROUND_ID, u"<font=2>" + localText.getText("TXT_KEY_WTP_YIELD_AMOUNT_HINT2", ()) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W / 2, 222, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setButtonGFC("YAMOk", u"<font=3b>" + localText.getText("TXT_KEY_MAIN_MENU_OK", ()) + u"</font>", "", self.W / 2 - 210, self.H - 62, 200, 36, WidgetTypes.WIDGET_GENERAL, BTN_OK, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("YAMCancel", u"<font=3b>" + localText.getText("TXT_KEY_POPUP_CANCEL", ()) + u"</font>", "", self.W / 2 + 10, self.H - 62, 200, 36, WidgetTypes.WIDGET_GENERAL, BTN_CANCEL, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		self.drawValue()
		return 1

	def drawValue(self):
		screen = self.getScreen()
		if self.bSelected:
			szText = u"<color=255,220,100>" + self.szValue + u"</color>"
		else:
			szText = u"<color=255,255,255>" + self.szValue + u"</color><color=255,220,100>|</color>"
		screen.setLabelAt("YAMValue", self.BACKGROUND_ID, u"<font=4b>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W / 2, 76, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
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

	def finish(self, bOk):
		if self.bFinished:
			return
		self.bFinished = True
		if bOk:
			iAmount = max(1, min(self.iMax, self.getValue()))
			try:
				CyGame().sendYieldTransfer(self.iUnit, self.iData3, self.iYield, iAmount, self.bPlayerAction)
			except:
				import traceback
				logYield(traceback.format_exc())
		self.getScreen().hideScreen()

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

	def handleInput(self, inputClass):
		iCode = int(inputClass.getNotifyCode())
		if iCode == int(NotifyCode.NOTIFY_CHARACTER):
			if inputClass.getID() != 0:
				try:
					self.handleKey(inputClass.getData(), inputClass.isCtrlKeyDown())
				except:
					import traceback
					logYield(traceback.format_exc())
			return 0
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

	def update(self, fDelta):
		return 0

	def onClose(self):
		self.bFinished = True
		return 0
