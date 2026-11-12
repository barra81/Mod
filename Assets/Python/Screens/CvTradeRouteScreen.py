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
BTN_FAV_IMP = 41020 # (the favorite checkbox of a row: 41020 + slot)
BTN_FAV_EXP = 41100 # + slot
BTN_VIEW = 41200 # the drop down: default view / favorites
BTN_ROW = 42000 # + slot * 16 + field
VIEW_ALL = 0
VIEW_FAV = 1
VIEW_MARKED = 2

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

# the lightening of a marked button (a translucent orange rectangle, the picture WTPMark.dds stretched to the face of the button, dimmer
# than the hover effect of the game) and, because that covers the hover effect of the game, our own one on marked buttons (WTPHover.dds,
# brighter). The pictures are 1 x 1 pixel (orange, different transparency); the margins are the border of the button picture that is
# left free. The hover effect is drawn on every button (also when the mouse is over its text).
USE_OVERLAY = True
MARK_ART = "Art/Interface/Screens/TradeRoutes/WTPMark.dds"
HOVER_ART = "Art/Interface/Screens/TradeRoutes/WTPHover.dds"
HILITE_LAYERS = 1
HOVER_LAYERS = 1
MARGIN_X = 2
MARGIN_Y = 3
# the font of all texts
TEXT_FONT = "3b"
# texts of the buttons: color of a text that is not marked, the offset of the text top to the middle of the button (font 3b: the
# letters from the top of the I to the bottom of the p are centered in the button)
TEXT_COLOR = "88,64,40"
TEXT_DY = -14

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

# the favorite goods are stored in the script data of the player (saved with the game, valid for all cities): a marker
# [[WTPFAV:TYPE_1,TYPE_2]] in the text (the random events keep their own markers in the same text, they are left alone)
FAV_PREFIX = "[[WTPFAV:"
FAV_SUFFIX = "]]"

def getActivePlayer():
	return gc.getPlayer(gc.getGame().getActivePlayer())

def loadFavorites():
	aFav = []
	try:
		szData = getActivePlayer().getScriptData()
		if szData == None:
			szData = ""
		iStart = szData.find(FAV_PREFIX)
		if iStart != -1:
			iStart += len(FAV_PREFIX)
			iEnd = szData.find(FAV_SUFFIX, iStart)
			if iEnd != -1:
				for szType in szData[iStart:iEnd].split(","):
					szType = szType.strip()
					if len(szType) > 0:
						aFav.append(szType)
	except:
		pass
	return aFav

def saveFavorites(aFav):
	try:
		pPlayer = getActivePlayer()
		szData = pPlayer.getScriptData()
		if szData == None:
			szData = ""
		iStart = szData.find(FAV_PREFIX)
		if iStart != -1:
			iEnd = szData.find(FAV_SUFFIX, iStart)
			if iEnd != -1:
				szData = szData[:iStart] + szData[iEnd + len(FAV_SUFFIX):]
		if len(aFav) > 0:
			szData = szData + FAV_PREFIX + ",".join(aFav) + FAV_SUFFIX
		pPlayer.setScriptData(szData)
	except:
		import traceback
		logTrade(traceback.format_exc())

# the building material preset is a switch: it remembers (per city, in the script data of the player like the favorites) which goods it
# turned on, so that switching it off takes only those away again (not the ones that were set by hand before)
BLD_PREFIX = "[[WTPBLD:"
BLD_SUFFIX = "]]"
BLD_MATERIAL = ["YIELD_CLAY", "YIELD_STONE", "YIELD_TOOLS"] # feeder 100 / 150
BLD_OTHER = ["YIELD_HORSES", "YIELD_SAILCLOTH", "YIELD_HARDWOOD", "YIELD_ROPE"] # feeder, levels unchanged

def loadBuild():
	dBuild = {}
	try:
		szData = getActivePlayer().getScriptData()
		if szData == None:
			szData = ""
		iStart = szData.find(BLD_PREFIX)
		if iStart != -1:
			iStart += len(BLD_PREFIX)
			iEnd = szData.find(BLD_SUFFIX, iStart)
			if iEnd != -1:
				for szEntry in szData[iStart:iEnd].split(";"):
					if szEntry.find(":") == -1:
						continue
					szCity, szTypes = szEntry.split(":", 1)
					aTypes = []
					for szType in szTypes.split(","):
						szType = szType.strip()
						if len(szType) > 0:
							aTypes.append(szType)
					dBuild[int(szCity)] = aTypes
	except:
		pass
	return dBuild

def saveBuild(dBuild):
	try:
		pPlayer = getActivePlayer()
		szData = pPlayer.getScriptData()
		if szData == None:
			szData = ""
		iStart = szData.find(BLD_PREFIX)
		if iStart != -1:
			iEnd = szData.find(BLD_SUFFIX, iStart)
			if iEnd != -1:
				szData = szData[:iStart] + szData[iEnd + len(BLD_SUFFIX):]
		aEntries = []
		for iCity in dBuild.keys():
			aEntries.append(str(iCity) + ":" + ",".join(dBuild[iCity]))
		if len(aEntries) > 0:
			szData = szData + BLD_PREFIX + ";".join(aEntries) + BLD_SUFFIX
		pPlayer.setScriptData(szData)
	except:
		import traceback
		logTrade(traceback.format_exc())

class CvTradeRouteScreen:
	"Import / export settings of a city"

	def __init__(self):
		self.BACKGROUND_ID = "TRSBackground"
		self.W = 1100
		self.H = 600
		self.OX = 0
		self.OY = 0
		self.ROW_H = 60
		self.CHECK_H = 28
		self.LIST_Y = 172
		self.BLOCK_IMP_X = 90
		self.BLOCK_EXP_X = 520
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
		self.iViewX = 0
		self.aAllYields = [] # all goods of the default view
		self.aFav = [] # the favorite goods (yield types)
		self.iView = VIEW_ALL
		self.aDrawn = [] # the names of the widgets that are drawn (to delete them again)
		self.dBtn = {} # the buttons (name: [x, y, w, h, code, text, marked, font, dy, panels])
		self.sHover = ""

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

	def isFav(self, iYield):
		return gc.getYieldInfo(iYield).getType() in self.aFav

	def toggleFav(self, iYield):
		szType = gc.getYieldInfo(iYield).getType()
		if szType in self.aFav:
			self.aFav.remove(szType)
		else:
			self.aFav.append(szType)
		saveFavorites(self.aFav)
		if self.iView == VIEW_FAV:
			self.buildView()
			self.drawRows()
			self.drawPage()
		else:
			self.drawRows()

	# the goods of the view: all of them (default) or the favorites
	def buildView(self):
		if self.iView == VIEW_FAV:
			self.aYields = [i for i in self.aAllYields if self.isFav(i)]
		elif self.iView == VIEW_MARKED:
			# the goods with any mark (import, feeder, export or auto export)
			self.aYields = [i for i in self.aAllYields if (self.dData[i]["imp"] or self.dData[i]["feeder"] or self.dData[i]["exp"] or self.dData[i]["auto"])]
		else:
			self.aYields = list(self.aAllYields)
		self.iFirst = 0

	def setView(self, iView):
		if iView == self.iView:
			return
		self.iView = iView
		self.buildView()
		self.drawRows()
		self.drawPage()

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
		for iYield in self.dData.keys():
			self.loadYield(pCity, iYield)
		if self.iView == VIEW_MARKED:
			self.buildView()
			self.drawPage()
		self.drawMarketButton(pCity)
		self.drawBuildButton()
		self.drawRows()

	def isBuildOn(self):
		return loadBuild().has_key(self.iCity)

	def drawBuildButton(self):
		iHalf = (self.W - 40 - 10) / 2
		szKey = "TXT_KEY_WTP_TRADEROUTE_PRESET3_SHORT"
		bOn = self.isBuildOn()
		if bOn:
			szKey = "TXT_KEY_WTP_TRADEROUTE_PRESET3_SHORT_ON"
		self.addButton("TRSPreset3", localText.getText(szKey, ()), bOn, self.OX + 20, self.OY + 96, iHalf, 28, BTN_PRESET + 3)

	def getYieldByType(self, szType):
		for iYield in self.dData.keys():
			if gc.getYieldInfo(iYield).getType() == szType:
				return iYield
		return -1

	# the building material preset as a switch (see BLD_PREFIX)
	def toggleBuild(self):
		dBuild = loadBuild()
		if dBuild.has_key(self.iCity):
			# off: only the goods the preset turned on are taken away again
			for szType in dBuild[self.iCity]:
				iYield = self.getYieldByType(szType)
				if iYield >= 0:
					self.dData[iYield]["imp"] = False
					self.dData[iYield]["feeder"] = False
			del dBuild[self.iCity]
		else:
			aAdded = []
			for szType in BLD_MATERIAL + BLD_OTHER:
				iYield = self.getYieldByType(szType)
				if iYield < 0:
					continue
				d = self.dData[iYield]
				if not (d["imp"] or d["feeder"]):
					aAdded.append(szType)
				d["imp"] = True
				d["feeder"] = True
				if szType in BLD_MATERIAL:
					d["maintain"] = 100
					d["impLimit"] = 150
			dBuild[self.iCity] = aAdded
		saveBuild(dBuild)
		self.apply()
		self.drawBuildButton()
		if self.iView == VIEW_MARKED:
			self.buildView()
			self.drawPage()
		self.drawRows()
		self.iReload = 60

	def drawMarketButton(self, pCity):
		szMarket = "TXT_KEY_WTP_TRADEROUTE_PRESET4_SHORT"
		if pCity.isAutoMarketImport():
			szMarket = "TXT_KEY_WTP_TRADEROUTE_PRESET4_SHORT_ON"
		iHalf = (self.W - 40 - 10) / 2
		self.addButton("TRSPreset4", localText.getText(szMarket, ()), pCity.isAutoMarketImport(), self.OX + 20 + iHalf + 10, self.OY + 96, iHalf, 28, BTN_PRESET + 4)

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
		self.aFav = loadFavorites()
		self.iView = VIEW_ALL
		self.dBtn = {}
		self.sHover = ""
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if not gc.getYieldInfo(iYield).isCargo():
				continue
			self.loadYield(pCity, iYield)
			if bCondensed and not pCity.isYieldInTradeRouteCondensedList(iYield):
				continue
			self.aYields.append(iYield)

		self.aAllYields = list(self.aYields)
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
			self.addButton("TRSPreset" + str(i), aszPreset[i], False, self.OX + 20 + i * (iBW + 10), self.OY + 62, iBW, 28, BTN_PRESET + i)
		iHalf = (self.W - 40 - 10) / 2
		self.drawBuildButton()
		self.drawMarketButton(pCity)

		self.addButton("TRSOk", localText.getText("TXT_KEY_MAIN_MENU_OK", ()), False, self.OX + self.W / 2 - 105, self.OY + self.H - 44, 100, 28, BTN_OK)
		self.addButton("TRSCancel", localText.getText("TXT_KEY_POPUP_CANCEL", ()), False, self.OX + self.W / 2 + 5, self.OY + self.H - 44, 100, 28, BTN_CANCEL)
		if len(self.aYields) > self.iVisible:
			self.addButton("TRSUp", u"\u00ab", False, self.OX + 24, self.OY + self.H - 44, 36, 28, BTN_UP)
			self.addButton("TRSDown", u"\u00bb", False, self.OX + 24 + 36 + 150, self.OY + self.H - 44, 36, 28, BTN_DOWN)
			self.aDrawn.append("TRSPage")

		self.iViewX = self.W - 20 - 160
		screen.addDropDownBoxGFC("TRSView", self.OX + self.iViewX, self.OY + self.H - 44, 160, WidgetTypes.WIDGET_GENERAL, BTN_VIEW, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("TRSView", localText.getText("TXT_KEY_WTP_TRADEROUTE_VIEW_ALL", ()), 0, 0, True)
		screen.addPullDownString("TRSView", localText.getText("TXT_KEY_WTP_TRADEROUTE_VIEW_FAV", ()), 1, 1, False)
		screen.addPullDownString("TRSView", localText.getText("TXT_KEY_WTP_TRADEROUTE_VIEW_MARKED", ()), 2, 2, False)
		self.aDrawn.append("TRSView")
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

	# a button: blank button of the game, on it the text of the game (placed exactly, yellow when marked); a marked button is lighter
	def addButton(self, szName, szText, bMark, iX, iY, iW, iH, iCode, szFont = "", iDy = 0):
		screen = self.pHost
		if szFont == "":
			szFont = TEXT_FONT
		self.removeButton(szName)
		screen.setButtonGFC(szName, u"", "", iX, iY, iW, iH, WidgetTypes.WIDGET_GENERAL, iCode, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		aLights = []
		if bMark and USE_OVERLAY:
			for i in range(HILITE_LAYERS):
				szLight = "TRSb" + str(i) + "_" + szName
				screen.setImageButton(szLight, MARK_ART, iX + MARGIN_X, iY + MARGIN_Y, iW - 2 * MARGIN_X, iH - 2 * MARGIN_Y, WidgetTypes.WIDGET_GENERAL, iCode, -1)
				aLights.append(szLight)
		self.dBtn[szName] = [iX, iY, iW, iH, iCode, szText, bMark, szFont, iDy, aLights]
		self.drawButtonText(szName)

	def drawButtonText(self, szName):
		b = self.dBtn[szName]
		szLabel = "TRSL" + szName
		self.drop(szLabel)
		szColor = TEXT_COLOR
		if b[6]:
			szColor = "255,220,100"
		szShown = u"<font=" + b[7] + u"><color=" + szColor + u">" + b[5] + u"</color></font>"
		self.pHost.setText(szLabel, "", szShown, CvUtil.FONT_CENTER_JUSTIFY, b[0] + b[2] / 2, b[1] + b[3] / 2 + TEXT_DY + b[8], 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, b[4], -1)

	def removeButton(self, szName):
		self.drop(szName)
		self.drop("TRSL" + szName)
		for i in range(HILITE_LAYERS):
			self.drop("TRSb" + str(i) + "_" + szName)
		if self.dBtn.has_key(szName):
			if self.sHover == szName:
				self.clearHover()
			del self.dBtn[szName]

	def clearHover(self):
		for i in range(HOVER_LAYERS):
			self.drop("TRSHover" + str(i))
		self.sHover = ""

	# the button under the mouse gets a lighter / orange panel (called every frame)
	def updateHover(self):
		if not USE_OVERLAY:
			return
		iX = CyGame().getCursorClientX()
		iY = CyGame().getCursorClientY()
		szNew = ""
		for szName in self.dBtn.keys():
			b = self.dBtn[szName]
			if iX >= b[0] and iX < b[0] + b[2] and iY >= b[1] + 3 and iY < b[1] + b[3] - 3:
				szNew = szName
				break
		if szNew == self.sHover:
			return
		self.clearHover()
		if szNew != "":
			b = self.dBtn[szNew]
			for i in range(HOVER_LAYERS):
				self.pHost.setImageButton("TRSHover" + str(i), HOVER_ART, b[0] + MARGIN_X, b[1] + MARGIN_Y, b[2] - 2 * MARGIN_X, b[3] - 2 * MARGIN_Y, WidgetTypes.WIDGET_GENERAL, b[4], -1)
			self.sHover = szNew
			self.drawButtonText(szNew) # (the text on top of the panel)

	def drawCheck(self, szName, szText, bOn, iX, iY, iCode):
		self.addButton(szName, szText, bOn, iX, iY, self.CHECK_W, self.CHECK_H, iCode)

	def drawRows(self):
		screen = self.pHost
		self.clearHover()
		szImport = localText.getText("TXT_KEY_POPUP_IMPORT_IMPORT", ())
		szFeeder = localText.getText("TXT_KEY_POPUP_IMPORT_FEEDER", ())
		szLand = localText.getText("TXT_KEY_POPUP_IMPORT_LAND", ())
		szSea = localText.getText("TXT_KEY_POPUP_IMPORT_SEA", ())
		szExport = localText.getText("TXT_KEY_POPUP_IMPORT_EXPORT", ())
		szAuto = localText.getText("TXT_KEY_POPUP_IMPORT_AUTO_EXPORT", ())
		szFav = localText.getText("TXT_KEY_WTP_TRADEROUTE_FAVORITE", ())
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
			screen.setImageButton(szIcon, gc.getYieldInfo(iYield).getButton(), self.OX + 22, iY + (self.ROW_H - 32) / 2, 32, 32, WidgetTypes.WIDGET_HELP_YIELD, iYield, -1)
			# import block
			iX = self.OX + self.BLOCK_IMP_X
			self.drawSpin(iSlot, 0, d["impLimit"], iX, iY, iBase + F_IMP_MINUS, iBase + F_IMP_PLUS)
			iCX = iX + self.BLOCK_SPIN_W + 8
			self.drawCheck("TRSc" + str(iSlot) + "_2", szImport, d["imp"], iCX, iY + 2, iBase + F_IMP_CHECK)
			self.drawCheck("TRSc" + str(iSlot) + "_3", szFeeder, d["feeder"], iCX + self.CHECK_W + 4, iY + 2, iBase + F_IMP_FEEDER)
			self.drawCheck("TRSc" + str(iSlot) + "_4", szLand, (d["impDom"] & 1) != 0, iCX, iY + 2 + self.CHECK_H + 2, iBase + F_IMP_LAND)
			self.drawCheck("TRSc" + str(iSlot) + "_5", szSea, (d["impDom"] & 2) != 0, iCX + self.CHECK_W + 4, iY + 2 + self.CHECK_H + 2, iBase + F_IMP_SEA)
			# export block
			iX = self.OX + self.BLOCK_EXP_X
			self.drawSpin(iSlot, 1, d["maintain"], iX, iY, iBase + F_EXP_MINUS, iBase + F_EXP_PLUS)
			iCX = iX + self.BLOCK_SPIN_W + 8
			self.drawCheck("TRSc" + str(iSlot) + "_8", szExport, d["exp"], iCX, iY + 2, iBase + F_EXP_CHECK)
			self.drawCheck("TRSc" + str(iSlot) + "_9", szAuto, d["auto"], iCX + self.CHECK_W + 4, iY + 2, iBase + F_EXP_AUTO)
			self.drawCheck("TRSc" + str(iSlot) + "_10", szLand, (d["expDom"] & 1) != 0, iCX, iY + 2 + self.CHECK_H + 2, iBase + F_EXP_LAND)
			self.drawCheck("TRSc" + str(iSlot) + "_11", szSea, (d["expDom"] & 2) != 0, iCX + self.CHECK_W + 4, iY + 2 + self.CHECK_H + 2, iBase + F_EXP_SEA)
			# the favorite checkbox at the right end of the row (one setting per good, for import and export)
			bFav = self.isFav(iYield)
			self.drawCheck("TRSc" + str(iSlot) + "_fe", szFav, bFav, self.OX + self.iViewX + (160 - self.CHECK_W) / 2, iY + (self.ROW_H - self.CHECK_H) / 2, BTN_FAV_EXP + iSlot)

	def drawSpin(self, iSlot, iBlock, iValue, iX, iY, iMinusCode, iPlusCode):
		screen = self.pHost
		szTag = str(iSlot) + "_" + str(iBlock)
		iBH = 30
		iBY = iY + (self.ROW_H - iBH) / 2
		self.drop("TRSv" + szTag)
		self.addButton("TRSm" + szTag, u"-", False, iX, iBY, 28, iBH, iMinusCode, "", 1)
		self.addButton("TRSp" + szTag, u"+", False, iX + self.BLOCK_SPIN_W - 28 - 7, iBY, 28, iBH, iPlusCode, "", -1)
		screen.setLabelAt("TRSv" + szTag, self.BACKGROUND_ID, u"<font=3><color=255,255,255>" + unicode(iValue) + u"</color></font>", CvUtil.FONT_CENTER_JUSTIFY, (iX - self.OX) + self.BLOCK_SPIN_W / 2, (iY - self.OY) + (self.ROW_H - 22) / 2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def refreshRow(self, iSlot):
		# only the changed row is drawn again: all of them (cheap enough, the list is short)
		self.drawRows()

	def clearSlot(self, iSlot):
		self.drop("TRSIcon" + str(iSlot))
		for iBlock in range(2):
			self.removeButton("TRSm" + str(iSlot) + "_" + str(iBlock))
			self.removeButton("TRSp" + str(iSlot) + "_" + str(iBlock))
			self.drop("TRSv" + str(iSlot) + "_" + str(iBlock))
		for szTag in ("2", "3", "4", "5", "8", "9", "10", "11", "fe"):
			self.removeButton("TRSc" + str(iSlot) + "_" + szTag)

	def clearRows(self):
		for iSlot in range(self.iVisible):
			self.clearSlot(iSlot)

	def getNumPages(self):
		return max(1, (len(self.aYields) + self.iVisible - 1) / self.iVisible)

	def drawPage(self):
		if len(self.aAllYields) <= self.iVisible:
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
		for iYield in self.dData.keys():
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

	def favClicked(self, iSlot):
		iIndex = self.iFirst + iSlot
		if iIndex < len(self.aYields):
			self.toggleFav(self.aYields[iIndex])

	# the tooltip of a widget of the window (CvScreensInterface.getWidgetHelp); empty text: none
	def getHelp(self, iCode):
		if iCode == BTN_VIEW:
			return localText.getText("TXT_KEY_WTP_TRADEROUTE_VIEW_HELP", ())
		if iCode >= BTN_FAV_IMP and iCode < BTN_FAV_IMP + 80:
			return localText.getText("TXT_KEY_WTP_TRADEROUTE_FAVORITE_HELP", ())
		if iCode >= BTN_FAV_EXP and iCode < BTN_FAV_EXP + 80:
			return localText.getText("TXT_KEY_WTP_TRADEROUTE_FAVORITE_HELP", ())
		if iCode == BTN_UP:
			return localText.getText("TXT_KEY_WTP_TRADEROUTE_PAGE_PREV_HELP", ())
		if iCode == BTN_DOWN:
			return localText.getText("TXT_KEY_WTP_TRADEROUTE_PAGE_NEXT_HELP", ())
		if iCode >= BTN_ROW:
			iField = (iCode - BTN_ROW) % 16
			aszKey = {F_IMP_MINUS: "TXT_KEY_POPUP_IMPORT_IMPORT_HELP", F_IMP_PLUS: "TXT_KEY_POPUP_IMPORT_IMPORT_HELP", F_IMP_CHECK: "TXT_KEY_POPUP_IMPORT_IMPORT_HELP", F_IMP_FEEDER: "TXT_KEY_POPUP_IMPORT_FEEDER_HELP", F_IMP_LAND: "TXT_KEY_POPUP_IMPORT_LAND_HELP", F_IMP_SEA: "TXT_KEY_POPUP_IMPORT_SEA_HELP", F_EXP_MINUS: "TXT_KEY_POPUP_IMPORT_EXPORT_HELP", F_EXP_PLUS: "TXT_KEY_POPUP_IMPORT_EXPORT_HELP", F_EXP_CHECK: "TXT_KEY_POPUP_IMPORT_EXPORT_HELP", F_EXP_AUTO: "TXT_KEY_POPUP_IMPORT_AUTO_EXPORT_HELP", F_EXP_LAND: "TXT_KEY_POPUP_EXPORT_LAND_HELP", F_EXP_SEA: "TXT_KEY_POPUP_EXPORT_SEA_HELP"}
			if aszKey.has_key(iField):
				return localText.getText(aszKey[iField], ())
		if iCode >= BTN_PRESET and iCode < BTN_PRESET + 5:
			aszKey = ["TXT_KEY_WTP_TRADEROUTE_PRESET0_HELP", "TXT_KEY_WTP_TRADEROUTE_PRESET1_HELP", "TXT_KEY_WTP_TRADEROUTE_PRESET2_HELP", "TXT_KEY_TRADEROUTE_PRESET_BUILD", "TXT_KEY_TRADEROUTE_PRESET_MARKET_AUTO"]
			if iCode - BTN_PRESET == 4:
				pCity = self.getCity()
				if pCity != None and not pCity.isNone() and pCity.isAutoMarketImport():
					return localText.getText("TXT_KEY_TRADEROUTE_PRESET_MARKET_AUTO_OFF", ())
			return localText.getText(aszKey[iCode - BTN_PRESET], ())
		return u""

	# a preset: the changes of the window are sent first, the window stays open and shows the result a moment later
	def runPreset(self, iPreset):
		if iPreset == 3:
			self.toggleBuild()
			return
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
			self.clearHover()
			for szName in self.dBtn.keys():
				self.removeButton(szName)
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
		if int(inputClass.getNotifyCode()) == int(NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED) and inputClass.getFunctionName() == "TRSView":
			iIndex = self.pHost.getSelectedPullDownID("TRSView")
			self.setView(self.pHost.getPullDownData("TRSView", iIndex))
			return 1
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
		elif iData >= BTN_FAV_IMP and iData < BTN_FAV_IMP + 80:
			self.favClicked(iData - BTN_FAV_IMP)
		elif iData >= BTN_FAV_EXP and iData < BTN_FAV_EXP + 80:
			self.favClicked(iData - BTN_FAV_EXP)
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
			self.updateHover()
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

