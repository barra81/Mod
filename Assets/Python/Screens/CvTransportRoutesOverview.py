## WTP: overview of the trade route assignments of all transports (the "R" screen of every transport side by side)
## Opened from the trade routes tab of the domestic advisor, returns there when it is closed.

from CvPythonExtensions import *
import CvUtil
import CvScreenEnums

gc = CyGlobalContext()
localText = CyTranslator()

# widget data of the buttons
BTN_PREV = 30001
BTN_NEXT = 30002
BTN_PREV_PAGE = 30003
BTN_NEXT_PAGE = 30004

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

		self.XResolution = screen.getXResolution()
		self.YResolution = screen.getYResolution()
		self.iNumVisible = max(1, (self.XResolution - 2 * self.MARGIN + self.GAP) / (self.COL_WIDTH + self.GAP))
		self.iFirst = 0
		self.iUsedSlots = 0
		self.TABLE_Y = 50 + self.HEADER_HEIGHT
		self.EXIT_Y = self.YResolution - 45
		self.NAV_Y = self.EXIT_Y - 42
		self.TABLE_HEIGHT = self.NAV_Y - self.TABLE_Y - 8

		screen.setRenderInterfaceOnly(False)
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
		screen.setDimensions(0, 0, self.XResolution, self.YResolution)
		screen.showWindowBackground(False)
		screen.addPanel(self.BACKGROUND_ID, u"", u"", True, False, 0, 0, self.XResolution, self.YResolution, PanelStyles.PANEL_STYLE_MAIN, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt("TROTitle", self.BACKGROUND_ID, u"<font=4b>" + localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.XResolution / 2, 12, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# navigation row (scrolling to the side) and the exit button at the very bottom
		iButtonW = 60
		screen.setButtonGFC("TROPrevPage", u"<font=3b><<</font>", "", self.MARGIN, self.NAV_Y, iButtonW, 32, WidgetTypes.WIDGET_GENERAL, BTN_PREV_PAGE, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("TROPrev", u"<font=3b><</font>", "", self.MARGIN + iButtonW + 8, self.NAV_Y, iButtonW, 32, WidgetTypes.WIDGET_GENERAL, BTN_PREV, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("TRONext", u"<font=3b>></font>", "", self.XResolution - self.MARGIN - 2 * iButtonW - 8, self.NAV_Y, iButtonW, 32, WidgetTypes.WIDGET_GENERAL, BTN_NEXT, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("TRONextPage", u">>", "", self.XResolution - self.MARGIN - iButtonW, self.NAV_Y, iButtonW, 32, WidgetTypes.WIDGET_GENERAL, BTN_NEXT_PAGE, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setButtonGFC("ScreenExit", u"<font=3b>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + u"</font>", "", self.MARGIN, self.EXIT_Y, self.XResolution - 2 * self.MARGIN, 30, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
		screen.setActivation("ScreenExit", ActivationTypes.ACTIVATE_MIMICPARENTFOCUS)

		self.drawColumns()
		return 0

	# everything that is needed of a transport, read once when the screen opens (the routes are plain data, the assignment is edited here)
	def readTransport(self, pGroup, pHead):
		dTransport = {}
		dTransport["unit"] = pHead.getID()
		dTransport["name"] = pHead.getName()
		dTransport["button"] = pHead.getButton()
		dTransport["size"] = pGroup.getNumUnits()
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
		iNum = len(self.Transports)
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
			dTransport = self.Transports[self.iFirst + iSlot]
			iX = iStartX + iSlot * (self.COL_WIDTH + self.GAP)
			self.aColumnX.append(iX)
			self.drawHeader(iSlot, dTransport, iX)
			self.drawTable(iSlot, dTransport, iX)
		for iSlot in range(iShown, self.iUsedSlots):
			screen.hide("TROUnit" + str(iSlot))
			screen.hide("TROName" + str(iSlot))
			screen.hide("TROInfo" + str(iSlot))
			screen.hide("TROTable" + str(iSlot))
		self.iUsedSlots = iShown

		# the position label between the navigation buttons
		szPosition = localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_POSITION", (self.iFirst + 1, self.iFirst + iShown, iNum))
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
		screen.setImageButton(szUnit, dTransport["button"], iX, 50, 48, 48, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.show(szUnit)
		szName = dTransport["name"]
		if dTransport["size"] > 1:
			szName = szName + u" (%d)" % dTransport["size"]
		screen.setLabelAt("TROName" + str(iSlot), self.BACKGROUND_ID, u"<font=3b>" + szName + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 56, 52, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.show("TROName" + str(iSlot))
		self.drawInfo(iSlot, dTransport, iX)

	def drawInfo(self, iSlot, dTransport, iX):
		screen = self.getScreen()
		szInfo = dTransport["where"] + u"   " + localText.getText("TXT_KEY_WTP_TRANSPORT_OVERVIEW_ASSIGNED", (self.getAssignedCount(dTransport), len(dTransport["routes"])))
		screen.setLabelAt("TROInfo" + str(iSlot), self.BACKGROUND_ID, u"<font=2>" + szInfo + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, iX + 56, 78, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.show("TROInfo" + str(iSlot))

	def drawTable(self, iSlot, dTransport, iX):
		screen = self.getScreen()
		szTable = "TROTable" + str(iSlot)
		screen.addTableControlGFC(szTable, 6, iX, self.TABLE_Y, self.COL_WIDTH, self.TABLE_HEIGHT, True, False, 32, 32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setStyle(szTable, "Table_StandardCiv_Style")
		screen.enableSelect(szTable, False)
		iCityWidth = (self.COL_WIDTH - 32 - 32 - 44 - 24) / 2
		screen.setTableColumnHeader(szTable, 0, u"id", 0)
		screen.setTableColumnHeader(szTable, 1, u"", 32)
		screen.setTableColumnHeader(szTable, 2, u"", 32)
		screen.setTableColumnHeader(szTable, 3, localText.getText("TXT_KEY_TRADE_ROUTES_MAIN_TABLE_3", ()), iCityWidth)
		screen.setTableColumnHeader(szTable, 4, localText.getText("TXT_KEY_TRADE_ROUTES_MAIN_TABLE_4", ()), iCityWidth)
		screen.setTableColumnHeader(szTable, 5, localText.getText("TXT_KEY_TRADE_ROUTES_MAIN_TABLE_5", ()), 44)
		aRoutes = dTransport["routes"]
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
		if iIndex < 0 or iIndex >= len(self.Transports):
			return
		screen = self.getScreen()
		szTable = "TROTable" + str(iSlot)
		try:
			iRoute = int(screen.getTableText(szTable, 0, iRow))
		except:
			return
		dTransport = self.Transports[iIndex]
		if not dTransport["assigned"].has_key(iRoute):
			return
		dTransport["assigned"][iRoute] = not dTransport["assigned"][iRoute]
		for tRoute in dTransport["routes"]:
			if tRoute[4] == iRoute:
				self.fillRow(szTable, iRow, tRoute, dTransport["assigned"][iRoute])
				break
		iX = self.aColumnX[iSlot]
		self.drawInfo(iSlot, dTransport, iX)

	def handleInput(self, inputClass):
		if inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED:
			szName = inputClass.getFunctionName()
			if szName[:8] == "TROTable":
				try:
					self.toggleRoute(int(szName[8:]), inputClass.getMouseY())
				except:
					pass
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
				else:
					return 0
				self.iFirst = max(0, min(self.iFirst, max(0, len(self.Transports) - self.iNumVisible)))
				if self.iFirst != iOld:
					self.drawColumns()
		return 0

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
