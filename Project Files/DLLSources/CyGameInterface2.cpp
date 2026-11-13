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
		.def("getNumReplayMessages", &CyGame::getNumReplayMessages)
		.def("openDomesticMarket", &CyGame::openDomesticMarket, "void (int iCityID) - opens the domestic market popup of the city")
		.def("setWheelCapture", &CyGame::setWheelCapture, "void (bool bOn) - collects the mouse wheel (takeWheelNotches) instead of the game using it")
		.def("takeWheelNotches", &CyGame::takeWheelNotches, "int () - the notches of the mouse wheel since the last call")
		.def("isCtrlKeyPressed", &CyGame::isCtrlKeyPressed, "bool () - is the control key down")
		.def("sendDiploYieldAmount", &CyGame::sendDiploYieldAmount, "void (int iYield, int iAmount, int iFromPlayer) - sets the amount of goods of a diplomacy deal")
		.def("sendYieldTransfer", &CyGame::sendYieldTransfer, "void (int iUnitID, int iData3, int iYield, int iAmount, bool bPlayerAction) - transfers goods like the amount popup (bPlayerAction: Europe / Africa / Port Royal)")
		.def("getWidgetHelpText", &CyGame::getWidgetHelpText, "wstring () - the last help text of a widget of the interface")
		.def("getWidgetHelpCount", &CyGame::getWidgetHelpCount, "int () - number of help requests so far")
		.def("getWidgetHelpType", &CyGame::getWidgetHelpType, "int () - widget type of the last help request")
		.def("getWidgetHelpFor", &CyGame::getWidgetHelpFor, "wstring (int eWidgetType, int iData1, int iData2, bool bOption) - the help text of a widget")
		.def("getCursorClientX", &CyGame::getCursorClientX, "int () - mouse x in the game window")
		.def("getCursorClientY", &CyGame::getCursorClientY, "int () - mouse y in the game window")
		.def("getNumHudMessages", &CyGame::getNumHudMessages, "int () - messages of the turn for the message panel")
		.def("getHudMessageText", &CyGame::getHudMessageText, "wstring (int)")
		.def("getHudMessageX", &CyGame::getHudMessageX, "int (int)")
		.def("getHudMessageY", &CyGame::getHudMessageY, "int (int)")
		.def("getNumHudPriority", &CyGame::getNumHudPriority, "int () - priority messages (at the top) of the turn")
		.def("getNumHudPriorityPrevious", &CyGame::getNumHudPriorityPrevious, "int () - priority messages (at the top) of the turn before")
		.def("getNumHudMessagesPrevious", &CyGame::getNumHudMessagesPrevious, "int () - messages of the turn before")
		.def("getHudMessagePreviousText", &CyGame::getHudMessagePreviousText, "wstring (int)")
		.def("getHudMessagePreviousX", &CyGame::getHudMessagePreviousX, "int (int)")
		.def("getHudMessagePreviousY", &CyGame::getHudMessagePreviousY, "int (int)")
		.def("getReplayInfo", &CyGame::getReplayInfo, python::return_value_policy<python::manage_new_object>())
		;
}
