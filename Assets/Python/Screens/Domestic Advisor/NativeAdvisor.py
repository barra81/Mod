## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import CvScreenEnums

import DomesticAdvisorTable
import BaseAdvisorWindow

## Based on work from R&R, Robert Surcouf,  Domestic Advisor Screen

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

def logWaypoint(szText):
	try:
		f = open("WTP_Waypoint.log", "a")
		f.write(szText + "\n")
		f.close()
	except:
		pass

class NativeAdvisor(BaseAdvisorWindow.BaseAdvisorWindow):
	def __init__(self, parent):
		BaseAdvisorWindow.BaseAdvisorWindow.__init__(self, parent, "NativeStateClass")
	
		self.settlementIcon = gc.getBuildingInfo(BuildingTypes.BUILDING_CHICKEE).getButton()
		self.tradeStationChar = gc.getYieldInfo(YieldTypes.YIELD_TRADE_GOODS).getChar()
		self.tradeStationText = u" %c" % self.tradeStationChar
		
	def getKnownSettlementList(self):
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		knownList = []
		citylist = self.parent.GetNativeCities()
		for iNativeCity in range(len(citylist)):
			pLoopCity = citylist[iNativeCity]
			
			ePlayer = gc.getPlayer(pLoopCity.getOwner())
			
			# figure out if the city should be displayed
			bIsVisited = pLoopCity.isScoutVisited(gc.getGame().getActiveTeam())
			
			# visited cities are always known. No need to test visited cities
			bIsKnown = bIsVisited
			
			if not bIsKnown:
				if (ePlayer.isAlive() and (gc.getTeam(ePlayer.getTeam()).isHasMet(player.getTeam()))):
					bIsKnown = pLoopCity.isRevealed(player.getTeam(), False)
			
			# add a line for every single known native city
			if bIsKnown:
				knownList.append(pLoopCity)
		return knownList

	def contactNation(self, iRow, iPlotIndex = -1):
		try:
			# the table can be sorted: the plot index of the cell identifies the settlement, not the row
			iNative = -1
			if iPlotIndex >= 0:
				pPlot = gc.getMap().plotByIndex(iPlotIndex)
				if pPlot is not None and not pPlot.isNone() and pPlot.isCity():
					iNative = pPlot.getPlotCity().getOwner()
			if iNative < 0:
				citylist = self.getKnownSettlementList()
				if iRow < 0 or iRow >= len(citylist):
					return False
				iNative = citylist[iRow].getOwner()
			player = gc.getPlayer(gc.getGame().getActivePlayer())
			if not player.canContact(iNative):
				return False
			self.parent.getScreen().hideScreen()
			# back to the native info tab when the diplomacy screen is closed (see CvDiplomacy)
			import CvScreensInterface
			CvScreensInterface.bReturnToDomesticAfterDiplomacy = True
			player.contact(iNative)
			return True
		except:
			return False

	def hasOwnPresence(self, pNativeCity, player):
		if pNativeCity.getTradePostPlayer() == player.getID():
			return True
		if pNativeCity.getMissionaryPlayer() == player.getID() and pNativeCity.getMissionaryRate() > 0:
			return True
		return False

	def openWaypointPopup(self, iRow, iPlotIndex = -1):
		try:
			# the table can be sorted: the row is not the index of the list, so the plot index of the cell is used
			pNative = None
			if iPlotIndex >= 0:
				pPlot = gc.getMap().plotByIndex(iPlotIndex)
				if pPlot is not None and not pPlot.isNone() and pPlot.isCity():
					pNative = pPlot.getPlotCity()
			if pNative is None:
				citylist = self.getKnownSettlementList()
				if iRow < 0 or iRow >= len(citylist):
					return False
				pNative = citylist[iRow]
			player = gc.getPlayer(gc.getGame().getActivePlayer())
			if not self.hasOwnPresence(pNative, player):
				logWaypoint("no own presence in row %d" % iRow)
				return False
			self.parent.getScreen().hideScreen()
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_CHOOSEPRODUCTION)
			popupInfo.setData1(pNative.plot().getIndex())
			popupInfo.setData2(1002)
			popupInfo.addPopup(player.getID())
			logWaypoint("popup opened for plot %d" % pNative.plot().getIndex())
			return True
		except:
			import traceback
			logWaypoint(traceback.format_exc())
			return False

	def lookAtSettlement(self, iPlotID):
		plot = gc.getMap().plotByIndex(iPlotID)
		if plot is None or plot.isNone():
			return
		self.parent.getScreen().hideScreen()
		CyCamera().JustLookAtPlot(plot)
		
	def drawTableContent(self):
		citylist = self.getKnownSettlementList()		
		
		self.tableManager.setNumRows(len(citylist))
		
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		
		for iNativeCity in range(len(citylist)):
			pLoopCity = citylist[iNativeCity]
			
			ePlayer = gc.getPlayer(pLoopCity.getOwner())
			
			# figure out if the city should be displayed
			bIsVisited = pLoopCity.isScoutVisited(gc.getGame().getActiveTeam())
			
			if True:
				self.tableManager.addPanelButton(self.settlementIcon, WidgetTypes.WIDGET_JUMP_TO_SETTLEMENT, pLoopCity.plot().getIndex(), iNativeCity)
				self.tableManager.addText(pLoopCity.getName())
				# clickable: opens the diplomacy screen (symbol in front)
				self.tableManager.addText(u"%c " % CyGame().getSymbolID(FontSymbols.OPEN_BORDERS_CHAR) + gc.getPlayer(pLoopCity.getOwner()).getCivilizationShortDescription(0), pLoopCity.plot().getIndex())
				self.tableManager.addInt(pLoopCity.getPopulation())
				
				if bIsVisited:
					self.tableManager.drawChar(gc.getYieldInfo(pLoopCity.AI_getDesiredYield()))
				else:
					self.tableManager.skipCell()
				
				if pLoopCity.getTradePostPlayer() != -1:
					szText = eChar = u" %c" % gc.getCivilizationInfo(gc.getPlayer(pLoopCity.getTradePostPlayer()).getCivilizationType()).getTradingPostChar()
					self.tableManager.addText(szText, pLoopCity.getTradePostPlayer(), -1, player.getWikiWidget())
				else:
					self.tableManager.skipCell()
				
				# mission icon
				if pLoopCity.getMissionaryRate() > 0 and pLoopCity.getMissionaryPlayer() != PlayerTypes.NO_PLAYER:
					pMissionPlayer = gc.getPlayer(pLoopCity.getMissionaryPlayer())
					if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_MORE_VARIABLES_HIDDEN) and pLoopCity.getMissionaryPlayer() == player.getID():
						iModifier = 100 + player.getMissionaryRateModifier()+ ePlayer.getMissionaryRateModifier()
						szText = localText.getText("TXT_KEY_GROWTH", (ePlayer.getMissionaryPoints(pMissionPlayer.getID()),ePlayer.missionaryThreshold(pMissionPlayer.getID()), pLoopCity.getMissionaryRate() * iModifier /100))
						self.tableManager.addText(szText, pMissionPlayer.getID(), -1, pMissionPlayer.getWikiWidget())
					else:
						self.tableManager.drawChar(pMissionPlayer)
				else:
					self.tableManager.skipCell()

				# teach unit
				if bIsVisited:
					self.tableManager.addText(gc.getUnitInfo(pLoopCity.getTeachUnit()).getDescription(), pLoopCity.getTeachUnit(), -1, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT)
				else:
					self.tableManager.skipCell()

				# WTP: waypoint for units created here by a mission / trading post of the player (click to set / remove)
				if self.hasOwnPresence(pLoopCity, player):
					iWaypoint = player.getNativeWaypoint(pLoopCity.plot().getIndex())
					pWaypointCity = None
					if iWaypoint >= 0:
						pWaypointCity = player.getCity(iWaypoint)
					if pWaypointCity is not None and not pWaypointCity.isNone():
						self.tableManager.addText(u"%c " % CyGame().getSymbolID(FontSymbols.MOVES_CHAR) + pWaypointCity.getName(), pLoopCity.plot().getIndex())
					else:
						self.tableManager.addText(u"%c " % CyGame().getSymbolID(FontSymbols.OPEN_BORDERS_CHAR) + localText.getText("TXT_KEY_WTP_WAYPOINT_COLUMN", ()), pLoopCity.plot().getIndex())
				else:
					self.tableManager.skipCell()
	
	def getWidgetHelp(self, argsList):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList

		if (eWidgetType == WidgetTypes.WIDGET_JUMP_TO_SETTLEMENT):
			plot = gc.getMap().plotByIndex(iData1)
			if plot is not None and not plot.isNone() and plot.isCity():
				return localText.getText("TXT_KEY_DOMESTIC_ADVISOR_JUMP_TO_SETTLEMENT_CITY", (plot.getPlotCity().getName(), ))
			return localText.getText("TXT_KEY_DOMESTIC_ADVISOR_JUMP_TO_SETTLEMENT", ())

		return None
	
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (inputClass.getMouseX() == 0):
				self.lookAtSettlement(inputClass.getData1())
				return 0
			# WTP: a click on the civ column opens the diplomacy screen of this nation
			if (inputClass.getMouseX() == 2):
				if self.contactNation(inputClass.getMouseY(), inputClass.getData1()):
					return 0
			# WTP: waypoint column
			logWaypoint("click: column %d row %d data1 %d data2 %d" % (inputClass.getMouseX(), inputClass.getMouseY(), inputClass.getData1(), inputClass.getData2()))
			if (inputClass.getMouseX() == 8):
				if self.openWaypointPopup(inputClass.getMouseY(), inputClass.getData1()):
					return 0
			return -1

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_JUMP_TO_SETTLEMENT):
				self.lookAtSettlement(inputClass.getData1())
				return 0

		return -1
	
	def hide(self):
		self.tableManager.hide()
		
	def setDirty(self):
		self.dirty = True
		
	def createTableHeader(self):
		# create table headers
		self.tableManager.addHeaderButton()
		self.tableManager.addHeaderCityName()
		self.tableManager.addHeaderCityName("CIV")
		self.tableManager.addHeaderTxt("TXT_KEY_POPULATION", 50)
		self.tableManager.addHeaderChar(CyGame().getSymbolID(FontSymbols.TRADE_CHAR))
		self.tableManager.addHeaderChar(self.tradeStationChar)
		
		# not hiding variables requires a wider column for missions
		iCrossWidth = 50
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_MORE_VARIABLES_HIDDEN):
			iCrossWidth = 130
		
		self.tableManager.addHeaderChar(gc.getYieldInfo(YieldTypes.YIELD_CROSSES).getChar(), iCrossWidth)
		self.tableManager.addHeaderTxt("TXT_KEY_PEDIA_SPECIAL_ABILITIES", 200)
		self.tableManager.addHeaderTxt("TXT_KEY_WTP_WAYPOINT_COLUMN", 160)
