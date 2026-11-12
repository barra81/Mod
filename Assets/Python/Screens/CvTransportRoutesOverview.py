## WTP: overview of the trade route assignments of all transports (the "R" screen of every transport side by side)
## Opened from the trade routes tab of the domestic advisor, returns there when it is closed.

from CvPythonExtensions import *
import CvUtil
import CvScreenEnums

gc = CyGlobalContext()
localText = CyTranslator()
ArtFileMgr = CyArtFileMgr()

# widget data of the buttons
BTN_PREV = 30001
BTN_NEXT = 30002
BTN_PREV_PAGE = 30003
BTN_NEXT_PAGE = 30004
BTN_CLEAR_SEARCH = 30005

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
		self.aShownRoutes = {} # slot -> the routes in the order of the rows
		self.aVisible = [] # indices of the transports that pass the filters
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
		self.iDomainFilter = 0
		self.iAssignFilter = 0
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

		screen.setRenderInterfaceOnly(False)
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
		screen.addDropDownBoxGFC("TRODomain", self.MARGIN, iY, 230, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("TRODomain", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_LAND_SEA", ()), 0, 0, True)
		screen.addPullDownString("TRODomain", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_LAND", ()), 1, 1, False)
		screen.addPullDownString("TRODomain", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_SEA", ()), 2, 2, False)
		screen.addDropDownBoxGFC("TROAssign", self.MARGIN + 240, iY, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
		screen.addPullDownString("TROAssign", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_ALL", ()), 0, 0, True)
		screen.addPullDownString("TROAssign", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_WITH_ROUTES", ()), 1, 1, False)
		screen.addPullDownString("TROAssign", localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_WITHOUT_ROUTES", ()), 2, 2, False)
		# the search field (typed with the keyboard, the rest of the best match is suggested in grey)
		self.iSearchX = self.MARGIN + 560
		self.iSearchW = 520
		screen.addPanel("TROSearchBG", u"", u"", False, False, self.iSearchX, iY - 2, self.iSearchW, 34, PanelStyles.PANEL_STYLE_IN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setButtonGFC("TROClearSearch", u"<font=3b>X</font>", "", self.iSearchX + self.iSearchW + 8, iY - 2, 40, 34, WidgetTypes.WIDGET_GENERAL, BTN_CLEAR_SEARCH, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		self.drawSearchText()

	def drawSearchText(self):
		screen = self.getScreen()
		if len(self.szQuery) == 0:
			szText = u"<color=140,140,140>" + localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_SEARCH_HINT", ()) + u"</color>"
		elif len(self.szSuggestion) > len(self.szQuery):
			szText = u"<color=255,255,255>" + self.szSuggestion[:len(self.szQuery)] + u"</color><color=130,130,130>" + self.szSuggestion[len(self.szQuery):] + u"</color>"
		else:
			szText = u"<color=255,255,255>" + self.szQuery + u"</color>"
		screen.setLabelAt("TROSearchText", "TROSearchBG", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 10, 7, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
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
			if self.iDomainFilter == 1 and not dTransport["land"]:
				continue
			if self.iDomainFilter == 2 and dTransport["land"]:
				continue
			iAssigned = self.getAssignedCount(dTransport)
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
		screen.setLabelAt("TROName" + str(iSlot), self.BACKGROUND_ID, u"<font=3b>" + szName + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 56, self.HEAD_Y + 2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.show("TROName" + str(iSlot))
		self.drawInfo(iSlot, dTransport, iX)

	def drawInfo(self, iSlot, dTransport, iX):
		screen = self.getScreen()
		szInfo = dTransport["where"] + u"   " + localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_ASSIGNED", (self.getAssignedCount(dTransport), len(dTransport["routes"])))
		screen.setLabelAt("TROInfo" + str(iSlot), self.BACKGROUND_ID, u"<font=2>" + szInfo + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 56, self.HEAD_Y + 28, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.show("TROInfo" + str(iSlot))

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
			if szName == "TRODomain" or szName == "TROAssign":
				screen = self.getScreen()
				iValue = screen.getPullDownData(szName, screen.getSelectedPullDownID(szName))
				if szName == "TRODomain":
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
					self.refresh()
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
			self.szQuery = self.szQuery + unicode(self.dKeys[iKey])
			bChanged = True
		elif iKey == self.iKeyBack:
			self.szQuery = self.szQuery[:-1]
			bChanged = True
		elif iKey in self.aKeyAccept:
			if len(self.szSuggestion) > len(self.szQuery):
				self.szQuery = self.szSuggestion
				bChanged = True
		if bChanged:
			self.refresh()

	def refresh(self):
		self.findSuggestion()
		self.drawSearchText()
		self.applyFilters()
		self.iFirst = 0
		self.drawColumns()

	def update(self, fDelta):
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
		self.Transports = []
		self.returnToDomestic()
		return 0
