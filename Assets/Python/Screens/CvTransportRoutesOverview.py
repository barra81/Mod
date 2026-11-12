## WTP: overview of the trade route assignments of all transports (the "R" screen of every transport side by side)
## Opened from the trade routes tab of the domestic advisor, returns there when it is closed.

from CvPythonExtensions import *
import CvUtil
import CvScreenEnums
import time

gc = CyGlobalContext()
localText = CyTranslator()
ArtFileMgr = CyArtFileMgr()

# widget data of the buttons
BTN_PREV = 30001
BTN_NEXT = 30002
BTN_PREV_PAGE = 30003
BTN_NEXT_PAGE = 30004
BTN_CLEAR_SEARCH = 30005
BTN_SEARCH = 30006
BTN_RENAME = 31000 # + the slot of the column

BTN_MANUAL = 32000 # + the slot of the column

# transports that were asked for a name lately (unit id -> time), and the numbers of the names that are offered but not answered yet
g_RenameAsked = {}
g_PendingNumbers = []

def isNamedLike(szName, szPrefix):
	return szName[:len(szPrefix) + 1] == szPrefix + u" " and szName[len(szPrefix) + 1:].isdigit()

def getUsedNumbers(player, szPrefix):
	aUsed = []
	(pUnit, iter) = player.firstUnit(False)
	while (pUnit):
		szName = pUnit.getNameNoDesc()
		if isNamedLike(szName, szPrefix):
			aUsed.append(int(szName[len(szPrefix) + 1:]))
		(pUnit, iter) = player.nextUnit(iter, False)
	return aUsed

# the popup that renames a transport (the name is set by the event RenameTransport, see CvEventManager)
def openNamePopup(iUnit, szBody, szDefault):
	popup = CyPopup(CvUtil.EventRenameTransport, EventContextTypes.EVENTCONTEXT_ALL, True)
	popup.setUserData((iUnit,))
	popup.setBodyString(szBody, CvUtil.FONT_CENTER_JUSTIFY)
	popup.createEditBox(szDefault, 0)
	popup.setEditBoxMaxCharCount(20, 20, 0)
	popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)

# a transport was set to full automation (bAuto) or got its first trade route: the player may take a numbered name
# (called by the DLL and when the overview is closed, a transport is asked once in a while only)
def offerTransportName(iUnit, bAuto):
	global g_PendingNumbers
	player = gc.getPlayer(gc.getGame().getActivePlayer())
	pUnit = player.getUnit(iUnit)
	if pUnit == None or pUnit.isNone():
		return
	fNow = time.time()
	if fNow - g_RenameAsked.get(iUnit, -1000.0) < 10.0:
		return
	if bAuto:
		szPrefix = localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_NAME_AUTO", ())
	else:
		szPrefix = localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_NAME_ROUTE", ())
	if isNamedLike(pUnit.getNameNoDesc(), szPrefix):
		return
	g_RenameAsked[iUnit] = fNow
	g_PendingNumbers = [t for t in g_PendingNumbers if fNow - t[2] < 120.0]
	aUsed = getUsedNumbers(player, szPrefix)
	for tPending in g_PendingNumbers:
		if tPending[0] == szPrefix:
			aUsed.append(tPending[1])
	iNumber = 1
	while iNumber in aUsed:
		iNumber += 1
	g_PendingNumbers.append((szPrefix, iNumber, fNow))
	openNamePopup(iUnit, localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_RENAME", (pUnit.getName(),)), szPrefix + u" " + unicode(iNumber))

# diagnosis of the clicks (WTP_Overview.log in the game folder)
def logOverview(szText):
	try:
		f = open("WTP_Overview.log", "a")
		f.write(szText + "\n")
		f.close()
	except:
		pass

# the keys of the search field: key name -> character
SEARCH_KEY_NAMES = {}
for _c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
	SEARCH_KEY_NAMES["KB_" + _c] = _c.lower()
for _c in "0123456789":
	SEARCH_KEY_NAMES["KB_" + _c] = _c
SEARCH_KEY_NAMES["KB_SPACE"] = " "
SEARCH_KEY_NAMES["KB_MINUS"] = "-"

class CvTransportRoutesOverview:
	"Trade route assignments of all transports"

	def __init__(self):
		self.SCREEN_NAME = "TransportRoutesOverview"
		self.BACKGROUND_ID = "TROBackground"
		self.COL_WIDTH = 420
		self.GAP = 8
		self.MARGIN = 16
		self.ROW_HEIGHT = 32
		self.HEADER_HEIGHT = 84
		self.iFirst = 0
		self.Transports = []
		self.iNumVisible = 1
		self.iUsedSlots = 0
		self.aColumnX = []
		self.iKeyLog = 0
		self.bRenameWatch = False
		self.aShownRoutes = {} # slot -> the routes in the order of the rows
		self.aVisible = [] # indices of the transports that pass the filters
		self.iTypeFilter = 0 # 0 trade routes (R), 1 fully automatic (Shift+Alt+C)
		self.bSearchSelected = False # the field was clicked: the next key replaces the text
		self.iDomainFilter = 0 # 0 land and sea, 1 land, 2 sea
		self.iAssignFilter = 0 # 0 all, 1 only transports with routes, 2 only transports without
		self.szQuery = u""
		self.szSuggestion = u""

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.TRANSPORT_ROUTES_OVERVIEW)

	def interfaceScreen(self):
		screen = self.getScreen()
		if screen.isActive():
			return

		self.player = gc.getPlayer(gc.getGame().getActivePlayer())
		self.Transports = []
		SelectionGroup, Iterator = self.player.firstSelectionGroup(False)
		while (SelectionGroup != None):
			if SelectionGroup.canAssignTradeRoute(-1, False):
				pHead = SelectionGroup.getHeadUnit()
				if pHead != None and not pHead.isNone():
					self.Transports.append(self.readTransport(SelectionGroup, pHead))
			SelectionGroup, Iterator = self.player.nextSelectionGroup(Iterator, False)

		if len(self.Transports) == 0:
			self.returnToDomestic()
			return

		self.buildSearchData()
		self.dKeys = {}
		for szKey in SEARCH_KEY_NAMES.keys():
			iKey = getattr(InputTypes, szKey, None)
			if iKey != None:
				self.dKeys[int(iKey)] = SEARCH_KEY_NAMES[szKey]
		self.iKeyBack = self.getKeyId("KB_BACKSPACE")
		self.aKeyAccept = [self.getKeyId("KB_TAB"), self.getKeyId("KB_RETURN"), self.getKeyId("KB_RIGHT")]
		self.iTypeFilter = 0
		self.bSearchSelected = False
		self.bRenameWatch = False
		self.iDomainFilter = 0 # standard filters: land and sea, only transports with trade routes
		self.iAssignFilter = 1
		self.szQuery = u""
		self.szSuggestion = u""

		self.XResolution = screen.getXResolution()
		self.YResolution = screen.getYResolution()
		self.iNumVisible = max(1, (self.XResolution - 2 * self.MARGIN + self.GAP) / (self.COL_WIDTH + self.GAP))
		self.iFirst = 0
		self.iUsedSlots = 0
		self.TOOLBAR_Y = 62
		self.HEAD_Y = 108
		self.TABLE_Y = self.HEAD_Y + self.HEADER_HEIGHT - 6
		self.EXIT_Y = self.YResolution - 45
		self.NAV_Y = self.EXIT_Y - 42
		self.TABLE_HEIGHT = self.NAV_Y - self.TABLE_Y - 8

		screen.setRenderInterfaceOnly(True) # as the screens that get keyboard input (the search field)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setDimensions(0, 0, self.XResolution, self.YResolution)
		screen.showWindowBackground(False)
		screen.addPanel(self.BACKGROUND_ID, u"", u"", True, False, 0, 0, self.XResolution, self.YResolution, PanelStyles.PANEL_STYLE_MAIN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt("TROTitle", self.BACKGROUND_ID, u"<font=4b>" + localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, 26, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# navigation row (scrolling to the side) and the exit button at the very bottom
		iButtonW = 60
		szLeft = ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_LEFT_ARROW").getPath()
		szRight = ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_RIGHT_ARROW").getPath()
		screen.setButtonGFC("TROPrevPage", u"<font=3b>-" + unicode(self.iNumVisible) + u"</font>", "", self.MARGIN, self.NAV_Y, iButtonW, 32, WidgetTypes.WIDGET_GENERAL, BTN_PREV_PAGE, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setImageButton("TROPrev", szLeft, self.MARGIN + iButtonW + 8, self.NAV_Y - 4, 40, 40, WidgetTypes.WIDGET_GENERAL, BTN_PREV, -1)
		screen.setImageButton("TRONext", szRight, self.XResolution - self.MARGIN - iButtonW - 8 - 40, self.NAV_Y - 4, 40, 40, WidgetTypes.WIDGET_GENERAL, BTN_NEXT, -1)
		screen.setButtonGFC("TRONextPage", u"<font=3b>+" + unicode(self.iNumVisible) + u"</font>", "", self.XResolution - self.MARGIN - iButtonW, self.NAV_Y, iButtonW, 32, WidgetTypes.WIDGET_GENERAL, BTN_NEXT_PAGE, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("ScreenExit", u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + u"</font>", "", self.MARGIN, self.EXIT_Y, self.XResolution - 2 * self.MARGIN, 30, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setActivation("ScreenExit", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)

		self.drawToolbar()
		self.applyFilters()
		self.drawColumns()
		return 0

	# the game cuts digits off the end of a widget name in the events, so the slot is a letter
	def getTableName(self, iSlot):
		return "TROTable" + chr(65 + iSlot)

	def getKeyId(self, szName):
		iKey = getattr(InputTypes, szName, None)
		if iKey == None:
			return -12345
		return int(iKey)

	# the names that the search field completes: cities, Europe and the goods of the routes (the ones that are used most often first)
	def buildSearchData(self):
		self.dCandidates = {}
		self.dYieldNames = {}
		for dTransport in self.Transports:
			for tRoute in dTransport["routes"]:
				if not self.dYieldNames.has_key(tRoute[2]):
					self.dYieldNames[tRoute[2]] = gc.getYieldInfo(tRoute[2]).getDescription()
				for szName in (tRoute[1], tRoute[3], self.dYieldNames[tRoute[2]]):
					szLower = szName.lower()
					if self.dCandidates.has_key(szLower):
						self.dCandidates[szLower][1] += 1
					else:
						self.dCandidates[szLower] = [szName, 1]

	def drawToolbar(self):
		screen = self.getScreen()
		iY = self.TOOLBAR_Y
		screen.addDropDownBoxGFC("TROType", self.MARGIN, iY, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("TROType", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_TYPE_ROUTES", ()), 0, 0, True)
		screen.addPullDownString("TROType", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_TYPE_AUTO", ()), 1, 1, False)
		screen.addDropDownBoxGFC("TRODomain", self.MARGIN + 310, iY, 230, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("TRODomain", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_LAND_SEA", ()), 0, 0, True)
		screen.addPullDownString("TRODomain", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_LAND", ()), 1, 1, False)
		screen.addPullDownString("TRODomain", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_SEA", ()), 2, 2, False)
		screen.addDropDownBoxGFC("TROAssign", self.MARGIN + 550, iY, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("TROAssign", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_ALL", ()), 0, 0, False)
		screen.addPullDownString("TROAssign", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_WITH_ROUTES", ()), 1, 1, True)
		screen.addPullDownString("TROAssign", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_WITHOUT_ROUTES", ()), 2, 2, False)
		# the search field (typed with the keyboard, the rest of the best match is suggested in grey)
		self.iSearchX = self.MARGIN + 870
		self.iSearchW = 520
		screen.addPanel("TROSearchBG", u"", u"", False, False, self.iSearchX, iY - 2, self.iSearchW, 34, PanelStyles.PANEL_STYLE_IN, WidgetTypes.WIDGET_GENERAL, BTN_SEARCH, -1)
		screen.setButtonGFC("TROClearSearch", u"<font=3b>X</font>", "", self.iSearchX + self.iSearchW + 8, iY - 2, 40, 34, WidgetTypes.WIDGET_GENERAL, BTN_CLEAR_SEARCH, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		self.drawSearchText()

	def drawSearchText(self):
		screen = self.getScreen()
		# the field is always active (every key goes to it): a cursor shows that, the hint stays grey behind it.
		# After a click the text is shown selected (gold): the next key replaces it
		szCursor = u"<color=255,220,100>|</color>"
		if len(self.szQuery) == 0:
			if self.bSearchSelected:
				szText = szCursor
			else:
				szText = szCursor + u"<color=140,140,140> " + localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_SEARCH_HINT", ()) + u"</color>"
		elif self.bSearchSelected:
			szText = u"<color=255,220,100>" + self.szQuery + u"</color>" + szCursor
		elif len(self.szSuggestion) > len(self.szQuery):
			szText = u"<color=255,255,255>" + self.szSuggestion[:len(self.szQuery)] + u"</color>" + szCursor + u"<color=130,130,130>" + self.szSuggestion[len(self.szQuery):] + u"</color>"
		else:
			szText = u"<color=255,255,255>" + self.szQuery + u"</color>" + szCursor
		screen.setTextAt("TROSearchText", "TROSearchBG", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 10, 7, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, BTN_SEARCH, -1)
		screen.show("TROSearchText")

	# the best completion of the typed text: a name that starts with it, the most used one first
	def findSuggestion(self):
		self.szSuggestion = u""
		szQuery = self.szQuery.lower()
		if len(szQuery) == 0:
			return
		aMatches = []
		for szLower in self.dCandidates.keys():
			if szLower[:len(szQuery)] == szQuery and len(szLower) > len(szQuery):
				aMatches.append((-self.dCandidates[szLower][1], szLower, self.dCandidates[szLower][0]))
		if len(aMatches) > 0:
			aMatches.sort()
			self.szSuggestion = aMatches[0][2]

	# which transports (and which of their routes) are shown
	def applyFilters(self):
		self.aVisible = []
		szQuery = self.szQuery.lower()
		for iIndex in range(len(self.Transports)):
			dTransport = self.Transports[iIndex]
			bAuto = dTransport["auto"]
			iAssigned = self.getAssignedCount(dTransport)
			if dTransport.get("manualSet", False):
				bAuto = dTransport["frozenAuto"]
				iAssigned = dTransport["frozenAssigned"]
			if self.iTypeFilter == 0 and bAuto:
				continue
			if self.iTypeFilter == 1 and not bAuto:
				continue
			if self.iDomainFilter == 1 and not dTransport["land"]:
				continue
			if self.iDomainFilter == 2 and dTransport["land"]:
				continue
			if self.iTypeFilter == 0:
				if self.iAssignFilter == 1 and iAssigned == 0:
					continue
				if self.iAssignFilter == 2 and iAssigned > 0:
					continue
			if len(szQuery) > 0:
				bFound = False
				for tRoute in dTransport["routes"]:
					if self.routeMatches(tRoute, szQuery):
						bFound = True
						break
				if not bFound:
					continue
			self.aVisible.append(iIndex)

	def routeMatches(self, tRoute, szQuery):
		if len(szQuery) == 0:
			return True
		if tRoute[1].lower().find(szQuery) >= 0 or tRoute[3].lower().find(szQuery) >= 0:
			return True
		return self.dYieldNames[tRoute[2]].lower().find(szQuery) >= 0

	# everything that is needed of a transport, read once when the screen opens (the routes are plain data, the assignment is edited here)
	def readTransport(self, pGroup, pHead):
		dTransport = {}
		dTransport["unit"] = pHead.getID()
		dTransport["name"] = pHead.getName()
		dTransport["button"] = pHead.getButton()
		dTransport["size"] = pGroup.getNumUnits()
		dTransport["land"] = (pHead.getDomainType() == DomainTypes.DOMAIN_LAND)
		iFull = gc.getInfoTypeForString("AUTOMATE_TRANSPORT_FULL")
		dTransport["auto"] = (iFull != -1 and pGroup.getAutomateType() == iFull)
		dTransport["rawName"] = pHead.getNameNoDesc()
		logOverview("transport %d '%s' automate type %d" % (pHead.getID(), pHead.getNameNoDesc(), int(pGroup.getAutomateType())))
		pPlot = pHead.plot()
		szWhere = u"(%d, %d)" % (pHead.getX(), pHead.getY())
		if pPlot != None and not pPlot.isNone() and pPlot.isCity():
			pCity = pPlot.getPlotCity()
			if pCity != None and not pCity.isNone():
				szWhere = pCity.getName()
		dTransport["where"] = szWhere

		aRoutes = []
		dAssigned = {}
		dOriginal = {}
		for pRoute in self.player.getViableTradeRoutes(pHead):
			iRoute = pRoute.getID()
			bAssigned = pGroup.isAssignedTradeRoute(iRoute)
			aRoutes.append((not bAssigned, pRoute.getSourceCityName(), pRoute.getYield(), pRoute.getDestinationCityName(), iRoute, pRoute.getDistanceBetweenCities(), pRoute.isPrivate(), pRoute.isReserved(), pRoute.getDestinationCity().iID == -1))
			dAssigned[iRoute] = bAssigned
			dOriginal[iRoute] = bAssigned
		aRoutes.sort() # assigned routes first, then by source, yield and destination
		dTransport["routes"] = aRoutes
		dTransport["assigned"] = dAssigned
		dTransport["original"] = dOriginal
		return dTransport

	def getAssignedCount(self, dTransport):
		iCount = 0
		for iRoute in dTransport["assigned"].keys():
			if dTransport["assigned"][iRoute]:
				iCount += 1
		return iCount

	def drawColumns(self):
		screen = self.getScreen()
		iNum = len(self.aVisible)
		iMaxFirst = max(0, iNum - self.iNumVisible)
		if self.iFirst > iMaxFirst:
			self.iFirst = iMaxFirst
		if self.iFirst < 0:
			self.iFirst = 0

		# the columns are centered when they do not fill the width
		iShown = min(self.iNumVisible, iNum - self.iFirst)
		iTotalWidth = iShown * self.COL_WIDTH + (iShown - 1) * self.GAP
		iStartX = (self.XResolution - iTotalWidth) / 2

		self.aColumnX = []
		for iSlot in range(iShown):
			dTransport = self.Transports[self.aVisible[self.iFirst + iSlot]]
			iX = iStartX + iSlot * (self.COL_WIDTH + self.GAP)
			self.aColumnX.append(iX)
			self.drawHeader(iSlot, dTransport, iX)
			self.drawTable(iSlot, dTransport, iX)
		for iSlot in range(iShown, self.iUsedSlots):
			screen.hide("TROUnit" + str(iSlot))
			screen.hide("TROName" + str(iSlot))
			screen.hide("TROInfo" + str(iSlot))
			screen.hide("TROManual" + str(iSlot))
			screen.hide("TROManualDone" + str(iSlot))
			screen.hide(self.getTableName(iSlot))
		self.iUsedSlots = iShown

		# the position label between the navigation buttons
		szPosition = localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_POSITION", (self.iFirst + min(1, iShown), self.iFirst + iShown, iNum))
		screen.setLabelAt("TROPosition", self.BACKGROUND_ID, u"<font=3>" + szPosition + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, self.NAV_Y + 6, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.show("TROPosition")
		if iNum <= self.iNumVisible:
			screen.hide("TROPrev")
			screen.hide("TRONext")
			screen.hide("TROPrevPage")
			screen.hide("TRONextPage")
		else:
			screen.show("TROPrev")
			screen.show("TRONext")
			screen.show("TROPrevPage")
			screen.show("TRONextPage")

	def drawHeader(self, iSlot, dTransport, iX):
		screen = self.getScreen()
		szUnit = "TROUnit" + str(iSlot)
		screen.setImageButton(szUnit, dTransport["button"], iX, self.HEAD_Y, 48, 48, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.show(szUnit)
		szName = dTransport["name"]
		if dTransport["size"] > 1:
			szName = szName + u" (%d)" % dTransport["size"]
		# a click on the name renames the transport
		screen.setTextAt("TROName" + str(iSlot), self.BACKGROUND_ID, u"<font=3b>" + szName + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 56, self.HEAD_Y + 2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, BTN_RENAME + iSlot, -1)
		screen.show("TROName" + str(iSlot))
		self.drawInfo(iSlot, dTransport, iX)

	def drawInfo(self, iSlot, dTransport, iX):
		screen = self.getScreen()
		szInfo = dTransport["where"] + u"   " + localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_ASSIGNED", (self.getAssignedCount(dTransport), len(dTransport["routes"])))
		screen.setLabelAt("TROInfo" + str(iSlot), self.BACKGROUND_ID, u"<font=2>" + szInfo + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 56, self.HEAD_Y + 28, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.show("TROInfo" + str(iSlot))
		# a transport with an automation (full automation or trade routes) can be set back to manual here; afterwards a red text says so
		szManual = "TROManual" + str(iSlot)
		szDone = "TROManualDone" + str(iSlot)
		if dTransport.get("manualSet", False):
			screen.hide(szManual)
			screen.setLabelAt(szDone, self.BACKGROUND_ID, u"<font=3b><color=255,60,60>" + localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_MANUAL_DONE", ()) + u"</color></font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 56, self.HEAD_Y + 50, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.show(szDone)
		elif dTransport["auto"] or self.getAssignedCount(dTransport) > 0:
			screen.hide(szDone)
			screen.setButtonGFC(szManual, u"<font=2>" + localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_MANUAL", ()) + u"</font>", "", iX + 56, self.HEAD_Y + 46, 170, 26, WidgetTypes.WIDGET_GENERAL, BTN_MANUAL + iSlot, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
			screen.show(szManual)
		else:
			screen.hide(szManual)
			screen.hide(szDone)

	def drawTable(self, iSlot, dTransport, iX):
		screen = self.getScreen()
		szTable = self.getTableName(iSlot)
		screen.addTableControlGFC(szTable, 6, iX, self.TABLE_Y, self.COL_WIDTH, self.TABLE_HEIGHT, True, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setStyle(szTable, "Table_StandardCiv_Style")
		screen.enableSort(szTable)
		screen.enableSelect(szTable, False)
		iCityWidth = (self.COL_WIDTH - 32 - 32 - 44 - 24) / 2
		screen.setTableColumnHeader(szTable, 0, u"id", 0)
		screen.setTableColumnHeader(szTable, 1, u"", 32)
		screen.setTableColumnHeader(szTable, 2, u"", 32)
		screen.setTableColumnHeader(szTable, 3, localText.getText("TXT_KEY_TRADE_ROUTES_MAIN_TABLE_3", ()), iCityWidth)
		screen.setTableColumnHeader(szTable, 4, localText.getText("TXT_KEY_TRADE_ROUTES_MAIN_TABLE_4", ()), iCityWidth)
		screen.setTableColumnHeader(szTable, 5, localText.getText("TXT_KEY_TRADE_ROUTES_MAIN_TABLE_5", ()), 44)
		aRoutes = []
		szQuery = self.szQuery.lower()
		for tRoute in dTransport["routes"]:
			if self.routeMatches(tRoute, szQuery):
				aRoutes.append(tRoute)
		self.aShownRoutes[iSlot] = aRoutes
		for iRow in range(len(aRoutes)):
			screen.appendTableRow(szTable)
			screen.setTableRowHeight(szTable, iRow, self.ROW_HEIGHT)
			self.fillRow(szTable, iRow, aRoutes[iRow], dTransport["assigned"][aRoutes[iRow][4]])
		screen.show(szTable)

	def fillRow(self, szTable, iRow, tRoute, bAssigned):
		screen = self.getScreen()
		iRoute = tRoute[4]
		if bAssigned:
			szColor = u"<color=120,255,120>"
			szCheck = u"%c" % CyGame().getSymbolID(FontSymbols.CHECKBOX_SELECTED_CHAR)
		else:
			szCheck = u"%c" % CyGame().getSymbolID(FontSymbols.CHECKBOX_CHAR)
			szColor = u"<color=255,255,255>"
			if tRoute[8]:
				szColor = u"<color=170,170,170>"
			if tRoute[6]:
				szColor = u"<color=120,200,255>"
			elif tRoute[7]:
				szColor = u"<color=255,200,50>"
		screen.setTableText(szTable, 0, iRow, u"%d" % iRoute, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText(szTable, 1, iRow, szCheck, "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText(szTable, 2, iRow, u"<font=3>%c</font>" % gc.getYieldInfo(tRoute[2]).getChar(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)
		screen.setTableText(szTable, 3, iRow, szColor + tRoute[1] + u"</color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, 4, iRow, szColor + tRoute[3] + u"</color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setTableText(szTable, 5, iRow, szColor + (u"%d" % tRoute[5]) + u"</color>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_CENTER_JUSTIFY)

	# a click on a row of the table of a slot: the route of this transport is switched
	def toggleRoute(self, iSlot, iRow):
		iIndex = self.iFirst + iSlot
		if iIndex < 0 or iIndex >= len(self.aVisible):
			return
		screen = self.getScreen()
		szTable = self.getTableName(iSlot)
		iRoute = -1
		try:
			iRoute = int(screen.getTableText(szTable, 0, iRow))
		except:
			logOverview("route id of row %d of %s not readable" % (iRow, szTable))
			aShown = self.aShownRoutes.get(iSlot, [])
			if iRow >= 0 and iRow < len(aShown):
				iRoute = aShown[iRow][4]
		dTransport = self.Transports[self.aVisible[iIndex]]
		if not dTransport["assigned"].has_key(iRoute):
			logOverview("route %d of row %d unknown" % (iRoute, iRow))
			return
		dTransport["assigned"][iRoute] = not dTransport["assigned"][iRoute]
		dTransport["manualSet"] = False
		for tRoute in dTransport["routes"]:
			if tRoute[4] == iRoute:
				self.fillRow(szTable, iRow, tRoute, dTransport["assigned"][iRoute])
				break
		iX = self.aColumnX[iSlot]
		self.drawInfo(iSlot, dTransport, iX)

	def handleInput(self, inputClass):
		iCode = inputClass.getNotifyCode()
		if iCode != NotifyCode.NOTIFY_CHARACTER and iCode != NotifyCode.NOTIFY_CURSOR_MOVE_ON and iCode != NotifyCode.NOTIFY_CURSOR_MOVE_OFF:
			logOverview("event code %d name '%s' button %d data %d/%d x %d y %d" % (int(iCode), inputClass.getFunctionName(), int(inputClass.getButtonType()), inputClass.getData1(), inputClass.getData2(), inputClass.getMouseX(), inputClass.getMouseY()))
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_CHARACTER:
			self.iKeyLog += 1
			if self.iKeyLog <= 40:
				logOverview("key %d id %d" % (inputClass.getData(), inputClass.getID()))
			if inputClass.getID() != 0:
				try:
					self.handleKey(inputClass.getData())
				except:
					import traceback
					logOverview(traceback.format_exc())
			return 0
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:
			szName = inputClass.getFunctionName()
			if szName == "TROType" or szName == "TRODomain" or szName == "TROAssign":
				screen = self.getScreen()
				iValue = screen.getPullDownData(szName, screen.getSelectedPullDownID(szName))
				if szName == "TROType":
					self.iTypeFilter = iValue
				elif szName == "TRODomain":
					self.iDomainFilter = iValue
				else:
					self.iAssignFilter = iValue
				self.refresh()
			elif szName[:8] == "TROTable" and len(szName) == 9:
				try:
					self.toggleRoute(ord(szName[8]) - 65, inputClass.getMouseY())
				except:
					import traceback
					logOverview(traceback.format_exc())
			else:
				logOverview("selected: '%s' x %d y %d" % (szName, inputClass.getMouseX(), inputClass.getMouseY()))
		elif inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED:
			if inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL:
				iData = inputClass.getData1()
				iOld = self.iFirst
				if iData == BTN_PREV:
					self.iFirst -= 1
				elif iData == BTN_NEXT:
					self.iFirst += 1
				elif iData == BTN_PREV_PAGE:
					self.iFirst -= self.iNumVisible
				elif iData == BTN_NEXT_PAGE:
					self.iFirst += self.iNumVisible
				elif iData == BTN_CLEAR_SEARCH:
					self.szQuery = u""
					self.bSearchSelected = False
					self.refresh()
					return 0
				elif iData >= BTN_MANUAL and iData < BTN_MANUAL + 100:
					self.setManual(iData - BTN_MANUAL)
					return 0
				elif iData >= BTN_RENAME and iData < BTN_RENAME + 100:
					self.renameTransport(iData - BTN_RENAME)
					return 0
				elif iData == BTN_SEARCH:
					self.bSearchSelected = True
					self.drawSearchText()
					return 0
				else:
					return 0
				self.iFirst = max(0, min(self.iFirst, max(0, len(self.aVisible) - self.iNumVisible)))
				if self.iFirst != iOld:
					self.drawColumns()
		return 0

	# a key of the search field
	def handleKey(self, iKey):
		bChanged = False
		if self.dKeys.has_key(iKey):
			if self.bSearchSelected:
				self.szQuery = u""
			self.szQuery = self.szQuery + unicode(self.dKeys[iKey])
			bChanged = True
		elif iKey == self.iKeyBack:
			if self.bSearchSelected:
				self.szQuery = u""
			else:
				self.szQuery = self.szQuery[:-1]
			bChanged = True
		elif iKey in self.aKeyAccept:
			if len(self.szSuggestion) > len(self.szQuery) and not self.bSearchSelected:
				self.szQuery = self.szSuggestion
				bChanged = True
		if bChanged:
			self.bSearchSelected = False
			self.refresh()

	def refresh(self):
		self.findSuggestion()
		self.drawSearchText()
		self.applyFilters()
		self.iFirst = 0
		self.drawColumns()

	# back to manual: the automation is switched off (that also takes the trade routes away)
	def setManual(self, iSlot):
		iIndex = self.iFirst + iSlot
		if iIndex < 0 or iIndex >= len(self.aVisible):
			return
		dTransport = self.Transports[self.aVisible[iIndex]]
		CyMessageControl().sendDoCommand(dTransport["unit"], CommandTypes.COMMAND_AUTOMATE, -1, -1, False)
		# it stays in the list (and in its filter) while this screen is open
		dTransport["frozenAuto"] = dTransport["auto"]
		dTransport["frozenAssigned"] = self.getAssignedCount(dTransport)
		dTransport["manualSet"] = True
		dTransport["auto"] = False
		for iRoute in dTransport["assigned"].keys():
			dTransport["assigned"][iRoute] = False
			dTransport["original"][iRoute] = False
		self.drawColumns()

	# the popup that renames a transport (the same one as for the name suggestion, with the current name)
	def renameTransport(self, iSlot):
		iIndex = self.iFirst + iSlot
		if iIndex < 0 or iIndex >= len(self.aVisible):
			return
		dTransport = self.Transports[self.aVisible[iIndex]]
		g_RenameAsked[dTransport["unit"]] = time.time()
		openNamePopup(dTransport["unit"], localText.getText("TXT_KEY_RENAME_UNIT", ()), dTransport["rawName"])
		self.bRenameWatch = True

	# after a rename the new name is shown in the column header (the popup is answered while this screen is open)
	def update(self, fDelta):
		if self.bRenameWatch:
			try:
				for iSlot in range(self.iUsedSlots):
					dTransport = self.Transports[self.aVisible[self.iFirst + iSlot]]
					pUnit = self.player.getUnit(dTransport["unit"])
					if pUnit != None and not pUnit.isNone() and pUnit.getNameNoDesc() != dTransport["rawName"]:
						dTransport["rawName"] = pUnit.getNameNoDesc()
						dTransport["name"] = pUnit.getName()
						self.drawHeader(iSlot, dTransport, self.aColumnX[iSlot])
			except:
				pass
		return 0

	def returnToDomestic(self):
		try:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
			popupInfo.setText(u"showDomesticAdvisor")
			popupInfo.addPopup(gc.getGame().getActivePlayer())
		except:
			pass

	def onClose(self):
		# the changes are sent when the screen is closed (as the R screen does), then the advisor opens again
		for dTransport in self.Transports:
			for iRoute in dTransport["assigned"].keys():
				if dTransport["assigned"][iRoute] != dTransport["original"][iRoute]:
					if self.player.getTradeRoute(iRoute).getID() != iRoute: # the route was deleted meanwhile
						continue
					CyMessageControl().sendDoCommand(dTransport["unit"], CommandTypes.COMMAND_ASSIGN_TRADE_ROUTE, iRoute, dTransport["assigned"][iRoute], False)
		try:
			self.askForNames()
		except:
			import traceback
			logOverview(traceback.format_exc())
		self.Transports = []
		self.returnToDomestic()
		return 0

	# transports that got their first trade route here are offered a numbered name (the DLL does the same when a route is set outside this screen)
	def askForNames(self):
		for dTransport in self.Transports:
			if dTransport["auto"]:
				continue
			iBefore = 0
			for iRoute in dTransport["original"].keys():
				if dTransport["original"][iRoute]:
					iBefore += 1
			if iBefore == 0 and self.getAssignedCount(dTransport) > 0:
				offerTransportName(dTransport["unit"], False)
