## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## New TAC - Interface
## Version 1.02
## by koma13 & Fankman
##


from CvPythonExtensions import *
import CvUtil
import WtpColors
import ScreenInput
import CvScreenEnums
# Achievements START
import CvScreensInterface
# Achievements END
import CvEventInterface
import time
import re
import sdToolKit
import sys
import math

# GLOBAL SYSTEM SHORTCUTS
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

# GLOBAL INFOCLASS COUNTS
g_NumEmphasizeInfos = 0
g_NumHurryInfos = 0
g_NumActionInfos = 0
g_eEndTurnButtonState = -1

# GLOBAL INITIALIZATION BOOLEAN
INITIALIZED = False
abandon_city_ZeroRedraw = True # TAC abandon city - Do we redraw if a pop 0 city is viewed?

# GLOBAL RESOLUTION VALUES
xResolution = -1
yResolution = -1

# GLOBAL INTERFACE FUNDAMENTAL CONSTRUCTS
FLAG_WIDTH = -1
FLAG_PERCENT_WIDTH = 8

MINI_MAP_WIDTH = -1
MINI_MAP_PERCENT_WIDTH = 30

LOWER_RIGHT_CORNER_BACKGROUND_WIDTH = MINI_MAP_WIDTH

SADDLE_HEIGHT = -1
SADDLE_HEIGHT_PERCENT = 31

LOWER_LEFT_CORNER_BACKGROUND_WIDTH = -1
LOWER_LEFT_CORNER_BACKGROUND_PERCENT_WIDTH = 22

LOWER_LEFT_CORNER_BACKGROUND_HEIGHT = -1
LOWER_LEFT_CORNER_BACKGROUND_PERCENT_HEIGHT = 25

LOWER_RIGHT_CORNER_BACKGROUND_WIDTH = -1
LOWER_RIGHT_CORNER_BACKGROUND_WIDTH_PERCENT = 19

LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT = -1
LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT_PERCENT = 10

BOTTOM_CENTER_HUD_HEIGHT = -1
BOTTOM_CENTER_HUD_PERCENT_HEIGHT = 15

TOP_CORNER_HUD_WIDTHS = -1
TOP_CORNER_HUD_PERCENT_WIDTH = 20

TOP_CORNER_HUD_HEIGHT = -1
TOP_CORNER_HUD_PERCENT_HEIGHT = 8

TOP_CENTER_HUD_HEIGHT = -1
TOP_CENTER_HUD_PERCENT_HEIGHT = 8

TOP_CENTER_HUD_WIDTH = -1
TOP_CENTER_HUD_PERCENT_WIDTH = 45

CITIZEN_BAR_HEIGHT = -1
CITIZEN_BAR_PERCENT_HEIGHT = 10

CITY_TITLE_BAR_HEIGHT = -1
CITY_TITLE_BAR_PERCENT_HEIGHT = 5

TRANSPORT_AREA_HEIGHT = -1

CITIZEN_BAR_WIDTH = -1
CITIZEN_BAR_WIDTH_PERCENT = 80

STACK_BAR_HEIGHT = -1
STACK_BAR_PERCENT_HEIGHT = 2.7

EJECT_AREA_WIDTH = -1
EJECT_AREA_PERCENT_WIDTH = 6

MINI_MAP_RADIUS = -1
MINI_MAP_PERCENT_RADIUS = 31

LEFT_PLOT_LIST_EDGE = -1
LEFT_PLOT_LIST_PERCENT_EDGE = 40

RIGHT_PLOT_LIST_EDGE = -1
RIGHT_PLOT_LIST_PERCENT_EDGE = 25

MAIN_LARGE_PORTRAIT_HEIGHT = -1
MAIN_LARGE_PORTRAIT_PERCENT_HEIGHT = 22

MAIN_LARGE_PORTRAIT_WIDTH = -1
MAIL_LARGE_PORTRAIT_PERCENT_WIDTH = 10

UNIT_PORTRAIT_HEIGHT = -1
UNIT_PORTRAIT_PERCENT_HEIGHT = 15

UNIT_HEALTH_BAR_WIDTH = -1
UNIT_HEALHT_BAR_PERCENT_WIDTH = 17

CITY_VIEW_BOX_HEIGHT_AND_WIDTH = -1
# 41: leave room for bonus icons on the outer plots (38 clipped top/right).
CITY_VIEW_BOX_PERCENT_HEIGHT = 41
CITY_VIEW_BOX_MODIFIED_PERCENT_HEIGHT_AND_WIDTH = -1

CITY_MULTI_TAB_AREA_HEIGHT = -1
CITY_MULTI_TAB_SIZE = -1

MAP_EDGE_MARGIN_WIDTH = -1
MAP_EDGE_MARGIN_PERCENT_WIDTH = 0.7

BUILD_AREA_WIDTH = -1
BUILD_AREA_HEIGHT = -1

SMALL_BUTTON_SIZE = -1
MEDIUM_BUTTON_SIZE = -1
LARGE_BUTTON_SIZE = -1
STANDARD_FONT_SIZE = -1

ASPECT_RATIO = -1
ASPECT_ADJUSTMENT = -1

RESOURCE_TABLE_COLUMN_WIDTH = -1
RESOURCE_TABLE_MARGIN = -1

AVOID_GROWTH = -1
SHOW_ALL_YIELDS = -1

HELPTEXT_AREA_Y_MARGIN = 0
HELTTEXT_AREA_X_MARGIN = 7
HELPTEXT_AREA_MAX_WIDTH = 400
HELPTEXT_AREA_MIN_WIDTH = 150

# CITY BUILDINGS GRID MAP
BUILDING_DATA = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

BUILDING_DATA[0] = [30, 18, 20, 12] #Bells
BUILDING_DATA[1] = [72, 2, 20, 12] #Courthouse
BUILDING_DATA[2] = [44, 20, 20, 12] #Hammers
BUILDING_DATA[3] = [58, 18, 20, 12] #Meat
BUILDING_DATA[4] = [30, 36, 20, 12] #Coats
BUILDING_DATA[5] = [44, 38, 20, 12] #Leather
BUILDING_DATA[6] = [44, 2, 20, 12] #Cloth
BUILDING_DATA[7] = [58, 36, 20, 12] #Coloured Cloth
BUILDING_DATA[8] = [16, 38, 20, 12] #Beer
BUILDING_DATA[9] = [58, 0, 20, 12] #Rum
BUILDING_DATA[10] = [58, 54, 20, 12] #Wine
BUILDING_DATA[11] = [16, 20, 20, 12] #Cigars
BUILDING_DATA[12] = [86, 18, 20, 12] #Whale oil
BUILDING_DATA[13] = [30, 54, 20, 12] #Furniture
BUILDING_DATA[14] = [2, 18, 20, 12] #Tools
BUILDING_DATA[15] = [30, 0, 20, 12] #Crosses
BUILDING_DATA[16] = [2, 36, 20, 12] #Muskets
BUILDING_DATA[17] = [2, 0, 20, 12] #Fireworker
BUILDING_DATA[18] = [30, 72, 20, 12] #Horses
BUILDING_DATA[19] = [86, 36, 20, 12] #Dock
BUILDING_DATA[20] = [86, 54, 20, 12] #WareHouse
BUILDING_DATA[21] = [2, 54, 20, 12] #Spices
BUILDING_DATA[22] = [44, 74, 20, 12] #Domestic Market
BUILDING_DATA[23] = [86, 0, 20, 12] #Tavern
BUILDING_DATA[24] = [16, 2, 20, 12] #Education
BUILDING_DATA[25] = [87, 78, 20, 10] #Wall
BUILDING_DATA[26] = [72, 74, 20, 10] #Print
BUILDING_DATA[27] = [2, 89, 20, 9] #Mill
BUILDING_DATA[28] = [72, 86, 20, 10] #Trainstation
BUILDING_DATA[29] = [32, 89, 20, 7] #Corn
BUILDING_DATA[30] = [72, 38, 20, 12] #Medical Care
BUILDING_DATA[31] = [18, 88, 20, 8] #Well
BUILDING_DATA[32] = [84, 73, 20, 10] #Defense
BUILDING_DATA[33] = [44, 56, 20, 12] #Confectioner
BUILDING_DATA[34] = [16, 56, 20, 12] #Leather Padder
BUILDING_DATA[35] = [2, 72, 20, 12] #Cooking Oil Trader
BUILDING_DATA[36] = [58, 72, 20, 12] #Peanut Roaster
BUILDING_DATA[37] = [72, 56, 20, 12] #Potter
BUILDING_DATA[38] = [72, 20, 20, 12] #Tailor
BUILDING_DATA[39] = [16, 74, 20, 12] #Baker
BUILDING_DATA[40] = [81, 88, 20, 7] #Statue
BUILDING_DATA[41] = [45, 88, 20, 10] #Graveyard
BUILDING_DATA[42] = [59, 86, 20, 10] #Jail

BUILDING_GRID = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

BUILDING_AREA_WIDTH = -1
BUILDING_AREA_HEIGHT = -1

# PANEL TOGGLE CONTROLS
BUILDING_MANAGMENT_TOGGLE = 1000
AUTOMATION_MANAGMENT_TOGGLE = 1001
MAP_MANAGMENT_TOGGLE = 1002
GO_TO_CITY = 1003

# Achievements START
ACHIEVE_ADVISOR_SCREEN_MI = 4200
WTP_CYCLE_PREV = 4300 # arrows above the R / C button: the previous / next automated transport (data2: the automate type)
WTP_CYCLE_NEXT = 4301
# Achievements END

# R&R, Robert Surcouf VET NewCapacity Help - Start
VET_NEW_CAPACITY = 4201
# R&R, Robert Surcouf VET NewCapacity Help - End

TIMETEXT_ID = 4202

# CITY HAPPINESS vs UNHAPPINESS - START
HELP_TOTAL_HAPPINESS_POSITIVE = 4301
HELP_TOTAL_HAPPINESS_NEGATIVE = 4302
HELP_TOTAL_HAPPINESS_ZERO = 4303
# CITY HAPPINESS vs UNHAPPINESS - END

NEW_HARBOUR_SYSTEM = 4304 # WTP, ray, new Harbour System - START
NEW_BARRACKS_SYSTEM = 4305 # WTP, ray, new Barracks System - START

# CRIME and LAW - START
HELP_TOTAL_LAW_POSITIVE = 4401
HELP_TOTAL_LAW_NEGATIVE = 4402
HELP_TOTAL_LAW_ZERO = 4403
# CRIME and LAW - END

BUILDING_MANAGMENT_PANEL_UP = True
BUILDING_CHANGE_MANAGMENT_PANEL_UP = False
SHIP_MANAGMENT_PANEL_UP = False
AUTOMATION_MANAGMENT_PANEL_UP = False
MAP_MANAGMENT_PANEL_UP = False
GARRISON_MANAGMENT_PANEL_UP = False
SHOW_ALL_YIELDS = True

# HIDE TYPE
HIDE_TYPE_CITY = 0
HIDE_TYPE_MAP = 1
HIDE_TYPE_GLOBAL = 2
HIDE_TYPE_ADVANCED_START = 3
HIDE_TYPE_MINI_MAP = 4
NUM_HIDE_TYPES = 5

# HIDE LEVEL
HIDE_LEVEL_OFF = 0
HIDE_LEVEL_ALL = 1
HIDE_LEVEL_HIDE = 2
HIDE_LEVEL_NORMAL = 3
HIDE_LEVEL_UBER = 4
NUM_HIDE_LEVELS = 5

# BONUS HIDE GROUPS
RESOURCE_TABLE_HIDE = (NUM_HIDE_TYPES * NUM_HIDE_LEVELS) + 1
CITIZEN_HIDE = (NUM_HIDE_TYPES * NUM_HIDE_LEVELS) + 2
ACTION_BUTTON_HIDE = (NUM_HIDE_TYPES * NUM_HIDE_LEVELS) + 3

# EMPHASIZE DATA
EMPHASIZEYIELDS = []

# INIT MASTER HIDE LIST
MasterHideList = []
for i in range(NUM_HIDE_TYPES):
	SubList = []
	for j in range(NUM_HIDE_LEVELS):
		SubSubList = []
		SubList.append(SubSubList)
	MasterHideList.append(SubList)

# PLOT LIST BUTTONS
NUM_PLOT_LIST_BUTTONS = 1

# GLOBE LAYER OPTION POSITIONING
iGlobeLayerOptionsY_Minimal = 38 # distance from bottom edge
iGlobeLayerOptionHeight = 24

g_pSelectedUnit = 0

# WTP: a transport that was just automated (R menu / full automation) stays the selected unit and is followed on the map
# until another unit is selected or the turn ends
g_LastSelUnit = -1
g_LastSelAuto = -1
g_FollowUnit = -1
g_FollowTicks = 0 # (time.time() of the game is far too coarse here, so the first updates are counted)
g_FollowTurn = -1
g_FollowX = -1
g_FollowY = -1

# WTP: the transport the cycle arrows above the R / C button were last built for and their automate type
g_CycleUnit = -1
g_CycleType = -1
# WTP: the tooltip settings (options screen / Ctrl+Shift+T) are kept in a file in the game folder, so they stay after a restart
TIP_DELAYS = (0, 250, 500, 800, 1200, 2000, -1) # milliseconds, -1: never by itself, only the key X shows the tooltip
TIP_SETTINGS_FILE = "WTP_TooltipSettings.ini"

def wtpLoadTipSettings():
	# (mode, delay index, quick): default is the game tooltip (2), the delay "medium" (2) for the case that the hover tooltip is chosen
	aiValues = [2, 2, 0, 0, 0]
	try:
		f = open(TIP_SETTINGS_FILE, "r")
		for szLine in f.readlines():
			if "=" in szLine:
				aszPart = szLine.strip().split("=")
				try:
					if aszPart[0] == "mode":
						aiValues[0] = max(0, min(2, int(aszPart[1])))
					elif aszPart[0] == "delay":
						aiValues[1] = max(0, min(len(TIP_DELAYS) - 1, int(aszPart[1])))
					elif aszPart[0] == "quick":
						aiValues[2] = max(0, min(1, int(aszPart[1])))
					elif aszPart[0] == "autofreeze":
						aiValues[3] = max(0, min(1, int(aszPart[1])))
					elif aszPart[0] == "debug":
						aiValues[4] = max(0, min(1, int(aszPart[1])))
				except:
					pass
		f.close()
	except:
		pass
	return aiValues

aiTipSettings = wtpLoadTipSettings()

class CvMainInterface:
	"Main Interface Screen"

	BUTTON_TERRITORIAL_INFLUENCE = 750
	BUTTON_TRADE_ROUTE_MANAGER = 765 # WTP: HUD button next to the military advisor: opens the Trade Route Manager
	BUTTON_AUTO_ASSIGN_TARGET = 755 # WTP: city screen: the colony takes colonists of the job automation
	iTopRingFrames = 0 # WTP: frames since the last check of the ships in the ports for the rings of the top bar
	BUTTON_TIP_LINE = 762 # WTP: a line of a frozen hover tooltip (right click: Colopedia)
	dMessagePediaChars = {}
	aMessageConceptPatterns = []
	aMessageNameList = []
	aMessageSpecial = []
	dMessageConcepts = {}
	dMessagePediaCache = {}
	dMessagePediaAll = {} # the same with gold at the end instead of left out (mouse wheel list of the frozen tooltip)
	tMsgRect = (0, 0, 0, 0)
	iMsgW = 0
	iWidgetHelpCount = 0
	bCursorTipShown = False
	iCursorTipLines = 0
	iPreviewPrefDY = 0
	dFrozenPrefDY = {}
	iRedrawFrozen = 0
	dUnitTypeByName = {}
	# the lists of units of the child windows "more...units": the units of a window (by its lines) and the groups of units of its lines
	dUnitWin = {}
	dUnitGroups = {}
	iUnitGroupCounter = 0
	iTipHintLines = 0
	iPreviewHintLines = 0
	iTick = 0 # counted in update() (time.time() of the game is far too coarse)
	iWidgetHelpTick = -1000
	bTipFrozen = False # the hover tooltip is frozen (key X): the cursor can be moved onto it, right click: Colopedia, Esc: close
	tTipLayout = None
	aFrozen = [] # the frozen windows (key X), the last one on top: (widget name prefix, layout, paragraphs, indents, details)
	iFzCounter = 0
	szSuppressHelp = u"" # the text of the window that was just frozen: the tooltip of the same thing does not appear again at once
	iTipSelLevel = -1
	iPreviewParent = -1
	bPreviewDark = False # the window of the preview is the darker variant (the log of a transport)
	tScoreRect = None
	tPreviewLayout = None # the window beside the top frozen window (it can be frozen too): layout, paragraphs, widget name prefix
	aszPreviewParas = []
	szPreviewPrefix = "HudTipC1"
	bXHeld = False # key X is down: a short press freezes, holding it (0.6 s) closes all frozen windows
	bXHoldDone = False
	fXStart = 0.0
	tTipPlacedAt = (-1000, -1000)
	iTipDelay = TIP_DELAYS[aiTipSettings[1]] # (-1: only on the key X) milliseconds the cursor has to rest before the first tooltip appears (options screen, Game tab)
	szPendingHelp = None
	bPendingWidget = False
	fPendingStart = 0.0
	tPendingPos = (0, 0)
	fLastClock = -1.0
	iClockSame = 0
	bClockDead = False
	iTipMode = aiTipSettings[0] # Ctrl+Shift+T: 0 hover tooltip at the cursor, 1 own window at the place of the game tooltip, 2 off (the game tooltip)
	aiTipIndent = []
	dTipDetails = {}
	dNestedDetails = {} # the text of a child window -> the lines of it that have a child window of their own (line -> text), e.g. Statistics -> Logs
	dWideTips = {} # the text of a child window -> 1: the window gets the double maximum width (the log of a transport: long lines)
	aiWrapIndent = []
	bSecondTipShown = False # the window with the Colopedia hint of the line under the cursor in the frozen tooltip
	bExplainShown = False # the window that explains the colored label of a folded line (Stored..., Produced...), on the other side of the parent
	iExplainLines = 0
	bExplainFreezeHint = True # the explanation window gets the hint of the freezing (not the one with the hints of the keys)
	szExplainPrefix = "HudTipE1"
	tExplainLayout = None # its layout, to freeze it together with the window of the list of goods
	aszExplainParas = []
	tExplainKind = None # (class, kind) of the explanation window: ("explain", 0 = stored, 1 = produced), see getStackSpot
	tPreviewKind = None # the same for the child window shown now: ("list", kind) goods of the city, ("filter", kind) their marked goods
	dFrozenKind = {} # frozen windows of the goods of a city: prefix -> (class, kind); stored goods are stacked above produced goods
	dWpWin = {} # frozen windows with lines of waypoints: prefix -> {"unit": (owner, id), "paras": {paragraph: "row" | "new" | number of a waypoint}, "cmd": paragraph of the line Commands or -1}
	tPreviewWp = None # the same for the window of the line that is shown beside a frozen window now (becomes dWpWin[prefix] when it is frozen)
	tPreviewDetails = None # the folded lines of the window beside a frozen window (a line with a child window), for freezing
	iPreviewFreezeLines = 0 # of the hint lines under the second window the last ones (the hint of the freezing)
	fShiftSeen = 0.0 # the time Shift was seen down in the frozen window (the wheel click counts with it for a moment)
	szModMessageSound = "AS2D_POSITIVE_DINK" # the sound of the messages of the mod (notes, warnings)
	szModJumpSound = "AS2D_PING" # the sound of the jump to a waypoint
	tCursorFollow = None # (window, distance of the cursor from its corner, time) after a jump to a waypoint
	dCityWin = {} # frozen tooltips of an own city: prefix -> the city (its name line has the list of the own cities)
	dCityPlotWin = {} # frozen tooltips of a plot with an own city: prefix -> True (the line of the name of the city has the list of the cities)
	tTipCity = None # the own city of the tooltip of the cursor (None: it is not the tooltip of an own city)
	tCityJump = None # after the jump to a city: its tooltip is made and frozen when the camera is there
	bCityHold = False # the jump to a city is not finished: the child windows of the frozen tooltips do not appear yet
	szCityHoldWin = u"" # the window of the city that the jump made (the cursor goes with it until it has found its place)
	tCityHoldPos = None # its place in the last frame
	iCityHoldStill = 0 # the frames it stands still
	tJump = None # (x, y, time) of the last jump to a waypoint
	tLeftClick = None # (window, line, time) of a left click on the line of a window with waypoints
	bLeftJumped = False
	bWheelNeedsShift = True # the wheel click needs Shift (False: the wheel click alone jumps to the waypoint)
	dPaintPlain = {}
	dRowChild = {} # (frozen window, paragraph of its line "Set waypoint...") -> the frozen child window with the list of waypoints
	dWpMarked = {} # the frozen lists of waypoints with a line in yellow (chosen with the wheel)
	dModMessagePlot = {} # text of a message of the mod -> (x, y) of its place
	tTipWp = None # the registration of the line "Set waypoint..." of the tooltip at the cursor (it is in the tooltip already)
	tPreviewUnit = None # the own unit whose tooltip the window beside a frozen window is (it gets the line "Set waypoint..." when it is frozen)
	iWpUnit = -1 # the unit whose next order to move is saved as a waypoint (-1: none)
	fWpStart = 0.0
	dFrozenDark = {} # frozen windows that are always drawn in the darker variant (the explanation of a folded line)
	dFrozenCompanion = {} # frozen windows that belong to the frozen window below them (the explanation of a folded line): they close together
	tSecondTipKey = None
	tAutoFreeze = None # (x, y, time) of the plot of a unit that was activated: its tooltip is frozen as soon as it shows
	szAutoSelPrefix = u"" # the frozen window of the unit that a right click on a line of a stack selected (it goes when another unit is selected)
	tWpRenamePending = None # (number, sea) of a new waypoint: the window for its name opens in the next frame
	fTipSelectAt = -100.0 # the time (seconds) of the last selection of a unit made in a tooltip
	aTradeReturn = [] # the views the jumps from the tooltips of the import / export window started from (the last one is the one to go back to)
	dTraderLines = {} # the lines of the traders in the tooltips: text without colors -> id of the city
	dTraderWin = {} # frozen windows with such lines: prefix -> the good
	bForceTradeTip = False # the tooltip of a good is made although the cursor is not on its picture (refreshTradeTips)
	dNetLines = {} # the line "all colonies, net per turn" in the tooltips: text without colors -> the good
	iTradeTipYield = -1
	szTradeTipText = u""
	tPostJump = None # after a jump: the tooltip of the good is shown and frozen once the cursor is on its picture
	bEscHeld = False
	bEscHoldDone = False
	fEscStart = 0.0
	# the tab stops of the game text: 31 pixels for a line of 22 (see alignTabLines)
	TAB_STOP = 31.0
	iTipSelPara = -1 # the line of the frozen tooltip with a chosen target (shift + mouse wheel) and the index of the target
	iTipSelIdx = 0
	bTipWheel = False
	iTradeSel = -1 # the chosen line: index in the stops of the tooltip, -1: none
	iTradeMarked = -1 # the paragraph that is yellow in the tooltip now
	bTradeSel = False # the wheel is taken
	bTradeChild = False # the child window shown is the one of the chosen line
	szTradeSelFor = u"" # the text of the tooltip (or the name of the frozen window) that the choice is for
	szTradeMarkedWin = u"" # the frozen window that has the yellow line of the choice
	bTipDebug = (aiTipSettings[4] == 1) # options screen: errors in the code of the tooltips are shown as messages (test phase)
	szLastTipError = u""
	dHeaderUnits = {} # frozen window (prefix) -> {paragraph of the name of a unit: (owner, id)} as it was when the window was frozen
	tAutoSelUnit = None # (owner, id) of the unit that the frozen tooltips of szAutoSelPrefix belong to
	fCursorTipShownAt = 0.0 # when the tooltip of the cursor was built (ms)
	iSecondTipLines = 0
	aszTipParas = []
	bHoverTip = (aiTipSettings[0] != 2) # false: the game tooltip
	bHudHover = False # the cursor is on a HUD element / widget with its own help text (until the game reports "no widget" again)
	tHudHoverAt = (0, 0)
	szHudHelp = u"" # the text of the HUD element under the cursor: kept in the help area of the game ourselves (the tooltip of the game is lost when the screen changes)
	szCursorTipText = u""
	tCursorTipAt = (-1000, -1000)
	dMessagePediaNames = None # WTP: lower case name -> (name, Colopedia screen, id), built at the first use
	aszMessageTexts = []
	BUTTON_MESSAGE_PANEL = 756 # WTP: the message panel of the turn (click: expand / collapse)
	BUTTON_MESSAGE_MORE = 758 # WTP: message panel footer: the next older page of messages
	BUTTON_MESSAGE_PREVIOUS = 759 # WTP: message panel footer: the messages of the turn before / back
	BUTTON_MESSAGE_AUTO = 761 # WTP: message panel: auto expand at the start of a turn on / off
	BUTTON_MESSAGE_LINE = 757 # WTP: a line of a message of the message panel (click: center the map on its place)
	BUTTON_MESSAGE_WPS = 763 # WTP: message panel: the toggle "List WPs" (the panel shows the waypoints instead of the messages)
	BUTTON_MESSAGE_WP = 764 # WTP: message panel: a waypoint of the list (iData2 = its index in aMsgWpEntries)
	dMessagePediaAll = {} # the same with gold at the end instead of left out (mouse wheel list of the message panel)
	dMessageLineIndex = {}
	dMessageRects = {} # message -> (x, y, width, height) of its rows in the panel
	tMsgPanelRect = None
	tMsgAutoRect = None # the auto expand label at the top right of the panel (for its help window)
	bMsgWpView = False # the message panel shows the list of the waypoints
	bMsgWpSea = False # ... of the ships (otherwise of the land units); the toggle: off, land, sea, off ...
	iMsgWpPage = 0
	aMsgWpEntries = [] # the waypoints of the list: (sea, number, x, y, name, text of the line)
	aMsgWpRects = [] # (x, y, width, height, index, column) of the waypoints of the page that is shown
	tMsgWpSel = None # what was selected when the list of the waypoints was switched on (see getMsgSelectionKey): the list closes when that changes
	szMsgSelText = u"" # the message with a target chosen by shift + mouse wheel and the index of the target
	iMsgSelIdx = 0
	bMsgWheel = False
	tMsgPickKey = None
	bMsgPickShown = False
	iMsgPickLines = 0

	def numPlotListButtons( self ):
		return NUM_PLOT_LIST_BUTTONS

	# Adds the Widget to a list for hiding and unhiding as the screen updates
	def appendtoHideState( self, screen, Name, Type, Level ):
		global MasterHideList
		screen.hide(Name)
		MasterHideList[Type][Level].append(Name)

	# Shows Widgets of the specified Type at and above a particular Hiding level
	def SetHideState( self, screen, Type, Level ):

		for T in range(NUM_HIDE_TYPES):
			if T != Type:
				for L in range(NUM_HIDE_LEVELS):
					List = (T * NUM_HIDE_LEVELS) +  L
					screen.hideList(List)

		for T in range(NUM_HIDE_TYPES):
			if T == Type:
				for L in range(NUM_HIDE_LEVELS):
					if (L > Level):
						List = (T * NUM_HIDE_LEVELS) +  L
						screen.hideList(List)
					else:
						List = (T * NUM_HIDE_LEVELS) +  L
						screen.showList(List)

	def SetHideLists( self, screen ):
		for T in range(NUM_HIDE_TYPES):
			for L in range(NUM_HIDE_TYPES):
				HideIndex = (T * NUM_HIDE_LEVELS) + L
				screen.registerHideList(MasterHideList[T][L], len(MasterHideList[T][L]), HideIndex)

		screen.registerHideList([], 0, NUM_HIDE_TYPES * NUM_HIDE_LEVELS)

	# Sets Global screen construct values based on our Resolution
	def SetGlobals ( self, screen ):

	# GET RESOLUTION
		global xResolution
		global yResolution

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

	# ADJUST FOR RESOLUTION
		global FLAG_WIDTH
		FLAG_WIDTH = int((FLAG_PERCENT_WIDTH * xResolution) / 100)

		global MINI_MAP_WIDTH
		MINI_MAP_WIDTH = int((MINI_MAP_PERCENT_WIDTH * xResolution) / 100)

		global SADDLE_HEIGHT
		SADDLE_HEIGHT = int((SADDLE_HEIGHT_PERCENT * yResolution) / 100)

		global MINIMAP_HEIGHT
		MINIMAP_HEIGHT = SADDLE_HEIGHT - 5

		global LOWER_RIGHT_CORNER_BACKGROUND_WIDTH
		LOWER_RIGHT_CORNER_BACKGROUND_WIDTH = int((LOWER_RIGHT_CORNER_BACKGROUND_WIDTH_PERCENT * xResolution) / 100)

		global LOWER_LEFT_CORNER_BACKGROUND_WIDTH
		LOWER_LEFT_CORNER_BACKGROUND_WIDTH = int((LOWER_LEFT_CORNER_BACKGROUND_PERCENT_WIDTH * xResolution) / 100)

		global LOWER_LEFT_CORNER_BACKGROUND_HEIGHT
		LOWER_LEFT_CORNER_BACKGROUND_HEIGHT = int((LOWER_LEFT_CORNER_BACKGROUND_PERCENT_HEIGHT * yResolution) / 100)

		global LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT
		LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT = int((LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT_PERCENT * yResolution) / 100)

		global BOTTOM_CENTER_HUD_HEIGHT
		BOTTOM_CENTER_HUD_HEIGHT = int((BOTTOM_CENTER_HUD_PERCENT_HEIGHT * yResolution) / 100)

		global TOP_CORNER_HUD_WIDTHS
		TOP_CORNER_HUD_WIDTHS = int((TOP_CORNER_HUD_PERCENT_WIDTH * xResolution) / 100)

		global TOP_CORNER_HUD_HEIGHT
		TOP_CORNER_HUD_HEIGHT = int((TOP_CORNER_HUD_PERCENT_HEIGHT * yResolution) / 100)

		global TOP_CENTER_HUD_HEIGHT
		TOP_CENTER_HUD_HEIGHT = int((TOP_CENTER_HUD_PERCENT_HEIGHT * yResolution) / 100)

		global TOP_CENTER_HUD_WIDTH
		TOP_CENTER_HUD_WIDTH = max(400, int((TOP_CENTER_HUD_PERCENT_WIDTH * xResolution) / 100))

		global CITY_TITLE_BAR_HEIGHT
		CITY_TITLE_BAR_HEIGHT = int((CITY_TITLE_BAR_PERCENT_HEIGHT * yResolution) / 100)

		global CITIZEN_BAR_HEIGHT
		CITIZEN_BAR_HEIGHT = int((CITIZEN_BAR_PERCENT_HEIGHT * yResolution) / 100)

		global STACK_BAR_HEIGHT
		STACK_BAR_HEIGHT = int((STACK_BAR_PERCENT_HEIGHT * yResolution) / 100)

		global EJECT_AREA_WIDTH
		EJECT_AREA_WIDTH = int((EJECT_AREA_PERCENT_WIDTH * xResolution) / 100)

		global MINI_MAP_RADIUS
		MINI_MAP_RADIUS = int((MINI_MAP_PERCENT_RADIUS * xResolution) / 100)

		global LEFT_PLOT_LIST_EDGE
		LEFT_PLOT_LIST_EDGE = int((LEFT_PLOT_LIST_PERCENT_EDGE * xResolution) / 100)

		global RIGHT_PLOT_LIST_EDGE
		RIGHT_PLOT_LIST_EDGE = int((RIGHT_PLOT_LIST_PERCENT_EDGE * xResolution) / 100)

		global MAIN_LARGE_PORTRAIT_HEIGHT
		MAIN_LARGE_PORTRAIT_HEIGHT = int((MAIN_LARGE_PORTRAIT_PERCENT_HEIGHT * yResolution) / 100)

		global MAIN_LARGE_PORTRAIT_WIDTH
		MAIN_LARGE_PORTRAIT_WIDTH = int((MAIL_LARGE_PORTRAIT_PERCENT_WIDTH * xResolution) / 100)

		global UNIT_PORTRAIT_HEIGHT
		UNIT_PORTRAIT_HEIGHT = int((UNIT_PORTRAIT_PERCENT_HEIGHT * yResolution) / 100)

		global UNIT_HEALTH_BAR_WIDTH
		UNIT_HEALTH_BAR_WIDTH = int((UNIT_HEALHT_BAR_PERCENT_WIDTH * xResolution) / 100)

		global SMALL_BUTTON_SIZE
		global MEDIUM_BUTTON_SIZE
		global LARGE_BUTTON_SIZE
		global STANDARD_FONT_SIZE

		if xResolution > 1600 and yResolution > 1024:
			SMALL_BUTTON_SIZE = 36
			MEDIUM_BUTTON_SIZE = 42
			LARGE_BUTTON_SIZE =	48
			STANDARD_FONT_SIZE = 4
		elif xResolution > 1280 and yResolution > 800:
			SMALL_BUTTON_SIZE = 32
			MEDIUM_BUTTON_SIZE = 36
			LARGE_BUTTON_SIZE = 40
			STANDARD_FONT_SIZE = 3
		else:
			SMALL_BUTTON_SIZE = 24
			MEDIUM_BUTTON_SIZE = 32
			LARGE_BUTTON_SIZE = 36
			STANDARD_FONT_SIZE = 3

		global ASPECT_RATIO
		ASPECT_RATIO = xResolution / yResolution

		global ASPECT_ADJUSTMENT
		ASPECT_ADJUSTMENT = ((float(xResolution) / float(yResolution)) * 3.0) / 4.0

		AspectAdjustment = 1 - ((1 - ASPECT_ADJUSTMENT) / 3)
		global CITY_VIEW_BOX_MODIFIED_PERCENT_HEIGHT_AND_WIDTH
		CITY_VIEW_BOX_MODIFIED_PERCENT_HEIGHT_AND_WIDTH = int(CITY_VIEW_BOX_PERCENT_HEIGHT * AspectAdjustment)

		global MAP_EDGE_MARGIN_WIDTH
		MAP_EDGE_MARGIN_WIDTH = int((MAP_EDGE_MARGIN_PERCENT_WIDTH * xResolution) / 100)

		global CITY_VIEW_BOX_HEIGHT_AND_WIDTH
		CITY_VIEW_BOX_HEIGHT_AND_WIDTH = int((CITY_VIEW_BOX_MODIFIED_PERCENT_HEIGHT_AND_WIDTH * yResolution) / 100)

		global CITIZEN_BAR_WIDTH
		CITIZEN_BAR_WIDTH = int((CITIZEN_BAR_WIDTH_PERCENT * (xResolution - CITY_VIEW_BOX_HEIGHT_AND_WIDTH)) / 100)

		global BUILD_AREA_WIDTH
		BUILD_AREA_WIDTH = int(((100 - CITIZEN_BAR_WIDTH_PERCENT) * (xResolution - CITY_VIEW_BOX_HEIGHT_AND_WIDTH )) / 100)

		global BUILD_AREA_HEIGHT
		BUILD_AREA_HEIGHT = CITY_VIEW_BOX_HEIGHT_AND_WIDTH - STACK_BAR_HEIGHT

		global BUILDING_AREA_WIDTH
		BUILDING_AREA_WIDTH = int(CITIZEN_BAR_WIDTH - (STACK_BAR_HEIGHT * 2))

		global BUILDING_AREA_HEIGHT
		BUILDING_AREA_HEIGHT = yResolution - BOTTOM_CENTER_HUD_HEIGHT - STACK_BAR_HEIGHT - CITY_TITLE_BAR_HEIGHT

		global TRANSPORT_AREA_HEIGHT
		TRANSPORT_AREA_HEIGHT = (yResolution - BOTTOM_CENTER_HUD_HEIGHT - CITY_TITLE_BAR_HEIGHT - CITY_VIEW_BOX_HEIGHT_AND_WIDTH) / 2

		global TRANSPORT_AREA_WIDTH
		TRANSPORT_AREA_WIDTH = (xResolution - CITIZEN_BAR_WIDTH) * 7 / 10

		global CITY_MULTI_TAB_AREA_HEIGHT
		CITY_MULTI_TAB_AREA_HEIGHT = ((yResolution - BOTTOM_CENTER_HUD_HEIGHT - CITY_TITLE_BAR_HEIGHT - CITY_VIEW_BOX_HEIGHT_AND_WIDTH) / 2) - (STACK_BAR_HEIGHT * 3 / 2)

		global CITY_MULTI_TAB_SIZE
		CITY_MULTI_TAB_SIZE = (TRANSPORT_AREA_HEIGHT - STACK_BAR_HEIGHT - MAP_EDGE_MARGIN_WIDTH) / 3

		global RIGHT_PANEL_WIDTH
		RIGHT_PANEL_WIDTH = LOWER_RIGHT_CORNER_BACKGROUND_WIDTH * 6 / 5

		global MINIMAP_WIDTH
		MINIMAP_WIDTH = MINIMAP_HEIGHT * 87 / 100

		global UPPER_SADDLE_HEIGHT
		UPPER_SADDLE_HEIGHT = SADDLE_HEIGHT * 29 / 56

		global LOWER_SADDLE_HEIGHT
		LOWER_SADDLE_HEIGHT = SADDLE_HEIGHT * 28 / 100

		global DOMESTIC_ADVISOR_HEIGHT
		DOMESTIC_ADVISOR_HEIGHT = yResolution * 69 / 100

		global DOMESTIC_ADVISOR_SPACE
		DOMESTIC_ADVISOR_SPACE = yResolution - DOMESTIC_ADVISOR_HEIGHT

		global BOTTOM_BUTTON_SIZE
		BOTTOM_BUTTON_SIZE = (BUILD_AREA_WIDTH - (STACK_BAR_HEIGHT * 3 / 2)) / 4

		global BUILDING_GRID
		BUILDING_GRID = []
		for iBUILDING_TYPE in range(len(BUILDING_DATA)):
			TypeArray = []
			for iData in range(len(BUILDING_DATA[iBUILDING_TYPE])):
				if  iData == 0 :
					Dimention = BUILDING_AREA_WIDTH
				elif iData == 1:
					Dimention = BUILDING_AREA_HEIGHT
				elif iData == 2:
					Dimention = BUILDING_AREA_HEIGHT
				else:
					Dimention = BUILDING_AREA_WIDTH

				TypeArray.append(int((BUILDING_DATA[iBUILDING_TYPE][iData] * Dimention) / 100))

			BUILDING_GRID.append(TypeArray)

		global AVOID_GROWTH
		for iEmphasize in range(gc.getNumEmphasizeInfos()):
			if gc.getEmphasizeInfo(iEmphasize).isAvoidGrowth():
				AVOID_GROWTH = iEmphasize
				break

	# EMPHASIZE YIELDS
		global EMPHASIZEYIELDS
		EMPHASIZEYIELDS = []
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			for iEmp in range(gc.getNumEmphasizeInfos()):
				if gc.getEmphasizeInfo(iEmp).getYieldChange(iYield) != 0:
					EMPHASIZEYIELDS.append(iYield)
					break

	# LAST CACHED UNITS COUNT
		global LAST_CACHED_GARRISON_UNITS_COUNT
		LAST_CACHED_GARRISON_UNITS_COUNT = 0

		global LAST_CACHED_TRANSPORT_UNITS_COUNT
		LAST_CACHED_TRANSPORT_UNITS_COUNT = 0

	# SET INITIALIZATION
		global INITIALIZED
		INITIALIZED = True

		global HELPTEXT_AREA_Y_MARGIN
		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_MORE_VARIABLES_HIDDEN):
			HELPTEXT_AREA_Y_MARGIN = 40
		elif yResolution<800:
			HELPTEXT_AREA_Y_MARGIN = 10
		else:
			HELPTEXT_AREA_Y_MARGIN = 0

	# Wraps <Font> tags around text
	def setFontSize( self, Text, relativeSize ):
		size = STANDARD_FONT_SIZE + relativeSize
		if relativeSize == -1:
			# WTP: the texts of our own panels and tooltips (only they use -1)
			size = self.getTipFontSize()
		if size > 4:
			size = 4
		return "<font=" + str(size) + ">" + Text + "</font>"

	# Will Initialize the majority of Background panels and Widgets
	def interfaceScreen ( self ):
		if (CyGame().isPitbossHost()):
			return

		self.iTipFontSize = None
		self.bTerritorialInfluenceMode = False
		self.m_pCurrentTerritorialInfluencePlot = None
		self.bTerritorialInfluenceLeftMouseDown = False
		self.bTerritorialInfluenceRightMouseDown = False
		self.bTerritorialInfluenceOldNoUnitCycling = False
		# WTP: message panel (the messages of the turn, click to expand)
		# (the interface is built again when the player comes back to the game with Alt+Tab: the state of the panel stays then,
		# it starts from scratch only in another turn, i.e. after loading another game)
		if getattr(self, "iMessageTurn", -1) != CyGame().getGameTurn() or not hasattr(self, "iMsgMoveX"):
			self.bMessagePanelExpanded = False
			self.bMessageAutoExpand = None # opens expanded at the start of a turn (saved with the game; None: not read yet)
			self.iMessageTurn = -1
			self.bMessageTurnPending = True
			self.iMsgMoveX = 0 # the message panel moved by the player (Shift + arrow keys)
			self.iMsgMoveY = 0
			self.iMsgX = 0
			self.iMsgY = 0
			self.aMsgHeld = [] # the arrow keys that are down
			self.iMsgHoldWait = 0
			self.iMsgCamKeep = 0 # frames the camera is kept where it was (the game turns it a little with Shift + arrow keys itself)
			self.fMsgCamTurn = 0.0
			self.fMsgCamPitch = 0.0
			self.bMessagePosRead = False # the position is read from the script data of the player
			self.bMessagePanelPrevious = False # shows the messages of the turn before
			self.iMessagePage = 0 # page of the expanded panel (0 = the newest messages)
		self.aMsgHeld = []
		self.tMessagePanelKey = None
		self.aszMessageLines = []
		self.atMessageTargets = []

		self.TableYields = []
		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			if gc.getYieldInfo(iYield).isCargo():
				self.TableYields.append(iYield)
	# GLOBAL NUM VARIABLES SET
		global g_NumEmphasizeInfos
		global g_NumHurryInfos
		global g_NumActionInfos

		g_NumEmphasizeInfos = gc.getNumEmphasizeInfos()
		g_NumHurryInfos = gc.getNumHurryInfos()
		g_NumActionInfos = gc.getNumActionInfos()

	# INIT MAIN INTERFACE SCREEN
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
		self.SetGlobals (screen)
		screen.setForcedRedraw(True)
		screen.setMainInterface(True)

	# CITY BURLAP BACKGROUND PANELS
		screen.addPanel("CityTopBackground", u"", u"", True, False, 0, 0, xResolution, CITY_TITLE_BAR_HEIGHT, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("CityTopBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_BG_TOP").getPath(), 0, 0, xResolution, CITY_TITLE_BAR_HEIGHT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "CityTopBackground", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)

		screen.addPanel("CityLeftBackground", u"", u"", True, False, 0, CITY_TITLE_BAR_HEIGHT, CITIZEN_BAR_WIDTH, yResolution, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("CityLeftBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_BG_LEFT").getPath(), 0, CITY_TITLE_BAR_HEIGHT, CITIZEN_BAR_WIDTH, yResolution, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "CityLeftBackground", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)

		screen.addPanel("CityLowBackground", u"", u"", True, False, CITIZEN_BAR_WIDTH, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2), xResolution - CITIZEN_BAR_WIDTH, yResolution - CITY_VIEW_BOX_HEIGHT_AND_WIDTH - CITY_TITLE_BAR_HEIGHT + MAP_EDGE_MARGIN_WIDTH, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("CityLowBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_BG_LOW").getPath(), CITIZEN_BAR_WIDTH, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2), xResolution - CITIZEN_BAR_WIDTH, yResolution - CITY_VIEW_BOX_HEIGHT_AND_WIDTH - CITY_TITLE_BAR_HEIGHT + (MAP_EDGE_MARGIN_WIDTH * 2), WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "CityLowBackground", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)

		screen.addPanel("CityRightBackground", u"", u"", True, False, CITIZEN_BAR_WIDTH + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2), CITY_TITLE_BAR_HEIGHT, BUILD_AREA_WIDTH + (MAP_EDGE_MARGIN_WIDTH * 2), CITY_VIEW_BOX_HEIGHT_AND_WIDTH, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("CityRightBackground", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_BG_RIGHT").getPath(), CITIZEN_BAR_WIDTH + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2), CITY_TITLE_BAR_HEIGHT, BUILD_AREA_WIDTH + (MAP_EDGE_MARGIN_WIDTH * 2) + 10, CITY_VIEW_BOX_HEIGHT_AND_WIDTH, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "CityRightBackground", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)

	# CITY FRAMING PANELS
		screen.addPanel("CityTitlePanel", u"", u"", True, False, 0, 0, xResolution, CITY_TITLE_BAR_HEIGHT, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("CityTitlePanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SCREEN_TITLE").getPath(), 0, 0, xResolution, int(CITY_TITLE_BAR_HEIGHT * 1.3), WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "CityTitlePanel", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)

	# RESOURCE TABLE BACKGROUND
		screen.addScrollPanel( "CityTransportBackGroundPanel", u"", xResolution * 511 / 512 - xResolution * 73 / 256 , yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT * 9 / 8 - 2, xResolution * 19 / 64, TRANSPORT_AREA_HEIGHT + (STACK_BAR_HEIGHT / 3) + SMALL_BUTTON_SIZE * 11 / 8, PanelStyles.PANEL_STYLE_MAIN, False, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		#screen.addDrawControl("CityTransportBackGroundPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_WIDE_BOX").getPath(),  xResolution * 511 / 512 - xResolution * 73 / 256 , yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT * 9 / 8 - 2, xResolution * 19 / 64, TRANSPORT_AREA_HEIGHT + (STACK_BAR_HEIGHT / 3) + SMALL_BUTTON_SIZE * 11 / 8, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "CityTransportBackGroundPanel", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)

		screen.addPanel("CityBuildFramePanel", u"", u"", True, False, CITIZEN_BAR_WIDTH + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - MAP_EDGE_MARGIN_WIDTH, CITY_TITLE_BAR_HEIGHT, BUILD_AREA_WIDTH, CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2), PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("CityBuildFramePanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUILD_BOX").getPath(), CITIZEN_BAR_WIDTH + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - MAP_EDGE_MARGIN_WIDTH, CITY_TITLE_BAR_HEIGHT, BUILD_AREA_WIDTH, CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2), WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "CityBuildFramePanel", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)

		screen.addPanel("CityMapFramePanel", u"", u"", True, False, CITIZEN_BAR_WIDTH, CITY_TITLE_BAR_HEIGHT, CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2), CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) , PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("CityMapFramePanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_MAP_FRAME").getPath(), CITIZEN_BAR_WIDTH, CITY_TITLE_BAR_HEIGHT, CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2), CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2), WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "CityMapFramePanel", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)

		screen.addPanel("CityMultiTabFramePanel", u"", u"", True, False, CITIZEN_BAR_WIDTH, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH, xResolution - CITIZEN_BAR_WIDTH - MAP_EDGE_MARGIN_WIDTH, TRANSPORT_AREA_HEIGHT - STACK_BAR_HEIGHT, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("CityMultiTabFramePanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_WIDE_BOX").getPath(), CITIZEN_BAR_WIDTH, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - MAP_EDGE_MARGIN_WIDTH , xResolution - CITIZEN_BAR_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 1), TRANSPORT_AREA_HEIGHT - STACK_BAR_HEIGHT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "CityMultiTabFramePanel", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)

		screen.addScrollPanel("CityGarrisonBackGroundPanel", u"", CITIZEN_BAR_WIDTH, yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT * 9 / 8 - 2, xResolution - CITIZEN_BAR_WIDTH - TRANSPORT_AREA_WIDTH + STACK_BAR_HEIGHT + 15, TRANSPORT_AREA_HEIGHT + (STACK_BAR_HEIGHT / 3) + SMALL_BUTTON_SIZE * 11 / 8, PanelStyles.PANEL_STYLE_STANDARD, False, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("CityGarrisonBackGroundPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_WIDE_BOX").getPath(), CITIZEN_BAR_WIDTH, yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT * 9 / 8 - 2, xResolution - CITIZEN_BAR_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 1), TRANSPORT_AREA_HEIGHT + (STACK_BAR_HEIGHT / 1) , WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "CityGarrisonBackGroundPanel", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)

		# WTP, ray, Center Plot specific Backgrounds - START
		scrollbackgroundgraphic = "INTERFACE_SCROLL_BG"
		screen.addPanel("CityManagerBackground", u"", u"", True, False, 0, CITY_TITLE_BAR_HEIGHT, int(CITIZEN_BAR_WIDTH * 1.07), int((yResolution - (BOTTOM_CENTER_HUD_HEIGHT + CITY_TITLE_BAR_HEIGHT)) * 1.07), PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("CityManagerBackground", ArtFileMgr.getInterfaceArtInfo(scrollbackgroundgraphic).getPath(), 0, CITY_TITLE_BAR_HEIGHT, int(CITIZEN_BAR_WIDTH * 1.07), int((yResolution - (BOTTOM_CENTER_HUD_HEIGHT + CITY_TITLE_BAR_HEIGHT)) * 1.04), WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "CityManagerBackground", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)
		# WTP, ray, Center Plot specific Backgrounds - END

	# MAP BACKGROUND SADDLE

		screen.addPanel("InterfaceMapViewSaddleLeft", u"", u"", True, False, 0, yResolution - UPPER_SADDLE_HEIGHT, xResolution - RIGHT_PANEL_WIDTH, SADDLE_HEIGHT * 4 / 7, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("InterfaceMapViewSaddleLeft", ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_MAP_SADDLE_LEFT").getPath(), 0, yResolution - UPPER_SADDLE_HEIGHT, xResolution, SADDLE_HEIGHT * 4 / 7, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "InterfaceMapViewSaddleLeft", HIDE_TYPE_MAP, HIDE_LEVEL_NORMAL)

		screen.addPanel("InterfaceMapViewSaddleRight", u"", u"", True, False, xResolution - RIGHT_PANEL_WIDTH, yResolution - UPPER_SADDLE_HEIGHT, RIGHT_PANEL_WIDTH, SADDLE_HEIGHT * 4 / 7, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("InterfaceMapViewSaddleRight", ArtFileMgr.getInterfaceArtInfo("SCREEN_BG_MAP_SADDLE_RIGHT").getPath(), xResolution - RIGHT_PANEL_WIDTH, yResolution - UPPER_SADDLE_HEIGHT, RIGHT_PANEL_WIDTH, SADDLE_HEIGHT * 4 / 7, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "InterfaceMapViewSaddleRight", HIDE_TYPE_MAP, HIDE_LEVEL_NORMAL)


	# MULITPANEL TABS
		iCumulativeY = (STACK_BAR_HEIGHT * 3 / 2) + (MAP_EDGE_MARGIN_WIDTH / 2)
		RelativeButtonSize = 130

		screen.setImageButton("MapHighlightButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath(), xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - CITY_MULTI_TAB_SIZE - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2), CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + iCumulativeY - (CITY_MULTI_TAB_SIZE / 2) - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2), CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100, CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setImageButton("MapToggle", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_MAP_BUTTON").getPath(), xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - CITY_MULTI_TAB_SIZE, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + iCumulativeY - (CITY_MULTI_TAB_SIZE / 2), CITY_MULTI_TAB_SIZE, CITY_MULTI_TAB_SIZE, WidgetTypes.WIDGET_GENERAL, MAP_MANAGMENT_TOGGLE, -1)
		self.appendtoHideState(screen, "MapToggle", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)
		self.appendtoHideState(screen, "MapHighlightButton", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)
		iCumulativeY += CITY_MULTI_TAB_SIZE

		screen.setImageButton("BuildHighlightButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath(), xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - CITY_MULTI_TAB_SIZE - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2), CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + iCumulativeY - (CITY_MULTI_TAB_SIZE / 2) - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2), CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100, CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setImageButton("BuildToggle", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_BUILD_BUTTON").getPath(), xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - CITY_MULTI_TAB_SIZE, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + iCumulativeY - (CITY_MULTI_TAB_SIZE / 2), CITY_MULTI_TAB_SIZE, CITY_MULTI_TAB_SIZE, WidgetTypes.WIDGET_GENERAL, BUILDING_MANAGMENT_TOGGLE, -1)
		self.appendtoHideState(screen, "BuildToggle", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)
		self.appendtoHideState(screen, "BuildHighlightButton", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)
		iCumulativeY += CITY_MULTI_TAB_SIZE

		screen.setImageButton("GovernorHighlightButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath(), xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - CITY_MULTI_TAB_SIZE - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2), CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + iCumulativeY - (CITY_MULTI_TAB_SIZE / 2) - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2), CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100, CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setImageButton("GovernorToggle", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_GOVENOR_BUTTON").getPath(), xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - CITY_MULTI_TAB_SIZE, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + iCumulativeY - (CITY_MULTI_TAB_SIZE / 2), CITY_MULTI_TAB_SIZE, CITY_MULTI_TAB_SIZE, WidgetTypes.WIDGET_GENERAL, AUTOMATION_MANAGMENT_TOGGLE, -1)
		self.appendtoHideState(screen, "GovernorToggle", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)
		self.appendtoHideState(screen, "GovernorHighlightButton", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)
		iCumulativeY += CITY_MULTI_TAB_SIZE

	# CITY BUILDING MULTILIST
		self.BOTTOM_BUTTON_ROWS = 3

		screen.addMultiListControlGFC("CityBuildingSelectionMultiList", u"", CITIZEN_BAR_WIDTH + CITY_VIEW_BOX_HEIGHT_AND_WIDTH + (STACK_BAR_HEIGHT / 2) - MAP_EDGE_MARGIN_WIDTH, CITY_TITLE_BAR_HEIGHT + (STACK_BAR_HEIGHT / 2), BUILD_AREA_WIDTH, BUILD_AREA_HEIGHT - STACK_BAR_HEIGHT, self.BOTTOM_BUTTON_ROWS, BOTTOM_BUTTON_SIZE, BOTTOM_BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD )
		self.appendtoHideState(screen, "CityBuildingSelectionMultiList", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

		screen.addDDSGFC("MapCityLeftPanelShadow", "Art/Interface/Game Hud/shadow_box_2.dds", 0, DOMESTIC_ADVISOR_HEIGHT, MINIMAP_WIDTH, DOMESTIC_ADVISOR_SPACE - LOWER_SADDLE_HEIGHT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.hide("MapCityLeftPanelShadow")
		screen.addDDSGFC("MapCityRightPanelShadow", "Art/Interface/Game Hud/shadow_box_2.dds", xResolution - MINIMAP_WIDTH, DOMESTIC_ADVISOR_HEIGHT, MINIMAP_WIDTH, DOMESTIC_ADVISOR_SPACE - LOWER_SADDLE_HEIGHT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.hide("MapCityRightPanelShadow")

	# CITY BUILDING MAP CONSTRUCTION BAR
		screen.addStackedBarGFC("MapCityProductionBar", xResolution - MINIMAP_WIDTH + 3, yResolution - LOWER_SADDLE_HEIGHT - STACK_BAR_HEIGHT * 3 / 2 - 6, MINIMAP_WIDTH - 6, STACK_BAR_HEIGHT * 3 / 2, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1 )
		screen.setStackedBarColors("MapCityProductionBar", InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_GREAT_PEOPLE_STORED)
		screen.setStackedBarColors("MapCityProductionBar", InfoBarTypes.INFOBAR_RATE, ColorTypes.COLOR_GREAT_PEOPLE_RATE)
		screen.setStackedBarColors("MapCityProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ColorTypes.COLOR_EMPTY)
		screen.setStackedBarColors("MapCityProductionBar", InfoBarTypes.INFOBAR_EMPTY, ColorTypes.COLOR_EMPTY)
		screen.hide("MapCityProductionBar")

	# EMPHASIZE TABLE
		screen.addTableControlGFC("EmphasizeTable", 1, CITIZEN_BAR_WIDTH + CITY_VIEW_BOX_HEIGHT_AND_WIDTH + (STACK_BAR_HEIGHT / 2) - MAP_EDGE_MARGIN_WIDTH, CITY_TITLE_BAR_HEIGHT + (STACK_BAR_HEIGHT / 2), BUILD_AREA_WIDTH, BUILD_AREA_HEIGHT - STACK_BAR_HEIGHT, False, False, MEDIUM_BUTTON_SIZE, MEDIUM_BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
		self.appendtoHideState(screen, "EmphasizeTable", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)
		screen.setStyle("EmphasizeTable", "Table_EmptyScroll_Style")
		screen.appendTableRow("EmphasizeTable")
		for iYield in EMPHASIZEYIELDS:
			screen.appendTableRow("EmphasizeTable")

	# HELP TEXT AREA
		self.setGameHelpArea(screen, yResolution - SADDLE_HEIGHT)

	# ADVISOR BUTTONS

		SpaceAvailable = (xResolution / 2)
		self.ADVISOR_BUTTON_SPACING = SpaceAvailable / 15
		self.ADVISOR_BUTTON_SIZE = SMALL_BUTTON_SIZE * 2
		iBtnX = xResolution / 6 - self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("MainMenuButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_MENU_ICON").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_MENU_ICON, -1, -1 )
		screen.setImageShape("MainMenuButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("MainMenuButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "MainMenuButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("InterfaceHelpButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_CIVILOPEDIA_ICON").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CIVILOPEDIA).getActionInfoIndex(), -1 )
		screen.setImageShape("InterfaceHelpButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("InterfaceHelpButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "InterfaceHelpButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING * 2

		screen.setImageButton("AchieveAdvisorButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_ACHIEVE_BUTTON").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, ACHIEVE_ADVISOR_SCREEN_MI, -1 )
		screen.setImageShape("AchieveAdvisorButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("AchieveAdvisorButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "AchieveAdvisorButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("TurnLogButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_TURNLOG_ICON").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_TURN_LOG).getActionInfoIndex(), -1 )
		screen.setImageShape("TurnLogButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("TurnLogButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "TurnLogButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("CongressAdvisorButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CONTINENTAL_CONGRESS").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_CONGRESS_SCREEN).getActionInfoIndex(), -1 )
		screen.setImageShape("CongressAdvisorButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("CongressAdvisorButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "CongressAdvisorButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("InfoAdvisorButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_INFO").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_INFO).getActionInfoIndex(), -1 )
		screen.setImageShape("InfoAdvisorButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("InfoAdvisorButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "InfoAdvisorButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton( "SettingsAdvisorButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_VICTORY_ADVISOR").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_VICTORY_SCREEN).getActionInfoIndex(), -1 )
		screen.setImageShape("SettingsAdvisorButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("SettingsAdvisorButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "SettingsAdvisorButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING * 2

		screen.setImageButton("EuropeScreenButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_EUROPE_SCREEN).getActionInfoIndex(), -1 )
		screen.setImageShape("EuropeScreenButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("EuropeScreenButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "EuropeScreenButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		self.addTopPortRing(screen, "WtpTopPortRingEurope", iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("AfricaScreenButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_AFRICA").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_AFRICA_SCREEN).getActionInfoIndex(), -1 )
		screen.setImageShape("AfricaScreenButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("AfricaScreenButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "AfricaScreenButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		self.addTopPortRing(screen, "WtpTopPortRingAfrica", iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("PortRoyalScreenButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_PORT_ROYAL").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_PORT_ROYAL_SCREEN).getActionInfoIndex(), -1 )
		screen.setImageShape("PortRoyalScreenButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("PortRoyalScreenButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "PortRoyalScreenButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		self.addTopPortRing(screen, "WtpTopPortRingPortRoyal", iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("DiplomacyButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_DIPLOMACY").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_DIPLOMACY).getActionInfoIndex(), -1 )
		screen.setImageShape("DiplomacyButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("DiplomacyButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "DiplomacyButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("TerritorialInfluenceButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_GENERAL_TERRITORIAL_INFLUENCE").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, self.BUTTON_TERRITORIAL_INFLUENCE, -1 )
		screen.setImageShape("TerritorialInfluenceButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("TerritorialInfluenceButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "TerritorialInfluenceButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("DomesticAdvisorButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_DOMESTIC_ADVISOR").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_DOMESTIC_SCREEN).getActionInfoIndex(), -1 )
		screen.setImageShape("DomesticAdvisorButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("DomesticAdvisorButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "DomesticAdvisorButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("RevolutionAdvisorButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_REVOLUTION_ADVISOR").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_REVOLUTION_SCREEN).getActionInfoIndex(), -1 )
		screen.setImageShape("RevolutionAdvisorButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("RevolutionAdvisorButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "RevolutionAdvisorButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("ForeignAdvisorButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_FOREIGN_ADVISOR").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FOREIGN_SCREEN).getActionInfoIndex(), -1 )
		screen.setImageShape("ForeignAdvisorButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("ForeignAdvisorButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "ForeignAdvisorButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		screen.setImageButton("MilitaryAdvisorButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_MILITARY_ADVISOR").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_MILITARY_SCREEN).getActionInfoIndex(), -1 )
		screen.setImageShape("MilitaryAdvisorButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("MilitaryAdvisorButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "MilitaryAdvisorButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

		# WTP: Trade Route Manager (anchored to the military advisor: the same distance as the other buttons; the symbol of the Domestic Advisor)
		screen.setImageButton("TradeRouteManagerButton", "Art/Interface/Game Hud/Actions/automate_city_high_res.dds", iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, self.BUTTON_TRADE_ROUTE_MANAGER, -1 )
		screen.setImageShape("TradeRouteManagerButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("TradeRouteManagerButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "TradeRouteManagerButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING * 2

		screen.setImageButton( "FatherAdvisorButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_FOUNDING_FATHER").getPath(), iBtnX, (TOP_CENTER_HUD_HEIGHT - self.ADVISOR_BUTTON_SIZE) / 2, self.ADVISOR_BUTTON_SIZE, self.ADVISOR_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(ControlTypes.CONTROL_FATHER_SCREEN).getActionInfoIndex(), -1 )
		screen.setImageShape("FatherAdvisorButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("FatherAdvisorButton", self.ADVISOR_BUTTON_SIZE / 6, self.ADVISOR_BUTTON_SIZE / 6)
		self.appendtoHideState(screen, "FatherAdvisorButton", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		iBtnX += self.ADVISOR_BUTTON_SPACING

	# MINIMAP RING
		self.MINIMAP_SIDE_MARGIN = MINIMAP_HEIGHT * 13 / 100

		screen.addPanel("MiniMapRing", u"", u"", True, False, 0, yResolution - SADDLE_HEIGHT + self.MINIMAP_SIDE_MARGIN, SADDLE_HEIGHT, SADDLE_HEIGHT, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("MiniMapRing", ArtFileMgr.getInterfaceArtInfo("SCREEN_MINI_MAP_RING").getPath(), 0, yResolution - SADDLE_HEIGHT + self.MINIMAP_SIDE_MARGIN, SADDLE_HEIGHT, SADDLE_HEIGHT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		self.appendtoHideState(screen, "MiniMapRing", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		self.appendtoHideState(screen, "MiniMapRing", HIDE_TYPE_GLOBAL, HIDE_LEVEL_HIDE)

	# MINIMAP INITIALIZATION
		screen.initMinimap(self.MINIMAP_SIDE_MARGIN, MINIMAP_HEIGHT - self.MINIMAP_SIDE_MARGIN, yResolution - MINIMAP_HEIGHT + self.MINIMAP_SIDE_MARGIN, yResolution - self.MINIMAP_SIDE_MARGIN, -0.1, True )
		self.appendtoHideState(screen, "_FXS_Screen_Bogus_Minimap_Name", HIDE_TYPE_MAP, HIDE_LEVEL_ALL)
		self.appendtoHideState(screen, "_FXS_Screen_Bogus_Minimap_Name", HIDE_TYPE_CITY, HIDE_LEVEL_ALL)
		self.appendtoHideState(screen, "_FXS_Screen_Bogus_Minimap_Name", HIDE_TYPE_GLOBAL, HIDE_LEVEL_ALL)

	# UNIT HEALTH BAR
		screen.addStackedBarGFC("UnitHealthBar", xResolution - UNIT_HEALTH_BAR_WIDTH - 10, yResolution - LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT - STACK_BAR_HEIGHT, UNIT_HEALTH_BAR_WIDTH, STACK_BAR_HEIGHT, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setStackedBarColors("UnitHealthBar", InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_CULTURE_STORED)
		screen.setStackedBarColors("UnitHealthBar", InfoBarTypes.INFOBAR_RATE, ColorTypes.COLOR_CULTURE_RATE)
		screen.setStackedBarColors("UnitHealthBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ColorTypes.COLOR_EMPTY)
		screen.setStackedBarColors("UnitHealthBar", InfoBarTypes.INFOBAR_EMPTY, ColorTypes.COLOR_EMPTY)
		screen.hide("UnitHealthBar")

	# MINIMAP BUTTONS
		self.MINIMAP_BUTTON_SPACING = MEDIUM_BUTTON_SIZE
		self.MINIMAP_BUTTON_LEFT_OFFSET = 49

		self.ANGLE_SEPERATION = 90 / 4
		iAngle = 0
		iRadius = SADDLE_HEIGHT * 0.43

		self.MINI_MAP_BUTTON_SIZE = SMALL_BUTTON_SIZE * 15 / 8

		self.ButtonList = ["INTERFACE_MAP_UNIT", "INTERFACE_MAP_GRID_TOGGLE", "INTERFACE_MAP_SHOW_WORLD", "INTERFACE_MAP_INFO", "INTERFACE_MAP_ZOOM", "INTERFACE_MAP_YIELD", "INTERFACE_MAP_LIST"]
		self.ControlList = [ControlTypes.CONTROL_UNIT_ICONS, ControlTypes.CONTROL_GRID, ControlTypes.CONTROL_BARE_MAP, ControlTypes.CONTROL_RESOURCE_ALL, ControlTypes.CONTROL_GLOBELAYER, ControlTypes.CONTROL_YIELDS, ControlTypes.CONTROL_SCORES]
		self.ButtonNames = ["UnitIcons", "Grid", "BareMap", "ResourceIcons", "GlobeToggle", "Yields", "ScoresVisible"]

		for iButtonIndex in range(len(self.ButtonList)):
			Xcord = -math.sin(math.radians(self.ANGLE_SEPERATION * iButtonIndex + 45)) * int(iRadius) + int(SADDLE_HEIGHT / 2)
			Ycord = math.cos(math.radians(self.ANGLE_SEPERATION * iButtonIndex + 45)) * int(iRadius) - int(SADDLE_HEIGHT / 2) + yResolution + 3 + self.MINIMAP_SIDE_MARGIN

			szName = self.ButtonNames[iButtonIndex]
			screen.setImageButton(szName, ArtFileMgr.getInterfaceArtInfo(self.ButtonList[iButtonIndex]).getPath(), int(Xcord) - (self.MINI_MAP_BUTTON_SIZE / 2), int(Ycord) - (self.MINI_MAP_BUTTON_SIZE / 2), self.MINI_MAP_BUTTON_SIZE, self.MINI_MAP_BUTTON_SIZE, WidgetTypes.WIDGET_ACTION, gc.getControlInfo(self.ControlList[iButtonIndex]).getActionInfoIndex(), -1)
			screen.setImageShape(szName, ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
			screen.setHitMargins(szName, 5, 5)
			self.appendtoHideState(screen, szName, HIDE_TYPE_GLOBAL, HIDE_LEVEL_ALL)
			self.appendtoHideState(screen, szName, HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)

	# GLOBAL VIEW BUTTONS
		for i in range (CyGlobeLayerManager().getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)
			szStyle = ArtFileMgr.getInterfaceArtInfo(CyGlobeLayerManager().getLayer(i).getButtonStyle()).getPath()

			Xcord = -math.sin(math.radians(self.ANGLE_SEPERATION * i + 45)) * int(iRadius) + int(SADDLE_HEIGHT / 2)
			Ycord = math.cos(math.radians(self.ANGLE_SEPERATION * i + 45)) * int(iRadius) - int(SADDLE_HEIGHT / 2) + yResolution + 3 + self.MINIMAP_SIDE_MARGIN

			screen.setImageButton( szButtonID, szStyle, int(Xcord) - (self.MINI_MAP_BUTTON_SIZE / 2), int(Ycord) - (self.MINI_MAP_BUTTON_SIZE / 2), self.MINI_MAP_BUTTON_SIZE, self.MINI_MAP_BUTTON_SIZE, WidgetTypes.WIDGET_GLOBELAYER, i, -1)
			screen.setImageShape(szButtonID, ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
			screen.setHitMargins(szButtonID, 5, 5)
			screen.hide( szButtonID )

	# GOLD PILE
		screen.addDDSGFC("GoldPile", ArtFileMgr.getInterfaceArtInfo("SCREEN_GOLD_PILE").getPath(), 60, 8, 50, 50, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setImageShape("GoldPile", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("GoldPile", 30, 30)
		self.appendtoHideState(screen, "GoldPile", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)

		# desync log writing button
		# TODO figure out how to make it appear as needed instead of always or never
		if (0):
			screen.setImageButton("DesyncButton", "pink", 100, 100, 100, 100, WidgetTypes.WIDGET_NETWORK_DESYNC, -1, -1)

	# AUTOMATE PRODUCTION & CITIZEN BUTTON
		screen.addCheckBoxGFC("AutomateProduction", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_AUTOMATE_PRODUCTION").getPath(), ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath(), CITIZEN_BAR_WIDTH + ((xResolution - CITIZEN_BAR_WIDTH) * 3 / 7) , yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT - (STACK_BAR_HEIGHT * 2) - (SMALL_BUTTON_SIZE * 3 / 2), SMALL_BUTTON_SIZE * 2, SMALL_BUTTON_SIZE * 2, WidgetTypes.WIDGET_AUTOMATE_PRODUCTION, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL )
		self.appendtoHideState(screen, "AutomateProduction", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

		screen.setImageButton("AutomateCitizens", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_AUTOMATE_CITIZENS").getPath(), CITIZEN_BAR_WIDTH - (SMALL_BUTTON_SIZE * 3), yResolution - BOTTOM_CENTER_HUD_HEIGHT - (STACK_BAR_HEIGHT * 2) - SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE * 2, SMALL_BUTTON_SIZE * 2, WidgetTypes.WIDGET_AUTOMATE_CITIZENS, 1, -1)
		self.appendtoHideState(screen, "AutomateCitizens", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

		screen.setImageButton("LockCitizens", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_CITIZEN_LOCK").getPath(), CITIZEN_BAR_WIDTH - (SMALL_BUTTON_SIZE * 5), yResolution - BOTTOM_CENTER_HUD_HEIGHT - (STACK_BAR_HEIGHT * 2) - SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE * 2, SMALL_BUTTON_SIZE * 2, WidgetTypes.WIDGET_AUTOMATE_CITIZENS, 0, -1)
		self.appendtoHideState(screen, "LockCitizens", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

		# WTP: the colony takes colonists of the job automation (Auto Assign Job); off by default
		screen.setImageButton("AutoAssignTarget", "Art/Interface/Game Hud/Actions/auto_assign_target_off.dds", CITIZEN_BAR_WIDTH - (SMALL_BUTTON_SIZE * 7), yResolution - BOTTOM_CENTER_HUD_HEIGHT - (STACK_BAR_HEIGHT * 2) - SMALL_BUTTON_SIZE, SMALL_BUTTON_SIZE * 2, SMALL_BUTTON_SIZE * 2, WidgetTypes.WIDGET_GENERAL, self.BUTTON_AUTO_ASSIGN_TARGET, -1)
		self.appendtoHideState(screen, "AutoAssignTarget", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

	# RESOURCE TABLE
		screen.addScrollPanel("ResourceTable", u"", 0, yResolution - BOTTOM_CENTER_HUD_HEIGHT, xResolution, BOTTOM_CENTER_HUD_HEIGHT, PanelStyles.PANEL_STYLE_STANDARD, False, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.hide("ResourceTable")

		self.RESOURCE_LABELS = ["", ""]
		self.RESOURCE_LABELS[0] = localText.getText("TXT_KEY_SCREEN_STORED", ())
		self.RESOURCE_LABELS[1] = localText.getText("TXT_KEY_SCREEN_NET", ())

		global RESOURCE_TABLE_COLUMN_WIDTH
		RESOURCE_TABLE_COLUMN_WIDTH = int((xResolution) / len(self.TableYields))
		global RESOURCE_TABLE_MARGIN
		RESOURCE_TABLE_MARGIN = int((xResolution - RESOURCE_TABLE_COLUMN_WIDTH * len(self.TableYields)) / 2)
		ArtPath = ""
		xDelta = 0
		ixDelta = 0
		iDelta = 0
		iK1 = 1
		iK2 = 1
		iK3 = 1
		iMax = (xResolution * 2) / (yResolution * 33)
		iNum = len(self.TableYields)
		iY = yResolution - BOTTOM_CENTER_HUD_HEIGHT / iK1
		if iNum > iMax:
			if iNum % 3 == 1:
				iNum += 2
			if iNum % 3 == 2:
				iNum += 1
			iNum /= 3
			RESOURCE_TABLE_COLUMN_WIDTH = (xResolution - STACK_BAR_HEIGHT) / iNum
			iK2 = 3
			iK3 = 7
			if len(self.TableYields) % 3 == 1:
				ixDelta = RESOURCE_TABLE_COLUMN_WIDTH / 2
		self.iIconWidth = RESOURCE_TABLE_COLUMN_WIDTH
		if iK2 == 3:
			iMax = yResolution / 20
			if RESOURCE_TABLE_COLUMN_WIDTH > iMax:
				self.iIconWidth = iMax
		for iYield in self.TableYields:
			szName = "BonusPane" + str(iYield)

			# WTP ray
			if iYield >= 2 * iNum:
				xDelta = ixDelta
				iDelta = iNum * 2
				iK1 = 3
				iY = yResolution - BOTTOM_CENTER_HUD_HEIGHT / 3

			elif iYield >= iNum:
				xDelta = ixDelta
				iDelta = iNum
				iK1 = 2
				iY = yResolution - (2 * BOTTOM_CENTER_HUD_HEIGHT / 3)
			#screen.attachPanelAt("ResourceTable", szName, u"", u"", True, True, PanelStyles.PANEL_STYLE_STANDARD, STACK_BAR_HEIGHT + (iYield * RESOURCE_TABLE_COLUMN_WIDTH), yResolution - BOTTOM_CENTER_HUD_HEIGHT, RESOURCE_TABLE_COLUMN_WIDTH, BOTTOM_CENTER_HUD_HEIGHT - STACK_BAR_HEIGHT, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )
			iX = STACK_BAR_HEIGHT + ((iYield - iDelta) * RESOURCE_TABLE_COLUMN_WIDTH) + xDelta
			# WTP, ray adjustment, 3 rows
			screen.attachPanelAt("ResourceTable", szName, u"", u"", True, True, PanelStyles.PANEL_STYLE_STANDARD, iX, iY, RESOURCE_TABLE_COLUMN_WIDTH, (BOTTOM_CENTER_HUD_HEIGHT - STACK_BAR_HEIGHT) / iK2, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )

			if (iYield - iDelta) == 0:
				ArtPath = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOX_START").getPath()
			elif (iYield - iDelta) == (len(self.TableYields) / 3 - 1): # WTP, ray, adjustments
				ArtPath = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOX_END").getPath()
			elif (iYield - iDelta) == ((len(self.TableYields) / 3) * 2 - 1): # WTP, ray, adjustments
				ArtPath = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOX_END").getPath()
			else:
				ArtPath = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOX_MID").getPath()
			iX = STACK_BAR_HEIGHT + ((iYield - iDelta) * RESOURCE_TABLE_COLUMN_WIDTH) + xDelta
			screen.addDrawControl(szName, ArtPath, iX, iY, RESOURCE_TABLE_COLUMN_WIDTH, (BOTTOM_CENTER_HUD_HEIGHT - (STACK_BAR_HEIGHT * 3 / 2)) * iK2 / iK3 + 2, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1)
			self.appendtoHideState(screen, szName, HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)

			szName = "BonusPanePos" + str(iYield)
			iX = STACK_BAR_HEIGHT + ((iYield - iDelta) * RESOURCE_TABLE_COLUMN_WIDTH) + xDelta
			screen.attachPanelAt("ResourceTable", szName, u"", u"", True, True, PanelStyles.PANEL_STYLE_STANDARD, iX, iY, RESOURCE_TABLE_COLUMN_WIDTH, (BOTTOM_CENTER_HUD_HEIGHT - STACK_BAR_HEIGHT) / iK2, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )

			if (iYield - iDelta) == 0:
				ArtPath = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOX_POS_START").getPath()
			elif (iYield - iDelta) == (len(self.TableYields) - 1):
				ArtPath = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOX_POS_END").getPath()
			else:
				ArtPath = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOX_POS_MID").getPath()

			iX = STACK_BAR_HEIGHT + ((iYield - iDelta) * RESOURCE_TABLE_COLUMN_WIDTH) + xDelta
			screen.addDrawControl(szName, ArtPath, iX, iY, RESOURCE_TABLE_COLUMN_WIDTH, (BOTTOM_CENTER_HUD_HEIGHT - (STACK_BAR_HEIGHT * 3 / 2)) * iK2 / iK3 + 2, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )
			self.appendtoHideState(screen, szName, HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)

			szName = "BonusPaneNeg" + str(iYield)
			iX = STACK_BAR_HEIGHT + ((iYield - iDelta) * RESOURCE_TABLE_COLUMN_WIDTH) + xDelta
			screen.attachPanelAt("ResourceTable", szName, u"", u"", True, True, PanelStyles.PANEL_STYLE_STANDARD, iX, iY, RESOURCE_TABLE_COLUMN_WIDTH, (BOTTOM_CENTER_HUD_HEIGHT - STACK_BAR_HEIGHT) / iK2, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )

			if (iYield - iDelta) == 0:
				ArtPath = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOX_NEG_START").getPath()
			elif (iYield - iDelta) == (len(self.TableYields) - 1):
				ArtPath = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOX_NEG_END").getPath()
			else:
				ArtPath = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BOX_NEG_MID").getPath()

			iX = STACK_BAR_HEIGHT + ((iYield - iDelta) * RESOURCE_TABLE_COLUMN_WIDTH) + xDelta
			screen.addDrawControl(szName, ArtPath, iX, iY, RESOURCE_TABLE_COLUMN_WIDTH, (BOTTOM_CENTER_HUD_HEIGHT - (STACK_BAR_HEIGHT * 3 / 2)) * iK2 / iK3 + 2, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )
			self.appendtoHideState(screen, szName, HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)
			iX = STACK_BAR_HEIGHT + ((iYield - iDelta) * RESOURCE_TABLE_COLUMN_WIDTH) + (RESOURCE_TABLE_COLUMN_WIDTH / 2) + xDelta

			iZ = yResolution - (STACK_BAR_HEIGHT * 3) / iK1
			screen.setLabel("YieldStoredlabel" + str(iYield), "ResourceTable", "", CvUtil.FONT_CENTER_JUSTIFY, iX, iZ, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )
			iZ = yResolution - (STACK_BAR_HEIGHT * 2) / iK1
			screen.setLabel("YieldNetlabel" + str(iYield), "ResourceTable", "", CvUtil.FONT_CENTER_JUSTIFY, iX, iZ, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )

			iX = STACK_BAR_HEIGHT + ((iYield - iDelta) * RESOURCE_TABLE_COLUMN_WIDTH) + (RESOURCE_TABLE_COLUMN_WIDTH - self.iIconWidth) / 2 + xDelta

			screen.addDragableButton("YieldIcon" + str(iYield), gc.getYieldInfo(iYield).getIcon(), "", iX, iY, self.iIconWidth, self.iIconWidth, WidgetTypes.WIDGET_MOVE_CARGO_TO_TRANSPORT, iYield, -1, ButtonStyles.BUTTON_STYLE_IMAGE )
			self.appendtoHideState(screen, "YieldIcon" + str(iYield), HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)

		screen.addScrollPanel("CityReciveCargo", u"", 0, yResolution - BOTTOM_CENTER_HUD_HEIGHT, xResolution, BOTTOM_CENTER_HUD_HEIGHT, PanelStyles.PANEL_STYLE_MAIN, False, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )
		self.appendtoHideState(screen, "CityReciveCargo", HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)

		for iYield in self.TableYields:
			screen.moveToFront("YieldIcon" + str(iYield))

	# MAP YIELD EMPHASIZE
		BOX_WIDTH = xResolution / len(EMPHASIZEYIELDS)
		BOX_HEIGHT = BOX_WIDTH
		xLocation = (xResolution - BOX_WIDTH * len(EMPHASIZEYIELDS)) / 2
		yLocation = yResolution - SADDLE_HEIGHT * 13 / 100 - BOX_HEIGHT / 2

		for iYield in EMPHASIZEYIELDS:
			screen.addDDSGFC("MapYieldBox" + str(iYield), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_PRICE").getPath(), xLocation, yLocation, BOX_WIDTH, BOX_HEIGHT, WidgetTypes.WIDGET_GENERAL, iYield, -1 )
			screen.hide("MapYieldBox" + str(iYield))
			screen.addDDSGFC("MapYieldEmphasize" + str(iYield), "Art/Interface/Game Hud/box_green.dds", xLocation, yLocation, BOX_WIDTH, BOX_HEIGHT, WidgetTypes.WIDGET_GENERAL, iYield, -1 )
			screen.hide("MapYieldEmphasize" + str(iYield))
			screen.addDDSGFC("MapYieldDe-Emphasize" + str(iYield), "Art/Interface/Game Hud/box_red.dds", xLocation, yLocation, BOX_WIDTH, BOX_HEIGHT, WidgetTypes.WIDGET_GENERAL, iYield, -1 )
			screen.hide("MapYieldDe-Emphasize" + str(iYield))
			screen.setImageButton("MapYieldIcon" + str(iYield), gc.getYieldInfo(iYield).getIcon(), xLocation + BOX_WIDTH / 14, yLocation + BOX_HEIGHT / 14, BOX_WIDTH * 6 / 7, BOX_WIDTH * 6 / 7, WidgetTypes.WIDGET_EMPHASIZE, iYield, -1)
			screen.hide("MapYieldIcon" + str(iYield))

			xLocation += BOX_WIDTH

	# YIELD LOZENGE
		screen.addDDSGFC("BonusPaneNeg" + str(int(YieldTypes.YIELD_BELLS)), ArtFileMgr.getInterfaceArtInfo("INTERFACE_DEEMPHASIZE_LOZENGE").getPath(), (xResolution * 30 / 100) - STACK_BAR_HEIGHT, STACK_BAR_HEIGHT / 3, STACK_BAR_HEIGHT * 2, STACK_BAR_HEIGHT , WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.appendtoHideState(screen, "BonusPaneNeg" + str(int(YieldTypes.YIELD_BELLS)), HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)
		screen.addDDSGFC("BonusPaneNeg" + str(int(YieldTypes.YIELD_CROSSES)), ArtFileMgr.getInterfaceArtInfo("INTERFACE_DEEMPHASIZE_LOZENGE").getPath(), (xResolution * 70 / 100) - STACK_BAR_HEIGHT, STACK_BAR_HEIGHT / 3, STACK_BAR_HEIGHT * 2, STACK_BAR_HEIGHT , WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.appendtoHideState(screen, "BonusPaneNeg" + str(int(YieldTypes.YIELD_CROSSES)), HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)
		screen.addDDSGFC("BonusPaneNeg" + str(int(YieldTypes.YIELD_HAMMERS)), ArtFileMgr.getInterfaceArtInfo("INTERFACE_DEEMPHASIZE_LOZENGE").getPath(), (xResolution * 25 / 100) - STACK_BAR_HEIGHT, STACK_BAR_HEIGHT / 3, STACK_BAR_HEIGHT * 2, STACK_BAR_HEIGHT , WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.appendtoHideState(screen, "BonusPaneNeg" + str(int(YieldTypes.YIELD_HAMMERS)), HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)
		screen.addDDSGFC("BonusPaneNeg" + str(int(YieldTypes.YIELD_EDUCATION)), ArtFileMgr.getInterfaceArtInfo("INTERFACE_DEEMPHASIZE_LOZENGE").getPath(), (xResolution * 75 / 100) - STACK_BAR_HEIGHT, STACK_BAR_HEIGHT / 3, STACK_BAR_HEIGHT * 2, STACK_BAR_HEIGHT , WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.appendtoHideState(screen, "BonusPaneNeg" + str(int(YieldTypes.YIELD_EDUCATION)), HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)

		screen.addDDSGFC("BonusPanePos" + str(int(YieldTypes.YIELD_BELLS)), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EMPHASIZE_LOZENGE").getPath(), (xResolution * 30 / 100) - STACK_BAR_HEIGHT, STACK_BAR_HEIGHT / 3, STACK_BAR_HEIGHT * 2, STACK_BAR_HEIGHT , WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.appendtoHideState(screen, "BonusPanePos" + str(int(YieldTypes.YIELD_BELLS)), HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)
		screen.addDDSGFC("BonusPanePos" + str(int(YieldTypes.YIELD_CROSSES)), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EMPHASIZE_LOZENGE").getPath(), (xResolution * 70 / 100) - STACK_BAR_HEIGHT, STACK_BAR_HEIGHT / 3, STACK_BAR_HEIGHT * 2, STACK_BAR_HEIGHT , WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.appendtoHideState(screen, "BonusPanePos" + str(int(YieldTypes.YIELD_CROSSES)), HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)
		screen.addDDSGFC("BonusPanePos" + str(int(YieldTypes.YIELD_HAMMERS)), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EMPHASIZE_LOZENGE").getPath(), (xResolution * 25 / 100) - STACK_BAR_HEIGHT, STACK_BAR_HEIGHT / 3, STACK_BAR_HEIGHT * 2, STACK_BAR_HEIGHT , WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.appendtoHideState(screen, "BonusPanePos" + str(int(YieldTypes.YIELD_HAMMERS)), HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)
		screen.addDDSGFC("BonusPanePos" + str(int(YieldTypes.YIELD_EDUCATION)), ArtFileMgr.getInterfaceArtInfo("INTERFACE_EMPHASIZE_LOZENGE").getPath(), (xResolution * 75 / 100) - STACK_BAR_HEIGHT, STACK_BAR_HEIGHT / 3, STACK_BAR_HEIGHT * 2, STACK_BAR_HEIGHT , WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.appendtoHideState(screen, "BonusPanePos" + str(int(YieldTypes.YIELD_EDUCATION)), HIDE_TYPE_CITY, HIDE_LEVEL_NORMAL)

	# MAP PLOT LIST BUTTONS
		self.END_TURN_TEXT_BOTTOM_MARGIN = 55
		self.PLOT_LIST_BUTTON_SPACER = 6
		self.PLOT_LIST_HEALTH_BAR_SHORTENING_CORRECTION = 6
		self.PLOT_LIST_HEALTH_BAR_HEIGHT = 11
		self.PLOT_LIST_ICON_SIZE = 12

		self.PLOT_LIST_BUTTON_AREA_MARGIN = 10
		Width = xResolution - (SADDLE_HEIGHT + RIGHT_PANEL_WIDTH)
		Height = LARGE_BUTTON_SIZE + self.PLOT_LIST_BUTTON_SPACER
		global NUM_PLOT_LIST_BUTTONS
		NUM_PLOT_LIST_BUTTONS = int(Width / Height)
		iMargin = (Width - NUM_PLOT_LIST_BUTTONS * Height) / 2

		for j in range(gc.getMAX_PLOT_LIST_ROWS()):
			iRow = gc.getMAX_PLOT_LIST_ROWS() - (j + 1)
			yPixel = yResolution - LOWER_SADDLE_HEIGHT - (LARGE_BUTTON_SIZE + 4) - iRow * (LARGE_BUTTON_SIZE + self.PLOT_LIST_BUTTON_SPACER)
			xPixel = SADDLE_HEIGHT + iMargin
			szStringPanel = "PlotListPanelMulti" + str(j)
			screen.addPanel(szStringPanel, u"", u"", True, False, xPixel, yPixel, Width, Height, PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.appendtoHideState(screen, "PlotListPanelMulti", HIDE_TYPE_MAP, HIDE_LEVEL_ALL)

			for i in range(self.numPlotListButtons()):
				k = j * self.numPlotListButtons() + i
				xOffset = i * (LARGE_BUTTON_SIZE + self.PLOT_LIST_BUTTON_SPACER)

				szString = "PlotListButtonMulti" + str(k)
				screen.addCheckBoxGFCAt(szStringPanel, szString, ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_GOVERNOR").getPath(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xOffset, 0, LARGE_BUTTON_SIZE, LARGE_BUTTON_SIZE, WidgetTypes.WIDGET_PLOT_LIST, k, -1, ButtonStyles.BUTTON_STYLE_LABEL )
				screen.hide( szString )

				szStringHealth = szString + "Health"
				screen.addStackedBarGFCAt( szStringHealth, szStringPanel, xOffset, LARGE_BUTTON_SIZE - self.PLOT_LIST_HEALTH_BAR_SHORTENING_CORRECTION, LARGE_BUTTON_SIZE, self.PLOT_LIST_HEALTH_BAR_HEIGHT, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_GENERAL, k, -1 )
				screen.hide( szStringHealth )

				szStringIcon = szString + "Icon"
				szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
				screen.addDDSGFCAt( szStringIcon, szStringPanel, szFileName, xOffset, 0, self.PLOT_LIST_ICON_SIZE, self.PLOT_LIST_ICON_SIZE, WidgetTypes.WIDGET_PLOT_LIST, k, -1, False )
				screen.hide( szStringIcon )

	# ENDTURN TEXT & BUTTON
		screen.setLabel("EndTurnText", "Background", u"", CvUtil.FONT_CENTER_JUSTIFY, 0, yResolution - LOWER_SADDLE_HEIGHT - 12, -0.1, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest("EndTurnText", HitTestTypes.HITTEST_NOHIT )

		self.CENTER_POINT_HEIGHT = 1.45
		self.CENTER_HUD_HEIGHT = 0.095

		iRadius = SADDLE_HEIGHT * 0.43
		Xcord = math.sin(math.radians(135)) * int(iRadius) + int(SADDLE_HEIGHT / 2)
		Ycord = math.cos(math.radians(135)) * int(iRadius) - int(SADDLE_HEIGHT / 2) + yResolution + self.MINIMAP_SIDE_MARGIN

		screen.addPanel("EndTurnRing", u"", u"", True, False, int(Xcord) - LARGE_BUTTON_SIZE * 3 / 4, int(Ycord) - LARGE_BUTTON_SIZE * 3 / 4, LARGE_BUTTON_SIZE * 3 / 2, LARGE_BUTTON_SIZE * 3 / 2, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addDrawControl("EndTurnRing", ArtFileMgr.getInterfaceArtInfo("SCREEN_END_TURN_RING").getPath(), int(Xcord) - LARGE_BUTTON_SIZE, int(Ycord) - LARGE_BUTTON_SIZE, LARGE_BUTTON_SIZE * 2, LARGE_BUTTON_SIZE * 2, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest("EndTurnRing", HitTestTypes.HITTEST_NOHIT)
		self.appendtoHideState(screen, "EndTurnRing", HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)
		self.appendtoHideState(screen, "EndTurnRing", HIDE_TYPE_GLOBAL, HIDE_LEVEL_HIDE)

		screen.setImageButton("EndTurnButton", "", int(Xcord) - LARGE_BUTTON_SIZE, int(Ycord) - LARGE_BUTTON_SIZE, LARGE_BUTTON_SIZE * 2, LARGE_BUTTON_SIZE * 2, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.setHitTest("EndTurnButton", HitTestTypes.HITTEST_NOHIT)
		screen.setStyle("EndTurnButton", "Button_HUDEndTurn_Style")
		screen.setEndTurnState("EndTurnButton", "Red")
		screen.hide("EndTurnButton")

		screen.setImageButton("EndTurnLayer", "", int(Xcord) - LARGE_BUTTON_SIZE, int(Ycord) - LARGE_BUTTON_SIZE, LARGE_BUTTON_SIZE * 2, LARGE_BUTTON_SIZE * 2, WidgetTypes.WIDGET_END_TURN, -1, -1 )
		screen.setImageShape("EndTurnLayer", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
		screen.setHitMargins("EndTurnLayer", LARGE_BUTTON_SIZE / 3, LARGE_BUTTON_SIZE / 3)
		screen.hide("EndTurnLayer")


	# BUILDING CONSTRUCTION BAR
		screen.addStackedBarGFC("CityProductionBar", CITIZEN_BAR_WIDTH - 2 + CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100 - SMALL_BUTTON_SIZE / 4, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + (STACK_BAR_HEIGHT * 3 / 2) + (MAP_EDGE_MARGIN_WIDTH / 2) - (CITY_MULTI_TAB_SIZE / 2) - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2) - (STACK_BAR_HEIGHT / 2) + CITY_MULTI_TAB_SIZE * RelativeButtonSize / 200, xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - CITY_MULTI_TAB_SIZE - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2) - CITIZEN_BAR_WIDTH - CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100 + SMALL_BUTTON_SIZE / 2 + 4, STACK_BAR_HEIGHT, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1 )
		screen.setStackedBarColors("CityProductionBar", InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_GREAT_PEOPLE_STORED)
		screen.setStackedBarColors("CityProductionBar", InfoBarTypes.INFOBAR_RATE, ColorTypes.COLOR_GREAT_PEOPLE_RATE)
		screen.setStackedBarColors("CityProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ColorTypes.COLOR_EMPTY)
		screen.setStackedBarColors("CityProductionBar", InfoBarTypes.INFOBAR_EMPTY, ColorTypes.COLOR_EMPTY)
		self.appendtoHideState(screen, "CityProductionBar", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

		screen.addPanel("CityProductionBarFrame", u"", u"", True, False, CITIZEN_BAR_WIDTH - 2 + CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100 - SMALL_BUTTON_SIZE / 4, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + (STACK_BAR_HEIGHT * 3 / 2) + (MAP_EDGE_MARGIN_WIDTH / 2) - (CITY_MULTI_TAB_SIZE / 2) - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2) - (STACK_BAR_HEIGHT / 2) + CITY_MULTI_TAB_SIZE * RelativeButtonSize / 200, xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - CITY_MULTI_TAB_SIZE - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2) - CITIZEN_BAR_WIDTH - CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100 + SMALL_BUTTON_SIZE / 2 + 4, STACK_BAR_HEIGHT, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1 )
		screen.addDrawControl("CityProductionBarFrame", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUILD_PROGRESS_BAR").getPath(), CITIZEN_BAR_WIDTH - 2 + CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100 - SMALL_BUTTON_SIZE / 4, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + (STACK_BAR_HEIGHT * 3 / 2) + (MAP_EDGE_MARGIN_WIDTH / 2) - (CITY_MULTI_TAB_SIZE / 2) - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2) - (STACK_BAR_HEIGHT / 2) + CITY_MULTI_TAB_SIZE * RelativeButtonSize / 200, xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - CITY_MULTI_TAB_SIZE - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2) - CITIZEN_BAR_WIDTH - CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100 + SMALL_BUTTON_SIZE / 2 + 4, STACK_BAR_HEIGHT, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1 )
		self.appendtoHideState(screen, "CityProductionBarFrame", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)
		screen.setLabelAt("ProductionText", "CityProductionBar", "", CvUtil.FONT_CENTER_JUSTIFY, (xResolution - CITIZEN_BAR_WIDTH - BUILD_AREA_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2)) / 2, 0, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1 )

	# CITY REBEL BAR
		screen.addStackedBarGFC("RebelBar", STACK_BAR_HEIGHT, yResolution - BOTTOM_CENTER_HUD_HEIGHT - STACK_BAR_HEIGHT, CITIZEN_BAR_WIDTH - (STACK_BAR_HEIGHT * 2), STACK_BAR_HEIGHT, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_HELP_REBEL, 1, -1 )
		screen.setStackedBarColors("RebelBar", InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_BLUE)
		screen.setStackedBarColors("RebelBar", InfoBarTypes.INFOBAR_RATE, ColorTypes.COLOR_BLUE)
		screen.setStackedBarColors("RebelBar", InfoBarTypes.INFOBAR_RATE_EXTRA, ColorTypes.COLOR_EMPTY)
		screen.setStackedBarColors("RebelBar", InfoBarTypes.INFOBAR_EMPTY, ColorTypes.COLOR_EMPTY)
		self.appendtoHideState(screen, "RebelBar", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

		screen.addPanel("RebelBarFrame", u"", u"", True, False, STACK_BAR_HEIGHT, yResolution - BOTTOM_CENTER_HUD_HEIGHT - STACK_BAR_HEIGHT, CITIZEN_BAR_WIDTH - (STACK_BAR_HEIGHT * 2), STACK_BAR_HEIGHT, PanelStyles.PANEL_STYLE_STANDARD, WidgetTypes.WIDGET_HELP_REBEL, 1, -1 )
		screen.addDrawControl("RebelBarFrame", ArtFileMgr.getInterfaceArtInfo("INTERFACE_REBEL_PROGRESS_BAR").getPath(), STACK_BAR_HEIGHT, yResolution - BOTTOM_CENTER_HUD_HEIGHT - STACK_BAR_HEIGHT, CITIZEN_BAR_WIDTH - (STACK_BAR_HEIGHT * 2), STACK_BAR_HEIGHT, WidgetTypes.WIDGET_HELP_REBEL, 1, -1 )
		self.appendtoHideState(screen, "RebelBarFrame", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

		screen.setLabelAt("RebelText", "RebelBar", "", CvUtil.FONT_CENTER_JUSTIFY, (CITIZEN_BAR_WIDTH - (STACK_BAR_HEIGHT * 3 / 2)) / 2, 0, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

	# CITY BUILDING GRID
		#Androrc Multiple Professions per Building
		# pHeadSelectedCity = CyInterface().getHeadSelectedCity() --- This is can not be used un global and also is not used!
		for iSpecial in range(gc.getNumSpecialBuildingInfos()):
			iTargetBuilding = -1
			for iBuilding in range(gc.getNumBuildingInfos()):
				if gc.getCivilizationInfo(gc.getActivePlayer().getCivilizationType()).getCivilizationBuildings(gc.getBuildingInfo(iBuilding).getBuildingClassType()) == iBuilding:
					if(gc.getBuildingInfo(iBuilding).getSpecialBuildingType() == iSpecial):
						iTargetBuilding = iBuilding
						break

			screen.setImageButton("CityBuildingGraphic" + str(iSpecial), "", BUILDING_GRID[iSpecial][0] + STACK_BAR_HEIGHT, BUILDING_GRID[iSpecial][1] + CITY_TITLE_BAR_HEIGHT, BUILDING_GRID[iSpecial][3], BUILDING_GRID[iSpecial][3], WidgetTypes.WIDGET_ASSIGN_CITIZEN_TO_BUILDING, iSpecial, iTargetBuilding)
			screen.addDDSGFC("ProductionBox" + str(iSpecial), ArtFileMgr.getInterfaceArtInfo("INTERFACE_PRODUCTION_BOX").getPath(), BUILDING_GRID[iSpecial][0] + STACK_BAR_HEIGHT, BUILDING_GRID[iSpecial][1] + BUILDING_GRID[iSpecial][2], (BUILDING_GRID[iSpecial][3] + STACK_BAR_HEIGHT)*3/4, STACK_BAR_HEIGHT*3/4, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.hide("ProductionBox" + str(iSpecial))

	# BUTTONS
		screen.setImageButton("HurryGold", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_PURCHASE_UNIT").getPath(), CITIZEN_BAR_WIDTH - 2, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + (STACK_BAR_HEIGHT * 3 / 2) + (MAP_EDGE_MARGIN_WIDTH / 2) - (CITY_MULTI_TAB_SIZE / 2) - ((CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2), CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100, CITY_MULTI_TAB_SIZE * RelativeButtonSize / 100, WidgetTypes.WIDGET_HURRY, HurryTypes.HURRY_GOLD, -1)
		self.appendtoHideState(screen, "HurryGold", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

	# CITY AND PLOT SCROLL BUTTONS
		ScrollButtonSize = MEDIUM_BUTTON_SIZE
		# R&R, Robert Surcouf Screen Resolution/Ratio - Start
		#iXmodifier = xResolution * 5 / 100 - (xResolution - 1000)/200 					# More or less: 1024 -> 5% 1280 -> 4% / 1600 -> 2% / 1980 -> 0%
		#screen.setImageButton("CityScrollMinus",ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_LEFT_ARROW").getPath(), (xResolution * 35 / 100) - (ScrollButtonSize / 2), (STACK_BAR_HEIGHT / 2) - (ScrollButtonSize / 3), ScrollButtonSize, ScrollButtonSize, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1)
		screen.setImageButton("CityScrollMinus",ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_LEFT_ARROW").getPath(), (xResolution * 35 / 100) - (ScrollButtonSize / 2) +xResolution * 5 / 100 - (xResolution - 1000)/200 , (STACK_BAR_HEIGHT / 2) - (ScrollButtonSize / 3), ScrollButtonSize, ScrollButtonSize, WidgetTypes.WIDGET_CITY_SCROLL, -1, -1)
		self.appendtoHideState(screen, "CityScrollMinus", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)
		#screen.setImageButton("CityScrollPlus",ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_RIGHT_ARROW").getPath(), (xResolution * 65 / 100) - (ScrollButtonSize / 2), (STACK_BAR_HEIGHT / 2) - (ScrollButtonSize / 3), ScrollButtonSize, ScrollButtonSize, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1)
		screen.setImageButton("CityScrollPlus",ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_RIGHT_ARROW").getPath(), (xResolution * 65 / 100) - (ScrollButtonSize / 2)-xResolution * 5 / 100 - (xResolution - 1000)/200 , (STACK_BAR_HEIGHT / 2) - (ScrollButtonSize / 3), ScrollButtonSize, ScrollButtonSize, WidgetTypes.WIDGET_CITY_SCROLL, 1, -1)
		self.appendtoHideState(screen, "CityScrollPlus", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)
		# R&R, Robert Surcouf Screen Resolution/Ratio - End

		screen.setButtonGFC("PlotListDown", u"", "", xResolution - RIGHT_PANEL_WIDTH, yResolution - UPPER_SADDLE_HEIGHT - MEDIUM_BUTTON_SIZE * 3 / 2, MEDIUM_BUTTON_SIZE, MEDIUM_BUTTON_SIZE, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, -1, self.numPlotListButtons(), ButtonStyles.BUTTON_STYLE_ARROW_UP )
		screen.hide("PlotListDown")
		screen.setButtonGFC("PlotListUp", u"", "", xResolution - RIGHT_PANEL_WIDTH, yResolution - UPPER_SADDLE_HEIGHT - MEDIUM_BUTTON_SIZE / 2, MEDIUM_BUTTON_SIZE, MEDIUM_BUTTON_SIZE, WidgetTypes.WIDGET_PLOT_LIST_SHIFT, 1, self.numPlotListButtons(), ButtonStyles.BUTTON_STYLE_ARROW_DOWN )
		screen.hide("PlotListUp")

	# EXIT BUTTON
		screen.setText("CityExitText", "", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 10, CITY_TITLE_BAR_HEIGHT / 12, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )
		self.appendtoHideState(screen, "CityExitText", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

	#Erik Resource table toggle Yields
		screen.setImageButton("ShowOrHideYields", ArtFileMgr.getInterfaceArtInfo("INTERFACE_SHOW_OR_HIDE_YIELDS").getPath(), 0, yResolution * 82 / 100, ScrollButtonSize, ScrollButtonSize, WidgetTypes.WIDGET_HELP_SHOW_OR_HIDE_YIELDS, -1, -1)
		self.appendtoHideState(screen, "ShowOrHideYields", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

	# GROWTH EMPHASIZE/DEMPHASIZE
		screen.setImageButton("AvoidGrowth", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath(), 0, CITY_TITLE_BAR_HEIGHT / 10, ScrollButtonSize, ScrollButtonSize, WidgetTypes.WIDGET_EMPHASIZE, -1, AVOID_GROWTH)
		self.appendtoHideState(screen, "AvoidGrowth", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

	# Garrison and Transport Panel
		screen.addScrollPanel("CityGarrisonPanel", u"", CITIZEN_BAR_WIDTH + (SMALL_BUTTON_SIZE / 8), yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT * 9 / 8 - 2, xResolution - CITIZEN_BAR_WIDTH - TRANSPORT_AREA_WIDTH + STACK_BAR_HEIGHT * 4 / 8, TRANSPORT_AREA_HEIGHT - (STACK_BAR_HEIGHT / 3), PanelStyles.PANEL_STYLE_EMPTY, False, WidgetTypes.WIDGET_EJECT_CITIZEN, -1, -1 )
		self.appendtoHideState(screen, "CityGarrisonPanel", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

		screen.addScrollPanel("CityTransportPanel", u"", xResolution - TRANSPORT_AREA_WIDTH + MAP_EDGE_MARGIN_WIDTH - SMALL_BUTTON_SIZE / 2, yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT * 9 / 8 - 2, TRANSPORT_AREA_WIDTH * 126 / 128, TRANSPORT_AREA_HEIGHT - (STACK_BAR_HEIGHT / 3), PanelStyles.PANEL_STYLE_MAIN, False, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )
		self.appendtoHideState(screen, "CityTransportPanel", HIDE_TYPE_CITY, HIDE_LEVEL_HIDE)

	# SCORES TABLE
		screen.addPanel("ScoreBackground", u"", u"", True, False, 0, 0, 0, 0, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		for i in range(gc.getMAX_PLAYERS()):
			szName = "ScoreText" + str(i)
			screen.setText( szName, "Background", u"", CvUtil.FONT_RIGHT_JUSTIFY, 996, 622, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_CONTACT_CIV, i, -1 )
			screen.hide( szName )

		# This should be a forced redraw screen
		screen.setForcedRedraw(True)
		self.SetHideLists(screen)

		# This should show the screen immidiately and pass input to the game
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)

	# Will update the screen (every 250 MS)
	def updateScreen( self ):

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )

		messageControl = CyMessageControl()

		# Hide all interface widgets
		bShow = False
		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY ):
			if (gc.getGame().isPaused()):
				# Pause overrides other messages
				acOutput = localText.getText("SYSTEM_GAME_PAUSED", (gc.getPlayer(gc.getGame().getPausePlayer()).getNameKey(), ))
				screen.setEndTurnState("EndTurnText", acOutput )
				bShow = True
			elif (messageControl.GetFirstBadConnection() != -1):
				# Waiting on a bad connection to resolve
				if (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 1):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_WAITING_FOR_PLAYER", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					screen.setEndTurnState("EndTurnText", acOutput )
					bShow = True
				elif (messageControl.GetConnState(messageControl.GetFirstBadConnection()) == 2):
					if (gc.getGame().isMPOption(MultiplayerOptionTypes.MPOPTION_ANONYMOUS)):
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), 0))
					else:
						acOutput = localText.getText("SYSTEM_PLAYER_JOINING", (gc.getPlayer(messageControl.GetFirstBadConnection()).getNameKey(), (messageControl.GetFirstBadConnection() + 1)))
					screen.setEndTurnState("EndTurnText", acOutput )
					bShow = True
			else:
				# Flash select messages if no popups are present
				if ( CyInterface().shouldDisplayWaitingOthers() ):
					acOutput = localText.getText("SYSTEM_WAITING", ())
					screen.setEndTurnState("EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayEndTurn() ):
					acOutput = localText.getText("SYSTEM_END_TURN", ())
					screen.setEndTurnState("EndTurnText", acOutput )
					bShow = True
				elif ( CyInterface().shouldDisplayWaitingYou() ):
					acOutput = localText.getText("SYSTEM_WAITING_FOR_YOU", ())
					screen.setEndTurnState("EndTurnText", acOutput )
					bShow = True

		if ( bShow ):
			screen.showEndTurn("EndTurnText")
			if ( CyInterface().isCityScreenUp() ):
				screen.moveItem("EndTurnText", 0, yResolution - 194, -0.1 )
			else:
				screen.moveItem("EndTurnText", 0, yResolution - LOWER_SADDLE_HEIGHT - 24, -0.1 )
		else:
			screen.hideEndTurn("EndTurnText")

		self.updateEndTurnButton()
		self.updateMessagePanel()

		if (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
			if (CyInterface().isCityScreenUp()):
				screen.hide("ClockText")
			else:
				if (CyUserProfile().isClockOn()):
					screen.setLabel("ClockText", "Background", self.setFontSize(getClockText(), 0), CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 24, 42, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					screen.show("ClockText")
				else:
					screen.hide("ClockText")
		else:
			screen.hide("ClockText")

		return 0

	# Will redraw the interface
	def redraw( self ):

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if not INITIALIZED:
			self.SetGlobals(screen)

		# Check Dirty Bits, see what we need to redraw...
		if ( CyInterface().isDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT) ):
			# Miscellaneous buttons (civics screen, etc)
			self.updateMiscButtons()
			CyInterface().setDirty(InterfaceDirtyBits.MiscButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT) ):
			# Info Pane Dirty Bit
			# This must come before updatePlotListButtons so that the entity widget appears in front of the stats
			self.updateInfoPaneStrings()
			CyInterface().setDirty(InterfaceDirtyBits.InfoPane_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT) ):
			# Plot List Buttons Dirty
			self.updatePlotListButtons()
			CyInterface().setDirty(InterfaceDirtyBits.PlotListButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT) ):
			# Selection Buttons Dirty
			self.updateSelectionButtons()
			CyInterface().setDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GameData_DIRTY_BIT) ):
			# Game Data Strings Dirty
			self.updateGameDataStrings()
			CyInterface().setDirty(InterfaceDirtyBits.GameData_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Help_DIRTY_BIT) ):
			# Help Dirty bit
			self.updateHelpStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Help_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT) ):
			# Selection Data Dirty Bit
			self.updateCityScreen()
			#CyInterface().setDirty(InterfaceDirtyBits.Domestic_Advisor_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.ResourceTable_DIRTY_BIT) ):
			# Resource Table
			self.updateResourceTable()
			CyInterface().setDirty(InterfaceDirtyBits.ResourceTable_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT) ):
			# Citizen Buttons Dirty
			self.updateCitizenButtons()
			CyInterface().setDirty(InterfaceDirtyBits.CitizenButtons_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.Score_DIRTY_BIT) or CyInterface().checkFlashUpdate() ):
			# Scores!
			self.updateScoreStrings()
			CyInterface().setDirty(InterfaceDirtyBits.Score_DIRTY_BIT, False)
		if ( CyInterface().isDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT) ):
			# Globeview and Globelayer buttons
			CyInterface().setDirty(InterfaceDirtyBits.GlobeInfo_DIRTY_BIT, False)
			self.updateGlobeviewButtons()

		return 0

	# Will update the end Turn Button
	def updateEndTurnButton( self ):

		global g_eEndTurnButtonState
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if (CyInterface().shouldDisplayEndTurnButton() and CyInterface().getShowInterface() <= InterfaceVisibility.INTERFACE_HIDE and (not pHeadSelectedCity or CyEngine().isGlobeviewUp())):
			eState = CyInterface().getEndTurnState()
			bShow = False

			if (eState == EndTurnButtonStates.END_TURN_OVER_HIGHLIGHT):
				screen.setEndTurnState("EndTurnButton", u"Red")
				bShow = True
			elif (eState == EndTurnButtonStates.END_TURN_OVER_DARK):
				screen.setEndTurnState("EndTurnButton", u"Red")
				bShow = True
			elif (eState == EndTurnButtonStates.END_TURN_GO ):
				screen.setEndTurnState("EndTurnButton", u"Green")
				bShow = True

			if (bShow):
				screen.showEndTurn("EndTurnButton")
				screen.show("EndTurnLayer")
			else:
				screen.hideEndTurn("EndTurnButton")
				screen.hide("EndTurnLayer")

			if (g_eEndTurnButtonState == eState):
				return

			g_eEndTurnButtonState = eState

		else:
			screen.hideEndTurn("EndTurnButton")
			screen.hide("EndTurnLayer")

		return 0

	# Update the miscellaneous buttons
	def updateMiscButtons( self ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if (CyInterface().shouldDisplayFlag() and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
			screen.show("CivilizationFlag")
		else:
			screen.hide("CivilizationFlag")

		if (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
			iLevel = 3
		if (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE):
			iLevel = 2
		if (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL):
			iLevel = 1
		elif (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_ADVANCED_START):
			iLevel = 0
		elif (CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_MINIMAP_ONLY):
			iLevel = 1

		if (CyInterface().isCityScreenUp()):
			self.SetHideState(screen, HIDE_TYPE_CITY, iLevel)
		elif (CyEngine().isGlobeviewUp()):
			self.SetHideState(screen, HIDE_TYPE_GLOBAL, iLevel)
		else:
			self.SetHideState(screen, HIDE_TYPE_MAP, iLevel)
			self.updateTopPortRings(True)

		screen.updateMinimapVisibility()

		return 0

	# Update plot List Buttons
	def updatePlotListButtons( self ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		bHandled = False
		if (CyInterface().shouldDisplayUnitModel() and not CyEngine().isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and not pHeadSelectedCity):
			if (CyInterface().isCityScreenUp()):
				if ( not bHandled ):
					screen.hide("InterfaceUnitModel")
					bHandled = True

				screen.moveToFront("CityBuildQueue")
				screen.moveToFront("SelectedUnitText")
				screen.moveToFront("SelectedUnitName")

			elif (CyInterface().getHeadSelectedUnit()):
				screen.hide("InterfaceUnitModel")
				screen.moveToFront("SelectedUnitText")
				screen.moveToFront("SelectedUnitName")
				if (not pHeadSelectedCity):
					for iYield in EMPHASIZEYIELDS:
						screen.hide("MapYieldBox" + str(iYield))
						screen.hide("MapYieldIcon" + str(iYield))
						screen.hide("MapYieldEmphasize" + str(iYield))
						screen.hide("MapYieldDe-Emphasize" + str(iYield))

					screen.hide("MapBuildingSelectionMultiList")
					screen.hide("MapCityProductionBar")
					screen.hide("MapCityBuildQueue")
					screen.hide("MapCityLeftPanelShadow")
					screen.hide("MapCityRightPanelShadow")

			else:
				screen.hide("InterfaceUnitModel")
				if (not pHeadSelectedCity):
					for iYield in EMPHASIZEYIELDS:
						screen.hide("MapYieldBox" + str(iYield))
						screen.hide("MapYieldIcon" + str(iYield))
						screen.hide("MapYieldEmphasize" + str(iYield))
						screen.hide("MapYieldDe-Emphasize" + str(iYield))

					screen.hide("MapBuildingSelectionMultiList")
					screen.hide("MapCityProductionBar")
					screen.hide("MapCityBuildQueue")
					screen.hide("MapCityLeftPanelShadow")
					screen.hide("MapCityRightPanelShadow")

		else:
			screen.hide("InterfaceUnitModel")
			if (not pHeadSelectedCity):
				for iYield in EMPHASIZEYIELDS:
					screen.hide("MapYieldBox" + str(iYield))
					screen.hide("MapYieldIcon" + str(iYield))
					screen.hide("MapYieldEmphasize" + str(iYield))
					screen.hide("MapYieldDe-Emphasize" + str(iYield))

				screen.hide("MapBuildingSelectionMultiList")
				screen.hide("MapCityProductionBar")
				screen.hide("MapCityBuildQueue")
				screen.hide("MapCityLeftPanelShadow")
				screen.hide("MapCityRightPanelShadow")

		pPlot = CyInterface().getSelectionPlot()

		screen.hide("PlotListDown")
		screen.hide("PlotListUp")
		screen.hide("MapBuildingSelectionMultiList")
		screen.hide("MapCityProductionBar")
		screen.hide("MapCityBuildQueue")
		screen.hide("MapCityLeftPanelShadow")
		screen.hide("MapCityRightPanelShadow")

		for j in range(gc.getMAX_PLOT_LIST_ROWS()):
			for i in range(self.numPlotListButtons()):
				szString = "PlotListButtonMulti" + str(j * self.numPlotListButtons() + i)
				screen.hide( szString )
				screen.hide( szString + "Health")
				screen.hide( szString + "Icon")

		if ( pPlot and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and not CyEngine().isGlobeviewUp() and not CyInterface().isCityScreenUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):

			iVisibleUnits = CyInterface().getNumVisibleUnits()
			iCount = -(CyInterface().getPlotListColumn())
			bDownArrow = False
			bUpArrow = False

			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			if not CyInterface().isPlotListMultiRow():
				pPlayer.toggleMultiRowPlotList()

			iMaxRows = gc.getMAX_PLOT_LIST_ROWS()
			szPlotListButtonName = "PlotListButtonMulti"

			iCount += CyInterface().getPlotListOffset()
			iSkipped = 0

			CyInterface().cacheInterfacePlotUnits(pPlot)
			for i in range(CyInterface().getNumCachedInterfacePlotUnits()):
				pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
				if (pLoopUnit):
					if ((iCount == 0) and (CyInterface().getPlotListColumn() > 0)):
						bDownArrow = True
					elif ((iCount == (iMaxRows * self.numPlotListButtons() - 1)) and ((iVisibleUnits - iCount - CyInterface().getPlotListColumn() + iSkipped) > 1)):
						bUpArrow = True

					if ((iCount >= 0) and (iCount <  self.numPlotListButtons() * iMaxRows)):
						if ((pLoopUnit.getTeam() != gc.getGame().getActiveTeam()) or pLoopUnit.isWaiting()):
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()

						elif (pLoopUnit.canMove()):
							if (pLoopUnit.hasMoved()):
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
							else:
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
						else:
							szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()

						szString = szPlotListButtonName + str(iCount)
						screen.changeImageButton( szString, pLoopUnit.getButton() )
						if ( pLoopUnit.getOwner() == gc.getGame().getActivePlayer() ):
							screen.enable(szString, True)
						else:
							screen.enable(szString, False)

						screen.setState(szString, pLoopUnit.IsSelected())
						screen.show( szString )

						# place the health bar
						if (pLoopUnit.isFighting()):
							bShowHealth = False
						else:
							bShowHealth = pLoopUnit.canFight()

						if bShowHealth:
							szStringHealth = szString + "Health"
							screen.setBarPercentage( szStringHealth, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )
							if (pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_RED)
							elif (pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3)):
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_YELLOW)
							else:
								screen.setStackedBarColors(szStringHealth, InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_GREEN)
							screen.show( szStringHealth )

						# Adds the overlay first
						szStringIcon = szString + "Icon"
						screen.changeDDSGFC( szStringIcon, szFileName )
						screen.show( szStringIcon )

					iCount += 1

			if (iVisibleUnits > self.numPlotListButtons() * iMaxRows):
				screen.enable("PlotListDown", bDownArrow)
				screen.show("PlotListDown")
				screen.enable("PlotListUp", bUpArrow)
				screen.show("PlotListUp")

		if (not CyInterface().isCityScreenUp() and not CyEngine().isGlobeviewUp()):
			if (pHeadSelectedCity):
				screen.hide("InterfaceMapViewSaddleRight")
				screen.hide("MiniMapRing")

				screen.hide("_FXS_Screen_Bogus_Minimap_Name")
				screen.hide("EndTurnRing")
				screen.hide("EndTurnText")
				screen.show("MapCityLeftPanelShadow")
				screen.show("MapCityRightPanelShadow")

				for i in EMPHASIZEYIELDS:
					screen.show("MapYieldBox" + str(i))
					screen.show("MapYieldIcon" + str(i))
					screen.hide("MapYieldEmphasize" + str(i))
					screen.hide("MapYieldDe-Emphasize" + str(i))

					if pHeadSelectedCity.AI_getEmphasizeYieldCount(i) > 0:
						screen.show("MapYieldEmphasize" + str(i))
					elif pHeadSelectedCity.AI_getEmphasizeYieldCount(i) < 0:
						screen.show("MapYieldDe-Emphasize" + str(i))

				screen.addMultiListControlGFC("MapBuildingSelectionMultiList", u"", 0, DOMESTIC_ADVISOR_HEIGHT + 3, MINIMAP_WIDTH - 3, DOMESTIC_ADVISOR_SPACE - LOWER_SADDLE_HEIGHT - 6, self.BOTTOM_BUTTON_ROWS, BOTTOM_BUTTON_SIZE, BOTTOM_BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD )
				screen.clearMultiList("MapBuildingSelectionMultiList")

				iCount = 0
				iRow = 0
				bFound = False
				for i in range (gc.getNumUnitClassInfos()):
					eLoopUnit = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationUnits(i)
					if (eLoopUnit != UnitTypes.NO_UNIT):
						if (pHeadSelectedCity.canTrain(eLoopUnit, False, True)):
							szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(eLoopUnit)
							screen.appendMultiListButton("MapBuildingSelectionMultiList", szButton, iRow, WidgetTypes.WIDGET_TRAIN, i, -1, False)
							if ( not pHeadSelectedCity.canTrain(eLoopUnit, False, False) ):
								screen.disableMultiListButton("MapBuildingSelectionMultiList", iRow, iCount, szButton)
							elif pHeadSelectedCity.getUnitProduction(eLoopUnit) > 0:
								bUnitTypeInQueue = False
								for i in range(CyInterface().getNumOrdersQueued()):
									if (CyInterface().getOrderNodeType(i)  == OrderTypes.ORDER_TRAIN):
										if CyInterface().getOrderNodeData1(i) == eLoopUnit:
											bUnitTypeInQueue = True
											break
								if not bUnitTypeInQueue:
									screen.enableMultiListPulse("MapBuildingSelectionMultiList", True, iRow, iCount)

							iCount += 1
							bFound = True

				iCount = 0
				iRow += 1
				bFound = False
				for i in range (gc.getNumBuildingClassInfos()):
					eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)
					if (eLoopBuilding != BuildingTypes.NO_BUILDING):
						if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
							screen.appendMultiListButton("MapBuildingSelectionMultiList", gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
							if (not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False)):
								screen.disableMultiListButton("MapBuildingSelectionMultiList", iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton())
							elif pHeadSelectedCity.getBuildingProduction(eLoopBuilding) > 0:
								screen.enableMultiListPulse("MapBuildingSelectionMultiList", True, iRow, iCount)

							iCount += 1
							bFound = True

				iCount = 0
				iRow += 1
				bFound = False
				for i in range (gc.getNumFatherPointInfos()):
					if (pHeadSelectedCity.canConvince(i, False, True)):
						screen.appendMultiListButton("MapBuildingSelectionMultiList", gc.getFatherPointInfo(i).getButton(), iRow, WidgetTypes.WIDGET_CONVINCE, i, -1, False )
						if (not pHeadSelectedCity.canConvince(i, False, False)):
							screen.disableMultiListButton("MapBuildingSelectionMultiList", iRow, iCount, gc.getFatherPointInfo(i).getButton())
						iCount += 1
						bFound = True

				screen.show("MapBuildingSelectionMultiList")

			# MAP BUILD QUEUE
				QueueWidth = LOWER_RIGHT_CORNER_BACKGROUND_WIDTH
				screen.addTableControlGFC("MapCityBuildQueue", 2, xResolution - MINIMAP_WIDTH + 3, DOMESTIC_ADVISOR_HEIGHT + STACK_BAR_HEIGHT + 9, MINIMAP_WIDTH, DOMESTIC_ADVISOR_SPACE - LOWER_SADDLE_HEIGHT - STACK_BAR_HEIGHT * 5 / 2 - 18, False, False, self.SELECTION_PANEL_ROW_HEIGHT, self.SELECTION_PANEL_ROW_HEIGHT, TableStyles.TABLE_STYLE_STANDARD)
				screen.setStyle("MapCityBuildQueue", "Table_EmptyScroll_Style")
				screen.hide("MapCityBuildQueue")
				screen.setTableColumnHeader("MapCityBuildQueue", 0, u"", MINIMAP_WIDTH - (QueueWidth * 3 / 10))
				screen.setTableColumnHeader("MapCityBuildQueue", 1, u"", QueueWidth * 3 / 10)

				iOrders = CyInterface().getNumOrdersQueued()
				iRow = 0

				for i in range(iOrders):
					szLeftBuffer = u""
					szRightBuffer = u""

					if ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_TRAIN ):
						szLeftBuffer = gc.getUnitInfo(CyInterface().getOrderNodeData1(i)).getDescription()
						szRightBuffer = str(pHeadSelectedCity.getUnitProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i))

						if (CyInterface().getOrderNodeSave(i)):
							szLeftBuffer = u"*" + szLeftBuffer

					elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CONSTRUCT ):
						szLeftBuffer = gc.getBuildingInfo(CyInterface().getOrderNodeData1(i)).getDescription()
						szRightBuffer = str(pHeadSelectedCity.getBuildingProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i))

					elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CONVINCE ):
						szLeftBuffer = gc.getFatherPointInfo(CyInterface().getOrderNodeData1(i)).getDescription()

					if i == 0:
						szLeftBuffer = u"<color=255,223,0>" + szLeftBuffer + u"</color>"
						szRightBuffer = u"<color=255,223,0>" + szRightBuffer + u"</color>"

					screen.appendTableRow("MapCityBuildQueue")
					screen.setTableText("MapCityBuildQueue", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
					screen.setTableText("MapCityBuildQueue", 1, iRow, szRightBuffer + "  ", "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )

					iRow += 1
				screen.show("MapCityBuildQueue")


			# CURRENT PRODUCTION BAR FILL
				fProductionNeeded = float(pHeadSelectedCity.getProductionNeeded(YieldTypes.YIELD_HAMMERS))
				iProductionDiffNoFood = pHeadSelectedCity.getCurrentProductionDifference(True)
				iProductionDiffJustFood = 0
				if (fProductionNeeded > 0):
					iFirst = ((float(pHeadSelectedCity.getProduction())) / fProductionNeeded)
					screen.setBarPercentage("MapCityProductionBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						iSecond = (((float(iProductionDiffNoFood)) / fProductionNeeded) )
					else:
						iSecond = (((float(iProductionDiffNoFood)) / fProductionNeeded) ) / ( 1 - iFirst )
					screen.setBarPercentage("MapCityProductionBar", InfoBarTypes.INFOBAR_RATE, iSecond )
					if ( iFirst + iSecond == 1 ):
						screen.setBarPercentage("MapCityProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, (((float(iProductionDiffJustFood)) / fProductionNeeded) ) )
					else:
						screen.setBarPercentage("MapCityProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, (( ((float(iProductionDiffJustFood)) / fProductionNeeded) ) ) / ( 1 - ( iFirst + iSecond ) ) )

			# CURRENT PRODUCTION BAR TEXT
				if (pHeadSelectedCity.isProductionBuilding() or pHeadSelectedCity.isProductionUnit()):
					szBuffer = u"%s" % pHeadSelectedCity.getProductionName()
				elif pHeadSelectedCity.isProduction():
					szBuffer = pHeadSelectedCity.getProductionName()
				else:
					szBuffer = u""

				RedText = False
				for iYield in range(YieldTypes.NUM_YIELD_TYPES):
					if iYield != YieldTypes.YIELD_HAMMERS:
						if (CyInterface().getOrderNodeType(0) == OrderTypes.ORDER_TRAIN ):
							YieldRequired = gc.getUnitInfo(CyInterface().getOrderNodeData1(0)).getYieldCost(iYield)
						elif (CyInterface().getOrderNodeType(0) == OrderTypes.ORDER_CONSTRUCT):
							YieldRequired = gc.getBuildingInfo(CyInterface().getOrderNodeData1(0)).getYieldCost(iYield)
						else:
							YieldRequired = 0

						if (YieldRequired > 0):
							if (YieldRequired >  pHeadSelectedCity.getYieldStored(iYield) + pHeadSelectedCity.getYieldRushed(iYield)):
								RedText = True
								break
				if (RedText):
					screen.setStackedBarColors("MapCityProductionBar", InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_RED)
					screen.setStackedBarColors("MapCityProductionBar", InfoBarTypes.INFOBAR_RATE, ColorTypes.COLOR_WARNING_RATE)
				else:
					screen.setStackedBarColors("MapCityProductionBar", InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_GREAT_PEOPLE_STORED)
					screen.setStackedBarColors("MapCityProductionBar", InfoBarTypes.INFOBAR_RATE, ColorTypes.COLOR_GREAT_PEOPLE_RATE)

				screen.setLabelAt("ProductionText", "MapCityProductionBar", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, UNIT_HEALTH_BAR_WIDTH / 2, STACK_BAR_HEIGHT * 3 / 4, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1 )
				screen.show("MapCityProductionBar")

			self.updateScoreStrings()


		return 0

	# Will hide and show the selection buttons and their associated buttons
	# WTP: the yellow ring around the buttons of Europe, Africa and Port Royal in the top bar when an own ship lies in that port (the same ring as around
	# the sail buttons of a transport). The rings are made with the buttons (hidden with them); this shows the ones of the ports with a ship.
	def addTopPortRing(self, screen, szName, iX, iY):
		iSize = self.ADVISOR_BUTTON_SIZE * 4 / 5
		iPad = (self.ADVISOR_BUTTON_SIZE - iSize) / 2
		screen.addDDSGFC(szName, "Art/Interface/Game Hud/Actions/port_ring.dds", iX + iPad, iY + iPad, iSize, iSize, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setHitTest(szName, HitTestTypes.HITTEST_NOHIT)
		self.appendtoHideState(screen, szName, HIDE_TYPE_MAP, HIDE_LEVEL_HIDE)

	def updateTopPortRings(self, bForce):
		try:
			if CyInterface().isCityScreenUp() or CyEngine().isGlobeviewUp():
				return
			if CyInterface().getShowInterface() not in (InterfaceVisibility.INTERFACE_SHOW, InterfaceVisibility.INTERFACE_HIDE):
				return
			if not bForce and self.iTopRingFrames < 60:
				self.iTopRingFrames += 1
				return
			self.iTopRingFrames = 0
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
			dIn = {UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE: False, UnitTravelStates.UNIT_TRAVEL_STATE_IN_AFRICA: False, UnitTravelStates.UNIT_TRAVEL_STATE_IN_PORT_ROYAL: False}
			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			(pUnit, iter) = pPlayer.firstUnit()
			while (pUnit):
				eState = pUnit.getUnitTravelState()
				if eState in dIn and not dIn[eState]:
					if gc.getUnitInfo(pUnit.getUnitType()).getDomainType() == DomainTypes.DOMAIN_SEA and not pUnit.isCargo() and not pUnit.isDelayedDeath():
						dIn[eState] = True
				(pUnit, iter) = pPlayer.nextUnit(iter)
			for (szName, eState) in (("WtpTopPortRingEurope", UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE), ("WtpTopPortRingAfrica", UnitTravelStates.UNIT_TRAVEL_STATE_IN_AFRICA), ("WtpTopPortRingPortRoyal", UnitTravelStates.UNIT_TRAVEL_STATE_IN_PORT_ROYAL)):
				if dIn[eState]:
					screen.show(szName)
				else:
					screen.hide(szName)
		except:
			pass

	# WTP: is an own ship in the port of this sail command (Europe / Africa / Port Royal)?
	def isOwnShipInPort(self, iAction):
		try:
			# the sail buttons are automate actions (AUTOMATE_SAIL_TO_*), recognized by their button art (the Africa / Port Royal
			# automate types are not exposed to Python); the plain sail commands are handled as well
			kAction = gc.getActionInfo(iAction)
			szButton = kAction.getButton().lower()
			iCommand = kAction.getCommandType()
			if iCommand == CommandTypes.COMMAND_SAIL_TO_EUROPE or "sail_to_mother" in szButton:
				eState = UnitTravelStates.UNIT_TRAVEL_STATE_IN_EUROPE
			elif iCommand == CommandTypes.COMMAND_SAIL_TO_AFRICA or "sail_to_africa" in szButton:
				eState = UnitTravelStates.UNIT_TRAVEL_STATE_IN_AFRICA
			elif iCommand == CommandTypes.COMMAND_SAIL_TO_PORT_ROYAL or "sail_to_portroyal" in szButton:
				eState = UnitTravelStates.UNIT_TRAVEL_STATE_IN_PORT_ROYAL
			else:
				return False
			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			(pUnit, iter) = pPlayer.firstUnit()
			bFound = False
			while (pUnit):
				# the ships in a port have this travel state (the docks list of the player only holds the colonists)
				if gc.getUnitInfo(pUnit.getUnitType()).getDomainType() == DomainTypes.DOMAIN_SEA:
					if (pUnit.getUnitTravelState() == eState and not pUnit.isCargo() and not pUnit.isDelayedDeath()):
						bFound = True
				(pUnit, iter) = pPlayer.nextUnit(iter)
			return bFound
		except:
			pass
		return False

	# WTP: the automate type a HUD button stands for (R button: trade routes, C button: full automation), -1 for other buttons
	def getAutomateTypeOfButton(self, iAction):
		try:
			szButton = gc.getActionInfo(iAction).getButton().lower()
			if "automate_city_high_res" in szButton:
				return int(AutomateTypes.AUTOMATE_TRANSPORT_ROUTES)
			if "automate_transport_high_res" in szButton:
				return int(AutomateTypes.AUTOMATE_TRANSPORT_FULL)
		except:
			pass
		return -1

	# WTP: the own units (not in a ship) automated with this type, sorted by id
	def getAutomatedUnits(self, iType):
		aUnits = []
		try:
			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			(pUnit, iter) = pPlayer.firstUnit()
			while (pUnit):
				if not pUnit.isCargo() and not pUnit.isDelayedDeath():
					if int(pUnit.getGroup().getAutomateType()) == iType:
						aUnits.append(pUnit.getID())
				(pUnit, iter) = pPlayer.nextUnit(iter)
		except:
			pass
		aUnits.sort()
		return aUnits

	# WTP: select and center the next / previous transport of the list (the arrows above the R / C button)
	def cycleAutomated(self, iDirection, iType):
		try:
			aUnits = self.getAutomatedUnits(iType)
			if len(aUnits) == 0:
				return
			pCurrent = CyInterface().getHeadSelectedUnit()
			iIndex = -1
			if pCurrent != None and not pCurrent.isNone() and pCurrent.getID() in aUnits:
				iIndex = (aUnits.index(pCurrent.getID()) + iDirection) % len(aUnits)
			elif pCurrent != None and not pCurrent.isNone():
				# the selected transport is not automated (any more): go on from its place in the order of the ids
				iIndex = 0
				if iDirection > 0:
					for iPos in range(len(aUnits)):
						if aUnits[iPos] > pCurrent.getID():
							iIndex = iPos
							break
				else:
					iIndex = len(aUnits) - 1
					for iPos in range(len(aUnits) - 1, -1, -1):
						if aUnits[iPos] < pCurrent.getID():
							iIndex = iPos
							break
			else:
				iIndex = 0
			pUnit = gc.getPlayer(gc.getGame().getActivePlayer()).getUnit(aUnits[iIndex])
			if pUnit != None and not pUnit.isNone():
				CyInterface().selectUnit(pUnit, True, False, True)
				pUnit.centerCamera()
		except:
			pass

	# WTP: is the selected transport automated the way this button does it? R button (trade routes) / Shift+Alt+C button (full automation)
	def isAutomateMarked(self, iAction, pUnit):
		try:
			szButton = gc.getActionInfo(iAction).getButton().lower()
			if "automate_city_high_res" in szButton:
				iType = int(AutomateTypes.AUTOMATE_TRANSPORT_ROUTES)
			elif "automate_transport_high_res" in szButton:
				iType = int(AutomateTypes.AUTOMATE_TRANSPORT_FULL)
			else:
				return False
			return int(pUnit.getGroup().getAutomateType()) == iType
		except:
			return False

	def updateSelectionButtons( self ):
		global g_pSelectedUnit
		global g_CycleUnit
		global g_CycleType
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )

		# Find out our resolution
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		# All of the hides...
		screen.clearMultiList("CityBuildingSelectionMultiList")
		screen.hide("AutomateProduction")
		#screen.hide("CityTransportPanel")
		#screen.hide("CityGarrisonPanel")
		screen.hide("TradeRouteText")
		screen.hide("ImportTradeRouteText")
		screen.hide("ExportTradeRouteText")
		screen.hide("ImportButton")
		screen.hide("ExportButton")
		# teacher list - start - Nightinggale
		screen.hide("TeacherListButton")
		# teacher list - end - Nightinggale
		# R&R, Robert Surcouf, Custom House Popup-Screen START
		screen.hide("CustomHouseButton")
		screen.hide("DomesticMarketButton")
		# R&R, Robert Surcouf, Custom House Popup-Screen END
		screen.hide("ImportLabel")
		screen.hide("ExportLabel")
		screen.hide("CityBuildQueue")
		screen.hide("EmphasizeTable")

		self.setMinimapButtonVisibility(False)
		screen.hideList(ACTION_BUTTON_HIDE)

		for iYield in range(YieldTypes.NUM_YIELD_TYPES):
			screen.hide("YieldCost" + str(iYield))

		if (not CyInterface().isCityScreenUp() and not CyEngine().isGlobeviewUp() and pHeadSelectedCity):
			for i in EMPHASIZEYIELDS:
				screen.show("MapYieldIcon" + str(i))
				screen.hide("MapYieldEmphasize" + str(i))
				screen.hide("MapYieldDe-Emphasize" + str(i))

				if pHeadSelectedCity.AI_getEmphasizeYieldCount(i) > 0:
					screen.show("MapYieldEmphasize" + str(i))
				elif pHeadSelectedCity.AI_getEmphasizeYieldCount(i) < 0:
					screen.show("MapYieldDe-Emphasize" + str(i))

		if (not CyEngine().isGlobeviewUp() and CyInterface().isCityScreenUp() and pHeadSelectedCity):
			self.setMinimapButtonVisibility(True)

			self.updateGarrisonAndTransports()
			g_pSelectedUnit = 0
			screen.enable("HurryGold", pHeadSelectedCity.canHurry(0, False))

			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			iProductionBarSize = BOTTOM_BUTTON_SIZE + 3
			iProductionBarMargin = 0

		# BUILDING SELECTION BUTTONS
			iCount = 0
			iRow = 0
			for i in range (gc.getNumUnitClassInfos()):
				eLoopUnit = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationUnits(i)
				if (eLoopUnit != UnitTypes.NO_UNIT):
					if (pHeadSelectedCity.canTrain(eLoopUnit, False, True)):
						szButton = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitButton(eLoopUnit)
						screen.appendMultiListButton("CityBuildingSelectionMultiList", szButton, iRow, WidgetTypes.WIDGET_TRAIN, i, -1, False)
						if ( not pHeadSelectedCity.canTrain(eLoopUnit, False, False) ):
							screen.disableMultiListButton("CityBuildingSelectionMultiList", iRow, iCount, szButton)
						elif pHeadSelectedCity.getUnitProduction(eLoopUnit) > 0:
							bUnitTypeInQueue = False
							for i in range(CyInterface().getNumOrdersQueued()):
								if (CyInterface().getOrderNodeType(i)  == OrderTypes.ORDER_TRAIN):
									if CyInterface().getOrderNodeData1(i) == eLoopUnit:
										bUnitTypeInQueue = True
										break
							if not bUnitTypeInQueue:
								screen.enableMultiListPulse("CityBuildingSelectionMultiList", True, iRow, iCount)
						iCount += 1

			iCount = 0
			iRow += 1
			for i in range (gc.getNumBuildingClassInfos()):
				eLoopBuilding = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).getCivilizationBuildings(i)
				if (eLoopBuilding != BuildingTypes.NO_BUILDING):
					if (pHeadSelectedCity.canConstruct(eLoopBuilding, False, True, False)):
						screen.appendMultiListButton("CityBuildingSelectionMultiList", gc.getBuildingInfo(eLoopBuilding).getButton(), iRow, WidgetTypes.WIDGET_CONSTRUCT, i, -1, False )
						if (not pHeadSelectedCity.canConstruct(eLoopBuilding, False, False, False)):
							screen.disableMultiListButton("CityBuildingSelectionMultiList", iRow, iCount, gc.getBuildingInfo(eLoopBuilding).getButton())
						elif pHeadSelectedCity.getBuildingProduction(eLoopBuilding) > 0:
							screen.enableMultiListPulse("CityBuildingSelectionMultiList", True, iRow, iCount)

						iCount += 1

			iCount = 0
			iRow += 1
			for i in range (gc.getNumFatherPointInfos()):
				if (pHeadSelectedCity.canConvince(i, False, True)):
					screen.appendMultiListButton("CityBuildingSelectionMultiList", gc.getFatherPointInfo(i).getButton(), iRow, WidgetTypes.WIDGET_CONVINCE, i, -1, False )
					if (not pHeadSelectedCity.canConvince(i, False, False)):
						screen.disableMultiListButton("CityBuildingSelectionMultiList", iRow, iCount, gc.getFatherPointInfo(i).getButton())
					iCount += 1

		# GOVENOR MANAGMENT PANEL
			if AUTOMATION_MANAGMENT_PANEL_UP:
				screen.hide("InterfaceUnitModel")
				screen.hide("_FXS_Screen_Bogus_Minimap_Name")
				screen.hide("CityList")
				screen.hide("CityBuildingSelectionMultiList")
#TAC --->
				screen.hide("CityProductionBar")
				screen.hide("CityProductionBarFrame")
				screen.hide("HurryGold")
#<--- TAC
				screen.hide("MapHighlightButton")
				screen.hide("BuildHighlightButton")
				screen.show("GovernorHighlightButton")

			# EMPHASIZE TABLE
				iRow = 0
				screen.setTableText("EmphasizeTable", 0, iRow, self.setFontSize(localText.getText("TXT_KEY_EMPHASIZE", ()), 1), "", WidgetTypes.WIDGET_EMPHASIZE, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
				for iYield in EMPHASIZEYIELDS:
					iEmphasize = pHeadSelectedCity.AI_getEmphasizeYieldCount(iYield)
					if iEmphasize == 0:
						szText = localText.getText("TXT_KEY_EMPHASIS_NEUTRAL", (gc.getYieldInfo(iYield).getChar(), ))
					elif iEmphasize > 0:
						szText = localText.getText("TXT_KEY_EMPHASIZED", (gc.getYieldInfo(iYield).getChar(), ))
					else:
						szText = localText.getText("TXT_KEY_DEEMPHASIZED", (gc.getYieldInfo(iYield).getChar(), ))
					iRow += 1
					screen.setTableText("EmphasizeTable", 0, iRow, u"<font=3>%s</font>" % szText, "", WidgetTypes.WIDGET_EMPHASIZE, iYield, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.show("EmphasizeTable")

				# R&R, Robert Surcouf, Custom House Popup-Screen START
				screen.setButtonGFC("ImportButton", self.setFontSize(localText.getText("TXT_KEY_DEMO_SCREEN_IMPORTS_TEXT", ()), 1), "", CITIZEN_BAR_WIDTH + (MAP_EDGE_MARGIN_WIDTH * 2), CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH, BUILD_AREA_WIDTH - MEDIUM_BUTTON_SIZE+20, 3 * STACK_BAR_HEIGHT / 2, WidgetTypes.WIDGET_YIELD_IMPORT_EXPORT, True, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

				#screen.setButtonGFC("ImportButton", self.setFontSize(localText.getText("TXT_KEY_DEMO_SCREEN_IMPORTS_TEXT", ()), 1), "", CITIZEN_BAR_WIDTH + (MAP_EDGE_MARGIN_WIDTH * 2), CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH, BUILD_AREA_WIDTH - MEDIUM_BUTTON_SIZE, 3 * STACK_BAR_HEIGHT / 2, WidgetTypes.WIDGET_YIELD_IMPORT_EXPORT, true, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
				# R&R, Robert Surcouf, Custom House Popup-Screen END
				screen.addTableControlGFC("ImportTradeRouteText", 1, CITIZEN_BAR_WIDTH + (MAP_EDGE_MARGIN_WIDTH * 2), CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH + 3 * STACK_BAR_HEIGHT / 2, BUILD_AREA_WIDTH, TRANSPORT_AREA_HEIGHT - (STACK_BAR_HEIGHT * 3), False, False, MEDIUM_BUTTON_SIZE, MEDIUM_BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
				screen.setStyle("ImportTradeRouteText", "Table_EmptyScroll_Style")

				# R&R, Robert Surcouf, Custom House Popup-Screen START
				# R&R mod, vetiarvind, max yield import limit - start
				screen.setButtonGFC("ExportButton", self.setFontSize(localText.getText("TXT_KEY_DEMO_SCREEN_EXPORTS_TEXT", ()), 1), "", CITIZEN_BAR_WIDTH + (MAP_EDGE_MARGIN_WIDTH * 2) + BUILD_AREA_WIDTH, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH, BUILD_AREA_WIDTH - MEDIUM_BUTTON_SIZE+20, 3 * STACK_BAR_HEIGHT / 2, WidgetTypes.WIDGET_CONDENSED_YIELD_IMPORT_EXPORT, False, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
				# R&R mod, vetiarvind, max yield import limit - end
				#screen.setButtonGFC("ExportButton", self.setFontSize(localText.getText("TXT_KEY_DEMO_SCREEN_EXPORTS_TEXT", ()), 1), "", CITIZEN_BAR_WIDTH + (MAP_EDGE_MARGIN_WIDTH * 2) + BUILD_AREA_WIDTH, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH, BUILD_AREA_WIDTH - MEDIUM_BUTTON_SIZE, 3 * STACK_BAR_HEIGHT / 2, WidgetTypes.WIDGET_YIELD_IMPORT_EXPORT, False, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
				# R&R, Robert Surcouf, Custom House Popup-Screen END
				screen.addTableControlGFC("ExportTradeRouteText", 1, CITIZEN_BAR_WIDTH + (MAP_EDGE_MARGIN_WIDTH * 2) + BUILD_AREA_WIDTH, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH + 3 * STACK_BAR_HEIGHT / 2, BUILD_AREA_WIDTH, TRANSPORT_AREA_HEIGHT - (STACK_BAR_HEIGHT * 3), False, False, MEDIUM_BUTTON_SIZE, MEDIUM_BUTTON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
				screen.setStyle("ExportTradeRouteText", "Table_EmptyScroll_Style")

				for iYield in range(YieldTypes.NUM_YIELD_TYPES):
					# transport feeder - start - Nightinggale
					iAutoThreshold = pHeadSelectedCity.getAutoMaintainThreshold(iYield)
					iThreshold     = pHeadSelectedCity.getMaintainLevel(iYield)
					szThreshold = ""
					if (iAutoThreshold > 0):
						szThreshold += " ("
						if (iThreshold < iAutoThreshold):
							szThreshold += unicode(iAutoThreshold) + "/"
						szThreshold += unicode(iThreshold) + ")"
					# transport feeder - end - Nightinggale

					if (pHeadSelectedCity.isExport(iYield)):
						iExportRow = screen.appendTableRow("ExportTradeRouteText")
						szExportText = u"<font=3>%c %s</font>" % (gc.getYieldInfo(iYield).getChar(), gc.getYieldInfo(iYield).getDescription())
						# transport feeder - start - Nightinggale
						#if pHeadSelectedCity.getMaintainLevel(iYield) > 0:
						#	szExportText += " (%s %d)" % (localText.getText("TXT_KEY_TRADE_ROUTE_MAINTAIN", ()), pHeadSelectedCity.getMaintainLevel(iYield))
						szExportText += szThreshold
						# transport feeder - end - Nightinggale
						screen.setTableText("ExportTradeRouteText", 0, iExportRow, u"<font=3>%s</font>" % szExportText, "", WidgetTypes.WIDGET_YIELD_IMPORT_EXPORT, False, -1, CvUtil.FONT_LEFT_JUSTIFY )

					if (pHeadSelectedCity.isImport(iYield)):
						iImportRow = screen.appendTableRow("ImportTradeRouteText")
						szImportText = u"<font=3>%c %s</font>" % (gc.getYieldInfo(iYield).getChar(), gc.getYieldInfo(iYield).getDescription())
						# R&R mod, vetiarvind, max yield import limit - start
						if pHeadSelectedCity.getImportsLimit(iYield) > 0:
							szImportText += " (%s %d)" % (localText.getText("TXT_KEY_TRADE_ROUTE_LIMIT", ()), pHeadSelectedCity.getImportsLimit(iYield))
						# R&R mod, vetiarvind, max yield import limit - end
						# transport feeder - start - Nightinggale
						# turn text green or red for feeder serviced yields
						if (pHeadSelectedCity.isImportFeeder(iYield)):
							if (pHeadSelectedCity.isAutoImportStopped(iYield)):
								szImportText = localText.getText("TXT_KEY_COLOR_NEGATIVE", ()) + szImportText
							else:
								szImportText = localText.getText("TXT_KEY_COLOR_POSITIVE", ()) + szImportText
							szImportText += szThreshold
							szImportText += localText.getText("TXT_KEY_COLOR_REVERT", ())
						# transport feeder - end - Nightinggale
						screen.setTableText("ImportTradeRouteText", 0, iImportRow, szImportText, "", WidgetTypes.WIDGET_YIELD_IMPORT_EXPORT, True, -1, CvUtil.FONT_LEFT_JUSTIFY )

				# teacher list - start - Nightinggale
				screen.setImageButton("TeacherListButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_TEACHER_LIST").getPath(), xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - 2 * CITY_MULTI_TAB_SIZE, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + (STACK_BAR_HEIGHT * 3 / 2) + (MAP_EDGE_MARGIN_WIDTH / 2)-(CITY_MULTI_TAB_SIZE / 2), CITY_MULTI_TAB_SIZE, CITY_MULTI_TAB_SIZE, WidgetTypes.WIDGET_TEACHER_LIST, -1, -1)
				# teacher list - end - Nightinggale
				# R&R, Robert Surcouf, Custom House Popup-Screen START
				#screen.setButtonGFC("CustomHouseButton", self.setFontSize(localText.getText("TXT_KEY_EDIT_CUSTOM_HOUSE_TEXT", ()), 1), "", CITIZEN_BAR_WIDTH + (MAP_EDGE_MARGIN_WIDTH * 2) + BUILD_AREA_WIDTH/4, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH + 50, BUILD_AREA_WIDTH - MEDIUM_BUTTON_SIZE+90, 3 * STACK_BAR_HEIGHT / 2, WidgetTypes.WIDGET_CUSTOM_HOUSE, False, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
				screen.setImageButton("CustomHouseButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CUSTOM_HOUSE").getPath(), xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - 2 * CITY_MULTI_TAB_SIZE, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + (STACK_BAR_HEIGHT * 3 / 2) + (MAP_EDGE_MARGIN_WIDTH / 2)+(CITY_MULTI_TAB_SIZE / 2), CITY_MULTI_TAB_SIZE, CITY_MULTI_TAB_SIZE, WidgetTypes.WIDGET_CUSTOM_HOUSE, -1, -1)
				#screen.setButtonGFC("DomesticMarketButton", self.setFontSize(localText.getText("TXT_KEY_DOMESTIC_MARKET", ()), 1), "", CITIZEN_BAR_WIDTH + (MAP_EDGE_MARGIN_WIDTH * 2) + BUILD_AREA_WIDTH/4, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH + 90, BUILD_AREA_WIDTH - MEDIUM_BUTTON_SIZE+90, 3 * STACK_BAR_HEIGHT / 2, WidgetTypes.WIDGET_DOMESTIC_MARKET, False, -1, ButtonStyles.BUTTON_STYLE_STANDARD)
				screen.setImageButton("DomesticMarketButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_DOMESTIC_MARKET").getPath(), xResolution - (MAP_EDGE_MARGIN_WIDTH * 2) - 2 * CITY_MULTI_TAB_SIZE, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + (STACK_BAR_HEIGHT * 3 / 2) + (MAP_EDGE_MARGIN_WIDTH / 2)+ 3*(CITY_MULTI_TAB_SIZE / 2), CITY_MULTI_TAB_SIZE, CITY_MULTI_TAB_SIZE, WidgetTypes.WIDGET_DOMESTIC_MARKET, -1, -1)
				# R&R, Robert Surcouf, Custom House Popup-Screen END

		# BUILDING MANGMENT PANEL
			elif BUILDING_MANAGMENT_PANEL_UP:
				screen.hide("_FXS_Screen_Bogus_Minimap_Name")
				screen.hide("CityList")
				screen.setState("AutomateProduction", pHeadSelectedCity.isProductionAutomated())

				screen.hide("GovernorHighlightButton")
				screen.hide("MapHighlightButton")
				screen.show("BuildHighlightButton")

				screen.show("AutomateProduction")
				screen.show("CityBuildingSelectionMultiList")
#TAC --->
				screen.show("CityProductionBar")
				screen.show("CityProductionBarFrame")
				screen.show("HurryGold")
#<--- TAC
				screen.hide("EmphasizeTable")

				if (CyInterface().shouldDisplayUnitModel() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL ):
					if (CyInterface().isCitySelection()):
						iOrders = CyInterface().getNumOrdersQueued()
						if (iOrders > 0):
							eOrderNodeType = CyInterface().getOrderNodeType(0)
							if (eOrderNodeType  == OrderTypes.ORDER_TRAIN):
								screen.addUnitGraphicGFC("InterfaceUnitModel", CyInterface().getOrderNodeData1(0), -1, CITIZEN_BAR_WIDTH + ((xResolution - CITIZEN_BAR_WIDTH) * 3 / 7) + (SMALL_BUTTON_SIZE * 2), CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2), BUILD_AREA_WIDTH, CITY_MULTI_TAB_AREA_HEIGHT + (MAP_EDGE_MARGIN_WIDTH * 2), WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, -100, 0, 1, False )
							elif (eOrderNodeType == OrderTypes.ORDER_CONSTRUCT):
								screen.addBuildingGraphicGFC("InterfaceUnitModel", CyInterface().getOrderNodeData1(0), CITIZEN_BAR_WIDTH + ((xResolution - CITIZEN_BAR_WIDTH) * 3 / 7) + (SMALL_BUTTON_SIZE * 2), CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2), BUILD_AREA_WIDTH, CITY_MULTI_TAB_AREA_HEIGHT + (MAP_EDGE_MARGIN_WIDTH * 2), WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, -20, 30, 0.9, False )
							screen.moveToFront("AutomateProduction")
						else:
							screen.hide("ProductionText")
							screen.hide("AutomateProduction")
						screen.show("CityBuildQueue")

		# MAP MANAGMENT PANEL
			elif MAP_MANAGMENT_PANEL_UP:
				screen.hide("InterfaceUnitModel")
				screen.hide("CityBuildingSelectionMultiList")
				screen.hide("EmphasizeTable")
#TAC --->
				screen.hide("CityProductionBar")
				screen.hide("CityProductionBarFrame")
				screen.hide("HurryGold")
#<--- TAC

				screen.addTableControlGFC("CityList", 2, CITIZEN_BAR_WIDTH + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - MAP_EDGE_MARGIN_WIDTH, CITY_TITLE_BAR_HEIGHT + (STACK_BAR_HEIGHT / 2), BUILD_AREA_WIDTH, BUILD_AREA_HEIGHT - STACK_BAR_HEIGHT, False, False, self.SELECTION_PANEL_ROW_HEIGHT, self.SELECTION_PANEL_ROW_HEIGHT, TableStyles.TABLE_STYLE_STANDARD)
				screen.setStyle("CityList", "Table_EmptyScroll_Style")

				screen.setTableColumnHeader("CityList", 0, u"", BUILD_AREA_WIDTH - (BUILD_AREA_WIDTH * 3 / 10))
				screen.setTableColumnHeader("CityList", 1, u"", BUILD_AREA_WIDTH * 3 / 10)
				screen.appendTableRow("CityList")

				pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
				iRow = 0
				for iCity in range(gc.getActivePlayer().getNumCities()):
					pCity = pPlayer.getCity(iCity)
					if (pCity.getID() != pHeadSelectedCity.getID()):
						screen.appendTableRow("CityList")
						screen.setTableText("CityList", 0, iRow, pCity.getName(), "", WidgetTypes.WIDGET_GOTO_CITY, iCity, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText("CityList", 1, iRow, u" (%d)" %(pCity.getPopulation()), "", WidgetTypes.WIDGET_GOTO_CITY, iCity, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						iRow += 1

				screen.show("CityList")
				screen.show("_FXS_Screen_Bogus_Minimap_Name")

				screen.hide("GovernorHighlightButton")
				screen.hide("BuildHighlightButton")
				screen.show("MapHighlightButton")

		elif (not CyEngine().isGlobeviewUp() and pHeadSelectedUnit and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):
			if pHeadSelectedCity and not CyInterface().isCityScreenUp():
				self.setMinimapButtonVisibility(False)
			else:
				self.setMinimapButtonVisibility(True)

			if (CyInterface().getInterfaceMode() == InterfaceModeTypes.INTERFACEMODE_SELECTION):
				if (pHeadSelectedUnit.getOwner() == gc.getGame().getActivePlayer() and g_pSelectedUnit != pHeadSelectedUnit):
					g_pSelectedUnit = pHeadSelectedUnit
					iCount = 0
					actions = CyInterface().getActionsToShow()
					self.SADDLE_BUTTON_SIZE = LARGE_BUTTON_SIZE * 2

					iTotalActions = 0
					if CyInterface().canCreateGroup():
						iTotalActions += 1
					if CyInterface().canDeleteGroup():
						iTotalActions += 1
					iTotalActions += len(actions)

					ACTION_BUTTON_X_BEGIN = xResolution - RIGHT_PANEL_WIDTH
					ACTION_BUTTON_X_STEP = LARGE_BUTTON_SIZE * 3 / 2

					iMaxSpace = ACTION_BUTTON_X_BEGIN - SADDLE_HEIGHT
					iSpaceNeeded = len(range(iTotalActions)) * ACTION_BUTTON_X_STEP

					if iSpaceNeeded > iMaxSpace:
						ACTION_BUTTON_X_STEP = ACTION_BUTTON_X_STEP * iMaxSpace / iSpaceNeeded

					if pHeadSelectedUnit.getID() != g_CycleUnit:
						g_CycleUnit = -1 # the arrows stay only for the transport they were shown for
					ActionButtonList = []
					for iRing in range(40):
						screen.deleteWidget("WtpPortRing" + str(iRing))
					screen.deleteWidget("WtpCycleLeft")
					screen.deleteWidget("WtpCycleRight")
					for i in actions:
						if CyInterface().canHandleAction(i, True):
							Xcord = ACTION_BUTTON_X_BEGIN - iCount * ACTION_BUTTON_X_STEP - LARGE_BUTTON_SIZE
							Ycord = yResolution - SADDLE_HEIGHT / 8
							szName = "ActionButton" + str(iCount)
							screen.setImageButton(szName, gc.getActionInfo(i).getButton(), int(Xcord) - LARGE_BUTTON_SIZE, int(Ycord) - LARGE_BUTTON_SIZE, LARGE_BUTTON_SIZE * 2, LARGE_BUTTON_SIZE * 2, WidgetTypes.WIDGET_ACTION, i, -1)
							screen.setImageShape(szName, ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
							screen.setHitMargins(szName, 18, 18)
							if not CyInterface().canHandleAction(i, False):
								screen.overlayButtonGFC(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_DISABLED_BUTTON").getPath())
							elif pHeadSelectedUnit.isActionRecommended(i) and not self.isOwnShipInPort(i):
								# (WTP: the buttons to sail to Europe / Africa / Port Royal are marked when an own ship is in that port)
								screen.overlayButtonGFC(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
							if (CyInterface().canHandleAction(i, False) and self.isOwnShipInPort(i)) or self.isAutomateMarked(i, pHeadSelectedUnit):
								# WTP: a ring above the sail buttons (Europe / Africa / Port Royal) whose port has an own ship, a bit larger than the button;
								# the same ring marks the R button / full automation button of an automated transport
								szRing = "WtpPortRing" + str(iCount)
								iRingPad = -(LARGE_BUTTON_SIZE / 4)
								screen.addDDSGFC(szRing, "Art/Interface/Game Hud/Actions/port_ring.dds", int(Xcord) - LARGE_BUTTON_SIZE - iRingPad, int(Ycord) - LARGE_BUTTON_SIZE - iRingPad, LARGE_BUTTON_SIZE * 2 + iRingPad * 2, LARGE_BUTTON_SIZE * 2 + iRingPad * 2, WidgetTypes.WIDGET_GENERAL, -1, -1)
								screen.setHitTest(szRing, HitTestTypes.HITTEST_NOHIT)
								ActionButtonList.append(szRing)
							# arrows above the R / C button: cycle through the other transports automated the same way (R: trade routes, C: full
							# automation). They stay while the transport is selected after its automation was switched off (to go on from there)
							iCycleType = self.getAutomateTypeOfButton(i)
							if iCycleType != -1:
								bArrows = False
								if self.isAutomateMarked(i, pHeadSelectedUnit):
									g_CycleUnit = pHeadSelectedUnit.getID()
									g_CycleType = iCycleType
									bArrows = len(self.getAutomatedUnits(iCycleType)) > 1
								elif pHeadSelectedUnit.getID() == g_CycleUnit and iCycleType == g_CycleType:
									bArrows = len(self.getAutomatedUnits(iCycleType)) > 0
								if bArrows:
									iArrow = LARGE_BUTTON_SIZE * 3 / 4
									iArrowY = int(Ycord) - (LARGE_BUTTON_SIZE * 3 / 4) - iArrow + (LARGE_BUTTON_SIZE / 5) # just above the visible top of the ring (the ring art has a transparent margin)
									screen.setImageButton("WtpCycleLeft", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_LEFT_ARROW").getPath(), int(Xcord) - iArrow - 2, iArrowY, iArrow, iArrow, WidgetTypes.WIDGET_GENERAL, WTP_CYCLE_PREV, iCycleType)
									screen.setImageButton("WtpCycleRight", ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_RIGHT_ARROW").getPath(), int(Xcord) + 2, iArrowY, iArrow, iArrow, WidgetTypes.WIDGET_GENERAL, WTP_CYCLE_NEXT, iCycleType)
									ActionButtonList.append("WtpCycleLeft")
									ActionButtonList.append("WtpCycleRight")
							ActionButtonList.append(szName)

							iCount += 1

					if (CyInterface().canCreateGroup()):
						Xcord = ACTION_BUTTON_X_BEGIN - iCount * ACTION_BUTTON_X_STEP - LARGE_BUTTON_SIZE
						Ycord = yResolution - SADDLE_HEIGHT / 8
						screen.setImageButton("CreateGroupButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CREATEGROUP").getPath(), int(Xcord) - LARGE_BUTTON_SIZE, int(Ycord) - LARGE_BUTTON_SIZE, LARGE_BUTTON_SIZE * 2, LARGE_BUTTON_SIZE * 2, WidgetTypes.WIDGET_CREATE_GROUP, -1, -1)
						screen.setImageShape("CreateGroupButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
						screen.setHitMargins("CreateGroupButton", 18, 18)
						ActionButtonList.append("CreateGroupButton")

						iCount += 1

					if (CyInterface().canDeleteGroup()):
						Xcord = ACTION_BUTTON_X_BEGIN - iCount * ACTION_BUTTON_X_STEP - LARGE_BUTTON_SIZE
						Ycord = yResolution - SADDLE_HEIGHT / 8
						screen.setImageButton("DeleteGroupButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_SPLITGROUP").getPath(), int(Xcord) - LARGE_BUTTON_SIZE, int(Ycord) - LARGE_BUTTON_SIZE, LARGE_BUTTON_SIZE * 2, LARGE_BUTTON_SIZE * 2, WidgetTypes.WIDGET_DELETE_GROUP, -1, -1)
						screen.setImageShape("DeleteGroupButton", ImageShapes.IMAGE_SHAPE_ELLIPSE, -1)
						screen.setHitMargins("DeleteGroupButton", 18, 18)
						ActionButtonList.append("DeleteGroupButton")

						iCount += 1

					screen.registerHideList(ActionButtonList, len(ActionButtonList), ACTION_BUTTON_HIDE)

		elif (CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY):
			screen.hide("CityBuildingSelectionMultiList")
			screen.hide("EmphasizeTable")
			self.setMinimapButtonVisibility(True)

		return 0
	# Will update the citizen buttons
	def updateCitizenButtons( self ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		screen.hideList(CITIZEN_HIDE)

		if (CyInterface().isCityScreenUp()):
			CitizenHideList = []

		# ON PLOT WORKERS
###=====City Radius 2 (NeverMind)===1/2=====###
			city_radius = gc.getCityDiameter()
			pHeadSelectedCity = CyInterface().getHeadSelectedCity()
			ButtonSize = (CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 4 ))  / city_radius

			if (pHeadSelectedCity.getPopulation() == 0): # TAC abandon city
				return # TAC abandon city- Required to correct graphical bugginess when viewing a pop 0 city

			if (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
				for iPlotIndex in range(gc.getNUM_CITY_PLOTS()):
					# removed an if statement. Added a bogus one to avoid touching all lines due to indenting
					if 1:
						pUnit = pHeadSelectedCity.getUnitWorkingPlot(iPlotIndex)
						pPlot = pHeadSelectedCity.getCityIndexPlot(iPlotIndex)
						if not pPlot.isNone():
							worldPosition = pPlot.getPoint()
							worldPosition.x -= gc.getPLOT_SIZE() / 2
							# Two Plots, Robert Surcouf, Screen yResolution - Start
							if (city_radius == 5 and (xResolution * 10) / yResolution > 15):
								worldPosition.x +=(xResolution * 13)/yResolution
								worldPosition.y -=(xResolution * 13)/yResolution
							# Two Plots, Robert Surcouf, Screen yResolution - End
							screenPosition = CyEngine().worldPointToScreenPoint(worldPosition)

							# PLOT DRAG ON PANELS
###=====City Radius 2 (NeverMind)===2/2=====###

							x = int(screenPosition.x)
							y =	int(screenPosition.y) - ButtonSize / (city_radius - 1)
							size_x = CITY_VIEW_BOX_HEIGHT_AND_WIDTH / city_radius
							size_y = CITY_VIEW_BOX_HEIGHT_AND_WIDTH / city_radius

							if iPlotIndex == gc.getCITY_HOME_PLOT():
								screen.setImageButton("PlotDragOn" + str(iPlotIndex), "", x, y, size_x, size_y, WidgetTypes.WIDGET_CITY_CENTER_PLOT, -1, -1)
								CitizenHideList.append("PlotDragOn" + str(iPlotIndex))
								continue

							screen.addDDSGFC("PlotDragOn" + str(iPlotIndex), "", x, y, size_x, size_y, WidgetTypes.WIDGET_ASSIGN_CITIZEN_TO_PLOT, iPlotIndex, -1)
							CitizenHideList.append("PlotDragOn" + str(iPlotIndex))

							# city plot mouse over help - inaiwae - START
							screen.addDDSGFC("CityPlotInfo" + str(iPlotIndex), "", x-(size_x/32), y, size_x, size_y, WidgetTypes.WIDGET_CITY_PLOT_INFO, iPlotIndex, -1)
							CitizenHideList.append("CityPlotInfo" + str(iPlotIndex))
							# city plot mouse over help - inaiwae - END

							if (not pUnit.isNone()):
								if (pUnit.isColonistLocked()):
									szName = "CitizenButtonLock" + str(pUnit.getID())
									screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_CITIZEN_LOCK").getPath(), int(screenPosition.x) - 5, int(screenPosition.y) - ButtonSize / 2 - 5, STACK_BAR_HEIGHT * 3 / 2, STACK_BAR_HEIGHT * 3 / 2, WidgetTypes.WIDGET_GENERAL, -1, -1)
									CitizenHideList.append(szName)

								szName = "WorkerButton" + str(iPlotIndex)
								screen.addDragableButton(szName, pUnit.getFullLengthIcon(), "", int(screenPosition.x), int(screenPosition.y) - ButtonSize / 2, ButtonSize / 2, ButtonSize, WidgetTypes.WIDGET_CITIZEN, pUnit.getID(), -1, ButtonStyles.BUTTON_STYLE_IMAGE )
								CitizenHideList.append(szName)
							elif (pPlot.getOwner() == pHeadSelectedCity.getOwner()):
								szName = "WorkerSlot" + str(iPlotIndex)
								screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITIZEN_SLOT").getPath(), int(screenPosition.x), int(screenPosition.y) - ButtonSize / 2, ButtonSize / 2, ButtonSize, WidgetTypes.WIDGET_ASSIGN_CITIZEN_TO_PLOT, iPlotIndex, -1)
								CitizenHideList.append(szName)

		# IN CITY WORKERS
			pHeadSelectedCity = CyInterface().getHeadSelectedCity()
			pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()

			if (pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW):
				CitizenProfessionIndexArray = []
				CitizenSpecialBuildingIndexArray = []
				CitizenBarCount = 0
				for iProfession in range(gc.getNumProfessionInfos()):
					CitizenProfessionIndexArray.append([])

				for iSpecialBuilding in range(gc.getNumSpecialBuildingInfos()):
					CitizenSpecialBuildingIndexArray.append([])

				for j in range(pHeadSelectedCity.getPopulation()):
					# R&R, Robert Surcouf, Rebellion Fix START
					pCitizen = pHeadSelectedCity.getPopulationUnitByIndex(j)
					if pCitizen.getProfession() != ProfessionTypes.NO_PROFESSION:
						CitizenProfessionIndexArray[pCitizen.getProfession()].append(pCitizen)
						CitizenSpecialBuildingIndexArray[gc.getProfessionInfo(pCitizen.getProfession()).getSpecialBuilding()].append(pCitizen)
					CitizenBarCount += 1
					# R&R, Robert Surcouf, Rebellion Fix START
#MultipleYieldsProduced Start
				for iProfession in range(gc.getNumProfessionInfos()):
					if (not gc.getProfessionInfo(iProfession).isWorkPlot() and gc.getProfessionInfo(iProfession).isCitizen()):
						if gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).isValidProfession(iProfession):
							iSpecialBuildingType = gc.getProfessionInfo(iProfession).getSpecialBuilding()
							iYield = gc.getProfessionInfo(iProfession).getYieldsProduced(0)
							CityBuilding = -1
#MultipleYieldsProduced End

				for iBuilding in range(gc.getNumBuildingInfos()):
					if (pHeadSelectedCity.isHasBuilding(iBuilding)):
						iSpecialBuildingType = gc.getBuildingInfo(iBuilding).getSpecialBuildingType()
						CityBuilding = iBuilding

						iProfession = -1
						iSecondYield = -1
						bFirstYield = True
						if (gc.getBuildingInfo(CityBuilding).getMaxWorkers() >= 0):
							for iArrayProfession in range(gc.getNumProfessionInfos()):
								if (gc.getProfessionInfo(iArrayProfession).getSpecialBuilding() == iSpecialBuildingType):
									if (not gc.getProfessionInfo(iArrayProfession).isWorkPlot() and gc.getProfessionInfo(iArrayProfession).isCitizen()):
										if gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).isValidProfession(iArrayProfession):
											if (bFirstYield == True):
												iYield = gc.getProfessionInfo(iArrayProfession).getYieldsProduced(0) #MultipleYieldsProduced Start
												iProfession = iArrayProfession
												bFirstYield = False
											else:
												iSecondYield = gc.getProfessionInfo(iArrayProfession).getYieldsProduced(0) #MultipleYieldsProduced Start

							if (CityBuilding != -1 and iProfession != -1):
								ButtonSize = LARGE_BUTTON_SIZE * 5 / 2


								bHasYield = (pHeadSelectedCity.getBaseRawYieldProduced(iYield) != 0 or pHeadSelectedCity.getRawYieldConsumed(iYield) != 0)

								if (gc.getBuildingInfo(CityBuilding).getMaxWorkers() > 0):
									CitizenSpacing = BUILDING_GRID[iSpecialBuildingType][3] / gc.getBuildingInfo(iBuilding).getMaxWorkers()
								else:
									CitizenSpacing = ButtonSize / 2

								#RWL for SpecialBuilding Trade
								if (CityBuilding != -1):
									screen.show("ProductionBox" + str(iSpecialBuildingType))
									szName = "YieldOutPutIcon" + str(iYield)
									if (iSecondYield < 0 or iSecondYield >= YieldTypes.NUM_YIELD_TYPES or iSecondYield == iYield):
										screen.addDDSGFC(szName, gc.getYieldInfo(iYield).getIcon(), BUILDING_GRID[iSpecialBuildingType][0] + (STACK_BAR_HEIGHT / 2), BUILDING_GRID[iSpecialBuildingType][1] + BUILDING_GRID[iSpecialBuildingType][2] - (BUILDING_GRID[iSpecialBuildingType][2] / 6) + STACK_BAR_HEIGHT, STACK_BAR_HEIGHT * 3 / 2, STACK_BAR_HEIGHT * 3 / 2, WidgetTypes.WIDGET_HELP_YIELD, iYield, -1)
									else:
										# R&R, we do not show the first icon any more, if we have MultipleProfessionsPerBuilding
										# screen.addDDSGFC(szName, gc.getYieldInfo(iYield).getIcon(), BUILDING_GRID[iSpecialBuildingType][0] + (STACK_BAR_HEIGHT / 2), BUILDING_GRID[iSpecialBuildingType][1] + BUILDING_GRID[iSpecialBuildingType][2] - (BUILDING_GRID[iSpecialBuildingType][2] / 6) + STACK_BAR_HEIGHT, STACK_BAR_HEIGHT * 3 / 2, STACK_BAR_HEIGHT * 3 / 2, WidgetTypes.WIDGET_HELP_TWO_YIELDS, iYield, iSecondYield)
										szSecondName = "SecondYieldOutPutIcon" + str(iSecondYield) #the second icon must not use "szName", or it replaces the former icon
										if (iSecondYield == YieldTypes.YIELD_FOOD):
											screen.addDDSGFC(szSecondName, gc.getYieldInfo(iYield).getIcon(), BUILDING_GRID[iSpecialBuildingType][0] + (STACK_BAR_HEIGHT / 2), BUILDING_GRID[iSpecialBuildingType][1] + BUILDING_GRID[iSpecialBuildingType][2] - (BUILDING_GRID[iSpecialBuildingType][2] / 6) + STACK_BAR_HEIGHT, STACK_BAR_HEIGHT * 3 / 2, STACK_BAR_HEIGHT * 3 / 2, WidgetTypes.WIDGET_HELP_TWO_YIELDS, iYield, iSecondYield)
										else:
											screen.addDDSGFC(szSecondName, gc.getYieldInfo(iSecondYield).getCombiIcon(), BUILDING_GRID[iSpecialBuildingType][0] + (STACK_BAR_HEIGHT / 2), BUILDING_GRID[iSpecialBuildingType][1] + BUILDING_GRID[iSpecialBuildingType][2] - (BUILDING_GRID[iSpecialBuildingType][2] / 6) + STACK_BAR_HEIGHT, STACK_BAR_HEIGHT * 3 / 2, STACK_BAR_HEIGHT * 3 / 2, WidgetTypes.WIDGET_HELP_TWO_YIELDS, iYield, iSecondYield)
										CitizenHideList.append(szSecondName)
									CitizenHideList.append(szName)

								else:
									screen.hide("ProductionBox" + str(iSpecialBuildingType))

								ProfessionCount = len(CitizenSpecialBuildingIndexArray[iSpecialBuildingType])
								for GroupIndex in range(ProfessionCount):
									pCitizen = CitizenSpecialBuildingIndexArray[iSpecialBuildingType][GroupIndex]

									if (pCitizen.isColonistLocked()):
										szName = "CitizenButtonLock" + str(pCitizen.getID())
										screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITY_CITIZEN_LOCK").getPath(), BUILDING_GRID[iSpecialBuildingType][0] + (CitizenSpacing * GroupIndex) + (CitizenSpacing / 2) - (STACK_BAR_HEIGHT / 3), BUILDING_GRID[iSpecialBuildingType][1] + BUILDING_GRID[iSpecialBuildingType][2] - (ButtonSize) - (STACK_BAR_HEIGHT * 2 / 3), STACK_BAR_HEIGHT * 4 / 3, STACK_BAR_HEIGHT * 4 / 3, WidgetTypes.WIDGET_GENERAL, -1, -1)
										CitizenHideList.append(szName)

									szName = "CitizenButton" + str(iProfession) + "-" + str(GroupIndex)
									screen.addDragableButton(szName, pCitizen.getFullLengthIcon(), "", BUILDING_GRID[iSpecialBuildingType][0] + (CitizenSpacing * GroupIndex) + (CitizenSpacing/ 2), BUILDING_GRID[iSpecialBuildingType][1] + BUILDING_GRID[iSpecialBuildingType][2] - (ButtonSize), ButtonSize / 2, ButtonSize, WidgetTypes.WIDGET_CITIZEN, pCitizen.getID(), -1, ButtonStyles.BUTTON_STYLE_IMAGE)
									CitizenHideList.append(szName)

								for iSlot in range (gc.getBuildingInfo(CityBuilding).getMaxWorkers() - ProfessionCount):
									szName = "CitizenSlot" + str(iProfession) + "-" + str(iSlot)
									screen.addDDSGFC(szName, ArtFileMgr.getInterfaceArtInfo("INTERFACE_CITIZEN_SLOT").getPath(), BUILDING_GRID[iSpecialBuildingType][0] + (CitizenSpacing * (iSlot + ProfessionCount)) + (CitizenSpacing/ 2), BUILDING_GRID[iSpecialBuildingType][1] + BUILDING_GRID[iSpecialBuildingType][2] - ButtonSize, ButtonSize / 2, ButtonSize, WidgetTypes.WIDGET_ASSIGN_CITIZEN_TO_BUILDING, -1, CityBuilding)
									CitizenHideList.append(szName)

								SzText = ""
								bTwoYields = False
								for iArrayProfession in range(gc.getNumProfessionInfos()):
									if (gc.getProfessionInfo(iArrayProfession).getSpecialBuilding() == iSpecialBuildingType):
										if (not gc.getProfessionInfo(iArrayProfession).isWorkPlot() and gc.getProfessionInfo(iArrayProfession).isCitizen()):
											if gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType()).isValidProfession(iArrayProfession):
												iAmountYield = gc.getProfessionInfo(iArrayProfession).getYieldsProduced(0) #MultipleYieldsProduced Start
												ProducedYield = 0
												for pCitizen in CitizenSpecialBuildingIndexArray[iSpecialBuildingType]:
													if (pCitizen.getProfession() == iArrayProfession):
														ProducedYield += pHeadSelectedCity.getProfessionOutput(iArrayProfession, pCitizen)

												ProducedYield = ProducedYield * pHeadSelectedCity.getBaseYieldRateModifier(iAmountYield, 0) / 100

												CityProducedYield = pHeadSelectedCity.getBaseRawYieldProduced(iAmountYield)
												CityActualYield = pHeadSelectedCity.calculateActualYieldProduced(iAmountYield)

												if (CityProducedYield > 0):
													ActualYield = ProducedYield * CityActualYield / CityProducedYield
												else:
													ActualYield = ProducedYield

												UnproducedYield = ProducedYield - ActualYield

												if (bTwoYields == False):
													if (ActualYield > 0):
														bTwoYields = True
														SzText += u"<color=0,255,0> +" + str(ActualYield) + "</color>"
													if (UnproducedYield > 0):
														SzText += u"<color=255,0,0> -" + str(UnproducedYield) + "</color>"
												else:
													if (iAmountYield != iYield):
														if (ActualYield > 0):
															SzText += u"<color=255,255,255> /" + "</color>"
															SzText += u"<color=0,255,0> +" + str(ActualYield) + "</color>"
														if (UnproducedYield > 0):
															SzText += u"<color=255,0,0> -" + str(UnproducedYield) + "</color>"
        
								szName = "WorkerOutputText" + str(iYield)
								if (iSecondYield == -1 or iSecondYield == iYield):
									screen.setLabelAt(szName, "ProductionBox" + str(iSpecialBuildingType), self.setFontSize(SzText , 0), CvUtil.FONT_RIGHT_JUSTIFY, (BUILDING_GRID[iSpecialBuildingType][3] + STACK_BAR_HEIGHT) *2 / 3, STACK_BAR_HEIGHT *2 /5, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_YIELD, iYield, -1)
								else:
									screen.setLabelAt(szName, "ProductionBox" + str(iSpecialBuildingType), self.setFontSize(SzText , 0), CvUtil.FONT_RIGHT_JUSTIFY, (BUILDING_GRID[iSpecialBuildingType][3] + STACK_BAR_HEIGHT) *2 / 3, STACK_BAR_HEIGHT *2 /5, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_TWO_YIELDS, iYield, iSecondYield)

								CitizenHideList.append(szName)
								CitizenHideList.append("ProductionBox" + str(iSpecialBuildingType)) # R&R, Robert Surcouf Fix Production box
							else:
								screen.hide("ProductionBox" + str(iSpecialBuildingType))
				#Androrc End

				iSpace = CITIZEN_BAR_WIDTH - (LARGE_BUTTON_SIZE * 3)
				iSeperation = iSpace / CitizenBarCount
				if (iSeperation > (LARGE_BUTTON_SIZE * 2)):
					iSeperation = (LARGE_BUTTON_SIZE * 2)
				iCount = 0

				for iProfession in range(gc.getNumProfessionInfos()):
					for GroupIndex in range(len(CitizenProfessionIndexArray[iProfession])):
						pCitizen = CitizenProfessionIndexArray[iProfession][GroupIndex]
						szName = "PopulationButton" + str(iCount)
						ButtonSize = LARGE_BUTTON_SIZE * 3
						screen.show(szName)
						screen.setState(szName, pCitizen.isColonistLocked())
						CitizenHideList.append(szName)
						iCount += 1

			screen.registerHideList(CitizenHideList, len(CitizenHideList), CITIZEN_HIDE)
			self.updateGarrisonAndTransports()
			self.updateResourceTable()

		return 0

	# Will update the Garrison and Transport Panels
	def updateGarrisonAndTransports( self ):

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

#TAC --->
	# TRANSPORT MANAGMENT
		TransportButtonSize = LARGE_BUTTON_SIZE * 4 / 3
		CargoButtonSize = MEDIUM_BUTTON_SIZE
		yLocation = STACK_BAR_HEIGHT	* 3 / 2
		PanelHeight = TransportButtonSize * 6 / 5
		CyInterface().cacheInterfacePlotUnits(pHeadSelectedCity.plot())
		#screen.addScrollPanel("CityGarrisonPanel", u"", CITIZEN_BAR_WIDTH + (SMALL_BUTTON_SIZE / 2), yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT * 9 / 8 - 2, xResolution - CITIZEN_BAR_WIDTH - TRANSPORT_AREA_WIDTH + STACK_BAR_HEIGHT, TRANSPORT_AREA_HEIGHT + (STACK_BAR_HEIGHT / 3), PanelStyles.PANEL_STYLE_EMPTY, False, WidgetTypes.WIDGET_EJECT_CITIZEN, -1, -1 )
		#screen.addScrollPanel("CityTransportPanel", u"", xResolution - TRANSPORT_AREA_WIDTH + MAP_EDGE_MARGIN_WIDTH - SMALL_BUTTON_SIZE / 2, yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT * 9 / 8 - 2, TRANSPORT_AREA_WIDTH * 126 / 128, TRANSPORT_AREA_HEIGHT + (STACK_BAR_HEIGHT / 3), PanelStyles.PANEL_STYLE_MAIN, False, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )
		screen.setLabelAt("TransportPanelLabel", "CityTransportPanel", "    " + self.setFontSize((localText.getColorText("TXT_KEY_TRANSPORT_PANEL", (), ColorTypes.COLOR_FONT_CREAM)).upper(), 0), CvUtil.FONT_LEFT_JUSTIFY, 0, STACK_BAR_HEIGHT / 2, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )

		global LAST_CACHED_TRANSPORT_UNITS_COUNT
		for i in range(LAST_CACHED_TRANSPORT_UNITS_COUNT):
			screen.hide("VisitingShipPanel" + str(i))
			screen.hide("VisitingShipIcon" + str(i))
			screen.hide("TransportAutomated" + str(i))
			for j in range(10):
				screen.hide("CargoCell" + str(i) + "-" + str(j))
			screen.hide("CargoUnit" + str(i))
			screen.hide("CargoCount" + str(i))
		LAST_CACHED_TRANSPORT_UNITS_COUNT = CyInterface().getNumCachedInterfacePlotUnits()

		for i in range(CyInterface().getNumCachedInterfacePlotUnits()):
			pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
			if (pLoopUnit and pLoopUnit.getOwner() == pHeadSelectedCity.getOwner()):
				if (pLoopUnit.cargoSpace() > 0 and not pLoopUnit.isCargo()):
					visitingShipWidth = TransportButtonSize + pLoopUnit.cargoSpace() * (CargoButtonSize * 11 / 10)
					xPosition = (TRANSPORT_AREA_WIDTH * 116 / 128 - visitingShipWidth) / 2
					screen.addDDSGFCAt("VisitingShipPanel" + str(i), "CityTransportPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_IN_PORT_BOX").getPath(), xPosition, yLocation, TransportButtonSize + pLoopUnit.cargoSpace() * (CargoButtonSize * 11 / 10), PanelHeight, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_TRANSPORT, pLoopUnit.getID(), -1, False)
					screen.addCheckBoxGFCAt("CityTransportPanel", "VisitingShipIcon" + str(i), pLoopUnit.getButton(), "", xPosition, yLocation + (PanelHeight / 2) - (TransportButtonSize / 2), TransportButtonSize, TransportButtonSize, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_TRANSPORT, pLoopUnit.getID(), -1, ButtonStyles.BUTTON_STYLE_LABEL)
					if pLoopUnit.isAutomated():
						screen.addDDSGFCAt("TransportAutomated" + str(i), "CityTransportPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_AUTOMATE").getPath(), xPosition + (CargoButtonSize * 3 / 4), yLocation + (PanelHeight / 2) - (TransportButtonSize / 2) + (CargoButtonSize * 3 / 4), TransportButtonSize * 3 / 4, TransportButtonSize * 3 / 4, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_TRANSPORT, pLoopUnit.getID(), -1, False)
					yLocation += (PanelHeight / 2) - (CargoButtonSize / 2)
					xPosition += TransportButtonSize

					for j in range(pLoopUnit.cargoSpace()):
						screen.addDDSGFCAt("CargoCell" + str(i) + "-" + str(j), "CityTransportPanel", ArtFileMgr.getInterfaceArtInfo("INTERFACE_EUROPE_BOX_CARGO").getPath(), xPosition + (j * (CargoButtonSize * 11 / 10)), yLocation - (CargoButtonSize / 4), CargoButtonSize, CargoButtonSize, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_TRANSPORT, pLoopUnit.getID(), -1, False)

					for j in range(CyInterface().getNumCachedInterfacePlotUnits()):
						CargoUnit = CyInterface().getCachedInterfacePlotUnit(j)
						transportUnit = CargoUnit.getTransportUnit()
						if (not transportUnit.isNone() and transportUnit.getID() == pLoopUnit.getID()):
							iYield = CargoUnit.getYield()
							screen.addDragableButtonAt("CityTransportPanel", "CargoUnit" + str(j), CargoUnit.getButton(), "", xPosition, yLocation - (CargoButtonSize / 4), CargoButtonSize, CargoButtonSize, WidgetTypes.WIDGET_MOVE_CARGO_TO_CITY, pLoopUnit.getID(), CargoUnit.getID(), ButtonStyles.BUTTON_STYLE_LABEL)
							if CargoUnit.isGoods():
								szText = u"<font=3>%s</font>" % CargoUnit.getYieldStored()
								screen.setLabelAt("CargoCount" + str(j), "CityTransportPanel", szText, CvUtil.FONT_CENTER_JUSTIFY, xPosition + (CargoButtonSize / 2), yLocation + (TransportButtonSize * 4 / 6), -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
							xPosition += (CargoButtonSize * 11 / 10)
					yLocation += (PanelHeight / 2) + (CargoButtonSize / 2) + (CargoButtonSize / 10)

	# GARISSON MANAGMENT PANEL
		GarrisonButtonSize = LARGE_BUTTON_SIZE
		self.PLOT_LIST_ICON_SIZE = 12
		self.PLOT_LIST_HEALTH_BAR_HEIGHT = 11
		self.PLOT_LIST_HEALTH_BAR_SHORTENING_CORRECTION = 6
		CyInterface().cacheInterfacePlotUnits(pHeadSelectedCity.plot())
		#screen.addScrollPanel("CityGarrisonPanel", u"", CITIZEN_BAR_WIDTH + (SMALL_BUTTON_SIZE / 8), yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT * 9 / 8 - 2, xResolution - CITIZEN_BAR_WIDTH - TRANSPORT_AREA_WIDTH + STACK_BAR_HEIGHT * 4 / 8, TRANSPORT_AREA_HEIGHT + (STACK_BAR_HEIGHT / 3), PanelStyles.PANEL_STYLE_EMPTY, False, WidgetTypes.WIDGET_EJECT_CITIZEN, -1, -1 )
		screen.setLabelAt("CityGarrisonLabel", "CityGarrisonPanel", self.setFontSize((localText.getColorText("TXT_KEY_GARRISON_PANEL", (), ColorTypes.COLOR_FONT_CREAM)).upper(), 0), CvUtil.FONT_LEFT_JUSTIFY, SMALL_BUTTON_SIZE / 4, STACK_BAR_HEIGHT / 2, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_EJECT_CITIZEN, -1, -1 )

		global LAST_CACHED_GARRISON_UNITS_COUNT
		for i in range(LAST_CACHED_GARRISON_UNITS_COUNT):
			screen.hide("GarrisonUnit" + str(i))
			screen.hide("GarrisonHealth" + str(i))
			screen.hide("GarrisonMoveIcon" + str(i))
		LAST_CACHED_GARRISON_UNITS_COUNT = CyInterface().getNumCachedInterfacePlotUnits()

		xPosition = 0
		GarrisonUnitsWidth = GarrisonButtonSize * 3
		xPositionBase = (xResolution - CITIZEN_BAR_WIDTH - TRANSPORT_AREA_WIDTH - STACK_BAR_HEIGHT - GarrisonUnitsWidth) / 2

		yPosition = 0
		for i in range(CyInterface().getNumCachedInterfacePlotUnits()):
			pLoopUnit = CyInterface().getCachedInterfacePlotUnit(i)
			if (pLoopUnit):
				if (pLoopUnit.getOwner() == pHeadSelectedCity.getOwner() and pLoopUnit.cargoSpace() == 0):
					if (pLoopUnit.getYield() == YieldTypes.NO_YIELD ):
						if (pLoopUnit.getTransportUnit().isNone()):
							cityGarrisonX = xPosition * GarrisonButtonSize + xPositionBase
#<--- TAC
							cityGarrisonY = STACK_BAR_HEIGHT * 3 / 2 + (yPosition * (GarrisonButtonSize + self.PLOT_LIST_HEALTH_BAR_SHORTENING_CORRECTION))
							screen.addDragableButtonAt("CityGarrisonPanel", "GarrisonUnit" + str(i), pLoopUnit.getButton(), "", cityGarrisonX, cityGarrisonY, GarrisonButtonSize, GarrisonButtonSize, WidgetTypes.WIDGET_EJECT_CITIZEN, pLoopUnit.getID(), -1, ButtonStyles.BUTTON_STYLE_LABEL)

						# HEALTH BAR
							HealthBar = "GarrisonHealth" + str(i)
							screen.addStackedBarGFCAt( HealthBar, "CityGarrisonPanel", cityGarrisonX, cityGarrisonY + GarrisonButtonSize - (self.PLOT_LIST_HEALTH_BAR_HEIGHT / 2), GarrisonButtonSize, self.PLOT_LIST_HEALTH_BAR_HEIGHT, InfoBarTypes.NUM_INFOBAR_TYPES, WidgetTypes.WIDGET_EJECT_CITIZEN, pLoopUnit.getID(), -1 )
							screen.setBarPercentage( HealthBar, InfoBarTypes.INFOBAR_STORED, float( pLoopUnit.currHitPoints() ) / float( pLoopUnit.maxHitPoints() ) )

							if (pLoopUnit.getDamage() >= ((pLoopUnit.maxHitPoints() * 2) / 3)):
								screen.setStackedBarColors(HealthBar, InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_RED)
							elif (pLoopUnit.getDamage() >= (pLoopUnit.maxHitPoints() / 3)):
								screen.setStackedBarColors(HealthBar, InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_YELLOW)
							else:
								screen.setStackedBarColors(HealthBar, InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_GREEN)

						# MOVE ICON
							if pLoopUnit.isWaiting():
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_FORTIFY").getPath()
							elif (pLoopUnit.canMove()):
								if (pLoopUnit.hasMoved()):
									szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_HASMOVED").getPath()
								else:
									szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_MOVE").getPath()
							else:
								szFileName = ArtFileMgr.getInterfaceArtInfo("OVERLAY_NOMOVE").getPath()
							screen.addDDSGFCAt( "GarrisonMoveIcon" + str(i), "CityGarrisonPanel", szFileName, cityGarrisonX, (STACK_BAR_HEIGHT * 3 / 2) + (yPosition * (GarrisonButtonSize + self.PLOT_LIST_HEALTH_BAR_SHORTENING_CORRECTION)), self.PLOT_LIST_ICON_SIZE, self.PLOT_LIST_ICON_SIZE, WidgetTypes.WIDGET_EJECT_CITIZEN, -1, -1, False )

							xPosition += 1
							if (xPosition == 3):
								xPosition = 0
								yPosition += 1

		return 0

	# Will update the game data strings
	def updateGameDataStrings( self ):

		screen = CyGInterfaceScreen( "MainInterface", CvScreenEnums.MAIN_INTERFACE )
		screen.hide("ClockText")
		bShift = CyInterface().shiftKey()

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if (pHeadSelectedCity):
			ePlayer = pHeadSelectedCity.getOwner()
		else:
			ePlayer = gc.getGame().getActivePlayer()

		if ( ePlayer < 0 or ePlayer >= gc.getMAX_PLAYERS() ):
			return 0

		if ( CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY  and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_ADVANCED_START):
			szTimeText = unicode(CyGameTextMgr().getInterfaceTimeStr(gc.getGame().getActivePlayer()))
			screen.setLabel("TimeText", "Background", self.setFontSize(szTimeText, 1), CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 17, 17, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, TIMETEXT_ID, -1 )
			if (CyUserProfile().isClockOn()):
				screen.setLabel("ClockText", "Background", self.setFontSize(getClockText(), 0), CvUtil.FONT_RIGHT_JUSTIFY, xResolution - 24, 42, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.show("ClockText")

			if (gc.getPlayer(ePlayer).isAlive()):
				szText = CyGameTextMgr().getGoldStr(ePlayer)
				screen.setLabel("GoldText", "Background", self.setFontSize(szText, 1), CvUtil.FONT_LEFT_JUSTIFY, 17, 17, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, TIMETEXT_ID, -1 )
				# WTP: the gold pile icon follows the amount: up to 4 digits it keeps its place, from 5 digits every digit moves it 11 pixels to the right (5 = 75, 6 = 86), so the amount only just touches it
				try:
					iDigits = len([c for c in unicode(szText) if c.isdigit()])
					iPileX = 60
					if iDigits > 4:
						iPileX = 20 + iDigits * 11
					screen.moveItem("GoldPile", iPileX, 8, -0.3)
				except:
					pass

		return 0


	# Will update the selection Data Strings
	def updateCityScreen( self ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		# WTP: the switch for the job automation shows the colony's state
		if pHeadSelectedCity:
			self.drawAutoAssignTarget(pHeadSelectedCity.isAutoAssignTarget())

		# Find out our resolution
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()
		bShift = CyInterface().shiftKey()

	# INITILIZE CITY VIEW CAMERA
		# Pixel center of the map frame (not the unadjusted percent, which sat
		# too high on widescreen). Inset the 1.3x title-bar art; bias left so
		# east bonus icons clear the build panel. Do not also shift down, or
		# the south-plot yield stacks sit under the map-frame border.
		mapFrameSize = CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2)
		titleOverlap = int(CITY_TITLE_BAR_HEIGHT * 0.3)
		resourcePad = MAP_EDGE_MARGIN_WIDTH * 2
		x = (CITIZEN_BAR_WIDTH + (mapFrameSize / 2.0) - (resourcePad / 2.0)) / float(xResolution)
		y = 1.00 - ((CITY_TITLE_BAR_HEIGHT + (mapFrameSize / 2.0) + (titleOverlap / 2.0)) / float(yResolution))
		CyCamera().SetCityViewPortCenter(x, y)

		screen.hide("ClockText")
		screen.hide("DefenseText")
		screen.hide("LibertyText")
		screen.hide("HammerText")
		screen.hide("CrossesText")
		screen.hide("HealthText")
		screen.hide("TotalHappinessText") # CITY HAPPINESS vs UNHAPPINESS
		screen.hide("HappinessText") # CITY HAPPINESS vs UNHAPPINESS
		screen.hide("UnhappinessText") # CITY HAPPINESS vs UNHAPPINESS
		screen.hide("TotalLawText") # CITY LAW vs CRIME
		screen.hide("LawText") # CITY LAW vs CRIME
		screen.hide("CrimeText") # CITY LAW vs CRIME
		screen.hide("EducationText")
		screen.hide("CultureText")
		screen.hide("HarbourText")
		screen.hide("BarracksText")
		screen.hide("CityNameText")
		screen.hide("PopulationText")
		screen.hide("ProductionInputText")

		for iProfession in range(gc.getNumProfessionInfos()):
			if( not gc.getProfessionInfo(iProfession).isCitizen()):
				screen.hide("EjectProfession" + str(iProfession))

	# CITY SCREEN UP
		if (CyInterface().isCityScreenUp()):

			for iYield in EMPHASIZEYIELDS:
				screen.hide("MapYieldBox" + str(iYield))
				screen.hide("MapYieldIcon" + str(iYield))
				screen.hide("MapYieldEmphasize" + str(iYield))
				screen.hide("MapYieldDe-Emphasize" + str(iYield))

			minimapWidth = min(xResolution - MAP_EDGE_MARGIN_WIDTH - CITY_MULTI_TAB_SIZE - CITIZEN_BAR_WIDTH, yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT - (STACK_BAR_HEIGHT *2) - CITY_TITLE_BAR_HEIGHT - CITY_VIEW_BOX_HEIGHT_AND_WIDTH)
			xCenter = (CITIZEN_BAR_WIDTH + MAP_EDGE_MARGIN_WIDTH + xResolution - CITY_MULTI_TAB_SIZE) / 2
			yCenter = (CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH + yResolution - BOTTOM_CENTER_HUD_HEIGHT - TRANSPORT_AREA_HEIGHT - (STACK_BAR_HEIGHT *2)) / 2
			screen.placeMinimap(xCenter - minimapWidth / 2, xCenter + minimapWidth / 2, yCenter - minimapWidth / 2, yCenter + minimapWidth / 2)
			if (pHeadSelectedCity):

				self.updateSelectionButtons()

				for j in range(gc.getMAX_PLOT_LIST_ROWS()):
					for i in range(self.numPlotListButtons()):
						szString = "PlotListButtonMulti" + str(j * self.numPlotListButtons() + i)
						screen.hide( szString )
						screen.hide( szString + "Health")
						screen.hide( szString + "Icon")

				screen.show("ResourceTable")
				#for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				#	screen.show("YieldIcon" + str(iYield))

			# CITY SCROLL BUTTONS
				if (pHeadSelectedCity.getTeam() == gc.getGame().getActiveTeam()):
					if (gc.getActivePlayer().getNumCities() < 2):
						screen.hide("CityScrollMinus")
						screen.hide("CityScrollPlus")

			# CITY NAME HEADER
				szBuffer = u"<font=4>"
				if (pHeadSelectedCity.isCapital()):
					szBuffer += u"%c" %(CyGame().getSymbolID(FontSymbols.STAR_CHAR))
				szBuffer += u"%s: %d" %(pHeadSelectedCity.getName(), pHeadSelectedCity.getPopulation())
				if (pHeadSelectedCity.isOccupation()):
					szBuffer += u" (%c:%d)" %(CyGame().getSymbolID(FontSymbols.OCCUPATION_CHAR), pHeadSelectedCity.getOccupationTimer())
				# Robert Surcouf, moved VET NewCapacity

				szBuffer += u"</font>"

				localText.changeTextColor(szBuffer, ColorTypes.COLOR_FONT_CREAM)
				screen.setText("CityNameText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution / 2 , CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_CITY_NAME, -1, -1 )

			# POPULATION GROWTH/STARVATION TEXT
				iFoodDifference = pHeadSelectedCity.foodDifference()
				iProductionDiffNoFood = pHeadSelectedCity.getCurrentProductionDifference(True)
				iProductionDiffJustFood = 0
				szBuffer = u"<font=3>"
				if (iFoodDifference > 0):
					szBuffer = localText.getText("INTERFACE_CITY_GROWING", (pHeadSelectedCity.getFoodTurnsLeft(), ))
				elif (iFoodDifference < 0):
					szBuffer = localText.getText("INTERFACE_CITY_STARVING", ())
				else:
					szBuffer = localText.getText("INTERFACE_CITY_STAGNANT", ())
				szBuffer += u"</font>"
				screen.setText("PopulationText", "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution * 4 / 100, CITY_TITLE_BAR_HEIGHT / 8, -0.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_POPULATION, -1, -1 )
				screen.setStyle("PopulationText", "Button_Stone_Style")

			# CURRENT PRODUCTION BAR FILL
				fProductionNeeded = float(pHeadSelectedCity.getProductionNeeded(YieldTypes.YIELD_HAMMERS))
				if (fProductionNeeded > 0):
					iFirst = ((float(pHeadSelectedCity.getProduction())) / fProductionNeeded)
					screen.setBarPercentage("CityProductionBar", InfoBarTypes.INFOBAR_STORED, iFirst )
					if ( iFirst == 1 ):
						iSecond = (((float(iProductionDiffNoFood)) / fProductionNeeded) )
					else:
						iSecond = (((float(iProductionDiffNoFood)) / fProductionNeeded) ) / ( 1 - iFirst )
					screen.setBarPercentage("CityProductionBar", InfoBarTypes.INFOBAR_RATE, iSecond )
					if ( iFirst + iSecond == 1 ):
						screen.setBarPercentage("CityProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, (((float(iProductionDiffJustFood)) / fProductionNeeded) ) )
					else:
						screen.setBarPercentage("CityProductionBar", InfoBarTypes.INFOBAR_RATE_EXTRA, (( ((float(iProductionDiffJustFood)) / fProductionNeeded) ) ) / ( 1 - ( iFirst + iSecond ) ) )

			# CURRENT PRODUCTION BAR TEXT
				if (pHeadSelectedCity.isProductionBuilding() or pHeadSelectedCity.isProductionUnit()):
					szBuffer = localText.getText("INTERFACE_CITY_PRODUCTION", (pHeadSelectedCity.getProductionNameKey(), pHeadSelectedCity.getProductionTurnsLeft()))
				elif pHeadSelectedCity.isProduction():
					szBuffer = pHeadSelectedCity.getProductionName()
				else:
					szBuffer = u""

			# YIELD REQUIREMENT INFO
				szYieldSymbols = u""
				for iYield in range(YieldTypes.NUM_YIELD_TYPES):
					if iYield != YieldTypes.YIELD_HAMMERS:
						if (CyInterface().getOrderNodeType(0) == OrderTypes.ORDER_TRAIN ):
							iYieldRequired = gc.getPlayer(pHeadSelectedCity.getOwner()).getUnitYieldProductionNeeded(CyInterface().getOrderNodeData1(0), iYield)
						elif (CyInterface().getOrderNodeType(0) == OrderTypes.ORDER_CONSTRUCT):
							iYieldRequired = gc.getPlayer(pHeadSelectedCity.getOwner()).getBuildingYieldProductionNeeded(CyInterface().getOrderNodeData1(0), iYield)
						else:
							iYieldRequired = 0

						iYieldStored = pHeadSelectedCity.getYieldStored(iYield) + pHeadSelectedCity.getYieldRushed(iYield)
						if (iYieldRequired > iYieldStored):
							if (len(szYieldSymbols) > 0):
								szYieldSymbols += u","
							szYieldSymbols += u"% i%c" % (iYieldRequired - iYieldStored, gc.getYieldInfo(iYield).getChar())

				if len(szYieldSymbols) > 0:
					screen.setStackedBarColors("CityProductionBar", InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_RED)
					screen.setStackedBarColors("CityProductionBar", InfoBarTypes.INFOBAR_RATE, ColorTypes.COLOR_WARNING_RATE)
					szBuffer += u" " + localText.getText("TXT_KEY_PEDIA_REQUIRES", ()) + szYieldSymbols
				else:
					screen.setStackedBarColors("CityProductionBar", InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_GREAT_PEOPLE_STORED)
					screen.setStackedBarColors("CityProductionBar", InfoBarTypes.INFOBAR_RATE, ColorTypes.COLOR_GREAT_PEOPLE_RATE)
#TAC --->
				xPostionProductionBar = (xResolution - CITIZEN_BAR_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 3) - (SMALL_BUTTON_SIZE * 4) + 5) / 2
				screen.setLabelAt("ProductionText", "CityProductionBar", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xPostionProductionBar, STACK_BAR_HEIGHT / 2, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_HELP_SELECTED, 0, -1 )
#<--- TAC
			# 3 D BUILDINGS
				for iSpecial in range(gc.getNumSpecialBuildingInfos()):
					BuildingPresent = False
					for iBuilding in range(gc.getNumBuildingInfos()):
						if (pHeadSelectedCity.isHasBuilding(iBuilding)):
							if(gc.getBuildingInfo(iBuilding).getSpecialBuildingType() == iSpecial):
								BuildingPresent = True
								break

					if (BuildingPresent):
						Texture = gc.getBuildingInfo(iBuilding).getArtInfo().getCityTexture()
						screen.changeImageButton("CityBuildingGraphic" + str(iSpecial), gc.getBuildingInfo(iBuilding).getArtInfo().getCityTexture())
						screen.show("CityBuildingGraphic" + str(iSpecial))
					else:
						#screen.hide("CityBuildingGraphic" + str(iSpecial))
						szTexture = gc.getSpecialBuildingInfo(iSpecial).getNatureObject()
						screen.changeImageButton("CityBuildingGraphic" + str(iSpecial), szTexture)
						screen.show("CityBuildingGraphic" + str(iSpecial))

				# More or less: 1024 -> 5% 1280 -> 4% / 1600 -> 2% / 1980 -> 0%
				iXmodifier = max(xResolution * 5 / 100 - (xResolution - 1000)/200 , 0)

			# CITIY DEFENSE MODIFIER
				iDefenseModifier = pHeadSelectedCity.getDefenseModifier()
				if (iDefenseModifier != 0):
					szBuffer = u"+%s%%%c" % (str(iDefenseModifier), CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR))  #localText.getText("TXT_KEY_MAIN_CITY_DEFENSE", (CyGame().getSymbolID(FontSymbols.DEFENSE_CHAR), iDefenseModifier))
					if (pHeadSelectedCity.getDefenseDamage() > 0):
						szTempBuffer = u" (%d%%)" %(( ( gc.getMAX_CITY_DEFENSE_DAMAGE() - pHeadSelectedCity.getDefenseDamage() ) * 100 ) / gc.getMAX_CITY_DEFENSE_DAMAGE() )
						szBuffer = szBuffer + szTempBuffer
					szBuffer = "<font=3>" + szBuffer + "</font>"
					screen.setLabel("DefenseText", "Background", szBuffer, CvUtil.FONT_RIGHT_JUSTIFY, xResolution * 89 / 100 -iXmodifier , CITY_TITLE_BAR_HEIGHT / 8, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_DEFENSE, -1, -1 )
					screen.show("DefenseText")

			# CITY HAMMER PRODUCTION
				iHammers = pHeadSelectedCity.getCurrentProductionDifference(True)
				szBuffer = u"<font=3>" + u"%i%c" % (iHammers, gc.getYieldInfo(YieldTypes.YIELD_HAMMERS).getChar()) + u"</font>"
				screen.setLabel("HammerText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 11 / 100 +iXmodifier , CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_PRODUCTION_MOD_HELP, -1, -1 )

				netYields = list(pHeadSelectedCity.calculateNetYieldList())
			# CITY LIBERTYBELL PRODUCTION
				iLiberty = netYields[YieldTypes.YIELD_BELLS]
				szBuffer = u"<font=3>" + u"%i%c" % (iLiberty, gc.getYieldInfo(YieldTypes.YIELD_BELLS).getChar()) + u"</font>"
				screen.setLabel("LibertyText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 14 / 100 +iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_YIELD, YieldTypes.YIELD_BELLS, -1 )

			# CITY CROSS PRODUCTION
				iCrosses = netYields[YieldTypes.YIELD_CROSSES]
				szBuffer = u"<font=3>" + u"%i%c" % (iCrosses, gc.getYieldInfo(YieldTypes.YIELD_CROSSES).getChar()) + u"</font>"
				screen.setLabel("CrossesText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 17 / 100 +iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_YIELD, YieldTypes.YIELD_CROSSES, -1 )

			# CITY EDUCATION PRODUCTION
				iBooks = netYields[YieldTypes.YIELD_EDUCATION]
				szBuffer = u"<font=3>" + u"%i%c" % (iBooks, gc.getYieldInfo(YieldTypes.YIELD_EDUCATION).getChar()) + u"</font>"
				screen.setLabel("EducationText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 20 / 100 +iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_YIELD, YieldTypes.YIELD_EDUCATION, -1 )

			# CITY Culture PRODUCTION
				iCulture = pHeadSelectedCity.getCultureRate() # RaR, ray, small correction
				szBuffer = u"<font=3>" + u"%i%c" % (iCulture, gc.getYieldInfo(YieldTypes.YIELD_CULTURE).getChar()) + u"</font>"
				screen.setLabel("CultureText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 23 / 100 +iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_YIELD, YieldTypes.YIELD_CULTURE, -1 )

			# CITY HEALTH PRODUCTION
				#get the coloured string for current City Health
				iHealth = pHeadSelectedCity.getCityHealth()
				szBufferCurrentHealth = u"<font=3>" + u"<color="
				if iHealth > 0: # Green
					szBufferCurrentHealth += u"0,255,0" + u">" +str(iHealth) + u"</color>" + u"</font>"
				elif iHealth < 0: # Red
					szBufferCurrentHealth += u"255,0,0" + u">" + str(iHealth) + u"</color>" + u"</font>"
				else: # Yellow
					szBufferCurrentHealth += u"255,255,0" + u">" + str(iHealth) + u"</color>" + u"</font>"

				#get the coloured string for change of City Health
				iHealthChange = pHeadSelectedCity.getCityHealthChange()
				szBufferHealthChange = u"<font=3>" + u"<color="
				if iHealthChange > 0: # Green
					#not enough space for a + sign
					#szBufferHealthChange += u"0,255,0" + u">(+"+str(iHealthChange)+u")" + u"</color>" + u"</font>"
					szBufferHealthChange += u"0,255,0" + u">("+str(iHealthChange)+u")" + u"</color>" + u"</font>"
				elif iHealthChange < 0: # Red
					szBufferHealthChange += u"255,0,0" + u">("+str(iHealthChange)+u")" + u"</color>" + u"</font>"
				else: # Yellow
					szBufferHealthChange += u"255,255,0" + u">("+str(iHealthChange)+u")" + u"</color>" + u"</font>"

				#get the Health Icon String
				szBufferHealthIcon = u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_HEALTH).getChar()) + u"</font>"

				#now add them all together and display on top of the Screen
				szBuffer = szBufferCurrentHealth + szBufferHealthChange +szBufferHealthIcon
				screen.setLabel("HealthText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 68 / 100 +iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_YIELD, YieldTypes.YIELD_HEALTH, -1 )

			# CITY HAPPINESS vs UNHAPPINESS
				pHeadSelectedCity.updateCityHappiness()
				pHeadSelectedCity.updateCityUnHappiness()
				iHappiness = pHeadSelectedCity.getCityHappiness()
				iUnhappiness = pHeadSelectedCity.getCityUnHappiness()

				if iHappiness > iUnhappiness: # Green and we use Icon Happiness
					iTotalHap = iHappiness - iUnhappiness
					szBufferTotal = u"<font=3>" + u"<color="u"0,255,0" + u">"+str(iTotalHap) + u"</color>" + u"</font>"
					szBufferTotal += u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_HAPPINESS).getChar()) + u"</font>"
					szBufferTotal += u"<font=3>" + u"=" + u"</font>"
					screen.setLabel("TotalHappinessText", "Background", szBufferTotal, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 69 / 100 -iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, HELP_TOTAL_HAPPINESS_POSITIVE, -1 )
				elif iUnhappiness > iHappiness: # Red and we use Icon Unhappiness
					iTotalUnhap = iUnhappiness - iHappiness
					szBufferTotal = u"<font=3>" + u"<color="u"255,0,0" + u">"+str(iTotalUnhap) + u"</color>" + u"</font>"
					szBufferTotal += u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_UNHAPPINESS).getChar()) + u"</font>"
					szBufferTotal += u"<font=3>" + u"=" + u"</font>"
					screen.setLabel("TotalHappinessText", "Background", szBufferTotal, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 69 / 100-iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, HELP_TOTAL_HAPPINESS_NEGATIVE, -1 )
				else: # Yellow and we use Icon Happiness
					iTotalZeroHap = 0
					szBufferTotal = u"<font=3>" + u"<color="u"255,255,0" + u">" + str(iTotalZeroHap) + u"</color>" + u"</font>"
					szBufferTotal += u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_HAPPINESS).getChar()) + u"</font>"
					szBufferTotal += u"<font=3>" + u"=" + u"</font>"
					screen.setLabel("TotalHappinessText", "Background", szBufferTotal, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 69 / 100-iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, HELP_TOTAL_HAPPINESS_ZERO, -1 )

				szBufferHappiness = u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_HAPPINESS).getChar()) + u"</font>"
				szBufferHappiness += u"<font=3>" + u"-" + u"</font>"
				screen.setLabel("HappinessText", "Background", szBufferHappiness, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 72 / 100-iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_YIELD, YieldTypes.YIELD_HAPPINESS, -1 )

				szBufferUnHappiness = u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_UNHAPPINESS).getChar()) + u" </font>"
				screen.setLabel("UnhappinessText", "Background", szBufferUnHappiness, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 74 / 100-iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_YIELD, YieldTypes.YIELD_UNHAPPINESS, -1 )

			# CITY LAW vs CRIME
				pHeadSelectedCity.updateCityLaw()
				pHeadSelectedCity.updateCityCrime()
				iLaw = pHeadSelectedCity.getCityLaw()
				iCrime = pHeadSelectedCity.getCityCrime()

				if iLaw > iCrime: # Green and we use LAW Icon
					iTotalLaw = iLaw - iCrime
					szBufferTotal = u"<font=3>" + u"<color="u"0,255,0" + u">"+str(iTotalLaw) + u"</color>" + u"</font>"
					szBufferTotal += u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_LAW).getChar()) + u"</font>"
					szBufferTotal += u"<font=3>" + u"=" + u"</font>"
					screen.setLabel("TotalLawText", "Background", szBufferTotal, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 37 / 100 -iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, HELP_TOTAL_LAW_POSITIVE, -1 )
				elif iCrime > iLaw: # Red and we use CRIME Icon
					iTotalCrime = iCrime - iLaw
					szBufferTotal = u"<font=3>" + u"<color="u"255,0,0" + u">"+str(iTotalCrime) + u"</color>" + u"</font>"
					szBufferTotal += u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_CRIME).getChar()) + u"</font>"
					szBufferTotal += u"<font=3>" + u"=" + u"</font>"
					screen.setLabel("TotalLawText", "Background", szBufferTotal, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 37 / 100-iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, HELP_TOTAL_LAW_NEGATIVE, -1 )
				else: # Yellow and we use LAW Icon
					iTotalZeroLaw = 0
					szBufferTotal = u"<font=3>" + u"<color="u"255,255,0" + u">" + str(iTotalZeroLaw) + u"</color>" + u"</font>"
					szBufferTotal += u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_LAW).getChar()) + u"</font>"
					szBufferTotal += u"<font=3>" + u"=" + u"</font>"
					screen.setLabel("TotalLawText", "Background", szBufferTotal, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 37 / 100-iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, HELP_TOTAL_LAW_ZERO, -1 )

				szBufferLaw = u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_LAW).getChar()) + u"</font>"
				szBufferLaw += u"<font=3>" + u"-" + u"</font>"
				screen.setLabel("LawText", "Background", szBufferLaw, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 40 / 100-iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_YIELD, YieldTypes.YIELD_LAW, -1 )

				szBufferCrime = u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_CRIME).getChar()) + u" </font>"
				screen.setLabel("CrimeText", "Background", szBufferCrime, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 42 / 100-iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_YIELD, YieldTypes.YIELD_CRIME, -1 )

			# WTP, ray, new Harbour System - START
				if (pHeadSelectedCity.bShouldShowCityHarbourSystem()):

					iMaxHarbourSpace = pHeadSelectedCity.getCityHarbourSpace()
					iUsedHarbourSpace = pHeadSelectedCity.getCityHarbourSpaceUsed()
					iHalfMaxHarbourSpace = (iMaxHarbourSpace / 2)

					#green: less than 50 percent of the harbour space is full
					# we remove the numbers and put them in Mouse over to save space
					# careful, 2nd line of buffer now "=" instead "+="
					if (iUsedHarbourSpace <= iHalfMaxHarbourSpace):
						#szBuffer = u"<font=3>" + u" <color="u"0,255,0" + u">"+ str(iUsedHarbourSpace) + u"(" + str(iMaxHarbourSpace) + u")" + u"</color>" + u"</font>"
						szBuffer = u"<font=3>" + (u" %c" % CyGame().getSymbolID(FontSymbols.ANCHOR_CHAR)) + "</font>"
						screen.setLabel("HarbourText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 81 / 100 -iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_HARBOUR_SYSTEM, NEW_HARBOUR_SYSTEM, -1 )

					# red: the harbour is completely full
					elif (iUsedHarbourSpace >= iMaxHarbourSpace):
						#szBuffer = u"<font=3>" + u" <color="u"255,0,0" + u">"+ str(iUsedHarbourSpace) + u"(" + str(iMaxHarbourSpace) + u")" + u"</color>" + u"</font>"
						szBuffer = u"<font=3>" + (u" %c" % CyGame().getSymbolID(FontSymbols.NO_ANCHOR_CHAR)) + "</font>"
						screen.setLabel("HarbourText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 81 / 100 -iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_HARBOUR_SYSTEM, NEW_HARBOUR_SYSTEM, -1 )

					# yellow: more than half is full, but not completely
					else:
						#szBuffer = u"<font=3>" + u" <color="u"255,255,0" + u">" + str(iUsedHarbourSpace) + u"(" + str(iMaxHarbourSpace) + u")" + u"</color>" + u"</font>"
						szBuffer = u"<font=3>" + (u" %c" % CyGame().getSymbolID(FontSymbols.ANCHOR_CHAR)) + "</font>"
						screen.setLabel("HarbourText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 81 / 100 -iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_HARBOUR_SYSTEM, NEW_HARBOUR_SYSTEM, -1 )

			# WTP, ray, new Barracks System - START
				if (pHeadSelectedCity.bShouldShowCityBarracksSystem()):

					iMaxBarracksSpace = pHeadSelectedCity.getCityBarracksSpace()
					iUsedBarracksSpace = pHeadSelectedCity.getCityBarracksSpaceUsed()
					iHalfMaxBarracksSpace = (iMaxBarracksSpace / 2)

					#green: less than 50 percent of the barracks space is full
					# we remove the numbers and put them in Mouse over to save space
					# careful, 2nd line of buffer now "=" instead "+="
					if (iUsedBarracksSpace <= iHalfMaxBarracksSpace):
						#szBuffer = u"<font=3>" + u" <color="u"0,255,0" + u">"+ str(iUsedBarracksSpace) + u"(" + str(iMaxBarracksSpace) + u")" + u"</color>" + u"</font>"
						szBuffer = u"<font=3>" + (u" %c" % CyGame().getSymbolID(FontSymbols.BARRACKS_CHAR)) + "</font>"
						screen.setLabel("BarracksText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 83 / 100 -iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_BARRACKS_SYSTEM, NEW_BARRACKS_SYSTEM, -1 )

					# red: the barracks are completely full
					elif (iUsedBarracksSpace >= iMaxBarracksSpace):
						#szBuffer = u"<font=3>" + u" <color="u"255,0,0" + u">"+ str(iUsedBarracksSpace) + u"(" + str(iMaxBarracksSpace) + u")" + u"</color>" + u"</font>"
						szBuffer = u"<font=3>" + (u" %c" % CyGame().getSymbolID(FontSymbols.NO_BARRACKS_CHAR)) + "</font>"
						screen.setLabel("BarracksText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 83 / 100 -iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_BARRACKS_SYSTEM, NEW_BARRACKS_SYSTEM, -1 )

					# yellow: more than half is full, but not completely
					else:
						#szBuffer = u"<font=3>" + u" <color="u"255,255,0" + u">" + str(iUsedBarracksSpace) + u"(" + str(iMaxBarracksSpace) + u")" + u"</color>" + u"</font>"
						szBuffer = u"<font=3>" + (u" %c" % CyGame().getSymbolID(FontSymbols.BARRACKS_CHAR)) + "</font>"
						screen.setLabel("BarracksText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 83 / 100 -iXmodifier, CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_HELP_BARRACKS_SYSTEM, NEW_BARRACKS_SYSTEM, -1 )

			# REBEL BAR FILL PERCENTAGE
				fPercentage = float(pHeadSelectedCity.getRebelPercent() / 100.0)
				screen.setBarPercentage("RebelBar", InfoBarTypes.INFOBAR_STORED, fPercentage)

			# REBEL BAR TEXT
				iRebel = pHeadSelectedCity.getRebelPercent()
				szBuffer = localText.getText("TXT_KEY_MISC_REBEL", (iRebel, ))
				screen.setLabelAt("RebelText", "RebelBar", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, (CITIZEN_BAR_WIDTH - (STACK_BAR_HEIGHT * 3 / 2)) / 2, STACK_BAR_HEIGHT / 2, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
				screen.setHitTest("RebelText", HitTestTypes.HITTEST_NOHIT)
				screen.show("RebelText")

			# PRODUCTION
				szBuffer = u"<font=3>"
				aiProducedYields = [[]] * YieldTypes.NUM_YIELD_TYPES
				for iYield in range(YieldTypes.NUM_YIELD_TYPES):
					aiProducedYields[iYield] = 0

				#iTotalYield = 0
				for iYield in range(YieldTypes.NUM_YIELD_TYPES):
					iUnproducedYield = pHeadSelectedCity.calculateActualYieldProduced(iYield) - pHeadSelectedCity.getBaseRawYieldProduced(iYield)
					if iUnproducedYield < 0:
						for iProfession in range(gc.getNumProfessionInfos()):
							if gc.getProfessionInfo(iProfession).getYieldsProduced(0) == iYield: #MultipleYieldsProduced Start
								iNeedYield = gc.getProfessionInfo(iProfession).getYieldsConsumed(0) #MultipleYieldsProduced Start
								aiProducedYields[iNeedYield] += iUnproducedYield
					iProducedYield = netYields[iYield]
					aiProducedYields[iYield] += iProducedYield

				iProdusedYield = 0
				for iYield in range(YieldTypes.NUM_YIELD_TYPES):
					if (not gc.getYieldInfo(iYield).isIgnoredForStorageCapacity() and gc.getYieldInfo(iYield).isCargo()):
						iProdusedYield += aiProducedYields[iYield]

				szBuffer += u" <color="
				iMaxYield = pHeadSelectedCity.getMaxYieldCapacity()
				iTotalYield = pHeadSelectedCity.getTotalYieldStored()
				if iTotalYield + iProdusedYield > iMaxYield:
					szBuffer += u"255,0,0"
				elif iTotalYield + (2 * iProdusedYield) > iMaxYield:
					szBuffer += u"255,255,0"
				else:
					szBuffer += u"0,255,0"
				szBuffer +=  u">("
				szBuffer += str(iTotalYield)
				if iProdusedYield > 0:
					szBuffer += u"+" + str(iProdusedYield)
				elif iProdusedYield < 0:
					szBuffer += str(iProdusedYield)
				szBuffer += u"/" + str(iMaxYield) + u")"
				szBuffer += u"</font>"

				# WTP, ray, adding the Yield Icon for Trade Goods to Storage Capacity
				szBuffer += u"<font=3>" + u"%c" % (gc.getYieldInfo(YieldTypes.YIELD_TRADE_GOODS).getChar()) + u"</font>"
				screen.setLabel("StorageCapacityText", "Background", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, xResolution * 90 / 100 , CITY_TITLE_BAR_HEIGHT / 12, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, VET_NEW_CAPACITY, -1 )

			screen.hide("TimeText")
			screen.hide("GoldText")

		else: # CITY SCREEN IS DOWN
			self.MINIMAP_SIDE_MARGIN = MINIMAP_HEIGHT * 13 / 100
			screen.placeMinimap(self.MINIMAP_SIDE_MARGIN, MINIMAP_HEIGHT - self.MINIMAP_SIDE_MARGIN, yResolution - MINIMAP_HEIGHT + self.MINIMAP_SIDE_MARGIN * 2, yResolution)
			self.setGameHelpArea(screen, yResolution - SADDLE_HEIGHT+HELPTEXT_AREA_Y_MARGIN)

			if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
				self.setMinimapButtonVisibility(True)
				pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())

				screen.hide("ResourceTable")
				for iYield in range(YieldTypes.NUM_YIELD_TYPES):
					screen.hide("YieldIcon" + str(iYield))
					screen.hide("YieldStoredlabel" + str(iYield))
					screen.hide("YieldNetlabel" + str(iYield))

				screen.hide("LibertyText")
				screen.hide("CrossesText")
				screen.hide("HealthText")
				screen.hide("TotalHappinessText") # CITY HAPPINESS vs UNHAPPINESS
				screen.hide("HappinessText") # CITY HAPPINESS vs UNHAPPINESS
				screen.hide("UnhappinessText") # CITY HAPPINESS vs UNHAPPINESS
				screen.hide("TotalLawText") # CITY LAW vs CRIME
				screen.hide("LawText") # CITY LAW vs CRIME
				screen.hide("CrimeText") # CITY LAW vs CRIME
				screen.hide("HammerText")
				screen.hide("EducationText")
				screen.hide("CultureText")
				screen.hide("HarbourText")
				screen.hide("BarracksText")
				screen.hide("StorageCapacityText")

			for iSpecial in range(gc.getNumSpecialBuildingInfos()):
				screen.hide("CityBuildingGraphic" + str(iSpecial))
				screen.hide("ProductionBox" + str(iSpecial))

			screen.hideList(RESOURCE_TABLE_HIDE)
			screen.hide("CityList")

		return 0

	# Will set the table to display the out put of a city or the players whole empire
	def updateResourceTable( self ):

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
		ResourceHideList = []

		if not CyInterface().isCityScreenUp():
			screen.hideList(RESOURCE_TABLE_HIDE)
			return


		xDelta = 0
		ixDelta = 0
		iDelta = 0
		yDelta = CyInterface().determineWidth(self.setFontSize(u"0", 0)) * 3 / 2
		iK1 = 2
		iMax = (xResolution * 2) / (yResolution * 33)
		iNum = len(self.TableYields)
		if iNum > iMax:
			if iNum % 3 == 1:
				iNum += 1
			iNum /= 3
			RESOURCE_TABLE_COLUMN_WIDTH = (xResolution - STACK_BAR_HEIGHT) / iNum
			iK1 = 1
			if len(self.TableYields) % 3 == 1:
				ixDelta = RESOURCE_TABLE_COLUMN_WIDTH / 2

		pCity = CyInterface().getHeadSelectedCity()
		if pCity != None:
			netYields = list(pCity.calculateNetYieldList())
			for index in range(len(self.TableYields)):
				if index >= 2 * iNum:
					xDelta = ixDelta
					iDelta = iNum * 2
					iK1 = 3
				elif index >= iNum:
					xDelta = ixDelta
					iDelta = iNum
					iK1 = 2

				i = self.TableYields[index]
				iStored = pCity.getYieldStored(i)
				iRate = netYields[i]
				bIgnoredForStorageCapacity = gc.getYieldInfo(i).isIgnoredForStorageCapacity()
				szStored = ""
				if (iStored > pCity.getMaxYieldCapacity() and not bIgnoredForStorageCapacity):
					szStored = u"<color=255,0,0>%d</color>" %(iStored)
				else:
					if iStored == 0:
						szStored = u""
					else:
						szStored = u"<color=0,255,255>%d</color>" %(iStored)
				szRate = u"%d" %(iRate)
				if(iRate > 0):
					szRate = u"<color=0,255,0>+" + szRate + u"</color>"
				if(iRate == 0):
					szRate = u""
				if(iRate < 0):
					szRate = u"<color=255,255,0>" + szRate + u"</color>"

				szStorageLabel = "YieldStoredlabel" + str(i)
				iX = STACK_BAR_HEIGHT + ((index - iDelta) * RESOURCE_TABLE_COLUMN_WIDTH) + (RESOURCE_TABLE_COLUMN_WIDTH / 2) + xDelta
				iY = yResolution - BOTTOM_CENTER_HUD_HEIGHT / iK1 + self.iIconWidth - yResolution / 25
				# WTP, ray, 3 rows
				if (iK1 == 2):
					iY = yResolution - (2 * BOTTOM_CENTER_HUD_HEIGHT / 3) + self.iIconWidth - yResolution / 25
				elif (iK1 == 3):
					iY = yResolution - BOTTOM_CENTER_HUD_HEIGHT / 3 + self.iIconWidth - yResolution / 25
				screen.setLabel(szStorageLabel, "", self.setFontSize(szStored, 0), CvUtil.FONT_CENTER_JUSTIFY, iX, iY, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )
				ResourceHideList.append(szStorageLabel)
				szRateLabel = "YieldNetlabel" + str(i)
				iY += yDelta
				screen.setLabel(szRateLabel, "", self.setFontSize(szRate, 0), CvUtil.FONT_CENTER_JUSTIFY, iX, iY, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_RECEIVE_MOVE_CARGO_TO_CITY, -1, -1 )
				ResourceHideList.append(szRateLabel)

				if SHOW_ALL_YIELDS == False and iStored == 0 and iRate == 0:
					screen.hide("YieldIcon" + str(index))
				else:
					screen.show("YieldIcon" + str(index))

			# The stuff below does not depend on the yield index so they were moved out of the loop above
			# REBEL BAR FILL PERCENTAGE
			fPercentage = float(pCity.getRebelPercent() / 100.0)
			screen.setBarPercentage("RebelBar", InfoBarTypes.INFOBAR_STORED, fPercentage)

			# REBEL BAR TEXT
			iRebel = pCity.getRebelPercent()
			szBuffer = localText.getText("TXT_KEY_MISC_REBEL", (iRebel, ))
			screen.setLabelAt("RebelText", "RebelBar", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, (CITIZEN_BAR_WIDTH - (STACK_BAR_HEIGHT * 3 / 2)) / 2, STACK_BAR_HEIGHT / 2, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
			screen.setHitTest("RebelText", HitTestTypes.HITTEST_NOHIT)
			screen.show("RebelText")

			# GOLD
			screen.hide("TimeText")
			screen.hide("GoldText")
			screen.registerHideList(ResourceHideList, len(ResourceHideList), RESOURCE_TABLE_HIDE)

		# EMPHISIZE DISPLAY
			for i in range(YieldTypes.NUM_YIELD_TYPES):
				if pCity.AI_getEmphasizeYieldCount(i) > 0:
					screen.hide("BonusPane" + str(i))
					screen.show("BonusPanePos" + str(i))
					screen.hide("BonusPaneNeg" + str(i))
				elif pCity.AI_getEmphasizeYieldCount(i) < 0:
					screen.hide("BonusPane" + str(i))
					screen.hide("BonusPanePos" + str(i))
					screen.show("BonusPaneNeg" + str(i))
				else:
					screen.show("BonusPane" + str(i))
					screen.hide("BonusPanePos" + str(i))
					screen.hide("BonusPaneNeg" + str(i))

			if pCity.AI_isEmphasize(AVOID_GROWTH):
				screen.overlayButtonGFC("AvoidGrowth", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
			else:
				screen.overlayButtonGFC("AvoidGrowth", None)

	# Will update the info pane strings
	def updateInfoPaneStrings( self ):

		iRow = 0
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pHeadSelectedUnit = CyInterface().getHeadSelectedUnit()

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		bShift = CyInterface().shiftKey()

		self.SELECTION_PALEL_HEIGHT = LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT - (LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT / 10)
		self.SELECTION_PANEL_ROW_HEIGHT = self.SELECTION_PALEL_HEIGHT / 3
		self.SELECTION_PALEL_LEFT_COLUMN_WIDTH = 60

		screen.addPanel("SelectedUnitPanel", u"", u"", True, False, xResolution - LOWER_RIGHT_CORNER_BACKGROUND_WIDTH, yResolution - LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT, LOWER_RIGHT_CORNER_BACKGROUND_WIDTH, LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT - (LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT / 10), PanelStyles.PANEL_STYLE_EMPTY, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.hide("SelectedUnitPanel")

		bUnitHasPromotions = False

		if pHeadSelectedUnit != None:
			if pHeadSelectedUnit.getProfession() != ProfessionTypes.NO_PROFESSION:
				for i in range(gc.getNumPromotionInfos()):
					if (pHeadSelectedUnit.isHasPromotion(i) and not gc.getPromotionInfo(i).isGraphicalOnly()):
						bUnitHasPromotions = True
						break

		if bUnitHasPromotions:
			iHeight = (yResolution / 45)
		else:
			iHeight = (yResolution / 33) - 1

		screen.addTableControlGFC("SelectedUnitName", 1, xResolution - LOWER_RIGHT_CORNER_BACKGROUND_WIDTH * 105 / 100, yResolution - LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT, LOWER_RIGHT_CORNER_BACKGROUND_WIDTH * 105 / 100 + 5, iHeight, False, False, self.SELECTION_PANEL_ROW_HEIGHT, self.SELECTION_PANEL_ROW_HEIGHT, TableStyles.TABLE_STYLE_STANDARD)
		screen.setStyle("SelectedUnitName", "Table_EmptyScroll_Style")
		screen.hide("SelectedUnitName")

		screen.addTableControlGFC("SelectedUnitText", 3, xResolution - LOWER_RIGHT_CORNER_BACKGROUND_WIDTH * 105 / 100, yResolution - LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT + iHeight, LOWER_RIGHT_CORNER_BACKGROUND_WIDTH * 105 / 100 + 5, LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT - (LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT / 10), False, False, self.SELECTION_PANEL_ROW_HEIGHT, self.SELECTION_PANEL_ROW_HEIGHT, TableStyles.TABLE_STYLE_STANDARD)
		screen.setStyle("SelectedUnitText", "Table_EmptyScroll_Style")
		screen.hide("SelectedUnitText")
		screen.hide("SelectedUnitLabel")

		QueueWidth = (xResolution - CITIZEN_BAR_WIDTH) * 3 / 7
		screen.addTableControlGFC("CityBuildQueue", 2, CITIZEN_BAR_WIDTH + 5, CITY_TITLE_BAR_HEIGHT + CITY_VIEW_BOX_HEIGHT_AND_WIDTH - (MAP_EDGE_MARGIN_WIDTH * 2) + (STACK_BAR_HEIGHT * 3 / 2) + (MAP_EDGE_MARGIN_WIDTH / 2) - (CITY_MULTI_TAB_SIZE / 2) - ((CITY_MULTI_TAB_SIZE * 130 / 100) / 2) + (CITY_MULTI_TAB_SIZE / 2) - (STACK_BAR_HEIGHT / 2) + CITY_MULTI_TAB_SIZE * 130 / 100, QueueWidth, TRANSPORT_AREA_HEIGHT - (STACK_BAR_HEIGHT * 2) - SMALL_BUTTON_SIZE * 3 / 2 + 5, False, False, self.SELECTION_PANEL_ROW_HEIGHT, self.SELECTION_PANEL_ROW_HEIGHT, TableStyles.TABLE_STYLE_STANDARD)
		screen.setStyle("CityBuildQueue", "Table_EmptyScroll_Style")
		screen.hide("CityBuildQueue")

	# UNIT HEALTH BAR
		if (pHeadSelectedUnit and pHeadSelectedUnit.getUnitTravelState() == UnitTravelStates.NO_UNIT_TRAVEL_STATE and not pHeadSelectedCity and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW and not CyEngine().isGlobeviewUp()):
			fPercentage = 1 - float(pHeadSelectedUnit.getDamage() / 100.0)
			screen.setBarPercentage("UnitHealthBar", InfoBarTypes.INFOBAR_STORED, fPercentage)
			if (fPercentage >= .666):
				screen.setStackedBarColors("UnitHealthBar", InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_GREEN)
			elif (fPercentage >= .333):
				screen.setStackedBarColors("UnitHealthBar", InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_YELLOW)
			else:
				screen.setStackedBarColors("UnitHealthBar", InfoBarTypes.INFOBAR_STORED, ColorTypes.COLOR_RED)
			screen.show("UnitHealthBar")
		else:
			screen.hide("UnitHealthBar")

		if (CyEngine().isGlobeviewUp() or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL):
			screen.hide("TimeText")
			screen.hide("GoldText")
			for iYield in EMPHASIZEYIELDS:
				screen.hide("MapYieldBox" + str(iYield))
				screen.hide("MapYieldIcon" + str(iYield))
				screen.hide("MapYieldEmphasize" + str(iYield))
				screen.hide("MapYieldDe-Emphasize" + str(iYield))

			screen.hide("MapBuildingSelectionMultiList")
			screen.hide("MapCityProductionBar")
			screen.hide("MapCityBuildQueue")
			screen.hide("MapCityLeftPanelShadow")
			screen.hide("MapCityRightPanelShadow")

			return
		else:
			screen.show("TimeText")
			screen.show("GoldText")
			screen.setTableColumnHeader("CityBuildQueue", 0, u"", QueueWidth - (QueueWidth * 3 / 10))
			screen.setTableColumnHeader("CityBuildQueue", 1, u"", QueueWidth * 3 / 10)

		if (pHeadSelectedCity):
			iOrders = CyInterface().getNumOrdersQueued()
			for i in range(iOrders):
				if (not i == 0):

					szLeftBuffer = u""
					szRightBuffer = u""

					if ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_TRAIN ):
						szLeftBuffer = gc.getUnitInfo(CyInterface().getOrderNodeData1(i)).getDescription()
						szRightBuffer = str(pHeadSelectedCity.getUnitProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i))

						if (CyInterface().getOrderNodeSave(i)):
							szLeftBuffer = u"*" + szLeftBuffer

					elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CONSTRUCT ):
						szLeftBuffer = gc.getBuildingInfo(CyInterface().getOrderNodeData1(i)).getDescription()
						szRightBuffer = str(pHeadSelectedCity.getBuildingProductionTurnsLeft(CyInterface().getOrderNodeData1(i), i))

					elif ( CyInterface().getOrderNodeType(i) == OrderTypes.ORDER_CONVINCE ):
						szLeftBuffer = gc.getFatherPointInfo(CyInterface().getOrderNodeData1(i)).getDescription()

					screen.appendTableRow("CityBuildQueue")
					screen.setTableText("CityBuildQueue", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
					screen.setTableText("CityBuildQueue", 1, iRow, szRightBuffer + "  ", "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )

					iRow += 1

		elif (pHeadSelectedUnit and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW and not pHeadSelectedCity):
			screen.setTableColumnHeader("SelectedUnitName", 0, u"", LOWER_RIGHT_CORNER_BACKGROUND_WIDTH * 105 / 100 + 5)
			screen.setTableColumnHeader("SelectedUnitText", 0, u"", LOWER_RIGHT_CORNER_BACKGROUND_WIDTH * 105 / 100 - self.SELECTION_PALEL_LEFT_COLUMN_WIDTH)
			screen.setTableColumnHeader("SelectedUnitText", 1, u"", self.SELECTION_PALEL_LEFT_COLUMN_WIDTH)

			if (CyInterface().mirrorsSelectionGroup()):
				pSelectedGroup = pHeadSelectedUnit.getGroup()
			else:
				pSelectedGroup = 0

			if (CyInterface().getLengthSelectionList() > 1):
				screen.setText("SelectedUnitLabel", "Background", localText.getText("TXT_KEY_UNIT_STACK", (CyInterface().getLengthSelectionList(), )), CvUtil.FONT_LEFT_JUSTIFY, xResolution - LOWER_RIGHT_CORNER_BACKGROUND_WIDTH, yResolution - LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT , -0.1, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_UNIT_NAME, -1, -1 )
				screen.hide("UnitHealthBar")

				iRow += 1

				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					if (pHeadSelectedUnit):
						for i in range(gc.getNumUnitInfos()):
							iCount = CyInterface().countEntities(i)

							if (iCount > 0):
								szRightBuffer = u""
								szLeftBuffer = gc.getUnitInfo(i).getDescription()

								if (iCount > 1):
									szRightBuffer = u"(" + str(iCount) + u")"

								szBuffer = szLeftBuffer + u"  " + szRightBuffer
								iRow = screen.appendTableRow("SelectedUnitText")
								screen.show("SelectedUnitText")
								screen.show("SelectedUnitPanel")

			else:
				if (pHeadSelectedUnit.getHotKeyNumber() == -1):
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME", (pHeadSelectedUnit.getName(), ))
				else:
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME_HOT_KEY", (pHeadSelectedUnit.getHotKeyNumber(), pHeadSelectedUnit.getName()))
				szBuffer = "<font=2b>" + szBuffer + "</font>"

				iRow = screen.appendTableRow("SelectedUnitName")

				screen.setTableRowHeight("SelectedUnitText", iRow, iHeight)
				screen.setTableRowHeight("SelectedUnitName", iRow, iHeight)

				screen.setTableText("SelectedUnitName", 0, iRow, szBuffer, "", WidgetTypes.WIDGET_UNIT_NAME, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
				screen.show("SelectedUnitName")
				screen.show("SelectedUnitText")

				if (pHeadSelectedUnit.getProfession() != -1):
					szBuffer = localText.getText("INTERFACE_PANE_UNIT_NAME", (gc.getProfessionInfo(pHeadSelectedUnit.getProfession()).getDescription(), ))
					szBuffer = "<font=2b>" + szBuffer + "</font>"

					iRow = screen.appendTableRow("SelectedUnitText")
					screen.setTableText("SelectedUnitText", 0, iRow, szBuffer, "", WidgetTypes.WIDGET_UNIT_NAME, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
					screen.show("SelectedUnitText")

				if ((pSelectedGroup == 0) or (pSelectedGroup.getLengthMissionQueue() <= 1)):
					screen.show("SelectedUnitText")
					screen.show("SelectedUnitPanel")

					szBuffer, szLeftBuffer, szRightBuffer = u"", u"", u""

					if (pHeadSelectedUnit.canFight()):
						szLeftBuffer = localText.getText("INTERFACE_PANE_STRENGTH", ())
						if (pHeadSelectedUnit.isFighting()):
							szRightBuffer = u"?/%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
						elif (pHeadSelectedUnit.isHurt()):
							szRightBuffer = u"%.1f/%d%c" %(((float(pHeadSelectedUnit.baseCombatStr() * pHeadSelectedUnit.currHitPoints())) / (float(pHeadSelectedUnit.maxHitPoints()))), pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
						else:
							szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))

					if pHeadSelectedUnit.baseCombatStr() > 0:
						szBuffer = szLeftBuffer + szRightBuffer
						screen.setLabelAt("StrengthText", "UnitHealthBar", szBuffer, CvUtil.FONT_CENTER_JUSTIFY, UNIT_HEALTH_BAR_WIDTH / 2, STACK_BAR_HEIGHT / 2, -1.3, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )
					else:
						screen.hide("UnitHealthBar")

					szLeftBuffer = u""
					szRightBuffer = u""

					if ((pHeadSelectedUnit.movesLeft() % gc.getMOVE_DENOMINATOR()) > 0 ):
						iDenom = 1
					else:
						iDenom = 0
					iCurrMoves = ((pHeadSelectedUnit.movesLeft() / gc.getMOVE_DENOMINATOR()) + iDenom )
					szLeftBuffer = localText.getText("INTERFACE_PANE_MOVEMENT", ())
					if (pHeadSelectedUnit.baseMoves() == iCurrMoves):
						szRightBuffer = u"%d%c" %(pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )
					else:
						szRightBuffer = u"%d/%d%c" %(iCurrMoves, pHeadSelectedUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR) )

					iRow = screen.appendTableRow("SelectedUnitText")
					screen.setTableText("SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
					screen.setTableText("SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, -1, -1, CvUtil.FONT_RIGHT_JUSTIFY )
					screen.show("SelectedUnitText")
					screen.show("SelectedUnitPanel")

					szLeftBuffer = ""
					iMaxWidthPromotions = LOWER_RIGHT_CORNER_BACKGROUND_WIDTH * 105 / 100 - self.SELECTION_PALEL_LEFT_COLUMN_WIDTH
					iCurrentWidthPromotions = 0
					for i in range(gc.getNumPromotionInfos()):
						if (pHeadSelectedUnit.isHasPromotion(i) and not gc.getPromotionInfo(i).isGraphicalOnly()):
							if iCurrentWidthPromotions + 18 > iMaxWidthPromotions:
								iRow = screen.appendTableRow("SelectedUnitText")
								screen.setTableText("SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_UNIT_PROMOTION, pHeadSelectedUnit.getOwner(), pHeadSelectedUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY )
								iCurrentWidthPromotions = 0
								szLeftBuffer = ""
							iCurrentWidthPromotions += 18
							szLeftBuffer += "<img=%s size=16></img>" % (gc.getPromotionInfo(i).getButton(), )

					if len(szLeftBuffer) > 0:
						iRow = screen.appendTableRow("SelectedUnitText")
						screen.setTableText("SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_UNIT_PROMOTION, pHeadSelectedUnit.getOwner(), pHeadSelectedUnit.getID(), CvUtil.FONT_LEFT_JUSTIFY )

			if (pSelectedGroup):
				iNodeCount = pSelectedGroup.getLengthMissionQueue()
				if (iNodeCount > 1):
					for i in range( iNodeCount ):
						szLeftBuffer = u""
						szRightBuffer = u""

						if (gc.getMissionInfo(pSelectedGroup.getMissionType(i)).isBuild()):
							if (i == 0):
								szLeftBuffer = gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription()
								szRightBuffer = localText.getText("INTERFACE_CITY_TURNS", (pSelectedGroup.plot().getBuildTurnsLeft(pSelectedGroup.getMissionData1(i), 0, 0), ))
							else:
								szLeftBuffer = u"%s..." %(gc.getBuildInfo(pSelectedGroup.getMissionData1(i)).getDescription())
						else:
							szLeftBuffer = u"%s..." %(gc.getMissionInfo(pSelectedGroup.getMissionType(i)).getDescription())

						szBuffer = szLeftBuffer + "  " + szRightBuffer
						screen.appendTableRow("SelectedUnitText")
						screen.setTableText("SelectedUnitText", 0, iRow, szLeftBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_LEFT_JUSTIFY )
						screen.setTableText("SelectedUnitText", 1, iRow, szRightBuffer, "", WidgetTypes.WIDGET_HELP_SELECTED, i, -1, CvUtil.FONT_RIGHT_JUSTIFY )
						screen.show("SelectedUnitText")
						screen.show("SelectedUnitPanel")
						iRow += 1

	# Will update the scores
	def updateScoreStrings( self ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )

		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		screen.hide("ScoreBackground")

		for i in range( gc.getMAX_PLAYERS() ):
			szName = "ScoreText" + str(i)
			screen.hide( szName )

		self.SCORE_BACKGROUND_SIDE_MARGIN = 21
		self.SCORE_BACKGROUND_BOTTOM_MARGIN_LARGE = 18
		self.SCORE_BACKGROUND_BOTTOM_MARGIN_SMALL = -100
		self.SCORE_TEXT_BOTTOM_MARGIN_LARGE = 38
		self.SCORE_TEXT_BOTTOM_MARGIN_SMALL = -80

		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if ((CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_MINIMAP_ONLY)):
			if (CyInterface().isScoresVisible() and not CyInterface().isCityScreenUp() and not CyEngine().isGlobeviewUp() ):

				iCount = 8
				iBtnHeight = 22
				iWidth = int((25 * xResolution) / 100)
				yCoord = yResolution - SADDLE_HEIGHT * 14/16 - self.SCORE_TEXT_BOTTOM_MARGIN_SMALL

				# Scrollable Scoreboard: the rows are collected first, the table is as wide as the longest entry (created after the loop)
				aScoreRows = []
				iTableY = yCoord # the yCoord is changed below
				iMaxTextWidth = 0

				i = 0
				while (i < gc.getMAX_CIV_TEAMS()):
					eTeam = gc.getGame().getRankTeam(i)
					if (gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(eTeam) or gc.getTeam(eTeam).isHuman() or gc.getGame().isDebugMode()):
						#j = gc.getMAX_CIV_PLAYERS() - 1
						#while (j > -1):
						j = 0
						while (j < gc.getMAX_CIV_PLAYERS()):
							ePlayer = gc.getGame().getRankPlayer(j)
							if (gc.getPlayer(ePlayer).isAlive()):
								# < JAnimals Mod Start 1/1 > AND # R&R, ray, Church
								if (gc.getGame().isBarbarianPlayer(ePlayer) or gc.getGame().isChurchPlayer(ePlayer)):
									#j = j - 1
									j = j + 1
									continue
								# < JAnimals Mod End 1/1 >
								if (gc.getPlayer(ePlayer).getTeam() == eTeam):
									szBuffer = u"<font=2>"

									if (gc.getGame().isGameMultiPlayer()):
										if (not (gc.getPlayer(ePlayer).isTurnActive())):
											szBuffer = szBuffer + "*"

									if gc.getGame().getPlayerScore(ePlayer) > 0:
										szBuffer += u"%d: " % gc.getGame().getPlayerScore(ePlayer)

									if (gc.getTeam(eTeam).isParentOf(gc.getGame().getActiveTeam())):
											szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.ANCHOR_EUROPE_CHAR))
											szBuffer = szBuffer +  szTempBuffer  + " "

									if (not CyInterface().isFlashingPlayer(ePlayer) or CyInterface().shouldFlash(ePlayer)):
										if (ePlayer == gc.getGame().getActivePlayer()):
											szTempBuffer = u"[<color=%d,%d,%d,%d>%s</color>]" %(gc.getPlayer(ePlayer).getPlayerTextColorR(), gc.getPlayer(ePlayer).getPlayerTextColorG(), gc.getPlayer(ePlayer).getPlayerTextColorB(), gc.getPlayer(ePlayer).getPlayerTextColorA(), gc.getPlayer(ePlayer).getName())
										else:
											szTempBuffer = u"<color=%d,%d,%d,%d>%s</color>" %(gc.getPlayer(ePlayer).getPlayerTextColorR(), gc.getPlayer(ePlayer).getPlayerTextColorG(), gc.getPlayer(ePlayer).getPlayerTextColorB(), gc.getPlayer(ePlayer).getPlayerTextColorA(), gc.getPlayer(ePlayer).getName())
									else:
										szTempBuffer = u"%s" %(gc.getPlayer(ePlayer).getName())
									szBuffer = szBuffer + szTempBuffer

									if (gc.getTeam(eTeam).isAlive()):
										if ( not (gc.getTeam(gc.getGame().getActiveTeam()).isHasMet(eTeam)) ):
											szBuffer = szBuffer + (" ?")
										if (gc.getTeam(eTeam).isAtWar(gc.getGame().getActiveTeam())):
											szBuffer = szBuffer + "("  + localText.getColorText("TXT_KEY_WAR", (), ColorTypes.COLOR_RED).upper() + ")"
										if (not gc.getPlayer(ePlayer).isHuman() and ePlayer != gc.getGame().getActivePlayer()):
											iAtt = gc.getPlayer(ePlayer).AI_getAttitude(gc.getGame().getActivePlayer())
											cAtt = unichr(CyGame().getSymbolID(FontSymbols.ATTITUDE_FURIOUS_CHAR) + iAtt)
											szBuffer += " " +cAtt #+ " (" +u"%d" %iGold  + localText.getText("[ICON_GOLD]", ()) + ")"
										else:
											szBuffer += "    "
										if (gc.getTeam(eTeam).isOpenBorders(gc.getGame().getActiveTeam())):
											szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.OPEN_BORDERS_CHAR))
											szBuffer = szBuffer + szTempBuffer
										if (gc.getTeam(eTeam).isDefensivePact(gc.getGame().getActiveTeam())):
											szTempBuffer = u"%c" %(CyGame().getSymbolID(FontSymbols.DEFENSIVE_PACT_CHAR))
											szBuffer = szBuffer + szTempBuffer
										# Alignement
										elif (not gc.getTeam(eTeam).isOpenBorders(gc.getGame().getActiveTeam())):
											szBuffer = szBuffer + "    "
										if (not gc.getPlayer(ePlayer).isHuman() and ePlayer != gc.getGame().getActivePlayer() and not gc.getPlayer(ePlayer).isEurope() and (not gc.getPlayer(ePlayer).isNative() or gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_MORE_VARIABLES_HIDDEN))):
											iGold = gc.getPlayer(ePlayer).getGold()
											# Alignement issues
											if iGold<10:
												szBuffer += "        (" +u"%d" %iGold  + localText.getText("[ICON_GOLD]", ()) + ")"
											elif iGold<100:
												szBuffer += "     (" +u"%d" %iGold  + localText.getText("[ICON_GOLD]", ()) + ")"
											elif iGold<1000:
												szBuffer += "   (" +u"%d" %iGold  + localText.getText("[ICON_GOLD]", ()) + ")"
											else:
												szBuffer += " (" +u"%d" %iGold  + localText.getText("[ICON_GOLD]", ()) + ")"
										else:
											szBuffer += "               "
									if (CyGame().isNetworkMultiPlayer()):
										szBuffer = szBuffer + CyGameTextMgr().getNetStats(ePlayer)

									if (gc.getPlayer(ePlayer).isHuman() and CyInterface().isOOSVisible()):
										szTempBuffer = u" <color=255,0,0>* %s *</color>" %(CyGameTextMgr().getOOSSeeds(ePlayer))
										szBuffer = szBuffer + szTempBuffer

									szBuffer = szBuffer + "</font>"

									iTextWidth = CyInterface().determineWidth( szBuffer )
									if ( iTextWidth > iMaxTextWidth ):
										iMaxTextWidth = iTextWidth

									szName = "ScoreText" + str(ePlayer)
									if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart() or pHeadSelectedCity != None):
										yCoord = yResolution - SADDLE_HEIGHT * 38 / 100 - 20
									else:
										yCoord = yResolution - SADDLE_HEIGHT - self.SCORE_TEXT_BOTTOM_MARGIN_SMALL

									aScoreRows.append((szBuffer, ePlayer))

									CyInterface().checkFlashReset(ePlayer)

									iCount += 1
							#j = j - 1
							j = j + 1
					#i = i - 1
					i = i + 1

				if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW or CyInterface().isInAdvancedStart() or pHeadSelectedCity != None):
					yCoord = yResolution - SADDLE_HEIGHT * 38 / 100
				else:
					yCoord = yResolution - SADDLE_HEIGHT - self.SCORE_BACKGROUND_BOTTOM_MARGIN_SMALL

				if not pHeadSelectedCity:
					# width of the longest entry plus room for the table border and the scroll bar (never wider than before)
					iWidth = min(iWidth, iMaxTextWidth + 20)
					# (on a small screen the wooden panel of the HUD at the bottom right is higher in relation to the screen: the table ends above it)
					iScoreLift = 0
					if yResolution < 800:
						iScoreLift = 32
					self.tScoreRect = (xResolution - self.SCORE_BACKGROUND_SIDE_MARGIN/2 - iWidth, iTableY + int(yResolution * 0.066) - iScoreLift - (iBtnHeight * 7), iWidth, (iBtnHeight * 7))
					screen.addTableControlGFC("ScoreBackground", 1, xResolution - self.SCORE_BACKGROUND_SIDE_MARGIN/2 - iWidth, iTableY + int(yResolution * 0.066) - iScoreLift - (iBtnHeight * 7), iWidth, (iBtnHeight * 7), False, False, 0, 0, TableStyles.TABLE_STYLE_STANDARD)
					screen.enableSelect("ScoreBackground", False)
					screen.setTableColumnHeader("ScoreBackground", 0, "", iWidth - 10)
					for (szRowText, ePlayerRow) in aScoreRows:
						iRow = screen.appendTableRow("ScoreBackground")
						screen.setTableText("ScoreBackground", 0, iRow, szRowText, "", WidgetTypes.WIDGET_CONTACT_CIV, ePlayerRow, -1, CvUtil.FONT_RIGHT_JUSTIFY)
					screen.show("ScoreBackground")

	# WTP: own tooltip window at the mouse cursor (the tooltip of the game stays at its place). It shows the same text, is vertically
	# centered on the cursor, right of it (left if there is no room) and lies in front of the HUD elements.
	def showCursorTooltip( self, screen, szHelp, bWidget = False, bFromPending = False ):
		if not self.bHoverTip:
			return
		# (the cursor on a frozen window: its lines have tooltips of their own, the plot under the window is not interesting)
		if self.bTipFrozen and self.getFrozenAt(gc.getGame().getCursorClientX(), gc.getGame().getCursorClientY()) >= 0:
			return
		try:
			# the help of the map plot is not shown while the cursor is on a HUD element (the game reports the plot behind it)
			if not bWidget and self.isHudHover():
				return
			# the same on the own panels of the HUD: no plot help while the cursor is on them (a shown one goes away)
			if not bWidget and self.isCursorOnOwnPanel():
				self.szSuppressHelp = u""
				self.hideCursorTooltip(screen)
				return
			if (CyInterface().isCityScreenUp() and not (bWidget and (self.isTradeIconHover() or self.bForceTradeTip))) or len(szHelp) == 0:
				self.szSuppressHelp = u""
				self.hideCursorTooltip(screen)
				return
			# the tooltip of the thing that was just frozen does not appear a second time at once
			if szHelp == self.szSuppressHelp:
				return
			self.szSuppressHelp = u""
			iCursorX = gc.getGame().getCursorClientX()
			iCursorY = gc.getGame().getCursorClientY()
			# the same text again with the cursor near the last place: the window stays as it is (no flicker)
			if self.bCursorTipShown and szHelp == self.szCursorTipText and abs(iCursorX - self.tCursorTipAt[0]) < 80 and abs(iCursorY - self.tCursorTipAt[1]) < 80:
				return
			# tooltip delay: a tooltip waits until the cursor has rested for the time of the option. Another text (the cursor has gone from one
			# thing to the next) removes the tooltip that is shown and starts the time again
			# (in the import / export window the tooltips come at once, whatever the delay is)
			if self.iTipDelay != 0 and not bFromPending and not self.isCursorInTradeWindow() and (not self.bCursorTipShown or (szHelp != self.szCursorTipText and not self.bTipQuick)):
				if self.bCursorTipShown:
					self.hideCursorTooltip(screen)
				if self.szPendingHelp is None:
					self.fPendingStart = self.getTipNow()
					self.tPendingPos = (iCursorX, iCursorY)
				self.szPendingHelp = szHelp
				self.bPendingWidget = bWidget
				return
			self.szPendingHelp = None
			self.hideCursorTooltip(screen)
			xRes = screen.getXResolution()
			yRes = screen.getYResolution()
			iLine = self.getTipLineDistance(yRes) # distance of the text lines (as in the message panel)
			iPad = max(6, iLine / 2)
			iChar = iLine * 0.32 # width of a character (measured in the message panel)
			iMaxWidth = self.getTipMaxWidth(xRes, iChar, False)
			if bWidget:
				# texts of HUD elements are long sentences: narrower window, more lines (as the tooltip of the game)
				iMaxWidth = self.getTipMaxWidth(xRes, iChar, True)
			iCharsPerLine = max(20, int((iMaxWidth - 2 * iPad) / iChar))
			aszLines = []
			aiPara = [] # the paragraph (text between two line breaks of the help) of every line: right click in the frozen window
			aiIndent = [] # indent of continued rows of icons (pixels)
			aszRaw = self.carryColors(self.stripCarries(szHelp).split(u"\n"))
			self.tTipCity = None
			aszParas = self.foldYieldDetails(aszRaw)
			if aszParas is None:
				aszParas = self.foldCityDetails(aszRaw)
			self.tTipWp = None
			if aszParas is None:
				aszParas = self.foldUnitDetails(aszRaw)
				# the tooltip of an own unit alone: the line "Set waypoint..." is in it already (not if it has the line "Commands": there it is the
				# first line of the child window)
				try:
					tRowWp = self.getHoverWaypointRow(aszParas, self.dTipDetails)
					if tRowWp is not None:
						iSlot = self.getWaypointSlot(aszParas)
						tRowWp["paras"][iSlot] = "row"
						aszParas = list(aszParas)
						aszParas.insert(iSlot, localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_SET_ROW", ()))
						dShift = {}
						for kDet in self.dTipDetails.keys():
							if kDet >= iSlot:
								dShift[kDet + 1] = self.dTipDetails[kDet]
							else:
								dShift[kDet] = self.dTipDetails[kDet]
						self.dTipDetails = dShift
						self.tTipWp = tRowWp
				except:
					self.tTipWp = None
			# a plot that is saved as a waypoint says so in its last line (above the hint of the freezing)
			try:
				if not bWidget and not self.bHudHover and self.getTerrainLineIndex(aszParas) >= 0:
					pPlotWp = CyInterface().getMouseOverPlot()
					if pPlotWp is not None and not pPlotWp.isNone():
						szWp = self.getWaypointPlotLine(pPlotWp.getX(), pPlotWp.getY())
						if len(szWp) > 0:
							aszParas = list(aszParas)
							aszParas.append(szWp)
			except:
				pass
			aszParas = self.alignTabLines(aszParas)
			for iPara in range(len(aszParas)):
				aszWrapped = self.wrapMessage(aszParas[iPara], iCharsPerLine, True)
				aszLines += aszWrapped
				aiPara += [iPara] * len(aszWrapped)
				for fIndent in self.aiWrapIndent:
					aiIndent.append(int(fIndent * iChar))
			# the hint at the end: the tooltip can be frozen with X (the frozen window does not have it)
			aszHint = self.wrapMessage(localText.getText("TXT_KEY_WTP_TIP_FREEZE_HINT", ()), iCharsPerLine)
			if self.isPopupWidgetTip():
				aszHint = [] # (no freezing in the popup of the game)
			aszLines += aszHint
			aiPara += [-1] * len(aszHint)
			aiIndent += [0] * len(aszHint)
			self.iTipHintLines = len(aszHint)
			self.aiTipIndent = aiIndent
			iWidth = self.getTipTextWidth(aszLines, iChar, iMaxWidth, iPad, aiIndent)
			iHeight = len(aszLines) * iLine + 2 * iPad
			(iX, iY) = self.getTipPlacement(iWidth, iHeight, iCursorX, iCursorY, xRes, yRes)
			self.tTipPlacedAt = (iCursorX, iCursorY)
			self.tTipLayout = (iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine)
			self.aszTipParas = aszParas
			self.drawCursorTip(screen, False)
			self.bCursorTipShown = True
			self.szCursorTipText = szHelp
			self.fCursorTipShownAt = self.getTipNow()
			self.tCursorTipAt = (iCursorX, iCursorY)
		except:
			self.bCursorTipShown = False

	# the cargo line of a unit that carries only goods ends with "(carries Goods)" (text of the game): the child tooltip of the line tells that, so it
	# is removed here (the text is taken from the translation, with a placeholder for the name)
	def stripCarries( self, szHelp ):
		try:
			aParts = localText.getText("TXT_KEY_UNIT_CARRIES", (u"QQQQ",)).split(u"QQQQ")
			if len(aParts) != 2:
				return szHelp
			szPre = aParts[0].strip()
			szPost = aParts[1].strip()
			if len(szPre) == 0 or len(szPost) == 0:
				return szHelp
			return re.sub(u"[ \t]*" + re.escape(szPre) + u"[^\n]*?" + re.escape(szPost), u"", szHelp)
		except:
			return szHelp

	# A color of the game text can go over several lines ("[COLOR_CYAN]...[NEWLINE]...[COLOR_REVERT]"), but every line is drawn on its own: a line
	# that begins inside of a color gets the color again.
	def carryColors( self, aszParas ):
		aNew = []
		aOpen = []
		for szPara in aszParas:
			if len(aOpen) > 0:
				aNew.append(aOpen[-1] + szPara)
			else:
				aNew.append(szPara)
			for tTag in re.finditer(u"<color=[^>]*>|</color>", szPara):
				if tTag.group(0) == u"</color>":
					if len(aOpen) > 0:
						aOpen.pop()
				else:
					aOpen.append(tTag.group(0))
		return aNew

	# a text without color tags and icons, words separated by one space
	def normTipText( self, szText ):
		szText = re.sub(u"<[^>]*>", u"", szText)
		szText = u"".join([c for c in szText if ord(c) < 0x2000])
		return u" ".join(szText.split())

	def getTipPrefix( self, szKey, aArgs ):
		return self.normTipText(localText.getText(szKey, aArgs)).split(u":")[0].strip()

	# the first line of a unit: its name in a color (the color depends on the owner), then the strength and the moves with their icons
	def isUnitHeader( self, szText ):
		if szText.find(u"<color=") != 0:
			return False
		return re.search(u", [0-9][0-9./]*\\s*[\u2000-\uffff]", re.sub(u"<[^>]*>", u"", szText)) is not None

	# a line of a list: it starts with the bullet (an icon of the game font)
	def isBulletLine( self, szText ):
		szPlain = re.sub(u"<[^>]*>", u"", szText).lstrip()
		return len(szPlain) > 0 and ord(szPlain[0]) >= 0x2000

	# the row of the promotion pictures of a unit (only pictures)
	def isPromotionRow( self, szText ):
		if szText.lower().find(u"<img=") < 0 and re.search(u"[\u2000-\uffff]", re.sub(u"<[^>]*>", u"", szText)) is None:
			return False
		return len(self.normTipText(szText)) == 0

	# Folds the lines of the help text that are not needed at first sight (the lines are the paragraphs of the text); their tooltip lists them.
	# - a unit with promotions (or a military unit: it has a line "Barracks Space Needed"): the XP goes into the row of the promotion pictures,
	#   the plain "Fortify bonus" line follows that row, and everything after the line "Social Status" up to the next unit is folded into the
	#   line "Promotion sum."
	# - the share of the cultures on a plot (82% Dutch ...) is folded into the line "Culture %" above the line "Movement Cost"
	def foldUnitDetails( self, aszParas ):
		self.dTipDetails = {}
		try:
			szBarracks = self.getTipPrefix("TXT_KEY_UNIT_BARRACKS_SPACE_NEEDED", (0, u""))
			szSocial = self.getTipPrefix("TXT_KEY_CITIZEN_STATUS_FREE", ())
			szFortify = self.getTipPrefix("TXT_KEY_UNIT_HELP_FORTIFY_BONUS", (0,))
			szEthn = self.getTipPrefix("TXT_KEY_ETHNICITY_EUROPEAN", ())
			szCargoLine = self.getTipPrefix("TXT_KEY_UNIT_HELP_CARGO_SPACE", (0, 0))
			szMove = self.getTipPrefix("TXT_KEY_FEATURE_MOVEMENT_COST", (0,))
			szYellow = u"<color=255,255,0,255>"
			# a header with the promotion pictures at its end (ships, units of others): the pictures become a row of their own
			aSplit = []
			for szPara in aszParas:
				if (szPara.find(szYellow) == 0 or self.isUnitHeader(szPara)) and szPara.lower().find(u"<img=") > 0:
					iImg = szPara.lower().find(u"<img=")
					if self.isPromotionRow(szPara[iImg:]):
						aSplit.append(szPara[:iImg])
						aSplit.append(szPara[iImg:])
						continue
				aSplit.append(szPara)
			# a unit with an attached leader: the line "commanded by" stands between its header and the row of its promotions; the row comes first
			szCommanded = self.normTipText(localText.getText("TXT_KEY_UNIT_HELP_COMMANDED_BY", ()))
			if len(szCommanded) > 3:
				for k in range(len(aSplit) - 2):
					if (aSplit[k].find(szYellow) == 0 or self.isUnitHeader(aSplit[k])) and self.normTipText(aSplit[k + 1]).find(szCommanded) == 0 and self.isPromotionRow(aSplit[k + 2]):
						szSwap = aSplit[k + 1]
						aSplit[k + 1] = aSplit[k + 2]
						aSplit[k + 2] = szSwap
			aszParas = aSplit
			aOut = [] # [text, folded lines or None]
			n = len(aszParas)
			i = 0
			while i < n:
				aOut.append([aszParas[i], None])
				i += 1
				if aszParas[i - 1].find(szYellow) != 0 and not self.isUnitHeader(aszParas[i - 1]) and not (i < n and self.isPromotionRow(aszParas[i])):
					continue
				# a unit: its lines end at the next unit or at the share of the cultures
				iStart = i
				bPromo = (i < n and self.isPromotionRow(aszParas[i]))
				if bPromo:
					iStart = i + 1
				iEnd = iStart
				while iEnd < n and aszParas[iEnd].find(szYellow) != 0 and not self.isUnitHeader(aszParas[iEnd]) and re.match(u"^[0-9]+% ", self.normTipText(aszParas[iEnd])) is None:
					iEnd += 1
				aLines = aszParas[iStart:iEnd]
				iBarracks = -1
				iSocial = -1
				iFortify = -1
				iEthn = -1
				iCargo = -1
				for k in range(len(aLines)):
					szNorm = self.normTipText(aLines[k])
					if iBarracks < 0 and len(szBarracks) > 3 and szNorm.find(szBarracks) >= 0:
						iBarracks = k
					elif iSocial < 0 and len(szSocial) > 3 and szNorm.find(szSocial) >= 0:
						iSocial = k
					elif iEthn < 0 and len(szEthn) > 3 and szNorm.find(szEthn) == 0:
						iEthn = k
					elif iCargo < 0 and len(szCargoLine) > 3 and szNorm.find(szCargoLine) == 0:
						iCargo = k
					elif iFortify < 0 and len(szFortify) > 3 and szNorm.find(szFortify) == 0 and aLines[k].find(u"<color") < 0:
						iFortify = k
				iFold = -1
				bCargoFold = False
				if iSocial >= 0:
					# (units with promotions in the header have no separate row: the bullet lines after the social status are folded in any case)
					iFold = iSocial + 1
				elif iBarracks >= 0:
					# (also without a separate row of promotions: natives have their promotions at the end of the header)
					iFold = iBarracks
				elif iCargo >= 0:
					# (a ship or a land transport: the bullet lines after the line "Cargo space" are folded, the slots of goods are not)
					iFold = iCargo + 1
					bCargoFold = True
				elif bPromo:
					# (units of others have no line "Social Status": everything is folded)
					iFold = 0
				bSum = True
				if iFold < 0 and iEthn >= 0 and iSocial > iEthn:
					# (no promotions to fold: only the lines of the ethnicity and the social status are put together)
					iFold = iSocial + 1
					bSum = False
				if bPromo:
					# the XP of the unit moves to the row of the promotions
					szHeader = aOut[-1][0]
					tXP = re.search(u",\\s*((?:<[^>]*>)*[^,<:()]{1,10}:\\s*\\(\\s*[0-9]+\\s*/\\s*[0-9]+\\s*\\)(?:<[^>]*>)*)\\s*$", szHeader)
					szRow = aszParas[i]
					if tXP is not None:
						aOut[-1][0] = szHeader[:tXP.start()]
						szRow = szRow + u" " + tXP.group(1)
					aOut.append([szRow, None])
				if iFold < 0:
					i = iStart
					continue
				if iFortify >= 0 and (bSum or iFortify < iFold) and not bCargoFold:
					aOut.append([aLines[iFortify], None])
				bMerge = (iEthn >= 0 and iSocial > iEthn and iSocial < iFold)
				for k in range(iFold):
					if k == iFortify and not bCargoFold:
						continue
					if bMerge and k == iEthn:
						# ethnicity and social status in one line (the ethnicity), both when hovering
						aOut.append([aLines[iEthn], aLines[iEthn] + u"\n" + aLines[iSocial]])
					elif bMerge and k == iSocial:
						pass
					else:
						aOut.append([aLines[k], None])
				# only the list of the unit is folded (lines with a bullet): the lines after it (the commands "(< CTRL > to select ...)", the
				# lines of the plot) stay where they are
				aFolded = []
				iSegEnd = iFold
				while bSum and iSegEnd < len(aLines) and (iSegEnd == iFortify or self.isBulletLine(aLines[iSegEnd])):
					if iSegEnd != iFortify:
						aFolded.append(aLines[iSegEnd])
					iSegEnd += 1
				if bCargoFold and iFortify >= iFold and iFortify < iSegEnd:
					# (the fortify bonus stays a line of its own, below the cargo space)
					aOut.append([aLines[iFortify], None])
				if len(aFolded) > 0:
					aOut.append([localText.getText("TXT_KEY_WTP_TIP_PROMO_SUM", ()), u"\n".join(aFolded)])
				i = iStart + iSegEnd
			# the shares of the cultures: one line above the movement cost
			aFinal = []
			aCulture = []
			for aEntry in aOut:
				if aEntry[1] is None and re.match(u"^[0-9]+% ", self.normTipText(aEntry[0])) is not None:
					aCulture.append(aEntry[0])
				else:
					aFinal.append(aEntry)
			if len(aCulture) > 0:
				# the line of the culture with the highest share (with its colors), "more..." if there are others
				iBest = 0
				iBestShare = -1
				for k in range(len(aCulture)):
					iShare = int(re.match(u"^([0-9]+)% ", self.normTipText(aCulture[k])).group(1))
					if iShare > iBestShare:
						iBestShare = iShare
						iBest = k
				szCulture = aCulture[iBest]
				szDetails = None
				if len(aCulture) > 1:
					szCulture = szCulture + u" " + localText.getText("TXT_KEY_WTP_TIP_MORE", ())
					szDetails = u"\n".join(aCulture)
				iAt = len(aFinal)
				for k in range(len(aFinal)):
					if len(szMove) > 3 and self.normTipText(aFinal[k][0]).find(szMove) == 0:
						iAt = k
						break
				aFinal.insert(iAt, [szCulture, szDetails])
			# the line "Cargo space" of a ship: what it can carry (child tooltip)
			szCargo = self.getTipPrefix("TXT_KEY_UNIT_HELP_CARGO_SPACE", (0, 0))
			szLastHeader = None
			for aEntry in aFinal:
				if aEntry[1] is None:
					if self.isUnitHeader(aEntry[0]):
						szLastHeader = aEntry[0]
					elif szLastHeader is not None and len(szCargo) > 3 and self.normTipText(aEntry[0]).find(szCargo) == 0:
						aEntry[1] = self.getCargoRulesText(szLastHeader)
			# the statistics of a transport: the rows marked with \u00ab are the child window of the line Statistics
			aFinal = self.foldTransportStats(aFinal)
			# the lines of the commands of a stack of units in one line
			aCommands = []
			iCmdAt = -1
			aRest = []
			for aEntry in aFinal:
				if aEntry[1] is None and aEntry[0].find(u"(") >= 0 and self.isCommandText(aEntry[0]):
					if iCmdAt < 0:
						iCmdAt = len(aRest)
					aCommands.append(aEntry[0])
				else:
					aRest.append(aEntry)
			if len(aCommands) > 0:
				aRest.insert(iCmdAt, [localText.getText("TXT_KEY_WTP_TIP_COMMANDS", ()), u"\n".join(aCommands)])
				aFinal = aRest
			aFinal = self.foldUnitGroups(aFinal)
			aFinal = self.foldSellPrices(aFinal)
			aFinal = self.foldCargoValue(aFinal)
			aNew = []
			for aEntry in aFinal:
				if aEntry[1] is not None:
					self.dTipDetails[len(aNew)] = aEntry[1]
				aNew.append(aEntry[0])
			return aNew
		except:
			self.dTipDetails = {}
		return aszParas

	# the sell prices of a cargo slot (the lines Europe / Africa / Port Royal and the line Total): only the line Total stays, the three markets are its
	# the line "Total value" of a loaded sea transport: the lines of the goods on board (marked with >> by the DLL) become its child window
	# the line "Statistics" of a transport of the player (DLL): the rows after it (marked with \u00ab) become its child window
	def foldTransportStats( self, aFinal ):
		try:
			szPrefix = self.getTipPrefix("TXT_KEY_WTP_TRANSPORT_STATS", ())
			if len(szPrefix) < 3:
				return aFinal
			aNewFinal = []
			k = 0
			while k < len(aFinal):
				if aFinal[k][1] is None and self.normTipText(aFinal[k][0]).find(szPrefix) == 0:
					aRows = []
					j = k + 1
					while j < len(aFinal) and aFinal[j][1] is None and self.normTipText(aFinal[j][0]).find(u"\u00ab") == 0:
						aRows.append(aFinal[j][0].replace(u"\u00ab", u"", 1))
						j += 1
					# the log lines (marked with \u00aa): the child window of the first row (Logs); the legend (\u00ba): the child window of the last line of the log window
					aLog = []
					while j < len(aFinal) and aFinal[j][1] is None and self.normTipText(aFinal[j][0]).find(u"\u00aa") == 0:
						aLog.append(aFinal[j][0].replace(u"\u00aa", u"", 1))
						j += 1
					# the legend of the log (marked with \u00ba): the child window of the last line of the log window (Legend)
					aLegend = []
					while j < len(aFinal) and aFinal[j][1] is None and self.normTipText(aFinal[j][0]).find(u"\u00ba") == 0:
						aLegend.append(aFinal[j][0].replace(u"\u00ba", u"", 1))
						j += 1
					if len(aRows) > 0:
						szRows = u"\n".join(aRows)
						if len(aLog) > 0 or len(aLegend) > 0:
							if len(self.dNestedDetails) > 200:
								self.dNestedDetails = {}
							dRowDetails = {}
							if len(aLog) > 0:
								dRowDetails[0] = u"\n".join(aLog)
								if len(self.dWideTips) > 200:
									self.dWideTips = {}
								self.dWideTips[dRowDetails[0]] = 1
							if len(aLegend) > 0 and len(aLog) > 0:
								self.dNestedDetails[dRowDetails[0]] = {len(aLog) - 1: u"\n".join(aLegend)}
							self.dNestedDetails[szRows] = dRowDetails
						aNewFinal.append([aFinal[k][0], szRows])
						k = j
						continue
				aNewFinal.append(aFinal[k])
				k += 1
			return aNewFinal
		except:
			return aFinal

	def foldCargoValue( self, aFinal ):
		try:
			szPrefix = self.getTipPrefix("TXT_KEY_WTP_CARGO_VALUE_HELP", (u"",))
			if len(szPrefix) < 3:
				return aFinal
			aNewFinal = []
			k = 0
			while k < len(aFinal):
				if aFinal[k][1] is None and self.normTipText(aFinal[k][0]).find(szPrefix) == 0:
					aRows = []
					j = k + 1
					while j < len(aFinal) and aFinal[j][1] is None and self.normTipText(aFinal[j][0]).find(u"\u00bb") == 0:
						aRows.append(aFinal[j][0].replace(u"\u00bb", u"", 1))
						j += 1
					if len(aRows) > 0:
						aNewFinal.append([aFinal[k][0], u"\n".join(aRows)])
						k = j
						continue
				aNewFinal.append(aFinal[k])
				k += 1
			return aNewFinal
		except:
			return aFinal

	# child tooltip
	def foldSellPrices( self, aFinal ):
		try:
			szEurope = self.normTipText(localText.getText("TXT_KEY_EUROPE_PRICE_HELP", ()))
			szAfrica = self.normTipText(localText.getText("TXT_KEY_AFRICA_PRICE_HELP", ()))
			szRoyal = self.normTipText(localText.getText("TXT_KEY_PORT_ROYAL_PRICE_HELP", ()))
			szTotal = self.normTipText(localText.getText("TXT_KEY_WTP_TOTAL_PRICE_HELP", ()))
			if min(len(szEurope), len(szAfrica), len(szRoyal), len(szTotal)) < 3:
				return aFinal
			aNewFinal = []
			k = 0
			while k < len(aFinal):
				if k + 3 < len(aFinal) and aFinal[k][1] is None and aFinal[k + 1][1] is None and aFinal[k + 2][1] is None and aFinal[k + 3][1] is None and self.normTipText(aFinal[k][0]).find(szEurope) == 0 and self.normTipText(aFinal[k + 1][0]).find(szAfrica) == 0 and self.normTipText(aFinal[k + 2][0]).find(szRoyal) == 0 and self.normTipText(aFinal[k + 3][0]).find(szTotal) == 0:
					aMarkets = []
					for j in range(3):
						aMarkets.append(aFinal[k + j][0].rstrip().rstrip(u",").strip())
					aNewFinal.append([aFinal[k + 3][0], u"\n".join(aMarkets)])
					k += 4
				else:
					aNewFinal.append(aFinal[k])
					k += 1
			return aNewFinal
		except:
			return aFinal

	# a line of the units that the game lists in groups (a plot with more than 10 units: "Free Colonist (3) 2, Master Potter (1) 2, ...")
	def isUnitGroupLine( self, szText ):
		if szText.find(u"<color=") != 0 or self.isUnitHeader(szText):
			return False
		return re.match(u"^[^(),]+ \\([0-9]+\\)", re.sub(u"<[^>]*>", u"", szText)) is not None

	# the lines of the groups of units become one line "more...units"; its child window lists the units one by one (a right click selects one)
	def foldUnitGroups( self, aFinal ):
		try:
			aRun = []
			for k in range(len(aFinal)):
				if aFinal[k][1] is None and self.isUnitGroupLine(aFinal[k][0]):
					aRun.append(k)
			if len(aRun) == 0:
				return aFinal
			szPlain = u"\n".join([re.sub(u"<[^>]*>", u"", aFinal[k][0]) for k in aRun])
			iTotal = 0
			for szCount in re.findall(u"\\(([0-9]+)\\)", szPlain):
				iTotal += int(szCount)
			if iTotal < 2:
				return aFinal
			pPlot = CyInterface().getMouseOverPlot()
			if pPlot is None or pPlot.isNone():
				pPlot = self.getStackPlot()
			aUnits = None
			if pPlot is not None and not pPlot.isNone():
				aUnits = self.getGroupedUnits(pPlot, szPlain)
			if aUnits is None or len(aUnits) < 2:
				return aFinal
			self.iUnitGroupCounter += 1
			if len(self.dUnitGroups) > 100:
				self.dUnitGroups = {}
			szMarker = u"@WTPUNITS%d" % self.iUnitGroupCounter
			self.dUnitGroups[szMarker] = aUnits
			aKeep = []
			for k in range(len(aFinal)):
				if k == aRun[0]:
					aKeep.append([localText.getText("TXT_KEY_WTP_TIP_MORE_UNITS", ()), szMarker])
				elif k not in aRun:
					aKeep.append(aFinal[k])
			return aKeep
		except:
			pass
		return aFinal

	def getUnitTypeName( self, pUnit ):
		return re.sub(u"<[^>]*>", u"", gc.getUnitInfo(pUnit.getUnitType()).getDescription())

	# the units of a plot in the order of the tooltip of the game: the own ones first, a transport followed by its cargo
	def getPlotUnitOrder( self, pPlot ):
		aAll = []
		eActive = gc.getGame().getActivePlayer()
		eTeam = gc.getGame().getActiveTeam()
		for iPass in range(2):
			for k in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(k)
				if pUnit.isInvisible(eTeam, True) or pUnit.isCargo():
					continue
				if (pUnit.getOwner() == eActive) == (iPass == 0):
					aAll.append(pUnit)
					if pUnit.hasCargo():
						for j in range(pPlot.getNumUnits()):
							pCargo = pPlot.getUnit(j)
							if pCargo.isInvisible(eTeam, True) or not pCargo.isCargo():
								continue
							pTransport = pCargo.getTransportUnit()
							if pTransport is not None and not pTransport.isNone() and pTransport.getID() == pUnit.getID() and pTransport.getOwner() == pUnit.getOwner():
								aAll.append(pCargo)
		return aAll

	# the units of the groups of the text (the game lists the first 10 units of a plot one by one, the unit of the tooltip is no part of the
	# groups): [(owner, id)], None if the groups of the text and the units of the plot do not fit together
	def getGroupedUnits( self, pPlot, szPlain ):
		try:
			aAll = self.getPlotUnitOrder(pPlot)
			if len(aAll) <= 10:
				return None
			aGroup = aAll[10:]
			dWant = {}
			for tEntry in re.findall(u"(?:^|, )([^,()\n]+?) \\(([0-9]+)\\)", szPlain, re.M):
				szName = tEntry[0].strip()
				dWant[szName] = dWant.get(szName, 0) + int(tEntry[1])
			dHave = {}
			for pUnit in aGroup:
				szName = self.getUnitTypeName(pUnit)
				dHave[szName] = dHave.get(szName, 0) + 1
			for szName in dHave.keys():
				while dHave[szName] > dWant.get(szName, 0):
					# (the unit of the tooltip itself: the selected one, else the last of its type)
					iRemove = -1
					for k in range(len(aGroup)):
						if self.getUnitTypeName(aGroup[k]) == szName:
							iRemove = k
							if aGroup[k].IsSelected():
								break
					if iRemove < 0:
						break
					del aGroup[iRemove]
					dHave[szName] -= 1
			iWant = 0
			for szName in dWant.keys():
				iWant += dWant[szName]
				if dHave.get(szName, 0) != dWant[szName]:
					return None
			if len(aGroup) != iWant:
				return None
			return [(pUnit.getOwner(), pUnit.getID()) for pUnit in aGroup]
		except:
			pass
		return None

	# the line of a unit in the list of the child window: like the first line of a unit in a tooltip
	def getUnitListLine( self, tKey ):
		try:
			pUnit = gc.getPlayer(tKey[0]).getUnit(tKey[1])
			if pUnit is None or pUnit.isNone():
				return None
			szLine = u"<color=255,255,0,255>" + pUnit.getNameAndProfession() + u"</color>"
			if pUnit.canFight():
				szLine += u", %d%c" % (pUnit.baseCombatStr(), CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR))
			if pUnit.maxMoves() > 0:
				szLine += u", %d%c" % (pUnit.baseMoves(), CyGame().getSymbolID(FontSymbols.MOVES_CHAR))
			eActive = gc.getGame().getActivePlayer()
			if pUnit.getOwner() == eActive:
				if pUnit.getExperience() > 0:
					szLine += localText.getText("TXT_KEY_UNIT_HELP_LEVEL", (pUnit.getExperience(), pUnit.experienceNeeded()))
			else:
				try:
					if not gc.getUnitInfo(pUnit.getUnitType()).isHiddenNationality():
						pOwner = gc.getPlayer(pUnit.getOwner())
						szLine += u", <color=%d,%d,%d,%d>%s</color>" % (pOwner.getPlayerTextColorR(), pOwner.getPlayerTextColorG(), pOwner.getPlayerTextColorB(), pOwner.getPlayerTextColorA(), pOwner.getName())
				except:
					pass
			return szLine
		except:
			pass
		return None

	# the text of a child window with units: as many units as fit into iBudget lines (the height of the parent window), the rest is behind
	# a last line "more...units"; (text, [the unit of every line (None: no unit), the units of that last line, the number of that line])
	def getUnitListText( self, aUnits, iCharsPerLine, iBudget ):
		aLines = []
		aKeys = []
		iUsed = 0
		iDone = 0
		for k in range(len(aUnits)):
			szLine = self.getUnitListLine(aUnits[k])
			if szLine is None:
				iDone = k + 1
				continue
			iNeed = len(self.wrapMessage(szLine, iCharsPerLine))
			iReserve = 0
			if k < len(aUnits) - 1:
				iReserve = 1
			if len(aLines) > 0 and iUsed + iNeed + iReserve > iBudget:
				break
			aLines.append(szLine)
			aKeys.append(aUnits[k])
			iUsed += iNeed
			iDone = k + 1
		aMore = aUnits[iDone:]
		if len(aMore) == 1:
			# (the last unit takes no more room than the line "more...units")
			szLine = self.getUnitListLine(aMore[0])
			if szLine is None:
				aMore = []
			elif iUsed + len(self.wrapMessage(szLine, iCharsPerLine)) <= iBudget:
				aLines.append(szLine)
				aKeys.append(aMore[0])
				aMore = []
		iMorePara = -1
		if len(aMore) > 0:
			iMorePara = len(aLines)
			aLines.append(localText.getText("TXT_KEY_WTP_TIP_MORE_UNITS", ()))
			aKeys.append(None)
		return (u"\n".join(aLines), [aKeys, aMore, iMorePara])

	# (state, goods missing, goods needing imports, goods with an import rule): state 2 = a production of the city lacks raw materials (the red
	# numbers of the city screen), 1 = a raw material is consumed more than produced and has no import rule, 3 = the same, all with an import rule, 0 = ok
	def getCityProductionState( self, pCity ):
		try:
			aMissing = []
			aNeed = []
			aSet = []
			for iYield in range(YieldTypes.NUM_YIELD_TYPES):
				if pCity.calculateActualYieldProduced(iYield) < pCity.getBaseRawYieldProduced(iYield):
					aMissing.append(iYield)
				if iYield != YieldTypes.YIELD_FOOD and pCity.getRawYieldConsumed(iYield) > pCity.getBaseRawYieldProduced(iYield):
					# the goods made of this raw material
					bSet = pCity.isImport(iYield)
					for iProfession in range(gc.getNumProfessionInfos()):
						bConsumes = False
						for k in range(gc.getProfessionInfo(iProfession).getNumYieldsConsumed()):
							if gc.getProfessionInfo(iProfession).getYieldsConsumed(k) == iYield:
								bConsumes = True
						if bConsumes:
							iOut = gc.getProfessionInfo(iProfession).getYieldsProduced(0)
							if iOut < 0:
								continue
							if bSet:
								if iOut not in aSet:
									aSet.append(iOut)
							elif iOut not in aNeed:
								aNeed.append(iOut)
			for iOut in aNeed:
				if iOut in aSet:
					aSet.remove(iOut)
			if len(aMissing) > 0:
				return (2, aMissing, aNeed, aSet)
			if len(aNeed) > 0:
				return (1, aMissing, aNeed, aSet)
			if len(aSet) > 0:
				return (3, aMissing, aNeed, aSet)
		except:
			pass
		return (0, [], [], [])

	# what a ship can carry (the type is the name in the brackets of the header line), None if the ship is not found
	def getCargoRulesText( self, szHeader ):
		try:
			szFirst = re.sub(u"<[^>]*>", u"", szHeader).split(u",")[0].strip()
			tName = re.search(u"\\(([^()]*)\\)\\s*$", szFirst)
			if tName is None:
				# (a ship without a name of its own: the header is the name of its type, e.g. "Smuggling Ship")
				szType = szFirst
			else:
				szType = tName.group(1).strip()
			for eType in range(gc.getNumUnitInfos()):
				pInfo = gc.getUnitInfo(eType)
				if pInfo.getCargoSpace() > 0 and (pInfo.getDomainType() == DomainTypes.DOMAIN_SEA or pInfo.getDomainType() == DomainTypes.DOMAIN_LAND) and pInfo.getDescription() == szType:
					if pInfo.getSpecialCargo() >= 0:
						szRules = localText.getText("TXT_KEY_WTP_TIP_CARGO_GOODS", ())
					elif hasattr(pInfo, "isSlaveShip") and pInfo.isSlaveShip():
						szRules = localText.getText("TXT_KEY_WTP_TIP_CARGO_SLAVE", ())
					elif hasattr(pInfo, "isTreasureShip") and pInfo.isTreasureShip():
						szRules = localText.getText("TXT_KEY_WTP_TIP_CARGO_TREASURE", ())
					elif hasattr(pInfo, "isTroopShip") and pInfo.isTroopShip():
						szRules = localText.getText("TXT_KEY_WTP_TIP_CARGO_TROOP", ())
					else:
						szRules = localText.getText("TXT_KEY_WTP_TIP_CARGO_ALL", ())
					# the ports over the sea that the ship can sail to (first line)
					if pInfo.getDomainType() == DomainTypes.DOMAIN_SEA and hasattr(pInfo, "canSailToEurope") and hasattr(pInfo, "canSailToAfrica"):
						aPorts = []
						if pInfo.canSailToEurope():
							aPorts.append(localText.getText("TXT_KEY_WTP_TIP_PORT_EUROPE", ()))
						if pInfo.canSailToAfrica():
							aPorts.append(localText.getText("TXT_KEY_WTP_TIP_PORT_AFRICA", ()))
						bSlave = hasattr(pInfo, "isSlaveShip") and pInfo.isSlaveShip()
						if pInfo.isHiddenNationality() or bSlave:
							aPorts.append(localText.getText("TXT_KEY_WTP_TIP_PORT_ROYAL", ()))
						if len(aPorts) > 0:
							szRules = localText.getText("TXT_KEY_WTP_TIP_PORTS", (u", ".join(aPorts),)) + u"\n" + szRules
						else:
							szRules = localText.getText("TXT_KEY_WTP_TIP_NO_OCEAN", ()) + u"\n" + szRules
					return szRules
		except:
			pass
		return None

	# the tooltip of a city (banner): a line with the used storage above "Stored", the buildings in one line ("Buildings", the list when hovering)
	# returns the new paragraphs (self.dTipDetails set) or None if the text is not the tooltip of a city
	def foldCityDetails( self, aszParas ):
		try:
			n = len(aszParas)
			if n < 4:
				return None
			if self.getPlainCommandText(aszParas[n - 2]) != self.getPlainCommandText(localText.getText("TXT_KEY_CITY_BAR_SELECT_CTRL", ())):
				return None
			if self.getPlainCommandText(aszParas[n - 1]) != self.getPlainCommandText(localText.getText("TXT_KEY_CITY_BAR_SELECT_ALT", ())):
				return None
			szName = self.getPlainCommandText(aszParas[0])
			pCity = None
			for ePlayer in range(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(ePlayer)
				if not pPlayer.isAlive():
					continue
				(loopCity, iter) = pPlayer.firstCity(False)
				while loopCity:
					if loopCity.getName() == szName:
						pCity = loopCity
						break
					(loopCity, iter) = pPlayer.nextCity(iter, False)
				if pCity is not None:
					break
			self.dTipDetails = {}
			if pCity is None:
				return None
			szStored = self.getTipPrefix("TXT_KEY_CITY_BAR_STORED", (u"",))
			szProducing = self.getTipPrefix("TXT_KEY_CITY_BAR_PRODUCING", (u"",))
			szList = None
			aBuildings = []
			for eBuilding in range(gc.getNumBuildingInfos()):
				if pCity.isHasRealBuilding(eBuilding):
					aBuildings.append(gc.getBuildingInfo(eBuilding).getDescription())
			if len(aBuildings) > 0:
				szList = self.normTipText(u", ".join(aBuildings))
			aOut = []
			bBuildings = False
			for iParaAt in range(len(aszParas)):
				szPara = aszParas[iParaAt]
				szNorm = self.normTipText(szPara)
				if iParaAt >= n - 3:
					# the three lines of the commands
					if iParaAt == n - 3:
						aOut.append([localText.getText("TXT_KEY_WTP_TIP_COMMANDS", ()), u"\n".join(aszParas[n - 3:])])
					continue
				if len(szStored) > 3 and szNorm.find(szStored) == 0:
					iTotal = pCity.getTotalYieldStored()
					iMax = pCity.getMaxYieldCapacity()
					# what the next turn change takes from the storage (child tooltip of the storage line)
					szForecast = self.getOverflowForecastText(pCity)
					if iTotal > iMax:
						aOut.append([localText.getText("TXT_KEY_WTP_TIP_STORAGE_FULL", (iTotal, iMax)), szForecast])
					else:
						szStorage = localText.getText("TXT_KEY_WTP_TIP_STORAGE", (iTotal, iMax))
						# orange: only about 10 % free, or the maximum is reached within 5 turns with the current net yields
						iNet = 0
						for iYield in range(YieldTypes.NUM_YIELD_TYPES):
							if not gc.getYieldInfo(iYield).isIgnoredForStorageCapacity() and gc.getYieldInfo(iYield).isCargo():
								iNet += pCity.calculateNetYield(iYield)
						if iTotal * 10 >= iMax * 9 or iTotal + 5 * iNet >= iMax:
							szStorage = u"<color=" + WtpColors.code(WtpColors.RAW_SCARCE) + u">" + szStorage + u"</color>"
						aOut.append([szStorage, szForecast])
					# the line of the stock in one line; red: no food or no lumber in the city
					szLabel = localText.getText("TXT_KEY_WTP_TIP_STORED_FOLD", ())
					bNoFood = pCity.getYieldStored(YieldTypes.YIELD_FOOD) <= 0
					bNoWood = pCity.getYieldStored(YieldTypes.YIELD_LUMBER) <= 0
					if bNoFood or bNoWood:
						if bNoFood and bNoWood:
							szLabel = localText.getText("TXT_KEY_WTP_TIP_STORED_BOTH", ())
						elif bNoWood:
							szLabel = localText.getText("TXT_KEY_WTP_TIP_STORED_WOOD", ())
						else:
							szLabel = localText.getText("TXT_KEY_WTP_TIP_STORED_FOOD", ())
						szLabel = u"<color=" + WtpColors.code(WtpColors.RAW_MISSING) + u">" + szLabel + u"</color>"
					# the goods of the list: exported ones golden yellow, imported ones in the color of the imports in the production line
					aSeg = szPara.split(u", ")
					for k in range(len(aSeg)):
						szColor = None
						for iYield in range(YieldTypes.NUM_YIELD_TYPES):
							if aSeg[k].find(unichr(gc.getYieldInfo(iYield).getChar())) >= 0:
								if pCity.isImport(iYield):
									szColor = WtpColors.code(WtpColors.IMPORT)
								elif pCity.isExport(iYield):
									szColor = WtpColors.code(WtpColors.EXPORT)
								break
						if szColor is not None:
							aSeg[k] = u"<color=" + szColor + u">" + aSeg[k] + u"</color>"
					szPara = u", ".join(aSeg)
					aOut.append([szLabel, szPara])
					continue
				if len(szProducing) > 3 and szNorm.find(szProducing) == 0:
					# the line of the production in one line; red: the production lacks goods to work at its capacity,
					# orange: the stock suffices, but the city produces less of a raw material than its production consumes (imports needed)
					szLabel = localText.getText("TXT_KEY_WTP_TIP_PRODUCED_FOLD", ())
					(iState, aMissing, aNeed, aSet) = self.getCityProductionState(pCity)
					if iState == 2:
						szLabel = u"<color=" + WtpColors.code(WtpColors.RAW_MISSING) + u">" + localText.getText("TXT_KEY_WTP_TIP_PRODUCED_MISSING", ()) + u"</color>"
					elif iState == 1:
						szLabel = u"<color=" + WtpColors.code(WtpColors.RAW_SCARCE) + u">" + localText.getText("TXT_KEY_WTP_TIP_PRODUCED_IMPORT", ()) + u"</color>"
					elif iState == 3:
						szLabel = u"<color=" + WtpColors.code(WtpColors.IMPORT) + u">" + localText.getText("TXT_KEY_WTP_TIP_PRODUCED_IMPORT_SET", ()) + u"</color>"
					if iState > 0:
						# the affected goods in the list: red (missing) before orange (imports); the same goods: red
						aSeg = szPara.split(u", ")
						for k in range(len(aSeg)):
							szColor = None
							for iYield in aSet:
								if aSeg[k].find(unichr(gc.getYieldInfo(iYield).getChar())) >= 0:
									szColor = WtpColors.code(WtpColors.IMPORT)
							for iYield in aNeed:
								if aSeg[k].find(unichr(gc.getYieldInfo(iYield).getChar())) >= 0:
									szColor = WtpColors.code(WtpColors.RAW_SCARCE)
							for iYield in aMissing:
								if aSeg[k].find(unichr(gc.getYieldInfo(iYield).getChar())) >= 0:
									szColor = WtpColors.code(WtpColors.RAW_MISSING)
							if szColor is not None:
								aSeg[k] = u"<color=" + szColor + u">" + aSeg[k] + u"</color>"
						szPara = u", ".join(aSeg)
					aOut.append([szLabel, szPara])
					continue
				if not bBuildings and szList is not None and szNorm == szList:
					aOut.append([localText.getText("TXT_KEY_WTP_TIP_BUILDINGS", ()), szPara])
					bBuildings = True
					continue
				aOut.append([szPara, None])
			aNew = []
			for aEntry in aOut:
				if aEntry[1] is not None:
					self.dTipDetails[len(aNew)] = aEntry[1]
				aNew.append(aEntry[0])
			try:
				# an own city: the name line has the list of the own cities as its child window (see tryCityListJump)
				if pCity.getOwner() == gc.getGame().getActivePlayer():
					self.tTipCity = pCity.getID()
					szCities = self.getCityListText(pCity.getID())
					if len(szCities) > 0:
						self.dTipDetails[0] = szCities
			except:
				pass
			return aNew
		except:
			self.dTipDetails = {}
		return None

	# the own cities in the order of their foundation: (turn of the foundation, id, name)
	def getCityOrder( self ):
		aList = []
		try:
			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			(loopCity, iter) = pPlayer.firstCity(False)
			while loopCity:
				aList.append((loopCity.getGameTurnFounded(), loopCity.getID(), loopCity.getName()))
				(loopCity, iter) = pPlayer.nextCity(iter, False)
		except:
			pass
		aList.sort()
		return aList

	# the child window of the name line of an own city: the own cities one per line, the city of the tooltip in green; u"" if there is only one
	def getCityListText( self, iCurrent ):
		aOrder = self.getCityOrder()
		if len(aOrder) < 2:
			return u""
		aLines = []
		for tCity in aOrder:
			szName = re.sub(u"<[^>]*>", u"", tCity[2])
			if tCity[1] == iCurrent:
				szName = u"<color=120,230,120,255>" + szName + u"</color>"
			aLines.append(szName)
		return u"\n".join(aLines)

	# the frozen tooltip of a plot with an own city (the units of the city, the plot): the line with the name of the city gets the list of the
	# cities as its child window, like the name line of the tooltip of the city
	def registerPlotCity( self, iLevel ):
		try:
			tA = self.aFrozen[iLevel][5]
			if tA is None or tA[0] < 0:
				return
			pPlot = CyMap().plot(tA[0], tA[1])
			if pPlot is None or pPlot.isNone() or not pPlot.isCity():
				return
			pCity = pPlot.getPlotCity()
			if pCity is None or pCity.isNone() or pCity.getOwner() != gc.getGame().getActivePlayer():
				return
			szList = self.getCityListText(pCity.getID())
			if len(szList) == 0:
				return
			szName = self.normTipText(pCity.getName())
			aszParas = self.aFrozen[iLevel][2]
			for k in range(len(aszParas)):
				if self.normTipText(aszParas[k]) == szName:
					self.aFrozen[iLevel][4][k] = szList
					self.dCityWin[self.aFrozen[iLevel][0]] = pCity.getID()
					self.dCityPlotWin[self.aFrozen[iLevel][0]] = True
					return
		except:
			self.tipError("registerPlotCity")

	# the paragraph of the line with the name of the city in a frozen tooltip with the list of the cities (-1: none): the first line of the
	# tooltip of the city, in the tooltip of a plot the line with the name (it moves when the units are sorted)
	def getCityLinePara( self, iLevel ):
		try:
			if iLevel < 0 or iLevel >= len(self.aFrozen):
				return -1
			szPrefix = self.aFrozen[iLevel][0]
			if not self.dCityWin.has_key(szPrefix):
				return -1
			if not self.dCityPlotWin.has_key(szPrefix):
				return 0
			pCity = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(self.dCityWin[szPrefix])
			if pCity is None or pCity.isNone():
				return -1
			szName = self.normTipText(pCity.getName())
			aszParas = self.aFrozen[iLevel][2]
			for k in range(len(aszParas)):
				if self.normTipText(aszParas[k]) == szName and self.aFrozen[iLevel][4].has_key(k):
					return k
		except:
			pass
		return -1

	# the frozen tooltip of an own city: its city (-1: it is no such window)
	def getCityOfWindow( self, iLevel ):
		try:
			if iLevel < 0 or iLevel >= len(self.aFrozen):
				return -1
			return self.dCityWin.get(self.aFrozen[iLevel][0], -1)
		except:
			return -1

	# A click on the name line of the frozen tooltip of an own city. Right click: the map looks at the city that Shift + mouse wheel has chosen in
	# the list (without a choice: at the city of the tooltip). Left click: the jump to the next city of the list (the chosen one): the tooltip of
	# this one is frozen there and the cursor stands on its name line again; the tooltip that the click was made in is closed.
	def tryCityListJump( self, iLevel, iPara, bLeft ):
		try:
			iCur = self.getCityOfWindow(iLevel)
			if iCur < 0 or iPara < 0 or iPara != self.getCityLinePara(iLevel):
				return False
			aOrder = self.getCityOrder()
			if len(aOrder) == 0:
				return False
			iTarget = iCur
			if self.iTipSelPara == iPara and self.iTipSelLevel == iLevel and self.iTipSelIdx >= 0 and self.iTipSelIdx < len(aOrder):
				iTarget = aOrder[self.iTipSelIdx][1]
			elif bLeft:
				iPos = 0
				for k in range(len(aOrder)):
					if aOrder[k][1] == iCur:
						iPos = k
						break
				iTarget = aOrder[(iPos + 1) % len(aOrder)][1]
			pCity = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(iTarget)
			if pCity is None or pCity.isNone():
				return False
			CyCamera().JustLookAtPlot(pCity.plot())
			self.tJump = (pCity.getX(), pCity.getY(), (self.getTipNow() / 1000.0))
			try:
				CyInterface().playGeneralSound(self.szModJumpSound)
			except:
				pass
			if not bLeft or iTarget == iCur:
				return True
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			# (the list window of the old city goes at once, it does not wait for the camera)
			self.hideSecondTip(screen)
			self.tSecondTipKey = None
			self.closeFrozenChild(screen, iLevel)
			self.tCityJump = {"city": iTarget, "wait": 3, "tries": 0, "still": 0, "last": None}
			self.bCityHold = True
			self.szCityHoldWin = u""
			return True
		except:
			self.tipError("tryCityListJump")
		return False

	# after the jump to a city: when the camera is there the tooltip of the city (the text that the game shows on its banner) is made, frozen at
	# the city (it moves with the map, other frozen windows give way) and the cursor goes to its name line
	def updateCityJump( self ):
		t = self.tCityJump
		if t is None:
			return
		try:
			if t["wait"] > 0:
				t["wait"] -= 1
				return
			pCity = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(t["city"])
			if pCity is None or pCity.isNone():
				self.tCityJump = None
				return
			(iSX, iSY) = self.getPlotScreen(pCity.getX(), pCity.getY())
			# (the camera needs some time to arrive: the window is made when the city has stood still on the screen for a few frames, so that the
			# window does not fly along with the city; at most about 1.5 seconds)
			t["tries"] += 1
			tLast = t["last"]
			if tLast is not None and abs(iSX - tLast[0]) <= 1 and abs(iSY - tLast[1]) <= 1:
				t["still"] += 1
			else:
				t["still"] = 0
			t["last"] = (iSX, iSY)
			# (a city that has not moved yet is standing still too: the camera may start late. It counts as arrived when the city is near the
			# middle of the screen; a city that the camera cannot center (map edge) counts after about a second)
			xCheck = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).getXResolution()
			yCheck = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).getYResolution()
			bCentered = (abs(iSX - xCheck / 2) < xCheck * 0.3 and abs(iSY - yCheck / 2) < yCheck * 0.3)
			bReady = (t["still"] >= 4 and (bCentered or t["tries"] >= 60))
			if not bReady and t["tries"] < 150:
				return
			self.tCityJump = None
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			# (the cursor goes to the city, but not onto the HUD: a city at the lower right of the map (the camera cannot center it there) would put
			# the cursor on the score table; the game then reports the help of the HUD and no tooltip is made)
			xRes = screen.getXResolution()
			yRes = screen.getYResolution()
			iSX = max(int(xRes * 0.05), min(int(xRes * 0.72), iSX))
			iSY = max(int(yRes * 0.12), min(int(yRes * 0.62), iSY))
			gc.getGame().setCursorClient(iSX, iSY)
			self.bHudHover = False
			self.szHudHelp = u""
			self.szPendingHelp = None
			szHelp = gc.getGame().getCityBarHelpFor(pCity.getOwner(), pCity.getID())
			if len(szHelp) == 0:
				return
			self.szSuppressHelp = u""
			self.hideCursorTooltip(screen)
			self.showCursorTooltip(screen, szHelp, False, True)
			if not self.bCursorTipShown or self.tTipCity != t["city"]:
				return
			if not self.freezeCursorTooltip() or len(self.aFrozen) == 0:
				return
			iNew = len(self.aFrozen) - 1
			tL = self.aFrozen[iNew][1]
			self.aFrozen[iNew][5] = self.makeAnchor(tL, (pCity.getX(), pCity.getY()))
			# (the cursor on the name line: it goes with the window while the window finds its place - the anchor, the other windows that it gives
			# way to - as after a jump to a waypoint)
			iDX = min(tL[2] / 2, 60)
			iDY = tL[6] + tL[7] / 2
			gc.getGame().setCursorClient(tL[0] + iDX, tL[1] + iDY)
			self.tCursorFollow = [self.aFrozen[iNew][0], iDX, iDY, (self.getTipNow() / 1000.0), -1, -1, 0]
			self.szCityHoldWin = self.aFrozen[iNew][0]
			self.tCityHoldPos = None
			self.iCityHoldStill = 0
			self.tSecondTipKey = None
		except:
			self.tCityJump = None
			self.tipError("updateCityJump")

	# where a window of this size goes: mode 0 beside the cursor (right of it, left if there is no room; beside the own windows when the cursor is
	# on one) with its top at the lower end of the cursor; mode 1 at the place of the game tooltip (left, above the HUD, growing upwards)
	def getTipPlacement( self, iWidth, iHeight, iCursorX, iCursorY, xRes, yRes ):
		if self.iTipMode == 1:
			return (HELTTEXT_AREA_X_MARGIN, max(4, yRes - SADDLE_HEIGHT - iHeight))
		if self.isPopupWidgetTip():
			# the popup of the production of a city (1440p only; the popup is about 400 pixels wide, its left edge about 175 pixels left of the middle of the
			# screen, measured at 2560 x 1440): the tooltip stands right beside it, on its left
			try:
				if yRes == 1440 and self.iLastWidgetType in (int(WidgetTypes.WIDGET_TRAIN), int(WidgetTypes.WIDGET_CONSTRUCT)):
					return (max(4, xRes / 2 - 175 - 12 - iWidth), max(4, min(yRes - iHeight - 4, iCursorY - iHeight / 2)))
			except:
				pass
			# (the popup stands in the middle of the screen, about half of its width: the left edge is free)
			return (max(4, int(xRes * 0.01)), max(4, min(yRes - iHeight - 4, iCursorY - iHeight / 2)))
		iGap = max(48, int(yRes * 0.04))
		tRect = self.getTipAvoidRect(iCursorX, iCursorY)
		if tRect is not None:
			iX = tRect[0] + tRect[2] + 12
			if self.isTradeIconHover():
				# the goods of the import / export window: the tooltip opens left of the window (the pictures are at its left edge)
				iX = tRect[0] - 12 - iWidth
				if iX < 4:
					iX = tRect[0] + tRect[2] + 12
					if iX + iWidth > xRes - 4:
						# (no room on both sides: at the left edge of the screen, over the window)
						iX = 4
			elif iX + iWidth > xRes - 4:
				iX = tRect[0] - 12 - iWidth
		else:
			iX = iCursorX + iGap
			if iX + iWidth > xRes - 4:
				iX = iCursorX - int(iGap * 0.6) - iWidth
		iX = max(4, iX)
		iY = max(4, min(yRes - iHeight - 4, iCursorY + self.getCursorBottom(yRes)))
		if tRect is not None and self.isTradeIconHover():
			# the picture of a good: the tooltip stands left of it, its middle at the height of the middle of the picture
			try:
				tWin = CvScreensInterface.tradeRouteScreen
				tCenter = tWin.getIconCenter(tWin.getIconYieldAt(iCursorX, iCursorY))
				if tCenter is not None:
					iY = max(4, min(yRes - iHeight - 4, tCenter[1] - iHeight / 2))
			except:
				pass
		if len(self.aFrozen) > 0 and tRect is not None:
			# beside a window of the mod (import / export window): not over a frozen tooltip, not over the window; the other side of the window
			# and above / below the frozen ones if it is not free
			iLeftX = tRect[0] - 12 - iWidth
			iRightX = tRect[0] + tRect[2] + 12
			iStep = iHeight + 6
			aCands = []
			# the heights that are closest to the wanted one first: right above / below the frozen windows (not a whole window height away)
			aYs = [iY]
			for tFz in self.aFrozen:
				try:
					aYs.append(tFz[1][1] - iHeight - 6)
					aYs.append(tFz[1][1] + tFz[1][3] + 6)
				except:
					pass
			aYs = [max(4, min(yRes - iHeight - 4, iOneY)) for iOneY in aYs]
			aYs.sort(lambda a, b: cmp(abs(a - iY), abs(b - iY)))
			for iSideX in (iX, iLeftX, iRightX):
				for iOneY in aYs:
					aCands.append((iSideX, iOneY))
				for iShift in (1, -1, 2, -2):
					aCands.append((iSideX, iY + iShift * iStep))
			(iX, iY) = self.pickFreeSpot(aCands, iWidth, iHeight, xRes, yRes, -1, [tRect])
		if len(self.aFrozen) > 0 and tRect is None:
			# it does not cover a frozen window: the other side of the cursor, then below and above the cursor
			iRight = iCursorX + iGap
			iLeft = iCursorX - int(iGap * 0.6) - iWidth
			iBelow = iCursorY + self.getCursorBottom(yRes)
			(iX, iY) = self.pickFreeSpot([(iX, iY), (iRight, iY), (iLeft, iY), (iX, iBelow + 2 * iGap), (iX, iCursorY - iHeight - iGap)], iWidth, iHeight, xRes, yRes)
		return (iX, iY)

	# the window follows the cursor: the game asks for the same text again only now and then, and a window that stays where it was made
	# would be too far away from the cursor
	def followCursorTip( self, screen ):
		iCursorX = gc.getGame().getCursorClientX()
		iCursorY = gc.getGame().getCursorClientY()
		if abs(iCursorX - self.tTipPlacedAt[0]) < 6 and abs(iCursorY - self.tTipPlacedAt[1]) < 6:
			return
		(iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine) = self.tTipLayout
		(iNX, iNY) = self.getTipPlacement(iWidth, iHeight, iCursorX, iCursorY, screen.getXResolution(), screen.getYResolution())
		self.tTipPlacedAt = (iCursorX, iCursorY)
		if iNX == iX and iNY == iY:
			return
		for szName in self.getCursorTipNames():
			screen.hide(szName)
			screen.deleteWidget(szName)
		self.tTipLayout = (iNX, iNY, iWidth, iHeight, aszLines, aiPara, iPad, iLine)
		self.drawCursorTip(screen, False)

	# width of a window for the lines (icons of the game font are wider than letters: getMessageWidth, as the lines were wrapped)
	# pixel width of a text of the tooltip font by character classes (fitted to measured lines of the game: a line of 50 characters is between 250
	# and 350 pixels wide, so a character count is not good enough). The values are for a line distance of 22 pixels, the others are scaled.
	# Width of the letters in thousandths of the font size (a serif font like Times: measured on the screenshots of the tooltips, the
	# factor to pixels is 15.9 for a line of 22 pixels, the icons of the game font are 19.7 pixels wide)
	TIP_CHAR_WIDTHS = {}
	for szWtpChars, aiWtpWidths in (
			(u"abcdefghijklmnopqrstuvwxyz", [444,500,444,500,444,333,500,500,278,278,500,278,778,500,500,500,500,333,389,278,500,500,722,500,500,444]),
			(u"ABCDEFGHIJKLMNOPQRSTUVWXYZ", [722,667,667,722,611,556,722,722,333,389,722,611,889,722,722,556,722,667,556,611,722,722,944,722,722,611]),
			(u"0123456789", [500,500,500,500,500,500,500,500,500,500]),
			(u" ,.:;-()%/+'!|\"", [250,250,250,278,278,333,333,333,833,278,564,180,333,200,408])):
		for iWtpChar in range(len(szWtpChars)):
			TIP_CHAR_WIDTHS[szWtpChars[iWtpChar]] = aiWtpWidths[iWtpChar]

	def getTextPixels( self, szPlain, iLine ):
		fSum = 0.0
		szPlain = szPlain.replace(u"&lt;", u"<").replace(u"&gt;", u">").replace(u"&amp;", u"&")
		for c in szPlain:
			if c == u"\t" or ord(c) < 32:
				# (the [TAB] of the game text may arrive as another control character than a tab)
				# a tab goes to the next tab stop (31 pixels for a line of 22 pixels: measured on the sell price lines of a cargo ship)
				# (the tab stops of the game do not shrink with a smaller font: 31 pixels, in the units of the 22 pixel layout they are wider then)
				fStop = 31.0 * 22.0 / max(1.0, float(iLine))
				fSum = (int(fSum / fStop) + 1) * fStop
			elif c == u"\u2022":
				fSum += 8.0 # the bullet of a list
			elif ord(c) >= 0x2000:
				fSum += 19.7 # icon of the game font
			elif self.TIP_CHAR_WIDTHS.has_key(c):
				fSum += self.TIP_CHAR_WIDTHS[c] * 0.0159
			elif c.isupper():
				fSum += 10.3
			else:
				fSum += 7.1 # other letters (accents)
		return fSum * iLine / 22.0

	def hasControlChar( self, szText ):
		for c in szText:
			if ord(c) < 32:
				return True
		return False

	def getTipTextWidth( self, aszLines, iChar, iMaxWidth, iPad, aiIndent = None ):
		iLine = iChar / 0.32
		fPixel = 0
		fTabPixel = 0
		for i in range(len(aszLines)):
			# (the [TAB] of the game text arrives as the tag <tab>: it is a tab stop, not a tag without width)
			szLineTabs = re.sub(u"(?i)<tab>", u"\t", aszLines[i])
			fThis = self.getTextPixels(re.sub(u"<[^>]*>", u"", szLineTabs), iLine) + len(re.findall(u"<img=", aszLines[i].lower())) * 18.0 * iLine / 22.0
			if aiIndent is not None and i < len(aiIndent):
				fThis += aiIndent[i]
			if self.hasControlChar(szLineTabs):
				# the tab stops (and the columns of the lines with tabs, which are aligned with the widths of the 1440 font) do not shrink with a
				# smaller font: the line is never estimated narrower than 96 percent of its width in the font of the 1440 layout
				if iLine < 22.0:
					fThis = max(fThis, 0.96 * (self.getTextPixels(re.sub(u"<[^>]*>", u"", szLineTabs), 22.0) + len(re.findall(u"<img=", aszLines[i].lower())) * 18.0))
				fTabPixel = max(fTabPixel, fThis)
			else:
				fPixel = max(fPixel, fThis)
		# a little reserve (4.5 % + 4 pixels) and the border; the lines were wrapped by a character count, so wide letters can make a line wider than
		# the maximum. The lines with tab stops (the sell prices of cargo) cannot be wrapped: they may make the window up to 1.5 times as wide.
		iWidth = max(120, min(int(iMaxWidth * 1.15), int(fPixel * 1.045) + 2 * iPad + 4))
		if fTabPixel > 0:
			# (the tab stops are only estimated: one more border width on the right side)
			iWidth = max(iWidth, min(int(iMaxWidth * 1.5), int(fTabPixel * 1.06) + 3 * iPad + 4))
		return iWidth

	def drawCursorTip( self, screen, bClickable ):
		self.iTradeMarked = -1
		self.iCursorTipLines = len(self.tTipLayout[4])
		self.drawTipWindow(screen, "HudTip", self.tTipLayout, bClickable, 0, self.aiTipIndent)

	def getTipWindowNames( self, szPrefix, iLines ):
		aszNames = [szPrefix + "Back1", szPrefix + "Back2", szPrefix + "Back3"]
		for i in range(iLines):
			aszNames.append(szPrefix + "Line%d" % i)
		return aszNames

	def deleteTipWindow( self, screen, szPrefix, iLines ):
		for szName in self.getTipWindowNames(szPrefix, iLines):
			screen.hide(szName)
			screen.deleteWidget(szName)

	# a tooltip window; the lines of a frozen one can be clicked (right click: Colopedia), their data is the level of the window and the paragraph
	# WAYPOINTS OF UNITS. The tooltip of an own unit gets the line "Set waypoint..." when it is frozen (above the hint of the freezing; in the
	# child window of the line "Commands" as its first line, if there is one). Its child window lists "New waypoint" and the saved waypoints: a right
	# click on a saved one sends the unit there (Ctrl + right click deletes the waypoint). "New waypoint" selects the unit: the target of its next
	# order to move (the ordinary right click on the map) is saved as a waypoint (the name of the colony there, otherwise the number and the
	# terrain) and the unit goes there at once. The waypoints are kept in the savegame (sdToolKit), for each player.
	# The waypoints of ships are kept apart from those of land units: two lists, each numbered on its own (the numbers of the waypoints are
	# the same counter, so every waypoint is told apart by its number in both lists)
	def getAllWaypoints( self, ePlayer = -1 ):
		# (list of the land units, list of the ships, the number that the next waypoint gets); a waypoint is (number, x, y, name)
		try:
			if ePlayer < 0:
				ePlayer = gc.getGame().getActivePlayer()
			if sdToolKit.sdEntityExists('WTPWaypoints', ePlayer):
				aLand = []
				for tWp in sdToolKit.sdGetVal('WTPWaypoints', ePlayer, 'List'):
					# (the name without a number in front: "3: Hills" of an older version)
					aLand.append((tWp[0], tWp[1], tWp[2], re.sub(u"^[0-9]+[:.]\\s*", u"", tWp[3])))
				aSea = []
				try:
					aSea = list(sdToolKit.sdGetVal('WTPWaypoints', ePlayer, 'SeaList'))
				except:
					pass
				return (aLand, aSea, sdToolKit.sdGetVal('WTPWaypoints', ePlayer, 'Next'))
		except:
			pass
		return ([], [], 0)

	def saveAllWaypoints( self, aLand, aSea, iNext, ePlayer = -1 ):
		try:
			if ePlayer < 0:
				ePlayer = gc.getGame().getActivePlayer()
			sdToolKit.sdEntityInit('WTPWaypoints', ePlayer, {'List': aLand, 'SeaList': aSea, 'Next': iNext})
		except:
			pass

	# the waypoints of the land units (bSea False) or of the ships (bSea True): (list, the number of the next waypoint)
	def getWaypoints( self, ePlayer = -1, bSea = False ):
		(aLand, aSea, iNext) = self.getAllWaypoints(ePlayer)
		if bSea:
			return (aSea, iNext)
		return (aLand, iNext)

	def saveWaypoints( self, aWp, iNext, ePlayer = -1, bSea = False ):
		(aLand, aSea, iOld) = self.getAllWaypoints(ePlayer)
		if bSea:
			aSea = aWp
		else:
			aLand = aWp
		self.saveAllWaypoints(aLand, aSea, iNext, ePlayer)

	# a message of the mod (a warning, a note of the tooltips): in the message panel (if it is installed and on) as a message at the top, all in the
	# yellow of the units; otherwise as the game shows its messages
	# tPlot = (x, y): the place of the message (a click on its line in the message panel shows it on the map; the panel gets no place from the
	# game for the messages of the mod, so the text is remembered with its place, see getMessageTargets)
	def showModMessage( self, szText, szSound = None, tPlot = None ):
		if szSound is None:
			szSound = self.szModMessageSound
		if tPlot is not None:
			self.dModMessagePlot[re.sub(u"<[^>]*>", u"", szText).strip()] = tPlot
		szYellow = u"<color=255,255,0,255>" + re.sub(u"<color=[^>]*>|</color>", u"", szText) + u"</color>"
		bPanel = False
		try:
			if self.isMessagePanelOption():
				gc.getGame().addHudMessage(szYellow, True)
				bPanel = True
		except:
			pass
		if not bPanel:
			try:
				CyInterface().addImmediateMessage(szYellow, "")
			except:
				pass
		# a short, quiet sound (the same with and without the panel)
		try:
			if len(szSound) > 0:
				CyInterface().playGeneralSound(szSound)
		except:
			pass

	def isSeaUnit( self, pUnit ):
		try:
			return pUnit.getDomainType() == DomainTypes.DOMAIN_SEA
		except:
			return False

	# the own colony (of the active player) on a plot, or None
	def getOwnColonyAt( self, iX, iY, ePlayer = -1 ):
		try:
			if ePlayer < 0:
				ePlayer = gc.getGame().getActivePlayer()
			pPlot = CyMap().plot(iX, iY)
			if pPlot.isCity():
				pCity = pPlot.getPlotCity()
				if pCity.getOwner() == ePlayer:
					return pCity
		except:
			pass
		return None

	# is the text the name of one of the own colonies (not looking at upper and lower case, at numbers and dots in front)?
	def isColonyName( self, szName, ePlayer = -1 ):
		try:
			if ePlayer < 0:
				ePlayer = gc.getGame().getActivePlayer()
			szCheck = re.sub(u"^[\\s0-9.:]+", u"", szName).strip().lower()
			if len(szCheck) == 0:
				return False
			pPlayer = gc.getPlayer(ePlayer)
			(loopCity, iter) = pPlayer.firstCity(False)
			while loopCity:
				if re.sub(u"<[^>]*>", u"", loopCity.getName()).strip().lower() == szCheck:
					return True
				(loopCity, iter) = pPlayer.nextCity(iter, False)
		except:
			pass
		return False

	# the waypoints as they are listed: first those that lead to an own colony (without a number, the capital first, then in the order the colonies
	# were founded), then the others, numbered from 1 in the order of the list. Each entry: (number of the waypoint, x, y, name, text of the line)
	def getWaypointView( self, bSea, ePlayer = -1 ):
		(aWp, iNext) = self.getWaypoints(ePlayer, bSea)
		aCol = []
		aRest = []
		for tWp in aWp:
			pCity = self.getOwnColonyAt(tWp[1], tWp[2], ePlayer)
			if pCity is not None:
				iCapital = 1
				if pCity.isCapital():
					iCapital = 0
				iFounded = 0
				try:
					iFounded = pCity.getGameTurnFounded()
				except:
					pass
				aCol.append(((iCapital, iFounded, pCity.getID()), tWp, pCity.getName()))
			else:
				aRest.append(tWp)
		aCol.sort()
		aView = []
		for (tKey, tWp, szName) in aCol:
			aView.append((tWp[0], tWp[1], tWp[2], szName, szName))
		for k in range(len(aRest)):
			aView.append((aRest[k][0], aRest[k][1], aRest[k][2], aRest[k][3], u"%d. %s" % (k + 1, aRest[k][3])))
		return aView

	# the line for the tooltip of a plot that is saved as a waypoint (of the land units and / or of the ships): "Set as WP: name" in the colour of the
	# line "Set waypoint..." (the name has no colour of its own); an empty text if the plot is none
	def getWaypointPlotLine( self, iX, iY ):
		aNames = []
		try:
			for bSea in (False, True):
				for tEntry in self.getWaypointView(bSea):
					if tEntry[1] == iX and tEntry[2] == iY:
						szName = self.normTipText(tEntry[4])
						if szName not in aNames:
							aNames.append(szName)
		except:
			return u""
		if len(aNames) == 0:
			return u""
		return localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_IS_SET", (u", ".join(aNames),))

	# True if the paragraph is the line "Set as WP: name" of the tooltip of a plot
	def isWaypointPlotPara( self, szPara ):
		try:
			szPre = re.sub(u"<[^>]*>", u"", localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_IS_SET", (u"QQQQ",)).split(u"QQQQ")[0]).strip()
			return len(szPre) > 0 and re.sub(u"<[^>]*>", u"", szPara).strip().startswith(szPre)
		except:
			return False

	# right click on the line "Set as WP: name" of a frozen window of a plot: Ctrl: delete the waypoint(s) of the plot, Shift: rename (the first one);
	# True if the line was hit (a plain right click does nothing there)
	def runWaypointPlotClick( self, iLevel, iPara, bSecond, bShift, iOption = -1 ):
		try:
			aszParas = self.aFrozen[iLevel][2]
			if iPara < 0 or iPara >= len(aszParas) or not self.isWaypointPlotPara(aszParas[iPara]):
				return False
			tAnchor = self.aFrozen[iLevel][5]
			if tAnchor is None or self.aFrozen[iLevel][6] >= 0:
				return True
			# (the choice of shift + mouse wheel: 0 delete, 1 rename; otherwise the modifier keys)
			if iOption == 0:
				bSecond = True
				bShift = False
			elif iOption == 1:
				bShift = True
			if not (bSecond or bShift):
				return True
			tHit = None
			for bSea in (False, True):
				(aWp, iNext) = self.getWaypoints(-1, bSea)
				aKeep = []
				for tWp in aWp:
					if tWp[1] == tAnchor[0] and tWp[2] == tAnchor[1]:
						if tHit is None:
							tHit = (bSea, tWp[0])
						if not bShift:
							continue # (deleted)
					aKeep.append(tWp)
				if not bShift and len(aKeep) != len(aWp):
					self.saveWaypoints(aKeep, iNext, -1, bSea)
			if tHit is None:
				return True
			self.unfreezeAllTips()
			if bShift:
				CvEventInterface.beginEvent(CvUtil.EventRenameWaypoint, (tHit[1], self.getWaypointTextById(tHit[0], tHit[1])))
			else:
				self.refreshWaypointLists()
			return True
		except:
			return False

	# the line of a waypoint (by its number) as it is shown
	def getWaypointTextById( self, bSea, iId, ePlayer = -1 ):
		for tEntry in self.getWaypointView(bSea, ePlayer):
			if tEntry[0] == iId:
				return tEntry[4]
		return u""

	# the name that a waypoint gets when it is set: the colony on the plot, otherwise the terrain ("Hills/Forest/Savanna")
	def getWaypointLabel( self, pPlot ):
		try:
			if pPlot.isCity():
				return pPlot.getPlotCity().getName()
		except:
			pass
		aParts = []
		try:
			if pPlot.isPeak():
				aParts.append(localText.getText("TXT_KEY_PLOT_PEAK", ()))
			elif pPlot.isHills():
				aParts.append(localText.getText("TXT_KEY_PLOT_HILLS", ()))
			if pPlot.getFeatureType() >= 0:
				aParts.append(gc.getFeatureInfo(pPlot.getFeatureType()).getDescription())
			if pPlot.getTerrainType() >= 0:
				szTerrain = gc.getTerrainInfo(pPlot.getTerrainType()).getDescription()
				bKnown = False
				for szPart in aParts:
					if self.normTipText(szPart) == self.normTipText(szTerrain):
						bKnown = True
				if not bKnown:
					aParts.append(szTerrain)
		except:
			pass
		if len(aParts) == 0:
			return u"(%d, %d)" % (pPlot.getX(), pPlot.getY())
		return u"/".join(aParts)

	# the new name from the window to rename a waypoint: "2. name" puts it at the place 2 of the list (the others move, the numbers stay continuous),
	# a name without a number keeps its place
	def applyWaypointRename( self, ePlayer, iId, szNew ):
		try:
			bSea = False
			(aWp, iNext) = self.getWaypoints(ePlayer, False)
			iAt = -1
			for k in range(len(aWp)):
				if aWp[k][0] == iId:
					iAt = k
			if iAt < 0:
				bSea = True
				(aWp, iNext) = self.getWaypoints(ePlayer, True)
				for k in range(len(aWp)):
					if aWp[k][0] == iId:
						iAt = k
			if iAt < 0:
				return
			tWp = aWp[iAt]
			szName = szNew.strip()
			iPlace = -1
			tMatch = re.match(u"^([0-9]+)\\s*\\.\\s*(.*)$", szName, re.UNICODE)
			if tMatch is not None:
				iPlace = max(0, int(tMatch.group(1)) - 1)
				szName = tMatch.group(2).strip()
			if len(szName) == 0:
				szName = tWp[3]
			# the names of the colonies are protected: also with a number in front ("3 Plymouth", "3. Plymouth")
			if self.getOwnColonyAt(tWp[1], tWp[2], ePlayer) is None and self.isColonyName(szName, ePlayer):
				self.showModMessage(localText.getText("TXT_KEY_WTP_WAYPOINT_NAME_COLONY", (szName,)))
				return
			del aWp[iAt]
			iInsert = iAt
			if iPlace >= 0:
				# (the number counts the waypoints without a colony: the place among them)
				aPlain = []
				for k in range(len(aWp)):
					if self.getOwnColonyAt(aWp[k][1], aWp[k][2], ePlayer) is None:
						aPlain.append(k)
				if iPlace < len(aPlain):
					iInsert = aPlain[iPlace]
				else:
					iInsert = len(aWp)
			aWp.insert(iInsert, (tWp[0], tWp[1], tWp[2], szName))
			self.saveWaypoints(aWp, iNext, ePlayer, bSea)
			self.refreshWaypointLists()
		except:
			pass
	# the waypoint that is chosen (the line under the cursor of a list, or the line of the list that the wheel has chosen on the line "Set
	# waypoint..."): the camera looks at its plot; the unit stays selected; the frozen window of the line goes there as well (it keeps its distance)
	def jumpToSelectedWaypoint( self, iFz, iPara, iSel, bWpLine, aWpStops, bWpRow, iRowChild, aChildKeys ):
		tWpJ = self.dWpWin.get(self.aFrozen[iFz][0])
		if tWpJ is None:
			return u"the line is no line of waypoints"
		iId = -1
		if bWpLine:
			iP = iPara
			if iSel >= 0 and iSel < len(aWpStops):
				iP = aWpStops[iSel][0]
			kind = tWpJ["paras"].get(iP)
			if isinstance(kind, int):
				iId = kind
		elif bWpRow and iSel > 0:
			if iRowChild >= 0:
				if iSel < len(aChildKeys) and self.dWpWin.has_key(self.aFrozen[iRowChild][0]):
					kind = self.dWpWin[self.aFrozen[iRowChild][0]]["paras"].get(aChildKeys[iSel])
					if isinstance(kind, int):
						iId = kind
			else:
				aViewJ = self.getWaypointView(tWpJ["sea"])
				if iSel - 1 < len(aViewJ):
					iId = aViewJ[iSel - 1][0]
		if iId < 0:
			return u"no waypoint is chosen (Shift + mouse wheel chooses one)"
		for tEntry in self.getWaypointView(tWpJ["sea"]):
			if tEntry[0] == iId:
				# the child window of the cursor is frozen for the jump: it goes with its parent window to the new place
				try:
					# (not for the list of waypoints: its window beside the line is only the help, every jump would freeze one more of them)
					if self.bSecondTipShown and not bWpLine:
						self.freezePreview(CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE))
				except:
					pass
				CyCamera().JustLookAtPlot(CyMap().plot(tEntry[1], tEntry[2]))
				self.tJump = (tEntry[1], tEntry[2], (self.getTipNow() / 1000.0))
				# (no message in the panel for a jump, only the sound)
				try:
					CyInterface().playGeneralSound(self.szModJumpSound)
				except:
					pass

				# the cursor goes with the window under it (the same place of the same line)
				try:
					(iWX, iWY) = self.aFrozen[iFz][1][:2]
					self.tCursorFollow = [self.aFrozen[iFz][0], gc.getGame().getCursorClientX() - iWX, gc.getGame().getCursorClientY() - iWY, (self.getTipNow() / 1000.0), -1, -1, 0]
				except:
					self.tCursorFollow = None
				iRoot = iFz
				for k in range(10):
					if self.aFrozen[iRoot][6] < 0:
						break
					iRoot = self.aFrozen[iRoot][6]
				tA = self.aFrozen[iRoot][5]
				if tA is not None:
					self.aFrozen[iRoot][5] = (tEntry[1], tEntry[2], tA[2], tA[3])
				return u""
		return u"waypoint not found"

	# left click on the line of a frozen child window: the child window goes again (with the windows that belong to it); the windows after it
	# keep their places in the list
	def closeFrozenChild( self, screen, iChild ):
		try:
			aRemove = [iChild]
			if iChild + 1 < len(self.aFrozen) and self.dFrozenCompanion.has_key(self.aFrozen[iChild + 1][0]):
				aRemove.append(iChild + 1)
			bMore = True
			while bMore:
				bMore = False
				for i in range(len(self.aFrozen)):
					if not (i in aRemove) and self.aFrozen[i][6] in aRemove:
						aRemove.append(i)
						bMore = True
			aNew = []
			dMap = {}
			aGone = []
			for i in range(len(self.aFrozen)):
				if i in aRemove:
					aGone.append(self.aFrozen[i][0])
					self.deleteTipWindow(screen, self.aFrozen[i][0], len(self.aFrozen[i][1][4]))
				else:
					dMap[i] = len(aNew)
					aNew.append(self.aFrozen[i])
			for tFz in aNew:
				if tFz[6] >= 0:
					tFz[6] = dMap.get(tFz[6], -1)
			self.aFrozen[:] = aNew
			for tKey in self.dRowChild.keys():
				if self.dRowChild[tKey] in aGone or tKey[0] in aGone:
					del self.dRowChild[tKey]
			for szGone in aGone:
				if self.dFrozenCompanion.has_key(szGone):
					del self.dFrozenCompanion[szGone]
			self.tSecondTipKey = None
			self.iTipSelPara = -1
			self.bTipFrozen = (len(self.aFrozen) > 0)
			self.redrawFrozenTips(screen)
		except:
			pass

	def onTipLineLeftClick( self, iData ):
		try:
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			iLevel = iData / 1000
			iPara = iData % 1000
			# a line of a colony in the tooltip of a good of the import / export window: the jump to it
			if self.tryTraderJump(iLevel, iPara):
				return
			# the name line of the tooltip of an own city: the jump to the next city
			if self.tryCityListJump(iLevel, iPara, True):
				return
			# a window with waypoints: the left click on the line of a waypoint jumps to it (the update of the frozen windows knows which one is chosen);
			# when it is no waypoint (the line "Set waypoint..."), the click does what it always did
			if iLevel >= 0 and iLevel < len(self.aFrozen) and self.dWpWin.has_key(self.aFrozen[iLevel][0]):
				self.tLeftClick = (iLevel, iPara, (self.getTipNow() / 1000.0))
				self.bLeftJumped = False
				try:
					self.updateFrozenTip()
				except:
					pass
				self.tLeftClick = None
				if self.bLeftJumped:
					self.bLeftJumped = False
					return
			if iLevel >= 0 and iLevel < len(self.aFrozen):
				szKey = (self.aFrozen[iLevel][0], iPara)
				szChild = self.dRowChild.get(szKey)
				if szChild is not None:
					# (the line has a frozen child window: it goes again)
					for i in range(len(self.aFrozen)):
						if self.aFrozen[i][0] == szChild and self.aFrozen[i][6] == iLevel:
							self.closeFrozenChild(screen, i)
							return
					del self.dRowChild[szKey]
			if self.bSecondTipShown:
				self.freezePreview(screen)
		except:
			pass

	# the frozen lists of waypoints are written again after a waypoint was deleted or renamed (they stay where they are, their size follows)
	def refreshWaypointLists( self ):
		try:
			if self.bMsgWpView:
				self.tMessagePanelKey = None
				self.updateMessagePanel()
		except:
			pass
		try:
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			for i in range(len(self.aFrozen)):
				szPrefix = self.aFrozen[i][0]
				tWp = self.dWpWin.get(szPrefix)
				if tWp is None or not self.isWaypointList(tWp):
					continue
				aView = self.getWaypointView(tWp["sea"])
				iStart = 0
				if not ("new" in tWp["paras"].values()):
					# (a later page of the list: it begins with the first waypoint that it has)
					for iP in tWp["paras"].keys():
						if not isinstance(tWp["paras"][iP], tuple):
							for k in range(len(aView)):
								if aView[k][0] == tWp["paras"][iP] and (iStart == 0 or k < iStart):
									iStart = k
				if iStart >= len(aView):
					iStart = 0
				aParas = []
				dParas = {}
				if iStart == 0:
					aParas.append(localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_NEW", ()))
					dParas[0] = "new"
				iEnd = min(len(aView), iStart + 5)
				for k in range(iStart, iEnd):
					dParas[len(aParas)] = aView[k][0]
					aParas.append(aView[k][4])
				if iEnd < len(aView):
					dParas[len(aParas)] = ("more", iEnd)
					aParas.append(localText.getText("TXT_KEY_WTP_TIP_MORE", ()))
				(iX, iY, iW, iH, aszLines, aiPara, iPad, iLine) = self.aFrozen[i][1]
				iTail = len(aiPara)
				while iTail > 0 and aiPara[iTail - 1] < 0:
					iTail -= 1
				aszTail = list(aszLines[iTail:])
				aszNew = self.carryColors(aParas) + aszTail
				aiNew = range(len(aParas)) + [-1] * len(aszTail)
				iChar = iLine * 0.32
				iWidth = self.getTipTextWidth(aszNew, iChar, max(300, int(screen.getXResolution() * 0.2)), iPad)
				iHeight = len(aszNew) * iLine + 2 * iPad
				iNX = max(4, min(screen.getXResolution() - iWidth - 4, iX))
				iNY = max(4, min(screen.getYResolution() - iHeight - 4, iY))
				tNew = (iNX, iNY, iWidth, iHeight, aszNew, aiNew, iPad, iLine)
				self.deleteTipWindow(screen, szPrefix, len(aszLines))
				self.aFrozen[i][1] = tNew
				self.aFrozen[i][2] = aParas
				self.aFrozen[i][3] = [0] * len(aszNew)
				tWp["paras"] = dParas
				if tWp.has_key("plain"):
					del tWp["plain"]
				tWp["marked"] = -1
				self.drawTipWindow(screen, szPrefix, tNew, True, i, self.aFrozen[i][3], self.dFrozenDark.has_key(szPrefix))
			self.tSecondTipKey = None
		except:
			pass

	# the own unit that a frozen window of a tooltip belongs to: the window of one unit alone (None: a stack, a city, ...)
	def getWaypointRowUnit( self, iLevel ):
		try:
			if iLevel < 0 or iLevel >= len(self.aFrozen) or self.aFrozen[iLevel][6] >= 0:
				return None
			aszParas = self.aFrozen[iLevel][2]
			tAnchor = self.aFrozen[iLevel][5]
			if tAnchor is not None:
				pPlot = CyMap().plot(tAnchor[0], tAnchor[1])
			else:
				pPlot = self.getStackPlot()
			iPlotStart = self.getPlotStartPara(aszParas, pPlot)
			iHead = -1
			iHeaders = 0
			for k in range(iPlotStart):
				if self.isUnitHeader(aszParas[k]):
					iHeaders += 1
					if iHead < 0:
						iHead = k
			if iHeaders == 0:
				return None
			if iHeaders >= 2:
				# a stack: the unit that is selected (the one that the game shows), otherwise the first own unit of the plot
				eActive = gc.getGame().getActivePlayer()
				if pPlot is None or pPlot.isNone():
					return None
				pHead = CyInterface().getHeadSelectedUnit()
				if pHead is not None and not pHead.isNone() and pHead.getOwner() == eActive and pHead.getX() == pPlot.getX() and pHead.getY() == pPlot.getY():
					return pHead
				for k in range(pPlot.getNumUnits()):
					if pPlot.getUnit(k).getOwner() == eActive:
						return pPlot.getUnit(k)
				return None
			return self.getHeaderUnit(iLevel, aszParas, iHead)
		except:
			pass
		return None

	# the paragraph of the line "Commands" of a tooltip (that has a child window), -1 if there is none
	def getCommandsPara( self, aszParas, dDetails ):
		szCmd = self.normTipText(localText.getText("TXT_KEY_WTP_TIP_COMMANDS", ()))
		for k in range(len(aszParas)):
			if dDetails.has_key(k) and self.normTipText(re.sub(u"<[^>]*>", u"", aszParas[k])) == szCmd:
				return k
		return -1

	# the row of the promotion pictures of a unit, also with its XP (foldUnitDetails puts the XP into that row)
	def isPromoOrXpRow( self, szText ):
		if self.isPromotionRow(szText):
			return True
		szPlain = re.sub(u"[^,<:()>]{1,10}:\\s*\\(\\s*[0-9]+\\s*/\\s*[0-9]+\\s*\\)", u"", szText)
		return szPlain != szText and self.isPromotionRow(szPlain)

	# the paragraph where the line "Set waypoint..." of a unit goes: directly below the row of its promotions, without that row directly below
	# its name (iHead: the paragraph of the name, -1: the first unit of the tooltip)
	def getWaypointSlot( self, aszParas, iHead = -1 ):
		if iHead < 0:
			for k in range(len(aszParas)):
				if self.isUnitHeader(aszParas[k]):
					iHead = k
					break
		if iHead < 0:
			return len(aszParas)
		iSlot = iHead + 1
		# (the line "commanded by" of a unit with a leader belongs to the lines of the name: the row goes below it)
		szCommanded = self.normTipText(localText.getText("TXT_KEY_UNIT_HELP_COMMANDED_BY", ()))
		for k in range(2):
			if iSlot >= len(aszParas):
				break
			if self.isPromoOrXpRow(aszParas[iSlot]):
				iSlot += 1
			elif len(szCommanded) > 3 and self.normTipText(aszParas[iSlot]).find(szCommanded) == 0:
				iSlot += 1
			else:
				break
		return iSlot

	# the tooltip at the cursor (not frozen yet) of one own unit without the line "Commands": the registration of its line "Set waypoint..."
	# (the paragraph is added by the caller), otherwise None
	def getHoverWaypointRow( self, aszParas, dDetails ):
		if self.getCommandsPara(aszParas, dDetails) >= 0:
			return None
		# (a temporary window: the functions that find the unit of a tooltip look at the frozen windows)
		self.aFrozen.append([u"", (0, 0, 0, 0, [], [], 0, 0), list(aszParas), [], {}, self.makeAnchor((0, 0)), -1, None])
		try:
			pUnit = self.getWaypointRowUnit(len(self.aFrozen) - 1)
		finally:
			self.aFrozen.pop()
		if pUnit is None or pUnit.isNone() or pUnit.getOwner() != gc.getGame().getActivePlayer():
			return None
		return {"unit": (pUnit.getOwner(), pUnit.getID()), "sea": self.isSeaUnit(pUnit), "paras": {}, "cmd": -1}

	# the line "Set waypoint..." in the frozen window iLevel (of the tooltip of the unit): a paragraph above the hint at the end, or the first line
	# of the child window of the line "Commands"
	def addWaypointRow( self, screen, iLevel, pUnit ):
		try:
			if pUnit is None or pUnit.isNone() or pUnit.getOwner() != gc.getGame().getActivePlayer():
				return
			szPrefix = self.aFrozen[iLevel][0]
			tLayout = self.aFrozen[iLevel][1]
			aszParas = list(self.aFrozen[iLevel][2])
			aiIndent = list(self.aFrozen[iLevel][3])
			dDetails = dict(self.aFrozen[iLevel][4])
			szRow = localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_SET", ())
			szRowOwn = localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_SET_ROW", ())
			dReg = {"unit": (pUnit.getOwner(), pUnit.getID()), "sea": self.isSeaUnit(pUnit), "paras": {}, "cmd": -1}
			szCmd = self.normTipText(localText.getText("TXT_KEY_WTP_TIP_COMMANDS", ()))
			iCmd = -1
			for k in range(len(aszParas)):
				if dDetails.has_key(k) and self.normTipText(re.sub(u"<[^>]*>", u"", aszParas[k])) == szCmd:
					iCmd = k
					break
			if iCmd >= 0:
				dDetails[iCmd] = szRow + u"\n" + dDetails[iCmd]
				dReg["cmd"] = iCmd
				self.aFrozen[iLevel][4] = dDetails
			else:
				# directly below the promotions of the unit (below its name without them); no unit header: above the hint lines at the end
				iHead = -1
				bHeaders = False
				for k in range(len(aszParas)):
					if self.isUnitHeader(aszParas[k]):
						bHeaders = True
						pHeader = self.getHeaderUnit(iLevel, aszParas, k)
						if pHeader is not None and not pHeader.isNone() and pHeader.getID() == pUnit.getID() and pHeader.getOwner() == pUnit.getOwner():
							iHead = k
							break
				if bHeaders and iHead < 0:
					# (the unit has no name line in this window, e.g. it is in the groups of "more...units": no row, it would be under another unit)
					return
				if iHead >= 0:
					iPara = self.getWaypointSlot(aszParas, iHead)
				else:
					iPara = len(aszParas)
				szRow = szRowOwn
				aszParas.insert(iPara, szRow)
				(iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine) = tLayout
				iChar = iLine * 0.32
				aszRow = self.wrapMessage(szRow, max(20, int((iWidth - 2 * iPad) / iChar)))
				iAt = len(aiPara)
				while iAt > 0 and aiPara[iAt - 1] < 0:
					iAt -= 1
				if iHead >= 0:
					iAt = len(aiPara)
					for k in range(len(aiPara)):
						if aiPara[k] >= iPara:
							iAt = k
							break
					aiShift = []
					for x in aiPara:
						if x >= iPara:
							aiShift.append(x + 1)
						else:
							aiShift.append(x)
					aiPara = aiShift
					dMapIns = {}
					for kOld in range(len(aszParas) - 1):
						if kOld >= iPara:
							dMapIns[kOld] = kOld + 1
						else:
							dMapIns[kOld] = kOld
					self.remapFrozenParas(iLevel, dMapIns)
				aszLines = list(aszLines[:iAt]) + aszRow + list(aszLines[iAt:])
				aiPara = list(aiPara[:iAt]) + [iPara] * len(aszRow) + list(aiPara[iAt:])
				aiIndent = list(aiIndent[:iAt]) + [0] * len(aszRow) + list(aiIndent[iAt:])
				iHeight += iLine * len(aszRow)
				iWidth = max(iWidth, self.getTipTextWidth(aszRow, iChar, int(iWidth * 1.3), iPad))
				iNY = max(4, min(screen.getYResolution() - iHeight - 4, iY))
				iNX = max(4, min(screen.getXResolution() - iWidth - 4, iX))
				tNew = (iNX, iNY, iWidth, iHeight, aszLines, aiPara, iPad, iLine)
				tAnchor = self.aFrozen[iLevel][5]
				if tAnchor is not None:
					tAnchor = (tAnchor[0], tAnchor[1], tAnchor[2] + iNX - iX, tAnchor[3] + iNY - iY)
				self.deleteTipWindow(screen, szPrefix, len(tLayout[4]))
				self.aFrozen[iLevel][1] = tNew
				self.aFrozen[iLevel][2] = aszParas
				self.aFrozen[iLevel][3] = aiIndent
				self.aFrozen[iLevel][5] = tAnchor
				self.drawTipWindow(screen, szPrefix, tNew, True, iLevel, aiIndent, self.dFrozenDark.has_key(szPrefix))
				dReg["paras"][iPara] = "row"
			self.dWpWin[szPrefix] = dReg
		except:
			self.tipError("addWaypointRow")

	# the paragraphs of a frozen window changed (a line was inserted, removed, the units were put in another order): everything that is kept per
	# paragraph of that window follows. dMap: old paragraph -> new paragraph (-1: the paragraph is gone), for every old paragraph
	def remapFrozenParas( self, iLevel, dMap ):
		szPrefix = self.aFrozen[iLevel][0]
		# the details of the lines (child windows)
		dDetails = self.aFrozen[iLevel][4]
		dNew = {}
		for kDet in dDetails.keys():
			iNew = dMap.get(kDet, kDet)
			if iNew >= 0:
				dNew[iNew] = dDetails[kDet]
		self.aFrozen[iLevel][4] = dNew
		# the lines of waypoints
		dReg = self.dWpWin.get(szPrefix)
		if dReg is not None:
			dParas = {}
			for kReg in dReg["paras"].keys():
				iNew = dMap.get(kReg, kReg)
				if iNew >= 0:
					dParas[iNew] = dReg["paras"][kReg]
			dReg["paras"] = dParas
			if dReg.get("cmd", -1) >= 0:
				dReg["cmd"] = dMap.get(dReg["cmd"], dReg["cmd"])
			if dReg.get("marked", -1) >= 0:
				dReg["marked"] = dMap.get(dReg["marked"], dReg["marked"])
		# the frozen child windows of the lines
		dChild = {}
		for tKey in self.dRowChild.keys():
			if tKey[0] == szPrefix:
				dChild[tKey] = self.dRowChild[tKey]
		for tKey in dChild.keys():
			del self.dRowChild[tKey]
		for tKey in dChild.keys():
			iNew = dMap.get(tKey[1], tKey[1])
			if iNew >= 0:
				self.dRowChild[(szPrefix, iNew)] = dChild[tKey]
		# the unit of each name
		dHeads = self.dHeaderUnits.get(szPrefix)
		if dHeads is not None:
			dNewHeads = {}
			for kHead in dHeads.keys():
				iNew = dMap.get(kHead, kHead)
				if iNew >= 0:
					dNewHeads[iNew] = dHeads[kHead]
			self.dHeaderUnits[szPrefix] = dNewHeads
		# the line under the cursor
		if self.tSecondTipKey is not None and self.tSecondTipKey[0] == iLevel and dMap.has_key(self.tSecondTipKey[1]):
			tOldKey = self.tSecondTipKey
			self.tSecondTipKey = (tOldKey[0], dMap[tOldKey[1]]) + tuple(tOldKey[2:])
		if self.iTipSelLevel == iLevel and self.iTipSelPara >= 0:
			self.iTipSelPara = dMap.get(self.iTipSelPara, self.iTipSelPara)

	# a unit of a stack was selected: in the frozen windows of that stack the line "Set waypoint..." goes to the selected unit (it stands
	# below the active unit)
	def refreshWaypointRows( self, screen, pSelect ):
		try:
			for iLevel in range(len(self.aFrozen)):
				if self.aFrozen[iLevel][6] >= 0:
					continue
				tAnchor = self.aFrozen[iLevel][5]
				if tAnchor is None or tAnchor[0] < 0:
					continue
				pPlot = CyMap().plot(tAnchor[0], tAnchor[1])
				if pPlot is None or pPlot.isNone() or pPlot.getX() != pSelect.getX() or pPlot.getY() != pSelect.getY():
					continue
				if self.dWpWin.has_key(self.aFrozen[iLevel][0]):
					self.moveWaypointRow(screen, iLevel, pSelect)
				self.moveUnitToTop(screen, iLevel, pSelect)
		except:
			self.tipError("refreshWaypointRows")

	# the active unit stands at the start of the list of units of a stack tooltip: the block of the selected unit (its name, its promotions, its
	# lines) goes to the start of the frozen window (the other blocks keep their order, the lines after the units stay)
	def moveUnitToTop( self, screen, iLevel, pUnit ):
		try:
			szPrefix = self.aFrozen[iLevel][0]
			aszParas = list(self.aFrozen[iLevel][2])
			dDetails = self.aFrozen[iLevel][4]
			tAnchor = self.aFrozen[iLevel][5]
			pPlot = CyMap().plot(tAnchor[0], tAnchor[1])
			iPlotStart = self.getPlotStartPara(aszParas, pPlot)
			aHeads = []
			for k in range(iPlotStart):
				if self.isUnitHeader(aszParas[k]):
					aHeads.append(k)
			if len(aHeads) < 2:
				return
			# (the region of the units ends at the line "more...units" or "Commands")
			iCmd = self.getCommandsPara(aszParas, dDetails)
			iEnd = iPlotStart
			for k in range(aHeads[0], iPlotStart):
				if k == iCmd or (dDetails.has_key(k) and dDetails[k].find(u"@WTPUNITS") == 0):
					iEnd = k
					break
			aHeads = [k for k in aHeads if k < iEnd]
			if len(aHeads) < 2:
				return
			iBlock = -1
			for i in range(len(aHeads)):
				pHeader = self.getHeaderUnit(iLevel, aszParas, aHeads[i])
				if pHeader is not None and not pHeader.isNone() and pHeader.getID() == pUnit.getID() and pHeader.getOwner() == pUnit.getOwner():
					iBlock = i
					break
			if iBlock <= 0:
				return
			aBounds = []
			for i in range(len(aHeads)):
				if i + 1 < len(aHeads):
					aBounds.append((aHeads[i], aHeads[i + 1]))
				else:
					aBounds.append((aHeads[i], iEnd))
			aOrder = range(aHeads[0])
			aBlocks = [aBounds[iBlock]] + aBounds[:iBlock] + aBounds[iBlock + 1:]
			for tB in aBlocks:
				aOrder += range(tB[0], tB[1])
			aOrder += range(iEnd, len(aszParas))
			dMap = {}
			for i in range(len(aOrder)):
				dMap[aOrder[i]] = i
			(iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine) = self.aFrozen[iLevel][1]
			aiIndent = self.aFrozen[iLevel][3]
			# the lines of the region must be one piece
			iFrom = -1
			iTo = -1
			for k in range(len(aiPara)):
				if aiPara[k] >= aHeads[0] and aiPara[k] < iEnd:
					if iFrom < 0:
						iFrom = k
					iTo = k
			if iFrom < 0:
				return
			for k in range(iFrom, iTo + 1):
				if aiPara[k] < aHeads[0] or aiPara[k] >= iEnd:
					return
			dLines = {}
			for k in range(iFrom, iTo + 1):
				if not dLines.has_key(aiPara[k]):
					dLines[aiPara[k]] = []
				dLines[aiPara[k]].append(k)
			aNewLines = list(aszLines[:iFrom])
			aNewPara = list(aiPara[:iFrom])
			aNewIndent = list(aiIndent[:iFrom])
			for iOld in aOrder[aHeads[0]:iEnd]:
				for k in dLines.get(iOld, []):
					aNewLines.append(aszLines[k])
					aNewPara.append(dMap[iOld])
					aNewIndent.append(aiIndent[k])
			aNewLines += list(aszLines[iTo + 1:])
			aNewPara += list(aiPara[iTo + 1:])
			aNewIndent += list(aiIndent[iTo + 1:])
			aszNew = [aszParas[i] for i in aOrder]
			tNew = (iX, iY, iWidth, iHeight, aNewLines, aNewPara, iPad, iLine)
			self.deleteTipWindow(screen, szPrefix, len(aszLines))
			self.aFrozen[iLevel][1] = tNew
			self.aFrozen[iLevel][2] = aszNew
			self.aFrozen[iLevel][3] = aNewIndent
			self.remapFrozenParas(iLevel, dMap)
			self.drawTipWindow(screen, szPrefix, tNew, True, iLevel, aNewIndent, self.dFrozenDark.has_key(szPrefix))
			try:
				# the cursor was on a line of the units (the right click that selected the unit): it goes to the name line of the unit, that is at
				# the start of the list now (the line "Set waypoint..." moved to this unit before: no line below the name); the child window of
				# the unit (beside the line, frozen next) goes with it
				iCurX = gc.getGame().getCursorClientX()
				iCurY = gc.getGame().getCursorClientY()
				if iCurX >= iX and iCurX < iX + iWidth and iCurY >= iY + iPad and iCurY < iY + iPad + len(aszLines) * iLine:
					iOldLine = int((iCurY - iY - iPad) / iLine)
					if iOldLine >= iFrom and iOldLine <= iTo:
						iNewY = iY + iPad + iFrom * iLine + iLine / 2
						gc.getGame().setCursorClient(iCurX, iNewY)
						# (the line that the window is frozen for is the name line at the start of the list now: the frozen child window is
						# registered for it, no second one comes for the line under the cursor)
						iKeySel = -1
						if self.tSecondTipKey is not None:
							iKeySel = self.tSecondTipKey[2]
						self.tSecondTipKey = (iLevel, aHeads[0], iKeySel, iFrom, False)
						if self.bSecondTipShown and self.tPreviewLayout is not None:
							tP = self.tPreviewLayout
							iPNewY = max(4, min(screen.getYResolution() - tP[3] - 4, tP[1] + (iNewY - iCurY)))
							self.iPreviewPrefDY += iPNewY - tP[1]
							self.tPreviewLayout = (tP[0], iPNewY, tP[2], tP[3], tP[4], tP[5], tP[6], tP[7])
			except:
				pass
		except:
			self.tipError("moveUnitToTop")

	def moveWaypointRow( self, screen, iLevel, pUnit ):
		try:
			szPrefix = self.aFrozen[iLevel][0]
			dOld = self.dWpWin[szPrefix]
			tUnit = (pUnit.getOwner(), pUnit.getID())
			if dOld["unit"] == tUnit:
				return
			aRows = [k for k in dOld["paras"].keys() if dOld["paras"][k] == "row"]
			if dOld["cmd"] >= 0 or len(aRows) != 1:
				# (the row is the first line of the child window of "Commands": only its unit changes)
				dOld["unit"] = tUnit
				dOld["sea"] = self.isSeaUnit(pUnit)
				return
			iOld = aRows[0]
			(iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine) = self.aFrozen[iLevel][1]
			aiIndent = self.aFrozen[iLevel][3]
			aszParas = list(self.aFrozen[iLevel][2])
			dDetails = self.aFrozen[iLevel][4]
			self.deleteTipWindow(screen, szPrefix, len(aszLines))
			aszNewLines = []
			aiNewPara = []
			aiNewIndent = []
			for k in range(len(aszLines)):
				if aiPara[k] == iOld:
					iHeight -= iLine
					continue
				aszNewLines.append(aszLines[k])
				if aiPara[k] > iOld:
					aiNewPara.append(aiPara[k] - 1)
				else:
					aiNewPara.append(aiPara[k])
				aiNewIndent.append(aiIndent[k])
			dMapRem = {}
			for kOld in range(len(aszParas)):
				if kOld == iOld:
					dMapRem[kOld] = -1
				elif kOld > iOld:
					dMapRem[kOld] = kOld - 1
				else:
					dMapRem[kOld] = kOld
			aszParas.pop(iOld)
			self.aFrozen[iLevel][1] = (iX, iY, iWidth, iHeight, aszNewLines, aiNewPara, iPad, iLine)
			self.aFrozen[iLevel][2] = aszParas
			self.aFrozen[iLevel][3] = aiNewIndent
			self.remapFrozenParas(iLevel, dMapRem)
			del self.dWpWin[szPrefix]
			self.addWaypointRow(screen, iLevel, pUnit)
		except:
			self.tipError("moveWaypointRow")

	# is the frozen window a list of waypoints (not the line "Set waypoint..." alone)?
	def isWaypointList( self, tWp ):
		for k in tWp["paras"].keys():
			if tWp["paras"][k] == "row":
				return False
		return len(tWp["paras"]) > 0

	# the places that shift + mouse wheel stops at in a list of waypoints: (paragraph, choice): -1 for "New waypoint" and "more...", the choices
	# 0 start, 1 delete, 2 rename for a waypoint
	def getWaypointStops( self, tWp ):
		aStops = []
		aKeys = tWp["paras"].keys()
		aKeys.sort()
		for iP in aKeys:
			kind = tWp["paras"][iP]
			# (one stop per line: start, delete and rename are chosen with the keys)
			aStops.append((iP, -1))
		return aStops

	# the line of the list that the wheel has chosen is yellow (iPara -1: no line, the lines have their colors again)
	def markWaypointLine( self, screen, iLevel, iPara ):
		try:
			# (the window that was marked before: back to its colors)
			for szOld in self.dWpMarked.keys():
				if iLevel < 0 or iLevel >= len(self.aFrozen) or self.aFrozen[iLevel][0] != szOld:
					for i in range(len(self.aFrozen)):
						if self.aFrozen[i][0] == szOld:
							self.paintWaypointLines(screen, i, -1)
					del self.dWpMarked[szOld]
			if iLevel >= 0 and iLevel < len(self.aFrozen):
				if self.paintWaypointLines(screen, iLevel, iPara) and iPara >= 0:
					self.dWpMarked[self.aFrozen[iLevel][0]] = True
		except:
			pass

	def paintWaypointLines( self, screen, iLevel, iPara ):
		try:
			szPrefix = self.aFrozen[iLevel][0]
			tWp = self.dWpWin.get(szPrefix)
			if tWp is None:
				# (a window without lines of waypoints, e.g. the commands of a unit: its own place to keep the lines as they were)
				if len(self.dPaintPlain) > 200:
					self.dPaintPlain = {}
				tWp = self.dPaintPlain.setdefault(szPrefix, {})
			(iX, iY, iW, iH, aszLines, aiPara, iPad, iLine) = self.aFrozen[iLevel][1]
			if not tWp.has_key("plain") or len(tWp["plain"]) != len(aszLines):
				tWp["plain"] = list(aszLines)
			aNew = []
			for i in range(len(aszLines)):
				szLine = tWp["plain"][i]
				if iPara >= 0 and aiPara[i] == iPara:
					szLine = u"<color=255,255,0,255>" + re.sub(u"<color=[^>]*>|</color>", u"", szLine) + u"</color>"
				aNew.append(szLine)
			if aNew == list(aszLines):
				return True
			tNew = (iX, iY, iW, iH, aNew, aiPara, iPad, iLine)
			self.deleteTipWindow(screen, szPrefix, len(aszLines))
			self.aFrozen[iLevel][1] = tNew
			self.drawTipWindow(screen, szPrefix, tNew, True, iLevel, self.aFrozen[iLevel][3], self.dFrozenDark.has_key(szPrefix))
			return True
		except:
			pass
		return False

	# a line of a saved waypoint in a frozen window (its choices: start, delete, rename): the number of the waypoint, otherwise -1
	def getWaypointLineId( self, iLevel, iPara ):
		try:
			tWp = self.dWpWin.get(self.aFrozen[iLevel][0])
			if tWp is not None and tWp["paras"].has_key(iPara):
				kind = tWp["paras"][iPara]
				if not isinstance(kind, tuple) and kind != "row" and kind != "new":
					return kind
		except:
			pass
		return -1

	# the child window of a line of waypoints (hovering): the list of the waypoints (5 on a page, the line "more..." opens the next page), or
	# what a right click does
	def showWaypointTip( self, screen, iLevel, tWp, iPara, iCursorY, tAnchor, iSel = -1, iEntry = -1 ):
		kind = tWp["paras"][iPara]
		if kind == "row" or isinstance(kind, tuple):
			aView = self.getWaypointView(tWp["sea"])
			aLines = []
			dParas = {}
			iStart = 0
			if kind == "row":
				# (iEntry: the line that the wheel has chosen, 0 "New waypoint", then the waypoints; the page of the list follows it)
				if iEntry > 0:
					iStart = ((iEntry - 1) / 5) * 5
				if iStart == 0:
					aLines.append(localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_NEW", ()))
					dParas[0] = "new"
			else:
				iStart = kind[1]
			iEnd = min(len(aView), iStart + 5)
			for k in range(iStart, iEnd):
				dParas[len(aLines)] = aView[k][0]
				aLines.append(aView[k][4])
			if iEnd < len(aView):
				dParas[len(aLines)] = ("more", iEnd)
				aLines.append(localText.getText("TXT_KEY_WTP_TIP_MORE", ()))
			dMarked = -1
			dMarkedText = u""
			if kind == "row" and iEntry >= 0:
				if iEntry == 0:
					iMarked = 0
				else:
					iMarked = iEntry - 1 - iStart
					if iStart == 0:
						iMarked += 1
				if iMarked >= 0 and iMarked < len(aLines):
					dMarkedText = aLines[iMarked]
					aLines[iMarked] = u"<color=255,255,0,255>" + re.sub(u"<color=[^>]*>|</color>", u"", aLines[iMarked]) + u"</color>"
					dMarked = iMarked
			szListHint = localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_WHEEL", ())
			if len(aView) > 0:
				# (what Ctrl / Shift + right click and the wheel click do with a waypoint)
				szListHint = szListHint + u"\n" + localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_KEYS", ())
			self.showSecondTip(screen, u"\n".join(aLines), iCursorY, tAnchor, iLevel)
			if self.bSecondTipShown:
				# the hints are in a window of their own beside the parent (as the explanation of the colors of the goods), without the hint of the freezing
				self.showFoldExplain(screen, szListHint, tAnchor, False)
				self.tPreviewWp = {"unit": tWp["unit"], "sea": tWp["sea"], "paras": dParas, "cmd": -1, "marked": dMarked, "markedText": dMarkedText}
		elif kind == "new":
			self.showSecondTip(screen, localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_NEW_HELP", ()), iCursorY, tAnchor, iLevel)
		else:
			# the choices of a saved waypoint: start, delete, rename (then the hint of the wheel); shift + mouse wheel chooses one, a right click runs it
			aLines = localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_OPTIONS", ()).split(u"\n")
			if iSel >= 0 and iSel < 3 and iSel < len(aLines):
				aLines[iSel] = u"<color=255,255,0,255>" + aLines[iSel] + u"</color>"
			self.showSecondTip(screen, u"\n".join(aLines), iCursorY, tAnchor, iLevel)

	# right click (Ctrl: the second choice, Shift: the third) on a line of waypoints of a frozen window: True if the click was for a waypoint
	def runWaypointClick( self, iLevel, iPara, bSecond, bShift = False, iOption = -1, kindOverride = None ):
		try:
			tWp = self.dWpWin.get(self.aFrozen[iLevel][0])
			if tWp is None or not tWp["paras"].has_key(iPara):
				return False
			kind = tWp["paras"][iPara]
			if kindOverride is not None:
				# (the line of the list that was chosen with the wheel on the line "Set waypoint...")
				kind = kindOverride
			if isinstance(kind, tuple):
				# (the line "more...": it only opens the next page when the cursor is on it)
				return True
			pUnit = gc.getPlayer(tWp["unit"][0]).getUnit(tWp["unit"][1])
			if pUnit is None or pUnit.isNone():
				return True
			if kind == "row" or kind == "new":
				# (the line "Set waypoint..." itself: a new waypoint at once)
				self.startWaypointMode(pUnit)
				return True
			(aWp, iNext) = self.getWaypoints(-1, tWp["sea"])
			# the choice: the one chosen with shift + mouse wheel (0 start, 1 delete, 2 rename), otherwise the modifier keys
			if iOption < 0:
				if bShift:
					iOption = 2
				elif bSecond:
					iOption = 1
				else:
					iOption = 0
			for k in range(len(aWp)):
				if aWp[k][0] == kind:
					if iOption == 2:
						# rename: the small window (the frozen windows stay, the lists are written again when the name is applied)
						CvEventInterface.beginEvent(CvUtil.EventRenameWaypoint, (aWp[k][0], self.getWaypointTextById(tWp["sea"], aWp[k][0])))
					elif iOption == 1:
						# (delete; the numbers of the others close up)
						del aWp[k]
						self.saveWaypoints(aWp, iNext, -1, tWp["sea"])
						self.refreshWaypointLists()
					else:
						# (first choice: start)
						CyInterface().selectUnit(pUnit, True, False, False)
						self.markTipSelection()
						self.unfreezeAllTips()
						self.sendUnitToPlot(pUnit, aWp[k][1], aWp[k][2])
					break
			return True
		except:
			pass
		return False

	def sendUnitToPlot( self, pUnit, iX, iY ):
		try:
			CyMessageControl().sendPushMission(pUnit.getID(), MissionTypes.MISSION_MOVE_TO, iX, iY, 0, False)
		except:
			try:
				pPlot = CyMap().plot(iX, iY)
				pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iX, iY, 0, False, True, MissionAITypes.NO_MISSIONAI, pPlot, pUnit)
			except:
				pass

	# a unit was selected in a tooltip: for a moment the selection does not count as a change (the list of the waypoints of the message panel
	# stays open, see updateMessageScroll)
	def markTipSelection( self ):
		self.fTipSelectAt = (self.getTipNow() / 1000.0)

	# "New waypoint": the unit is selected, the target of its next order to move is saved (for one minute)
	def startWaypointMode( self, pUnit ):
		CyInterface().selectUnit(pUnit, True, False, False)
		self.markTipSelection()
		self.iWpUnit = pUnit.getID()
		self.fWpStart = (self.getTipNow() / 1000.0)
		self.unfreezeAllTips()

	# the preview window of a line of a unit: its hint "Right click: Select ..." goes (the unit is selected now)
	def dropPreviewSelectHint( self ):
		try:
			(iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine) = self.tPreviewLayout
			iHints = self.iPreviewHintLines - self.iPreviewFreezeLines
			if iHints <= 0:
				return
			iTo = len(aszLines) - self.iPreviewFreezeLines
			iFrom = iTo - iHints
			if iFrom < 0:
				return
			for k in range(iFrom, iTo):
				if aiPara[k] >= 0:
					return
			aszNew = list(aszLines[:iFrom]) + list(aszLines[iTo:])
			aiNew = list(aiPara[:iFrom]) + list(aiPara[iTo:])
			self.tPreviewLayout = (iX, iY, iWidth, iHeight - iLine * iHints, aszNew, aiNew, iPad, iLine)
			self.iPreviewHintLines = self.iPreviewFreezeLines
		except:
			self.tipError("dropPreviewSelectHint")

	# a unit of the player is activated (event "unitSelected"): the tooltip of the plot under the cursor is frozen as soon as it shows (stack or
	# single unit); it goes with the first order of the unit
	def onUnitActivated( self, pUnit ):
		try:
			if not self.bTipAutoFreeze or not self.bHoverTip or pUnit is None or pUnit.isNone() or pUnit.getOwner() != gc.getGame().getActivePlayer():
				return
			if self.getFrozenAt(gc.getGame().getCursorClientX(), gc.getGame().getCursorClientY()) >= 0:
				# (selected from a frozen window: it keeps its own handling)
				return
			pMouse = CyInterface().getMouseOverPlot()
			if pMouse is None or pMouse.isNone() or pMouse.getX() != pUnit.getX() or pMouse.getY() != pUnit.getY():
				return
			if len(self.szAutoSelPrefix) > 0:
				self.closeAutoSelWindows()
			self.tAutoFreeze = None
			if len(self.aFrozen) == 0:
				self.tAutoFreeze = (pUnit.getX(), pUnit.getY(), self.getTipNow(), (pUnit.getOwner(), pUnit.getID()))
		except:
			self.tipError("onUnitActivated")

	# the window that the choice is for: the tooltip of the cursor (-2), a frozen tooltip of the good under the cursor (its index; after a jump
	# the tooltip of the good is frozen), -1: none
	def getTradeTipTarget( self ):
		try:
			if not self.isTradeWindowOpen():
				return -1
			iCX = gc.getGame().getCursorClientX()
			iCY = gc.getGame().getCursorClientY()
			iYield = CvScreensInterface.tradeRouteScreen.getIconYieldAt(iCX, iCY)
			if iYield < 0 or self.getFrozenAt(iCX, iCY) >= 0:
				return -1
			for i in range(len(self.aFrozen)):
				if self.dTraderWin.get(self.aFrozen[i][0], -1) == iYield:
					return i
			if self.bCursorTipShown and self.tTipLayout is not None and self.iTradeTipYield == iYield and self.szCursorTipText == self.szTradeTipText:
				return -2
		except:
			pass
		return -1

	def getTradeTipStops( self, iTarget ):
		if iTarget >= 0:
			aszParas = self.aFrozen[iTarget][2]
			dDetails = self.aFrozen[iTarget][4]
		else:
			aszParas = self.aszTipParas
			dDetails = self.dTipDetails
		aStops = []
		for k in range(len(aszParas)):
			if dDetails.has_key(k) or self.dTraderLines.has_key(self.normTipText(aszParas[k])) or self.dNetLines.has_key(self.normTipText(aszParas[k])):
				aStops.append(k)
		return aStops

	def getTradeTipDetail( self, iTarget, iPara ):
		if iTarget >= 0:
			szDetail = self.aFrozen[iTarget][4].get(iPara)
			aszParas = self.aFrozen[iTarget][2]
			iYield = self.dTraderWin.get(self.aFrozen[iTarget][0], -1)
		else:
			szDetail = self.dTipDetails.get(iPara)
			aszParas = self.aszTipParas
			iYield = self.iTradeTipYield
		if szDetail is None and iYield >= 0 and iPara >= 0 and iPara < len(aszParas):
			# (a line of a colony: its export settings for the good and its stock)
			iCity = self.dTraderLines.get(self.normTipText(aszParas[iPara]))
			if iCity is not None:
				szTrader = self.getTraderChildText(iYield, iCity)
				if len(szTrader) > 0:
					return szTrader
			if self.dNetLines.has_key(self.normTipText(aszParas[iPara])):
				return self.getNetHelpText(iYield)
		return szDetail

	# the child tooltip of the line of a colony in the tooltip of a good (import / export window): the name of the colony, its export settings
	# for the good as the letters E (export), A (auto export), L (land), S (sea), and for an importing colony I (import), F (feeder), L, S - those
	# that are on in the colony are yellow - and the stock
	def getTraderChildText( self, iYield, iCity ):
		try:
			pCity = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(iCity)
			if pCity is None or pCity.isNone():
				return u""
			bExp = pCity.isExport(iYield)
			bAuto = pCity.isAutoExport(iYield)
			iDom = pCity.getExportDomains(iYield)
			bImp = pCity.isImport(iYield)
			bFeeder = pCity.isImportFeeder(iYield)
			iImpDom = pCity.getImportDomains(iYield)
			tWin = CvScreensInterface.tradeRouteScreen
			if tWin.isOpen() and tWin.iCity == iCity and tWin.dData.has_key(iYield):
				# (the colony of the open window: what the window shows is the newer state)
				d = tWin.dData[iYield]
				bExp = d["exp"]
				bAuto = d["auto"]
				iDom = d["expDom"]
				bImp = d["imp"]
				bFeeder = d["feeder"]
				iImpDom = d["impDom"]
			szLines = pCity.getName()
			# (the settings of what the colony does with the good: the import row if it imports, the export row if it exports; the letters that are on
			# are yellow)
			# (the letters of each language are in the text keys, 4 letters divided by slashes, e.g. I/F/L/S)
			aRows = []
			if bImp:
				aRows.append((localText.getText("TXT_KEY_WTP_TIP_TRADER_IMPORT_SETTINGS", ()), localText.getText("TXT_KEY_WTP_TIP_TRADER_IMPORT_LETTERS", ()), [bImp, bFeeder, (iImpDom & 1) != 0, (iImpDom & 2) != 0]))
			if bExp or not bImp:
				aRows.append((localText.getText("TXT_KEY_WTP_TIP_TRADER_EXPORT_SETTINGS", ()), localText.getText("TXT_KEY_WTP_TIP_TRADER_EXPORT_LETTERS", ()), [bExp, bAuto, (iDom & 1) != 0, (iDom & 2) != 0]))
			for tRow in aRows:
				aLetters = tRow[1].split(u"/")
				aParts = []
				for i in range(len(aLetters)):
					if i < len(tRow[2]) and tRow[2][i]:
						aParts.append(u"<color=255,255,0,255>" + aLetters[i] + u"</color>")
					else:
						aParts.append(aLetters[i])
				szLines += u"\n" + tRow[0] + u": " + u"/".join(aParts)
			szLines += u"\n" + localText.getText("TXT_KEY_WTP_TIP_TRADER_STOCK", (pCity.getYieldStored(iYield),)) + u" " + unichr(gc.getYieldInfo(iYield).getChar())
			# (the planned use of the good in the colony, also when nothing is used up at the moment because another raw material is missing completely:
			# the same number as the line "converted to" in the tooltip of the good inside the city)
			if iYield != YieldTypes.YIELD_FOOD:
				iPlannedUse = pCity.getRawYieldConsumed(iYield)
				if iPlannedUse > 0:
					szLines += u"\n" + localText.getText("TXT_KEY_WTP_TIP_TRADER_USE", (u"<color=255,0,0,255>-%d</color>" % iPlannedUse,)) + u" " + unichr(gc.getYieldInfo(iYield).getChar())
			# (the production of the good per turn, what is left after the colony's own use: green with a plus sign, red when negative)
			iNet = pCity.calculateNetYield(iYield)
			if iNet > 0:
				szNet = u"<color=0,255,0,255>+%d</color>" % iNet
			elif iNet < 0:
				szNet = u"<color=255,0,0,255>%d</color>" % iNet
			else:
				szNet = u"0"
			szLines += u"\n" + localText.getText("TXT_KEY_WTP_TIP_TRADER_NET", (szNet,)) + u" " + unichr(gc.getYieldInfo(iYield).getChar())
			# (how many of this raw material are missing in the colony for the full production: the same calculation as the line in the tooltip of the
			# raw material inside the city, see CvGameTextMgr::setYieldHelp: what the workers want to use up, minus the stock and what the colony makes of it)
			if iYield != YieldTypes.YIELD_FOOD:
				iMissingRaw = pCity.getRawYieldConsumed(iYield) - pCity.getYieldStored(iYield) - pCity.calculateActualYieldProduced(iYield) * pCity.getBaseYieldRateModifier(iYield, 0) / 100
				if iMissingRaw > 0:
					szLines += u"\n" + localText.getText("TXT_KEY_WTP_TIP_TRADER_RAW_MISSING", (-iMissingRaw, unichr(gc.getYieldInfo(iYield).getChar())))
			return szLines
		except:
			self.tipError("getTraderChildText")
		return u""

	# the mouse wheel capture of the tooltips (Shift + wheel): with the import / export window open it is not simply switched off, the window
	# decides (it needs the wheel while the cursor is in it)
	def setWheelCapture( self, bOn ):
		try:
			if not bOn and CvScreensInterface.tradeRouteScreen.isOpen():
				CvScreensInterface.tradeRouteScreen.updateWheelCapture()
				return
		except:
			pass
		gc.getGame().setWheelCapture(bOn)

	# a tooltip takes the wheel just now (the import / export window leaves it alone)
	def isTipWheelActive( self ):
		return self.bTipWheel or self.bTradeSel or getattr(self, "bMsgWheel", False)

	def clearTradeTipSelect( self, screen ):
		try:
			if self.bTradeSel:
				self.bTradeSel = False
				self.bTipWheel = False
				self.setWheelCapture(False)
			if self.bTradeChild:
				self.bTradeChild = False
				self.hideSecondTip(screen)
			if len(self.szTradeMarkedWin) > 0:
				# (a frozen tooltip: its yellow line goes)
				for i in range(len(self.aFrozen)):
					if self.aFrozen[i][0] == self.szTradeMarkedWin:
						self.markWaypointLine(screen, i, -1)
				self.szTradeMarkedWin = u""
			self.iTradeSel = -1
			self.iTradeMarked = -1
			self.szTradeSelFor = u""
		except:
			self.tipError("clearTradeTipSelect")

	def updateTradeTipSelect( self ):
		try:
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			iTarget = self.getTradeTipTarget()
			if iTarget == -1:
				if self.iTradeSel >= 0 or self.bTradeSel or self.bTradeChild or len(self.szTradeMarkedWin) > 0:
					self.clearTradeTipSelect(screen)
				return
			if iTarget >= 0:
				szFor = self.aFrozen[iTarget][0]
			else:
				szFor = self.szCursorTipText
			if self.szTradeSelFor != szFor:
				# (another tooltip: the choice starts again)
				if self.szTradeSelFor != u"":
					self.clearTradeTipSelect(screen)
				self.szTradeSelFor = szFor
			aStops = self.getTradeTipStops(iTarget)
			bWheel = gc.getGame().isShiftKeyPressed() and len(aStops) > 0
			if bWheel != self.bTradeSel:
				self.bTradeSel = bWheel
				self.bTipWheel = bWheel
				self.setWheelCapture(bWheel)
			if bWheel:
				iNotches = gc.getGame().takeWheelNotches()
				if iNotches != 0:
					if self.iTradeSel < 0 or self.iTradeSel >= len(aStops):
						self.iTradeSel = 0
					else:
						# (the wheel towards the user: the next one, away from the user: the one before)
						self.iTradeSel = (self.iTradeSel - iNotches) % len(aStops)
			iMark = -1
			if self.iTradeSel >= 0 and self.iTradeSel < len(aStops):
				iMark = aStops[self.iTradeSel]
			bRedo = (iMark != self.iTradeMarked)
			if not bRedo and iMark >= 0 and iTarget >= 0:
				# (the frozen windows are painted again when the cursor goes over their lines: the choice stays yellow)
				bRedo = not self.dWpMarked.has_key(self.aFrozen[iTarget][0])
			if bRedo:
				self.markTradeTipLine(screen, iMark, iTarget)
			elif self.bTradeChild and not self.bSecondTipShown:
				self.markTradeTipLine(screen, iMark, iTarget)
		except:
			self.tipError("updateTradeTipSelect")

	# the chosen paragraph in yellow (-1: none); its child window beside the tooltip
	def markTradeTipLine( self, screen, iMark, iTarget ):
		if iTarget >= 0:
			(iX, iY, iW, iH, aszLines, aiPara, iPad, iLine) = self.aFrozen[iTarget][1]
			self.markWaypointLine(screen, iTarget, iMark)
			self.szTradeMarkedWin = self.aFrozen[iTarget][0]
		else:
			(iX, iY, iW, iH, aszLines, aiPara, iPad, iLine) = self.tTipLayout
			aNew = []
			for i in range(len(aszLines)):
				szLine = aszLines[i]
				if iMark >= 0 and aiPara[i] == iMark:
					szLine = u"<color=255,255,0,255>" + re.sub(u"<color=[^>]*>|</color>", u"", szLine) + u"</color>"
				aNew.append(szLine)
			self.deleteTipWindow(screen, "HudTip", len(aszLines))
			self.drawTipWindow(screen, "HudTip", (iX, iY, iW, iH, aNew, aiPara, iPad, iLine), False, 0, self.aiTipIndent)
		self.iTradeMarked = iMark
		if self.bTradeChild or self.bSecondTipShown:
			self.bTradeChild = False
			self.hideSecondTip(screen)
		iFirst = -1
		for i in range(len(aiPara)):
			if aiPara[i] == iMark:
				iFirst = i
				break
		szDetail = None
		if iMark >= 0:
			szDetail = self.getTradeTipDetail(iTarget, iMark)
		if szDetail is not None and iFirst >= 0:
			if iTarget >= 0:
				# (the child window of this line is frozen already: no second one)
				szChild = self.dRowChild.get((self.aFrozen[iTarget][0], iMark))
				if szChild is not None:
					for i in range(len(self.aFrozen)):
						if self.aFrozen[i][0] == szChild:
							return
				self.showSecondTip(screen, szDetail, iY + iPad + iFirst * iLine, self.aFrozen[iTarget][1], iTarget)
			else:
				self.showSecondTip(screen, szDetail, iY + iPad + iFirst * iLine, self.tTipLayout)
			self.bTradeChild = self.bSecondTipShown

	# right click on the picture of the good: runs the chosen line (True), False: there is none
	def runTradeTipSelection( self ):
		try:
			if self.iTradeSel < 0:
				return False
			iTarget = self.getTradeTipTarget()
			if iTarget == -1:
				return False
			aStops = self.getTradeTipStops(iTarget)
			if self.iTradeSel >= len(aStops):
				return False
			iPara = aStops[self.iTradeSel]
			szDetail = self.getTradeTipDetail(iTarget, iPara)
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			self.clearTradeTipSelect(screen)
			self.hideSecondTip(screen)
			if iTarget == -2:
				# (the tooltip of the cursor is frozen first, as for a click on its line)
				if not self.freezeCursorTooltip() or len(self.aFrozen) == 0:
					return False
				iTarget = len(self.aFrozen) - 1
			if self.tryTraderJump(iTarget, iPara):
				return True
			if szDetail is not None:
				szChild = self.dRowChild.get((self.aFrozen[iTarget][0], iPara))
				if szChild is not None:
					for i in range(len(self.aFrozen)):
						if self.aFrozen[i][0] == szChild:
							return True
				aiFPara = self.aFrozen[iTarget][1][5]
				iLineIdx = 0
				if iPara in aiFPara:
					iLineIdx = aiFPara.index(iPara)
				iLayY = self.aFrozen[iTarget][1][1] + self.aFrozen[iTarget][1][6] + iLineIdx * self.aFrozen[iTarget][1][7]
				self.showSecondTip(screen, szDetail, iLayY, self.aFrozen[iTarget][1], iTarget)
				if self.bSecondTipShown:
					self.tSecondTipKey = (iTarget, iPara, -1, iLineIdx, False)
					self.freezePreview(screen)
			return True
		except:
			self.tipError("runTradeTipSelection")
		return False

	# left click on the picture of a good of the import / export window: the tooltip that is shown for it is frozen (like X), a click on the
	# picture of a good whose tooltip is frozen releases that tooltip (with the windows that belong to it)
	def toggleTradeTipFreeze( self ):
		try:
			if not self.isTradeWindowOpen():
				return False
			iYield = CvScreensInterface.tradeRouteScreen.getIconYieldAt(gc.getGame().getCursorClientX(), gc.getGame().getCursorClientY())
			if iYield < 0:
				return False
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			for i in range(len(self.aFrozen)):
				if self.dTraderWin.get(self.aFrozen[i][0], -1) == iYield:
					self.clearTradeTipSelect(screen)
					self.closeFrozenChild(screen, i)
					return True
			if self.bCursorTipShown and self.tTipLayout is not None and self.iTradeTipYield == iYield and self.szCursorTipText == self.szTradeTipText:
				self.clearTradeTipSelect(screen)
				self.freezeCursorTooltip()
				return True
			if self.szPendingHelp is not None and self.iTradeTipYield == iYield:
				# (the tooltip still waits for its delay: the click shows it frozen at once)
				self.pressX()
				return True
		except:
			self.tipError("toggleTradeTipFreeze")
		return False

	def updateAutoFreeze( self ):
		try:
			tAuto = self.tAutoFreeze
			if tAuto is None:
				return
			if self.getTipNow() - tAuto[2] > 5000:
				self.tAutoFreeze = None
				return
			if len(self.aFrozen) > 0 or self.bHudHover or not self.bCursorTipShown:
				return
			pMouse = CyInterface().getMouseOverPlot()
			if pMouse is None or pMouse.isNone() or pMouse.getX() != tAuto[0] or pMouse.getY() != tAuto[1]:
				self.tAutoFreeze = None
				return
			# (the tooltip must have been built after the activation, or still be the help text of the plot: no old tooltip of something else)
			if self.fCursorTipShownAt < tAuto[2] and CyInterface().getHelpString() != self.szCursorTipText:
				return
			self.tAutoFreeze = None
			if self.freezeCursorTooltip() and len(self.aFrozen) > 0:
				self.szAutoSelPrefix = self.aFrozen[-1][0]
				self.tAutoSelUnit = tAuto[3]
		except:
			self.tAutoFreeze = None
			self.tipError("updateAutoFreeze")

	# the frozen tooltip of the unit that a right click selected from a stack, and the stack tooltip that it belongs to
	def closeAutoSelWindows( self ):
		try:
			iFound = -1
			for i in range(len(self.aFrozen)):
				if self.aFrozen[i][0] == self.szAutoSelPrefix:
					iFound = i
					break
			self.szAutoSelPrefix = u""
			self.tAutoSelUnit = None
			if iFound < 0:
				return
			iRoot = iFound
			for k in range(10):
				if self.aFrozen[iRoot][6] < 0:
					break
				iRoot = self.aFrozen[iRoot][6]
			self.closeFrozenChild(CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE), iRoot)
		except:
			self.tipError("closeAutoSelWindows")

	# called by the game for every order that the player gives to a group (CvEventManager.onSelectionGroupPushMission)
	def onWaypointMission( self, eOwner, eMission, aUnitIds = None ):
		try:
			if len(self.szAutoSelPrefix) > 0 and eOwner == gc.getGame().getActivePlayer():
				# an order for the unit that was selected from a stack tooltip: the frozen tooltips of the stack go (an order for other units does
				# not close them)
				if aUnitIds is None or self.tAutoSelUnit is None or (self.tAutoSelUnit[1] in aUnitIds):
					self.closeAutoSelWindows()
		except:
			self.tipError("onWaypointMission")
		try:
			if self.iWpUnit < 0:
				return
			if eOwner != gc.getGame().getActivePlayer() or (self.getTipNow() / 1000.0) - self.fWpStart > 60:
				self.iWpUnit = -1
				return
			pHead = CyInterface().getHeadSelectedUnit()
			if pHead is None or pHead.isNone() or pHead.getID() != self.iWpUnit or eMission != MissionTypes.MISSION_MOVE_TO:
				# another unit or another order: the waypoint mode is over
				self.iWpUnit = -1
				return
			pPlot = pHead.getGroup().lastMissionPlot()
			if pPlot is None or pPlot.isNone():
				return
			self.iWpUnit = -1
			bSea = self.isSeaUnit(pHead)
			(aWp, iNext) = self.getWaypoints(-1, bSea)
			iNext += 1
			# (the new waypoint is the last of the list of the ships or of the land units: its number follows the existing ones)
			aWp.append((iNext, pPlot.getX(), pPlot.getY(), self.getWaypointLabel(pPlot)))
			self.saveWaypoints(aWp, iNext, -1, bSea)
			self.showModMessage(localText.getText("TXT_KEY_WTP_WAYPOINT_SAVED", (self.getWaypointTextById(bSea, iNext),)), None, (pPlot.getX(), pPlot.getY()))
			# the name is always asked for (the window of the rename with the suggested name, only OK); not for an own colony: its name is fixed.
			# The window opens in the next frame (see updatePendingWpRename), not in the middle of the order of the game
			if self.getOwnColonyAt(pPlot.getX(), pPlot.getY()) is None:
				self.tWpRenamePending = (iNext, bSea)
		except:
			self.iWpUnit = -1

	# the window to name a new waypoint (the rename window with the suggested name: OK takes it, or the player changes it first)
	def updatePendingWpRename( self ):
		if self.tWpRenamePending is None:
			return
		(iId, bSea) = self.tWpRenamePending
		self.tWpRenamePending = None
		try:
			szText = self.getWaypointTextById(bSea, iId)
			if len(szText) > 0:
				CvEventInterface.beginEvent(CvUtil.EventRenameWaypoint, (iId, szText))
		except:
			pass

	def getOverflowForecastText( self, pCity ):
		# the goods that the storage overflow (or the sale threshold of a custom house) takes at the next turn change, and the gold of their sale:
		# the forecast comes from the DLL, the same calculation as the turn change (None: nothing is lost, or the DLL has no forecast)
		try:
			aiForecast = pCity.getStorageOverflowForecast()
		except:
			return None
		iNum = YieldTypes.NUM_YIELD_TYPES
		if len(aiForecast) < 2 * iNum:
			return None
		aLines = []
		iGold = 0
		for iYield in range(iNum):
			iLoss = aiForecast[iYield]
			if iLoss <= 0:
				continue
			iYieldGold = aiForecast[iNum + iYield]
			iGold += iYieldGold
			szIcon = u"%c" % gc.getYieldInfo(iYield).getChar()
			szName = gc.getYieldInfo(iYield).getDescription()
			if iYieldGold > 0:
				aLines.append(localText.getText("TXT_KEY_WTP_TIP_OVERFLOW_SOLD", (szIcon, szName, iLoss, iYieldGold)))
			else:
				aLines.append(localText.getText("TXT_KEY_WTP_TIP_OVERFLOW_LOST", (szIcon, szName, iLoss)))
		if len(aLines) == 0:
			return None
		aLines.insert(0, localText.getText("TXT_KEY_WTP_TIP_OVERFLOW_HEAD", ()))
		if iGold > 0:
			aLines.append(localText.getText("TXT_KEY_WTP_TIP_OVERFLOW_TOTAL", (iGold, )))
		return u"\n".join(aLines)

	def drawTipWindow( self, screen, szPrefix, tLayout, bClickable, iLevel, aiIndent, bDark = False ):
		(iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine) = tLayout
		screen.addPanel(szPrefix + "Back1", u"", u"", True, False, iX, iY, iWidth, iHeight, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel(szPrefix + "Back2", u"", u"", True, False, iX, iY, iWidth, iHeight, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, -1, -1)
		# over an element of the HUD (the panel style is semi-transparent) one more layer, as the expanded message panel has
		bOverHud = self.isTipOverHud(screen, iX, iY, iWidth, iHeight)
		if self.isTradeWindowOpen():
			# (with the import / export window open all tooltips are the darker variant)
			bDark = True
		if bDark:
			# (the darker variant, as over an element of the HUD, wherever the window is)
			bOverHud = True
		if bOverHud:
			screen.addPanel(szPrefix + "Back3", u"", u"", True, False, iX, iY, iWidth, iHeight, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, -1, -1)
		for i in range(len(aszLines)):
			eWidget = WidgetTypes.WIDGET_GENERAL
			iData1 = -1
			iData2 = -1
			if bClickable and aiPara[i] >= 0 and aszLines[i].lower().find(u"<img=") < 0:
				iData1 = self.BUTTON_TIP_LINE
				iData2 = iLevel * 1000 + aiPara[i]
			iIndent = 0
			if i < len(aiIndent):
				iIndent = aiIndent[i]
			screen.setText(szPrefix + "Line%d" % i, "Background", self.setFontSize(aszLines[i], -1), CvUtil.FONT_LEFT_JUSTIFY, iX + iPad + iIndent, iY + iPad + i * iLine, -0.3, FontTypes.SMALL_FONT, eWidget, iData1, iData2)
		for szName in self.getTipWindowNames(szPrefix, len(aszLines)):
			if szName == szPrefix + "Back3" and not bOverHud:
				continue
			screen.show(szName)
			screen.moveToFront(szName)

	# does the window cover an element of the HUD (the bars at the top and bottom, the unit panel, the minimap, the score table)?
	def isTipOverHud( self, screen, iX, iY, iWidth, iHeight ):
		try:
			xRes = screen.getXResolution()
			yRes = screen.getYResolution()
			if iY + iHeight > yRes - max(UPPER_SADDLE_HEIGHT, BOTTOM_CENTER_HUD_HEIGHT):
				return True
			# the top of the screen (the advisor buttons, gold, date)
			if iY < max(TOP_CORNER_HUD_HEIGHT, TOP_CENTER_HUD_HEIGHT):
				return True
			if iX + iWidth > xRes - LOWER_RIGHT_CORNER_BACKGROUND_WIDTH and iY + iHeight > yRes - LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT:
				return True
			if self.tScoreRect is not None:
				(iSX, iSY, iSW, iSH) = self.tScoreRect
				if iX < iSX + iSW and iX + iWidth > iSX and iY < iSY + iSH and iY + iHeight > iSY:
					return True
		except:
			pass
		return False

	# the hint line at the end of a frozen window (wrapped to the width of the window: the window does not get wider because of it)
	def addFrozenHint( self, screen, tLayout, aiIndent, szKey = "TXT_KEY_WTP_TIP_FROZEN_HINT" ):
		(iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine) = tLayout
		szHint = localText.getText(szKey, ())
		iChar = iLine * 0.32
		aszHint = self.wrapMessage(szHint, max(20, int((iWidth - 2 * iPad) / iChar)))
		aszLines = list(aszLines) + aszHint
		aiPara = list(aiPara) + [-1] * len(aszHint)
		aiIndent = list(aiIndent) + [0] * len(aszHint)
		iHeight += iLine * len(aszHint)
		iWidth = max(iWidth, self.getTipTextWidth(aszHint, iChar, int(iWidth * 1.3), iPad))
		iY = max(4, min(screen.getYResolution() - iHeight - 4, iY))
		iX = max(4, min(screen.getXResolution() - iWidth - 4, iX))
		return ((iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine), aiIndent)

	# NESTED TOOLTIPS. The key X (short press) freezes the tooltip that is shown: it stays where it is, the cursor can be moved onto it and a
	# right click on a line opens the Colopedia page of the first thing named in it (Ctrl: the second). The window beside it (the tooltip of
	# the line under the cursor) can be frozen with X as well, and so on. Esc unfreezes the last frozen window, X held (0.6 s) all of them.
	def keyXDown( self ):
		# False: the key is not ours (no tooltip), the game gets it
		try:
			if self.isPediaActive():
				return False
			if not (self.bTipFrozen or self.bCursorTipShown or self.szPendingHelp is not None or self.isTradeStackOpen()):
				return False
			if not self.bXHeld:
				self.bXHeld = True
				self.bXHoldDone = False
				self.fXStart = self.getTipNow()
			return True
		except:
			return False

	def keyXUp( self ):
		if not self.bXHeld:
			return False
		self.bXHeld = False
		if self.bXHoldDone:
			return True
		try:
			self.pressX()
		except:
			pass
		return True

	# short press of X: the window beside a frozen one is frozen; otherwise the tooltip that is shown at the cursor (several can be frozen, to
	# compare them)
	def pressX( self ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		if self.bSecondTipShown:
			self.freezePreview(screen)
		elif self.szPendingHelp is not None:
			# the tooltip still waits for its delay: X shows it at once
			szHelp = self.szPendingHelp
			bWidget = self.bPendingWidget
			self.szPendingHelp = None
			self.showCursorTooltip(screen, szHelp, bWidget, True)
		elif self.bCursorTipShown:
			self.freezeCursorTooltip()

	# a frozen window: its widgets get names of their own, its lines can be clicked
	def addFrozenWindow( self, screen, tLayout, aszParas, aiIndent, dDetails, tAnchor = None, iParent = -1, bDark = False ):
		iLevel = len(self.aFrozen)
		self.iFzCounter += 1
		szPrefix = "HudFz%d" % self.iFzCounter
		if bDark:
			self.dFrozenDark[szPrefix] = True
		self.drawTipWindow(screen, szPrefix, tLayout, True, iLevel, aiIndent, self.dFrozenDark.has_key(szPrefix))
		tRel = None
		if iParent >= 0:
			# a child window keeps its place to its parent window
			tRel = (tLayout[0] - self.aFrozen[iParent][1][0], tLayout[1] - self.aFrozen[iParent][1][1])
		self.aFrozen.append([szPrefix, tLayout, aszParas, aiIndent, dDetails, tAnchor, iParent, tRel])
		self.bTipFrozen = True
		try:
			# (the unit of every name: the tooltip lists the units in the order of the moment, a later selection must not change that)
			if iParent < 0 and tAnchor is not None:
				dHeads = {}
				for k in range(len(aszParas)):
					if self.isUnitHeader(aszParas[k]):
						pHead = self.getHeaderUnit(iLevel, aszParas, k, True)
						if pHead is not None and not pHead.isNone():
							dHeads[k] = (pHead.getOwner(), pHead.getID())
				if len(self.dHeaderUnits) > 100:
					dKeep = {}
					for tFz in self.aFrozen:
						if self.dHeaderUnits.has_key(tFz[0]):
							dKeep[tFz[0]] = self.dHeaderUnits[tFz[0]]
					self.dHeaderUnits = dKeep
				if len(dHeads) > 0:
					self.dHeaderUnits[szPrefix] = dHeads
		except:
			self.tipError("addFrozenWindow")

	# after the game window was activated again (alt-tab) the widgets of the frozen windows are gone: they are drawn again a few frames later
	def windowActivated( self ):
		if len(self.aFrozen) > 0:
			self.iRedrawFrozen = 6

	def redrawFrozenTips( self, screen ):
		try:
			for i in range(len(self.aFrozen)):
				szPrefix = self.aFrozen[i][0]
				tLayout = self.aFrozen[i][1]
				self.deleteTipWindow(screen, szPrefix, len(tLayout[4]))
				self.drawTipWindow(screen, szPrefix, tLayout, True, i, self.aFrozen[i][3], self.dFrozenDark.has_key(szPrefix))
		except:
			pass

	# the place of a map plot on the screen
	def getPlotScreen( self, iPlotX, iPlotY ):
		pt = CyEngine().worldPointToScreenPoint(CyMap().plot(iPlotX, iPlotY).getPoint())
		return (int(pt.x), int(pt.y))

	# A window frozen at the map stays at that place of the map (it moves with the map when that is scrolled or zoomed): the anchor is the
	# plot under the cursor and the distance of the window to the place of that plot on the screen. None: the window stays on the screen.
	def makeAnchor( self, tLayout, tPlot = None ):
		try:
			if tPlot is None:
				if self.bHudHover:
					return None
				pPlot = CyInterface().getMouseOverPlot()
				if pPlot is None or pPlot.isNone():
					return None
				tPlot = (pPlot.getX(), pPlot.getY())
			(iSX, iSY) = self.getPlotScreen(tPlot[0], tPlot[1])
			return (tPlot[0], tPlot[1], tLayout[0] - iSX, tLayout[1] - iSY)
		except:
			return None

	# a frozen window moves to a place (its widgets are drawn again)
	def moveFrozenWindow( self, screen, i, iNX, iNY ):
		tLayout = self.aFrozen[i][1]
		# a window is pushed along by the edges of the screen (all four), the place of the map it belongs to is kept (see updateFrozenAnchors)
		iNX = max(4, min(screen.getXResolution() - tLayout[2] - 4, iNX))
		iNY = max(4, min(screen.getYResolution() - tLayout[3] - 4, iNY))
		if iNX == tLayout[0] and iNY == tLayout[1]:
			return
		szPrefix = self.aFrozen[i][0]
		self.deleteTipWindow(screen, szPrefix, len(tLayout[4]))
		tNew = (iNX, iNY, tLayout[2], tLayout[3], tLayout[4], tLayout[5], tLayout[6], tLayout[7])
		self.aFrozen[i][1] = tNew
		self.drawTipWindow(screen, szPrefix, tNew, True, i, self.aFrozen[i][3], self.dFrozenDark.has_key(szPrefix))

	# every frame: the frozen windows of the map follow the map, the child windows follow their parent window
	def updateFrozenAnchors( self, screen ):
		xRes = screen.getXResolution()
		yRes = screen.getYResolution()
		# the windows that do not move with the map are obstacles for the others; the others are placed one after the other (the older one first,
		# a child window after its parent) and a window that would lie on or touch one that is placed already is pushed away from it
		aPlaced = []
		for i in range(len(self.aFrozen)):
			if self.aFrozen[i][6] < 0 and self.aFrozen[i][5] is None:
				aPlaced.append(self.aFrozen[i][1][:4])
		for i in range(len(self.aFrozen)):
			iParent = self.aFrozen[i][6]
			tAnchor = self.aFrozen[i][5]
			try:
				if iParent >= 0 or tAnchor is not None:
					tLayout = self.aFrozen[i][1]
					if iParent >= 0:
						iNX = self.aFrozen[iParent][1][0] + self.aFrozen[i][7][0]
						iNY = self.aFrozen[iParent][1][1] + self.aFrozen[i][7][1]
					else:
						(iSX, iSY) = self.getPlotScreen(tAnchor[0], tAnchor[1])
						iNX = iSX + tAnchor[2]
						iNY = iSY + tAnchor[3]
					iNX = max(4, min(xRes - tLayout[2] - 4, iNX))
					iNY = max(4, min(yRes - tLayout[3] - 4, iNY))
					(iNX, iNY) = self.pushOutOfWindows(iNX, iNY, tLayout[2], tLayout[3], aPlaced, xRes, yRes)
					self.moveFrozenWindow(screen, i, iNX, iNY)
					aPlaced.append(self.aFrozen[i][1][:4])
			except:
				pass

	# a window at (iX, iY) that lies on a window of the list or comes closer than a few pixels to it goes to the nearest place beside, above or
	# below that window that is on the screen (again and again, for the next window it touches); the windows of the frozen tooltips never overlap
	def pushOutOfWindows( self, iX, iY, iW, iH, aRects, xRes, yRes ):
		iGap = 6
		for iTry in range(8):
			tHit = None
			for tRect in aRects:
				(iRX, iRY, iRW, iRH) = tRect
				if iX < iRX + iRW + iGap and iX + iW > iRX - iGap and iY < iRY + iRH + iGap and iY + iH > iRY - iGap:
					tHit = tRect
					break
			if tHit is None:
				return (iX, iY)
			(iRX, iRY, iRW, iRH) = tHit
			aCands = [(iRX - iW - iGap, iY), (iRX + iRW + iGap, iY), (iX, iRY - iH - iGap), (iX, iRY + iRH + iGap)]
			tBest = None
			iBest = 0
			for (iCX, iCY) in aCands:
				if iCX < 4 or iCY < 4 or iCX + iW > xRes - 4 or iCY + iH > yRes - 4:
					continue
				iDist = abs(iCX - iX) + abs(iCY - iY)
				if tBest is None or iDist < iBest:
					tBest = (iCX, iCY)
					iBest = iDist
			if tBest is None:
				# (no side has room: the nearest one, pushed back onto the screen)
				for (iCX, iCY) in aCands:
					iCX = max(4, min(xRes - iW - 4, iCX))
					iCY = max(4, min(yRes - iH - 4, iCY))
					iDist = abs(iCX - iX) + abs(iCY - iY)
					if tBest is None or iDist < iBest:
						tBest = (iCX, iCY)
						iBest = iDist
			if tBest[0] == iX and tBest[1] == iY:
				return (iX, iY)
			(iX, iY) = tBest
		return (iX, iY)

	# Shift + X: the frozen parent windows are brought to the cursor and stacked diagonally there, each one below the one before and beside it
	# (to the left, to the right if there is no room), so that the child windows beside them do not get in the way of each other. The oldest
	# window is at the cursor.
	def stackFrozenTips( self ):
		try:
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			aiParents = []
			for i in range(len(self.aFrozen)):
				if self.aFrozen[i][6] < 0:
					aiParents.append(i)
			if len(aiParents) < 1:
				return len(self.aFrozen) > 0
			# the first window goes to the cursor, the others are stacked from there
			self.moveFrozenWindow(screen, aiParents[0], gc.getGame().getCursorClientX(), gc.getGame().getCursorClientY() + self.getCursorBottom(screen.getYResolution()))
			tFirst = self.aFrozen[aiParents[0]][1]
			iNeeded = 0
			for i in aiParents[1:]:
				iNeeded += self.aFrozen[i][1][2] + 8
			bLeft = (tFirst[0] - iNeeded >= 4)
			iPrevX = tFirst[0]
			iPrevY = tFirst[1]
			iPrevW = tFirst[2]
			iPrevH = tFirst[3]
			for i in aiParents[1:]:
				tLayout = self.aFrozen[i][1]
				iY = iPrevY + iPrevH + 8
				if bLeft:
					iX = iPrevX - tLayout[2] - 8
				else:
					iX = iPrevX + iPrevW + 8
				self.moveFrozenWindow(screen, i, iX, iY)
				tNow = self.aFrozen[i][1]
				iPrevX = tNow[0]
				iPrevY = tNow[1]
				iPrevW = tNow[2]
				iPrevH = tNow[3]
			for i in aiParents:
				tAnchor = self.aFrozen[i][5]
				if tAnchor is not None:
					# (the window stays at its new place of the map)
					self.aFrozen[i][5] = self.makeAnchor(self.aFrozen[i][1], (tAnchor[0], tAnchor[1]))
			self.updateFrozenAnchors(screen)
			self.placeChildTips(screen)
			return True
		except:
			pass
		return False

	# After the parent windows were moved every child window looks again for its own place: beside its parent (right, then left) at the height
	# that it had been given, then the other places (see showSecondTip); a place that was taken away from it earlier may be free again.
	def placeChildTips( self, screen ):
		try:
			xRes = screen.getXResolution()
			yRes = screen.getYResolution()
			for i in range(len(self.aFrozen)):
				iParent = self.aFrozen[i][6]
				if iParent < 0:
					continue
				(iPX, iPY, iPW, iPH) = self.aFrozen[iParent][1][:4]
				(iX, iY, iW, iH) = self.aFrozen[i][1][:4]
				iDY = self.dFrozenPrefDY.get(self.aFrozen[i][0], iY - iPY)
				iRight = iPX + iPW + 12
				iLeft = iPX - 12 - iW
				(iNX, iNY) = self.pickFreeSpot([(iRight, iPY + iDY), (iLeft, iPY + iDY), (iRight, iPY), (iLeft, iPY), (iRight, iPY + iPH - iH), (iLeft, iPY + iPH - iH), (iPX, iPY + iPH + 12), (iPX, iPY - 12 - iH)], iW, iH, xRes, yRes, i)
				self.moveFrozenWindow(screen, i, iNX, iNY)
				tNow = self.aFrozen[i][1]
				self.aFrozen[i][7] = (tNow[0] - iPX, tNow[1] - iPY)
		except:
			pass

	def freezeCursorTooltip( self ):
		try:
			if self.isPediaActive():
				return False
			if not self.bHoverTip or not self.bCursorTipShown or self.tTipLayout is None:
				return False
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			for szName in self.getCursorTipNames():
				screen.hide(szName)
				screen.deleteWidget(szName)
			self.szSuppressHelp = self.szCursorTipText
			(tFLayout, aiFIndent) = self.removeFreezeHint(self.tTipLayout, self.aiTipIndent, self.iTipHintLines)
			(tLayout, aiIndent) = self.addFrozenHint(screen, tFLayout, aiFIndent)
			self.addFrozenWindow(screen, tLayout, self.aszTipParas, aiIndent, dict(self.dTipDetails), self.makeAnchor(tLayout))
			if self.iTradeTipYield >= 0 and self.szCursorTipText == self.szTradeTipText:
				# (the tooltip of a good of the import / export window: its lines of colonies can be clicked)
				self.dTraderWin[self.aFrozen[-1][0]] = self.iTradeTipYield
			if self.tTipCity is not None:
				# (the tooltip of an own city: the list of the cities in the name line)
				self.dCityWin[self.aFrozen[-1][0]] = self.tTipCity
			else:
				self.registerPlotCity(len(self.aFrozen) - 1)
			try:
				# the tooltip of an own unit: the line "Set waypoint..."
				iNew = len(self.aFrozen) - 1
				if self.tTipWp is not None:
					# (it is in the tooltip already)
					self.dWpWin[self.aFrozen[iNew][0]] = self.tTipWp
					self.tTipWp = None
				else:
					self.addWaypointRow(screen, iNew, self.getWaypointRowUnit(iNew))
			except:
				pass
			# the tooltip window of the cursor is free again for the next tooltip
			self.bCursorTipShown = False
			self.szCursorTipText = u""
			self.szPendingHelp = None
			return True
		except:
			pass
		return False

	# the layout without the last lines (the hint that the tooltip can be frozen)
	def removeFreezeHint( self, tLayout, aiIndent, iLines ):
		if iLines <= 0:
			return (tLayout, list(aiIndent))
		(iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine) = tLayout
		return ((iX, iY, iWidth, iHeight - iLines * iLine, list(aszLines[:-iLines]), list(aiPara[:-iLines]), iPad, iLine), list(aiIndent[:-iLines]))

	def freezePreview( self, screen ):
		try:
			tKeyAtFreeze = self.tSecondTipKey
			self.deleteTipWindow(screen, self.szPreviewPrefix, self.iSecondTipLines)
			# (the hints of the line (select the unit, talk, wheel, keys) stay in the frozen window, only the hint of the freezing changes)
			iRemoveLines = self.iPreviewFreezeLines
			(tFLayout, aiFIndent) = self.removeFreezeHint(self.tPreviewLayout, [0] * len(self.tPreviewLayout[4]), iRemoveLines)
			(tLayout, aiIndent) = self.addFrozenHint(screen, tFLayout, aiFIndent, "TXT_KEY_WTP_TIP_FROZEN_HINT_CHILD")
			iParent = self.iPreviewParent
			if iParent >= len(self.aFrozen):
				iParent = -1
			tPreviewWp = self.tPreviewWp
			tPreviewUnit = self.tPreviewUnit
			dPreviewDetails = self.tPreviewDetails
			if dPreviewDetails is None:
				dPreviewDetails = {}
			self.tPreviewWp = None
			self.tPreviewUnit = None
			self.tPreviewDetails = None
			self.addFrozenWindow(screen, tLayout, self.aszPreviewParas, aiIndent, dict(dPreviewDetails), None, iParent, self.bPreviewDark)
			try:
				# (the child window of the line "all colonies, net per turn" in the tooltip of a good: its lines of colonies can be clicked, the jump)
				if iParent >= 0 and self.dTraderWin.has_key(self.aFrozen[iParent][0]):
					for szPara in self.aszPreviewParas:
						if self.dTraderLines.has_key(self.normTipText(szPara)):
							self.dTraderWin[self.aFrozen[-1][0]] = self.dTraderWin[self.aFrozen[iParent][0]]
							break
			except:
				pass
			if self.tPreviewKind is not None:
				self.dFrozenKind[self.aFrozen[-1][0]] = self.tPreviewKind
			self.tPreviewKind = None
			if iParent >= 0:
				self.dFrozenPrefDY[self.aFrozen[-1][0]] = self.iPreviewPrefDY
				# (the frozen window of a line: the cursor stays on that line, no second window appears there)
				if tKeyAtFreeze is not None:
					self.dRowChild[(self.aFrozen[iParent][0], tKeyAtFreeze[1])] = self.aFrozen[-1][0]
					try:
						# (a line of a unit of a stack: all lines of the unit have this child window, it is registered at the name of the unit)
						tBlockFz = self.getBlockUnit(iParent, self.aFrozen[iParent][2], tKeyAtFreeze[1])
						if tBlockFz is not None and tBlockFz[1] >= 0:
							self.dRowChild[(self.aFrozen[iParent][0], tBlockFz[1])] = self.aFrozen[-1][0]
					except:
						pass
			# a window with lines of waypoints (the list, the commands), or the tooltip of an own unit of a stack (the line "Set waypoint...")
			if tPreviewWp is not None:
				self.dWpWin[self.aFrozen[-1][0]] = tPreviewWp
				# (the line that the wheel had chosen is not yellow in the frozen window: the wheel starts again there)
				try:
					iMark = tPreviewWp.get("marked", -1)
					if iMark >= 0:
						(iFX, iFY, iFW, iFH, aszFLines, aiFPara, iFPad, iFLine) = self.aFrozen[-1][1]
						aPlain = []
						for i in range(len(aszFLines)):
							szPlain = aszFLines[i]
							if aiFPara[i] == iMark:
								if aiFPara.count(iMark) == 1 and len(tPreviewWp.get("markedText", u"")) > 0:
									# (the line as it was before it was yellow, with its colors)
									szPlain = tPreviewWp["markedText"]
								else:
									szPlain = re.sub(u"<color=[^>]*>|</color>", u"", szPlain)
							aPlain.append(szPlain)
						tPreviewWp["plain"] = aPlain
						self.paintWaypointLines(screen, len(self.aFrozen) - 1, -1)
				except:
					pass
			elif tPreviewUnit is not None:
				try:
					self.addWaypointRow(screen, len(self.aFrozen) - 1, gc.getPlayer(tPreviewUnit[0]).getUnit(tPreviewUnit[1]))
				except:
					pass
			# the explanation of the colors of the line (beside the parent window) is frozen with it and closes with it
			if self.bExplainShown and self.tExplainLayout is not None:
				self.deleteTipWindow(screen, self.szExplainPrefix, self.iExplainLines)
				self.bExplainShown = False
				self.iExplainLines = 0
				tE = self.tExplainLayout
				tELayout = (tE[0], tE[1], tE[2], tE[3], list(tE[4]), [-1] * len(tE[4]), tE[6], tE[7])
				if self.bExplainFreezeHint:
					(tELayout, aiEIndent) = self.addFrozenHint(screen, tELayout, [0] * len(tE[4]))
				else:
					aiEIndent = [0] * len(tE[4])
				self.addFrozenWindow(screen, tELayout, self.aszExplainParas, aiEIndent, {}, None, iParent, True)
				self.dFrozenCompanion[self.aFrozen[-1][0]] = True
				if self.tExplainKind is not None:
					self.dFrozenKind[self.aFrozen[-1][0]] = self.tExplainKind
			self.bSecondTipShown = False
			self.iSecondTipLines = 0
			self.tSecondTipKey = None
			self.iTipSelPara = -1
			self.iTipSelIdx = 0
			if self.bTipWheel:
				self.bTipWheel = False
				self.setWheelCapture(False)
		except:
			pass

	def getSecondTipNames( self ):
		return self.getTipWindowNames(self.szPreviewPrefix, self.iSecondTipLines)

	def hideFoldExplain( self, screen ):
		try:
			if self.bExplainShown:
				self.deleteTipWindow(screen, self.szExplainPrefix, self.iExplainLines)
		except:
			pass
		self.bExplainShown = False
		self.iExplainLines = 0

	def hideSecondTip( self, screen ):
		self.hideFoldExplain(screen)
		self.tPreviewKind = None
		self.tPreviewWp = None
		self.tPreviewUnit = None
		self.tPreviewDetails = None
		try:
			if self.bSecondTipShown:
				for szName in self.getSecondTipNames():
					screen.hide(szName)
					screen.deleteWidget(szName)
		except:
			pass
		self.bSecondTipShown = False
		self.iSecondTipLines = 0

	def getFrozenAt( self, iCX, iCY ):
		i = len(self.aFrozen) - 1
		while i >= 0:
			(iX, iY, iW, iH, aszLines, aiPara, iPad, iLine) = self.aFrozen[i][1]
			if iCX >= iX and iCX < iX + iW and iCY >= iY and iCY < iY + iH:
				return i
			i -= 1
		return -1

	# the first of the places (x, y) where a window of this size covers no frozen window (kept on the screen); the one that covers the least if
	# there is none
	def pickFreeSpot( self, aCands, iWidth, iHeight, xRes, yRes, iExclude = -1, aExtra = None ):
		tBest = None
		iBest = -1
		for (iX, iY) in aCands:
			iX = max(4, min(xRes - iWidth - 4, iX))
			iY = max(4, min(yRes - iHeight - 4, iY))
			iOver = 0
			# (more windows to keep free: x, y, width, height)
			if aExtra is not None:
				for (iEX, iEY, iEW, iEH) in aExtra:
					iDX = min(iX + iWidth, iEX + iEW) - max(iX, iEX)
					iDY = min(iY + iHeight, iEY + iEH) - max(iY, iEY)
					if iDX > 0 and iDY > 0:
						iOver += iDX * iDY
			for iFz in range(len(self.aFrozen)):
				if iFz == iExclude:
					continue
				(iFX, iFY, iFW, iFH) = self.aFrozen[iFz][1][:4]
				iDX = min(iX + iWidth, iFX + iFW) - max(iX, iFX)
				iDY = min(iY + iHeight, iFY + iFH) - max(iY, iFY)
				if iDX > 0 and iDY > 0:
					iOver += iDX * iDY
			if iOver == 0:
				return (iX, iY)
			if tBest is None or iOver < iBest:
				tBest = (iX, iY)
				iBest = iOver
		return tBest

	def showSecondTip( self, screen, szText, iCursorY, tAnchor, iParent = -1, aUnits = None, szHint = None, szTail = None, tKind = None ):
		try:
			(iFX, iFY, iFW, iFH, aszFLines, aiFPara, iPad, iLine) = tAnchor
			xRes = screen.getXResolution()
			yRes = screen.getYResolution()
			iChar = iLine * 0.32
			iMaxWidth = self.getTipMaxWidth(xRes, iChar, False)
			if self.dWideTips.has_key(szText):
				# the log of a transport: double width (long lines), but not wider than the screen allows
				iMaxWidth = min(iMaxWidth * 2, int((xRes - 40) / 1.15))
			iCharsPerLine = max(20, int((iMaxWidth - 2 * iPad) / iChar))
			aszLines = []
			aiPara = []
			tUnitWin = None
			if aUnits is not None:
				# (a list of units: not higher than the parent window)
				iHintLines = len(self.wrapMessage(localText.getText("TXT_KEY_WTP_TIP_FREEZE_HINT_CHILD", ()), iCharsPerLine))
				(szText, tUnitWin) = self.getUnitListText(aUnits, iCharsPerLine, max(3, len(aszFLines) - iHintLines))
			aszParas = self.carryColors(szText.split(u"\n"))
			# the window of the stored or produced goods of a city (or of their marked goods): stacked with the other one, stored on top
			if tKind is None:
				if self.isStoredGoodsWindow(aszParas):
					tKind = ("list", 0)
				elif self.isStoredGoodsWindow(aszParas, "TXT_KEY_CITY_BAR_PRODUCING"):
					tKind = ("list", 1)
			self.tPreviewKind = tKind
			if tUnitWin is not None:
				if len(self.dUnitWin) > 200:
					self.dUnitWin = {}
				self.dUnitWin[tuple(aszParas)] = tUnitWin
			for iPart in range(len(aszParas)):
				aszWrapped = self.wrapMessage(aszParas[iPart], iCharsPerLine)
				aszLines += aszWrapped
				aiPara += [iPart] * len(aszWrapped)
			# (a hint of the line in front of the hint of the freezing: both go away when the window is frozen)
			aszHint = []
			if szHint is not None and len(szHint) > 0:
				for szHintPart in szHint.split(u"\n"):
					aszHint += self.wrapMessage(szHintPart, iCharsPerLine)
			aszFreeze = self.wrapMessage(localText.getText("TXT_KEY_WTP_TIP_FREEZE_HINT_CHILD", ()), iCharsPerLine)
			aszLines += aszHint
			aiPara += [-1] * len(aszHint)
			# (lines of the window after its hints, above the hint of the freezing: they are paragraphs of the window that follow the others)
			if szTail is not None and len(szTail) > 0:
				aszTailParas = self.carryColors(szTail.split(u"\n"))
				for iTail in range(len(aszTailParas)):
					aszWrapped = self.wrapMessage(aszTailParas[iTail], iCharsPerLine)
					aszLines += aszWrapped
					aiPara += [len(aszParas) + iTail] * len(aszWrapped)
				aszParas = list(aszParas) + aszTailParas
			aszLines += aszFreeze
			aiPara += [-1] * len(aszFreeze)
			self.iPreviewHintLines = len(aszHint) + len(aszFreeze)
			self.iPreviewFreezeLines = len(aszFreeze)
			iWidth = self.getTipTextWidth(aszLines, iChar, iMaxWidth, iPad)
			iHeight = len(aszLines) * iLine + 2 * iPad
			# goods tooltips of the import/export window: the child windows always open to the left of the parent as long as there is room
			bLeft = self.isTradeWindowOpen()
			iX = iFX + iFW + 12
			if bLeft and iFX - 12 - iWidth >= 4:
				iX = iFX - 12 - iWidth
			elif iX + iWidth > xRes - 4:
				iX = iFX - 12 - iWidth
			iX = max(4, iX)
			iY = max(4, min(yRes - iHeight - 4, iCursorY + self.getCursorBottom(yRes)))
			# it does not cover another frozen window: beside the window (right, left), then above and below it
			iRight = iFX + iFW + 12
			iLeft = iFX - 12 - iWidth
			# (the place that the window would like to have: its distance below the top of its parent window)
			self.iPreviewPrefDY = iY - iFY
			tStack = None
			if tKind is not None:
				tStack = self.getStackSpot(screen, tKind, iParent, iWidth, iHeight, tKind[0] == "filter")
			if tStack is not None:
				(iX, iY) = tStack
			else:
				(iX, iY) = self.pickFreeSpot([(iX, iY), (iLeft, iY), (iRight, iY), (iLeft, iFY), (iRight, iFY), (iLeft, iFY + iFH - iHeight), (iRight, iFY + iFH - iHeight), (iFX, iFY + iFH + 12), (iFX, iFY - 12 - iHeight)], iWidth, iHeight, xRes, yRes)
			self.tPreviewLayout = (iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine)
			self.iPreviewParent = iParent
			self.aszPreviewParas = aszParas
			self.iSecondTipLines = len(aszLines)
			# (the log of a transport always opens in the darker variant, also over the map)
			self.bPreviewDark = self.dWideTips.has_key(szText)
			self.drawTipWindow(screen, self.szPreviewPrefix, self.tPreviewLayout, False, 0, [], self.bPreviewDark)
			self.bSecondTipShown = True
		except:
			self.bSecondTipShown = False

	# the folded lines of a city tooltip that change their text and color with the state of the city: for each group the colored states
	# (text of the label, color, text that explains it)
	def getFoldGroups( self ):
		return [
			[("TXT_KEY_WTP_TIP_STORED_WOOD", WtpColors.code(WtpColors.RAW_MISSING), "TXT_KEY_WTP_TIP_STORED_LEGEND_WOOD"),
			("TXT_KEY_WTP_TIP_STORED_FOOD", WtpColors.code(WtpColors.RAW_MISSING), "TXT_KEY_WTP_TIP_STORED_LEGEND_FOOD"),
			("TXT_KEY_WTP_TIP_STORED_BOTH", WtpColors.code(WtpColors.RAW_MISSING), "TXT_KEY_WTP_TIP_STORED_LEGEND_BOTH")],
			[("TXT_KEY_WTP_TIP_PRODUCED_MISSING", WtpColors.code(WtpColors.RAW_MISSING), "TXT_KEY_WTP_TIP_PRODUCED_LEGEND_MISSING"),
			("TXT_KEY_WTP_TIP_PRODUCED_IMPORT", WtpColors.code(WtpColors.RAW_SCARCE), "TXT_KEY_WTP_TIP_PRODUCED_LEGEND_IMPORT"),
			("TXT_KEY_WTP_TIP_PRODUCED_IMPORT_SET", WtpColors.code(WtpColors.IMPORT), "TXT_KEY_WTP_TIP_PRODUCED_LEGEND_IMPORT_SET")]
		]

	# the text of the window that explains the colored labels of the folded line "Stored..." or "Produced..." (all colored states of that line,
	# each in its color, the state of the city now first); empty when the label is not one of the colored ones (then there is nothing to explain)
	def getFoldLegend( self, szLabel ):
		try:
			szNorm = self.normTipText(szLabel)
			for aGroup in self.getFoldGroups():
				aCurrent = []
				aOthers = []
				for tState in aGroup:
					if self.normTipText(localText.getText(tState[0], ())) == szNorm:
						aCurrent.append(tState)
					else:
						aOthers.append(tState)
				if len(aCurrent) > 0:
					# the state the city is in now comes first
					aLines = []
					for (szLabelKey, szColor, szExplainKey) in aCurrent + aOthers:
						aLines.append(u"<color=" + szColor + u">" + localText.getText(szLabelKey, ()) + u"</color>: " + localText.getText(szExplainKey, ()))
					return u"\n".join(aLines)
		except:
			pass
		return u""

	# the window with the explanation of a folded line: above the parent window, flush with its right edge (when there is room), otherwise
	# beside or below the parent window where nothing is covered
	def showFoldExplain( self, screen, szText, tAnchor, bFreezeHint = True, tKind = None ):
		try:
			self.bExplainFreezeHint = bFreezeHint
			self.tExplainKind = tKind
			(iFX, iFY, iFW, iFH, aszFLines, aiFPara, iPad, iLine) = tAnchor
			xRes = screen.getXResolution()
			yRes = screen.getYResolution()
			iChar = iLine * 0.32
			iMaxWidth = self.getTipMaxWidth(xRes, iChar, False)
			iCharsPerLine = max(20, int((iMaxWidth - 2 * iPad) / iChar))
			aszParas = self.carryColors(szText.split(u"\n"))
			aszLines = []
			aiPara = []
			for iPart in range(len(aszParas)):
				aszWrapped = self.wrapMessage(aszParas[iPart], iCharsPerLine)
				aszLines += aszWrapped
				aiPara += [iPart] * len(aszWrapped)
			iWidth = self.getTipTextWidth(aszLines, iChar, iMaxWidth, iPad)
			iHeight = len(aszLines) * iLine + 2 * iPad
			iRight = iFX + iFW + 12
			iLeft = iFX - 12 - iWidth
			iY0 = iFY
			aExtra = []
			bChildRight = True
			if self.bSecondTipShown and self.tPreviewLayout is not None:
				(iCX, iCY, iCW, iCH) = self.tPreviewLayout[:4]
				aExtra.append((iCX, iCY, iCW, iCH))
				iY0 = iCY
				bChildRight = (iCX + iCW / 2 >= iFX + iFW / 2)
			# above the parent window, flush with its right edge; where that is not possible: the side opposite to the list of goods, then
			# below the parent window, then the other side
			aCands = [(iFX + iFW - iWidth, iFY - 12 - iHeight)]
			if bChildRight:
				aCands += [(iLeft, iY0), (iLeft, iFY), (iLeft, iFY + iFH - iHeight)]
				aCands += [(iFX + iFW - iWidth, iFY + iFH + 12), (iRight, iFY), (iRight, iFY + iFH - iHeight)]
			else:
				aCands += [(iRight, iY0), (iRight, iFY), (iRight, iFY + iFH - iHeight)]
				aCands += [(iFX + iFW - iWidth, iFY + iFH + 12), (iLeft, iFY), (iLeft, iFY + iFH - iHeight)]
			tStack = None
			if tKind is not None:
				iExplainParent = -1
				if self.bSecondTipShown:
					iExplainParent = self.iPreviewParent
				tStack = self.getStackSpot(screen, tKind, iExplainParent, iWidth, iHeight, False, aExtra)
			if tStack is not None:
				(iX, iY) = tStack
			else:
				(iX, iY) = self.pickFreeSpot(aCands, iWidth, iHeight, xRes, yRes, -1, aExtra)
			tLayout = (iX, iY, iWidth, iHeight, aszLines, aiPara, iPad, iLine)
			self.iExplainLines = len(aszLines)
			self.tExplainLayout = tLayout
			self.aszExplainParas = aszParas
			self.drawTipWindow(screen, self.szExplainPrefix, tLayout, False, 0, [], True)
			self.bExplainShown = True
		except:
			self.bExplainShown = False

	# every frame while frozen: the line of the frozen window under the cursor decides about the second window. Shift + mouse wheel on a line
	# chooses among all the things named in it (the window lists them, the chosen one in yellow; a right click opens its page)
	def updateFrozenTip( self ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		if self.iRedrawFrozen > 0:
			self.iRedrawFrozen -= 1
			if self.iRedrawFrozen == 0:
				self.redrawFrozenTips(screen)
		iCX = gc.getGame().getCursorClientX()
		iCY = gc.getGame().getCursorClientY()
		self.updateFrozenAnchors(screen)
		iFz = self.getFrozenAt(iCX, iCY)
		iPara = -1
		iLineIdx = -1
		bPromoLine = False
		aszLines = []
		aszTopParas = []
		dDetails = {}
		tTop = None
		if iFz >= 0:
			tTop = self.aFrozen[iFz][1]
			aszTopParas = self.aFrozen[iFz][2]
			dDetails = self.aFrozen[iFz][4]
			(iX, iY, iW, iH, aszLines, aiPara, iPad, iLine) = tTop
		if iFz >= 0 and iCY >= iY + iPad and iCY < iY + iPad + len(aszLines) * iLine:
			iLineIdx = int((iCY - iY - iPad) / iLine)
			iPara = aiPara[iLineIdx]
			# the line with the promotion pictures of a unit: its tooltip lists the promotions and what they do (nothing for the Colopedia)
			bPromoLine = (aszLines[iLineIdx].lower().find(u"<img=") >= 0)
		# the mouse wheel is only taken (the map does not zoom) while shift is down and the cursor is on a line with named things
		bWheel = False
		bShift = False
		try:
			bShift = gc.getGame().isShiftKeyPressed()
		except:
			pass
		# (the list of waypoints: the wheel goes through its lines, a waypoint has the choices start, delete, rename; no Colopedia on these lines)
		aWpStops = []
		bWpLine = False
		if iFz >= 0 and iPara >= 0:
			tWpList = self.dWpWin.get(self.aFrozen[iFz][0])
			if tWpList is not None and tWpList["paras"].has_key(iPara) and self.isWaypointList(tWpList):
				aWpStops = self.getWaypointStops(tWpList)
				bWpLine = len(aWpStops) > 0
		bWpRow = False
		iWpRowCount = 0
		iRowChild = -1
		aChildKeys = []
		if iFz >= 0 and iPara >= 0:
			tWpRow = self.dWpWin.get(self.aFrozen[iFz][0])
			if tWpRow is not None and tWpRow["paras"].get(iPara) == "row":
				bWpRow = True
				iWpRowCount = len(self.getWaypointView(tWpRow["sea"])) + 1
				# (the list of this line is frozen already: the wheel goes through its lines)
				szChild = self.dRowChild.get((self.aFrozen[iFz][0], iPara))
				if szChild is not None:
					for i in range(len(self.aFrozen)):
						if self.aFrozen[i][0] == szChild and self.aFrozen[i][6] == iFz and self.dWpWin.has_key(szChild):
							iRowChild = i
							aChildKeys = [k for k in self.dWpWin[szChild]["paras"].keys() if not isinstance(self.dWpWin[szChild]["paras"][k], tuple)]
							aChildKeys.sort()
							iWpRowCount = len(aChildKeys)
		# (the line "Commands" of a unit: the wheel goes through the lines of its child window)
		bCmdRow = False
		if iFz >= 0 and iPara >= 0 and not bWpRow and dDetails.has_key(iPara) and not self.dUnitGroups.has_key(dDetails[iPara]) and iPara == self.getCommandsPara(aszTopParas, dDetails):
			bCmdRow = True
			iWpRowCount = len(dDetails[iPara].split(u"\n"))
			szChild = self.dRowChild.get((self.aFrozen[iFz][0], iPara))
			if szChild is not None:
				for i in range(len(self.aFrozen)):
					if self.aFrozen[i][0] == szChild and self.aFrozen[i][6] == iFz:
						iRowChild = i
						aChildKeys = range(len(self.aFrozen[i][2]))
						iWpRowCount = len(aChildKeys)
		# (the name line of the tooltip of an own city: the wheel goes through the list of the cities in its child window)
		bCityRow = False
		if iFz >= 0 and iPara >= 0 and not bWpRow and not bCmdRow and dDetails.has_key(iPara) and iPara == self.getCityLinePara(iFz):
			bCityRow = True
			iWpRowCount = len(dDetails[iPara].split(u"\n"))
		# (the line "Set as WP: name" of a plot: the wheel chooses delete or rename)
		bPlotWp = False
		try:
			if iFz >= 0 and iPara >= 0 and iPara < len(aszTopParas) and self.aFrozen[iFz][6] < 0 and not bWpRow and not bCmdRow and not bCityRow and self.isWaypointPlotPara(aszTopParas[iPara]):
				bPlotWp = True
				iWpRowCount = 2
		except:
			bPlotWp = False
		bWpWindow = (iFz >= 0 and iPara >= 0 and self.dWpWin.has_key(self.aFrozen[iFz][0]) and self.dWpWin[self.aFrozen[iFz][0]]["paras"].has_key(iPara))
		try:
			if (bWpLine or bWpRow or bCmdRow or bCityRow or bPlotWp) and bShift:
				bWheel = True
			elif iPara >= 0 and not bWpWindow and not bPromoLine and bShift and len(self.getPediaLineTargets(iFz, aszTopParas, iPara, True)) > 0 and self.getBlockUnit(iFz, aszTopParas, iPara) is None:
				bWheel = True
		except:
			pass
		if bWheel != self.bTipWheel and not self.bTradeSel:
			self.bTipWheel = bWheel
			self.setWheelCapture(bWheel)
		if bWheel:
			iNotches = gc.getGame().takeWheelNotches()
			if iNotches != 0:
				if bWpLine:
					aTargets = aWpStops
				elif bWpRow or bCmdRow or bCityRow or bPlotWp:
					aTargets = range(iWpRowCount)
				else:
					aTargets = self.getPediaLineTargets(iFz, aszTopParas, iPara, True)
				if iPara != self.iTipSelPara or iFz != self.iTipSelLevel:
					self.iTipSelPara = iPara
					self.iTipSelLevel = iFz
					self.iTipSelIdx = 0
					if bWpLine:
						# (the first stop of the line under the cursor)
						for k in range(len(aWpStops)):
							if aWpStops[k][0] == iPara:
								self.iTipSelIdx = k
								break
				# the wheel towards the user: the next one, away from the user: the one before
				self.iTipSelIdx = (self.iTipSelIdx - iNotches) % len(aTargets)
		iSel = -1
		if iPara >= 0 and iPara == self.iTipSelPara and iFz == self.iTipSelLevel and not bPromoLine:
			iSel = self.iTipSelIdx
		# (after a jump to a waypoint the window goes to its new place: the cursor goes with it)
		if self.tCursorFollow is not None:
			try:
				tCF = self.tCursorFollow
				if (self.getTipNow() / 1000.0) - tCF[3] > 1.2:
					self.tCursorFollow = None
					self.tSecondTipKey = None
				elif tCF[4] >= 0 and (abs(iCX - tCF[4]) > 2 or abs(iCY - tCF[5]) > 2):
					# (the player moves the mouse: the cursor is free again at once)
					self.tCursorFollow = None
					self.tSecondTipKey = None
				else:
					for i in range(len(self.aFrozen)):
						if self.aFrozen[i][0] == tCF[0]:
							iNewX = self.aFrozen[i][1][0] + tCF[1]
							iNewY = self.aFrozen[i][1][1] + tCF[2]
							# (the window stands still for a few frames: the cursor is free again)
							if iNewX == tCF[4] and iNewY == tCF[5] and (self.getTipNow() / 1000.0) - tCF[3] > 0.25:
								tCF[6] += 1
								if tCF[6] >= 3:
									self.tCursorFollow = None
									self.tSecondTipKey = None
									break
							else:
								tCF[6] = 0
							tCF[4] = iNewX
							tCF[5] = iNewY
							gc.getGame().setCursorClient(tCF[4], tCF[5])
			except:
				self.tCursorFollow = None
		# (after the jump the game may look at its unit again for a moment: the camera is put on the waypoint again for a short time)
		if self.tJump is not None:
			try:
				if (self.getTipNow() / 1000.0) - self.tJump[2] > 1.0:
					self.tJump = None
				elif (self.getTipNow() / 1000.0) - self.tJump[2] > 0.05:
					CyCamera().JustLookAtPlot(CyMap().plot(self.tJump[0], self.tJump[1]))
			except:
				self.tJump = None
		# a left click on the line of a waypoint (written by onTipLineLeftClick, which asks for this update at once)
		bLeftClick = False
		if self.tLeftClick is not None:
			tLC = self.tLeftClick
			self.tLeftClick = None
			if (self.getTipNow() / 1000.0) - tLC[2] < 1.0 and iFz == tLC[0] and iPara == tLC[1]:
				bLeftClick = True
		self.bLeftJumped = False
		# a click of the mouse wheel (with Shift) on a chosen waypoint: the map looks at its place (the windows go there with it)
		try:
			if bLeftClick:
				szWhyL = self.jumpToSelectedWaypoint(iFz, iPara, iSel, bWpLine, aWpStops, bWpRow, iRowChild, aChildKeys)
				if len(szWhyL) == 0:
					self.bLeftJumped = True
			bMiddleClick = gc.getGame().takeMiddleClick()
			if bMiddleClick:
				# (the click can be some seconds old when the interface was not drawn: it counts only where the cursor still is)
				if abs(gc.getGame().getMiddleClickX() - iCX) > 8 or abs(gc.getGame().getMiddleClickY() - iCY) > 8:
					bMiddleClick = False
			if bShift:
				self.fShiftSeen = (self.getTipNow() / 1000.0)
			if bMiddleClick:
				# (Shift counts when it was down a moment ago: the click and the key are not read in the same instant)
				bShiftNow = bShift or ((self.getTipNow() / 1000.0) - self.fShiftSeen < 1.0)
				# (test phase: the jump needs no Shift; set to True for Shift + wheel click again)
				if not self.bWheelNeedsShift:
					bShiftNow = True
				szWhy = u""
				if not bShiftNow:
					szWhy = u"Shift is not pressed"
				elif iFz < 0 or iPara < 0:
					szWhy = u"the cursor is not on a line of a frozen window"
				else:
					szWhy = self.jumpToSelectedWaypoint(iFz, iPara, iSel, bWpLine, aWpStops, bWpRow, iRowChild, aChildKeys)
				if len(szWhy) > 0:
					# (test aid: why nothing happened)
					self.showModMessage(u"Wheel click: no jump (" + szWhy + u")")
		except:
			pass
		# the jump to a city is not finished (the camera is on its way, the new window and the cursor find their places): no child windows yet; they
		# come when the window stands still (the cursor is free then and the update below makes the window of the line the cursor is on)
		if self.bCityHold:
			bFollowCity = (self.tCursorFollow is not None and self.tCursorFollow[0] == self.szCityHoldWin)
			bStill = False
			if self.tCityJump is None and bFollowCity:
				# (the window stands still for two frames: the jump is finished at once, the cursor follows no longer; no waiting time)
				for iHold in range(len(self.aFrozen)):
					if self.aFrozen[iHold][0] == self.szCityHoldWin:
						tHoldPos = (self.aFrozen[iHold][1][0], self.aFrozen[iHold][1][1])
						if tHoldPos == self.tCityHoldPos:
							self.iCityHoldStill += 1
						else:
							self.iCityHoldStill = 0
						self.tCityHoldPos = tHoldPos
						bStill = (self.iCityHoldStill >= 2)
			if bStill:
				self.tCursorFollow = None
			if self.tCityJump is None and (not bFollowCity or bStill):
				self.bCityHold = False
				self.tSecondTipKey = None
			else:
				if self.bSecondTipShown:
					self.hideSecondTip(screen)
				self.tSecondTipKey = None
				return
		tKey = (iFz, iPara, iSel, iLineIdx, bPromoLine)
		if tKey == self.tSecondTipKey:
			return
		self.tSecondTipKey = tKey
		self.hideSecondTip(screen)
		tUnitWin = None
		tWp = None
		if iFz >= 0 and iPara >= 0:
			tUnitWin = self.dUnitWin.get(tuple(aszTopParas))
			tWp = self.dWpWin.get(self.aFrozen[iFz][0])
		# the list of waypoints: the line chosen with the wheel is yellow, and it (with its choice) is what the child window shows
		iWpPara = iPara
		iWpOption = -1
		iMark = -1
		if bWpLine and iSel >= 0 and iSel < len(aWpStops):
			iWpPara = aWpStops[iSel][0]
			iWpOption = aWpStops[iSel][1]
			iMark = iWpPara
		self.markWaypointLine(screen, iFz, iMark)
		if iRowChild >= 0:
			# (no second window: the line chosen with the wheel is yellow in the frozen list)
			iChildMark = -1
			if iSel >= 0 and iSel < len(aChildKeys):
				iChildMark = aChildKeys[iSel]
			self.markWaypointLine(screen, iRowChild, iChildMark)
			return
		if iFz >= 0 and iPara >= 0 and iSel < 0 and not bWpRow:
			# (the line has a frozen child window already: no second one)
			szFrozenChild = self.dRowChild.get((self.aFrozen[iFz][0], iPara))
			if szFrozenChild is None and not bPromoLine and not (tWp is not None and tWp["paras"].has_key(iPara)):
				try:
					# (the child window of the unit of the line is frozen already, from another line of the unit)
					tBlockHover = self.getBlockUnit(iFz, aszTopParas, iPara)
					if tBlockHover is not None and tBlockHover[1] >= 0:
						szFrozenChild = self.dRowChild.get((self.aFrozen[iFz][0], tBlockHover[1]))
				except:
					szFrozenChild = None
			if szFrozenChild is not None:
				for i in range(len(self.aFrozen)):
					if self.aFrozen[i][0] == szFrozenChild and self.aFrozen[i][6] == iFz:
						return
		if bPromoLine:
			szText = self.getPromotionTipText(aszLines[iLineIdx])
			if len(szText) > 0:
				self.showSecondTip(screen, szText, iCY, tTop, iFz)
		elif iPara >= 0 and iSel < 0 and self.dTraderWin.has_key(self.aFrozen[iFz][0]) and self.dTraderLines.has_key(self.normTipText(aszTopParas[iPara])):
			# a line of a colony in the tooltip of a good: the export settings of the colony for that good and its stock
			szTraderChild = self.getTraderChildText(self.dTraderWin[self.aFrozen[iFz][0]], self.dTraderLines[self.normTipText(aszTopParas[iPara])])
			if len(szTraderChild) > 0:
				self.showSecondTip(screen, szTraderChild, iCY, tTop, iFz)
		elif iPara >= 0 and iSel < 0 and self.dTraderWin.has_key(self.aFrozen[iFz][0]) and self.dNetLines.has_key(self.normTipText(aszTopParas[iPara])):
			# the line "all colonies, net per turn" in the tooltip of a good: what the sum means (consumption already deducted)
			self.showSecondTip(screen, self.getNetHelpText(self.dTraderWin[self.aFrozen[iFz][0]]), iCY, tTop, iFz)
		elif tWp is not None and tWp["paras"].has_key(iPara):
			# a line of waypoints: the list of the waypoints, or the choices of a waypoint (the one chosen with the wheel in yellow)
			if bWpRow:
				self.showWaypointTip(screen, iFz, tWp, iWpPara, iCY, tTop, -1, iSel)
			else:
				self.showWaypointTip(screen, iFz, tWp, iWpPara, iCY, tTop, iWpOption)
		elif tUnitWin is not None and iPara == tUnitWin[2]:
			# the last line of a list of units: the units that did not fit into its window
			self.showSecondTip(screen, u"", iCY, tTop, iFz, tUnitWin[1])
		elif iPara >= 0 and dDetails.has_key(iPara):
			if self.dUnitGroups.has_key(dDetails[iPara]):
				# the line "more...units": the units that the game lists in groups
				self.showSecondTip(screen, u"", iCY, tTop, iFz, self.dUnitGroups[dDetails[iPara]])
			else:
				# the line "Details" of a military unit: the lines folded into it
				szDetail = dDetails[iPara]
				iMarkCmd = -1
				szMarkOrig = u""
				if (bCmdRow or bCityRow) and iSel >= 0:
					# (the line of the commands (or of the city) that the wheel has chosen is yellow)
					aDetailLines = szDetail.split(u"\n")
					if iSel < len(aDetailLines):
						iMarkCmd = iSel
						szMarkOrig = aDetailLines[iSel]
						aDetailLines[iSel] = u"<color=255,255,0,255>" + re.sub(u"<color=[^>]*>|</color>", u"", szMarkOrig) + u"</color>"
						szDetail = u"\n".join(aDetailLines)
				elif iSel >= 0 and self.isBuildingsRow(iFz, aszTopParas, iPara):
					# the line "Buildings": the building of the list that the wheel has chosen is yellow in its child window
					aBuildingTargets = self.getPediaLineTargets(iFz, aszTopParas, iPara, True)
					if iSel < len(aBuildingTargets):
						aSegs = szDetail.split(u", ")
						for k in range(len(aSegs)):
							if re.sub(u"<[^>]*>", u"", aSegs[k]).strip().lower() == aBuildingTargets[iSel][0].lower():
								aSegs[k] = u"<color=255,255,0,255>" + re.sub(u"<color=[^>]*>|</color>", u"", aSegs[k]) + u"</color>"
								break
						szDetail = u", ".join(aSegs)
				self.showSecondTip(screen, szDetail, iCY, tTop, iFz)
				if self.bSecondTipShown and self.dNestedDetails.has_key(szDetail):
					self.tPreviewDetails = self.dNestedDetails[szDetail]
				if tWp is not None and iPara == tWp["cmd"] and self.bSecondTipShown:
					# the child window of the line "Commands" of a unit: its first line is "Set waypoint..."
					self.tPreviewWp = {"unit": tWp["unit"], "sea": tWp["sea"], "paras": {0: "row"}, "cmd": -1, "marked": iMarkCmd, "markedText": szMarkOrig}
				# the folded line "Stored..." / "Produced..." in a color: its explanation, in a second window beside the parent
				szLegend = self.getFoldLegend(aszTopParas[iPara])
				# (the line "Stored...": the legend of the marks of its goods always, after the explanation of a red state)
				if self.getFoldKind(aszTopParas[iPara]) == 0:
					if len(szLegend) > 0:
						szLegend += u"\n"
					szLegend += localText.getText("TXT_KEY_WTP_TIP_STORED_COLORS", ())
				if len(szLegend) > 0:
					self.showFoldExplain(screen, szLegend, tTop, True, ("explain", self.getFoldKind(aszTopParas[iPara])))
		elif iPara >= 0 and self.isCommandLine(iFz, aszTopParas, iPara):
			# the command lines of a city tooltip: no Colopedia, a right click runs the command
			self.showSecondTip(screen, localText.getText("TXT_KEY_WTP_TIP_RUN_COMMAND", ()), iCY, tTop, iFz)
		elif ((iPara >= 0 and iSel < 0) or (iLineIdx >= 0 and self.isHintLine(aiPara, iLineIdx))) and self.isStoredGoodsWindow(aszTopParas):
			# the window with the goods of a city: what the colors of the goods mean, on the lines of the goods and on the last line
			# (the hint "Frozen - Esc or hold X: close"; there the highlight that the game draws under a line does not hide the colors)
			szFilter = self.getGoodsFilterText(aszTopParas, 0)
			if len(szFilter) > 0:
				self.showSecondTip(screen, szFilter, iCY, tTop, iFz, None, localText.getText("TXT_KEY_WTP_TIP_GOODS_TRADE_HINT", ()), None, ("filter", 0))
		elif ((iPara >= 0 and iSel < 0) or (iLineIdx >= 0 and self.isHintLine(aiPara, iLineIdx))) and self.isStoredGoodsWindow(aszTopParas, "TXT_KEY_CITY_BAR_PRODUCING"):
			# the window with the goods that a city produces: the same
			szFilter = self.getGoodsFilterText(aszTopParas, 1)
			if len(szFilter) > 0:
				self.showSecondTip(screen, szFilter, iCY, tTop, iFz, None, localText.getText("TXT_KEY_WTP_TIP_GOODS_TRADE_HINT_RAW", ()), None, ("filter", 1))
		elif iPara >= 0 and iSel < 0 and self.showAloneUnitTip(screen, iFz, aszTopParas, iPara, iCY, tTop):
			# a line of a unit of a stack: the tooltip of the unit as if it stood alone on the plot
			pass
		elif iPara >= 0:
			if iSel >= 0:
				szText = self.getTipSecondText(iPara, iSel, aszTopParas, iFz)
			else:
				szText = self.getTipSecondText(iPara, -1, aszTopParas, iFz)
			if len(szText) > 0:
				self.showSecondTip(screen, szText, iCY, tTop, iFz)

	# is the line one of the lines after the last line of the content (the hint at the end of a frozen window)?
	def isHintLine( self, aiPara, iLineIdx ):
		try:
			iLast = -1
			for i in range(len(aiPara)):
				if aiPara[i] >= 0:
					iLast = i
			return iLineIdx > iLast
		except:
			return False

	# the child window with the goods stored in a city (its first line begins like the line "Stored" of the city tooltip)
	def isStoredGoodsWindow( self, aszParas, szKey = "TXT_KEY_CITY_BAR_STORED" ):
		try:
			if len(aszParas) == 0:
				return False
			szStored = self.getTipPrefix(szKey, (u"",))
			szFirst = self.normTipText(re.sub(u"<[^>]*>", u"", aszParas[0]))
			return len(szStored) > 3 and szFirst.find(szStored) == 0
		except:
			return False

	# which of the two folded lines "Stored..." (0) and "Produced..." (1) a label belongs to (-1: none)
	def getFoldKind( self, szLabel ):
		try:
			szNorm = self.normTipText(szLabel)
			# (the plain lines without a state)
			if szNorm == self.normTipText(localText.getText("TXT_KEY_WTP_TIP_STORED_FOLD", ())):
				return 0
			if szNorm == self.normTipText(localText.getText("TXT_KEY_WTP_TIP_PRODUCED_FOLD", ())):
				return 1
			aGroups = self.getFoldGroups()
			for iGroup in range(len(aGroups)):
				for tState in aGroups[iGroup]:
					if self.normTipText(localText.getText(tState[0], ())) == szNorm:
						return iGroup
		except:
			pass
		return -1

	# is a window of this size at this place on the screen and without contact to a frozen window (except iExclude) or one of the extra rectangles?
	def isSpotFree( self, iX, iY, iWidth, iHeight, xRes, yRes, iExclude = -1, aExtra = None, iGap = 4 ):
		if iX < 4 or iY < 4 or iX + iWidth > xRes - 4 or iY + iHeight > yRes - 4:
			return False
		aRects = []
		if aExtra is not None:
			aRects += list(aExtra)
		for i in range(len(self.aFrozen)):
			if i != iExclude:
				aRects.append(self.aFrozen[i][1][:4])
		for (iRX, iRY, iRW, iRH) in aRects:
			if iX < iRX + iRW + iGap and iX + iWidth > iRX - iGap and iY < iRY + iRH + iGap and iY + iHeight > iRY - iGap:
				return False
		return True

	# The windows of the stored goods and of the produced goods of a city (and their help windows) lie one below the other, the stored goods on
	# top, whether the other one is frozen or not. tKind = (class, kind): kind 0 stored, 1 produced. The place of the new window (None: there is
	# no window of the other kind, the usual places apply). When the new window does not fit above / below the other one, the other one makes room.
	def getStackSpot( self, screen, tKind, iParent, iWidth, iHeight, bAnyParent = False, aExtra = None ):
		try:
			iSib = -1
			for i in range(len(self.aFrozen)):
				tK = self.dFrozenKind.get(self.aFrozen[i][0])
				if tK is not None and tK[0] == tKind[0] and tK[1] != tKind[1] and (bAnyParent or self.aFrozen[i][6] == iParent):
					iSib = i
			if iSib < 0:
				return None
			xRes = screen.getXResolution()
			yRes = screen.getYResolution()
			iGap = 8
			(iSX, iSY, iSW, iSH) = self.aFrozen[iSib][1][:4]
			iNX = iSX
			if tKind[1] == 0:
				# stored: above the produced goods
				if self.isSpotFree(iNX, iSY - iHeight - iGap, iWidth, iHeight, xRes, yRes, -1, aExtra):
					return (iNX, iSY - iHeight - iGap)
				# otherwise the produced goods go down and this window takes their place
				if self.isSpotFree(iNX, iSY + iHeight + iGap, iSW, iSH, xRes, yRes, iSib, aExtra) and self.isSpotFree(iNX, iSY, iWidth, iHeight, xRes, yRes, iSib, aExtra):
					self.moveStackSibling(screen, iSib, iNX, iSY + iHeight + iGap)
					return (iNX, iSY)
			else:
				# produced: below the stored goods
				if self.isSpotFree(iNX, iSY + iSH + iGap, iWidth, iHeight, xRes, yRes, -1, aExtra):
					return (iNX, iSY + iSH + iGap)
				# otherwise the stored goods go up and this window takes their place
				if self.isSpotFree(iNX, iSY - iSH - iGap, iSW, iSH, xRes, yRes, iSib, aExtra) and self.isSpotFree(iNX, iSY, iWidth, iHeight, xRes, yRes, iSib, aExtra):
					self.moveStackSibling(screen, iSib, iNX, iSY - iSH - iGap)
					return (iNX, iSY)
			# no room above or below (a small screen, the help windows of both next to the tooltip of the city): side by side with the other
			# one, the stored goods on the left, at the height of the other window
			if tKind[1] == 0:
				aSide = [(iSX - iWidth - iGap, iSY), (iSX + iSW + iGap, iSY)]
			else:
				aSide = [(iSX + iSW + iGap, iSY), (iSX - iWidth - iGap, iSY)]
			for (iSideX, iSideY) in aSide:
				if self.isSpotFree(iSideX, iSideY, iWidth, iHeight, xRes, yRes, -1, aExtra):
					return (iSideX, iSideY)
		except:
			pass
		return None

	# a frozen window goes to another place; a child window keeps that place to its parent
	def moveStackSibling( self, screen, iSib, iNX, iNY ):
		self.moveFrozenWindow(screen, iSib, iNX, iNY)
		iParent = self.aFrozen[iSib][6]
		if iParent >= 0 and iParent < len(self.aFrozen):
			self.aFrozen[iSib][7] = (self.aFrozen[iSib][1][0] - self.aFrozen[iParent][1][0], self.aFrozen[iSib][1][1] - self.aFrozen[iParent][1][1])

	# the window that lists the marked goods of the window of the stored goods (kind 0) or the produced goods (kind 1) of a city, sorted by the
	# colors of the marks (one line for each good, the explanation of the color as the heading); empty when no good is marked
	def getGoodsFilterText( self, aszParas, iKind ):
		try:
			if iKind == 0:
				szLegend = localText.getText("TXT_KEY_WTP_TIP_STORED_COLORS", ())
				aColors = [WtpColors.code(WtpColors.EXPORT), WtpColors.code(WtpColors.IMPORT)]
			else:
				szLegend = localText.getText("TXT_KEY_WTP_TIP_PRODUCED_COLORS", ())
				aColors = [WtpColors.code(WtpColors.RAW_MISSING), WtpColors.code(WtpColors.RAW_SCARCE), WtpColors.code(WtpColors.IMPORT)]
			aLegend = szLegend.split(u"\n")
			aGoods = []
			for i in range(len(aColors)):
				aGoods.append([])
			aSeg = aszParas[0].split(u", ")
			for k in range(len(aSeg)):
				szSeg = aSeg[k]
				if k == 0:
					# (the first part starts with the name of the line: "Stored : ")
					szSeg = re.sub(u"^((?:<color=[^>]*>)?)[^:<>]*:\\s*", u"\\1", szSeg)
				mColor = re.search(u"<color=(\\d+,\\d+,\\d+,\\d+)>", szSeg)
				if mColor is None or not (mColor.group(1) in aColors):
					continue
				szName = u""
				for iYield in range(YieldTypes.NUM_YIELD_TYPES):
					if szSeg.find(unichr(gc.getYieldInfo(iYield).getChar())) >= 0:
						szName = re.sub(u"<[^>]*>", u"", gc.getYieldInfo(iYield).getDescription() or u"")
						break
				if len(szName) > 0:
					if szSeg.endswith(u"</color>"):
						szSeg = szSeg[:-len(u"</color>")] + u" " + szName + u"</color>"
					else:
						szSeg = szSeg + u" " + szName
				aGoods[aColors.index(mColor.group(1))].append(szSeg)
			aLines = []
			for i in range(len(aColors)):
				if len(aGoods[i]) > 0:
					if i < len(aLegend):
						aLines.append(aLegend[i])
					aLines += aGoods[i]
			return u"\n".join(aLines)
		except:
			return u""

	# the goods (yield types) with a mark of color (stored goods: exported, imported; produced goods: missing, scarce, import set) in the lines of a window
	def getMarkedGoodTypes( self, aszParas ):
		aTypes = []
		try:
			aMarks = [WtpColors.code(WtpColors.EXPORT), WtpColors.code(WtpColors.IMPORT), WtpColors.code(WtpColors.RAW_MISSING), WtpColors.code(WtpColors.RAW_SCARCE)]
			for szPara in aszParas:
				for szSeg in szPara.split(u", "):
					mColor = re.search(u"<color=(\\d+,\\d+,\\d+,\\d+)>", szSeg)
					if mColor is None or not (mColor.group(1) in aMarks):
						continue
					for iYield in range(YieldTypes.NUM_YIELD_TYPES):
						if szSeg.find(unichr(gc.getYieldInfo(iYield).getChar())) >= 0:
							szType = gc.getYieldInfo(iYield).getType()
							if not (szType in aTypes):
								aTypes.append(szType)
							break
		except:
			pass
		return aTypes

	# the raw materials (yield types) that the professions need to make the goods (yield types)
	# (the professions of the citizens of the city decide what a building makes from what: the professions that make a good and that a citizen of
	# the city has now give its raw materials, all of the (up to two) goods that they consume; if no citizen has one of them, all professions that
	# make the good)
	def getRawMaterialTypes( self, aTypes, pCity ):
		aRaw = []
		try:
			aActive = []
			for i in range(pCity.getPopulation()):
				pUnit = pCity.getPopulationUnitByIndex(i)
				if pUnit is not None and not pUnit.isNone():
					iProf = pUnit.getProfession()
					if iProf >= 0 and not (iProf in aActive):
						aActive.append(iProf)
			for szType in aTypes:
				iOut = gc.getInfoTypeForString(szType)
				aMaking = []
				for iProfession in range(gc.getNumProfessionInfos()):
					if gc.getProfessionInfo(iProfession).getYieldsProduced(0) == iOut:
						aMaking.append(iProfession)
				aUse = [p for p in aMaking if p in aActive]
				# (a good made by several professions of the building, e.g. cloth from cotton by one weaver and from wool by another: only the
				# chains that are restricted count, those with a raw material that the city consumes more of than it produces)
				aLimited = []
				for iProfession in aUse:
					pProf = gc.getProfessionInfo(iProfession)
					for k in range(pProf.getNumYieldsConsumed()):
						iIn = pProf.getYieldsConsumed(k)
						if iIn >= 0 and iIn != YieldTypes.YIELD_FOOD and pCity.getRawYieldConsumed(iIn) > pCity.getBaseRawYieldProduced(iIn):
							if not (iProfession in aLimited):
								aLimited.append(iProfession)
				if len(aLimited) > 0:
					aUse = aLimited
				if len(aUse) == 0:
					aUse = aMaking
				for iProfession in aUse:
					pProf = gc.getProfessionInfo(iProfession)
					for k in range(pProf.getNumYieldsConsumed()):
						iIn = pProf.getYieldsConsumed(k)
						if iIn >= 0:
							szIn = gc.getYieldInfo(iIn).getType()
							if not (szIn in aRaw):
								aRaw.append(szIn)
		except:
			pass
		return aRaw

	# opens the import / export window of the city of a goods window (the city is named in the first line of its top window) with a temporary
	# filter view of the marked goods of the list (only for this opening)
	def openGoodsTradeWindow( self, iLevel, aszParas, iKind = 0 ):
		try:
			aTypes = self.getMarkedGoodTypes(aszParas)
			iTop = iLevel
			while self.aFrozen[iTop][6] >= 0:
				iTop = self.aFrozen[iTop][6]
			szName = self.getPlainCommandText(self.aFrozen[iTop][2][0])
			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			pCity = None
			(loopCity, iter) = pPlayer.firstCity(False)
			while loopCity:
				if loopCity.getName() == szName:
					pCity = loopCity
					break
				(loopCity, iter) = pPlayer.nextCity(iter, False)
			if pCity is None:
				return False
			if iKind == 1:
				# the producing goods: the marked ones are the goods whose raw materials are scarce or missing; the window shows these raw materials
				aTypes = self.getRawMaterialTypes(aTypes, pCity)
			import CvTradeRouteScreen
			if not CvTradeRouteScreen.isNewWindowEnabled():
				return False
			if len(aTypes) > 0:
				CvTradeRouteScreen.setTempFilter(aTypes)
			iOpened = CvScreensInterface.tradeRouteScreen.open(pCity.getID(), False)
			CvTradeRouteScreen.setTempFilter(None)
			if iOpened == 0:
				return False
			self.unfreezeAllTips()
			return True
		except:
			pass
		return False

	# the promotions named by the pictures of a line (<img=button path size=16>): their names and what they do
	def getPromotionTipText( self, szLine ):
		try:
			if len(self.dPromotionButtons) == 0:
				for i in range(gc.getNumPromotionInfos()):
					self.dPromotionButtons[gc.getPromotionInfo(i).getButton().replace("\\", "/").lower()] = i
			aszTexts = []
			aiDone = []
			for szPath in re.findall(u"<img=([^ >]+)", szLine):
				iPromotion = self.dPromotionButtons.get(str(szPath).replace("\\", "/").lower(), -1)
				if iPromotion < 0 or iPromotion in aiDone:
					continue
				aiDone.append(iPromotion)
				# the help text of the game starts with the name of the promotion itself
				szText = CyGameTextMgr().getPromotionHelp(iPromotion, False).strip()
				if len(szText) == 0:
					szText = u"<color=255,255,0,255>" + gc.getPromotionInfo(iPromotion).getDescription() + u"</color>"
				aszTexts.append(szText)
			return u"\n".join(aszTexts)
		except:
			return u""

	dPromotionButtons = {}

	# the text of the second window: what a right click opens, and all the hits of the line (the chosen one in yellow)
	# the player (not the own one) whose unit is named in the first line of a tooltip (the leader is the last part of the line): -1 if none or
	# if he cannot be talked to
	def getTalkPlayer( self, aszParas, iPara ):
		try:
			if iPara != 0 or len(aszParas) == 0:
				return -1
			if aszParas[0].find(u"<color=255,255,0,255>") != 0 and not self.isUnitHeader(aszParas[0]):
				return -1
			szHead = re.sub(u"<[^>]*>", u"", aszParas[0])
			szHead = u"".join([c for c in szHead if ord(c) < 0x2000])
			aParts = [x.strip() for x in szHead.split(u",") if len(x.strip()) > 0]
			if len(aParts) < 2:
				return -1
			szLeader = aParts[-1]
			eActive = gc.getGame().getActivePlayer()
			pActive = gc.getPlayer(eActive)
			for ePlayer in range(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(ePlayer)
				if ePlayer != eActive and pPlayer.isAlive() and pPlayer.getName() == szLeader:
					if pActive.canContact(ePlayer):
						return ePlayer
					return -1
		except:
			pass
		return -1

	# the child tooltip of a line: for the first line of a unit the draft of a ship and the ability to ignore borders, then the Colopedia
	# the line of the terrain in the tooltip of a plot: the name of the terrain (with the hills / peak before it) and then its yields, "Grassland, 6 [icon] , 7 [icon]";
	# -1 if there is none (the tooltip of a unit, a city ...)
	setTerrainNames = {} # the names of the terrains, features, hills and peak (the first part of the terrain line of a plot tooltip)
	def getTerrainLineIndex( self, aszParas ):
		try:
			if len(self.setTerrainNames) == 0:
				for e in range(gc.getNumTerrainInfos()):
					self.setTerrainNames[self.normTipText(gc.getTerrainInfo(e).getDescription())] = True
				for e in range(gc.getNumFeatureInfos()):
					self.setTerrainNames[self.normTipText(gc.getFeatureInfo(e).getDescription())] = True
				self.setTerrainNames[self.normTipText(localText.getText("TXT_KEY_PLOT_PEAK", ()))] = True
				self.setTerrainNames[self.normTipText(localText.getText("TXT_KEY_PLOT_HILLS", ())).replace(u"/", u"").strip()] = True
				self.setTerrainNames[u"Hills"] = True
			for i in range(len(aszParas)):
				szPlain = re.sub(u"<[^>]*>", u"", aszParas[i]).strip()
				if re.match(u"^[^,0-9]+, [0-9]+\\s*[\u2000-\uffff]", szPlain) is None:
					continue
				# (a unit header looks the same: only the names of terrains, features and the hills / peak count)
				aNames = [self.normTipText(x).strip() for x in szPlain.split(u",")[0].split(u"/")]
				bAll = True
				for szName in aNames:
					if not self.setTerrainNames.has_key(szName):
						bAll = False
				if bAll:
					return i
		except:
			pass
		return -1

	def getTipSecondText( self, iPara, iSel = -1, aszParas = None, iLevel = -1 ):
		szBase = self.getTipSecondTextBase(iPara, iSel, aszParas, iLevel)
		try:
			if iPara >= 0 and aszParas is not None and iPara < len(aszParas) and self.isWaypointPlotPara(aszParas[iPara]):
				aOpt = localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_PLOT_OPTIONS", ()).split(u"\n")
				if iSel >= 0 and iSel < len(aOpt):
					aOpt[iSel] = u"<color=255,255,0,255>" + aOpt[iSel] + u"</color>"
				return u"\n".join(aOpt)
		except:
			pass
		# the coordinates of the plot under the tooltip: in the child window of the line of the terrain ("Grassland, 6 [food] , 7 ...", also after
		# the line "Defense bonus"), not in the tooltip of a unit
		try:
			if iPara >= 0 and iSel < 0 and aszParas is not None and iPara == self.getTerrainLineIndex(aszParas):
				tXY = None
				if iLevel >= 0 and iLevel < len(self.aFrozen):
					tAnchor = self.aFrozen[iLevel][5]
					if tAnchor is not None and self.aFrozen[iLevel][6] < 0:
						tXY = (tAnchor[0], tAnchor[1])
				elif iLevel < 0 and not self.bHudHover:
					pPlotXY = CyInterface().getMouseOverPlot()
					if pPlotXY is not None and not pPlotXY.isNone():
						tXY = (pPlotXY.getX(), pPlotXY.getY())
				if tXY is not None:
					szXY = localText.getText("TXT_KEY_WTP_TIP_PLOT_COORDS", (tXY[0], tXY[1]))
					if len(szBase) > 0:
						szBase += u"\n" + szXY
					else:
						szBase = szXY
		except:
			pass
		try:
			if aszParas is not None and iSel < 0 and iPara >= 0 and iPara < len(aszParas) and self.isUnitHeader(aszParas[iPara]):
				szInfo = self.getUnitMoveInfoText(aszParas[iPara])
				if len(szInfo) > 0:
					if len(szBase) > 0:
						return szInfo + u"\n" + szBase
					return szInfo
		except:
			pass
		return szBase

	# the type of a unit of the first line of its tooltip: its name in the brackets
	def getUnitTypeOfHeader( self, szHeader ):
		try:
			szFirst = re.sub(u"<[^>]*>", u"", szHeader).split(u",")[0].strip()
			tName = re.search(u"\\(([^()]*)\\)\\s*$", szFirst)
			if tName is None:
				return -1
			if len(self.dUnitTypeByName) == 0:
				for eType in range(gc.getNumUnitInfos()):
					szName = gc.getUnitInfo(eType).getDescription()
					if not self.dUnitTypeByName.has_key(szName):
						self.dUnitTypeByName[szName] = eType
			return self.dUnitTypeByName.get(tName.group(1).strip(), -1)
		except:
			return -1

	# the draft of a ship (the waters that it cannot enter) and the ability to ignore borders; "" if there is nothing to tell
	def getUnitMoveInfoText( self, szHeader ):
		aLines = []
		eType = self.getUnitTypeOfHeader(szHeader)
		if eType < 0:
			return u""
		pInfo = gc.getUnitInfo(eType)
		try:
			if pInfo.getDomainType() == DomainTypes.DOMAIN_SEA:
				aWaters = []
				for eTerrain in range(gc.getNumTerrainInfos()):
					if pInfo.getTerrainImpassable(eTerrain) and gc.getTerrainInfo(eTerrain).isWater():
						aWaters.append(gc.getTerrainInfo(eTerrain).getDescription())
				aFeatures = []
				for eFeature in range(gc.getNumFeatureInfos()):
					if pInfo.getFeatureImpassable(eFeature):
						aFeatures.append(gc.getFeatureInfo(eFeature).getDescription())
				aAll = aWaters + aFeatures
				if len(aWaters) > 0:
					aLines.append(localText.getText("TXT_KEY_WTP_TIP_DRAFT_DEEP", (u", ".join(aAll),)))
				elif len(aFeatures) > 0:
					aLines.append(localText.getText("TXT_KEY_WTP_TIP_DRAFT_SHALLOW_LIM", (u", ".join(aAll),)))
				else:
					aLines.append(localText.getText("TXT_KEY_WTP_TIP_DRAFT_SHALLOW", ()))
			if hasattr(pInfo, "isRivalTerritory") and pInfo.isRivalTerritory():
				aLines.append(localText.getText("TXT_KEY_WTP_TIP_IGNORE_BORDERS", ()))
		except:
			pass
		return u"\n".join(aLines)

	# the own unit that a line of the first window names (the lines of the units of a plot: one line per unit, a right click selects the unit):
	# the plot is the one that the window was frozen at
	# the paragraph where the lines of the plot under the units begin. The terrain line is always there ("Hills/Jungle/Savanna, 7 ..."); the
	# lines of the plot that the game writes in front of it (the owner of the plot, the pioneer plan, the defense bonus: it is missing for many
	# plots) belong to the plot too. No terrain line found: the line "Defense bonus"; none of both: the number of paragraphs
	def getPlotStartPara( self, aszParas, pPlot ):
		try:
			iFirst = -1
			for k in range(len(aszParas)):
				if self.isUnitHeader(aszParas[k]):
					iFirst = k
					break
			if iFirst < 0:
				return len(aszParas)
			szDefense = self.getTipPrefix("TXT_KEY_PLOT_BONUS", (0,))
			aPre = [szDefense, self.getTipPrefix("TXT_KEY_PLOT_DEFENSIVE_BONUS_OWNED_PLOT", (0,)), self.getTipPrefix("TXT_KEY_PIONEER_PLAN_PLOT_HELP", (u"", 0))]
			aPre = [x for x in aPre if len(x) > 3]
			reTerrain = None
			if pPlot is not None and not pPlot.isNone() and pPlot.getTerrainType() >= 0:
				aNames = [self.normTipText(gc.getTerrainInfo(pPlot.getTerrainType()).getDescription()), self.normTipText(localText.getText("TXT_KEY_PLOT_PEAK", ()))]
				aNames = [re.escape(x) for x in aNames if len(x) > 0]
				if len(aNames) > 0:
					# (hills and the feature in front of the terrain: "Hills/Jungle/Savanna, 7 ...")
					reTerrain = re.compile(u"^(?:[^/,]{1,40}/){0,2}(?:" + u"|".join(aNames) + u")(?:[ ,]|$)", re.UNICODE)
			iTerrain = -1
			if reTerrain is not None:
				for k in range(iFirst + 1, len(aszParas)):
					if reTerrain.match(self.normTipText(aszParas[k])) is not None:
						iTerrain = k
						break
			if iTerrain < 0:
				for k in range(iFirst + 1, len(aszParas)):
					if len(szDefense) > 0 and self.normTipText(aszParas[k]).find(szDefense) == 0:
						return k
				return len(aszParas)
			# the names of the nations: a line with only the name of the owner of the plot
			aOwners = []
			for ePlayer in range(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(ePlayer)
				if pPlayer.isAlive():
					aOwners.append(self.normTipText(pPlayer.getCivilizationDescription(0)))
			iStart = iTerrain
			while iStart - 1 > iFirst:
				szPlain = self.normTipText(aszParas[iStart - 1])
				bPlotLine = (szPlain in aOwners)
				for szPre in aPre:
					if szPlain.find(szPre) == 0:
						bPlotLine = True
				if not bPlotLine:
					break
				iStart -= 1
			return iStart
		except:
			pass
		return len(aszParas)

	# the unit that a line of the first frozen window of a stack belongs to (every line from its first line up to the first line of the next
	# unit or of the plot): (unit, paragraph of its first line, first paragraph of the plot) or None. Not in the child windows
	def getBlockUnit( self, iLevel, aszParas, iPara ):
		try:
			if iLevel < 0 or iLevel >= len(self.aFrozen) or iPara < 0 or iPara >= len(aszParas):
				return None
			tUnitWin = self.dUnitWin.get(tuple(aszParas))
			if tUnitWin is not None:
				# a window that lists units (the child window "more...units"): every line is a unit, its plot lines are those of the stack window
				if iPara < len(tUnitWin[0]) and tUnitWin[0][iPara] is not None:
					pListed = gc.getPlayer(tUnitWin[0][iPara][0]).getUnit(tUnitWin[0][iPara][1])
					if pListed is not None and not pListed.isNone():
						return (pListed, iPara, -1)
				return None
			if self.aFrozen[iLevel][6] >= 0:
				return None
			tAnchor = self.aFrozen[iLevel][5]
			if tAnchor is not None:
				pPlot = CyMap().plot(tAnchor[0], tAnchor[1])
			else:
				pPlot = self.getStackPlot()
			iPlotStart = self.getPlotStartPara(aszParas, pPlot)
			if iPara >= iPlotStart:
				return None
			# (a window with one unit only is the tooltip of that unit alone: no child window that repeats it)
			iHeaders = 0
			for k in range(iPlotStart):
				if self.isUnitHeader(aszParas[k]):
					iHeaders += 1
			if iHeaders < 2:
				return None
			iHead = -1
			for k in range(iPara, -1, -1):
				if self.isUnitHeader(aszParas[k]):
					iHead = k
					break
			if iHead < 0:
				return None
			pUnit = self.getHeaderUnit(iLevel, aszParas, iHead, True)
			if pUnit is None:
				return None
			return (pUnit, iHead, iPlotStart)
		except:
			pass
		return None

	# the plot lines of the stack window that a window belongs to (the window itself, or its parent of the parents): the paragraphs of the tooltip
	# from the first line of the plot on
	def getRootPlotLines( self, iLevel ):
		iRoot = iLevel
		for k in range(10):
			if self.aFrozen[iRoot][6] < 0:
				break
			iRoot = self.aFrozen[iRoot][6]
		aszRoot = self.aFrozen[iRoot][2]
		tAnchor = self.aFrozen[iRoot][5]
		if tAnchor is not None:
			pPlot = CyMap().plot(tAnchor[0], tAnchor[1])
		else:
			pPlot = self.getStackPlot()
		return list(aszRoot[self.getPlotStartPara(aszRoot, pPlot):])

	# the child window of a line of a unit of a stack: the tooltip that the unit would have if it stood alone on the plot (its own help text,
	# then the lines of the plot). The hint of the right click (select the unit / talk) stands above the hint of the freezing; the Colopedia
	# is not offered here, it begins with the lines of this child window
	def showAloneUnitTip( self, screen, iLevel, aszParas, iPara, iCursorY, tAnchor ):
		try:
			tBlock = self.getBlockUnit(iLevel, aszParas, iPara)
			if tBlock is None:
				return False
			(pUnit, iHead, iPlotStart) = tBlock
			szUnit = self.stripCarries(CyGameTextMgr().getSpecificUnitHelp(pUnit, False, True)).strip()
			if len(szUnit) == 0:
				return False
			# the statistics of a transport (rows marked by the DLL): the child window of the line Statistics, as in the tooltip of the unit alone
			dStats = {}
			try:
				aStatFinal = self.foldTransportStats([[x, None] for x in szUnit.split(u"\n")])
				aStatParas = []
				for aStatEntry in aStatFinal:
					if aStatEntry[1] is not None:
						dStats[len(aStatParas)] = aStatEntry[1]
					aStatParas.append(aStatEntry[0])
				szUnit = u"\n".join(aStatParas)
			except:
				dStats = {}
			aLines = [szUnit]
			szSetRow = localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_SET", ())
			iSetSlot = -1
			if pUnit.getOwner() == gc.getGame().getActivePlayer():
				# (the line "Set waypoint..." stands directly below the promotions of the unit, below its name without them)
				aUnitParas = szUnit.split(u"\n")
				iSetSlot = self.getWaypointSlot(aUnitParas, 0)
				if iSetSlot > len(aUnitParas):
					iSetSlot = len(aUnitParas)
			szInfo = self.getUnitMoveInfoText(aszParas[iHead])
			if len(szInfo) > 0:
				aLines.append(szInfo)
			if iPlotStart >= 0:
				aPlotLines = list(aszParas[iPlotStart:])
			else:
				aPlotLines = self.getRootPlotLines(iLevel)
			# (not the line "Set waypoint..." of the parent window: this window gets its own)
			aPlotLines = [x for x in aPlotLines if x != szSetRow and x != localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_SET_ROW", ())]
			bOwn = (pUnit.getOwner() == gc.getGame().getActivePlayer())
			# the line "Commands" of the stack: it goes to the end of this window (with its child window, which begins with "Set waypoint...")
			szCmdLine = None
			szCmdDetails = u""
			if bOwn:
				try:
					iRoot = iLevel
					for k in range(10):
						if self.aFrozen[iRoot][6] < 0:
							break
						iRoot = self.aFrozen[iRoot][6]
					iCmdRoot = self.getCommandsPara(self.aFrozen[iRoot][2], self.aFrozen[iRoot][4])
					if iCmdRoot >= 0:
						szCmdRoot = self.aFrozen[iRoot][2][iCmdRoot]
						if szCmdRoot in aPlotLines:
							szCmdLine = szCmdRoot
							szCmdDetails = self.aFrozen[iRoot][4][iCmdRoot]
							aPlotLines = [x for x in aPlotLines if x != szCmdRoot]
				except:
					szCmdLine = None
			aLines += aPlotLines
			szHint = u""
			szTail = None
			tRowWp = None
			dDetails = None
			iMain = len(u"\n".join(aLines).split(u"\n"))
			if bOwn:
				szHint = localText.getText("TXT_KEY_WTP_TIP_SELECT_UNIT", (pUnit.getName(),))
				tUnit = (pUnit.getOwner(), pUnit.getID())
				if szCmdLine is not None:
					# (the line "Commands" below the hint of the unit)
					szTail = szCmdLine
					dDetails = {iMain: szSetRow + u"\n" + szCmdDetails}
					tRowWp = {"unit": tUnit, "sea": self.isSeaUnit(pUnit), "paras": {}, "cmd": iMain}
				else:
					tRowWp = {"unit": tUnit, "sea": self.isSeaUnit(pUnit), "paras": {iSetSlot: "row"}, "cmd": -1}
					aUnitParas = list(aLines[0].split(u"\n"))
					aUnitParas.insert(iSetSlot, localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_SET_ROW", ()))
					aLines[0] = u"\n".join(aUnitParas)
					# (the paragraphs behind the new line move down by one)
					dShiftStats = {}
					for kStat in dStats.keys():
						if kStat >= iSetSlot:
							dShiftStats[kStat + 1] = dStats[kStat]
						else:
							dShiftStats[kStat] = dStats[kStat]
					dStats = dShiftStats
			elif iHead == 0:
				eTalk = self.getTalkPlayer(aszParas, 0)
				if eTalk >= 0:
					szHint = localText.getText("TXT_KEY_WTP_TIP_TALK", (gc.getPlayer(eTalk).getCivilizationShortDescription(0),))
			self.showSecondTip(screen, u"\n".join(aLines), iCursorY, tAnchor, iLevel, None, szHint, szTail)
			if self.bSecondTipShown and tRowWp is not None:
				self.tPreviewWp = tRowWp
				self.tPreviewDetails = dDetails
			if self.bSecondTipShown and len(dStats) > 0:
				dAll = {}
				for kStat in dStats.keys():
					dAll[kStat] = dStats[kStat]
				if self.tPreviewDetails is not None:
					for kDet in self.tPreviewDetails.keys():
						dAll[kDet] = self.tPreviewDetails[kDet]
				self.tPreviewDetails = dAll
			return self.bSecondTipShown
		except:
			pass
		return False

	def getHeaderUnit( self, iLevel, aszParas, iPara, bAny = False ):
		try:
			if iLevel < 0 or iLevel >= len(self.aFrozen) or iPara < 0 or iPara >= len(aszParas):
				return None
			tUnitWin = self.dUnitWin.get(tuple(aszParas))
			if tUnitWin is not None:
				# a list of units ("more...units"): the unit of the line
				if iPara < len(tUnitWin[0]) and tUnitWin[0][iPara] is not None:
					pListed = gc.getPlayer(tUnitWin[0][iPara][0]).getUnit(tUnitWin[0][iPara][1])
					if pListed is not None and not pListed.isNone() and pListed.getOwner() == gc.getGame().getActivePlayer():
						return pListed
				return None
			if self.aFrozen[iLevel][6] >= 0 or not self.isUnitHeader(aszParas[iPara]):
				return None
			dHeads = self.dHeaderUnits.get(self.aFrozen[iLevel][0])
			if dHeads is not None and dHeads.has_key(iPara):
				pFix = gc.getPlayer(dHeads[iPara][0]).getUnit(dHeads[iPara][1])
				if pFix is not None and not pFix.isNone() and (bAny or pFix.getOwner() == gc.getGame().getActivePlayer()):
					return pFix
				return None
			szFirst = re.sub(u"<[^>]*>", u"", aszParas[iPara]).split(u",")[0].strip()
			iNth = 0
			for k in range(iPara):
				if self.isUnitHeader(aszParas[k]) and re.sub(u"<[^>]*>", u"", aszParas[k]).split(u",")[0].strip() == szFirst:
					iNth += 1
			tAnchor = self.aFrozen[iLevel][5]
			if tAnchor is not None:
				pPlot = CyMap().plot(tAnchor[0], tAnchor[1])
			else:
				pPlot = self.getStackPlot()
			if pPlot is None or pPlot.isNone():
				return None
			# the tooltip lists the selected units first, then the others in the order of the plot
			aSelected = []
			aOthers = []
			for k in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(k)
				if pUnit.IsSelected():
					aSelected.append(pUnit)
				else:
					aOthers.append(pUnit)
			aCands = []
			for pUnit in aSelected + aOthers:
				if self.unitMatchesHeader(pUnit, szFirst):
					aCands.append(pUnit)
			if iNth < len(aCands) and (bAny or aCands[iNth].getOwner() == gc.getGame().getActivePlayer()):
				return aCands[iNth]
		except:
			pass
		return None

	# the first part of the header line of a unit: its profession and the name of its type in brackets ("Colonial Militia (Veteran Infantry Soldier)"),
	# the name of the type alone for a unit without a profession ("Treasure")
	def unitMatchesHeader( self, pUnit, szFirst ):
		try:
			szName = re.sub(u"<[^>]*>", u"", pUnit.getName())
			if szFirst == szName or szFirst.find(szName + u" (") == 0:
				return True
			eProfession = pUnit.getProfession()
			if eProfession >= 0:
				szProfession = re.sub(u"<[^>]*>", u"", gc.getProfessionInfo(eProfession).getDescription())
				if szFirst == szProfession + u" (" + szName + u")" or szFirst == szProfession:
					return True
			szType = re.sub(u"<[^>]*>", u"", gc.getUnitInfo(pUnit.getUnitType()).getDescription())
			# (the type in the brackets only for a unit without an own name: units with names ("Tholen (War Galleon)") match by the name)
			if szName == szType and (szFirst == szType or szFirst.find(u"(" + szType + u")") >= 0):
				return True
		except:
			pass
		return False

	# the folded line "Buildings" of a city tooltip: the names of the buildings are in its child window
	def isBuildingsRow( self, iLevel, aszParas, iPara ):
		try:
			if iLevel >= 0 and iLevel < len(self.aFrozen) and iPara >= 0 and iPara < len(aszParas):
				return self.aFrozen[iLevel][4].has_key(iPara) and self.normTipText(aszParas[iPara]) == self.normTipText(localText.getText("TXT_KEY_WTP_TIP_BUILDINGS", ()))
		except:
			pass
		return False

	# the text of a line of a frozen tooltip that the Colopedia targets are taken from: the folded line "Buildings" has the names of the buildings
	# in its child window, so the buildings of the list are the targets of the line (mouse wheel: one after the other)
	def getPediaLineText( self, iLevel, aszParas, iPara ):
		if self.isBuildingsRow(iLevel, aszParas, iPara):
			return self.aFrozen[iLevel][4][iPara]
		return aszParas[iPara]

	# the targets of a line (all of them in the order of the wheel, or the default ones); the line "Buildings": only the buildings of its list
	def getPediaLineTargets( self, iLevel, aszParas, iPara, bAll ):
		szText = self.getPediaLineText(iLevel, aszParas, iPara)
		if bAll:
			aTargets = self.getTextPediaAllTargets(szText)
		else:
			aTargets = self.getTextPediaTargets(szText)
		if self.isBuildingsRow(iLevel, aszParas, iPara):
			aTargets = [t for t in aTargets if t[1] == CvScreenEnums.PEDIA_BUILDING]
		return aTargets

	def getTipSecondTextBase( self, iPara, iSel = -1, aszParas = None, iLevel = -1 ):
		try:
			if aszParas is None:
				aszParas = []
			szLine = aszParas[iPara]
			aTargets = self.getPediaLineTargets(iLevel, aszParas, iPara, False)
			aAll = self.getPediaLineTargets(iLevel, aszParas, iPara, True)
			eTalk = -1
			if iSel < 0:
				eTalk = self.getTalkPlayer(aszParas, iPara)
			pSelect = None
			if iSel < 0 and eTalk < 0:
				pSelect = self.getHeaderUnit(iLevel, aszParas, iPara)
			if eTalk >= 0 or pSelect is not None:
				# a unit of another nation: a right click talks to the nation; an own unit of a plot: it selects the unit; the Colopedia is Ctrl + right click
				if eTalk >= 0:
					szText = localText.getText("TXT_KEY_WTP_TIP_TALK", (gc.getPlayer(eTalk).getCivilizationShortDescription(0),))
				else:
					szText = localText.getText("TXT_KEY_WTP_TIP_SELECT_UNIT", (pSelect.getName(),))
				if len(aTargets) > 0:
					szText += u"\n" + localText.getText("TXT_KEY_WTP_TIP_PEDIA_HELP2", (aTargets[0][0],))
				if len(aAll) > 1:
					szText += u"\n" + localText.getText("TXT_KEY_WTP_TIP_PEDIA_LIST", ())
					for i in range(len(aAll)):
						szText += u"\n  " + aAll[i][0]
				return szText
			if len(aAll) == 0:
				return u""
			if iSel >= 0:
				iIdx = iSel
			else:
				iIdx = 0
				if len(aTargets) > 0:
					# (the first one of the default list)
					for i in range(len(aAll)):
						if aAll[i] == aTargets[0]:
							iIdx = i
			if iSel >= 0:
				szText = localText.getText("TXT_KEY_WTP_TIP_PEDIA_HELP", (aAll[iIdx][0],))
			else:
				if len(aTargets) == 0:
					return u""
				szText = localText.getText("TXT_KEY_WTP_TIP_PEDIA_HELP", (aTargets[0][0],))
				if len(aTargets) > 1:
					szText += u"\n" + localText.getText("TXT_KEY_WTP_TIP_PEDIA_HELP2", (aTargets[1][0],))
			if len(aAll) > 1:
				szText += u"\n" + localText.getText("TXT_KEY_WTP_TIP_PEDIA_LIST", ())
				for i in range(len(aAll)):
					if i == iIdx:
						szText += u"\n  <color=255,255,0,255>" + aAll[i][0] + u"</color>"
					else:
						szText += u"\n  " + aAll[i][0]
			return szText
		except:
			return u""

	def unfreezeAllTips( self ):
		while len(self.aFrozen) > 0:
			if not self.unfreezeCursorTooltip():
				break

	# Esc: the last frozen window is unfrozen (the window is gone, the ones before it stay frozen)
	def unfreezeCursorTooltip( self ):
		if len(self.aFrozen) == 0:
			self.bTipFrozen = False
			return False
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		self.hideSecondTip(screen)
		self.tSecondTipKey = None
		self.iTipSelPara = -1
		self.iTipSelIdx = 0
		if self.bTipWheel:
			self.bTipWheel = False
			try:
				self.setWheelCapture(False)
			except:
				pass
		(szPrefix, tLayout, aszParas, aiIndent, dDetails, tAnchor, iParent, tRel) = self.aFrozen.pop()
		try:
			self.deleteTipWindow(screen, szPrefix, len(tLayout[4]))
		except:
			pass
		# a companion window (the explanation of a folded line) goes together with the window it belongs to (the one below it)
		if self.dFrozenCompanion.has_key(szPrefix):
			del self.dFrozenCompanion[szPrefix]
			if len(self.aFrozen) > 0:
				(szPrefix, tLayout, aszParas, aiIndent, dDetails, tAnchor, iParent, tRel) = self.aFrozen.pop()
				try:
					self.deleteTipWindow(screen, szPrefix, len(tLayout[4]))
				except:
					pass
		self.bTipFrozen = (len(self.aFrozen) > 0)
		if not self.bTipFrozen:
			self.szSuppressHelp = u""
		return True

	def isPediaActive( self ):
		try:
			return CvScreensInterface.pediaMainScreen.getScreen().isActive()
		except:
			return False

	def isTipFrozen( self ):
		# (while the Colopedia is up, its keys are not ours: Esc closes the Colopedia and leaves the frozen window as it is)
		return self.bTipFrozen and not self.isPediaActive()

	# the paragraphs of a frozen window: level 0 is the first window, the others are the nested ones
	def getLevelParas( self, iLevel ):
		return self.aFrozen[iLevel][2]

	# the paragraphs for a command of a line of a frozen window: the commands of a city tooltip are folded into a child window, the name of the
	# city is the first line of its parent window
	def getCommandParas( self, iLevel, aszParas, iPara ):
		try:
			iParent = self.aFrozen[iLevel][6]
			if iParent >= 0:
				return ([self.aFrozen[iParent][2][0]] + list(aszParas), iPara + 1)
		except:
			pass
		return (aszParas, iPara)

	def isCommandLine( self, iLevel, aszParas, iPara ):
		(aszCmd, iCmd) = self.getCommandParas(iLevel, aszParas, iPara)
		return self.getCityCommand(aszCmd, iCmd) is not None or self.getUnitCommand(aszParas, iPara) is not None

	# the lines of the commands (select the city / all of the continent / all; select all units of the type / all units) in one line
	def isCommandText( self, szText ):
		try:
			szPlain = self.getPlainCommandText(szText)
			if szPlain == self.getPlainCommandText(localText.getText("TXT_KEY_MISC_ALT_SELECT", ())):
				return True
			szPre = self.getPlainCommandText(localText.getText("TXT_KEY_MISC_CTRL_SELECT", (u"QQQQ",))).split(u"QQQQ")[0].strip()
			return len(szPre) > 3 and szPlain.find(szPre) == 0
		except:
			return False

	# the command lines at the end of a city tooltip (select the city / all of the continent / all): (city, mode) or None
	# a text without color tags and without the signs < > (written as &lt; &gt; in one text and as < > in the other), words separated by one space
	def getPlainCommandText( self, szText ):
		szText = re.sub(u"</?(color|font|img)[^>]*>", u"", szText)
		szText = szText.replace(u"&lt;", u" ").replace(u"&gt;", u" ").replace(u"<", u" ").replace(u">", u" ")
		return u" ".join(szText.split())

	def getCityCommand( self, aszParas, iPara ):
		try:
			if iPara <= 0:
				return None
			szPara = self.getPlainCommandText(aszParas[iPara])
			if len(szPara) == 0:
				return None
			szCtrl = self.getPlainCommandText(localText.getText("TXT_KEY_CITY_BAR_SELECT_CTRL", ()))
			szAlt = self.getPlainCommandText(localText.getText("TXT_KEY_CITY_BAR_SELECT_ALT", ()))
			if szPara != szCtrl and szPara != szAlt and szPara.find(u"%") >= 0:
				return None
			szName = self.getPlainCommandText(aszParas[0])
			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			pCity = None
			(loopCity, iter) = pPlayer.firstCity(False)
			while loopCity:
				if loopCity.getName() == szName:
					pCity = loopCity
					break
				(loopCity, iter) = pPlayer.nextCity(iter, False)
			if pCity is None:
				return None
			if szPara == szCtrl:
				return (pCity, 1)
			if szPara == szAlt:
				return (pCity, 2)
			szSelect = self.getPlainCommandText(localText.getText("TXT_KEY_CITY_BAR_SELECT", (pCity.getName(),)))
			if szPara == szSelect:
				return (pCity, 0)
		except:
			pass
		return None

	# the command lines of the tooltip of a unit of the stack ("(< CTRL > to select all Treasure units)", "(< ALT > to select all units)"):
	# the plot of the stack of units (the one of the plot list)
	def getStackPlot( self ):
		pPlot = CyInterface().getSelectionPlot()
		if pPlot is None or pPlot.isNone():
			pHead = CyInterface().getHeadSelectedUnit()
			if pHead is not None and not pHead.isNone():
				pPlot = pHead.plot()
		if pPlot is None or pPlot.isNone():
			return None
		return pPlot

	# (mode, unit type) with mode 1: all units of that type on the plot, 2: all units of the domain (land / sea) of the unit of the tooltip;
	# the type is the one of the line "(< CTRL > to select all ... units)" of the same tooltip (the unit of the tooltip); None: no command
	def getUnitCommand( self, aszParas, iPara ):
		try:
			if iPara < 0 or iPara >= len(aszParas) or aszParas[iPara].find(u"(") < 0:
				return None
			pPlot = self.getStackPlot()
			if pPlot is None:
				return None
			szPara = self.getPlainCommandText(aszParas[iPara])
			szAlt = self.getPlainCommandText(localText.getText("TXT_KEY_MISC_ALT_SELECT", ()))
			eFound = -1
			for k in range(pPlot.getNumUnits()):
				eType = pPlot.getUnit(k).getUnitType()
				szCtrl = self.getPlainCommandText(localText.getText("TXT_KEY_MISC_CTRL_SELECT", (gc.getUnitInfo(eType).getTextKey(),)))
				if szPara == szCtrl:
					return (1, eType)
				if eFound < 0:
					for szOther in aszParas:
						if szOther.find(u"(") >= 0 and self.getPlainCommandText(szOther) == szCtrl:
							eFound = eType
							break
			if szPara == szAlt:
				if eFound < 0:
					pHead = CyInterface().getHeadSelectedUnit()
					if pHead is not None and not pHead.isNone():
						eFound = pHead.getUnitType()
				return (2, eFound)
		except:
			pass
		return None

	def runUnitCommand( self, aszParas, iPara ):
		try:
			tCommand = self.getUnitCommand(aszParas, iPara)
			if tCommand is None:
				return False
			(iMode, eType) = tCommand
			ePlayer = gc.getGame().getActivePlayer()
			pPlot = self.getStackPlot()
			eDomain = -1
			if iMode == 2 and eType >= 0:
				eDomain = gc.getUnitInfo(eType).getDomainType()
			aUnits = []
			for k in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(k)
				# (only units with moves left; Alt: the units of the same domain, land or sea)
				if pUnit.getOwner() == ePlayer and pUnit.movesLeft() > 0 and ((iMode == 2 and (eDomain < 0 or pUnit.getDomainType() == eDomain)) or (iMode == 1 and pUnit.getUnitType() == eType)):
					aUnits.append(pUnit)
			if len(aUnits) == 0:
				return False
			CyInterface().clearSelectionList()
			for pUnit in aUnits:
				CyInterface().selectUnit(pUnit, False, False, False)
			self.markTipSelection()
			self.unfreezeAllTips()
			return True
		except:
			pass
		return False

	# right click on such a line: the same as a click on the city banner (Ctrl: all cities of the continent, Alt: all cities): the cities are
	# selected (to give them production orders), the city screen is not opened
	def runCityCommand( self, aszParas, iPara ):
		try:
			tCommand = self.getCityCommand(aszParas, iPara)
			if tCommand is None:
				return False
			(pCity, iMode) = tCommand
			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			iArea = pCity.plot().getArea()
			CyInterface().clearSelectedCities()
			(loopCity, iter) = pPlayer.firstCity(False)
			while loopCity:
				if loopCity.getID() == pCity.getID() or iMode == 2 or (iMode == 1 and loopCity.plot().getArea() == iArea):
					CyInterface().addSelectedCity(loopCity)
				(loopCity, iter) = pPlayer.nextCity(iter, False)
			self.unfreezeAllTips()
			return True
		except:
			pass
		return False

	def openTipPedia( self, iData, bSecond, bShift = False ):
		try:
			iLevel = iData / 1000
			iPara = iData % 1000
			aszParas = self.getLevelParas(iLevel)
			# right click on the name line of the tooltip of an own city: the map looks at the city chosen in the list
			if self.tryCityListJump(iLevel, iPara, False):
				return
			# the line "Set as WP: name" of a plot: delete / rename the waypoint
			iPlotOption = -1
			if iPara == self.iTipSelPara and iLevel == self.iTipSelLevel:
				iPlotOption = self.iTipSelIdx
			if self.runWaypointPlotClick(iLevel, iPara, bSecond, bShift, iPlotOption):
				return
			# right click on the list of the stored / producing goods of a city: the import / export window of the city with these goods
			tKindHit = self.dFrozenKind.get(self.aFrozen[iLevel][0])
			if tKindHit is not None and tKindHit[0] == "list" and iPara >= 0 and iPara < len(aszParas):
				if self.openGoodsTradeWindow(iLevel, aszParas, tKindHit[1]):
					return
			# the same on the line "Stored..." / "Producing..." of the city tooltip itself (as if the right click was made in its child window)
			if tKindHit is None and iPara >= 0 and self.aFrozen[iLevel][4].has_key(iPara):
				aChild = self.carryColors(self.aFrozen[iLevel][4][iPara].split(u"\n"))
				iChildKind = -1
				if self.isStoredGoodsWindow(aChild):
					iChildKind = 0
				elif self.isStoredGoodsWindow(aChild, "TXT_KEY_CITY_BAR_PRODUCING"):
					iChildKind = 1
				if iChildKind >= 0 and self.openGoodsTradeWindow(iLevel, aChild, iChildKind):
					return
			if iPara >= 0 and iPara < len(aszParas):
				(aszCmd, iCmd) = self.getCommandParas(iLevel, aszParas, iPara)
				iOption = -1
				if iPara == self.iTipSelPara and iLevel == self.iTipSelLevel:
					iOption = self.iTipSelIdx
				iWpPara = iPara
				tWpHit = self.dWpWin.get(self.aFrozen[iLevel][0])
				if iOption >= 0 and tWpHit is not None and self.isWaypointList(tWpHit):
					# (the line and the choice that shift + mouse wheel has chosen in a list of waypoints)
					aWpStops = self.getWaypointStops(tWpHit)
					if iOption < len(aWpStops):
						iWpPara = aWpStops[iOption][0]
						iOption = aWpStops[iOption][1]
				kindWp = None
				if iOption >= 0 and tWpHit is not None and tWpHit["paras"].get(iPara) == "row":
					# (the line "Set waypoint..." with a line of the list chosen with the wheel: 0 a new waypoint, then the waypoints)
					aView = self.getWaypointView(tWpHit["sea"])
					if iOption == 0 or iOption > len(aView):
						kindWp = "new"
					else:
						kindWp = aView[iOption - 1][0]
					iOption = -1
				if iOption >= 0 and self.aFrozen[iLevel][4].has_key(iPara) and iPara == self.getCommandsPara(aszParas, self.aFrozen[iLevel][4]):
					# (the line "Commands" with a line of its child window chosen with the wheel: that command is run)
					aChildCmd = self.carryColors(self.aFrozen[iLevel][4][iPara].split(u"\n"))
					if iOption < len(aChildCmd):
						if aChildCmd[iOption] == localText.getText("TXT_KEY_WTP_TIP_WAYPOINT_SET", ()) and tWpHit is not None:
							pCmdUnit = gc.getPlayer(tWpHit["unit"][0]).getUnit(tWpHit["unit"][1])
							if pCmdUnit is not None and not pCmdUnit.isNone():
								self.startWaypointMode(pCmdUnit)
								return
						elif self.runUnitCommand(aChildCmd, iOption) or self.runCityCommand([aszParas[0]] + aChildCmd, iOption + 1):
							return
				if kindWp is not None and kindWp != "new" and (bSecond or bShift) and self.bSecondTipShown:
					# (delete / rename from the line "Set waypoint...": the list is frozen first, the windows stay frozen afterwards)
					self.freezePreview(CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE))
				if self.runWaypointClick(iLevel, iWpPara, bSecond, bShift, iOption, kindWp):
					try:
						screenWp = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
						self.hideSecondTip(screenWp)
						self.tSecondTipKey = None
						self.iTipSelPara = -1
						if self.bTipWheel:
							self.bTipWheel = False
							self.setWheelCapture(False)
					except:
						pass
					return
				if self.runCityCommand(aszCmd, iCmd) or self.runUnitCommand(aszParas, iPara):
					return
				aTargets = self.getPediaLineTargets(iLevel, aszParas, iPara, False)
				eTalk = -1
				pSelect = None
				tBlock = None
				if not (iPara == self.iTipSelPara and iLevel == self.iTipSelLevel):
					# a line of a unit of a stack: right click selects the unit (the first unit of the tooltip of another nation: talks); the
					# Colopedia is not opened from these lines, it begins with the child window of the unit
					tBlock = self.getBlockUnit(iLevel, aszParas, iPara)
					if tBlock is not None:
						if tBlock[0].getOwner() == gc.getGame().getActivePlayer():
							pSelect = tBlock[0]
						elif tBlock[1] == 0:
							eTalk = self.getTalkPlayer(aszParas, 0)
					else:
						eTalk = self.getTalkPlayer(aszParas, iPara)
						if eTalk < 0:
							pSelect = self.getHeaderUnit(iLevel, aszParas, iPara)
				if pSelect is not None:
					if bShift and tBlock is not None:
						# a line of an own unit of a stack: Shift + right click sets a waypoint for it
						self.startWaypointMode(pSelect)
						return
					elif bSecond:
						if tBlock is None:
							self.openPediaTargetIndex(aTargets, 0)
					else:
						CyInterface().selectUnit(pSelect, True, False, False)
						self.markTipSelection()
						if tBlock is not None:
							screenSel = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
							# the frozen tooltip of the unit that was selected before goes
							if len(self.szAutoSelPrefix) > 0:
								tKeySel = self.tSecondTipKey
								for iOldSel in range(len(self.aFrozen)):
									if self.aFrozen[iOldSel][0] == self.szAutoSelPrefix:
										self.closeFrozenChild(screenSel, iOldSel)
										break
								self.tSecondTipKey = tKeySel
								self.szAutoSelPrefix = u""
								self.tAutoSelUnit = None
							self.refreshWaypointRows(screenSel, pSelect)
						if tBlock is not None and self.bSecondTipShown and self.tPreviewLayout is not None:
							# a line of a unit of a stack: the tooltip of the unit (beside the line) is frozen at once
							self.dropPreviewSelectHint()
							self.freezePreview(CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE))
							self.szAutoSelPrefix = self.aFrozen[-1][0]
							self.tAutoSelUnit = (pSelect.getOwner(), pSelect.getID())
						else:
							self.unfreezeAllTips()
						return
				elif eTalk >= 0:
					if bSecond:
						if tBlock is None:
							self.openPediaTargetIndex(aTargets, 0)
					else:
						self.unfreezeAllTips()
						gc.getPlayer(gc.getGame().getActivePlayer()).contact(eTalk)
						return
				elif tBlock is not None:
					pass
				elif iPara == self.iTipSelPara and iLevel == self.iTipSelLevel:
					aTargets = self.getPediaLineTargets(iLevel, aszParas, iPara, True)
					# the target chosen with shift + mouse wheel
					self.openPediaTargetIndex(aTargets, self.iTipSelIdx)
				else:
					self.openPediaTargets(aTargets, bSecond)
		except:
			pass
		# the window stays frozen (to look up more lines after the Colopedia is closed); the wheel is given back, the second window goes
		try:
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			self.hideSecondTip(screen)
			self.tSecondTipKey = None
			if self.bTipWheel:
				self.bTipWheel = False
				self.setWheelCapture(False)
		except:
			pass

	# distance from the cursor position (hot spot) to the lower end of the cursor picture: the tooltip windows start there
	def getCursorBottom( self, yRes ):
		return max(20, int(yRes * 0.025))

	def getTipAvoidRect( self, iCursorX, iCursorY ):
		# the own windows whose elements have a tooltip: the tooltip appears beside the window, not over it
		aRects = []
		# (windows of other parts of the mod, if there are any: the import / export window, the amount dialog, the message panel)
		try:
			t = getattr(CvScreensInterface, "tradeRouteScreen", None)
			if t is not None and t.isOpen():
				aRects.append(t.getScreenRect())
		except:
			pass
		try:
			t = getattr(CvScreensInterface, "yieldAmountScreen", None)
			if t is not None and t.isOpen():
				aRects.append((t.iGX, t.iGY, t.W, t.H))
		except:
			pass
		aRects.append(self.tMsgRect)
		try:
			if gc.getGame().isDiplomacyUp():
				# the diplomacy window: in the middle of the screen, about 474 x 730 pixels (measured at 2560 x 1440; a little margin). The trade
				# window (two lists beside it) is about 1005 x 735: the game does not tell which of both is open, so the wider rectangle is used
				scrDiplo = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
				# the middle column (the plain dialog is only this wide: the tooltip of the portrait stands right beside it, not beside the
				# trade window; 1440p only) comes first
				if scrDiplo.getYResolution() == 1440:
					aRects.append((scrDiplo.getXResolution() / 2 - 248, scrDiplo.getYResolution() / 2 - 376, 496, 752))
				aRects.append((scrDiplo.getXResolution() / 2 - 512, scrDiplo.getYResolution() / 2 - 376, 1024, 752))
		except:
			pass
		for (x, y, w, h) in aRects:
			if w > 0 and iCursorX >= x and iCursorX < x + w and iCursorY >= y and iCursorY < y + h:
				return (x, y, w, h)
		return None

	def getCursorTipNames( self ):
		aszNames = ["HudTipBack1", "HudTipBack2", "HudTipBack3"]
		for i in range(self.iCursorTipLines):
			aszNames.append("HudTipLine%d" % i)
		return aszNames

	# the help area of the game tooltip: while the own tooltip is on it is put far outside of the screen (the game still shows its tooltip of a
	# HUD element for a moment before our window takes over)
	def setGameHelpArea( self, screen, iY ):
		iX = HELTTEXT_AREA_X_MARGIN
		if self.bHoverTip:
			iX = -5000
		screen.setHelpTextArea( HELPTEXT_AREA_MAX_WIDTH, FontTypes.SMALL_FONT, iX, iY, -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELPTEXT_AREA_MIN_WIDTH )

	def toggleHoverTip( self ):
		# 0: hover tooltip at the cursor, 1: own tooltip window at the place of the game tooltip, 2: off (game tooltip)
		self.setHoverTipMode((self.iTipMode + 1) % 3, True)

	# the DLL hides the game help of HUD elements while the diplomacy screen is open and the own tooltip is on
	def sendHideGameHelp( self ):
		try:
			gc.getGame().setHideGameHelp(self.bHoverTip)
		except:
			pass

	# also called by the options screen (Game tab); bMessage: the message of the hotkey
	def setHoverTipMode( self, iMode, bMessage ):
		self.iTipMode = iMode
		self.bHoverTip = (self.iTipMode != 2)
		self.sendHideGameHelp()
		self.saveTipSettings()
		self.unfreezeAllTips()
		self.bTipFrozen = False
		try:
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			self.bHudHover = False
			self.hideCursorTooltip(screen)
			self.setGameHelpArea(screen, screen.getYResolution() - SADDLE_HEIGHT)
			if self.iTipMode == 0:
				szKey = "TXT_KEY_WTP_HOVER_TIP_ON"
			elif self.iTipMode == 1:
				szKey = "TXT_KEY_WTP_HOVER_TIP_ORIGINAL"
			else:
				szKey = "TXT_KEY_WTP_HOVER_TIP_OFF"
				screen.setHelpTextString("")
			if bMessage:
				self.showModMessage(localText.getText(szKey, ()))
		except:
			pass

	def isHudHover( self ):
		if not self.bHudHover:
			return False
		try:
			# the game asks for the help text again with every cursor move over the element (log). A cursor that has moved away from the place
			# of the last question and is not asked about any more has left the element; far away it has surely left it
			iDist = max(abs(gc.getGame().getCursorClientX() - self.tHudHoverAt[0]), abs(gc.getGame().getCursorClientY() - self.tHudHoverAt[1]))
			if iDist > 150 or (iDist > 35 and self.iTick - self.iWidgetHelpTick >= 3):
				self.bHudHover = False
				self.szHudHelp = u""
		except:
			pass
		return self.bHudHover

	# called by the game when it asks for the help text of a widget under the cursor (CvScreensInterface.getWidgetHelp)
	iLastWidgetType = -1 # the widget type of the last help text that was shown as the own tooltip

	# the own tooltip of a button of the list of the game popups (what a colony builds: WIDGET_TRAIN / WIDGET_CONSTRUCT / WIDGET_CONVINCE):
	# the popup is above all screens of python, so the tooltip stands beside it (the left edge of the screen) and cannot be frozen (the keys go to the popup)
	def isPopupWidgetTip( self ):
		try:
			return self.bHudHover and not CyInterface().isCityScreenUp() and self.iLastWidgetType in (int(WidgetTypes.WIDGET_TRAIN), int(WidgetTypes.WIDGET_CONSTRUCT), int(WidgetTypes.WIDGET_CONVINCE))
		except:
			return False

	def widgetHelpSeen( self, szText, eWidgetType ):
		if not self.bHoverTip:
			return
		self.iLastWidgetType = int(eWidgetType)
		try:
			if self.bTipFrozen and self.getFrozenAt(gc.getGame().getCursorClientX(), gc.getGame().getCursorClientY()) >= 0:
				return
			if szText and len(szText) > 0 and int(eWidgetType) == int(WidgetTypes.WIDGET_CONTACT_CIV) and not self.isCursorInScoreTable():
				# (log: after a click on a unit the game reports the contact help of the score table although the cursor is on the map)
				return
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			if szText and len(szText) > 0 and int(eWidgetType) == int(WidgetTypes.WIDGET_HELP_YIELD) and self.isTradeWindowOpen():
				if self.isYieldTipFrozen(CvScreensInterface.tradeRouteScreen.getIconYieldAt(gc.getGame().getCursorClientX(), gc.getGame().getCursorClientY())):
					# (the tooltip of this good is frozen: no second one as long as it is; the one of the good before goes away too)
					screen.setHelpTextString(u"")
					if self.bCursorTipShown or self.szPendingHelp is not None:
						self.hideCursorTooltip(screen)
					return
			if szText and len(szText) > 0 and int(eWidgetType) == int(WidgetTypes.WIDGET_HELP_YIELD):
				szText = self.addRawNote(szText)
			if szText and len(szText) > 0:
				self.iWidgetHelpTick = self.iTick
				self.bHudHover = True
				self.tHudHoverAt = (gc.getGame().getCursorClientX(), gc.getGame().getCursorClientY())
				self.szHudHelp = szText
				self.showCursorTooltip(screen, szText, True)
				# the game tooltip is not shown while the own one is on
				screen.setHelpTextString(u"")
			elif int(eWidgetType) == int(WidgetTypes.WIDGET_GENERAL) and self.bHudHover:
				# the game asks for the help of "nothing in particular". Directly after the text of a widget (same place) it does that
				# too (log), so only a cursor that has moved away from the last widget text means that the HUD element was left
				if abs(gc.getGame().getCursorClientX() - self.tHudHoverAt[0]) > 4 or abs(gc.getGame().getCursorClientY() - self.tHudHoverAt[1]) > 4:
					self.bHudHover = False
					self.szHudHelp = u""
			# empty texts are ignored: the game reports them all the time on the map (log: type 24), they must not block the plot help
		except:
			pass

	# is there a frozen tooltip of this good (import / export window)?
	def isYieldTipFrozen( self, iYield ):
		if iYield < 0:
			return False
		for tFz in self.aFrozen:
			if self.dTraderWin.get(tFz[0], -1) == iYield:
				return True
		return False

	# THE TOOLTIP OF A GOOD: the lines of the ports (Europe, Africa, Port Royal: prices) are one line "Value..." under the name of the good, the
	# ports are in its child tooltip. Returns the paragraphs (self.dTipDetails set) or None if the text is no tooltip of a good with such lines.
	def foldYieldDetails( self, aszParas ):
		try:
			if len(aszParas) < 3:
				return None
			if not hasattr(self, "aszYieldNames"):
				self.aszYieldNames = {}
				for iYield in range(YieldTypes.NUM_YIELD_TYPES):
					self.aszYieldNames[self.normTipText(gc.getYieldInfo(iYield).getDescription())] = True
			if not self.aszYieldNames.has_key(self.normTipText(aszParas[0])):
				return None
			iFirst = -1
			iLast = -1
			for i in range(1, len(aszParas)):
				if self.dTraderLines.has_key(self.normTipText(aszParas[i])):
					# (the cities that import / export the good are not prices)
					if iFirst >= 0:
						break
					continue
				if re.search(u"(?i)\\t|<tab>", aszParas[i]) is not None and re.sub(u"(?i)<[^>]*>|\\t", u"", aszParas[i]).strip() != u"":
					if iFirst < 0:
						iFirst = i
					iLast = i
				elif iFirst >= 0:
					break
			if iFirst < 0 or iLast - iFirst < 1:
				return None
			self.dTipDetails = {}
			aLines = self.alignTabLines(list(aszParas[iFirst:iLast + 1]))
			aNew = list(aszParas[:iFirst]) + [localText.getText("TXT_KEY_WTP_TIP_VALUE_FOLD", ())] + list(aszParas[iLast + 1:])
			self.dTipDetails[iFirst] = u"\n".join(aLines)
			return aNew
		except:
			self.dTipDetails = {}
			return None

	# (the blanks to put behind a text of the width fW, the number of tab stops it has passed then)
	def getTabGuard( self, fW, fLine = 22.0 ):
		fSpace = 3.98 * fLine / 22.0
		iBlanks = 0
		while iBlanks < 6:
			fFrac = (fW + iBlanks * fSpace) % self.TAB_STOP
			if fFrac >= 8.0 and fFrac <= self.TAB_STOP - 8.0:
				break
			iBlanks += 1
		return (iBlanks, int((fW + iBlanks * fSpace) / self.TAB_STOP))

	# lines in a row with a name, tabs and then text: the text of all of them starts at the same stop
	def alignTabLines( self, aszParas ):
		try:
			fTabLine = float(self.getTipLineDistance(0))
			aRuns = []
			for szPara in aszParas:
				mTab = re.match(u"(?is)^(.*?)((?:\\t| |<tab>)*(?:\\t|<tab>)(?:\\t| |<tab>)*)(\\S.*)$", szPara)
				if mTab is None or mTab.group(1).strip() == u"":
					aRuns.append(None)
					continue
				aRuns.append(mTab)
			aNew = list(aszParas)
			i = 0
			while i < len(aszParas):
				if aRuns[i] is None:
					i += 1
					continue
				j = i
				while j < len(aszParas) and aRuns[j] is not None:
					j += 1
				if j - i >= 2:
					aEnds = []
					aWidths = []
					for k in range(i, j):
						fW = self.getTextPixels(re.sub(u"<[^>]*>", u"", aRuns[k].group(1)), fTabLine)
						(iBlanks, iPassed) = self.getTabGuard(fW, fTabLine)
						aWidths.append((iBlanks, iPassed))
						aEnds.append(iPassed + len(re.findall(u"(?i)\\t|<tab>", aRuns[k].group(2))))
					if min(aEnds) != max(aEnds):
						for k in range(i, j):
							mTab = aRuns[k]
							szMark = u"\t"
							if mTab.group(2).lower().find(u"<tab>") >= 0:
								szMark = u"<tab>"
							aNew[k] = mTab.group(1) + u" " * aWidths[k - i][0] + szMark * (max(aEnds) - aWidths[k - i][1]) + mTab.group(3)
				i = j
			return aNew
		except:
			return aszParas

	# THE CITIES IN THE TOOLTIP OF A GOOD (import / export window). One line for every colony that imports or exports the good: "Imports" in
	# the color of the import on the left of the name, "Exports" in the export color on the right of it. The names stand under each other
	# (a line without the left word gets blanks of its width). A left click on the line of a frozen tooltip jumps to the colony with its window
	# on the page of the good; closing that window takes the player back (same view, the tooltip frozen again, the cursor where it was).
	def getTradersNote( self, iYield ):
		try:
			aTraders = CvScreensInterface.tradeRouteScreen.getTraders(iYield)
			# the colony the window belongs to is the first line
			iOwn = CvScreensInterface.tradeRouteScreen.iCity
			aTraders = [t for t in aTraders if t[0] == iOwn] + [t for t in aTraders if t[0] != iOwn]
			if len(aTraders) == 0:
				return localText.getText("TXT_KEY_WTP_TIP_TRADERS_NONE", ())
			szImp = localText.getText("TXT_KEY_WTP_TIP_TRADERS_IMPORTS", ())
			szExp = localText.getText("TXT_KEY_WTP_TIP_TRADERS_EXPORTS", ())
			# the columns are tab stops (as the sell prices of the cargo lines): the names stand under each other exactly, the word "Exports" too
			aShown = aTraders[:15]
			fTabLine = float(self.getTipLineDistance(0))
			(iGuardImp, iPassedImp) = self.getTabGuard(self.getTextPixels(szImp, fTabLine), fTabLine)
			iNameStop = iPassedImp + 1
			aGuardName = []
			iEnd = 0
			for t in aShown:
				(iGuard, iPassed) = self.getTabGuard(iNameStop * self.TAB_STOP + self.getTextPixels(t[1], fTabLine), fTabLine)
				aGuardName.append((iGuard, iPassed))
				iEnd = max(iEnd, iPassed + 1)
			aLines = []
			for k in range(len(aShown)):
				(iCity, szName, bImp, bExp) = aShown[k]
				if bImp:
					szLine = WtpColors.tag(WtpColors.IMPORT, szImp) + u" " * iGuardImp + u"\t"
				else:
					szLine = u"\t" * iNameStop
				szLine += szName
				if bExp:
					szLine += u" " * aGuardName[k][0] + u"\t" * (iEnd - aGuardName[k][1]) + WtpColors.tag(WtpColors.EXPORT, szExp)
				aLines.append(szLine)
				self.dTraderLines[self.normTipText(szLine)] = iCity
			if len(aTraders) > 15:
				aLines.append(localText.getText("TXT_KEY_WTP_TIP_TRADERS_MORE", (len(aTraders) - 15,)))
			return u"\n".join(aLines)
		except:
			return u""

	# a left click on a line of a frozen window: is it the line of a colony of the traders? Then the jump is made (True)
	def tryTraderJump( self, iLevel, iPara ):
		try:
			if iLevel < 0 or iLevel >= len(self.aFrozen) or not self.dTraderWin.has_key(self.aFrozen[iLevel][0]):
				return False
			aszParas = self.aFrozen[iLevel][2]
			if iPara < 0 or iPara >= len(aszParas):
				return False
			iCity = self.dTraderLines.get(self.normTipText(aszParas[iPara]))
			if iCity is None:
				return False
			return self.jumpToTradeCity(iLevel, iCity, self.dTraderWin[self.aFrozen[iLevel][0]])
		except:
			return False

	def jumpToTradeCity( self, iLevel, iCity, iYield ):
		tWin = CvScreensInterface.tradeRouteScreen
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
		pCity = pPlayer.getCity(iCity)
		if pCity is None or pCity.isNone() or not tWin.isOpen():
			return False
		if iCity == tWin.iCity:
			# (the window of this colony is open: only its page goes to the good)
			tWin.showYield(iYield)
			return True
		# what the way back needs: the window with what it shows, the view (city screen or map), the frozen tooltip and where the cursor was
		tFz = self.aFrozen[iLevel]
		tR = {"state": tWin.getState(), "city": tWin.iCity, "map": not CyInterface().isCityScreenUp(), "yield": iYield,
			"frozen": (tFz[1], list(tFz[2]), list(tFz[3]), dict(tFz[4]), tFz[5]),
			"cursor": (gc.getGame().getCursorClientX(), gc.getGame().getCursorClientY()), "look": None, "zoom": None, "unit": None}
		if tR["map"]:
			try:
				tR["look"] = CyCamera().GetLookAt()
			except:
				tR["look"] = None
			try:
				tR["zoom"] = CyCamera().GetZoom()
			except:
				pass
			try:
				pUnit = CyInterface().getHeadSelectedUnit()
				if pUnit is not None and not pUnit.isNone():
					tR["unit"] = (pUnit.getOwner(), pUnit.getID())
			except:
				pass
		# a colony is in the stack only once: a jump away from a colony that is in it already (the jumps went round in a circle) takes the way
		# back to the first time, the loop between is dropped
		iSame = -1
		for iStack in range(len(self.aTradeReturn)):
			if self.aTradeReturn[iStack]["city"] == tR["city"]:
				iSame = iStack
				break
		if iSame >= 0:
			self.aTradeReturn = self.aTradeReturn[:iSame + 1]
		else:
			self.aTradeReturn.append(tR)
		tWin.finish(False, -1, True)
		self.unfreezeAllTips()
		if tR["map"]:
			# the window of the starting colony was open on the map: the jump stays on the map (the camera goes to the colony, its window opens there)
			try:
				CyCamera().JustLookAtPlot(pCity.plot())
			except:
				CvUtil.pyPrint("WTP trade jump: JustLookAtPlot failed")
		else:
			CyInterface().selectCity(pCity, False)
		self.tReopenTrade = {"city": iCity, "condensed": False, "focus": iYield, "map": tR["map"]}
		self.iReopenTries = 0
		self.iReopenWait = 3
		try:
			CyInterface().playGeneralSound(self.szModJumpSound)
		except:
			pass
		return True

	bTradeReturnPending = False # the way back of a jump that started in a city screen waits until the city screen of the colony of the jump is left

	# the window that was opened by a jump is closed by the player: back to where the jump started
	def tradeWindowClosed( self ):
		try:
			if len(self.aTradeReturn) == 0:
				return
			if not self.aTradeReturn[-1]["map"] and CyInterface().isCityScreenUp():
				# (the jump started in a city screen: closing the window (ok / cancel) does not take the player back, he stays in the city screen of the
				# colony of the jump; leaving that city screen is what takes him back, see checkTradeReturnPending)
				self.bTradeReturnPending = True
				return
			self.doTradeReturn()
		except:
			self.tReopenTrade = None

	# the city screen of the colony of a jump is left (the window is closed): now the way back, to the colony the jump started in
	def checkTradeReturnPending( self ):
		if not self.bTradeReturnPending:
			return
		try:
			if len(self.aTradeReturn) == 0:
				self.bTradeReturnPending = False
				return
			if CyInterface().isCityScreenUp() or self.isTradeWindowOpen() or self.tReopenTrade is not None:
				return
			self.bTradeReturnPending = False
			self.doTradeReturn()
		except:
			self.bTradeReturnPending = False

	def doTradeReturn( self ):
		try:
			tR = self.aTradeReturn.pop()
			# (the tooltip that was frozen in the colony of the jump goes: the one of the starting colony is made again)
			self.unfreezeAllTips()
			if tR["map"]:
				# (back to the map: nothing to leave when the jump stayed on the map)
				if CyInterface().isCityScreenUp():
					try:
						CyInterface().clearSelectedCities()
					except:
						CvUtil.pyPrint("WTP trade jump: clearSelectedCities failed")
			else:
				pCity = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(tR["city"])
				if pCity is not None and not pCity.isNone():
					CyInterface().selectCity(pCity, False)
			try:
				CyInterface().playGeneralSound(self.szModJumpSound)
			except:
				pass
			tState = dict(tR["state"])
			tState["map"] = tR["map"]
			tState["return"] = tR
			self.tReopenTrade = tState
			self.iReopenTries = 0
			self.iReopenWait = 3
		except:
			self.tReopenTrade = None

	def updatePostJump( self ):
		t = self.tPostJump
		if t is None:
			return
		try:
			if not self.isTradeWindowOpen():
				self.tPostJump = None
				return
			gc.getGame().setCursorClient(t["pos"][0], t["pos"][1])
			if t["wait"] > 0:
				t["wait"] -= 1
				return
			self.tPostJump = None
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			szHelp = gc.getGame().getWidgetHelpFor(int(WidgetTypes.WIDGET_HELP_YIELD), t["yield"], CvScreensInterface.tradeRouteScreen.iCity, False)
			if szHelp and len(szHelp) > 0:
				szHelp = self.addRawNote(szHelp, t["yield"])
				self.showCursorTooltip(screen, szHelp, True, True)
				self.freezeCursorTooltip()
		except:
			self.tPostJump = None

	# a change in the import / export window: the frozen tooltips of the good (all goods: -1) are made again with the new state (colonies that
	# import / export it, the sum) and stand where they stood; their child windows are closed
	def refreshTradeTips( self, iYieldOnly = -1 ):
		try:
			if not self.isTradeWindowOpen():
				return
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			aTargets = []
			for tFz in self.aFrozen:
				if self.dTraderWin.has_key(tFz[0]) and tFz[6] < 0 and (iYieldOnly < 0 or self.dTraderWin[tFz[0]] == iYieldOnly):
					aTargets.append((self.dTraderWin[tFz[0]], tFz[1][0], tFz[1][1], tFz[5]))
			tWin = CvScreensInterface.tradeRouteScreen
			for (iYield, iOldX, iOldY, tAnchor) in aTargets:
				for i in range(len(self.aFrozen)):
					if self.dTraderWin.get(self.aFrozen[i][0], -1) == iYield and self.aFrozen[i][6] < 0:
						self.closeFrozenChild(screen, i)
						break
				szHelp = gc.getGame().getWidgetHelpFor(int(WidgetTypes.WIDGET_HELP_YIELD), iYield, tWin.iCity, False)
				if not szHelp or len(szHelp) == 0:
					continue
				szHelp = self.addRawNote(szHelp, iYield)
				self.szSuppressHelp = u""
				self.szCursorTipText = u""
				self.bCursorTipShown = False
				self.bForceTradeTip = True
				try:
					self.showCursorTooltip(screen, szHelp, True, True)
				finally:
					self.bForceTradeTip = False
				if self.bCursorTipShown and self.freezeCursorTooltip() and len(self.aFrozen) > 0:
					iNew = len(self.aFrozen) - 1
					self.aFrozen[iNew][5] = tAnchor
					self.moveFrozenWindow(screen, iNew, iOldX, iOldY)
		except:
			self.tipError("refreshTradeTips")

	# the window of the starting colony is open again: the camera and the selected unit of the map, the frozen tooltip and the cursor as they were
	def restoreMapView( self, tR ):
		try:
			if tR["unit"] is not None:
				pUnit = gc.getPlayer(tR["unit"][0]).getUnit(tR["unit"][1])
				if pUnit is not None and not pUnit.isNone():
					CyInterface().selectUnit(pUnit, True, False, False)
		except:
			pass
		try:
			if tR["look"] is not None:
				CyCamera().JustLookAt(tR["look"])
			else:
				pCity = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(tR["city"])
				CyCamera().JustLookAtPlot(pCity.plot())
			if tR["zoom"] is not None:
				CyCamera().SetZoom(tR["zoom"])
		except:
			pass

	def keyEscDown( self ):
		if not self.bEscHeld:
			self.bEscHeld = True
			self.bEscHoldDone = False
			self.fEscStart = self.getTipNow()

	def updateEscHold( self ):
		try:
			if not self.bEscHeld or self.bEscHoldDone:
				return
			if self.getTipNow() - self.fEscStart < 600:
				return
			if self.isTradeWindowOpen():
				self.bEscHoldDone = True
				if len(self.aTradeReturn) > 0:
					self.closeAllTradeWindows(False)
			elif self.tReopenTrade is None:
				self.bEscHoldDone = True
		except:
			self.bEscHoldDone = True

	# an import / export window is open that was opened by a jump (there are windows stacked)
	def isTradeStackOpen( self ):
		try:
			return self.isTradeWindowOpen() and len(self.aTradeReturn) > 0
		except:
			return False

	# all stacked windows go. bBack (X held): back to the view the first jump started in (the colony, or the map as it was); otherwise (Esc held)
	# no jump: the city screen is left, on the map the windows just close
	def closeAllTradeWindows( self, bBack = True ):
		tR = self.aTradeReturn[0]
		self.aTradeReturn = []
		self.tPostJump = None
		CvScreensInterface.tradeRouteScreen.finish(False, -1, True)
		self.unfreezeAllTips()
		if not bBack:
			if CyInterface().isCityScreenUp():
				try:
					CyInterface().clearSelectedCities()
				except:
					pass
		elif tR["map"]:
			if CyInterface().isCityScreenUp():
				try:
					CyInterface().clearSelectedCities()
				except:
					pass
			self.restoreMapView(tR)
		else:
			pCity = gc.getPlayer(gc.getGame().getActivePlayer()).getCity(tR["city"])
			if pCity is not None and not pCity.isNone():
				CyInterface().selectCity(pCity, False)
		try:
			CyInterface().playGeneralSound(self.szModJumpSound)
		except:
			pass

	def restoreAfterReturn( self, tR ):
		try:
			if tR["map"]:
				self.restoreMapView(tR)
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			(tLayout, aszParas, aiIndent, dDetails, tAnchor) = tR["frozen"]
			self.addFrozenWindow(screen, tLayout, aszParas, aiIndent, dDetails, tAnchor)
			self.dTraderWin[self.aFrozen[-1][0]] = tR["yield"]
			gc.getGame().setCursorClient(tR["cursor"][0], tR["cursor"][1])
		except:
			pass

	# what a colony adds to the sum "all colonies, net per turn": its net surplus of the good
	def getCityNetShare( self, pCity, iYield ):
		iNet = pCity.calculateNetYield(iYield)
		if iYield != YieldTypes.YIELD_FOOD:
			# (the planned use of the colony counts fully, also the part that is not used up at the moment because another raw material is missing)
			iNet -= max(0, pCity.getRawYieldConsumed(iYield) - pCity.calculateActualYieldConsumed(iYield))
		return iNet

	# the child tooltip of that line: the explanation and every colony with what it adds; the colonies that neither import nor export the good
	# (they are not in the list of the traders above) are grey with a note
	def getNetHelpText( self, iYield ):
		szText = localText.getText("TXT_KEY_WTP_TIP_TRADERS_NET_ALL_HELP", ())
		try:
			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			aTrade = []
			aOther = []
			(loopCity, iter) = pPlayer.firstCity(False)
			while loopCity:
				iShare = self.getCityNetShare(loopCity, iYield)
				if iShare > 0:
					szShare = u"<color=0,255,0,255>+%d</color>" % iShare
				elif iShare < 0:
					szShare = u"<color=255,0,0,255>%d</color>" % iShare
				else:
					szShare = u"0"
				bTrade = loopCity.isExport(iYield) or loopCity.isImport(iYield)
				tWin = CvScreensInterface.tradeRouteScreen
				if tWin.isOpen() and tWin.iCity == loopCity.getID() and tWin.dData.has_key(iYield):
					bTrade = tWin.dData[iYield]["exp"] or tWin.dData[iYield]["imp"]
				if bTrade:
					szLine = loopCity.getName() + u": " + szShare
					aTrade.append(szLine)
					self.dTraderLines[self.normTipText(szLine)] = loopCity.getID()
				elif iShare != 0:
					szLine = u"<color=170,170,170,255>" + loopCity.getName() + u"</color>: " + szShare + u" <color=170,170,170,255>" + localText.getText("TXT_KEY_WTP_TIP_TRADERS_NET_NOTRADE", ()) + u"</color>"
					aOther.append(szLine)
					# (the lines of the colonies can be clicked as the lines of the traders: the jump to the colony, the window opens with the good)
					self.dTraderLines[self.normTipText(szLine)] = loopCity.getID()
				(loopCity, iter) = pPlayer.nextCity(iter, False)
			aLines = aTrade + aOther
			if len(aLines) > 0:
				szText += u"\n" + u"\n".join(aLines[:20])
		except:
			pass
		return szText

	# the line "all colonies: +N per turn" of the tooltip of a good (import / export window)
	def getTotalNetNote( self, iYield ):
		try:
			pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())
			iNet = 0
			(loopCity, iter) = pPlayer.firstCity(False)
			while loopCity:
				iNet += self.getCityNetShare(loopCity, iYield)
				(loopCity, iter) = pPlayer.nextCity(iter, False)
			if iNet > 0:
				szNet = u"<color=0,255,0,255>+%d</color>" % iNet
			elif iNet < 0:
				szNet = u"<color=255,0,0,255>%d</color>" % iNet
			else:
				szNet = u"0"
			szLine = localText.getText("TXT_KEY_WTP_TIP_TRADERS_NET_ALL", (szNet,)) + u" " + unichr(gc.getYieldInfo(iYield).getChar())
			self.dNetLines[self.normTipText(szLine)] = iYield
			return szLine
		except:
			return u""

	# the picture of a good in the import / export window that has an outer frame (it restricts the production of the city): its help text gets a note
	def addRawNote( self, szText, iYieldOver = -1 ):
		try:
			tWin = CvScreensInterface.tradeRouteScreen
			if tWin.isOpen():
				iYield = iYieldOver
				if iYield < 0:
					iYield = tWin.getIconYieldAt(gc.getGame().getCursorClientX(), gc.getGame().getCursorClientY())
				if iYield >= 0:
					szNote = tWin.getRawNote(iYield)
					if len(szNote) > 0:
						szText = szText + u"\n" + szNote
					# the colonies that export / import the good at the moment
					szTraders = self.getTradersNote(iYield)
					if len(szTraders) > 0:
						szText = szText + u"\n" + szTraders
					# the surplus per turn of all the colonies together (production minus own use), green with a plus sign, red when negative
					szTotal = self.getTotalNetNote(iYield)
					if len(szTotal) > 0:
						szText = szText + u"\n" + szTotal
					self.iTradeTipYield = iYield
					self.szTradeTipText = szText
		except:
			pass
		return szText

	def isTradeWindowOpen( self ):
		try:
			return CvScreensInterface.tradeRouteScreen.isOpen()
		except:
			return False

	def isCursorInTradeWindow( self ):
		try:
			t = CvScreensInterface.tradeRouteScreen
			iX = gc.getGame().getCursorClientX()
			iY = gc.getGame().getCursorClientY()
			tX, tY, tW, tH = t.getScreenRect()
			return t.isOpen() and iX >= tX and iX < tX + tW and iY >= tY and iY < tY + tH
		except:
			return False

	# the cursor is on the picture of a good in the import / export window (its tooltip is ours also in the city screen)
	def isTradeIconHover( self ):
		try:
			tWin = CvScreensInterface.tradeRouteScreen
			return tWin.isOpen() and tWin.getIconYieldAt(gc.getGame().getCursorClientX(), gc.getGame().getCursorClientY()) >= 0
		except:
			return False

	# the help texts the game itself makes for its HUD elements (the DLL stores the last one, CyGame.getWidgetHelp...)
	def pollWidgetHelp( self ):
		try:
			game = gc.getGame()
			iCount = game.getWidgetHelpCount()
			if iCount == self.iWidgetHelpCount:
				return
			self.iWidgetHelpCount = iCount
			self.widgetHelpSeen(game.getWidgetHelpText(), game.getWidgetHelpType())
		except:
			pass

	# time in milliseconds for the tooltip delay. time.time() of the game does not advance (log), time.clock() should; if that one does not
	# advance either, the frames are counted (60 per second assumed)
	def getTipNow( self ):
		try:
			fNow = time.clock() * 1000.0
			if fNow == self.fLastClock:
				self.iClockSame += 1
				if self.iClockSame > 120 and not self.bClockDead:
					self.bClockDead = True
			else:
				self.iClockSame = 0
				self.fLastClock = fNow
			if not self.bClockDead:
				return fNow
		except:
			self.bClockDead = True
		return self.iTick * 16.7

	def updatePendingTip( self ):
		iCursorX = gc.getGame().getCursorClientX()
		iCursorY = gc.getGame().getCursorClientY()
		fNow = self.getTipNow()
		if abs(iCursorX - self.tPendingPos[0]) > 3 or abs(iCursorY - self.tPendingPos[1]) > 3:
			# the cursor moves: the time starts again
			self.tPendingPos = (iCursorX, iCursorY)
			self.fPendingStart = fNow
		elif self.iTipDelay > 0 and fNow - self.fPendingStart >= self.iTipDelay:
			szHelp = self.szPendingHelp
			bWidget = self.bPendingWidget
			self.szPendingHelp = None
			self.showCursorTooltip(CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE), szHelp, bWidget, True)

	def setTipDelay( self, iIndex ):
		self.iTipDelayIndex = max(0, min(len(TIP_DELAYS) - 1, iIndex))
		self.iTipDelay = TIP_DELAYS[self.iTipDelayIndex]
		self.szPendingHelp = None
		self.saveTipSettings()

	def setTipDebug( self, bValue ):
		self.bTipDebug = bool(bValue)
		self.saveTipSettings()

	# test phase: an error in the code of the tooltips is shown as a message (once for the same error) instead of being swallowed
	def tipError( self, szWhere ):
		if not self.bTipDebug:
			return
		try:
			import sys
			tInfo = sys.exc_info()
			iLine = -1
			tb = tInfo[2]
			while tb is not None:
				iLine = tb.tb_lineno
				tb = tb.tb_next
			szMsg = u"Tooltip error in %s (line %d): %s" % (szWhere, iLine, str(tInfo[1]))
			if szMsg != self.szLastTipError:
				self.szLastTipError = szMsg
				self.showModMessage(szMsg)
		except:
			pass

	def setTipAutoFreeze( self, bValue ):
		self.bTipAutoFreeze = bool(bValue)
		if not self.bTipAutoFreeze:
			self.tAutoFreeze = None
		self.saveTipSettings()

	def setTipQuick( self, bQuick ):
		self.bTipQuick = bool(bQuick)
		self.saveTipSettings()

	def saveTipSettings( self ):
		try:
			f = open(TIP_SETTINGS_FILE, "w")
			f.write("mode=%d\n" % self.iTipMode)
			f.write("delay=%d\n" % self.iTipDelayIndex)
			if self.bTipQuick:
				f.write("quick=1\n")
			else:
				f.write("quick=0\n")
			if self.bTipAutoFreeze:
				f.write("autofreeze=1\n")
			else:
				f.write("autofreeze=0\n")
			if self.bTipDebug:
				f.write("debug=1\n")
			else:
				f.write("debug=0\n")
			f.close()
		except:
			pass

	iTipDelayIndex = aiTipSettings[1]
	bTipAutoFreeze = (aiTipSettings[3] == 1) # options screen: the tooltip of an activated unit is frozen until the unit gets an order (default off)
	bTipQuick = (aiTipSettings[2] == 1) # options screen: the next tooltip appears without delay while a tooltip is shown

	# the cursor is on a panel of the HUD that is not part of the map (message panel): the plot under it is not interesting, only the
	# tooltips of the panel itself are wanted. (getattr: the panel belongs to another branch, without it this is always False)
	def isCursorOnOwnPanel( self ):
		try:
			if getattr(self, "tMessagePanelKey", None) is None:
				return False
			tRect = getattr(self, "tMsgPanelRect", None)
			if tRect is None:
				return False
			(iX, iY, iW, iH) = tRect
			iCX = gc.getGame().getCursorClientX()
			iCY = gc.getGame().getCursorClientY()
			return iCX >= iX and iCX < iX + iW and iCY >= iY and iCY < iY + iH
		except:
			return False

	def isCursorInScoreTable( self ):
		if self.tScoreRect is None:
			return True
		(iX, iY, iW, iH) = self.tScoreRect
		iCX = gc.getGame().getCursorClientX()
		iCY = gc.getGame().getCursorClientY()
		return iCX >= iX - 10 and iCX < iX + iW + 10 and iCY >= iY - 10 and iCY < iY + iH + 10

	def hideCursorTooltip( self, screen ):
		self.szPendingHelp = None
		try:
			if self.bCursorTipShown:
				for szName in self.getCursorTipNames():
					screen.hide(szName)
					screen.deleteWidget(szName)
		except:
			pass
		self.bCursorTipShown = False
		self.szCursorTipText = u""

	def updateCursorTooltip( self ):
		# called every frame: the window goes away when the cursor has left its place (the game does not always say that a tooltip is gone)
		# the pictures of the goods of the import / export window in the city screen: the game gives no help text of its own there (the DLL
		# empties it; python cannot clear the help of the city screen). It is on as long as the window is open: a flag that follows the cursor
		# comes too late when the cursor moves fast from one picture to the next (the game tooltip showed up for a moment then)
		try:
			gc.getGame().setHideYieldHelp(self.bHoverTip and CyInterface().isCityScreenUp() and self.isTradeWindowOpen())
		except:
			pass
		self.updateEscHold()
		self.updateAutoFreeze()
		self.updateTradeTipSelect()
		if self.bXHeld and not self.bXHoldDone and self.getTipNow() - self.fXStart >= 600:
			# X held: all frozen windows are closed; with stacked import / export windows (jumps) all of them and back to the start of the first jump
			self.bXHoldDone = True
			if self.isTradeStackOpen():
				self.closeAllTradeWindows()
			else:
				self.unfreezeAllTips()
		if self.bTipFrozen:
			# a frozen window stays until Esc / X, but not into the city screen (except with the import / export window open there)
			if (CyInterface().isCityScreenUp() and not self.isTradeWindowOpen()) or CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL:
				self.unfreezeAllTips()
			else:
				try:
					self.updateFrozenTip()
				except:
					pass
			try:
				if self.getFrozenAt(gc.getGame().getCursorClientX(), gc.getGame().getCursorClientY()) >= 0:
					# the cursor is on a frozen window: no tooltip of the cursor
					if self.bCursorTipShown or self.szPendingHelp is not None:
						self.hideCursorTooltip(CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE))
					return
			except:
				pass
		if self.bHoverTip and not self.bHudHover and self.isCursorOnOwnPanel():
			# the cursor moved onto the message panel with a plot tooltip shown (or waiting): it goes away
			try:
				if self.bCursorTipShown or self.szPendingHelp is not None:
					self.hideCursorTooltip(CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE))
			except:
				pass
			return
		if self.bHoverTip and self.bHudHover and not self.isHudHover():
			# the cursor has left the HUD element: the help of what is under it now (map plot) takes the place of the element help at once
			try:
				screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
				szPlotHelp = CyInterface().getHelpString()
				if len(szPlotHelp) > 0:
					self.showCursorTooltip(screen, szPlotHelp)
				else:
					self.hideCursorTooltip(screen)
			except:
				pass
		if self.szPendingHelp is not None:
			try:
				self.updatePendingTip()
			except:
				self.szPendingHelp = None
		if not self.bCursorTipShown:
			return
		try:
			iDX = abs(gc.getGame().getCursorClientX() - self.tCursorTipAt[0])
			iDY = abs(gc.getGame().getCursorClientY() - self.tCursorTipAt[1])
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
			if iDX > 100 or iDY > 100 or (CyInterface().isCityScreenUp() and not self.isTradeIconHover()):
				self.hideCursorTooltip(screen)
			elif self.iTipMode == 0:
				self.followCursorTip(screen)
		except:
			self.bCursorTipShown = False
	# Will update the help Strings
	def updateHelpStrings( self ):
		self.sendHideGameHelp()
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE_ALL ):
			screen.setHelpTextString("")
			self.hideCursorTooltip(screen)
		else:
			szHelp = CyInterface().getHelpString()
			self.showCursorTooltip(screen, szHelp)
			# while the cursor is on a HUD element the plot help behind it must not replace the help of the element
			if not self.bHoverTip:
				screen.setHelpTextString( szHelp )
			else:
				# the own tooltip is on: the game tooltip stays away
				screen.setHelpTextString( u"" )

		return 0

	# Will set the promotion button position
	def setPromotionButtonPosition( self, szName, iPromotionCount ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
		yResolution = screen.getYResolution()

		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			screen.moveItem( szName, 266 - (24 * (iPromotionCount / 6)), yResolution - 144 + (24 * (iPromotionCount % 6)), -0.3 )

	# Will set the selection button position
	def setScoreTextPosition( self, szButtonID, iWhichLine ):

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
		yResolution = screen.getYResolution()
		if ( CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW ):
			yCoord = yResolution - 180
		else:
			yCoord = yResolution - 88
		screen.moveItem( szButtonID, 996, yCoord - (iWhichLine * 18), -0.3 )

	# Will build the globeview UI
	def updateGlobeviewButtons( self ):
		kInterface = CyInterface()
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		kEngine = CyEngine()
		kGLM = CyGlobeLayerManager()
		iCurrentLayerID = kGLM.getCurrentLayerID()

		# Positioning things based on the visibility of the globe
		#screen.setHelpTextArea( HELPTEXT_AREA_MAX_WIDTH, FontTypes.SMALL_FONT, HELTTEXT_AREA_X_MARGIN, yResolution - (MINI_MAP_RADIUS - 80), -0.1, False, "", True, False, CvUtil.FONT_LEFT_JUSTIFY, HELPTEXT_AREA_MIN_WIDTH)
		# Set base Y position for the LayerOptions, if we find them
		if CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_HIDE:
			iY = yResolution - iGlobeLayerOptionsY_Minimal
		else:
			iY = yResolution - LOWER_RIGHT_CORNER_BACKGROUND_HEIGHT

		# Hide the layer options ... all of them
		for i in range (20):
			szName = "GlobeLayerOption" + str(i)
			screen.hide(szName)

		# Setup the GlobeLayer panel
		if kEngine.isGlobeviewUp() and CyInterface().getShowInterface() != InterfaceVisibility.INTERFACE_HIDE_ALL:
			# set up panel
			if iCurrentLayerID != -1 and kGLM.getLayer(iCurrentLayerID).getNumOptions() != 0:
				bHasOptions = True
			else:
				bHasOptions = False
				screen.hide("ScoreBackground")

			# set up toggle button
			screen.overlayButtonGFC("GlobeToggle", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())

			# Set GlobeLayer indicators correctly
			for i in range(kGLM.getNumLayers()):
				szButtonID = "GlobeLayer" + str(i)
				if (iCurrentLayerID == i):
					screen.overlayButtonGFC(szButtonID, ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
				else:
					screen.overlayButtonGFC(szButtonID, None)

			# Set up options pane
			if bHasOptions:
				kLayer = kGLM.getLayer(iCurrentLayerID)

				iCurY = iY
				iNumOptions = kLayer.getNumOptions()
				iCurOption = kLayer.getCurrentOption()
				iMaxTextWidth = -1
				for iTmp in range(iNumOptions):
					iOption = iTmp
					szName = "GlobeLayerOption" + str(iOption)
					szCaption = kLayer.getOptionName(iOption)
					if(iOption == iCurOption):
						szBuffer = "  <color=0,255,0>%s</color>  " % (szCaption)
					else:
						szBuffer = "  %s  " % (szCaption)
					iTextWidth = CyInterface().determineWidth( szBuffer )

					screen.setText( szName, "Background", szBuffer, CvUtil.FONT_LEFT_JUSTIFY, xResolution - 9 - iTextWidth, iCurY-iGlobeLayerOptionHeight - 10, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GLOBELAYER_OPTION, iOption, -1 )
					screen.show( szName )

					iCurY -= iGlobeLayerOptionHeight

					if iTextWidth > iMaxTextWidth:
						iMaxTextWidth = iTextWidth

				#make extra space
				iCurY -= iGlobeLayerOptionHeight;
				iPanelWidth = iMaxTextWidth + 32
				iPanelHeight = iY - iCurY
				iPanelX = xResolution - 14 - iPanelWidth
				iPanelY = iCurY
#				screen.setPanelSize("ScoreBackground", iPanelX, iPanelY, iPanelWidth, iPanelHeight )
#				screen.show("ScoreBackground")

		else:
			if iCurrentLayerID != -1:
				kLayer = kGLM.getLayer(iCurrentLayerID)
				if kLayer.getName() == "RESOURCES":
					screen.overlayButtonGFC("ResourceIcons", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
				else:
					screen.overlayButtonGFC("ResourceIcons", None)

				if kLayer.getName() == "UNITS":
					screen.overlayButtonGFC("UnitIcons", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
				else:
					screen.overlayButtonGFC("UnitIcons", None)
			else:
				screen.overlayButtonGFC("ResourceIcons", None)
				screen.overlayButtonGFC("UnitIcons", None)

			if CyUserProfile().getGrid():
				screen.overlayButtonGFC("Grid", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
			else:
				screen.overlayButtonGFC("Grid", None)
			if CyUserProfile().getMap():
				screen.overlayButtonGFC("BareMap", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
			else:
				screen.overlayButtonGFC("BareMap", None)
			if CyUserProfile().getYields():
				screen.overlayButtonGFC("Yields", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
			else:
				screen.overlayButtonGFC("Yields", None)
			if CyUserProfile().getScores():
				screen.overlayButtonGFC("ScoresVisible", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
			else:
				screen.overlayButtonGFC("ScoresVisible", None)

			screen.hide("InterfaceGlobeLayerPanel")
			screen.overlayButtonGFC("GlobeToggle", None)

	# Update minimap buttons
	def setMinimapButtonVisibility( self, bVisible ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
		kInterface = CyInterface()
		kGLM = CyGlobeLayerManager()
		xResolution = screen.getXResolution()
		yResolution = screen.getYResolution()

		if (CyInterface().isCityScreenUp() or (CyInterface().getHeadSelectedCity() != None and not CyEngine().isGlobeviewUp())):
			bVisible = False

		kMainButtons = ["UnitIcons", "Grid", "BareMap", "Yields", "ScoresVisible", "ResourceIcons"]
		kGlobeButtons = []
		for i in range(kGLM.getNumLayers()):
			szButtonID = "GlobeLayer" + str(i)
			kGlobeButtons.append(szButtonID)

		if bVisible:
			if CyEngine().isGlobeviewUp():
				kHide = kMainButtons
				kShow = kGlobeButtons
			else:
				kHide = kGlobeButtons
				kShow = kMainButtons
			screen.show("GlobeToggle")

		else:
			kHide = kMainButtons + kGlobeButtons
			kShow = []
			screen.hide("GlobeToggle")

		for szButton in kHide:
			screen.hide(szButton)

		if len(kShow) > 0:
			for szButton in kShow:
				screen.show(szButton)

	def toggleTerritorialInfluence(self):

		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )

		self.bTerritorialInfluenceMode = not self.bTerritorialInfluenceMode

		if self.bTerritorialInfluenceMode:
			self.bTerritorialInfluenceOldNoUnitCycling = CyUserProfile().getPlayerOption(PlayerOptionTypes.PLAYEROPTION_NO_UNIT_CYCLING)

			if not self.bTerritorialInfluenceOldNoUnitCycling:
				CyMessageControl().sendPlayerOption(PlayerOptionTypes.PLAYEROPTION_NO_UNIT_CYCLING, True)

			screen.overlayButtonGFC("TerritorialInfluenceButton", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
			self.refreshTerritorialInfluence()
		else:
			if not self.bTerritorialInfluenceOldNoUnitCycling:
				CyMessageControl().sendPlayerOption(PlayerOptionTypes.PLAYEROPTION_NO_UNIT_CYCLING, False)

			screen.overlayButtonGFC("TerritorialInfluenceButton", None)
			CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
			CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)

	# Will handle the input for this screen...
	def handleInput ( self, inputClass ):

		global BUILDING_MANAGMENT_PANEL_UP
		global AUTOMATION_MANAGMENT_PANEL_UP
		global MAP_MANAGMENT_PANEL_UP
		global SHOW_ALL_YIELDS
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):

			# WTP: right click on the picture of a good of the import / export window with a line of its tooltip chosen (Shift + wheel): it is run
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_HELP_YIELD and (inputClass.getFlags() & MouseFlags.MOUSE_RBUTTONUP)):
				if self.runTradeTipSelection():
					return 1
			# WTP: left click on the picture of a good of the import / export window: the tooltip of the good is frozen / released
			if (inputClass.getButtonType() == WidgetTypes.WIDGET_HELP_YIELD and (inputClass.getFlags() & MouseFlags.MOUSE_LBUTTONUP)):
				if self.toggleTradeTipFreeze():
					return 1

			if (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == BUILDING_MANAGMENT_TOGGLE):
				BUILDING_MANAGMENT_PANEL_UP = True
				AUTOMATION_MANAGMENT_PANEL_UP, MAP_MANAGMENT_PANEL_UP = False, False
				self.updateSelectionButtons()

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == AUTOMATION_MANAGMENT_TOGGLE):
				AUTOMATION_MANAGMENT_PANEL_UP = True
				BUILDING_MANAGMENT_PANEL_UP, MAP_MANAGMENT_PANEL_UP = False, False
				self.updateSelectionButtons()

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == MAP_MANAGMENT_TOGGLE):
				MAP_MANAGMENT_PANEL_UP = True
				AUTOMATION_MANAGMENT_PANEL_UP, BUILDING_MANAGMENT_PANEL_UP = False, False
				self.updateSelectionButtons()

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and (inputClass.getData1() == WTP_CYCLE_PREV or inputClass.getData1() == WTP_CYCLE_NEXT)):
				if inputClass.getData1() == WTP_CYCLE_PREV:
					self.cycleAutomated(-1, inputClass.getData2())
				else:
					self.cycleAutomated(1, inputClass.getData2())

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_CLOSE_SCREEN):
				CyInterface().clearSelectedCities()

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_HELP_SHOW_OR_HIDE_YIELDS):
				if SHOW_ALL_YIELDS == True:
					SHOW_ALL_YIELDS = False
					screen.overlayButtonGFC("ShowOrHideYields", ArtFileMgr.getInterfaceArtInfo("INTERFACE_HIGHLIGHTED_BUTTON").getPath())
				else:
					SHOW_ALL_YIELDS = True
 					screen.overlayButtonGFC("ShowOrHideYields", None)
				self.updateResourceTable()

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == ACHIEVE_ADVISOR_SCREEN_MI):
				CvScreensInterface.showAchieveAdvisorScreen()

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == self.BUTTON_TERRITORIAL_INFLUENCE):
				self.toggleTerritorialInfluence()

			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == self.BUTTON_TRADE_ROUTE_MANAGER):
				self.openTradeRouteManager()


			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == self.BUTTON_AUTO_ASSIGN_TARGET):
				self.toggleAutoAssignTarget()
		return 0

	# WTP: the HUD button of the Trade Route Manager (the same as the hotkey Shift+Alt+T, see CvEventManager)
	def openTradeRouteManager(self):
		try:
			import CvTransportRoutesOverview
			CvTransportRoutesOverview.g_FromHotkey = True
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
			popupInfo.setText(u"showTransportRoutesOverview")
			popupInfo.addPopup(gc.getGame().getActivePlayer())
		except:
			pass
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == self.BUTTON_TIP_LINE):
				if (inputClass.getFlags() & MouseFlags.MOUSE_RBUTTONUP):
					# the line of a colony in the tooltip of a good of the import / export window: the jump (left and right click)
					if self.tryTraderJump(inputClass.getData2() / 1000, inputClass.getData2() % 1000):
						return 1
					# a line of the frozen hover tooltip: right click: Colopedia page of the first named thing of the line (Ctrl: the second)
					self.openTipPedia(inputClass.getData2(), inputClass.isCtrlKeyDown(), inputClass.isShiftKeyDown())
				elif (inputClass.getFlags() & MouseFlags.MOUSE_LBUTTONUP):
					# left click on a line with a child window: the child window is frozen (as with X); on the same line again: it goes again
					self.onTipLineLeftClick(inputClass.getData2())
			# WTP: message panel of the turn: a click expands or collapses it
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == self.BUTTON_MESSAGE_PANEL):
				self.bMessagePanelExpanded = not self.bMessagePanelExpanded
				self.bMessagePanelPrevious = False
				self.iMessagePage = 0
				self.updateMessagePanel()
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == self.BUTTON_MESSAGE_AUTO):
				self.setMessageAutoExpand(not self.getMessageAutoExpand())
				self.updateMessagePanel()
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == self.BUTTON_MESSAGE_MORE):
				if self.bMsgWpView:
					self.iMsgWpPage += 1 # (the list starts again with the first page after the last one)
				else:
					self.iMessagePage += 1 # (the panel starts again with the newest messages after the last page)
				self.updateMessagePanel()
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == self.BUTTON_MESSAGE_WPS):
				# (the toggle: the first click lists the waypoints of the land units, the second one those of the ships, the third one switches off)
				if not self.bMsgWpView:
					self.bMsgWpView = True
					self.bMsgWpSea = False
				elif not self.bMsgWpSea:
					self.bMsgWpSea = True
				else:
					self.bMsgWpView = False
					self.bMsgWpSea = False
				self.iMsgWpPage = 0
				# (the list starts collapsed; it goes back to the standard view when something else is selected, see updateMessageScroll)
				self.bMessagePanelExpanded = False
				self.bMessagePanelPrevious = False
				self.iMessagePage = 0
				self.tMsgWpSel = self.getMsgSelectionKey()
				self.tMessagePanelKey = None
				self.updateMessagePanel()
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == self.BUTTON_MESSAGE_PREVIOUS):
				self.bMessagePanelPrevious = not self.bMessagePanelPrevious
				self.iMessagePage = 0
				self.updateMessagePanel()
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == self.BUTTON_MESSAGE_LINE):
				if (inputClass.getFlags() & MouseFlags.MOUSE_RBUTTONUP):
					# right click: Colopedia page of the first named thing of the message, Ctrl + right click: of the second one
					iContact = self.getMessageContact(inputClass.getData2())
					if iContact >= 0 and not inputClass.isCtrlKeyDown():
						# a message that names a native tribe: right click talks to the nation (Ctrl: the first Colopedia page)
						self.contactMessageNation(iContact)
					else:
						self.openMessagePedia(inputClass.getData2(), inputClass.isCtrlKeyDown() and iContact < 0)
				else:
					self.clickMessageLine(inputClass.getData2())
			elif (inputClass.getButtonType() == WidgetTypes.WIDGET_GENERAL and inputClass.getData1() == self.BUTTON_MESSAGE_WP):
				self.clickMsgWaypoint(inputClass.getData2(), bool(inputClass.getFlags() & MouseFlags.MOUSE_RBUTTONUP), inputClass.isShiftKeyDown())
		return 0

	# WTP: the message panel. The game's own message area (top center) shows the messages of a turn only for a few seconds and ignores the
	# mouse. The DLL keeps the messages of the turn (CyGame.getNumHudMessages, MESSAGE_PANEL_ENABLED in GlobalDefinesAlt.xml) and this panel
	# shows them as long as the turn lasts: the newest ones when collapsed, all of them after a click on the header (it grows downwards).
	# Every line of a message is a clickable label (the game does not pass clicks on a multiline text): a click centers the map on the place
	# of the message (colony, battle, unit ...) or on the named colony / native settlement. A message that names a native tribe or its chief
	# and has no place of its own also opens the diplomacy with the tribe (and centers its main settlement).
	# widths of the letters of a proportional font in thousandths of an em (a wide W or M and a narrow i or l differ by a factor of 4; with the
	# same number of characters a line of wide letters would be much wider than the panel). 450 = the average of a line of English text.
	dMessageCharWidths = {}
	for szWidthChar, iWidthChar in zip(u"abcdefghijklmnopqrstuvwxyz", (556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500)):
		dMessageCharWidths[szWidthChar] = iWidthChar
	for szWidthChar in u"ABCDEFGHKLNOPQRSTUVXYZ":
		dMessageCharWidths[szWidthChar] = 667
	for szWidthChar, iWidthChar in ((u"M", 833), (u"W", 944), (u"I", 278), (u"J", 500), (u" ", 278), (u".", 278), (u",", 278), (u":", 278), (u";", 278), (u"!", 278), (u"'", 191), (u"-", 333), (u"(", 333), (u")", 333)):
		dMessageCharWidths[szWidthChar] = iWidthChar

	# WTP: line distance of the panels and tooltips. The font of these texts (<font=STANDARD_FONT_SIZE-1>) depends on the resolution class and
	# not on the screen height: the same font at 1080 and at 1440 (22 pixels line distance, measured), a smaller one in the lowest class.
	# So the distance is 22 pixels scaled by the width the game itself measures for the font in use against the font of the 1440 layout.
	dTipLineCache = {}
	iTipFontSize = None

	# WTP: the font of our own panels and tooltips: one step smaller than the standard font of the resolution class, and one more below
	# 1300 pixels of screen height (1080p), where the standard font is large for a screen of that size
	def getTipFontSize( self ):
		if self.iTipFontSize is None:
			iSize = STANDARD_FONT_SIZE - 1
			try:
				if CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE).getYResolution() < 1300 and iSize >= 3:
					iSize -= 1
			except:
				return iSize
			self.iTipFontSize = iSize
		return self.iTipFontSize

	def getTipLineDistance( self, yRes ):
		kKey = (self.getTipFontSize(), yRes)
		if self.dTipLineCache.has_key(kKey):
			return self.dTipLineCache[kKey]
		iLine = 22
		if self.getTipFontSize() == 3:
			self.dTipLineCache[kKey] = iLine
			return iLine
		try:
			szRef = u"The quick brown fox jumps over the lazy dog, 0123456789 and so on"
			iNow = CyInterface().determineWidth(self.setFontSize(szRef, -1))
			iBase = CyInterface().determineWidth(u"<font=3>" + szRef + u"</font>")
			if iNow > 0 and iBase > 0:
				fScale = max(0.6, min(1.0, float(iNow) / iBase))
				iLine = max(14, int(22 * fScale + 0.5))
				self.dTipLineCache[kKey] = iLine
			else:
				iLine = 19
		except:
			iLine = 19
		return iLine

	# maximal width of a tooltip window: a share of the screen width, but at least as many characters as at 1440 (the font does not get smaller
	# with the screen: at 1080 a window of 20 percent would hold far fewer characters per line), and never more than a larger share of the screen
	def getTipMaxWidth( self, xRes, iChar, bWidget ):
		if bWidget:
			return max(300, int(xRes * 0.14), min(int(xRes * 0.2), int(50 * iChar)))
		return max(300, int(xRes * 0.2), min(int(xRes * 0.28), int(72 * iChar)))

	def getMessageWidth(self, szText):
		# width in characters of an average letter: the symbols of the game font (icons) are wider than letters
		iWidth = 0
		# the help texts contain &lt; &gt; &amp; for the signs that are shown (&lt;F1&gt; is 4 characters wide)
		szText = szText.replace(u"&lt;", u"<").replace(u"&gt;", u">").replace(u"&amp;", u"&")
		for szChar in szText:
			if ord(szChar) >= 0x2000:
				iWidth += 3.4
			else:
				iWidth += self.dMessageCharWidths.get(szChar, 556) / 450.0
		return iWidth

	def wrapMessage(self, szMessage, iCharsPerLine, bIconIndent = False):
		# splits a message with color markup into lines of about iCharsPerLine visible characters; the colors that are open at the end of
		# a line are closed there and opened again at the start of the next line.
		# bIconIndent (hover tooltip): a row of icons (promotions) that does not fit is continued in the next line, under the first icon;
		# the indent of every line (in characters) is in self.aiWrapIndent afterwards
		aszLines = []
		aiIndent = []
		aszOpen = []
		szLine = u""
		iVisible = 0
		iLineIndent = 0
		bImgRun = False
		iImgIndent = 0
		aszTokens = re.split(u"(<[^>]*>)", szMessage)
		for iToken in range(len(aszTokens)):
			szToken = aszTokens[iToken]
			if not szToken:
				continue
			if szToken[0] == u"<" and szToken[-1] == u">":
				szLower = szToken.lower()
				if szLower.startswith(u"<img="):
					# a picture (the promotions of a unit): about as wide as an icon of the game font. A row of them that does not fit into the
					# rest of the line goes into the next line as a whole (a row longer than a line is broken there)
					if not bImgRun:
						bImgRun = True
						iImgIndent = 0
						if bIconIndent:
							fRun = 0
							for szNext in aszTokens[iToken:]:
								if szNext.lower().startswith(u"<img="):
									fRun += self.fImgWidth
								elif szNext and szNext.lower() != u"</img>" and szNext.strip():
									break
							# the promotions of a unit always go into a line of their own (not behind a number: that is a counted group)
							szBefore = re.sub(u"<[^>]*>", u"", szLine).rstrip()
							bOwnLine = (len(szBefore) > 0 and not szBefore[-1:].isdigit())
							if iVisible > iLineIndent and (bOwnLine or iVisible + fRun > iCharsPerLine):
								aszLines.append(szLine + u"</color>" * len(aszOpen))
								aiIndent.append(iLineIndent)
								szLine = u"".join(aszOpen)
								iVisible = 0
								iLineIndent = 0
					if iVisible > iLineIndent and iVisible + self.fImgWidth > iCharsPerLine:
						aszLines.append(szLine + u"</color>" * len(aszOpen))
						aiIndent.append(iLineIndent)
						szLine = u"".join(aszOpen)
						iVisible = iImgIndent
						iLineIndent = iImgIndent
					szLine += szToken
					iVisible += self.fImgWidth
					continue
				if szLower.startswith(u"<color"):
					aszOpen.append(szToken)
				elif szLower == u"</color>":
					if aszOpen:
						aszOpen.pop()
				szLine += szToken
				continue
			if szToken.strip():
				bImgRun = False
			szLead = szToken[:len(szToken) - len(szToken.lstrip())]
			szLine += szLead
			iVisible += len(szLead)
			aszWords = []
			for szWord in re.findall(u"\\S+\\s*", szToken, re.UNICODE):
				if bIconIndent:
					# a row of icons at the end of a word (\"(26/37)\" + promotions) is a word of its own
					aszWords += self.splitIconRow(szWord)
				else:
					aszWords.append(szWord)
			for szWord in aszWords:
				szCore = szWord.rstrip()
				iWord = self.getMessageWidth(szCore)
				if bIconIndent and len(szCore) > 1 and self.isIconRow(szCore):
					# the row of icons starts where it is and goes on under its first icon
					iIndent = iVisible
					if iIndent + 4 * 3.4 > iCharsPerLine:
						iIndent = 0
					bHas = iVisible > 0
					for szChar in szCore:
						iChar = self.getMessageWidth(szChar)
						if bHas and iVisible + iChar > iCharsPerLine:
							aszLines.append(szLine + u"</color>" * len(aszOpen))
							aiIndent.append(iLineIndent)
							szLine = u"".join(aszOpen)
							iVisible = iIndent
							iLineIndent = iIndent
							bHas = False
						szLine += szChar
						iVisible += iChar
						bHas = True
					szLine += szWord[len(szCore):]
					iVisible += len(szWord) - len(szCore)
					continue
				if iVisible > 0 and iVisible + iWord > iCharsPerLine:
					aszLines.append(szLine + u"</color>" * len(aszOpen))
					aiIndent.append(iLineIndent)
					szLine = u"".join(aszOpen)
					iVisible = 0
					iLineIndent = 0
				if iWord > iCharsPerLine:
					# a word without blanks that is longer than a line (e.g. a row of icons): broken between the characters
					for szChar in szWord:
						iChar = self.getMessageWidth(szChar)
						if iVisible > 0 and iVisible + iChar > iCharsPerLine:
							aszLines.append(szLine + u"</color>" * len(aszOpen))
							aiIndent.append(iLineIndent)
							szLine = u"".join(aszOpen)
							iVisible = 0
							iLineIndent = 0
						szLine += szChar
						iVisible += iChar
					continue
				szLine += szWord
				iVisible += self.getMessageWidth(szWord)
		aszLines.append(szLine)
		aiIndent.append(iLineIndent)
		self.aiWrapIndent = aiIndent
		return aszLines

	def getMessageTargets(self, aszMessages, aiX, aiY):
		# for every message: (x, y, ePlayer) - the plot to center (x < 0: none) and the native player to contact (-1: none)
		atTargets = []
		pMap = gc.getMap()
		iTeam = gc.getGame().getActiveTeam()
		aNatives = [] # (name, ePlayer, x, y)
		aCities = [] # (name, x, y)
		for ePlayer in range(gc.getMAX_PLAYERS()):
			pPlayer = gc.getPlayer(ePlayer)
			if not pPlayer.isAlive():
				continue
			pCapital = None
			for iCity in range(pPlayer.getNumCities()):
				pCity = pPlayer.getCity(iCity)
				if pCity is None or pCity.isNone() or not pCity.isRevealed(iTeam, False):
					continue
				if pCapital is None:
					pCapital = pCity
				aCities.append((pCity.getName(), pCity.getX(), pCity.getY()))
			if pPlayer.isNative():
				# (a tribe whose village is not known yet is in the list too: its messages (raids) still offer the talk, only the place is missing)
				iCapX = -1
				iCapY = -1
				if pCapital is not None:
					try:
						pBest = pPlayer.getCapitalCity()
						if pBest is not None and not pBest.isNone() and pBest.isRevealed(iTeam, False):
							pCapital = pBest
					except:
						pass
					iCapX = pCapital.getX()
					iCapY = pCapital.getY()
				for szName in (pPlayer.getName(), pPlayer.getCivilizationShortDescription(0), pPlayer.getCivilizationAdjective(0)):
					if szName and len(szName) >= 3:
						aNatives.append((szName, ePlayer, iCapX, iCapY))
		aCities.sort(key = lambda t: -len(t[0]))

		for i in range(len(aszMessages)):
			szPlain = re.sub(u"<[^>]*>", u"", aszMessages[i])
			iX = aiX[i]
			iY = aiY[i]
			if iX >= 0 and iY >= 0 and iX < pMap.getGridWidth() and iY < pMap.getGridHeight() and not pMap.plot(iX, iY).isNone():
				ePlace = -1
				# (also an attack that was fought off: "fought off an enemy Ngabe Warrior") every message about a raid (raid, raiding party, Überfall ...) also offers the contact to the tribe that raids
				if re.search(u"raid|\u00fcberfall|incursi|fought off|repelled|abgewehrt|zur\u00fcckgeschlagen|victory|sieg \u00fcber|gefecht gewonnen", szPlain, re.IGNORECASE | re.UNICODE):
					for (szName, ePlayer, iPX, iPY) in aNatives:
						if szName in szPlain:
							ePlace = ePlayer
							break
				atTargets.append((iX, iY, ePlace))
				continue
			tTarget = None
			# (a message of the mod with its place, e.g. a waypoint)
			tModPlot = getattr(self, "dModMessagePlot", {}).get(szPlain.strip())
			if tModPlot is not None:
				atTargets.append((tModPlot[0], tModPlot[1], -1))
				continue
			for (szName, ePlayer, iPX, iPY) in aNatives:
				if szName in szPlain:
					tTarget = (iPX, iPY, ePlayer)
					break
			if tTarget is None:
				for (szName, iPX, iPY) in aCities:
					if szName and szName in szPlain:
						tTarget = (iPX, iPY, -1)
						break
			if tTarget is None:
				tTarget = (-1, -1, -1)
			atTargets.append(tTarget)
		return atTargets

	# the auto expand option of the message panel, kept in the script data of the player: [[WTPMSG:0]] / [[WTPMSG:1]] (on when nothing is saved)
	def getMessageAutoExpand(self):
		if self.bMessageAutoExpand is None:
			self.bMessageAutoExpand = True
			try:
				szData = gc.getActivePlayer().getScriptData()
				if szData is not None and szData.find("[[WTPMSG:0]]") != -1:
					self.bMessageAutoExpand = False
			except:
				pass
		return self.bMessageAutoExpand

	def setMessageAutoExpand(self, bAuto):
		self.bMessageAutoExpand = bAuto
		try:
			pPlayer = gc.getActivePlayer()
			szData = pPlayer.getScriptData()
			if szData is None:
				szData = ""
			szData = szData.replace("[[WTPMSG:0]]", "").replace("[[WTPMSG:1]]", "")
			szData = szData + "[[WTPMSG:" + str(int(bAuto)) + "]]"
			pPlayer.setScriptData(szData)
		except:
			pass

	# the option "New message panel" of the game options (PLAYEROPTION_MODDER_1, default off, kept in the profile of the player)
	def isMessagePanelOption(self):
		try:
			return gc.getActivePlayer().isOption(PlayerOptionTypes.PLAYEROPTION_MODDER_1)
		except:
			return False

	# the position of the panel, kept in the script data of the player: [[WTPMSGPOS:x:y]] (offset from the default place)
	def readMessagePosition(self):
		if self.bMessagePosRead:
			return
		self.bMessagePosRead = True
		try:
			szData = gc.getActivePlayer().getScriptData()
			if szData is not None:
				iStart = szData.find("[[WTPMSGPOS:")
				if iStart != -1:
					iEnd = szData.find("]]", iStart)
					aszPos = szData[iStart + 12:iEnd].split(":")
					self.iMsgMoveX = int(aszPos[0])
					self.iMsgMoveY = int(aszPos[1])
		except:
			pass

	def saveMessagePosition(self):
		try:
			pPlayer = gc.getActivePlayer()
			szData = pPlayer.getScriptData()
			if szData is None:
				szData = ""
			iStart = szData.find("[[WTPMSGPOS:")
			if iStart != -1:
				iEnd = szData.find("]]", iStart)
				szData = szData[:iStart] + szData[iEnd + 2:]
			if self.iMsgMoveX != 0 or self.iMsgMoveY != 0:
				szData = szData + "[[WTPMSGPOS:" + str(self.iMsgMoveX) + ":" + str(self.iMsgMoveY) + "]]"
			pPlayer.setScriptData(szData)
		except:
			pass

	# the message panel is moved with Ctrl + Shift + W A S D (two keys at once: diagonal)
	def isMessagePanelShown(self):
		return self.tMessagePanelKey is not None

	# Ctrl + Shift + Q: back to the default place
	def resetMessagePanel(self):
		self.iMsgMoveX = 0
		self.iMsgMoveY = 0
		self.saveMessagePosition()
		self.updateMessagePanel()

	def pressMessageArrow(self, iDir):
		if iDir in self.aMsgHeld:
			return
		if len(self.aMsgHeld) == 0 and self.iMsgCamKeep <= 0:
			try:
				self.fMsgCamTurn = CyCamera().GetBaseTurn()
				self.fMsgCamPitch = CyCamera().GetBasePitch()
			except:
				pass
		self.iMsgCamKeep = 40
		self.aMsgHeld.append(iDir)
		self.iMsgHoldWait = 18
		self.moveMessagePanel([iDir])

	def releaseMessageArrow(self, iDir):
		if iDir in self.aMsgHeld:
			self.aMsgHeld.remove(iDir)
			self.iMsgCamKeep = 40
			if len(self.aMsgHeld) == 0:
				self.saveMessagePosition()

	def moveMessagePanel(self, aDirs):
		for iDir in aDirs:
			self.iMsgMoveX += [-40, 40, 0, 0][iDir]
			self.iMsgMoveY += [0, 0, -40, 40][iDir]
		self.updateMessagePanel()

	def updateMessageMove(self):
		# the camera stays where it was while the panel is moved (and a moment after, the game turns it back by itself)
		if self.iMsgCamKeep > 0:
			try:
				CyCamera().SetBaseTurn(self.fMsgCamTurn)
				CyCamera().SetBasePitch(self.fMsgCamPitch)
			except:
				pass
			if len(self.aMsgHeld) == 0:
				self.iMsgCamKeep -= 1
		if len(self.aMsgHeld) == 0:
			return
		try:
			bShift = CyInterface().shiftKey() and CyInterface().ctrlKey()
		except:
			bShift = True
		if not bShift:
			self.aMsgHeld = []
			self.saveMessagePosition()
			return
		self.iMsgHoldWait -= 1
		if self.iMsgHoldWait <= 0:
			self.iMsgHoldWait = 3
			self.moveMessagePanel(list(self.aMsgHeld))

	def hideMessagePanel(self, screen):
		for szName in self.aszMessageLines:
			screen.hide(szName)
		self.aszMessageLines = []
		screen.deleteWidget("HudMsgPanel")
		screen.deleteWidget("HudMsgPanelBack1")
		screen.deleteWidget("HudMsgPanelBack2")
		screen.hide("HudMsgHeader")
		screen.hide("HudMsgAuto")
		screen.hide("HudMsgWps")
		screen.hide("HudMsgFooterMore")
		screen.hide("HudMsgFooterPrevious")

	def updateMessagePanel(self):

		try:
			screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
			game = gc.getGame()
			iNumCurrent = game.getNumHudMessages()
			iNumPrevious = game.getNumHudMessagesPrevious()
			# a new turn: the panel opens expanded with its first messages (when the option is on)
			if game.getGameTurn() != self.iMessageTurn:
				self.iMessageTurn = game.getGameTurn()
				self.bMessageTurnPending = True
			if self.bMessageTurnPending and iNumCurrent > 0:
				self.bMessageTurnPending = False
				self.bMessagePanelExpanded = self.getMessageAutoExpand()
				self.bMessagePanelPrevious = False
				self.iMessagePage = 0
			bPrevious = self.bMessagePanelPrevious and self.bMessagePanelExpanded
			if bPrevious:
				iNum = iNumPrevious
			else:
				iNum = iNumCurrent
			# (MESSAGE_PANEL_ENABLED = 0: the DLL collects no messages, so there is nothing to show)
			bShow = ((iNumCurrent > 0 or self.bMsgWpView) and self.isMessagePanelOption()
				and CyInterface().getShowInterface() == InterfaceVisibility.INTERFACE_SHOW and not CyInterface().isCityScreenUp())
			if iNumCurrent == 0:
				self.bMessageTurnPending = True
				self.bMessagePanelExpanded = False
				self.bMessagePanelPrevious = False
				self.iMessagePage = 0

			if not bShow:
				if self.tMessagePanelKey is not None:
					self.tMessagePanelKey = None
					self.hideMessagePanel(screen)
				return

			xRes = screen.getXResolution()
			yRes = screen.getYResolution()
			if bPrevious:
				iNumPriority = game.getNumHudPriorityPrevious()
			else:
				iNumPriority = game.getNumHudPriority()
			self.readMessagePosition()
			aWpEntries = []
			tWpKey = None
			if self.bMsgWpView:
				aWpEntries = self.getMsgWaypointEntries()
				tWpKey = (self.iMsgWpPage, tuple([t[5] for t in aWpEntries]))
			tKey = (iNumCurrent, iNumPrevious, iNumPriority, bPrevious, self.iMessagePage, self.bMessagePanelExpanded, self.getMessageAutoExpand(), self.iMsgMoveX, self.iMsgMoveY, xRes, yRes, self.bMsgWpView, self.bMsgWpSea, tWpKey)
			if tKey == self.tMessagePanelKey:
				return
			self.tMessagePanelKey = tKey

			# geometry: centered below the top HUD, about as wide as the game's own message area
			iLine = self.getTipLineDistance(yRes) # distance of the text lines (measured: 22 pixels at 1440, the font follows the resolution class)
			iPad = max(6, iLine / 2)
			iWidth = max(380, int(xRes * 0.23))
			# the font does not shrink with the screen: at least the number of characters per line of the 1440 layout (84), at most a third of the screen
			iWidth = max(iWidth, min(int(xRes * 0.34), int(84 * iLine * 0.32)))
			iX = (xRes - iWidth) / 2
			# just below the round buttons of the top HUD (their size depends on the resolution class, not on the screen height: 83 pixels with 36)
			iY = max(int(yRes * 0.058), int(83 * SMALL_BUTTON_SIZE / 36.0))
			# moved by the player (stays on the screen)
			iBaseX = iX
			iBaseY = iY
			iX = max(0, min(xRes - iWidth, iX + self.iMsgMoveX))
			iY = max(0, min(yRes - 120, iY + self.iMsgMoveY))
			self.iMsgMoveX = iX - iBaseX
			self.iMsgMoveY = iY - iBaseY
			self.iMsgX = iX
			self.iMsgY = iY
			iHeaderHeight = int(iLine * 0.73)
			iGap = int(iLine * 0.8) # a blank line between the header and the messages
			iIndent = int(iLine * 0.95) # the lines after the first one of a message
			# characters per line (measured: about 6.6 pixels per character at 22 pixels line distance)
			iCharsPerLine = max(20, int((iWidth - 2 * iPad - iIndent) / (iLine * 0.32)))

			if self.bMsgWpView:
				self.drawMsgWaypointView(screen, aWpEntries, iX, iY, iWidth, iLine, iPad, iHeaderHeight, iGap, yRes)
				return

			aszMessages = []
			aiX = []
			aiY = []
			for i in range(iNum):
				if bPrevious:
					aszMessages.append(game.getHudMessagePreviousText(i))
					aiX.append(game.getHudMessagePreviousX(i))
					aiY.append(game.getHudMessagePreviousY(i))
				else:
					aszMessages.append(game.getHudMessageText(i))
					aiX.append(game.getHudMessageX(i))
					aiY.append(game.getHudMessageY(i))
			aatLines = [self.wrapMessage(szMessage, iCharsPerLine) for szMessage in aszMessages]
			atTargets = self.getMessageTargets(aszMessages, aiX, aiY)
			self.aszMessageTexts = aszMessages
			self.atMessageTargets = atTargets

			# which messages: collapsed the newest ones that fit; expanded pages of the full height of the panel, the newest page
			# first, a click on the footer shows the next older page (and after the last one the newest again)
			# the expanded panel ends at 80 percent of the screen height in its default place, moved down it may reach the bottom edge
			iBottomLimit = int(yRes * 0.80)
			if self.iMsgMoveY != 0:
				iBottomLimit = yRes - 10
			bFooterPrevious = self.bMessagePanelExpanded and (iNumPrevious > 0 or bPrevious)
			if self.bMessagePanelExpanded:
				iFooterLines = 1 # the footer of the previous turn
				iMaxLines = max(6, (iBottomLimit - iY - iHeaderHeight - iGap - 2 * iPad) / iLine - 2 * iFooterLines)
			else:
				iFooterLines = 0
				iMaxLines = 7 # collapsed: three priority messages of two lines each (3 * 2.2 lines)
				if yRes >= 1000:
					iMaxLines = 9 # 1080p and 1440p: eight lines of text (the extra space after each message counts as well), was 7 = six lines
			# the priority messages (the first iNumPriority ones) are always at the top of the newest page; on the other pages the others
			iNumPriority = min(iNumPriority, iNum)
			fMessageGap = 0.2 # extra space after every message (in lines), better to read
			aiPriority = []
			iPriorityLines = 0
			for i in range(iNumPriority):
				if len(aiPriority) > 0 and iPriorityLines + len(aatLines[i]) + fMessageGap > max(2, iMaxLines - 2 * int(self.bMessagePanelExpanded)):
					break
				aiPriority.append(i)
				iPriorityLines += len(aatLines[i]) + fMessageGap
			aPages = []
			iEnd = iNum
			while iEnd > iNumPriority:
				if len(aPages) == 0:
					iLimit = max(1, iMaxLines - iPriorityLines)
				else:
					iLimit = iMaxLines
				iFirst = iEnd
				iSum = 0
				while iFirst > iNumPriority and (iSum + len(aatLines[iFirst - 1]) + fMessageGap <= iLimit or (iFirst == iEnd and (self.bMessagePanelExpanded or iPriorityLines == 0))):
					iFirst -= 1
					iSum += len(aatLines[iFirst]) + fMessageGap
				aPages.append((iFirst, iEnd, iSum))
				iEnd = iFirst
				if not self.bMessagePanelExpanded:
					break
			if len(aPages) == 0:
				aPages.append((iNumPriority, iNumPriority, 0))
			bMore = (len(aPages) > 1)
			if self.iMessagePage >= len(aPages):
				self.iMessagePage = 0
			iFirst, iLast, iSum = aPages[self.iMessagePage]
			if self.iMessagePage == 0:
				aiShow = aiPriority + range(iFirst, iLast)
				iTextLines = iSum + iPriorityLines
			else:
				aiShow = range(iFirst, iLast)
				iTextLines = iSum
			iFooterHeight = 0
			if bMore:
				iFooterHeight += iLine
			if bFooterPrevious:
				iFooterHeight += iLine
			if iFooterHeight > 0:
				iFooterHeight += iGap / 2
			iTextHeight = int(iTextLines * iLine) + iPad / 2
			iHeight = iHeaderHeight + iGap + iTextHeight + iFooterHeight + iPad

			if self.bMessagePanelExpanded:
				if bPrevious:
					szHeader = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_PREVIOUS_HEADER", (iNum,))
				else:
					szHeader = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_COLLAPSE", (iNum,))
			else:
				szHeader = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_EXPAND", (iNum,))

			# the old labels are hidden, the ones that are needed again are shown by setText
			for szName in self.aszMessageLines:
				screen.hide(szName)
			self.aszMessageLines = []
			self.dMessageCapitals = {}
			self.dMessageLineIndex = {}
			self.dMessageRects = {}
			self.aMsgWpRects = []
			self.tMsgPanelRect = (iX, iY, iWidth, iHeight)

			# a denser background: the panel style is semi-transparent, several of them on top of each other are better to read
			# (two when collapsed, three when expanded)
			screen.deleteWidget("HudMsgPanel")
			screen.deleteWidget("HudMsgPanelBack1")
			screen.deleteWidget("HudMsgPanelBack2")
			screen.addPanel("HudMsgPanelBack1", u"", u"", True, False, iX, iY, iWidth, iHeight, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.show("HudMsgPanelBack1")
			screen.moveToFront("HudMsgPanelBack1")
			if self.bMessagePanelExpanded:
				screen.addPanel("HudMsgPanelBack2", u"", u"", True, False, iX, iY, iWidth, iHeight, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.show("HudMsgPanelBack2")
				screen.moveToFront("HudMsgPanelBack2")
			screen.addPanel("HudMsgPanel", u"", u"", True, False, iX, iY, iWidth, iHeight, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, self.BUTTON_MESSAGE_PANEL, -1)
			screen.show("HudMsgPanel")
			screen.moveToFront("HudMsgPanel")

			szBullet = u"%c " % game.getSymbolID(FontSymbols.BULLET_CHAR)
			iLabel = 0
			iTextY = iY + iHeaderHeight + iGap
			fRow = 0.0
			for i in aiShow:
				iTargetX, iTargetY, eContact = atTargets[i]
				self.dMessageRects[i] = (iX, iTextY + int(fRow * iLine), iWidth, max(1, int(len(aatLines[i]) * iLine)))
				for iPart in range(len(aatLines[i])):
					szLine = aatLines[i][iPart]
					if iPart == 0:
						szLine = szBullet + szLine
						iLineX = iX + iPad
					else:
						iLineX = iX + iPad + iIndent
					szName = "HudMsgLine%d" % iLabel
					iLabel += 1
					eWidget = WidgetTypes.WIDGET_GENERAL
					iData1 = self.BUTTON_MESSAGE_LINE
					iData2 = i
					screen.setText(szName, "Background", self.setFontSize(szLine, -1), CvUtil.FONT_LEFT_JUSTIFY, iLineX, iTextY + int(fRow * iLine), -0.3, FontTypes.SMALL_FONT, eWidget, iData1, iData2)
					self.dMessageLineIndex[szName] = i
					screen.show(szName)
					screen.moveToFront(szName)
					self.aszMessageLines.append(szName)
					fRow += 1.0
				fRow += fMessageGap

			# footer: further (older) messages, the messages of the turn before
			iFooterY = iTextY + int(iTextLines * iLine) + iPad / 2 + iGap / 2
			screen.hide("HudMsgFooterMore")
			screen.hide("HudMsgFooterPrevious")
			if bMore:
				iOlder = aPages[self.iMessagePage][0] - iNumPriority
				szMore = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_MORE", (iOlder, self.iMessagePage + 1, len(aPages)))
				screen.setText("HudMsgFooterMore", "Background", self.setFontSize(szMore, -1), CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth / 2, iFooterY, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, self.BUTTON_MESSAGE_MORE, -1)
				screen.show("HudMsgFooterMore")
				screen.moveToFront("HudMsgFooterMore")
				iFooterY += iLine
			if bFooterPrevious:
				if bPrevious:
					szPrevious = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_CURRENT", ())
				else:
					szPrevious = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_PREVIOUS", ())
				screen.setText("HudMsgFooterPrevious", "Background", self.setFontSize(szPrevious, -1), CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth / 2, iFooterY, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, self.BUTTON_MESSAGE_PREVIOUS, -1)
				screen.show("HudMsgFooterPrevious")
				screen.moveToFront("HudMsgFooterPrevious")

			screen.setText("HudMsgHeader", "Background", self.setFontSize(szHeader, -1), CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth / 2, iY + iPad / 2, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, self.BUTTON_MESSAGE_PANEL, -1)
			screen.show("HudMsgHeader")
			screen.moveToFront("HudMsgHeader")
			# the option at the top right corner
			if self.getMessageAutoExpand():
				szAuto = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_AUTO_ON", ())
			else:
				szAuto = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_AUTO_OFF", ())
			iAutoWidth = int(len(re.sub(u"<[^>]*>", u"", szAuto)) * iLine * 0.32) + iPad
			self.tMsgAutoRect = (iX + iWidth - iPad - iAutoWidth, iY, iAutoWidth + iPad, iHeaderHeight + iPad)
			screen.setText("HudMsgAuto", "Background", self.setFontSize(szAuto, -1), CvUtil.FONT_RIGHT_JUSTIFY, iX + iWidth - iPad, iY + iPad / 2, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, self.BUTTON_MESSAGE_AUTO, -1)
			screen.show("HudMsgAuto")
			screen.moveToFront("HudMsgAuto")
			self.drawMsgWpToggle(screen, iX, iY, iPad)
		except:
			# the panel must never break the main interface
			self.tMessagePanelKey = None
			if not getattr(self, "bMessagePanelErrorShown", False):
				self.bMessagePanelErrorShown = True
				CvUtil.pyPrint("Message panel failed: " + str(sys.exc_info()[1]))

	# WTP: shift + mouse wheel on a message line chooses among all the things named in it: a window beside the panel lists them (the chosen one
	# in yellow), the right click opens the chosen one. The rows of every message are kept when the panel is drawn.
	def isMessageSelected( self, iMessage ):
		try:
			return self.aszMessageTexts[iMessage] == self.szMsgSelText
		except:
			return False

	def getMessagePickNames( self ):
		aszNames = ["HudMsgPickBack1", "HudMsgPickBack2"]
		for i in range(self.iMsgPickLines):
			aszNames.append("HudMsgPickLine%d" % i)
		return aszNames

	def hideMessagePick( self, screen ):
		try:
			if self.bMsgPickShown:
				for szName in self.getMessagePickNames():
					screen.hide(szName)
					screen.deleteWidget(szName)
		except:
			pass
		self.bMsgPickShown = False
		self.iMsgPickLines = 0
	# the time in seconds for the time out of the list of the waypoints: the clock of the tooltips (getTipNow of port/nested-tooltip; the clock of
	# the game does not advance); 0 without it, then the list does not go back by itself
	def getMsgWpNow( self ):
		try:
			return self.getTipNow() / 1000.0
		except:
			return 0.0

	# the toggle "List WPs" at the top left corner of the message panel
	def drawMsgWpToggle( self, screen, iX, iY, iPad ):
		if self.bMsgWpView and self.bMsgWpSea:
			szWps = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_WPS_SEA", ())
		elif self.bMsgWpView:
			szWps = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_WPS_LAND", ())
		else:
			szWps = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_WPS_OFF", ())
		screen.setText("HudMsgWps", "Background", self.setFontSize(szWps, -1), CvUtil.FONT_LEFT_JUSTIFY, iX + iPad, iY + iPad / 2, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, self.BUTTON_MESSAGE_WPS, -1)
		screen.show("HudMsgWps")
		screen.moveToFront("HudMsgWps")

	# the waypoints for the list of the message panel: the ones of the land units or of the ships, in the order of the lists of the tooltips
	# (colonies first, then the others numbered): (sea, number, x, y, name, text of the line)
	def getMsgWaypointEntries( self ):
		aEntries = []
		try:
			for tEntry in self.getWaypointView(self.bMsgWpSea):
				aEntries.append((self.bMsgWpSea, tEntry[0], tEntry[1], tEntry[2], tEntry[3], tEntry[4]))
		except:
			pass
		return aEntries

	# the message panel with the list of the waypoints instead of the messages: in three columns (the entries one after the other from left to
	# right), a page of the height that the expanded panel has; the footer shows the next page
	def drawMsgWaypointView( self, screen, aEntries, iX, iY, iWidth, iLine, iPad, iHeaderHeight, iGap, yRes ):
		self.aszMessageTexts = []
		self.atMessageTargets = []
		self.aMsgWaypoints = []
		iCell = iWidth / 3
		# (a name must not reach into the next column: a safety margin of about a tenth, the widths of the letters are only estimated)
		iChars = max(8, int(0.9 * (iCell - 2 * iPad) / (iLine * 0.32)))
		iBottomLimit = int(yRes * 0.80)
		if self.iMsgMoveY != 0:
			iBottomLimit = yRes - 10
		iMaxRows = max(4, int((iBottomLimit - iY - iHeaderHeight - iGap - 2 * iPad) / iLine) - 2)
		if not self.bMessagePanelExpanded:
			# (collapsed: the first rows only; a click on the header shows all)
			iMaxRows = 3
		iPerPage = iMaxRows * 3
		iPages = max(1, (len(aEntries) + iPerPage - 1) / iPerPage)
		if not self.bMessagePanelExpanded:
			iPages = 1
		if self.iMsgWpPage >= iPages:
			self.iMsgWpPage = 0
		self.aMsgWpEntries = aEntries
		aShow = []
		for k in range(self.iMsgWpPage * iPerPage, min(len(aEntries), (self.iMsgWpPage + 1) * iPerPage)):
			aShow.append(k)
		iRows = max(1, (len(aShow) + 2) / 3)
		iFooterHeight = 0
		if iPages > 1:
			iFooterHeight = iLine + iGap / 2
		iHeight = iHeaderHeight + iGap + int(iRows * iLine) + iPad / 2 + iFooterHeight + iPad

		for szName in self.aszMessageLines:
			screen.hide(szName)
		self.aszMessageLines = []
		self.dMessageCapitals = {}
		self.dMessageLineIndex = {}
		self.dMessageRects = {}
		self.aMsgWpRects = []
		self.tMsgPanelRect = (iX, iY, iWidth, iHeight)
		screen.deleteWidget("HudMsgPanel")
		screen.deleteWidget("HudMsgPanelBack1")
		screen.deleteWidget("HudMsgPanelBack2")
		screen.addPanel("HudMsgPanelBack1", u"", u"", True, False, iX, iY, iWidth, iHeight, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.show("HudMsgPanelBack1")
		screen.moveToFront("HudMsgPanelBack1")
		screen.addPanel("HudMsgPanelBack2", u"", u"", True, False, iX, iY, iWidth, iHeight, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.show("HudMsgPanelBack2")
		screen.moveToFront("HudMsgPanelBack2")
		screen.addPanel("HudMsgPanel", u"", u"", True, False, iX, iY, iWidth, iHeight, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, self.BUTTON_MESSAGE_PANEL, -1)
		screen.show("HudMsgPanel")
		screen.moveToFront("HudMsgPanel")

		iTextY = iY + iHeaderHeight + iGap
		if len(aEntries) == 0:
			szEmpty = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_WPS_EMPTY", ())
			screen.setText("HudMsgLine0", "Background", self.setFontSize(szEmpty, -1), CvUtil.FONT_LEFT_JUSTIFY, iX + iPad, iTextY, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.show("HudMsgLine0")
			screen.moveToFront("HudMsgLine0")
			self.aszMessageLines.append("HudMsgLine0")
		for i in range(len(aShow)):
			iCol = i % 3
			iRow = i / 3
			iCellX = iX + iCol * iCell
			iCellY = iTextY + int(iRow * iLine)
			szText = aEntries[aShow[i]][5]
			# (the names can have color / font tags of the terrains: a long name is cut by its visible letters, the tags stay)
			# (yellow like the messages of the mod in the panel: the colors of the names are left out)
			szText = u"<color=255,255,0,255>" + self.cutTaggedText(re.sub(u"<color=[^>]*>|</color>", u"", szText), iChars) + u"</color>"
			szName = "HudMsgLine%d" % i
			screen.setText(szName, "Background", self.setFontSize(szText, -1), CvUtil.FONT_LEFT_JUSTIFY, iCellX + iPad, iCellY, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, self.BUTTON_MESSAGE_WP, aShow[i])
			screen.show(szName)
			screen.moveToFront(szName)
			self.aszMessageLines.append(szName)
			self.aMsgWpRects.append((iCellX, iCellY, iCell, int(iLine), aShow[i], iCol))

		screen.hide("HudMsgFooterMore")
		screen.hide("HudMsgFooterPrevious")
		if iPages > 1:
			iFooterY = iTextY + int(iRows * iLine) + iPad / 2 + iGap / 2
			szMore = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_WPS_MORE", (self.iMsgWpPage + 1, iPages))
			screen.setText("HudMsgFooterMore", "Background", self.setFontSize(szMore, -1), CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth / 2, iFooterY, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, self.BUTTON_MESSAGE_MORE, -1)
			screen.show("HudMsgFooterMore")
			screen.moveToFront("HudMsgFooterMore")

		if self.bMessagePanelExpanded:
			szHeader = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_WPS_HEADER_COLLAPSE", (len(aEntries),))
		else:
			szHeader = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_WPS_HEADER_EXPAND", (len(aEntries),))
		screen.setText("HudMsgHeader", "Background", self.setFontSize(szHeader, -1), CvUtil.FONT_CENTER_JUSTIFY, iX + iWidth / 2, iY + iPad / 2, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, self.BUTTON_MESSAGE_PANEL, -1)
		screen.show("HudMsgHeader")
		screen.moveToFront("HudMsgHeader")
		if self.getMessageAutoExpand():
			szAuto = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_AUTO_ON", ())
		else:
			szAuto = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_AUTO_OFF", ())
		iAutoWidth = int(len(re.sub(u"<[^>]*>", u"", szAuto)) * iLine * 0.32) + iPad
		self.tMsgAutoRect = (iX + iWidth - iPad - iAutoWidth, iY, iAutoWidth + iPad, iHeaderHeight + iPad)
		screen.setText("HudMsgAuto", "Background", self.setFontSize(szAuto, -1), CvUtil.FONT_RIGHT_JUSTIFY, iX + iWidth - iPad, iY + iPad / 2, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, self.BUTTON_MESSAGE_AUTO, -1)
		screen.show("HudMsgAuto")
		screen.moveToFront("HudMsgAuto")
		self.drawMsgWpToggle(screen, iX, iY, iPad)

	# a text with tags (<color=...>, <font=...>) cut to the width of iMax average letters (by the real width of its visible letters, narrow letters
	# take less room; the tags have no width); a cut text ends with "..", the tags that are open are closed
	def cutTaggedText( self, szText, iMax ):
		if self.getMessageWidth(re.sub(u"<[^>]*>", u"", szText)) <= iMax:
			return szText
		aOpen = []
		szResult = u""
		iVisible = 0
		for szPart in re.split(u"(<[^>]*>)", szText):
			if len(szPart) == 0:
				continue
			if szPart[0] == u"<" and szPart[-1] == u">":
				szResult += szPart
				if szPart[1:2] == u"/":
					if len(aOpen) > 0:
						aOpen.pop()
				else:
					mTag = re.match(u"<([a-zA-Z]+)", szPart)
					if mTag is not None:
						aOpen.append(mTag.group(1))
				continue
			bFull = False
			for szChar in szPart:
				iVisible += self.getMessageWidth(szChar)
				if iVisible > iMax - 1.3:
					bFull = True
					break
				szResult += szChar
			if bFull:
				break
		szResult += u".."
		while len(aOpen) > 0:
			szResult += u"</" + aOpen.pop() + u">"
		return szResult

	# a click on a waypoint of the list: left shows its place on the map, right renames it, Shift + right deletes it
	def clickMsgWaypoint( self, iIndex, bRight, bShift ):
		try:
			(bSea, iId, iX, iY, szName, szText) = self.aMsgWpEntries[iIndex]
			if not bRight:
				CyCamera().JustLookAtPlot(CyMap().plot(iX, iY))
			elif bShift:
				(aWp, iNext) = self.getWaypoints(-1, bSea)
				for k in range(len(aWp)):
					if aWp[k][0] == iId:
						# (the numbers of the others close up)
						del aWp[k]
						break
				self.saveWaypoints(aWp, iNext, -1, bSea)
				self.refreshWaypointLists()
			else:
				CvEventInterface.beginEvent(CvUtil.EventRenameWaypoint, (iId, szText))
		except:
			pass

	# the help window of a waypoint of the list
	def getMsgWaypointHelp( self, iIndex ):
		try:
			(bSea, iId, iX, iY, szName, szText) = self.aMsgWpEntries[iIndex]
			if bSea:
				szKind = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_WPS_KIND_SEA", ())
			else:
				szKind = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_WPS_KIND_LAND", ())
			return localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_WPS_HELP", (szText, szKind))
		except:
			return u""

	def showMessagePick( self, screen, szText, iCursorY, bPreferLeft = False ):
		try:
			xRes = screen.getXResolution()
			yRes = screen.getYResolution()
			iLine = self.getTipLineDistance(yRes) # as in the message panel
			iPad = max(6, iLine / 2)
			iChar = iLine * 0.32
			iMaxWidth = self.getTipMaxWidth(xRes, iChar, False)
			iCharsPerLine = max(20, int((iMaxWidth - 2 * iPad) / iChar))
			aszLines = []
			for szPart in szText.split(u"\n"):
				aszLines += self.wrapMessage(szPart, iCharsPerLine)
			iLongest = 0
			for szLine in aszLines:
				iLongest = max(iLongest, len(re.sub(u"<[^>]*>", u"", szLine)))
			iWidth = max(120, min(iMaxWidth, int(iLongest * iChar) + 2 * iPad + 8))
			iHeight = len(aszLines) * iLine + 2 * iPad
			(iPX, iPY, iPW, iPH) = self.tMsgPanelRect
			# beside the panel (right of it, left if there is no room) at the height of the cursor
			iX = iPX + iPW + 12
			if bPreferLeft and iPX - 12 - iWidth >= 4:
				iX = iPX - 12 - iWidth
			elif iX + iWidth > xRes - 4:
				iX = iPX - 12 - iWidth
			iX = max(4, iX)
			iY = max(4, min(yRes - iHeight - 4, iCursorY - iHeight / 2))
			screen.addPanel("HudMsgPickBack1", u"", u"", True, False, iX, iY, iWidth, iHeight, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.addPanel("HudMsgPickBack2", u"", u"", True, False, iX, iY, iWidth, iHeight, PanelStyles.PANEL_STYLE_HUD_HELP, WidgetTypes.WIDGET_GENERAL, -1, -1)
			self.iMsgPickLines = len(aszLines)
			for i in range(len(aszLines)):
				screen.setText("HudMsgPickLine%d" % i, "Background", self.setFontSize(aszLines[i], -1), CvUtil.FONT_LEFT_JUSTIFY, iX + iPad, iY + iPad + i * iLine, -0.3, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			for szName in self.getMessagePickNames():
				screen.show(szName)
				screen.moveToFront(szName)
			self.bMsgPickShown = True
		except:
			self.bMsgPickShown = False

	# what is selected now: the colony of the city screen or the first selected unit, as (1 colony / 0 unit, owner, number); None: nothing
	def getMsgSelectionKey( self ):
		try:
			pCity = CyInterface().getHeadSelectedCity()
			if pCity is not None and not pCity.isNone():
				return (1, pCity.getOwner(), pCity.getID())
			pUnit = CyInterface().getHeadSelectedUnit()
			if pUnit is not None and not pUnit.isNone():
				return (0, pUnit.getOwner(), pUnit.getID())
		except:
			pass
		return None

	# every frame: the message line under the cursor, the shift key and the mouse wheel
	def updateMessageScroll( self ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
		# the list of the waypoints goes back to the collapsed standard view when something else is selected than when it was switched on (another
		# unit or colony), or when what was selected is not selected any more (a selection made in a tooltip does not count)
		if self.bMsgWpView:
			try:
				if self.getMsgWpNow() - getattr(self, "fTipSelectAt", -100.0) < 1.5:
					# (a unit that the player chose in a tooltip, and what follows from it, does not count as another selection)
					self.tMsgWpSel = self.getMsgSelectionKey()
				elif self.getMsgSelectionKey() != self.tMsgWpSel:
					self.bMsgWpView = False
					self.bMsgWpSea = False
					self.bMessagePanelExpanded = False
					self.bMessagePanelPrevious = False
					self.iMessagePage = 0
					self.iMsgWpPage = 0
					self.tMessagePanelKey = None
					self.updateMessagePanel()
			except:
				pass
		iMsg = -1
		iWp = -1
		iWpCol = 0
		bAuto = False
		if len(self.aszMessageLines) > 0 and self.tMsgPanelRect is not None:
			iCX = gc.getGame().getCursorClientX()
			iCY = gc.getGame().getCursorClientY()
			if self.tMsgAutoRect is not None:
				(iAX, iAY, iAW, iAH) = self.tMsgAutoRect
				bAuto = (iCX >= iAX and iCX < iAX + iAW and iCY >= iAY and iCY < iAY + iAH)
			for iIndex in self.dMessageRects.keys():
				(iRX, iRY, iRW, iRH) = self.dMessageRects[iIndex]
				if iCX >= iRX and iCX < iRX + iRW and iCY >= iRY and iCY < iRY + iRH:
					iMsg = iIndex
					break
			# (the list of the waypoints: the cell under the cursor)
			for (iRX, iRY, iRW, iRH, iIndex, iColumn) in self.aMsgWpRects:
				if iCX >= iRX and iCX < iRX + iRW and iCY >= iRY and iCY < iRY + iRH:
					iWp = iIndex
					iWpCol = iColumn
					break
		aAll = []
		if iMsg >= 0:
			aAll = self.getMessagePediaAllTargets(iMsg)
		bShift = False
		try:
			bShift = CyInterface().shiftKey()
		except:
			pass
		# the wheel is only taken (the map does not zoom) while shift is down and the line names more than one thing
		bWheel = (iMsg >= 0 and bShift and len(aAll) > 1)
		if bWheel != self.bMsgWheel:
			self.bMsgWheel = bWheel
			try:
				gc.getGame().setWheelCapture(bWheel)
			except:
				pass
		if bWheel:
			iNotches = gc.getGame().takeWheelNotches()
			if iNotches != 0:
				szText = self.aszMessageTexts[iMsg]
				if szText != self.szMsgSelText:
					self.szMsgSelText = szText
					self.iMsgSelIdx = 0
				# the wheel towards the user: the next one, away from the user: the one before
				self.iMsgSelIdx = (self.iMsgSelIdx - iNotches) % len(aAll)
		# the window: while shift is down, or while a chosen one is kept (as long as the cursor stays on the line)
		bShow = (iMsg >= 0 and len(aAll) > 1 and (bShift or self.isMessageSelected(iMsg)))
		iSel = -1
		if bShow:
			iSel = 0
			if self.isMessageSelected(iMsg):
				iSel = self.iMsgSelIdx
		# the help of the line under the cursor / of the auto expand label: a window beside the panel (not at the cursor)
		szHelp = u""
		if not bShow:
			if bAuto:
				szHelp = localText.getText("TXT_KEY_WTP_MESSAGE_PANEL_AUTO_HELP", (self.iMsgX, self.iMsgY))
			elif iWp >= 0:
				szHelp = self.getMsgWaypointHelp(iWp)
			elif iMsg >= 0:
				szHelp = self.getMessagePediaHelp(iMsg)
		tKey = (iMsg, iSel, bShow, szHelp, iWpCol)
		if iMsg >= 0:
			tKey = (self.aszMessageTexts[iMsg], iSel, bShow, szHelp, iWpCol)
		if tKey == self.tMsgPickKey:
			return
		self.tMsgPickKey = tKey
		self.hideMessagePick(screen)
		if bShow:
			szText = localText.getText("TXT_KEY_WTP_TIP_PEDIA_LIST", ())
			for i in range(len(aAll)):
				if i == iSel:
					szText += u"\n  <color=255,255,0,255>" + aAll[i][0] + u"</color>"
				else:
					szText += u"\n  " + aAll[i][0]
			self.showMessagePick(screen, szText, gc.getGame().getCursorClientY())
		elif szHelp != u"":
			# (the help of the left column on the left of the panel, the one of the right column on the right, as long as there is room)
			self.showMessagePick(screen, szHelp, gc.getGame().getCursorClientY(), iWp >= 0 and iWpCol == 0)

	def splitIconRow(self, szWord):
		szCore = szWord.rstrip()
		iStart = len(szCore)
		while iStart > 0 and ord(szCore[iStart - 1]) >= 0x2000:
			iStart -= 1
		if iStart > 0 and len(szCore) - iStart >= 2:
			return [szWord[:iStart], szWord[iStart:]]
		return [szWord]

	fImgWidth = 3.6 # width of a picture (<img=...>) in characters

	# visible width of a line in characters (pictures and icons of the game font count more than a letter)
	def getLineWidth(self, szLine):
		return self.getMessageWidth(re.sub(u"<[^>]*>", u"", szLine)) + self.fImgWidth * len(re.findall(u"<img=", szLine.lower()))

	def isIconRow(self, szText):
		for szChar in szText:
			if ord(szChar) < 0x2000:
				return False
		return True

	def getMessagePediaTargets(self, iMessage):
		try:
			return self.getTextPediaTargets(self.aszMessageTexts[iMessage])
		except:
			return []

	def getMessagePediaAllTargets(self, iMessage):
		try:
			return self.getTextPediaAllTargets(self.aszMessageTexts[iMessage])
		except:
			return []

	def getTextPediaAllTargets(self, szMessage):
		# all things named in a text, in the order of priority (colored names and symbols, game concepts, other names; gold last)
		aResult = self.getTextPediaTargets(szMessage)
		return self.dMessagePediaAll.get(szMessage, aResult)

	def getTextPediaTargets(self, szMessage):
		# the things named (colored) in a text that have a Colopedia page: [(name, screen, id)] in the order of the text
		aResult = []
		try:
			if szMessage in self.dMessagePediaCache:
				return self.dMessagePediaCache[szMessage]
			if len(self.dMessagePediaCache) > 300:
				self.dMessagePediaCache = {}
				self.dMessagePediaAll = {}
			if self.dMessagePediaNames is None:
				dNames = {}
				# later entries must not overwrite earlier ones: units first, then professions, buildings, goods, bonuses, promotions
				aKinds = ((CvScreenEnums.PEDIA_UNIT, gc.getNumUnitInfos, gc.getUnitInfo),
					(CvScreenEnums.PEDIA_PROFESSION, gc.getNumProfessionInfos, gc.getProfessionInfo),
					(CvScreenEnums.PEDIA_BUILDING, gc.getNumBuildingInfos, gc.getBuildingInfo),
					(CvScreenEnums.PEDIA_YIELDS, gc.getNumYieldInfos, gc.getYieldInfo),
					(CvScreenEnums.PEDIA_BONUS, gc.getNumBonusInfos, gc.getBonusInfo),
					(CvScreenEnums.PEDIA_PROMOTION, gc.getNumPromotionInfos, gc.getPromotionInfo),
					(CvScreenEnums.PEDIA_TERRAIN, gc.getNumTerrainInfos, gc.getTerrainInfo),
					(CvScreenEnums.PEDIA_FEATURE, gc.getNumFeatureInfos, gc.getFeatureInfo),
					(CvScreenEnums.PEDIA_IMPROVEMENT, gc.getNumImprovementInfos, gc.getImprovementInfo))
				for (eScreen, fNum, fInfo) in aKinds:
					for i in range(fNum()):
						# (the names of some infos have color tags: [COLOR_CAT_ROAD]Paved Country Road[COLOR_REVERT])
						szName = re.sub(u"<[^>]*>", u"", fInfo(i).getDescription() or u"")
						if szName and len(szName) >= 3:
							szKey = szName.lower()
							if not szKey in dNames:
								dNames[szKey] = (szName, eScreen, i)
				# the roads have no page of their own: the concept "Pioneers and improvements" tells about them
				try:
					iImprovements = -1
					for i in range(gc.getNumConceptInfos()):
						if gc.getConceptInfo(i).getType() == "CONCEPT_IMPROVEMENTS":
							iImprovements = i
					if iImprovements >= 0:
						for i in range(gc.getNumRouteInfos()):
							szName = re.sub(u"<[^>]*>", u"", gc.getRouteInfo(i).getDescription() or u"")
							if szName and len(szName) >= 3 and not szName.lower() in dNames:
								dNames[szName.lower()] = (szName, "CONCEPT", iImprovements)
				except:
					pass
				# the symbols (font characters) of goods and bonus resources
				dChars = {}
				for (eScreen, fNum, fInfo) in ((CvScreenEnums.PEDIA_YIELDS, gc.getNumYieldInfos, gc.getYieldInfo), (CvScreenEnums.PEDIA_BONUS, gc.getNumBonusInfos, gc.getBonusInfo)):
					for i in range(fNum()):
						try:
							iChar = fInfo(i).getChar()
							if iChar > 0:
								dChars[unichr(iChar)] = (re.sub(u"<[^>]*>", u"", fInfo(i).getDescription()), eScreen, i)
						except:
							pass
				# concepts (Colopedia: game concepts): by their name and by the key words of the text MESSAGE_CONCEPT_WORDS ("stem=CONCEPT_TYPE;...")
				dConcepts = {}
				aConceptNames = []
				for i in range(gc.getNumConceptInfos()):
					try:
						szName = re.sub(u"<[^>]*>", u"", gc.getConceptInfo(i).getDescription() or u"")
						dConcepts[gc.getConceptInfo(i).getType()] = (szName, "CONCEPT", i)
						if szName and len(szName) >= 4:
							aConceptNames.append((szName, i))
					except:
						pass
				aAliases = []
				for szEntry in localText.getText("TXT_KEY_WTP_MESSAGE_CONCEPT_WORDS", ()).split(u";"):
					aParts = szEntry.strip().split(u"=")
					if len(aParts) == 2 and aParts[1].strip() in dConcepts:
						aAliases.append((re.compile(u"(?<!\\w)" + re.escape(aParts[0].strip()) + u"\\w*", re.UNICODE | re.IGNORECASE), dConcepts[aParts[1].strip()]))
				for (szName, i) in aConceptNames:
					aAliases.append((re.compile(u"(?<!\\w)" + re.escape(szName) + u"(?!\\w)", re.UNICODE | re.IGNORECASE), dConcepts[gc.getConceptInfo(i).getType()]))
				self.aMessageConceptPatterns = aAliases
				self.dMessageConcepts = dConcepts
				# the summarized storage messages (surplus sold / lost): fixed Colopedia entries instead of the many goods symbols
				aSpecial = []
				for (szKey, aTypes) in (("TXT_KEY_WTP_SURPLUS_SOLD", ("CONCEPT_DOMESTIC_MARKETS", "CONCEPT_NEW_STORAGE")), ("TXT_KEY_WTP_SURPLUS_LOST", ("CONCEPT_NEW_STORAGE",))):
					try:
						szText = localText.getText(szKey, (u"\x01", u"\x02", 0))
						szText = szText[szText.index(u"\x01") + 1:szText.index(u"\x02")]
						szText = re.sub(u"<[^>]*>", u"", szText).strip()
						if len(szText) > 10:
							aSpecial.append((szText, [dConcepts[t] for t in aTypes if t in dConcepts], None))
					except:
						pass
				# the messages about a new great person (great general / admiral, brave lieutenant, able captain): the unit page and the concept
				try:
					tConcept = dConcepts.get("CONCEPT_GREAT_GENERALS")
					dUnits = {}
					for szUnit in ("UNIT_GREAT_GENERAL", "UNIT_GREAT_ADMIRAL", "UNIT_BRAVE_LIEUTENANT", "UNIT_CAPABLE_CAPTAIN"):
						eUnit = gc.getInfoTypeForString(szUnit)
						if eUnit >= 0:
							dUnits[szUnit] = (gc.getUnitInfo(eUnit).getDescription(), CvScreenEnums.PEDIA_UNIT, eUnit)
					aGroups = []
					for szKey in ("TXT_KEY_MISC_GP_BORN", "TXT_KEY_MISC_GP_BORN_SOMEWHERE", "TXT_KEY_MISC_GP_BORN_FIELD"):
						aGroups.append((szKey, "UNIT_GREAT_GENERAL"))
					for szKey in ("TXT_KEY_MISC_BL_BORN", "TXT_KEY_MISC_BL_BORN_SOMEWHERE", "TXT_KEY_MISC_BL_BORN_FIELD"):
						aGroups.append((szKey, "UNIT_BRAVE_LIEUTENANT"))
					for szKey in ("TXT_KEY_MISC_CC_BORN", "TXT_KEY_MISC_CC_BORN_SOMEWHERE", "TXT_KEY_MISC_CC_BORN_FIELD"):
						aGroups.append((szKey, "UNIT_CAPABLE_CAPTAIN"))
					for (szKey, szUnit) in aGroups:
						if not szUnit in dUnits:
							continue
						aPieces = re.split(u"[\x01\x02]", localText.getText(szKey, (u"\x01", u"\x02")))
						aPieces = [re.sub(u"<[^>]*>", u"", t).strip() for t in aPieces]
						aPieces.sort(key = lambda t: -len(t))
						if len(aPieces[0]) > 10:
							aTargets = [dUnits[szUnit]]
							if tConcept is not None:
								aTargets.append(tConcept)
							# great generals: the admiral instead of the general if the text names him
							aSpecial.append((aPieces[0], aTargets, szUnit == "UNIT_GREAT_GENERAL" and "UNIT_GREAT_ADMIRAL" in dUnits and dUnits["UNIT_GREAT_ADMIRAL"]))
				except:
					pass
				self.aMessageSpecial = aSpecial
				self.dMessagePediaChars = dChars
				aNameList = [(k, v) for (k, v) in dNames.items() if len(k) >= 3]
				aNameList.sort(key = lambda t: -len(t[0]))
				self.aMessageNameList = aNameList
				self.dMessagePediaNames = dNames
			szPlainAll = re.sub(u"<[^>]*>", u"", szMessage)
			for (szFragment, aSpecialTargets, bGreat) in self.aMessageSpecial:
				if szFragment in szPlainAll:
					aResult = list(aSpecialTargets)
					if bGreat and bGreat[0].lower() in szPlainAll.lower() and len(aResult) > 0:
						aResult[0] = bGreat
					self.dMessagePediaCache[szMessage] = aResult
					return aResult
			# the names of settlements are cut out of the text (Fort Nassau is a city, not a fort)
			# exception: a settlement named like a Colopedia concept (Port Royal) keeps its link
			aConceptNames = [t[0].lower() for t in self.dMessageConcepts.values()]
			aCityNames = []
			for ePlayer in range(gc.getMAX_PLAYERS()):
				pPlayer = gc.getPlayer(ePlayer)
				if not pPlayer.isAlive():
					continue
				for iCity in range(pPlayer.getNumCities()):
					pCity = pPlayer.getCity(iCity)
					if pCity is not None and not pCity.isNone():
						szCity = pCity.getName().lower()
						if len(szCity) >= 3 and not szCity in aCityNames and not szCity in aConceptNames:
							aCityNames.append(szCity)
			aCityNames.sort(key = lambda t: -len(t))
			def maskCities(szText):
				szLower = szText.lower()
				for szCity in aCityNames:
					iPos = szLower.find(szCity)
					while iPos >= 0:
						szText = szText[:iPos] + u" " * len(szCity) + szText[iPos + len(szCity):]
						szLower = szLower[:iPos] + u" " * len(szCity) + szLower[iPos + len(szCity):]
						iPos = szLower.find(szCity, iPos + len(szCity))
				return szText
			dNames = self.dMessagePediaNames
			dChars = self.dMessagePediaChars
			aFound = [] # (position in the text, target)
			for oMatch in re.finditer(u"<color=[^>]*>(.*?)</color>", szMessage):
				szSegment = re.sub(u"<[^>]*>", u"", oMatch.group(1))
				szSegment = re.compile(u"^[^\\w]+|[^\\w]+$", re.UNICODE).sub(u"", szSegment).lower()
				if len(szSegment) < 3 or szSegment in aCityNames:
					continue
				tFound = dNames.get(szSegment)
				if tFound is None:
					# plural forms
					if szSegment.endswith(u"ies"):
						tFound = dNames.get(szSegment[:-3] + u"y")
					if tFound is None and szSegment.endswith(u"es"):
						tFound = dNames.get(szSegment[:-2])
					if tFound is None and szSegment.endswith(u"s"):
						tFound = dNames.get(szSegment[:-1])
				if tFound is not None:
					aFound.append((oMatch.start(), tFound))
			# symbols
			for iPos in range(len(szMessage)):
				tFound = dChars.get(szMessage[iPos])
				if tFound is not None:
					aFound.append((iPos, tFound))
			aFound.sort(key = lambda t: t[0])
			for (iPos, tFound) in aFound:
				if not tFound in aResult:
					aResult.append(tFound)
			# names in the whole text (marked or not): whole words only (at least 3 letters), the longest names first, a found name is cut out of the text
			szRest = maskCities(re.sub(u"<[^>]*>", u"", szMessage)).lower()
			aRest = []
			oWord = re.compile(u"\\w", re.UNICODE)
			for (szKey, tFound) in self.aMessageNameList:
				iStart = 0
				while True:
					iPos = szRest.find(szKey, iStart)
					if iPos < 0:
						break
					iEnd = iPos + len(szKey)
					bOk = (iPos == 0 or oWord.match(szRest[iPos - 1]) is None) and (iEnd >= len(szRest) or oWord.match(szRest[iEnd]) is None)
					if bOk:
						aRest.append((iPos, tFound))
						szRest = szRest[:iPos] + u" " * len(szKey) + szRest[iEnd:]
						break
					iStart = iPos + 1
			aRest.sort(key = lambda t: t[0])
			# game concepts in the plain text (after the marked names and symbols, before the other names)
			szPlain = maskCities(re.sub(u"<[^>]*>", u"", szMessage))
			aConcepts = []
			for (oPattern, tConcept) in self.aMessageConceptPatterns:
				oMatch = oPattern.search(szPlain)
				if oMatch is not None:
					aConcepts.append((oMatch.start(), tConcept))
			aConcepts.sort(key = lambda t: t[0])
			for (iPos, tFound) in aConcepts:
				if not tFound in aResult:
					aResult.append(tFound)
			# the names found in the whole text come last (the game concepts have priority)
			for (iPos, tFound) in aRest:
				if not tFound in aResult:
					aResult.append(tFound)
			# gold is mentioned in many messages: with more than two hits it is left out
			# (the list for the mouse wheel of the frozen tooltip keeps gold, at the end)
			aAll = list(aResult)
			if len(aResult) > 2:
				szGold = gc.getYieldInfo(YieldTypes.YIELD_GOLD).getDescription().lower()
				aResult = [t for t in aResult if t[0].lower() != szGold]
				aAll = aResult + [t for t in aAll if t[0].lower() == szGold]
			self.dMessagePediaAll[szMessage] = aAll
			self.dMessagePediaCache[szMessage] = aResult
		except:
			pass
		return aResult

	def openMessagePedia(self, iMessage, bSecond):
		try:
			aTargets = self.getMessagePediaTargets(iMessage)
			iIndex = 0
			if bSecond:
				iIndex = 1
			if self.isMessageSelected(iMessage):
				# the target chosen with shift + mouse wheel
				aTargets = self.getMessagePediaAllTargets(iMessage)
				iIndex = self.iMsgSelIdx
			if iIndex < len(aTargets):
				szName, eScreen, iEntry = aTargets[iIndex]
				if eScreen == "CONCEPT":
					iEntryId = CvScreensInterface.pediaMainScreen.pediaHistorical.getIdFromEntryInfo(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, iEntry)
					CvScreensInterface.pediaMainScreen.pediaJump(CvScreenEnums.PEDIA_HISTORY, iEntryId, True)
				else:
					CvScreensInterface.pediaMainScreen.pediaJump(eScreen, iEntry, True)
		except:
			pass

	# the native player a message names (-1: none); right click on such a message talks to the nation
	def getMessageContact(self, iMessage):
		try:
			iX, iY, eContact = self.atMessageTargets[iMessage]
			if eContact >= 0 and gc.getActivePlayer().canContact(eContact):
				return eContact
		except:
			pass
		return -1

	def contactMessageNation(self, eContact):
		try:
			gc.getActivePlayer().contact(eContact)
		except:
			pass

	def openPediaTargets(self, aTargets, bSecond):
		iIndex = 0
		if bSecond:
			iIndex = 1
		self.openPediaTargetIndex(aTargets, iIndex)

	def openPediaTargetIndex(self, aTargets, iIndex):
		try:
			if iIndex >= 0 and iIndex < len(aTargets):
				szName, eScreen, iEntry = aTargets[iIndex]
				if eScreen == "CONCEPT":
					iEntryId = CvScreensInterface.pediaMainScreen.pediaHistorical.getIdFromEntryInfo(CivilopediaPageTypes.CIVILOPEDIA_PAGE_CONCEPT, iEntry)
					CvScreensInterface.pediaMainScreen.pediaJump(CvScreenEnums.PEDIA_HISTORY, iEntryId, True)
				else:
					CvScreensInterface.pediaMainScreen.pediaJump(eScreen, iEntry, True)
		except:
			pass

	def getMessagePediaHelp(self, iMessage):
		try:
			iContact = self.getMessageContact(iMessage)
			if iContact >= 0:
				pNative = gc.getPlayer(iContact)
				szNation = pNative.getCivilizationShortDescription(0)
				if not szNation:
					szNation = pNative.getName()
				szText = localText.getText("TXT_KEY_WTP_MESSAGE_CONTACT_HELP", (szNation,))
				aContactTargets = self.getMessagePediaTargets(iMessage)
				if len(aContactTargets) > 0:
					szText += u"\n" + localText.getText("TXT_KEY_WTP_MESSAGE_PEDIA_HELP2", (aContactTargets[0][0],))
				return szText
			aTargets = self.getMessagePediaTargets(iMessage)
			if len(aTargets) == 0:
				return u""
			aAll = self.getMessagePediaAllTargets(iMessage)
			if self.isMessageSelected(iMessage):
				szText = localText.getText("TXT_KEY_WTP_MESSAGE_PEDIA_HELP", (aAll[self.iMsgSelIdx][0],))
			else:
				szText = localText.getText("TXT_KEY_WTP_MESSAGE_PEDIA_HELP", (aTargets[0][0],))
				if len(aTargets) > 1:
					szText += u"\n" + localText.getText("TXT_KEY_WTP_MESSAGE_PEDIA_HELP2", (aTargets[1][0],))
			if len(aAll) > 1:
				szText += u"\n" + localText.getText("TXT_KEY_WTP_MESSAGE_PEDIA_HELP_MORE", (len(aAll),))
			return szText
		except:
			return u""

	def clickMessageLine(self, iMessage):
		# centers the map on the place of the message
		try:
			iX, iY, eContact = self.atMessageTargets[iMessage]
			if iX >= 0:
				CyCamera().JustLookAtPlot(gc.getMap().plot(iX, iY))
		except:
			pass

	def getTipPediaHelp(self, iData):
		try:
			return self.getPediaHelpForTargets(self.getTextPediaTargets(self.getLevelParas(iData / 1000)[iData % 1000]))
		except:
			return u""

	def getPediaHelpForTargets(self, aTargets):
		try:
			if len(aTargets) == 0:
				return u""
			szText = localText.getText("TXT_KEY_WTP_MESSAGE_PEDIA_HELP", (aTargets[0][0],))
			if len(aTargets) > 1:
				szText += u"\n" + localText.getText("TXT_KEY_WTP_MESSAGE_PEDIA_HELP2", (aTargets[1][0],))
			return szText
		except:
			return u""

	def updateTerritorialInfluenceEditor(self):

		if not self.bTerritorialInfluenceMode:
			return

		if CyInterface().isCityScreenUp() or CyEngine().isGlobeviewUp():
			return

		pPlot = CyInterface().getMouseOverPlot()

		if pPlot is None or pPlot.isNone():
			return

		self.m_pCurrentTerritorialInfluencePlot = pPlot

		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		CyEngine().fillAreaBorderPlotAlt(pPlot.getX(), pPlot.getY(), AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER, "COLOR_BLUE", 1.0)

		bLeftMouseDown = CyInterface().isLeftMouseDown()
		bRightMouseDown = CyInterface().isRightMouseDown()

		if bLeftMouseDown and not self.bTerritorialInfluenceLeftMouseDown:
			iPlayer = CyGame().getActivePlayer()

			if iPlayer >= 0 and pPlot.canSetNotCulture(iPlayer):
				CyMessageControl().sendModNetMessage(
					750,
					iPlayer,
					pPlot.getX(),
					pPlot.getY(),
					1
				)

				CyEngine().fillAreaBorderPlotAlt(
					pPlot.getX(),
					pPlot.getY(),
					AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS,
					"COLOR_BLACK",
					1.0
				)

		elif bRightMouseDown and not self.bTerritorialInfluenceRightMouseDown:
			iPlayer = CyGame().getActivePlayer()

			if iPlayer >= 0:
				CyMessageControl().sendModNetMessage(
					750,
					iPlayer,
					pPlot.getX(),
					pPlot.getY(),
					0
				)

				self.refreshTerritorialInfluence(
					pPlot.getX(),
					pPlot.getY()
				)

		self.bTerritorialInfluenceLeftMouseDown = bLeftMouseDown
		self.bTerritorialInfluenceRightMouseDown = bRightMouseDown

	def refreshTerritorialInfluence(self, iSkipX = -1, iSkipY = -1):

		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)

		iPlayer = CyGame().getActivePlayer()

		if iPlayer < 0:
			return

		for iX in range(CyMap().getGridWidth()):
			for iY in range(CyMap().getGridHeight()):

				if iX == iSkipX and iY == iSkipY:
					continue

				pPlot = CyMap().plot(iX, iY)

				if not pPlot.isNone():
					if pPlot.isNotCulture(iPlayer):
						CyEngine().fillAreaBorderPlotAlt(
							iX,
							iY,
							AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS,
							"COLOR_BLACK",
							1.0
						)

	# Updates the Screen
	def update( self, fDelta ):
		self.iTick += 1
		self.updateTerritorialInfluenceEditor()
		self.updateAutomatedFollow()
		self.updateTopPortRings(False)
		return

	# WTP: the game selects the next unit when a transport gets automated: the transport stays selected (the game does its
	# selection change within a moment, so the transport is selected again during the first updates) and the camera follows it
	def updateAutomatedFollow(self):
		global g_LastSelUnit, g_LastSelAuto, g_FollowUnit, g_FollowTicks, g_FollowTurn, g_FollowX, g_FollowY
		try:
			iPlayer = gc.getGame().getActivePlayer()
			if iPlayer == -1:
				return
			pPlayer = gc.getPlayer(iPlayer)
			iRoutes = int(AutomateTypes.AUTOMATE_TRANSPORT_ROUTES)
			iFull = int(AutomateTypes.AUTOMATE_TRANSPORT_FULL)
			fNow = time.time()
			pSel = CyInterface().getHeadSelectedUnit()
			iSel = -1
			iSelAuto = -1
			if pSel != None and not pSel.isNone() and pSel.getOwner() == iPlayer:
				iSel = pSel.getID()
				iSelAuto = int(pSel.getGroup().getAutomateType())

			# the unit selected a moment ago got an automation of the transport menus
			if g_LastSelUnit != -1 and g_LastSelAuto != iRoutes and g_LastSelAuto != iFull and g_LastSelUnit != g_FollowUnit:
				pPrev = pPlayer.getUnit(g_LastSelUnit)
				if pPrev != None and not pPrev.isNone():
					iNow = int(pPrev.getGroup().getAutomateType())
					if iNow == iRoutes or iNow == iFull:
						g_FollowUnit = g_LastSelUnit
						g_FollowTicks = 0
						g_FollowTurn = gc.getGame().getGameTurn()
						g_FollowX = -1
						g_FollowY = -1

			if g_FollowUnit != -1:
				pFollow = pPlayer.getUnit(g_FollowUnit)
				if pFollow == None or pFollow.isNone() or g_FollowTurn != gc.getGame().getGameTurn():
					g_FollowUnit = -1
				elif g_FollowTicks < 8:
					g_FollowTicks += 1
					if iSel != g_FollowUnit:
						CyInterface().selectUnit(pFollow, True, False, True)
						pFollow.centerCamera()
						g_FollowX = pFollow.getX()
						g_FollowY = pFollow.getY()
					elif pFollow.getX() != g_FollowX or pFollow.getY() != g_FollowY:
						pFollow.centerCamera()
						g_FollowX = pFollow.getX()
						g_FollowY = pFollow.getY()
				elif iSel == g_FollowUnit:
					if pFollow.getX() != g_FollowX or pFollow.getY() != g_FollowY:
						pFollow.centerCamera()
						g_FollowX = pFollow.getX()
						g_FollowY = pFollow.getY()
				else:
					g_FollowUnit = -1 # another unit was selected: the following ends

			g_LastSelUnit = iSel
			g_LastSelAuto = iSelAuto
		self.updatePendingWpRename()
		self.updateCursorTooltip()
		self.pollWidgetHelp()
		self.updatePostJump()
		self.checkTradeReturnPending()
		self.updateCityJump()
		self.updateMessageMove()
		try:
			self.updateMessageScroll()
		except:
			pass
		return

	# Adds Mouse Over Help to General Widgets
	# WTP: city screen: the colony takes colonists of the job automation (the screen shows the new state at once, the game state
	# follows with the network message)
	def drawAutoAssignTarget( self, bOn ):
		screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE )
		if bOn:
			screen.changeImageButton("AutoAssignTarget", "Art/Interface/Game Hud/Actions/auto_assign_target_on.dds")
		else:
			screen.changeImageButton("AutoAssignTarget", "Art/Interface/Game Hud/Actions/auto_assign_target_off.dds")

	def toggleAutoAssignTarget( self ):
		pCity = CyInterface().getHeadSelectedCity()
		iPlayer = CyGame().getActivePlayer()
		if pCity is None or pCity.isNone() or pCity.getOwner() != iPlayer:
			return
		bOn = not pCity.isAutoAssignTarget()
		CyMessageControl().sendModNetMessage(758, iPlayer, pCity.getID(), int(bOn), 0)
		self.drawAutoAssignTarget(bOn)

	def getWidgetHelp( self, argsList ):
		iScreen, eWidgetType, iData1, iData2, bOption = argsList

		if eWidgetType == WidgetTypes.WIDGET_GENERAL:
			if iData1 == BUILDING_MANAGMENT_TOGGLE:
				return localText.getText("TXT_KEY_INTERFACE_BUILD_TOGGLE", ());
			elif iData1 == MAP_MANAGMENT_TOGGLE:
				return localText.getText("TXT_KEY_INTERFACE_MAP_TOGGLE", ());
			elif iData1 == AUTOMATION_MANAGMENT_TOGGLE:
				return localText.getText("TXT_KEY_INTERFACE_GOVERNOR_TOGGLE", ());
			elif iData1 == ACHIEVE_ADVISOR_SCREEN_MI:
				return localText.getText("TXT_KEY_INTERFACE_ACHIEVE_ADVISOR", ("F10", ""));
			elif iData1 == self.BUTTON_TERRITORIAL_INFLUENCE:
				return localText.getText("TXT_KEY_INTERFACE_TERRITORIAL_INFLUENCE", ("Ctrl+I", ""));
			elif iData1 == self.BUTTON_TRADE_ROUTE_MANAGER:
				return localText.getText("TXT_KEY_INTERFACE_TRADE_ROUTE_MANAGER", ("Shift+Alt+T", ""));
			elif iData1 == self.BUTTON_AUTO_ASSIGN_TARGET:
				pCity = CyInterface().getHeadSelectedCity()
				if pCity and pCity.isAutoAssignTarget():
					return localText.getText("TXT_KEY_INTERFACE_AUTO_ASSIGN_TARGET_ON", ())
				return localText.getText("TXT_KEY_INTERFACE_AUTO_ASSIGN_TARGET_OFF", ())
			elif iData1 == self.BUTTON_TIP_LINE:
				if CyInterface().isCityScreenUp() and self.isTradeWindowOpen():
					# (in the city screen with the import / export window the game shows this text in a window of its own, over ours)
					return u""
				return self.getTipPediaHelp(iData2)
			elif iData1 == self.BUTTON_MESSAGE_LINE or iData1 == self.BUTTON_MESSAGE_AUTO or iData1 == self.BUTTON_MESSAGE_WPS or iData1 == self.BUTTON_MESSAGE_WP:
				# (the help of the message panel is a window beside the panel, see updateMessageScroll)
				return u""
			elif iData1 == VET_NEW_CAPACITY:
				return localText.getText("TXT_KEY_NEW_STORAGE_CITY_SCREEN", ());
			elif iData1 == NEW_HARBOUR_SYSTEM:
				return localText.getText("TXT_KEY_CONCEPT_NEW_HARBOUR_SYSTEM", ());
			elif iData1 == NEW_BARRACKS_SYSTEM:
				return localText.getText("TXT_KEY_CONCEPT_NEW_BARRACKS_SYSTEM", ());
			elif iData1 == HELP_TOTAL_HAPPINESS_POSITIVE:
				return localText.getText("TXT_KEY_TOTAL_HAPPINESS_POSITIVE_EFFECTS", ());
			elif iData1 == HELP_TOTAL_HAPPINESS_NEGATIVE:
				return localText.getText("TXT_KEY_TOTAL_HAPPINESS_NEGATIVE_EFFECTS", ());
			elif iData1 == HELP_TOTAL_HAPPINESS_ZERO:
				return localText.getText("TXT_KEY_TOTAL_HAPPINESS_ZERO_EFFECTS", ());
			elif iData1 == HELP_TOTAL_LAW_POSITIVE:
				return localText.getText("TXT_KEY_TOTAL_LAW_POSITIVE_EFFECTS", ());
			elif iData1 == HELP_TOTAL_LAW_NEGATIVE:
				return localText.getText("TXT_KEY_TOTAL_LAW_NEGATIVE_EFFECTS", ());
			elif iData1 == HELP_TOTAL_LAW_ZERO:
				return localText.getText("TXT_KEY_TOTAL_LAW_ZERO_EFFECTS", ());
			elif iData1 == TIMETEXT_ID:
				return self.timeTextHelp()

		return u""

	def timeTextHelp(self):
		player = gc.getPlayer(gc.getGame().getActivePlayer())
		team = gc.getTeam(player.getTeam())

		bMessage = False
		szMessage  = localText.getText("TXT_KEY_TIMETEXT_TURN_NO_LIMIT", (CyGame().getGameTurn() + 1,))
		for iLoopVC in range(gc.getNumVictoryInfos()):
			victory = gc.getVictoryInfo(iLoopVC)
			if gc.getGame().isVictoryValid(iLoopVC):
				if (victory.isEndScore()):
					szMessage  = localText.getText("TXT_KEY_TIMETEXT_TURN", (CyGame().getGameTurn() + 1,CyGame().getEstimateEndTurn() +1))
					bMessage  = True
					break
		if not bMessage:
			for i in range(gc.getMAX_CIV_PLAYERS()):
				if gc.getPlayer(i).isInRevolution():
					szMessage  = localText.getText("TXT_KEY_TIMETEXT_TURN", (CyGame().getGameTurn() + 1,CyGame().getEstimateEndTurn() +1))
					break

		if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_MORE_VARIABLES_HIDDEN):
			szMessage += localText.getText("TXT_KEY_CURRENT_ERA", (gc.getEraInfo(player.getCurrentEra()).getText(),()))
		szMessage += localText.getText("TXT_KEY_TIMETEXT_IMMIGRATION_TITLE", ())
		szMessage += localText.getText("TXT_KEY_TIMETEXT_IMMIGRATION", (player.getCrossesStored(), player.immigrationThreshold(), gc.getYieldInfo(YieldTypes.YIELD_CROSSES).getChar(), player.getYieldRate(YieldTypes.YIELD_CROSSES)))
		szMessage += localText.getText("TXT_KEY_TIMETEXT_REBELS_TITLE", ())
		szMessage += localText.getText("TXT_KEY_TIMETEXT_REBELS", (team.getRebelPercent(),))
		szMessage += localText.getText("TXT_KEY_TIMETEXT_GENERALS_TITLE", ())
		szMessage += localText.getText("TXT_KEY_TIMETEXT_GENERALS", (player.getCombatExperience(), player.greatGeneralThreshold()))

		Fathers = []
		for i in range(gc.getNumFatherCategoryInfos()):
			Fathers.append([])

		for i in range(gc.getNumFatherInfos()):
			if gc.getGame().getFatherTeam(i) == TeamTypes.NO_TEAM:
				if not team.isFatherIgnore(i):
					iType = gc.getFatherInfo(i).getFatherCategory()
					Fathers[iType].append(i)

		for category in Fathers:
			category.sort(lambda x, y: team.getFatherPointCost(x, gc.getFatherInfo(x).getFatherCategory()) - team.getFatherPointCost(y, gc.getFatherInfo(y).getFatherCategory()))

		for iCategory in range(gc.getNumFatherCategoryInfos()):
			szCategory = gc.getFatherCategoryInfo(iCategory).getDescription()
			if Fathers[iCategory] > []:
				iFather = Fathers[iCategory][0]
				szFather = gc.getFatherInfo(iFather).getDescription()
				szMessage += localText.getText("TXT_KEY_TIMETEXT_FF", (szCategory, szFather))
				for iFatherPoint in range(gc.getNumFatherPointInfos()):
					iCost = team.getFatherPointCost(iFather, iFatherPoint)
					if iCost > 0:
						iPoints = team.getFatherPoints(iFatherPoint)
						szMessage += localText.getText("TXT_KEY_TIMETEXT_FF_POINTS", (iPoints, iCost, gc.getFatherPointInfo(iFatherPoint).getChar()))

		szMessage += localText.getText("TXT_KEY_TIMETEXT_CLOCK", (getClockText(),()))

		return szMessage

