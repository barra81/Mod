#pragma once

// selectionGroupAI.h

#ifndef CIV4_SELECTION_GROUP_AI_H
#define CIV4_SELECTION_GROUP_AI_H

#include "CvSelectionGroup.h"

class CvTradeRoute;

class CvSelectionGroupAI : public CvSelectionGroup
{

public:

	DllExport CvSelectionGroupAI();
	DllExport virtual ~CvSelectionGroupAI();

	void AI_init();
	void AI_uninit();
	void AI_reset();

	void AI_separate();
	void AI_seperateNonAI(UnitAITypes eUnitAI);
	void AI_seperateAI(UnitAITypes eUnitAI);

	void AI_separateEmptyTransports();		// TAC - AI Assault Sea - koma13, jdog5000(BBAI)

	bool AI_update();

	int AI_attackOdds(const CvPlot* pPlot, bool bPotentialEnemy) const;
	CvUnit* AI_getBestGroupAttacker(const CvPlot* pPlot, bool bPotentialEnemy, int& iUnitOdds, bool bForce = false, bool bNoBlitz = false) const;
	CvUnit* AI_getBestGroupSacrifice(const CvPlot* pPlot, bool bPotentialEnemy, bool bForce = false, bool bNoBlitz = false) const;
	int AI_compareStacks(const CvPlot* pPlot, bool bPotentialEnemy, bool bCheckCanAttack = false, bool bCheckCanMove = false) const;
	int AI_sumStrength(const CvPlot* pAttackedPlot = NULL, DomainTypes eDomainType = NO_DOMAIN, bool bCheckCanAttack = false, bool bCheckCanMove = false) const;
	void AI_queueGroupAttack(int iX, int iY);
	void AI_cancelGroupAttack();
	bool AI_isGroupAttack();

	bool AI_isControlled() const;
	bool AI_isDeclareWar(const CvPlot* pPlot = NULL);

	CvPlot* AI_getMissionAIPlot()
	{
		return AI_getMissionAIPlot_();
	}
	CvPlot* AI_getMissionAIPlot_() const;

	bool AI_isForceSeparate();
	void AI_makeForceSeparate();

	MissionAITypes AI_getMissionAIType()
	{
		return AI_getMissionAIType_();
	}
	MissionAITypes AI_getMissionAIType_() const;

	void AI_setMissionAI(MissionAITypes eNewMissionAI, CvPlot* pNewPlot, CvUnit* pNewUnit);
	CvUnit* AI_ejectBestDefender(CvPlot* pTargetPlot);

	CvUnit* AI_getMissionAIUnit();

	bool AI_isFull();

	bool AI_launchAssault(CvPlot* pTargetCityPlot = NULL);
	void AI_groupBombard();

	int AI_getYieldsLoaded(short* piYields) const;
	// WTP: free space in partly filled slots of a yield on board (a new load of the same yield is merged into them); NO_YIELD: of all yields
	int getPartialYieldSpace(YieldTypes eYield) const;
	// WTP: true if the group can load this yield here (free slot, or room in a partly filled slot of it)
	bool canLoadYieldHere(YieldTypes eYield) const;
	// WTP: a detour for loading is only worth it if a free slot is left, or if the yields available on it (per yield, NUM_YIELD_TYPES entries) can fill
	// at least 20% of a slot in total in the partly filled slots of the transport
	bool isDetourWorthwhile(const int* aiAvailable) const;

	bool AI_tradeRoutes();

	void read(CvSavegameReader reader);
	void write(CvSavegameWriter writer);

	void AI_resetSavedData();

	bool AI_isControlled() { return AI_isControlledInternal(); }
	bool AI_isControlledInternal() const { return (!isHuman() || isAutomated()); }

	// <advc.003u> Counterparts to CvSelectionGroup::getHeadUnit
	CvUnitAI const* AI_getHeadUnit() const;
	CvUnitAI* AI_getHeadUnit(); // </advc.003u>

	enum UnloadMode
	{
		NoForce,
		Force
	};

protected:

	int m_iMissionAIX;
	int m_iMissionAIY;

	bool m_bForceSeparate;

	MissionAITypes m_eMissionAIType;

	IDInfo m_missionAIUnit;

	bool m_bGroupAttack;
	int m_iGroupAttackX;
	int m_iGroupAttackY;

	// R&R mod, vetiarvind, max yield import limit - start	
	bool getIgnoreDangerStatus() const;
	// R&R mod, vetiarvind, max yield import limit - end

public:
	// WTP: the current orders of a human player's automated transport for the unit tooltip (not saved, rebuilt by AI_tradeRoutes):
	// a yield on board is brought from a source colony to a destination colony, or (bLoaded false) it is to be fetched there
	struct WtpTradeOrder
	{
		YieldTypes eYield;
		IDInfo kSource;
		IDInfo kDestination;
		bool bLoaded;
	};
	const std::vector<WtpTradeOrder>& getTradeOrders() const { return m_aTradeOrders; }
	std::vector<WtpTradeOrder> m_aTradeOrders;
	// WTP: the priority target of an automated transport that makes a pick-up stop on its way (not saved: after loading a savegame it decides anew)
	IDInfo m_kPriorityTarget;
	int m_iPriorityDetour; // turns of detour already used by the pick-up stops on the way to this target

private:
	// R&R mod, vetiarvind, max yield import limit - start
	int estimateYieldsToLoad(const CvCity* pDestinationCity, int maxYieldsToLoad, YieldTypes eYield, int turnsToReach, int alreadyLoaded) const;
	void unloadToCity(CvCity* pCity, CvUnit* unit, UnloadMode um = NoForce);
	// R&R mod, vetiarvind, max yield import limit - end

	void updateTradeOrders(const std::vector<CvTradeRoute*>& routes, const std::vector<int>& routeValues, const IDInfo& kBestDestination);
	void processTradeRoute(CvTradeRoute* pRoute, std::map<IDInfo, int>& cityValues, std::vector<CvTradeRoute*>& routes, std::vector<int>& routeValues, std::vector<bool>& yieldsDelivered, std::vector<bool>& yieldsToUnload);
};

#endif
