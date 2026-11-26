#include "CvGameCoreDLL.h"
#include "CyGame.h"
#include "CyDeal.h"
#include "CvRandom.h"
#include "CyCity.h"
#include "CyReplayInfo.h"

#include <boost/python/class.hpp>
#include <boost/python/manage_new_object.hpp>

//
// published python interface for CyGame
//

void CyGamePythonInterface2(python::class_<CyGame>& x)
{
	OutputDebugString("Python Extension Module - CyGamePythonInterface2\n");

	x
		.def("getHandicapType", &CyGame::getHandicapType, "HandicapType () - difficulty level settings")
		.def("getCalendar", &CyGame::getCalendar, "CalendarType ()")
		.def("getStartEra", &CyGame::getStartEra)
		.def("getGameSpeedType", &CyGame::getGameSpeedType)
		.def("getCargoYieldCapacity", &CyGame::getCargoYieldCapacity)
		.def("getRankPlayer", &CyGame::getRankPlayer)
		.def("getPlayerScore", &CyGame::getPlayerScore)
		.def("getRankTeam", &CyGame::getRankTeam)
		.def("getTeamRank", &CyGame::getTeamRank)
		.def("getTeamScore", &CyGame::getTeamScore)
		.def("isOption", &CyGame::isOption, "bool (eIndex) - returns whether Game Option is valid")
		.def("setOption", &CyGame::setOption, "void (GameOptionIndex, bEnabled) - sets a Game Option")
		.def("isMPOption", &CyGame::isMPOption, "bool (eIndex) - returns whether MP Option is valid")
		.def("isForcedControl", &CyGame::isForcedControl, "bool (eIndex) - returns whether Control should be forced")
		.def("getUnitCreatedCount", &CyGame::getUnitCreatedCount, "int (eIndex) - returns number of this unit type created (?)")
		.def("getUnitClassCreatedCount", &CyGame::getUnitClassCreatedCount, "int (eIndex) - returns number of this unit class type created (?)")
		.def("getBuildingClassCreatedCount", &CyGame::getBuildingClassCreatedCount, "int (BuildingClassType) - building Class count")
		.def("isVictoryValid", &CyGame::isVictoryValid)
		.def("isSpecialUnitValid", &CyGame::isSpecialUnitValid)
		.def("makeSpecialUnitValid", &CyGame::makeSpecialUnitValid)
		.def("isSpecialBuildingValid", &CyGame::isSpecialBuildingValid)
		.def("makeSpecialBuildingValid", &CyGame::makeSpecialBuildingValid)
		.def("isUniqueGoodyValid", &CyGame::isUniqueGoodyValid) // R&R, ray, Goody Enhancement
		.def("setUniqueGoodyValid", &CyGame::setUniqueGoodyValid) // R&R, ray, Goody Enhancement
		.def("isInAdvancedStart", &CyGame::isInAdvancedStart, "bool")
		.def("getScriptData", &CyGame::getScriptData, "str () - Returns ScriptData member (used to store custom data)")
		.def("setScriptData", &CyGame::setScriptData, "void (str) - Sets ScriptData member (used to store custom data)")
		.def("setName", &CyGame::setName)
		.def("getName", &CyGame::getName)
		.def("getIndexAfterLastDeal", &CyGame::getIndexAfterLastDeal)
		.def("getNumDeals", &CyGame::getNumDeals)
		.def("getDeal", &CyGame::getDeal, python::return_value_policy<python::manage_new_object>())
		.def("addDeal", &CyGame::addDeal, python::return_value_policy<python::manage_new_object>())
		.def("getMapRand", &CyGame::getMapRand, python::return_value_policy<python::reference_existing_object>())
		.def("getMapRandNum", &CyGame::getMapRandNum)
		.def("getSorenRand", &CyGame::getSorenRand, python::return_value_policy<python::reference_existing_object>())
		.def("getSorenRandNum", &CyGame::getSorenRandNum)
		.def("calculateSyncChecksum", &CyGame::calculateSyncChecksum)
		.def("calculateOptionsChecksum", &CyGame::calculateOptionsChecksum)
		.def("GetWorldBuilderMode", &CyGame::GetWorldBuilderMode)
		.def("isPitbossHost", &CyGame::isPitbossHost)
		.def("getCurrentLanguage", &CyGame::getCurrentLanguage)
		.def("setCurrentLanguage", &CyGame::setCurrentLanguage)
		.def("getReplayMessageTurn", &CyGame::getReplayMessageTurn)
		.def("getReplayMessageType", &CyGame::getReplayMessageType)
		.def("getReplayMessagePlotX", &CyGame::getReplayMessagePlotX)
		.def("getReplayMessagePlotY", &CyGame::getReplayMessagePlotY)
		.def("getReplayMessagePlayer", &CyGame::getReplayMessagePlayer)
		.def("getReplayMessageColor", &CyGame::getReplayMessageColor)
		.def("getReplayMessageText", &CyGame::getReplayMessageText)
		.def("setCursorClient", &CyGame::setCursorClient, "void (int iX, int iY) - puts the cursor on this place of the game window")
		.def("getMiddleClickX", &CyGame::getMiddleClickX, "int () - x of the cursor at the last wheel click")
		.def("getMiddleClickY", &CyGame::getMiddleClickY, "int () - y of the cursor at the last wheel click")
		.def("takeMiddleClick", &CyGame::takeMiddleClick, "bool () - was the mouse wheel clicked a moment ago (asked once per click)")
		.def("getWidgetHelpText", &CyGame::getWidgetHelpText, "wstring () - the last help text of a widget of the interface")
		.def("getWidgetHelpCount", &CyGame::getWidgetHelpCount, "int () - number of help requests so far")
		.def("getWidgetHelpType", &CyGame::getWidgetHelpType, "int () - widget type of the last help request")
		.def("getWidgetHelpFor", &CyGame::getWidgetHelpFor, "wstring (int eWidgetType, int iData1, int iData2, bool bOption) - the help text of a widget")
		.def("getCityBarHelpFor", &CyGame::getCityBarHelpFor, "wstring (int iPlayer, int iCityID) - the tooltip text of the banner of a city")
		.def("isDiplomacyUp", &CyGame::isDiplomacyUp, "bool () - is a diplomacy screen open")
		.def("setHideYieldHelp", &CyGame::setHideYieldHelp, "void (bool) - the game gives no help text for goods pictures (import / export window of the city screen)")
		.def("setHideGameHelp", &CyGame::setHideGameHelp, "void (bool) - the game gives no help text for HUD elements while the diplomacy screen is open")
		.def("getNumReplayMessages", &CyGame::getNumReplayMessages)
		.def("setWheelCapture", &CyGame::setWheelCapture, "void (bool bOn) - collects the mouse wheel (takeWheelNotches) instead of the game using it")
		.def("takeWheelNotches", &CyGame::takeWheelNotches, "int () - the notches of the mouse wheel since the last call")
		.def("isCtrlKeyPressed", &CyGame::isCtrlKeyPressed, "bool () - is the control key down")
		.def("isShiftKeyPressed", &CyGame::isShiftKeyPressed, "bool () - is the shift key down")
		.def("getCursorClientX", &CyGame::getCursorClientX, "int () - mouse x in the game window")
		.def("getCursorClientY", &CyGame::getCursorClientY, "int () - mouse y in the game window")
		.def("getNumHudMessages", &CyGame::getNumHudMessages, "int () - messages of the turn for the message panel")
		.def("getHudMessageText", &CyGame::getHudMessageText, "wstring (int)")
		.def("getHudMessageX", &CyGame::getHudMessageX, "int (int)")
		.def("getHudMessageY", &CyGame::getHudMessageY, "int (int)")
		.def("getNumHudPriority", &CyGame::getNumHudPriority, "int () - priority messages (at the top) of the turn")
		.def("addHudMessage", &CyGame::addHudMessage, "void (wstring szText, bool bPriority) - a message for the message panel (priority: at the top)")
		.def("addMessage", &CyGame::addMessage, "void (int iPlayer, bool bForce, int iLength, wstring szString, string szSound, int eType, string szIcon, int eFlashColor, int iFlashX, int iFlashY, bool bShowOffScreenArrows, bool bShowOnScreenArrows) - CyInterface().addMessage through the DLL (the message panel gets the message)")
		.def("getNumHudPriorityPrevious", &CyGame::getNumHudPriorityPrevious, "int () - priority messages (at the top) of the turn before")
		.def("getNumHudMessagesPrevious", &CyGame::getNumHudMessagesPrevious, "int () - messages of the turn before")
		.def("getHudMessagePreviousText", &CyGame::getHudMessagePreviousText, "wstring (int)")
		.def("getHudMessagePreviousX", &CyGame::getHudMessagePreviousX, "int (int)")
		.def("getHudMessagePreviousY", &CyGame::getHudMessagePreviousY, "int (int)")
		.def("isArrowKeyPressed", &CyGame::isArrowKeyPressed, "bool (int iDir) - is an arrow key down (0 left, 1 right, 2 up, 3 down)")
		.def("isVirtualKeyPressed", &CyGame::isVirtualKeyPressed, "bool (int iVirtualKey) - is the key with this Windows virtual key code down")
		.def("sendYieldTransfer", &CyGame::sendYieldTransfer, "void (int iUnitID, int iData3, int iYield, int iAmount, bool bPlayerAction) - transfers goods like the amount popup (bPlayerAction: Europe / Africa / Port Royal)")
		.def("sendDiploYieldAmount", &CyGame::sendDiploYieldAmount, "void (int iYield, int iAmount, int iFromPlayer) - sets the amount of goods of a diplomacy deal")
		.def("openDomesticMarket", &CyGame::openDomesticMarket, "void (int iCityID) - opens the domestic market popup of the city")
		.def("getReplayInfo", &CyGame::getReplayInfo, python::return_value_policy<python::manage_new_object>())
		;
}
