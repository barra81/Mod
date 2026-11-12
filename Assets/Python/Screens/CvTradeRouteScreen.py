## WTP: window of the governor button of the city screen (import / export settings of the goods). It replaces the popup of the
## game, which has a fixed width (no room for the land / sea checkboxes) and no mouse wheel. The DLL
## (CvDLLButtonPopup::launchYieldImportExportPopup) calls askTradeRouteSetup in CvScreensInterface; the settings are sent
## with CyMessageControl().sendDoTask exactly as the popup did (CvDLLButtonPopup::OnOkClicked).
## The window is drawn on the main interface (like the amount dialog) and CvMainInterface.redraw does nothing while it is open.

from CvPythonExtensions import *
import CvUtil
import CvScreenEnums

gc = CyGlobalContext()
localText = CyTranslator()

BTN_OK = 41001
BTN_CANCEL = 41002
BTN_UP = 41003
BTN_DOWN = 41004
BTN_PRESET = 41010 # + 0..4
BTN_ROW = 42000 # + slot * 16 + field

# fields of a row
F_IMP_MINUS = 0
F_IMP_PLUS = 1
F_IMP_CHECK = 2
F_IMP_FEEDER = 3
F_IMP_LAND = 4
F_IMP_SEA = 5
F_EXP_MINUS = 6
F_EXP_PLUS = 7
F_EXP_CHECK = 8
F_EXP_AUTO = 9
F_EXP_LAND = 10
F_EXP_SEA = 11

STEP = 10
STEP_CTRL = 50
MAX_VALUE = 0xFFFF

def logTrade(szText):
	try:
		f = open("WTP_TradeRoutes.log", "a")
		f.write(szText + "\n")
		f.close()
	except:
		pass

class CvTradeRouteScreen:
	"Import / export settings of a city"

	def __init__(self):
		self.BACKGROUND_ID = "TRSBackground"
		self.W = 1200
		self.H = 600
		self.OX = 0
		self.OY = 0
		self.ROW_H = 54
		self.LIST_Y = 194
		self.BLOCK_IMP_X = 90
		self.BLOCK_EXP_X = 640
		self.CHECK_W = 124
		self.BLOCK_SPIN_W = 116
		self.iCity = -1
		self.bCondensed = False
		self.bFinished = True
		self.pHost = None
		self.aYields = []
		self.dData = {}
		self.iFirst = 0
		self.iVisible = 0
		self.iReload = 0
		self.aDrawn = [] # the names of the widgets that are drawn (to delete them again)

	def isOpen(self):
		return not self.bFinished

	def isHostMain(self):
		return not self.bFinished

	def getCity(self):
		try:
			return gc.getPlayer(gc.getGame().getActivePlayer()).getCity(self.iCity)
		except:
			return None

	def getKeyId(self, szName):
		iKey = getattr(InputTypes, szName, None)
		if iKey == None:
			return -12345
		return int(iKey)

	def loadYield(self, pCity, iYield):
		d = {}
		d["imp"] = pCity.isImport(iYield)
		d["feeder"] = pCity.isImportFeeder(iYield)
		d["impLimit"] = pCity.getImportsLimit(iYield)
		d["impDom"] = pCity.getImportDomains(iYield)
		d["exp"] = pCity.isExport(iYield)
		d["auto"] = pCity.isAutoExport(iYield)
		d["maintain"] = pCity.getMaintainLevel(iYield)
		d["expDom"] = pCity.getExportDomains(iYield)
		self.dData[iYield] = d

	# the settings of the city are read again (after a preset: the city changes a moment after the command was sent)
	def reloadFromCity(self):
		pCity = self.getCity()
		if pCity == None or pCity.isNone():
			return
		for iYield in self.aYields:
			self.loadYield(pCity, iYield)
		self.drawMarketButton(pCity)
		self.drawRows()

	def drawMarketButton(self, pCity):
		szMarket = "TXT_KEY_TRADEROUTE_PRESET_MARKET_AUTO"
		if pCity.isAutoMarketImport():
			szMarket = "TXT_KEY_TRADEROUTE_PRESET_MARKET_AUTO_OFF"
		self.drop("TRSPreset4")
		self.pHost.setButtonGFC("TRSPreset4", u"<font=2b>" + localText.getText(szMarket, ()) + u"</font>", "", self.OX + 20, self.OY + 96 + 30, self.W - 40, 26, WidgetTypes.WIDGET_GENERAL, BTN_PRESET + 4, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

	# opens the window (1: it is open, 0: the DLL shows its own popup instead)
	def open(self, iCity, bCondensed):
		if not self.bFinished:
			return 1
		self.iCity = iCity
		pCity = self.getCity()
		if pCity == None or pCity.isNone():
			return 0
		self.bCondensed = bCondensed
		self.aYields = []
		self.dData = {}
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if not gc.getYieldInfo(iYield).isCargo():
				continue
			if bCondensed and not pCity.isYieldInTradeRouteCondensedList(iYield):
				continue
			self.aYields.append(iYield)
			self.loadYield(pCity, iYield)

		self.iKeyEsc = self.getKeyId("KB_ESCAPE")
		self.pHost = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		screen = self.pHost
		iXRes = screen.getXResolution()
		iYRes = screen.getYResolution()
		self.H = min(int(iYRes * 0.86), self.LIST_Y + len(self.aYields) * self.ROW_H + 70)
		self.iVisible = max(1, (self.H - self.LIST_Y - 70) / self.ROW_H)
		self.iVisible = min(self.iVisible, len(self.aYields))
		self.H = self.LIST_Y + self.iVisible * self.ROW_H + 70
		self.OX = (iXRes - self.W) / 2
		self.OY = (iYRes - self.H) / 2
		self.iFirst = 0
		self.bFinished = False
		self.aDrawn = []

		screen.addPanel(self.BACKGROUND_ID, u"", u"", True, False, self.OX, self.OY, self.W, self.H, PanelStyles.PANEL_STYLE_MAIN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.aDrawn.append(self.BACKGROUND_ID)
		szTitle = u"<font=3><color=255,220,100>" + pCity.getName() + u"</color></font>"
		screen.setLabelAt("TRSTitle", self.BACKGROUND_ID, szTitle, CvUtil.FONT_CENTER_JUSTIFY, self.W / 2, 18, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt("TRSHint", self.BACKGROUND_ID, u"<font=2>" + localText.getText("TXT_KEY_WTP_TRADEROUTE_HINT", ()) + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W / 2, 44, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.aDrawn.append("TRSTitle")
		self.aDrawn.append("TRSHint")
		iHeadW = self.BLOCK_SPIN_W + 8 + 2 * self.CHECK_W + 4
		screen.setLabelAt("TRSHeadImp", self.BACKGROUND_ID, u"<font=3b><color=255,220,100>" + localText.getText("TXT_KEY_WTP_TRADEROUTE_IMPORT_OPTIONS", ()) + u"</color></font>", CvUtil.FONT_CENTER_JUSTIFY, self.BLOCK_IMP_X + iHeadW / 2, self.LIST_Y - 28, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt("TRSHeadExp", self.BACKGROUND_ID, u"<font=3b><color=255,220,100>" + localText.getText("TXT_KEY_WTP_TRADEROUTE_EXPORT_OPTIONS", ()) + u"</color></font>", CvUtil.FONT_CENTER_JUSTIFY, self.BLOCK_EXP_X + iHeadW / 2, self.LIST_Y - 28, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.aDrawn.append("TRSHeadImp")
		self.aDrawn.append("TRSHeadExp")

		# the presets (the buttons of the old popup)
		iBW = (self.W - 40 - 20) / 3
		aszPreset = [localText.getText("TXT_KEY_POPUP_IMPORT_CLEAR_ALL", ()), localText.getText("TXT_KEY_POPUP_IMPORT_ALL", ()), localText.getText("TXT_KEY_POPUP_IMPORT_EXPORT_ALL", ())]
		for i in range(3):
			szName = "TRSPreset" + str(i)
			screen.setButtonGFC(szName, u"<font=2b>" + aszPreset[i] + u"</font>", "", self.OX + 20 + i * (iBW + 10), self.OY + 66, iBW, 26, WidgetTypes.WIDGET_GENERAL, BTN_PRESET + i, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
			self.aDrawn.append(szName)
		szName = "TRSPreset3"
		screen.setButtonGFC(szName, u"<font=2b>" + localText.getText("TXT_KEY_TRADEROUTE_PRESET_BUILD", ()) + u"</font>", "", self.OX + 20, self.OY + 96, self.W - 40, 26, WidgetTypes.WIDGET_GENERAL, BTN_PRESET + 3, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		self.aDrawn.append(szName)
		self.drawMarketButton(pCity)
		self.aDrawn.append("TRSPreset4")

		screen.setButtonGFC("TRSOk", u"<font=3b>" + localText.getText("TXT_KEY_MAIN_MENU_OK", ()) + u"</font>", "", self.OX + self.W / 2 - 105, self.OY + self.H - 44, 100, 28, WidgetTypes.WIDGET_GENERAL, BTN_OK, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("TRSCancel", u"<font=3b>" + localText.getText("TXT_KEY_POPUP_CANCEL", ()) + u"</font>", "", self.OX + self.W / 2 + 5, self.OY + self.H - 44, 100, 28, WidgetTypes.WIDGET_GENERAL, BTN_CANCEL, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		self.aDrawn.append("TRSOk")
		self.aDrawn.append("TRSCancel")
		if len(self.aYields) > self.iVisible:
			screen.setButtonGFC("TRSUp", u"<font=3b>\u00ab</font>", "", self.OX + 24, self.OY + self.H - 44, 36, 28, WidgetTypes.WIDGET_GENERAL, BTN_UP, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
			screen.setButtonGFC("TRSDown", u"<font=3b>\u00bb</font>", "", self.OX + 24 + 36 + 150, self.OY + self.H - 44, 36, 28, WidgetTypes.WIDGET_GENERAL, BTN_DOWN, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
			self.aDrawn.append("TRSUp")
			self.aDrawn.append("TRSDown")
			self.aDrawn.append("TRSPage")

		self.drawRows()
		self.drawPage()
		try:
			CyGame().setWheelCapture(True)
		except:
			pass
		return 1

	def drop(self, szName):
		try:
			self.pHost.deleteWidget(szName)
		except:
			pass

	def drawCheck(self, szName, szText, bOn, iX, iY, iCode):
		screen = self.pHost
		self.drop(szName)
		if bOn:
			szShown = u"<font=3b><color=255,220,100>[x] " + szText + u"</color></font>"
		else:
			szShown = u"<font=3b>[   ] " + szText + u"</font>"
		screen.setButtonGFC(szName, szShown, "", iX, iY, self.CHECK_W, 24, WidgetTypes.WIDGET_GENERAL, iCode, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

	def drawRows(self):
		screen = self.pHost
		szImport = localText.getText("TXT_KEY_POPUP_IMPORT_IMPORT", ())
		szFeeder = localText.getText("TXT_KEY_POPUP_IMPORT_FEEDER", ())
		szLand = localText.getText("TXT_KEY_POPUP_IMPORT_LAND", ())
		szSea = localText.getText("TXT_KEY_POPUP_IMPORT_SEA", ())
		szExport = localText.getText("TXT_KEY_POPUP_IMPORT_EXPORT", ())
		szAuto = localText.getText("TXT_KEY_POPUP_IMPORT_AUTO_EXPORT", ())
		for iSlot in range(self.iVisible):
			iIndex = self.iFirst + iSlot
			if iIndex >= len(self.aYields):
				self.clearSlot(iSlot)
				continue
			iYield = self.aYields[iIndex]
			d = self.dData[iYield]
			iY = self.OY + self.LIST_Y + iSlot * self.ROW_H
			iBase = BTN_ROW + iSlot * 16
			szIcon = "TRSIcon" + str(iSlot)
			self.drop(szIcon)
			screen.setImageButton(szIcon, gc.getYieldInfo(iYield).getButton(), self.OX + 22, iY + 10, 32, 32, WidgetTypes.WIDGET_HELP_YIELD, iYield, -1)
			# import block
			iX = self.OX + self.BLOCK_IMP_X
			self.drawSpin(iSlot, 0, d["impLimit"], iX, iY, iBase + F_IMP_MINUS, iBase + F_IMP_PLUS)
			iCX = iX + self.BLOCK_SPIN_W + 8
			self.drawCheck("TRSc" + str(iSlot) + "_2", szImport, d["imp"], iCX, iY + 3, iBase + F_IMP_CHECK)
			self.drawCheck("TRSc" + str(iSlot) + "_3", szFeeder, d["feeder"], iCX + self.CHECK_W + 4, iY + 3, iBase + F_IMP_FEEDER)
			self.drawCheck("TRSc" + str(iSlot) + "_4", szLand, (d["impDom"] & 1) != 0, iCX, iY + 28, iBase + F_IMP_LAND)
			self.drawCheck("TRSc" + str(iSlot) + "_5", szSea, (d["impDom"] & 2) != 0, iCX + self.CHECK_W + 4, iY + 28, iBase + F_IMP_SEA)
			# export block
			iX = self.OX + self.BLOCK_EXP_X
			self.drawSpin(iSlot, 1, d["maintain"], iX, iY, iBase + F_EXP_MINUS, iBase + F_EXP_PLUS)
			iCX = iX + self.BLOCK_SPIN_W + 8
			self.drawCheck("TRSc" + str(iSlot) + "_8", szExport, d["exp"], iCX, iY + 3, iBase + F_EXP_CHECK)
			self.drawCheck("TRSc" + str(iSlot) + "_9", szAuto, d["auto"], iCX + self.CHECK_W + 4, iY + 3, iBase + F_EXP_AUTO)
			self.drawCheck("TRSc" + str(iSlot) + "_10", szLand, (d["expDom"] & 1) != 0, iCX, iY + 28, iBase + F_EXP_LAND)
			self.drawCheck("TRSc" + str(iSlot) + "_11", szSea, (d["expDom"] & 2) != 0, iCX + self.CHECK_W + 4, iY + 28, iBase + F_EXP_SEA)

	def drawSpin(self, iSlot, iBlock, iValue, iX, iY, iMinusCode, iPlusCode):
		screen = self.pHost
		szMinus = "TRSm" + str(iSlot) + "_" + str(iBlock)
		szPlus = "TRSp" + str(iSlot) + "_" + str(iBlock)
		szValue = "TRSv" + str(iSlot) + "_" + str(iBlock)
		self.drop(szMinus)
		self.drop(szPlus)
		self.drop(szValue)
		screen.setButtonGFC(szMinus, u"<font=3b>-</font>", "", iX, iY + 13, 24, 26, WidgetTypes.WIDGET_GENERAL, iMinusCode, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC(szPlus, u"<font=3b>+</font>", "", iX + self.BLOCK_SPIN_W - 24, iY + 13, 24, 26, WidgetTypes.WIDGET_GENERAL, iPlusCode, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setLabelAt(szValue, self.BACKGROUND_ID, u"<font=3><color=255,255,255>" + unicode(iValue) + u"</color></font>", CvUtil.FONT_CENTER_JUSTIFY, (iX - self.OX) + self.BLOCK_SPIN_W / 2, (iY - self.OY) + 16, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def refreshRow(self, iSlot):
		# only the changed row is drawn again: all of them (cheap enough, the list is short)
		self.drawRows()

	def clearSlot(self, iSlot):
		self.drop("TRSIcon" + str(iSlot))
		for iBlock in range(2):
			self.drop("TRSm" + str(iSlot) + "_" + str(iBlock))
			self.drop("TRSp" + str(iSlot) + "_" + str(iBlock))
			self.drop("TRSv" + str(iSlot) + "_" + str(iBlock))
		for iField in (2, 3, 4, 5, 8, 9, 10, 11):
			self.drop("TRSc" + str(iSlot) + "_" + str(iField))

	def clearRows(self):
		for iSlot in range(self.iVisible):
			self.clearSlot(iSlot)

	def getNumPages(self):
		return max(1, (len(self.aYields) + self.iVisible - 1) / self.iVisible)

	def drawPage(self):
		if len(self.aYields) <= self.iVisible:
			return
		szText = u"<font=3b>" + localText.getText("TXT_KEY_WTP_TRADEROUTE_PAGE", (self.iFirst / self.iVisible + 1, self.getNumPages())) + u"</font>"
		self.pHost.setLabelAt("TRSPage", self.BACKGROUND_ID, szText, CvUtil.FONT_CENTER_JUSTIFY, 24 + 36 + 75, self.H - 40, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	# iDelta pages forward / back
	def scroll(self, iDelta):
		iPage = max(0, min(self.getNumPages() - 1, self.iFirst / self.iVisible + iDelta))
		if iPage * self.iVisible != self.iFirst:
			self.iFirst = iPage * self.iVisible
			self.drawRows()
			self.drawPage()

	def changeValue(self, iSlot, iBlock, iDelta):
		iIndex = self.iFirst + iSlot
		if iIndex >= len(self.aYields):
			return
		d = self.dData[self.aYields[iIndex]]
		szKey = "impLimit"
		if iBlock == 1:
			szKey = "maintain"
		d[szKey] = max(0, min(MAX_VALUE, d[szKey] + iDelta))
		self.drawRows()

	def toggleField(self, iSlot, iField):
		iIndex = self.iFirst + iSlot
		if iIndex >= len(self.aYields):
			return
		d = self.dData[self.aYields[iIndex]]
		if iField == F_IMP_CHECK:
			d["imp"] = not d["imp"]
		elif iField == F_IMP_FEEDER:
			d["feeder"] = not d["feeder"]
		elif iField == F_IMP_LAND:
			d["impDom"] = d["impDom"] ^ 1
		elif iField == F_IMP_SEA:
			d["impDom"] = d["impDom"] ^ 2
		elif iField == F_EXP_CHECK:
			d["exp"] = not d["exp"]
		elif iField == F_EXP_AUTO:
			d["auto"] = not d["auto"]
		elif iField == F_EXP_LAND:
			d["expDom"] = d["expDom"] ^ 1
		elif iField == F_EXP_SEA:
			d["expDom"] = d["expDom"] ^ 2
		self.drawRows()

	def apply(self):
		pCity = self.getCity()
		if pCity == None or pCity.isNone():
			return
		for iYield in self.aYields:
			d = self.dData[iYield]
			if (d["imp"] != pCity.isImport(iYield) or d["exp"] != pCity.isExport(iYield) or d["feeder"] != pCity.isImportFeeder(iYield)
				or d["auto"] != pCity.isAutoExport(iYield) or d["impDom"] != pCity.getImportDomains(iYield)
				or d["expDom"] != pCity.getExportDomains(iYield) or d["maintain"] != pCity.getMaintainLevel(iYield)
				or d["impLimit"] != pCity.getImportsLimit(iYield)):
				iData1 = iYield | (d["impDom"] << 8) | (d["expDom"] << 10)
				# (see NetworkDataTradeRouteInts: the maintain level in the lower, the import limit in the upper 16 bits)
				iData2 = (d["maintain"] & 0xFFFF) | ((d["impLimit"] & 0xFFFF) << 16)
				if iData2 >= 2147483648L:
					iData2 = iData2 - 4294967296L
				CyMessageControl().sendDoTask(self.iCity, TaskTypes.TASK_YIELD_TRADEROUTE, iData1, int(iData2), d["imp"], d["exp"], d["feeder"], d["auto"])

	# a preset: the changes of the window are sent first, the window stays open and shows the result a moment later
	def runPreset(self, iPreset):
		try:
			self.apply()
			if iPreset <= 2:
				# 0: clear all, 1: import all, 2: auto export all
				CyMessageControl().sendDoTask(self.iCity, TaskTypes.TASK_AUTO_TRADEROUTE, 0, 0, iPreset == 0, iPreset == 1, iPreset == 2, False)
			else:
				CyMessageControl().sendDoTask(self.iCity, TaskTypes.TASK_TRADEROUTE_PRESET, iPreset - 3, 0, False, False, False, False)
		except:
			import traceback
			logTrade(traceback.format_exc())
		self.iReload = 60

	def finish(self, bOk, iPreset):
		if self.bFinished:
			return
		if bOk:
			try:
				self.apply()
				if iPreset >= 0 and iPreset <= 2:
					# 0: clear all, 1: import all, 2: auto export all
					CyMessageControl().sendDoTask(self.iCity, TaskTypes.TASK_AUTO_TRADEROUTE, 0, 0, iPreset == 0, iPreset == 1, iPreset == 2, False)
				elif iPreset >= 3:
					CyMessageControl().sendDoTask(self.iCity, TaskTypes.TASK_TRADEROUTE_PRESET, iPreset - 3, 0, False, False, False, False)
			except:
				import traceback
				logTrade(traceback.format_exc())
		self.bFinished = True
		try:
			CyGame().setWheelCapture(False)
		except:
			pass
		try:
			self.clearRows()
			for szName in self.aDrawn:
				self.drop(szName)
			for szName in ("TRSOk", "TRSCancel", "TRSUp", "TRSDown", "TRSPage", "TRSHeadImp", "TRSHeadExp", "TRSTitle", "TRSHint", self.BACKGROUND_ID):
				self.drop(szName)
			for i in range(5):
				self.drop("TRSPreset" + str(i))
		except:
			import traceback
			logTrade(traceback.format_exc())
		# the interface is redrawn completely afterwards
		for szBit in ("MiscButtons_DIRTY_BIT", "GameData_DIRTY_BIT", "ResourceTable_DIRTY_BIT", "Minimap_Section_DIRTY_BIT", "Help_DIRTY_BIT", "InfoPane_DIRTY_BIT", "SelectionButtons_DIRTY_BIT", "CityScreen_DIRTY_BIT"):
			try:
				CyInterface().setDirty(getattr(InterfaceDirtyBits, szBit), True)
			except:
				pass
		self.pHost = None

	# a key down event (CvEventManager.onKbdEvent gives them to the window while it is open)
	def handleKey(self, iKey, bCtrl):
		if iKey == self.iKeyEsc:
			self.finish(False, -1)

	# the clicks on the buttons of the window; returns 1 if the event was for it
	def handleEmbeddedInput(self, inputClass):
		if int(inputClass.getNotifyCode()) != int(NotifyCode.NOTIFY_CLICKED) or inputClass.getButtonType() != WidgetTypes.WIDGET_GENERAL:
			return 0
		iData = inputClass.getData1()
		if iData < BTN_OK or iData >= BTN_ROW + 16 * 64:
			return 0
		bCtrl = inputClass.isCtrlKeyDown()
		iStep = STEP
		if bCtrl:
			iStep = STEP_CTRL
		if iData == BTN_OK:
			self.finish(True, -1)
		elif iData == BTN_CANCEL:
			self.finish(False, -1)
		elif iData == BTN_UP:
			self.scroll(-1)
		elif iData == BTN_DOWN:
			self.scroll(1)
		elif iData >= BTN_PRESET and iData < BTN_PRESET + 5:
			self.runPreset(iData - BTN_PRESET)
		elif iData >= BTN_ROW:
			iSlot = (iData - BTN_ROW) / 16
			iField = (iData - BTN_ROW) % 16
			if iField == F_IMP_MINUS:
				self.changeValue(iSlot, 0, -iStep)
			elif iField == F_IMP_PLUS:
				self.changeValue(iSlot, 0, iStep)
			elif iField == F_EXP_MINUS:
				self.changeValue(iSlot, 1, -iStep)
			elif iField == F_EXP_PLUS:
				self.changeValue(iSlot, 1, iStep)
			else:
				self.toggleField(iSlot, iField)
		else:
			return 0
		return 1

	# the mouse wheel (collected by the DLL while the window is open): over a number it changes it, elsewhere it scrolls the list
	def update(self, fDelta):
		if self.bFinished:
			return 0
		try:
			if self.iReload > 0:
				self.iReload -= 1
				if self.iReload % 10 == 0:
					self.reloadFromCity()
			iNotches = CyGame().takeWheelNotches()
			if iNotches == 0:
				return 0
			iX = CyGame().getCursorClientX() - self.OX
			iY = CyGame().getCursorClientY() - self.OY
			iStep = STEP
			if CyGame().isCtrlKeyPressed():
				iStep = STEP_CTRL
			iSlot = (iY - self.LIST_Y) / self.ROW_H
			iBlock = -1
			if iY >= self.LIST_Y and iSlot >= 0 and iSlot < self.iVisible:
				if iX >= self.BLOCK_IMP_X and iX < self.BLOCK_IMP_X + self.BLOCK_SPIN_W:
					iBlock = 0
				elif iX >= self.BLOCK_EXP_X and iX < self.BLOCK_EXP_X + self.BLOCK_SPIN_W:
					iBlock = 1
			for i in range(abs(iNotches)):
				if iBlock >= 0:
					if iNotches > 0:
						self.changeValue(iSlot, iBlock, iStep)
					else:
						self.changeValue(iSlot, iBlock, -iStep)
				else:
					if iNotches > 0:
						self.scroll(-1)
					else:
						self.scroll(1)
		except:
			import traceback
			logTrade(traceback.format_exc())
		return 0

	def onClose(self):
		self.bFinished = True
		try:
			CyGame().setWheelCapture(False)
		except:
			pass
		return 0

