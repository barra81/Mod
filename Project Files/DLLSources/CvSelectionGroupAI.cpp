// selectionGroupAI.cpp

#include "CvGameCoreDLL.h"
#include "CvSelectionGroupAI.h"
#include "CvPlayerAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvTeamAI.h"
#include "CvDLLEntityIFaceBase.h"
#include "CvGameCoreUtils.h"
#include "FProfiler.h"
#include "CvInfos.h"
#include "CvTradeRoute.h"
//TAC Whaling, ray
#include "CvDLLInterfaceIFaceBase.h"
//End TAC Whaling, ray

#include "CvSavegame.h"
// Public Functions...

CvSelectionGroupAI::CvSelectionGroupAI()
{
	AI_reset();
}


CvSelectionGroupAI::~CvSelectionGroupAI()
{
	AI_uninit();
}


void CvSelectionGroupAI::AI_init()
{
	AI_reset();

	//--------------------------------
	// Init other game data
}


void CvSelectionGroupAI::AI_uninit()
{
}


void CvSelectionGroupAI::AI_reset()
{
	AI_uninit();
	AI_resetSavedData();
	m_kPriorityTarget = IDInfo();
	m_iPriorityDetour = 0;
	m_iNoDestinationSince = -1;
	m_kTooltipStop = IDInfo();
	m_bTooltipWaiting = false;
	m_aiTooltipStopYields.clear();
}


void CvSelectionGroupAI::AI_separate()
{
	CLLNode<IDInfo>* pEntityNode;
	CvUnit* pLoopUnit;

	pEntityNode = headUnitNode();

	while (pEntityNode != NULL)
	{
		pLoopUnit = ::getUnit(pEntityNode->m_data);
		pEntityNode = nextUnitNode(pEntityNode);

		if (pLoopUnit != NULL)
		{
			pLoopUnit->joinGroup(NULL);
			if (pLoopUnit->plot()->getTeam() == getTeam())
			{
				pLoopUnit->getGroup()->pushMission(MISSION_SKIP);
			}
		}
	}
}

void CvSelectionGroupAI::AI_seperateNonAI(UnitAITypes eUnitAI)
{
	CLLNode<IDInfo>* pEntityNode;
	CvUnit* pLoopUnit;

	pEntityNode = headUnitNode();

	while (pEntityNode != NULL)
	{
		pLoopUnit = ::getUnit(pEntityNode->m_data);
		pEntityNode = nextUnitNode(pEntityNode);
		if (pLoopUnit != NULL && pLoopUnit->AI_getUnitAIType() != eUnitAI)
		{
			pLoopUnit->joinGroup(NULL);
			if (pLoopUnit->plot()->getTeam() == getTeam())
			{
				pLoopUnit->getGroup()->pushMission(MISSION_SKIP);
			}
		}
	}
}

void CvSelectionGroupAI::AI_seperateAI(UnitAITypes eUnitAI)
{
	CLLNode<IDInfo>* pEntityNode;
	CvUnit* pLoopUnit;

	pEntityNode = headUnitNode();

	while (pEntityNode != NULL)
	{
		pLoopUnit = ::getUnit(pEntityNode->m_data);
		pEntityNode = nextUnitNode(pEntityNode);
		if (pLoopUnit != NULL && pLoopUnit->AI_getUnitAIType() == eUnitAI)
		{
			pLoopUnit->joinGroup(NULL);
			// TAC - AI Assault Sea - koma13, jdog5000(BBAI)
			// Was potential crash in use of plot() if group emptied
			//if (plot()->getTeam() == getTeam())
			if (pLoopUnit->plot()->getTeam() == getTeam())
			// TAC - AI Assault Sea - koma13, jdog5000(BBAI)
			{
				pLoopUnit->getGroup()->pushMission(MISSION_SKIP);
			}
		}
	}
}
// TAC - AI Assault Sea - koma13, jdog5000(BBAI)
void CvSelectionGroupAI::AI_separateEmptyTransports()
{
	CLLNode<IDInfo>* pEntityNode;
	CvUnit* pLoopUnit;

	pEntityNode = headUnitNode();

	while (pEntityNode != NULL)
	{
		pLoopUnit = ::getUnit(pEntityNode->m_data);
		pEntityNode = nextUnitNode(pEntityNode);
		if (pLoopUnit != NULL && (pLoopUnit->AI_getUnitAIType() == UNITAI_ASSAULT_SEA) && (pLoopUnit->getCargo() == 0))
		{
			pLoopUnit->joinGroup(NULL);
			if (pLoopUnit->plot()->getTeam() == getTeam())
			{
				pLoopUnit->getGroup()->pushMission(MISSION_SKIP);
			}
		}
	}
}
// TAC - AI Assault Sea - koma13, jdog5000(BBAI)

// Returns true if the group has become busy...
bool CvSelectionGroupAI::AI_update()
{
	CLLNode<IDInfo>* pEntityNode;
	CvUnit* pLoopUnit;
	bool bDead;
	bool bFollow;

	PROFILE_FUNC();

	FAssert(getOwnerINLINE() != NO_PLAYER);

	if (!AI_isControlled())
	{
		return false;
	}

	if (getNumUnits() == 0)
	{
		return false;
	}

	if (isForceUpdate())
	{
		clearMissionQueue(); // XXX ???
		setActivityType(ACTIVITY_AWAKE);
		setForceUpdate(false);

		// if we are in the middle of attacking with a stack, cancel it
		AI_cancelGroupAttack();
	}

	FAssert(!(GET_PLAYER(getOwnerINLINE()).isAutoMoves()));

	int iTempHack = 0; // XXX

	bDead = false;

	bool bFailedAlreadyFighting = false;
	while ((m_bGroupAttack && !bFailedAlreadyFighting) || readyToMove())
	{
		iTempHack++;
		if (iTempHack > 100)
		{
			FAssert(false);
			CvUnit* pHeadUnit = getHeadUnit();
			if (NULL != pHeadUnit)
			{
				if (GC.getLogging())
				{
					char szOut[1024];
					CvWString szTempString;
					getUnitAIString(szTempString, pHeadUnit->AI_getUnitAIType());
					sprintf(szOut, "Unit stuck in loop: %S(%S)[%d, %d] (%S)", pHeadUnit->getName().GetCString(), GET_PLAYER(pHeadUnit->getOwnerINLINE()).getName(),
						pHeadUnit->getX_INLINE(), pHeadUnit->getY_INLINE(), szTempString.GetCString());
					gDLL->messageControlLog(szOut);
				}

				pHeadUnit->finishMoves();
			}
			break;
		}

		// if we want to force the group to attack, force another attack
		if (m_bGroupAttack)
		{
			if (isBusy())
			{
				break;
			}

			m_bGroupAttack = false;

			groupAttack(CREATE_ASSERT_DATA, m_iGroupAttackX, m_iGroupAttackY, MOVE_DIRECT_ATTACK, bFailedAlreadyFighting);
		}
		// else pick AI action
		else
		{
			CvUnit* pHeadUnit = getHeadUnit();

			if (pHeadUnit == NULL || pHeadUnit->isDelayedDeath())
			{
				break;
			}

			if (pHeadUnit->AI_update())
			{
				// AI_update returns true when we should abort the loop and wait until next slice
				break;
			}
		}

		if (doDelayedDeath())
		{
			bDead = true;
			break;
		}

		// if no longer group attacking, and force separate is true, then bail, decide what to do after group is split up
		// (UnitAI of head unit may have changed)
		if (!m_bGroupAttack && AI_isForceSeparate())
		{
			AI_separate();	// pointers could become invalid...
			return true;
		}
	}

	if (!bDead)
	{
		CvUnit* pHeadUnit = getHeadUnit();
		if (pHeadUnit != NULL)
		{
			if ((pHeadUnit->getUnitTravelState() == UNIT_TRAVEL_STATE_IN_EUROPE || pHeadUnit->getUnitTravelState() == UNIT_TRAVEL_STATE_IN_AFRICA) && AI_isControlled())
			{
				pEntityNode = headUnitNode();

				while (pEntityNode != NULL)
				{
					pLoopUnit = ::getUnit(pEntityNode->m_data);
					pEntityNode = nextUnitNode(pEntityNode);

					if (pLoopUnit != NULL)
					{
						pLoopUnit->AI_europeUpdate();
					}
				}
			}
		}

		if (!isHuman())
		{
			bFollow = false;

			// if we not group attacking, then check for follow action
			if (!m_bGroupAttack)
			{
				pEntityNode = headUnitNode();

				while ((pEntityNode != NULL) && readyToMove(true))
				{
					pLoopUnit = ::getUnit(pEntityNode->m_data);
					pEntityNode = nextUnitNode(pEntityNode);

					if (pLoopUnit != NULL && pLoopUnit->canMove())
					{
						if (pLoopUnit->AI_follow())
						{
							bFollow = true;
							break;
						}
					}
				}
			}

			if (doDelayedDeath())
			{
				bDead = true;
			}

			if (!bDead)
			{
				if (!bFollow && readyToMove(true))
				{
					pushMission(MISSION_SKIP);
				}
			}
		}
	}

	if (bDead)
	{
		return true;
	}

	return (isBusy() || isCargoBusy());
}


// Returns attack odds out of 100 (the higher, the better...)
int CvSelectionGroupAI::AI_attackOdds(const CvPlot* pPlot, bool bPotentialEnemy) const
{
	PROFILE_FUNC();

	CvUnit* pAttacker;

	FAssert(getOwnerINLINE() != NO_PLAYER);

	/************************************************************************************************/
	/* BETTER_BTS_AI_MOD                      02/21/10                                jdog5000      */
	/*                                                                                              */
	/* Efficiency, Lead From Behind                                                                 */
	/************************************************************************************************/
	// From Lead From Behind by UncutDragon
	// original
	//if (pPlot->getBestDefender(NO_PLAYER, getOwnerINLINE(), NULL, !bPotentialEnemy, bPotentialEnemy) == NULL)
	// modified
	if (!pPlot->hasDefender(false, NO_PLAYER, getOwnerINLINE(), NULL, !bPotentialEnemy, bPotentialEnemy))
		/************************************************************************************************/
		/* BETTER_BTS_AI_MOD                       END                                                  */
		/************************************************************************************************/
	{
		return 100;
	}

	int iOdds = 0;
	pAttacker = AI_getBestGroupAttacker(pPlot, bPotentialEnemy, iOdds);

	if (pAttacker == NULL)
	{
		return 0;
	}

	return iOdds;
}

CvUnit* CvSelectionGroupAI::AI_getBestGroupAttacker(const CvPlot* pPlot, bool bPotentialEnemy, int& iUnitOdds, bool bForce, bool bNoBlitz) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvUnit* pBestUnit;
	int iValue;
	int iBestValue;
	int iOdds;
	int iBestOdds;

	iBestValue = 0;
	iBestOdds = 0;
	pBestUnit = NULL;

	pUnitNode = headUnitNode();

	bool bIsHuman = true;
	
	if (pUnitNode != NULL)
	{
		const CvUnit* pUnit = ::getUnit(pUnitNode->m_data);
		if (pUnit != NULL)
		{
			bIsHuman = GET_PLAYER(pUnit->getOwnerINLINE()).isHuman();
		}
	}

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (pLoopUnit != NULL && !pLoopUnit->isDead())
		{
			bool bCanAttack = false;
			bCanAttack = pLoopUnit->canAttack();

			if (bCanAttack && bNoBlitz && pLoopUnit->isBlitz() && pLoopUnit->isMadeAttack())
			{
				bCanAttack = false;
			}

			// attack bug fix - start - Nightinggale
			if (bCanAttack && !pLoopUnit->canMoveInto(*pPlot, true))
			{
				// Don't let the AI attack with this unit as it can't move into the plot in question.
				bCanAttack = false;
			}
			// attack bug fix - end - Nightinggale

			if (bCanAttack)
			{
				if (bForce || pLoopUnit->canMove())
				{
					if (bForce || pLoopUnit->canMoveInto(*pPlot, /*bAttack*/ true, /*bDeclareWar*/ bPotentialEnemy))
					{
						iOdds = pLoopUnit->AI_attackOdds(pPlot, bPotentialEnemy);

						iValue = iOdds;
						FAssertMsg(iValue > 0, "iValue is expected to be greater than 0");

						// if non-human, prefer the last unit that has the best value (so as to avoid splitting the group)
						if (iValue > iBestValue || (!bIsHuman && iValue > 0 && iValue == iBestValue))
						{
							iBestValue = iValue;
							iBestOdds = iOdds;
							pBestUnit = pLoopUnit;
						}
					}
				}
			}
		}
	}

	iUnitOdds = iBestOdds;
	return pBestUnit;
}

CvUnit* CvSelectionGroupAI::AI_getBestGroupSacrifice(const CvPlot* pPlot, bool bPotentialEnemy, bool bForce, bool bNoBlitz) const
{
	int iBestValue = 0;
	CvUnit* pBestUnit = NULL;

	CLLNode<IDInfo>* pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (pLoopUnit != NULL && !pLoopUnit->isDead())
		{
			bool bCanAttack = false;
			bCanAttack = pLoopUnit->canAttack();

			if (bCanAttack && bNoBlitz && pLoopUnit->isBlitz() && pLoopUnit->isMadeAttack())
			{
				bCanAttack = false;
			}

			if (bCanAttack)
			{
				if (bForce || pLoopUnit->canMove())
				{
					if (bForce || pLoopUnit->canMoveInto(*pPlot, true))
					{
                        int iValue = pLoopUnit->AI_sacrificeValue(pPlot);
						FAssertMsg(iValue > 0, "iValue is expected to be greater than 0");

						// we want to pick the last unit of highest value, so pick the last unit with a good value
						if (iValue >= iBestValue)
						{
							iBestValue = iValue;
							pBestUnit = pLoopUnit;
						}
					}
				}
			}
		}
	}

	return pBestUnit;
}

// Returns ratio of strengths of stacks times 100
// (so 100 is even ratio, numbers over 100 mean this group is more powerful than the stack on a plot)
int CvSelectionGroupAI::AI_compareStacks(const CvPlot* pPlot, bool bPotentialEnemy, bool bCheckCanAttack, bool bCheckCanMove) const
{
	FAssert(pPlot != NULL);

	int	compareRatio;
	DomainTypes eDomainType = getDomainType();

	// choose based on the plot, not the head unit (mainly for transport carried units)
	if (pPlot->isWater())
		eDomainType = DOMAIN_SEA;
	else
		eDomainType = DOMAIN_LAND;

	compareRatio = AI_sumStrength(pPlot, eDomainType, bCheckCanAttack, bCheckCanMove);
	compareRatio *= 100;

	PlayerTypes eOwner = getOwnerINLINE();
	if (eOwner == NO_PLAYER)
	{
		eOwner = getHeadOwner();
	}
	FAssert(eOwner != NO_PLAYER);

	int defenderSum = pPlot->AI_sumStrength(NO_PLAYER, getOwnerINLINE(), eDomainType, true, !bPotentialEnemy, bPotentialEnemy);
	compareRatio /= std::max(1, defenderSum);

	return compareRatio;
}

int CvSelectionGroupAI::AI_sumStrength(const CvPlot* pAttackedPlot, DomainTypes eDomainType, bool bCheckCanAttack, bool bCheckCanMove) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	int	strSum = 0;

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (pLoopUnit != NULL && !pLoopUnit->isDead())
		{
			bool bCanAttack = pLoopUnit->canAttack();

			if (!bCheckCanAttack || bCanAttack)
			{
				if (!bCheckCanMove || pLoopUnit->canMove())
					if (!bCheckCanMove || pAttackedPlot == NULL || pLoopUnit->canMoveInto(*pAttackedPlot, /*bAttack*/ true, /*bDeclareWar*/ true))
						if (eDomainType == NO_DOMAIN || pLoopUnit->getDomainType() == eDomainType)
							strSum += pLoopUnit->currEffectiveStr(pAttackedPlot, pLoopUnit);
			}
		}
	}

	return strSum;
}

void CvSelectionGroupAI::AI_queueGroupAttack(int iX, int iY)
{
	m_bGroupAttack = true;

	m_iGroupAttackX = iX;
	m_iGroupAttackY = iY;
}

inline void CvSelectionGroupAI::AI_cancelGroupAttack()
{
	m_bGroupAttack = false;
}

inline bool CvSelectionGroupAI::AI_isGroupAttack()
{
	return m_bGroupAttack;
}

bool CvSelectionGroupAI::AI_isControlled() const
{
	return (!isHuman() || isAutomated());
}


bool CvSelectionGroupAI::AI_isDeclareWar(const CvPlot* pPlot)
{
	FAssert(getHeadUnit() != NULL);

	if (isHuman())
	{
		return false;
	}
	else
	{
		bool bLimitedWar = false;
		if (pPlot != NULL)
		{
			TeamTypes ePlotTeam = pPlot->getTeam();
			if (ePlotTeam != NO_TEAM)
			{
				WarPlanTypes eWarplan = GET_TEAM(getTeam()).AI_getWarPlan(ePlotTeam);
				if (eWarplan == WARPLAN_LIMITED)
				{
					bLimitedWar = true;
				}
			}
		}

		CvUnit* pHeadUnit = getHeadUnit();

		if (pHeadUnit != NULL)
		{
			switch (pHeadUnit->AI_getUnitAIType())
			{
			case UNITAI_UNKNOWN:
			case UNITAI_ANIMAL: // R&R, ray, Wild Animals
			case UNITAI_ANIMAL_SEA: // R&R, ray, Wild Animals
			case UNITAI_FLEEING: // R&R, ray, Fleeing Units
			case UNITAI_COLONIST:
			case UNITAI_SETTLER:
			case UNITAI_WORKER:
			case UNITAI_MISSIONARY:
			case UNITAI_TRADER: // WTP, ray, Native Trade Posts - START
			case UNITAI_SCOUT:
			case UNITAI_WAGON:
			case UNITAI_TREASURE:
			case UNITAI_YIELD:
			case UNITAI_GENERAL:
				return false;
				break;

			case UNITAI_DEFENSIVE:
			case UNITAI_OFFENSIVE:
			case UNITAI_COUNTER:
				return true;
				break;
			//TAC Whaling, ray
			case UNITAI_WORKER_SEA:
			//End TAC Whaling, ray
			case UNITAI_TRANSPORT_SEA:
			case UNITAI_TRANSPORT_COAST:
				return false;
				break;

			case UNITAI_ASSAULT_SEA:
			case UNITAI_COMBAT_SEA:
			case UNITAI_PIRATE_SEA:
			case UNITAI_ESCORT_SEA:			// TAC - AI Escort Sea - koma13
				return true;
				break;

			default:
				FAssert(false);
				break;
			}
		}
	}

	return false;
}


CvPlot* CvSelectionGroupAI::AI_getMissionAIPlot_() const
{
	return GC.getMap().plotSoren(m_iMissionAIX, m_iMissionAIY);
}


bool CvSelectionGroupAI::AI_isForceSeparate()
{
	return m_bForceSeparate;
}


void CvSelectionGroupAI::AI_makeForceSeparate()
{
	m_bForceSeparate = true;
}


MissionAITypes CvSelectionGroupAI::AI_getMissionAIType_() const
{
	return m_eMissionAIType;
}


void CvSelectionGroupAI::AI_setMissionAI(MissionAITypes eNewMissionAI, CvPlot* pNewPlot, CvUnit* pNewUnit)
{
	m_eMissionAIType = eNewMissionAI;

	if (pNewPlot != NULL)
	{
		m_iMissionAIX = pNewPlot->getX_INLINE();
		m_iMissionAIY = pNewPlot->getY_INLINE();
	}
	else
	{
		m_iMissionAIX = INVALID_PLOT_COORD;
		m_iMissionAIY = INVALID_PLOT_COORD;
	}

	if (pNewUnit != NULL)
	{
		m_missionAIUnit = pNewUnit->getIDInfo();
	}
	else
	{
		m_missionAIUnit.reset();
	}
}


CvUnit* CvSelectionGroupAI::AI_getMissionAIUnit()
{
	return getUnit(m_missionAIUnit);
}

bool CvSelectionGroupAI::AI_isFull()
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;

	if (getNumUnits() > 0)
	{
		UnitAITypes eUnitAI = getHeadUnitAI();
		// do two passes, the first pass, we ignore units with speical cargo
		int iSpecialCargoCount = 0;
		int iCargoCount = 0;

		// first pass, count but ignore special cargo units
		pUnitNode = headUnitNode();

		while (pUnitNode != NULL)
		{
			pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = nextUnitNode(pUnitNode);
			if (pLoopUnit != NULL && pLoopUnit->AI_getUnitAIType() == eUnitAI)
			{
				if (pLoopUnit->cargoSpace() > 0)
				{
					iCargoCount++;
				}

				if (pLoopUnit->specialCargo() != NO_SPECIALUNIT)
				{
					iSpecialCargoCount++;
				}
				else if (!(pLoopUnit->isFull()))
				{
					return false;
				}
			}
		}

		// if every unit in the group has special cargo, then check those, otherwise, consider ourselves full
		if (iSpecialCargoCount >= iCargoCount)
		{
			pUnitNode = headUnitNode();
			while (pUnitNode != NULL)
			{
				pLoopUnit = ::getUnit(pUnitNode->m_data);
				pUnitNode = nextUnitNode(pUnitNode);

				if (pLoopUnit != NULL && pLoopUnit->AI_getUnitAIType() == eUnitAI)
				{
					if (!(pLoopUnit->isFull()))
					{
						return false;
					}
				}
			}
		}

		return true;
	}

	return false;
}


bool CvSelectionGroupAI::AI_launchAssault(CvPlot* pTargetCityPlot)
{
	std::multimap<int, CvUnit*, std::greater<int> > units;
	std::multimap<int, CvUnit*, std::greater<int> >::iterator units_it;

	CLLNode<IDInfo>* pUnitNode = plot()->headUnitNode();
	CvUnit* pLoopUnit;

    while (pUnitNode != NULL)
    {
		pLoopUnit = plot()->getUnitNodeLoop(pUnitNode);

        if (pLoopUnit != NULL && pLoopUnit->isCargo())
        {
            if (pLoopUnit->getTransportUnit()->getGroup() == this)
            {
                int iValue = pLoopUnit->baseCombatStr();
                if (pLoopUnit->canAttack())
                {
                    iValue *= 10;
                }
                iValue *= 100;

                units.insert(std::make_pair(iValue, pLoopUnit));
            }
        }
    }

    if (units.empty())
    {
        return false;
    }

    bool bAction = false;
    for (units_it = units.begin(); units_it != units.end(); ++units_it)
    {
        pLoopUnit = units_it->second;
		if (pLoopUnit->canMove() && pLoopUnit->canAttack())
		{
//			if (pLoopUnit->AI_attackFromTransport(NULL, 40, 80))
//			{
//			    bAction = true;
//			}
            int iPriority = 41;
            pLoopUnit->AI_setMovePriority(iPriority);
		}
    }
//    for (units_it = units.begin(); units_it != units.end(); ++units_it)
//    {
//        pLoopUnit = units_it->second;
//        if (pLoopUnit->canMove())
//        {
//            if (pLoopUnit->AI_moveFromTransport(NULL))
//            {
//                bAction = true;
//            }
//        }
//    }
//    for (units_it = units.begin(); units_it != units.end(); ++units_it)
//    {
//        pLoopUnit = units_it->second;
//		if (pLoopUnit->canMove() && pLoopUnit->canAttack())
//		{
//			if (pLoopUnit->AI_attackFromTransport(NULL, 0, 100))
//			{
//			    bAction = true;
//			}
//		}
//    }
    if (bAction)
    {
	    //pushMission(MISSION_SKIP);
	    return true;
    }

    return false;

}

void CvSelectionGroupAI::AI_groupBombard()
{
 	CLLNode<IDInfo>* pEntityNode = headUnitNode();
	CvUnit* pLoopUnit = NULL;

	while (pEntityNode != NULL)
	{
		pLoopUnit = ::getUnit(pEntityNode->m_data);
		pEntityNode = nextUnitNode(pEntityNode);

		if (pLoopUnit != NULL && pLoopUnit->canBombard(plot()))
		{
		    pLoopUnit->bombard();
		}
	}
}

// Erik: I've changed this function to return the total amount of yields stored
// rather than the amount of treasure since that wasn't used anyway
int CvSelectionGroupAI::AI_getYieldsLoaded(short* piYields) const
{
	FAssert(piYields != NULL);

	int iAmount = 0;

	CLinkList<IDInfo> unitList;
	buildCargoUnitList(unitList);

	CLLNode<IDInfo>* pUnitNode = unitList.head();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = unitList.next(pUnitNode);

		// Should not be possible, but let's add this for safety
		if (pLoopUnit == NULL)
			continue;

		if (pLoopUnit->getYieldStored() > 0)
		{
			if (!pLoopUnit->getUnitInfo().isTreasure() && pLoopUnit->getYield() != NO_YIELD)
			{
				piYields[pLoopUnit->getYield()] += pLoopUnit->getYieldStored();
				iAmount += pLoopUnit->getYieldStored();
			}
		}
	}

	return iAmount;
}

int CvSelectionGroupAI::getPartialYieldSpace(YieldTypes eYield) const
{
	int iSpace = 0;
	CLinkList<IDInfo> unitList;
	buildCargoUnitList(unitList);
	CLLNode<IDInfo>* pUnitNode = unitList.head();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = unitList.next(pUnitNode);
		if (pLoopUnit != NULL && pLoopUnit->getYield() != NO_YIELD && !pLoopUnit->getUnitInfo().isTreasure() && (eYield == NO_YIELD || pLoopUnit->getYield() == eYield))
		{
			iSpace += std::max(0, GC.getGameINLINE().getCargoYieldCapacity() - pLoopUnit->getYieldStored());
		}
	}
	return iSpace;
}

// a detour only counts as worth it if at least this share of a slot is missing in a full transport's partly filled slots
static const int WTP_DETOUR_MIN_SLOT_PERCENT = 20;
// a detour of a transport to load more is only worth it if it has a free slot, or if the yields that are available on the detour can fill at
// least 20% of a slot (of the game speed dependent capacity) in total in its partly filled slots: a single slot that needs less does not
// justify a detour, several slots that are all filled further by the detour do
bool CvSelectionGroupAI::isDetourWorthwhile(const int* aiAvailable) const
{
	if (!isFull())
	{
		return true;
	}
	int iFillable = 0;
	for (YieldTypes eYield = FIRST_YIELD; eYield < NUM_YIELD_TYPES; ++eYield)
	{
		if (aiAvailable[eYield] > 0)
		{
			iFillable += std::min(aiAvailable[eYield], getPartialYieldSpace(eYield));
		}
	}
	return iFillable * 100 >= WTP_DETOUR_MIN_SLOT_PERCENT * GC.getGameINLINE().getCargoYieldCapacity();
}

int CvSelectionGroupAI::getFreeSlotCount() const
{
	int iFreeSlots = 0;
	CLLNode<IDInfo>* pFreeNode = headUnitNode();
	while (pFreeNode != NULL)
	{
		CvUnit* const pFreeUnit = ::getUnit(pFreeNode->m_data);
		pFreeNode = nextUnitNode(pFreeNode);
		if (pFreeUnit != NULL && !pFreeUnit->isCargo() && pFreeUnit->cargoSpace() > pFreeUnit->getCargo())
		{
			iFreeSlots += pFreeUnit->cargoSpace() - pFreeUnit->getCargo();
		}
	}
	return iFreeSlots;
}

bool CvSelectionGroupAI::canLoadYieldHere(YieldTypes eYield) const
{
	CLLNode<IDInfo>* pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);
		if (pLoopUnit != NULL && pLoopUnit->canLoadYield(plot(), eYield, false))
		{
			return true;
		}
	}
	return false;
}

void CvSelectionGroupAI::processTradeRoute(CvTradeRoute* pRoute, std::map<IDInfo, int>& cityValues, std::vector<CvTradeRoute*>& routes, std::vector<int>& routeValues, std::vector<bool>& yieldsDelivered, std::vector<bool>& yieldsToUnload)
{
	routes.push_back(pRoute);
	routeValues.push_back(0);

	yieldsDelivered[pRoute->getYield()] = true;
	CvCity* pPlotCity = plot()->getPlotCity();

	if (pPlotCity != NULL && ::getCity(pRoute->getDestinationCity()) == pPlotCity)
	{
		yieldsToUnload[pRoute->getYield()] = true;
	}

	cityValues[pRoute->getSourceCity()] = 0;
	cityValues[pRoute->getDestinationCity()] = 0;
}

// WTP: a human player's fully automated transport (Automate Transport) fills free cargo slots with yields for colonies that lie on
// its way, and with mixed cargo it serves the nearest colony first. Set to false to get the old behavior (one destination per trip).
static const bool WTP_TRADE_ROUTE_FILL_HOLD = true;
// a colony counts as on the way if the trip over it takes at most this many turns more than the direct trip
static const int WTP_FILL_HOLD_MAX_DETOUR_TURNS = 2;
// WTP: pick-up stop: with free cargo slots the transport stops at a colony on its way that has yields for its destination, if it can load at least
// a quarter of a cargo slot (game speed dependent: the capacity of a slot is 100 on the normal speed, 200 on epic)
static const int WTP_PICKUP_STOP_MIN_SLOT_DIVISOR = 4;

// WTP timing: a path search of the trade routes of a transport, with its own timing slot (from the position of the transport / from colony to colony)
static bool WTP_timedPath(const CvSelectionGroupAI* pGroup, WtpTiming::Slot eSlot, const CvPlot* pFromPlot, const CvPlot* pToPlot, int iFlags, bool bReuse, int* piTurns = NULL)
{
	WtpTiming::Scope wtpPathTimer(eSlot);
	return pGroup->generatePath(pFromPlot, pToPlot, iFlags, bReuse, piTurns);
}

// WTP: the path of a transport of this unit type from a source city to a destination city, kept for the turn.
// Every transport of every yield of every route asked for the same long coastal paths again and again.
static bool WTP_getRoutePathCached(CvSelectionGroupAI* pGroup, const CvCity* pSourceCity, const CvCity* pDestinationCity, int iFlags, bool bIgnoreDanger, int* piTurns)
{
	static int iCacheTurn = -1;
	static std::map<std::pair<std::pair<int, int>, std::pair<int, int> >, std::pair<bool, int> > aRoutePaths;
	if (iCacheTurn != GC.getGameINLINE().getGameTurn())
	{
		iCacheTurn = GC.getGameINLINE().getGameTurn();
		aRoutePaths.clear();
	}
	const std::pair<std::pair<int, int>, std::pair<int, int> > kRouteKey(
		std::make_pair(((int)pGroup->getHeadUnit()->getUnitType() * 2 + (bIgnoreDanger ? 1 : 0)) * MAX_PLAYERS + pDestinationCity->getOwnerINLINE(), (int)pSourceCity->getOwnerINLINE()),
		std::make_pair(pSourceCity->getID(), pDestinationCity->getID()));
	std::map<std::pair<std::pair<int, int>, std::pair<int, int> >, std::pair<bool, int> >::const_iterator itRoute = aRoutePaths.find(kRouteKey);
	if (itRoute != aRoutePaths.end())
	{
		*piTurns = itRoute->second.second;
		return itRoute->second.first;
	}
	const bool bOk = WTP_timedPath(pGroup, WtpTiming::SLOT_TR_PATH_ROUTE, pSourceCity->plot(), pDestinationCity->plot(), iFlags, true, piTurns);
	aRoutePaths[kRouteKey] = std::make_pair(bOk, *piTurns);
	return bOk;
}

// ---------------------------------------------------------------------------------------------------------------------------------
// WTP: urgency of the trade routes of a human player's automated transports (Automate Transport and the assigned routes).
// The next job of a transport is not the nearest one any more but the most urgent one, the way only decides between similar jobs:
//  - a colony that needs a good and has none (its production stops) is served before one that imports the same good but has enough of it;
//    of several colonies in need the one that loses the more valuable production (consumption of the raw material x value of what is made of it) comes first
//  - imports count more than exports (3 : 1)
//  - an export is the more urgent the fuller the store of the colony is and the more could be fetched; raw materials before finished goods
//  - the transports know of each other: what another transport is bringing to a colony or is on its way to fetch (its orders) is subtracted
//    A transport that is still on its way to fetch goods loses the job to one that gets there at least WTP_URGENCY_TAKEOVER_TURNS turns earlier (goods on board are never redistributed)
// The AI players keep their old values.
static const bool WTP_TRADE_ROUTE_URGENCY = true;
// an empty transport does not set out for less than this part of a slot (of 200: 50), however urgent: a trip like that would not even cover what the colony
// uses in a turn or two. A job that has waited for the aging time is served anyway, and a transport with cargo takes small amounts on its way.
static const int WTP_URGENCY_MIN_TRIP_SLOT_DIVISOR = 4;
static const int WTP_URGENCY_TIER = 100000; // one level of urgency (0..3)
static const int WTP_URGENCY_MAGNITUDE = 39999; // the grading inside of a level (value of the goods, amount)
static const int WTP_URGENCY_RAW_BONUS = 40000; // an exported raw material is graded above every finished good of the same level
static const int WTP_URGENCY_DISTANCE_PERCENT = 8; // per turn of the way: the value is divided by 1 + 8% of the turns

// Aging: a job that waits long gets more urgent, so that a colony that is always less urgent than the others is served in the end (with too few transports). The colonies are usually
// 1-2 turns apart, so the levels rise fast: +1 level after WTP_URGENCY_AGING_TURNS turns without a delivery (import) or a pick-up (export) of the good, +2 after twice that.
static const int WTP_URGENCY_AGING_TURNS = 3;

// the turn of the last delivery (side 0) or pick-up (side 1) of a good at a colony by a transport of the player (not saved: after loading a savegame everything starts new)
static std::map<std::pair<std::pair<int, int>, int>, int>& wtpServedTurns()
{
	static std::map<std::pair<std::pair<int, int>, int>, int> aiServed;
	return aiServed;
}

static void wtpNoteServed(const CvCity* pCity, YieldTypes eYield, int iSide)
{
	if (pCity != NULL && eYield != NO_YIELD)
	{
		wtpServedTurns()[std::make_pair(std::make_pair((int)pCity->getOwnerINLINE(), pCity->getID()), (int)eYield * 2 + iSide)] = GC.getGameINLINE().getGameTurn();
	}
}

// the levels that a job has gained by waiting (0..2); a job that is seen for the first time starts to wait now
static int wtpAgingLevels(const CvCity* pCity, YieldTypes eYield, int iSide)
{
	std::map<std::pair<std::pair<int, int>, int>, int>& aiServed = wtpServedTurns();
	const std::pair<std::pair<int, int>, int> kKey(std::make_pair((int)pCity->getOwnerINLINE(), pCity->getID()), (int)eYield * 2 + iSide);
	std::map<std::pair<std::pair<int, int>, int>, int>::const_iterator it = aiServed.find(kKey);
	if (it == aiServed.end())
	{
		aiServed[kKey] = GC.getGameINLINE().getGameTurn();
		return 0;
	}
	return std::min(2, std::max(0, GC.getGameINLINE().getGameTurn() - it->second) / WTP_URGENCY_AGING_TURNS);
}

// a nearer transport takes over the job of one that is still on its way to fetch the goods if it arrives at least this many turns earlier
static const int WTP_URGENCY_TAKEOVER_TURNS = 2;

struct WtpTradeClaims
{
	struct Claim
	{
		IDInfo kCity;
		int iYield;
		int iAmount;
		int iTurns; // 0: the goods are on board of the other transport (never taken over); otherwise its turns to the source colony
	};
	std::vector<Claim> aIncoming; // what other transports bring to a colony (loaded, or on their way to fetch it)
	std::vector<Claim> aOutgoing; // what other transports are on their way to fetch in a colony
	// the turns that the transport that asks needs to the source colony of the job it looks at: a claim of a transport that needs at least WTP_URGENCY_TAKEOVER_TURNS
	// more is not counted (this transport would be there first). The default counts every claim.
	int iMyTurns;

	WtpTradeClaims() : iMyTurns(1000) {}

	static int sum(const std::vector<Claim>& aClaims, const IDInfo& kCity, YieldTypes eYield, int iMyTurns)
	{
		int iSum = 0;
		for (uint i = 0; i < aClaims.size(); ++i)
		{
			if (aClaims[i].kCity == kCity && aClaims[i].iYield == (int)eYield && (aClaims[i].iTurns <= 0 || aClaims[i].iTurns < iMyTurns + WTP_URGENCY_TAKEOVER_TURNS))
			{
				iSum += aClaims[i].iAmount;
			}
		}
		return iSum;
	}
	int incoming(const IDInfo& kCity, YieldTypes eYield) const { return sum(aIncoming, kCity, eYield, iMyTurns); }
	int outgoing(const IDInfo& kCity, YieldTypes eYield) const { return sum(aOutgoing, kCity, eYield, iMyTurns); }
};

// the orders of the other automated transports of the player (what they carry to which colony, what they will fetch where): rebuilt at every decision of a transport,
// so that the transports that decide one after the other see each other
static void wtpCollectTradeClaims(const CvSelectionGroupAI* pSelf, WtpTradeClaims& kClaims)
{
	const CvPlayer& kOwner = GET_PLAYER(pSelf->getOwnerINLINE());
	const int iSlot = GC.getGameINLINE().getCargoYieldCapacity();
	int iLoop;
	for (CvSelectionGroup* pLoopGroup = kOwner.firstSelectionGroup(&iLoop); pLoopGroup != NULL; pLoopGroup = kOwner.nextSelectionGroup(&iLoop))
	{
		if (pLoopGroup == pSelf)
		{
			continue;
		}
		const CvSelectionGroupAI* pOther = static_cast<const CvSelectionGroupAI*>(pLoopGroup);
		// (only transports that are still automated: the orders of a group that was taken over are not rebuilt any more)
		if (pOther->getAutomateType() != AUTOMATE_TRANSPORT_FULL && pOther->getAutomateType() != AUTOMATE_TRANSPORT_ROUTES)
		{
			continue;
		}
		const std::vector<CvSelectionGroupAI::WtpTradeOrder>& aOrders = pOther->getTradeOrders();
		if (aOrders.empty())
		{
			continue;
		}
		short aiLoaded[NUM_YIELD_TYPES];
		std::fill(aiLoaded, aiLoaded + NUM_YIELD_TYPES, 0);
		pOther->AI_getYieldsLoaded(aiLoaded);
		for (uint i = 0; i < aOrders.size(); ++i)
		{
			const CvSelectionGroupAI::WtpTradeOrder& kOrder = aOrders[i];
			if (kOrder.eYield < 0 || kOrder.eYield >= NUM_YIELD_TYPES)
			{
				continue;
			}
			int iAmount = 0;
			if (kOrder.bLoaded)
			{
				iAmount = aiLoaded[kOrder.eYield];
			}
			else
			{
				// (a transport on its way to fetch: at most the load of a cargo slot of what the colony has to give)
				const CvCity* pSource = ::getCity(kOrder.kSource);
				if (pSource != NULL)
				{
					iAmount = std::min(iSlot, std::max(0, pSource->getYieldStored(kOrder.eYield) - pSource->getAutoMaintainThreshold(kOrder.eYield)));
				}
				if (iAmount > 0)
				{
					WtpTradeClaims::Claim kOut;
					kOut.kCity = kOrder.kSource;
					kOut.iYield = (int)kOrder.eYield;
					kOut.iAmount = iAmount;
					kOut.iTurns = std::max(1, kOrder.iTurns);
					kClaims.aOutgoing.push_back(kOut);
				}
			}
			if (iAmount > 0)
			{
				WtpTradeClaims::Claim kIn;
				kIn.kCity = kOrder.kDestination;
				kIn.iYield = (int)kOrder.eYield;
				kIn.iAmount = iAmount;
				kIn.iTurns = kOrder.bLoaded ? 0 : std::max(1, kOrder.iTurns);
				kClaims.aIncoming.push_back(kIn);
			}
		}
	}
}

// a raw material: no profession makes it from other goods (cached)
static bool wtpIsRawYield(YieldTypes eYield)
{
	static std::vector<char> aiRaw; // 0: not known, 1: raw, 2: finished
	if (aiRaw.empty())
	{
		aiRaw.assign(NUM_YIELD_TYPES, 1);
		for (int iProfession = 0; iProfession < GC.getNumProfessionInfos(); ++iProfession)
		{
			const CvProfessionInfo& kProfession = GC.getProfessionInfo((ProfessionTypes)iProfession);
			if (kProfession.getNumYieldsConsumed() > 0)
			{
				for (int j = 0; j < kProfession.getNumYieldsProduced(); ++j)
				{
					const int iProduced = kProfession.getYieldsProduced(j);
					if (iProduced >= 0 && iProduced < NUM_YIELD_TYPES)
					{
						aiRaw[iProduced] = 2;
					}
				}
			}
		}
	}
	return aiRaw[eYield] == 1;
}

// what a unit of the good is worth (the price in Europe, 1 for goods that are not traded)
static int wtpUrgencyYieldValue(const CvPlayerAI& kOwner, YieldTypes eYield)
{
	if (eYield < 0 || eYield >= NUM_YIELD_TYPES || !GC.getYieldInfo(eYield).isCargo() || kOwner.getParent() == NO_PLAYER)
	{
		return 1;
	}
	// (the price list of the king)
	return std::max(1, GET_PLAYER(kOwner.getParent()).getYieldBuyPrice(eYield));
}

// what a colony makes of a unit of this raw material is worth (the best of the professions that consume it, cached per turn)
static int wtpUrgencyProductValue(const CvPlayerAI& kOwner, YieldTypes eYield)
{
	static int iCacheTurn = -1;
	static std::map<std::pair<int, int>, int> aiValues;
	if (iCacheTurn != GC.getGameINLINE().getGameTurn())
	{
		iCacheTurn = GC.getGameINLINE().getGameTurn();
		aiValues.clear();
	}
	const std::pair<int, int> kKey((int)kOwner.getID(), (int)eYield);
	std::map<std::pair<int, int>, int>::const_iterator it = aiValues.find(kKey);
	if (it != aiValues.end())
	{
		return it->second;
	}
	int iBest = 0;
	for (int iProfession = 0; iProfession < GC.getNumProfessionInfos(); ++iProfession)
	{
		const CvProfessionInfo& kProfession = GC.getProfessionInfo((ProfessionTypes)iProfession);
		bool bConsumes = false;
		for (int j = 0; j < kProfession.getNumYieldsConsumed(); ++j)
		{
			if (kProfession.getYieldsConsumed(j) == eYield)
			{
				bConsumes = true;
			}
		}
		if (bConsumes)
		{
			for (int j = 0; j < kProfession.getNumYieldsProduced(); ++j)
			{
				iBest = std::max(iBest, wtpUrgencyYieldValue(kOwner, (YieldTypes)kProfession.getYieldsProduced(j)));
			}
		}
	}
	if (iBest <= 0)
	{
		iBest = wtpUrgencyYieldValue(kOwner, eYield);
	}
	aiValues[kKey] = iBest;
	return iBest;
}

// what the production of a colony consumes of a good per turn (cached per turn)
static int wtpUrgencyConsumption(const CvCity* pCity, YieldTypes eYield)
{
	static int iCacheTurn = -1;
	static std::map<std::pair<std::pair<int, int>, int>, int> aiConsumed;
	if (iCacheTurn != GC.getGameINLINE().getGameTurn())
	{
		iCacheTurn = GC.getGameINLINE().getGameTurn();
		aiConsumed.clear();
	}
	const std::pair<std::pair<int, int>, int> kKey(std::make_pair((int)pCity->getOwnerINLINE(), pCity->getID()), (int)eYield);
	std::map<std::pair<std::pair<int, int>, int>, int>::const_iterator it = aiConsumed.find(kKey);
	if (it != aiConsumed.end())
	{
		return it->second;
	}
	const int iConsumed = std::max(0, pCity->getRawYieldConsumed(eYield));
	aiConsumed[kKey] = iConsumed;
	return iConsumed;
}

// the urgency of a delivery of iAmount of a good to a colony: 0..3 levels (3: the production of the colony is short of it now, 2: it lasts only a few turns, or the
// colony needs it for its construction, 1: the store is below the level the player wants to keep, 0: it would only be stored) x WTP_URGENCY_TIER, plus the grading
// inside of the level: the value of what the colony cannot produce without it, the larger it is the more urgent. Colonies that cannot be found: 0.
static int wtpImportUrgency(const CvPlayerAI& kOwner, const IDInfo& kDestination, YieldTypes eYield, int iAmount, const WtpTradeClaims& kClaims)
{
	const CvCity* pCity = ::getCity(kDestination);
	if (pCity == NULL || iAmount <= 0)
	{
		return 0;
	}
	// what is there and what the other transports bring
	const int iStock = pCity->getYieldStored(eYield) + kClaims.incoming(kDestination, eYield);
	const int iConsumed = wtpUrgencyConsumption(pCity, eYield);
	const int iNeeded = pCity->getProductionNeeded(eYield);
	const int iMaintain = pCity->getAutoMaintainThreshold(eYield);
	int iTier = 0;
	int iMagnitude = 0;
	if (iConsumed > 0)
	{
		const int iUnit = wtpUrgencyProductValue(kOwner, eYield);
		if (iStock < iConsumed)
		{
			iTier = 3;
		}
		else if (iStock < 3 * iConsumed)
		{
			iTier = 2;
		}
		else
		{
			iTier = 1;
		}
		// the value of the production per turn that depends on it (what the delivery can save: at most what is missing for the next turn, in the lower levels the consumption)
		const int iShortage = std::max(0, iConsumed - iStock);
		const int iAtStake = (iTier == 3) ? iShortage : iConsumed;
		iMagnitude = iUnit * std::min(iAtStake, iAmount) + iUnit * iConsumed / 4;
	}
	if (iNeeded > 0 && iStock < iNeeded)
	{
		// construction: the missing goods of the building or unit in production
		iTier = std::max(iTier, 2);
		iMagnitude += wtpUrgencyYieldValue(kOwner, eYield) * std::min(iAmount, iNeeded - iStock) / 4;
	}
	if (iTier == 0)
	{
		if (iMaintain > 0 && iStock < iMaintain)
		{
			iTier = 1;
			iMagnitude = wtpUrgencyYieldValue(kOwner, eYield) * std::min(iAmount, iMaintain - iStock) / 10;
		}
		else
		{
			iMagnitude = wtpUrgencyYieldValue(kOwner, eYield) * iAmount / 50;
		}
	}
	// (waiting: more urgent by levels, at most the highest)
	iTier = std::min(3, iTier + wtpAgingLevels(pCity, eYield, 0));
	return iTier * WTP_URGENCY_TIER + std::min(WTP_URGENCY_MAGNITUDE, iMagnitude);
}

// the urgency of fetching iAmount of a good from a colony: the fuller its store, the more urgent (above 85 percent goods are lost), then the amount that could be
// fetched; raw materials before finished goods. The amounts that other transports are on their way to fetch are subtracted.
static int wtpExportUrgency(const CvPlayerAI& kOwner, const IDInfo& kSource, YieldTypes eYield, int iAmount, const WtpTradeClaims& kClaims)
{
	const CvCity* pCity = ::getCity(kSource);
	if (pCity == NULL || iAmount <= 0)
	{
		return 0;
	}
	const int iCapacity = std::max(1, pCity->getMaxYieldCapacity());
	const int iStock = std::max(0, pCity->getYieldStored(eYield) - kClaims.outgoing(kSource, eYield));
	const int iTotal = pCity->getTotalYieldStored();
	const int iFill = std::max((100 * iStock) / iCapacity, (100 * iTotal) / iCapacity);
	int iTier = 0;
	if (iFill >= 85)
	{
		iTier = 2;
	}
	else if (iFill >= 50)
	{
		iTier = 1;
	}
	// (waiting: more urgent by levels, at most the highest)
	iTier = std::min(3, iTier + wtpAgingLevels(pCity, eYield, 1));
	// the amount that could be fetched (of 200: a load of two slots) and how full the store is
	int iMagnitude = std::min(iAmount, 400) * 50 + iFill * 100;
	iMagnitude = std::min(WTP_URGENCY_MAGNITUDE, iMagnitude);
	if (wtpIsRawYield(eYield))
	{
		iMagnitude += WTP_URGENCY_RAW_BONUS;
	}
	return iTier * WTP_URGENCY_TIER + iMagnitude;
}

// the value of a route: imports count three times, exports once
static int wtpUrgencyRouteValue(const CvPlayerAI& kOwner, const CvTradeRoute* pRoute, int iAmount, const WtpTradeClaims& kClaims)
{
	const int iImport = wtpImportUrgency(kOwner, pRoute->getDestinationCity(), pRoute->getYield(), iAmount, kClaims);
	const int iExport = wtpExportUrgency(kOwner, pRoute->getSourceCity(), pRoute->getYield(), iAmount, kClaims);
	return (3 * iImport + iExport) / 4;
}

// WTP: rebuilds the orders of the transport after it has decided where to go (and loaded here): every yield on board is brought from
// its source to its destination colony; an empty transport on its way to a source colony will fetch the yields of the best route from there
void CvSelectionGroupAI::updateTradeOrders(const std::vector<CvTradeRoute*>& routes, const std::vector<int>& routeValues, const IDInfo& kBestDestination, int iTurnsToBest)
{
	std::vector<WtpTradeOrder> aNewOrders;
	const CvCity* pPlotCity = plot()->getPlotCity();

	short aiLoaded[NUM_YIELD_TYPES];
	std::fill(aiLoaded, aiLoaded + NUM_YIELD_TYPES, 0);
	AI_getYieldsLoaded(aiLoaded);

	bool bAnyLoaded = false;
	for (int iYield = 0; iYield < NUM_YIELD_TYPES; ++iYield)
	{
		if (aiLoaded[iYield] <= 0)
		{
			continue;
		}
		bAnyLoaded = true;
		const YieldTypes eYield = (YieldTypes)iYield;

		// an order that is still valid is kept (the yield was loaded earlier)
		bool bKept = false;
		for (uint i = 0; i < m_aTradeOrders.size(); ++i)
		{
			const WtpTradeOrder& kOld = m_aTradeOrders[i];
			if (kOld.eYield == eYield && ::getCity(kOld.kDestination) != pPlotCity && ::getCity(kOld.kDestination) != NULL)
			{
				WtpTradeOrder kOrder = kOld;
				kOrder.bLoaded = true;
				aNewOrders.push_back(kOrder);
				bKept = true;
				break;
			}
		}
		if (bKept)
		{
			continue;
		}

		// new cargo: the route of this yield from here (the best destination first), else any route to the best destination
		int iBestRoute = -1;
		int iBestPriority = 0;
		for (uint i = 0; i < routes.size(); ++i)
		{
			if (routes[i]->getYield() != eYield || ::getCity(routes[i]->getDestinationCity()) == NULL || ::getCity(routes[i]->getDestinationCity()) == pPlotCity)
			{
				continue;
			}
			const bool bFromHere = (::getCity(routes[i]->getSourceCity()) == pPlotCity);
			const bool bToBest = (routes[i]->getDestinationCity() == kBestDestination);
			const int iPriority = (bFromHere ? 2 : 0) + (bToBest ? 4 : 0) + (bFromHere || bToBest ? 1 : 0);
			if (iPriority > iBestPriority || (iPriority == iBestPriority && iBestRoute >= 0 && routeValues[i] > routeValues[iBestRoute]))
			{
				iBestPriority = iPriority;
				iBestRoute = i;
			}
		}
		if (iBestRoute >= 0)
		{
			WtpTradeOrder kOrder;
			kOrder.eYield = eYield;
			kOrder.kSource = routes[iBestRoute]->getSourceCity();
			kOrder.kDestination = routes[iBestRoute]->getDestinationCity();
			kOrder.bLoaded = true;
			aNewOrders.push_back(kOrder);
		}
	}

	if (!bAnyLoaded && kBestDestination.eOwner != NO_PLAYER)
	{
		// empty: on its way to fetch the yields of the best route that starts in the destination colony
		int iBestRoute = -1;
		for (uint i = 0; i < routes.size(); ++i)
		{
			if (routes[i]->getSourceCity() == kBestDestination && routeValues[i] > 0 && (iBestRoute < 0 || routeValues[i] > routeValues[iBestRoute]))
			{
				iBestRoute = i;
			}
		}
		if (iBestRoute >= 0)
		{
			// the goods of this route pair, the most valuable first; no more of them than the transport has cargo slots (every good takes at least
			// one slot: the orders of an empty transport are shown in its tooltip, a list of all goods of the pair said more than it can carry)
			std::vector<int> aFetch;
			for (uint i = 0; i < routes.size(); ++i)
			{
				if (routes[i]->getSourceCity() == kBestDestination && routes[i]->getDestinationCity() == routes[iBestRoute]->getDestinationCity() && routeValues[i] > 0)
				{
					aFetch.push_back(i);
				}
			}
			const CvUnit* pHeadFetch = getHeadUnit();
			const uint iMaxFetch = std::max(1, (pHeadFetch != NULL) ? (int)pHeadFetch->cargoSpace() : 1);
			for (uint iPick = 0; iPick < iMaxFetch && !aFetch.empty(); ++iPick)
			{
				uint iBestIndex = 0;
				for (uint j = 1; j < aFetch.size(); ++j)
				{
					if (routeValues[aFetch[j]] > routeValues[aFetch[iBestIndex]])
					{
						iBestIndex = j;
					}
				}
				const int i = aFetch[iBestIndex];
				aFetch.erase(aFetch.begin() + iBestIndex);
				WtpTradeOrder kOrder;
				kOrder.eYield = routes[i]->getYield();
				kOrder.kSource = routes[i]->getSourceCity();
				kOrder.kDestination = routes[i]->getDestinationCity();
				kOrder.bLoaded = false;
				kOrder.iTurns = iTurnsToBest;
				aNewOrders.push_back(kOrder);
			}
		}
	}

	m_aTradeOrders = aNewOrders;
}

bool CvSelectionGroupAI::AI_tradeRoutes()
{
	WtpTiming::Scope wtpTimer(WtpTiming::SLOT_TRADE_ROUTES);
	PROFILE_FUNC();

	m_kTooltipStop = IDInfo();
	m_bTooltipWaiting = false;
	m_aiTooltipStopYields.clear();
	WtpTiming::Lap wtpTradeLap(WtpTiming::SLOT_TR_SETUP); // WTP: timing log of the parts of this function (each part ends where the next one begins)

	const IDInfo kEurope(getOwnerINLINE(), CvTradeRoute::EUROPE_CITY_ID);

	CvCity* pPlotCity = plot()->getPlotCity();
	CvPlayerAI& kOwner = GET_PLAYER(getOwnerINLINE());
	std::set<int>::iterator it;

	std::map<IDInfo, int> cityValues;
	std::map<IDInfo, std::pair<bool, int> > aGroupToDestPaths; // WTP: destination city -> (path from this group, turns)

	std::vector<CvTradeRoute*> routes;
	std::vector<int> routeValues;

	std::vector<bool> yieldsDelivered(NUM_YIELD_TYPES, false);
	std::vector<bool> yieldsToUnload(NUM_YIELD_TYPES, false);
	std::vector<int> yieldsOnBoard(NUM_YIELD_TYPES, false);

	// R&R mod, vetiarvind, max yield import limit - start
	const bool bIgnoreDanger = getIgnoreDangerStatus();
	// R&R mod, vetiarvind, max yield import limit - end

	// WTP: a human player's land transport with Automate Transport makes no trips of more than 10 turns (to the source
	// colony, from there to the destination, to its next destination)
	static const int LAND_TRANSPORT_MAX_TRIP_TURNS = 10;
	const bool bMaxTrip = isHuman() && getAutomateType() == AUTOMATE_TRANSPORT_FULL && getDomainType() == DOMAIN_LAND;
	// WTP: Automate Transport and the assigned routes (R) fill the hold and stop at colonies on the way
	const bool bFillHold = WTP_TRADE_ROUTE_FILL_HOLD && isHuman() && (getAutomateType() == AUTOMATE_TRANSPORT_FULL || getAutomateType() == AUTOMATE_TRANSPORT_ROUTES);
	// WTP: the most urgent job first (see wtpImportUrgency), with the orders of the other transports of the player known
	const bool bUrgency = WTP_TRADE_ROUTE_URGENCY && bFillHold;
	WtpTradeClaims kClaims;
	if (bUrgency)
	{
		wtpCollectTradeClaims(this, kClaims);
	}

	// Erik: We need to determine if we're dealing with a coastal transport
	bool bCoastalTransport = false;
	CLLNode<IDInfo>* pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (pLoopUnit != NULL)
		{
			UnitAITypes aiType = pLoopUnit->AI_getUnitAIType();

			if (aiType == UNITAI_TRANSPORT_COAST)
			{
				bCoastalTransport = true;
				break;
			}
		}
	}

	if (!isHuman() || (getAutomateType() == AUTOMATE_TRANSPORT_FULL))
	{
		std::vector<CvTradeRoute*> aiRoutes;
		kOwner.getTradeRoutes(aiRoutes);
		for (uint i = 0; i < aiRoutes.size(); ++i)
		{
			CvTradeRoute* pRoute = aiRoutes[i];

			// transport feeder - start - Nightinggale
			CvCity* pDestinationCity = ::getCity(pRoute->getDestinationCity());
			if (pDestinationCity != NULL && pDestinationCity->isAutoImportStopped(pRoute->getYield()))
			{
				// ignore trade routes where destination is using feeder service and is full
				continue;
			}
			// transport feeder - end - Nightinggale

			// WTP: reserved and private routes are served only by the transports assigned to them
			if (pRoute->isPrivate() || (isHuman() && pRoute->isReserved()))
			{
				continue;
			}

			// traderoute fix - start - Nightinggale
			if (isHuman() && (pRoute->getDestinationCity().eOwner != getOwnerINLINE() || (pRoute->getDestinationCity() == kEurope)))
			{
				// humans can't transport to allied cities with fully automated transports
				// human transport can't go to Europe automatically
				continue;
			}
			// traderoute fix - end - Nightinggale

			// Erik: Coastal transports cannot have europe as their destination
			if (bCoastalTransport && (pRoute->getDestinationCity().eOwner != getOwnerINLINE() || (pRoute->getDestinationCity() == kEurope)))
				continue;

			CvCity* pSourceCity = ::getCity(pRoute->getSourceCity());
			CvArea* pSourceWaterArea = pSourceCity->waterArea();
			// R&R, vetiarvind, max trade capacity  - start
			const DomainTypes domainType = getDomainType();
			// R&R, vetiarvind, max trade capacity  - end

			if ((pSourceCity != NULL) && ((domainType != DOMAIN_SEA) || (pSourceWaterArea != NULL)))
			{
				int iSourceArea = (domainType == DOMAIN_SEA) ? pSourceWaterArea->getID() : pSourceCity->getArea();
				if (domainType == DOMAIN_SEA ? plot()->isAdjacentToArea(iSourceArea) : (iSourceArea == getArea()) ||
					domainType == DOMAIN_LAND && plot()->getTerrainType() == TERRAIN_LARGE_RIVERS && plot()->isAdjacentToArea(pSourceCity->getArea()))
				{
					if ((domainType == DOMAIN_SEA) || (pRoute->getDestinationCity() != kEurope))
					{
						processTradeRoute(pRoute, cityValues, routes, routeValues, yieldsDelivered, yieldsToUnload);
					}
				}
				// TODO: Need to path find if the area check fails like below
			}
		}
	}
	else //human or non-automate-full case: just uses the unit's routes but the same logic as above..can be refactored as a function
	{
		for (it = m_aTradeRoutes.begin(); it != m_aTradeRoutes.end(); ++it)
		{
			CvTradeRoute* pRoute = kOwner.getTradeRoute(*it);
			CvCity* pSourceCity = ::getCity(pRoute->getSourceCity());
			if (pSourceCity != NULL)
			{
				const DomainTypes domainType = getDomainType();

				CvArea* pSourceWaterArea = pSourceCity->waterArea();
				if (getDomainType() != DOMAIN_SEA || pSourceWaterArea != NULL) //land or good water..this if block is basically the same code as the AI_full_automate case
				{
					int iSourceArea = (getDomainType() == DOMAIN_SEA) ? pSourceWaterArea->getID() : pSourceCity->getArea();
					if (domainType == DOMAIN_SEA ? plot()->isAdjacentToArea(iSourceArea) : (iSourceArea == getArea()) ||
						domainType == DOMAIN_LAND && plot()->getTerrainType() == TERRAIN_LARGE_RIVERS && plot()->isAdjacentToArea(pSourceCity->getArea()))
					{
						if ((domainType == DOMAIN_SEA) || (pRoute->getDestinationCity() != kEurope))
						{
							processTradeRoute(pRoute, cityValues, routes, routeValues, yieldsDelivered, yieldsToUnload);
						}
					}
					else
					{
						// Due to the introduction of the large river feature, the area check may not be sufficient. This is the case
						// if the source city is in a different area, connected by river fords \ ferry stations
						const bool res = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pSourceCity->plot(), (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY), true);

						if (res)
						{
							processTradeRoute(pRoute, cityValues, routes, routeValues, yieldsDelivered, yieldsToUnload);
						}
						else
						{
							FAssertMsg(false, "Unexpected : Unit can't run trade route it's assigned to");
						}
					}

				}
			}
		}
	} // human or non-automate-full

	wtpTradeLap.next(WtpTiming::SLOT_TR_UNLOAD);
	if ((pPlotCity != NULL) && hasCargo())
	{
		std::vector<CvUnit*> units;

		//Unload everything which we should unload here, or can't unload anywhere...
		CLLNode<IDInfo>* pUnitNode = plot()->headUnitNode();
		while (pUnitNode != NULL)
		{
			CvUnit* pLoopUnit = plot()->getUnitNodeLoop(pUnitNode);

			if (pLoopUnit != NULL)
			{
				YieldTypes eYield = pLoopUnit->getYield();
				CvUnit* pTransport = pLoopUnit->getTransportUnit();

				if ((eYield != NO_YIELD) && pTransport != NULL && (yieldsToUnload[eYield] || !(yieldsDelivered[eYield])))
				{
					if (pTransport->getGroup() == this && pLoopUnit->canUnload())
					{
						units.push_back(pLoopUnit);
					}
				}
			}
		}

		for (uint i = 0; i < units.size(); ++i)
		{
			// R&R mod, vetiarvind, max yield import limit - start
			//units[i]->unload();
			unloadToCity(pPlotCity, units[i], UnloadMode::Force);
			// R&R mod, vetiarvind, max yield import limit - end
		}

		// It may happen that the destination has stopped importing the yield, if so search for
		// another nearby city that imports the yield. If that fails, force unload the yield
		// as a last resort if not a single city imports this yield so that we can free up
		// the storage space
		// Note that this is very rate since the presence of a port city in any given area
		// will act as a "sink" for excess yields of any type

	}

	wtpTradeLap.next(WtpTiming::SLOT_TR_VALUES);
	short aiYieldsLoaded[NUM_YIELD_TYPES];

	std::fill(aiYieldsLoaded, aiYieldsLoaded + NUM_YIELD_TYPES, 0);
	const bool bNoCargo = (AI_getYieldsLoaded(aiYieldsLoaded) == 0);

	if (!bNoCargo)
	{
		//We need to iterate over every destination city and see if we can unload.
		for (uint i = 0; i < routes.size(); ++i)
		{
			CvCity* pDestinationCity = ::getCity(routes[i]->getDestinationCity());
			if ((pDestinationCity != NULL) && (pDestinationCity != pPlotCity))
			{
				// R&R mod, vetiarvind, max yield import limit - start

				YieldTypes eYield = routes[i]->getYield();
				int yieldsToUnload = aiYieldsLoaded[eYield];
				// WTP: a private route unloads without import limit
				if(pDestinationCity != NULL && pDestinationCity->getMaxImportAmount(eYield) > 0 && !routes[i]->isPrivate())
				{
					int turnsToReach = 0;
					// WTP: the path to a destination city is searched once per call (several yields go to the same city)
					std::map<IDInfo, std::pair<bool, int> >::const_iterator itToDest = aGroupToDestPaths.find(routes[i]->getDestinationCity());
					if (itToDest != aGroupToDestPaths.end())
					{
						turnsToReach = itToDest->second.second;
					}
					else
					{
						const bool bToDestOk = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pDestinationCity->plot(), (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY), true, &turnsToReach);
						aGroupToDestPaths[routes[i]->getDestinationCity()] = std::make_pair(bToDestOk, turnsToReach);
					}
					yieldsToUnload = std::min(yieldsToUnload, estimateYieldsToLoad(pDestinationCity, 9999, eYield, turnsToReach, 0));
				}
				//int iRouteValue = kOwner.AI_transferYieldValue(routes[i]->getDestinationCity(), routes[i]->getYield(), aiYieldsLoaded[routes[i]->getYield()]);
				int iRouteValue = bUrgency ? wtpImportUrgency(kOwner, routes[i]->getDestinationCity(), routes[i]->getYield(), yieldsToUnload, kClaims)
					: kOwner.AI_transferYieldValue(routes[i]->getDestinationCity(), routes[i]->getYield(), yieldsToUnload);
				// R&R mod, vetiarvind, max yield import limit - end

				if (iRouteValue > 0)
				{
					cityValues[routes[i]->getDestinationCity()] += iRouteValue;
					routeValues[i] += iRouteValue;
				}
			}
		}
	}

	wtpTradeLap.next(WtpTiming::SLOT_TR_MAINLOOP);
	bool bNoRoute = true;
	std::map<int, std::pair<bool, int> > aSourcePaths; // WTP: source city ID -> (path from it to this group, turns)
	std::map<int, std::pair<bool, int> > aMaxTripSourcePaths; // WTP: source city ID -> (path from this group to it, turns), for the check of the maximum trip of land transports

	//We need to iterate over every source city, and see if there's anything which needs moving to the respective destination city.
	//We apply some bias to the city we are presently at, but not too much - sometimes empty runs need to be made...
	//Basically this looks at the entire NEXT trade run (source-city to dest-city), with some bias given towards
	//starting it from pPlotCity as sourceCity.
	//If we are carrying cargo, only count cities where we can unload.

	// WTP: an AI player has many routes, and every route with something to carry cost path searches (the AI's transports took up to half
	// of the waiting time between turns). The routes are ranked by their value without any path (the paths can only lower it), and only the
	// best WTP_AI_ROUTE_BATCH routes are evaluated with paths. The rest follows only if not a single one of the best routes is viable.
	static const uint WTP_AI_ROUTE_BATCH = 12;
	std::vector<bool> aRouteDeferred(routes.size(), false);
	bool bAnyDeferred = false;
	if (!isHuman() && routes.size() > WTP_AI_ROUTE_BATCH)
	{
		std::vector<std::pair<std::pair<int, int>, int> > aRank; // ((value, -distance), route index)
		for (uint i = 0; i < routes.size(); ++i)
		{
			CvCity* pRankSource = ::getCity(routes[i]->getSourceCity());
			if (pRankSource == NULL || !(bNoCargo || (cityValues[routes[i]->getSourceCity()] > 0)))
			{
				continue;
			}
			const int iRankAmount = pRankSource->getYieldStored(routes[i]->getYield()) - pRankSource->getAutoMaintainThreshold(routes[i]->getYield());
			if (iRankAmount <= 0)
			{
				continue;
			}
			const int iRankExport = kOwner.AI_transferYieldValue(routes[i]->getSourceCity(), routes[i]->getYield(), -iRankAmount);
			const int iRankImport = kOwner.AI_transferYieldValue(routes[i]->getDestinationCity(), routes[i]->getYield(), iRankAmount);
			const int iRankValue = (iRankExport + iRankImport + 2 * std::min(iRankExport, iRankImport)) / 4;
			aRank.push_back(std::make_pair(std::make_pair(iRankValue, -plotDistance(plot()->getX_INLINE(), plot()->getY_INLINE(), pRankSource->getX_INLINE(), pRankSource->getY_INLINE())), (int)i));
		}
		if (aRank.size() > WTP_AI_ROUTE_BATCH)
		{
			std::sort(aRank.begin(), aRank.end(), std::greater<std::pair<std::pair<int, int>, int> >());
			for (uint k = WTP_AI_ROUTE_BATCH; k < aRank.size(); ++k)
			{
				aRouteDeferred[aRank[k].second] = true;
			}
			bAnyDeferred = true;
		}
	}

	for (int iBatch = 0; iBatch < 2; ++iBatch)
	{
	if (iBatch == 1 && !(bAnyDeferred && bNoRoute && bNoCargo))
	{
		break;
	}
	for (uint i = 0; i < routes.size(); ++i)
	{
		if (aRouteDeferred[i] != (iBatch == 1))
		{
			continue;
		}
		CvCity* pSourceCity = ::getCity(routes[i]->getSourceCity());

		if ((pSourceCity != NULL) && (bNoCargo || (cityValues[routes[i]->getSourceCity()] > 0)))
		{
			CvCity* pDestinationCity = ::getCity(routes[i]->getDestinationCity());
			YieldTypes eYield = routes[i]->getYield();

			// transport feeder - start - Nightinggale
			//int iAmount = pSourceCity->getYieldStored(eYield) - pSourceCity->getMaintainLevel(eYield);
			int iAmount = pSourceCity->getYieldStored(eYield) - pSourceCity->getAutoMaintainThreshold(eYield);
			// transport feeder - end - Nightinggale
			if (bUrgency && pSourceCity != pPlotCity)
			{
				// WTP: what another transport is on its way to fetch there is no job for this one, unless this one is there at least 2 turns earlier (in a colony
				// the transport stands in it loads what is there)
				kClaims.iMyTurns = 1000;
				if (kClaims.outgoing(routes[i]->getSourceCity(), eYield) > 0)
				{
					int iMyTurns = 0;
					std::map<int, std::pair<bool, int> >::const_iterator itMyTurns = aSourcePaths.find(pSourceCity->getID());
					if (itMyTurns != aSourcePaths.end())
					{
						iMyTurns = itMyTurns->second.second;
					}
					else
					{
						const bool bMyOk = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_ROUTE, pSourceCity->plot(), plot(), (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY), true, &iMyTurns);
						aSourcePaths[pSourceCity->getID()] = std::make_pair(bMyOk, iMyTurns);
					}
					kClaims.iMyTurns = iMyTurns;
				}
				iAmount -= kClaims.outgoing(routes[i]->getSourceCity(), eYield);
			}
			else
			{
				kClaims.iMyTurns = (bUrgency && pSourceCity == pPlotCity) ? 0 : 1000;
			}
			// WTP: land transport with Automate Transport: no trip of more than 10 turns
			// WTP: a route with nothing to carry gets no path search: it could not add any value (most routes have nothing to move in a given turn)
			if (bMaxTrip && pDestinationCity != NULL && iAmount > 0)
			{
				const int iFlags = (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY);
				int iToSource = 0;
				int iToDestination = 0;
				// WTP: the same paths as before, only kept: from the position of this group to a source city once per source city of this call (several
				// yields / routes of one source city asked for it again), source to destination once per turn and unit type (wagons of one nation
				// stood in the same area and each searched the same ~300 coastal / land paths: 6-12 s of a turn change)
				bool bToSourceOk = true;
				if (pSourceCity != pPlotCity)
				{
					std::map<int, std::pair<bool, int> >::const_iterator itMaxTrip = aMaxTripSourcePaths.find(pSourceCity->getID());
					if (itMaxTrip != aMaxTripSourcePaths.end())
					{
						bToSourceOk = itMaxTrip->second.first;
						iToSource = itMaxTrip->second.second;
					}
					else
					{
						bToSourceOk = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pSourceCity->plot(), iFlags, true, &iToSource);
						aMaxTripSourcePaths[pSourceCity->getID()] = std::make_pair(bToSourceOk, iToSource);
					}
				}
				if ((pSourceCity != pPlotCity && (!bToSourceOk || iToSource > LAND_TRANSPORT_MAX_TRIP_TURNS))
					|| !WTP_getRoutePathCached(this, pSourceCity, pDestinationCity, iFlags, bIgnoreDanger, &iToDestination) || iToDestination > LAND_TRANSPORT_MAX_TRIP_TURNS)
				{
					continue;
				}
			}
			// R&R mod, vetiarvind, max yield import limit - start
			// WTP: a private route loads without import limit (see below)
			if(pDestinationCity != NULL && iAmount > 0 && pDestinationCity->getMaxImportAmount(eYield) > 0 && !routes[i]->isPrivate())
			{
				int turnsToReachToSource = 0, turnsToReachFromSourceToDest = 0;
				// WTP: the paths are kept: source to this group once per source city of this call, source to destination
				// once per turn and unit type (several yields of a source city, and every transport every turn, searched
				// the same long coastal paths again: the coastal transports took several percent of the AI's time)
				const int iFlags = (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY);
				bool bSourceOk;
				std::map<int, std::pair<bool, int> >::const_iterator itSource = aSourcePaths.find(pSourceCity->getID());
				if (itSource != aSourcePaths.end())
				{
					bSourceOk = itSource->second.first;
					turnsToReachToSource = itSource->second.second;
				}
				else
				{
					bSourceOk = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_ROUTE, pSourceCity->plot(), plot(), iFlags, true, &turnsToReachToSource);
					aSourcePaths[pSourceCity->getID()] = std::make_pair(bSourceOk, turnsToReachToSource);
				}
				const bool bDestOk = WTP_getRoutePathCached(this, pSourceCity, pDestinationCity, iFlags, bIgnoreDanger, &turnsToReachFromSourceToDest);

				if (!(bSourceOk && bDestOk))
					// We require both of these paths to be valid. If not, we skip this route
					continue;

				// At least one destination is reachable
				bNoRoute = false;

				// Erik: If we can travel from the current plot to the source, and then from source to destination in the same turn,
				// we have to make sure that we don't overestimate the amount that we should load
				int turnsRequired;
				if (turnsToReachToSource == turnsToReachFromSourceToDest)
				{
					// No need to add both legs of the journey since that would have the transport load too much cargo for the destination city
					turnsRequired = turnsToReachToSource + turnsToReachFromSourceToDest - 2;
					// In case generatePath could ever return 0
					turnsRequired = std::max(0, turnsRequired);
				}
				else
				{
					// Slightly underestimate the cargo we should carry (we cannot get this 100% correct since it depends on fractional movement,
					// other transports, consumption changes at the destination etc.
					turnsRequired = std::max(turnsToReachToSource, turnsToReachFromSourceToDest);
				}

				iAmount = estimateYieldsToLoad(pDestinationCity, iAmount, eYield, turnsRequired, aiYieldsLoaded[eYield]);
			}
			// WTP: a private route between colonies: no import limit, the route counts as viable
			else if (pDestinationCity != NULL && routes[i]->isPrivate())
			{
				bNoRoute = false;
			}
			// Note that Europe has no import limit!
			else if (pDestinationCity == NULL && routes[i]->getDestinationCity() == kEurope)
			{
				// This is a Europe trade-route, exempt it from the reachability criteria
				// TODO: Check that there is actually a route to Europe!
				bNoRoute = false;
			}

			// R&R mod, vetiarvind, max yield import limit - end
			if (bUrgency && bNoCargo && iAmount > 0 && iAmount < GC.getGameINLINE().getCargoYieldCapacity() / WTP_URGENCY_MIN_TRIP_SLOT_DIVISOR)
			{
				// WTP: too little for a trip of its own (the stock grows meanwhile); after the waiting time of the aging it is carried anyway
				if (wtpAgingLevels(pSourceCity, eYield, 1) <= 0)
				{
					iAmount = 0;
				}
			}
			if (iAmount > 0)
			{

				int iRouteValue;
				if (bUrgency)
				{
					iRouteValue = wtpUrgencyRouteValue(kOwner, routes[i], iAmount, kClaims);
				}
				else
				{
					int iExportValue = kOwner.AI_transferYieldValue(routes[i]->getSourceCity(), routes[i]->getYield(), -iAmount);
					int iImportValue = kOwner.AI_transferYieldValue(routes[i]->getDestinationCity(), routes[i]->getYield(), iAmount);
					iRouteValue = (iExportValue + iImportValue + 2 * std::min(iExportValue, iImportValue)) / 4;
				}

				if (pSourceCity == pPlotCity)
				{
					cityValues[routes[i]->getDestinationCity()] += 2 * iRouteValue;
				}
				else
				{
					cityValues[routes[i]->getSourceCity()] += iRouteValue;
				}

				routeValues[i] = iRouteValue;
			}
		}
	}
	} // iBatch

	// We bail if there's not a single viable destination
	// Transports with cargo should carry on because they might need to drop it off somewhere before they can start on normal traderoutes
	if (bNoRoute && bNoCargo)
	{
		m_aTradeOrders.clear();
		m_iNoDestinationSince = -1;
		return false;
	}

	// TAC - Trade Routes Advisor - koma13 - START
	// R&R mod, vetiarvind, max yield import limit - start
	// refactor contents of this block to set bIgnoreDanger into getIgnoreDangerStatus()
	// R&R mod, vetiarvind, max yield import limit - end
	// TAC - Trade Routes Advisor - koma13 - END

	wtpTradeLap.next(WtpTiming::SLOT_TR_BEST);
	IDInfo kBestDestination(NO_PLAYER, -1);
	int iBestDestinationValue = 0;
	//select best destination
	// WTP: an AI player's transport tries the destinations in the order of their value without a path (the path can only lower it, except
	// for the coastal transport, which tries the 8 best). Before every colony with a value got its own path search.
	static const int WTP_AI_MAX_DESTINATION_PATHS = 8;
	int iDestinationPaths = 0;
	std::vector<std::pair<IDInfo, int> > aDestinations(cityValues.begin(), cityValues.end());
	if (!isHuman() && aDestinations.size() > 1)
	{
		std::vector<std::pair<int, int> > aKeys; // (-value, index): ascending order is the best first
		for (uint k = 0; k < aDestinations.size(); ++k)
		{
			int iKey = 0;
			if (aDestinations[k].second > 0)
			{
				CvCity* pKeyCity = ::getCity(aDestinations[k].first);
				if (pKeyCity != NULL)
				{
					iKey = aDestinations[k].second / (1 + kOwner.AI_plotTargetMissionAIs(pKeyCity->plot(), MISSIONAI_TRANSPORT, this, 0));
				}
			}
			aKeys.push_back(std::make_pair(-iKey, (int)k));
		}
		std::sort(aKeys.begin(), aKeys.end());
		std::vector<std::pair<IDInfo, int> > aSorted;
		for (uint k = 0; k < aKeys.size(); ++k)
		{
			aSorted.push_back(aDestinations[aKeys[k].second]);
		}
		aDestinations.swap(aSorted);
	}
	for (std::vector<std::pair<IDInfo, int> >::iterator it = aDestinations.begin(); it != aDestinations.end(); ++it)
	{
		if (!isHuman() && iBestDestinationValue > 0 && (!bCoastalTransport || iDestinationPaths >= WTP_AI_MAX_DESTINATION_PATHS))
		{
			break;
		}
		int iValue = it->second;

		if (iValue > 0)
		{
			CvCity* pCity = ::getCity(it->first);
			if (pCity != NULL)
			{
				++iDestinationPaths;
				FAssert(!atPlot(pCity->plot()));
				// TAC - Trade Routes Advisor - koma13 - START
				//if (WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pCity->plot(), MOVE_NO_ENEMY_TERRITORY, true))

				CvPlot* pDestinationCityPlot = pCity->plot();

				int iTurns = 0;
				bool bDestinationReachable;
				std::map<IDInfo, std::pair<bool, int> >::const_iterator itToDest = aGroupToDestPaths.find(it->first);
				if (itToDest != aGroupToDestPaths.end())
				{
					bDestinationReachable = itToDest->second.first;
					iTurns = itToDest->second.second;
				}
				else
				{
					bDestinationReachable = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pDestinationCityPlot, (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY), true, &iTurns);
					aGroupToDestPaths[it->first] = std::make_pair(bDestinationReachable, iTurns);
				}
				if (bDestinationReachable
					&& (!bMaxTrip || iTurns <= LAND_TRANSPORT_MAX_TRIP_TURNS)) // WTP: land transport: no trip of more than 10 turns
				// TAC - Trade Routes Advisor - koma13 - END
				{
					if (!bUrgency)
					{
						iValue /= 1 + kOwner.AI_plotTargetMissionAIs(pDestinationCityPlot, MISSIONAI_TRANSPORT, this, 0);
					}

					// WTP: a human player's automated transport serves the most urgent colony first (with cargo on board as well as on the empty way to a colony whose
					// yields are fetched); the distance only decides between jobs of a similar urgency (the transports know of each other by their orders, see wtpCollectTradeClaims,
					// so the colonies that another transport serves are not divided by the number of the transports on their way any more)
					if (bUrgency && iValue > 0)
					{
						iValue = std::max(1, (int)(iValue * 100.0 / (100 + WTP_URGENCY_DISTANCE_PERCENT * std::max(0, iTurns))));
					}
					else if (bFillHold && iValue > 0)
					{
						iValue = std::max(1, iValue / std::max(1, iTurns));
					}

					if (bCoastalTransport)
					{
						// Erik: Eventually these tuning factors should not be hard-coded!
						const int CoastalTransportRangeThreshold = 4;
						const int CoastalTransportDifferentAreaMultiplier = 2;

						// Erik: If this is a coastal transport, avoid routes that are much longer than land routes unless there are no other wagons in this area

						// Erik: If the destination city is in a different area, then this is a more attractive route (wagons cannot cross coast!)
						// Note: We don't have to check for the areas being coastally reachable, since that already checked

						const CvArea* pDestinationArea = pDestinationCityPlot->area();
						const CvArea* pPlotArea = plot()->area();

						if (pDestinationArea != pPlotArea)
						{
							// Erik: Double the value of the route. Even if we encourage transportion between areas we don't want to sail around the world!
							// so we make that less attractive
							iValue *= CoastalTransportDifferentAreaMultiplier;
							iValue /=  std::max(1, iTurns - (CoastalTransportRangeThreshold * CoastalTransportDifferentAreaMultiplier));
						}
						else
						{
							if (pPlotArea->getNumAIUnits(getOwnerINLINE(), UNITAI_WAGON) > 0)
							{
								// Erik: Longer routes are less attractive for coastal transports
								iValue /= std::max(1, iTurns - CoastalTransportRangeThreshold);
							}
						}
					}
				}
				else
				{
					iValue = 0;
				}
			}

			if (iValue > iBestDestinationValue)
			{
				iBestDestinationValue = iValue;
				kBestDestination = it->first;
			}
		}
	}

	// WTP: the priority target stays: a transport that stopped at a colony on its way continues to the target it had decided on
	// (the stops on the way are secondary). The target is dropped when it is reached, or when it has nothing to deliver or fetch any more
	if (m_kPriorityTarget.eOwner != NO_PLAYER)
	{
		CvCity* const pPriorityCity = ::getCity(m_kPriorityTarget);
		if (!bFillHold || pPriorityCity == NULL || pPriorityCity == pPlotCity || cityValues[m_kPriorityTarget] <= 0)
		{
			m_kPriorityTarget = IDInfo();
			m_iPriorityDetour = 0;
		}
		else
		{
			std::map<IDInfo, std::pair<bool, int> >::const_iterator itPriorityPath = aGroupToDestPaths.find(m_kPriorityTarget);
			bool bPriorityOk;
			if (itPriorityPath != aGroupToDestPaths.end())
			{
				bPriorityOk = itPriorityPath->second.first;
			}
			else
			{
				int iPriorityTurns = 0;
				bPriorityOk = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pPriorityCity->plot(), (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY), true, &iPriorityTurns);
				aGroupToDestPaths[m_kPriorityTarget] = std::make_pair(bPriorityOk, iPriorityTurns);
			}
			if (bPriorityOk)
			{
				kBestDestination = m_kPriorityTarget;
			}
			else
			{
				m_kPriorityTarget = IDInfo();
				m_iPriorityDetour = 0;
			}
		}
	}

	if ((pPlotCity != NULL) && (kBestDestination.eOwner != NO_PLAYER))
	{
		//We need to keep looping and recalculating
		//For example a city might have "101" of an item, we want to move the first 100 but not the 1.
		//But it could also have 200, in which case we might want 2 loads of 100...
		//But it could also have 200 of two resources, and we'd want to move 100 of each...
		// WTP: pass 0 loads for the best destination. Pass 1 (human player's automated transport only) fills the free slots
		// with yields for other colonies that lie on the way to it
		std::set<IDInfo> aFillDestinations;
		for (int iPass = 0; iPass < 2; ++iPass)
		{
		if (iPass == 1)
		{
			if (!bFillHold || (isFull() && getPartialYieldSpace(NO_YIELD) <= 0))
			{
				break;
			}
			CvCity* const pBestCity = ::getCity(kBestDestination);
			if (pBestCity == NULL)
			{
				break;
			}
			const int iFillFlags = (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY);
			int iToBest = 0;
			bool bBestOk;
			std::map<IDInfo, std::pair<bool, int> >::const_iterator itBestPath = aGroupToDestPaths.find(kBestDestination);
			if (itBestPath != aGroupToDestPaths.end())
			{
				bBestOk = itBestPath->second.first;
				iToBest = itBestPath->second.second;
			}
			else
			{
				bBestOk = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pBestCity->plot(), iFillFlags, true, &iToBest);
				aGroupToDestPaths[kBestDestination] = std::make_pair(bBestOk, iToBest);
			}
			if (!bBestOk)
			{
				break;
			}
			for (uint i = 0; i < routes.size(); ++i)
			{
				const IDInfo kFillDestination = routes[i]->getDestinationCity();
				if (kFillDestination == kBestDestination || ::getCity(routes[i]->getSourceCity()) != pPlotCity || (routes[i]->isPrivate() && getAutomateType() != AUTOMATE_TRANSPORT_ROUTES)
					|| aFillDestinations.find(kFillDestination) != aFillDestinations.end())
				{
					continue;
				}
				CvCity* const pFillCity = ::getCity(kFillDestination);
				if (pFillCity == NULL || pFillCity == pPlotCity)
				{
					continue;
				}
				int iToFill = 0;
				bool bFillOk;
				std::map<IDInfo, std::pair<bool, int> >::const_iterator itFillPath = aGroupToDestPaths.find(kFillDestination);
				if (itFillPath != aGroupToDestPaths.end())
				{
					bFillOk = itFillPath->second.first;
					iToFill = itFillPath->second.second;
				}
				else
				{
					bFillOk = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pFillCity->plot(), iFillFlags, true, &iToFill);
					aGroupToDestPaths[kFillDestination] = std::make_pair(bFillOk, iToFill);
				}
				int iFillToBest = 0;
				// the yields that the current city has for this destination
				int aiFillAvailable[NUM_YIELD_TYPES];
				std::fill(aiFillAvailable, aiFillAvailable + NUM_YIELD_TYPES, 0);
				for (uint j = 0; j < routes.size(); ++j)
				{
					if (routes[j]->getDestinationCity() == kFillDestination && ::getCity(routes[j]->getSourceCity()) == pPlotCity)
					{
						int iFillAmount = std::max(0, pPlotCity->getYieldStored(routes[j]->getYield()) - pPlotCity->getAutoMaintainThreshold(routes[j]->getYield()));
						// the import limit of the receiving colony (what is on board of this yield counts already)
						if (iFillAmount > 0 && pFillCity->getMaxImportAmount(routes[j]->getYield()) > 0 && !routes[j]->isPrivate())
						{
							iFillAmount = estimateYieldsToLoad(pFillCity, iFillAmount, routes[j]->getYield(), iToFill, aiYieldsLoaded[routes[j]->getYield()]);
						}
						aiFillAvailable[routes[j]->getYield()] += iFillAmount;
					}
				}
				if (bFillOk && WTP_getRoutePathCached(this, pFillCity, pBestCity, iFillFlags, bIgnoreDanger, &iFillToBest)
					&& (iToFill + iFillToBest <= iToBest || (iToFill + iFillToBest <= iToBest + WTP_FILL_HOLD_MAX_DETOUR_TURNS && isDetourWorthwhile(aiFillAvailable))))
				{
					aFillDestinations.insert(kFillDestination);
				}
			}
			if (aFillDestinations.empty())
			{
				break;
			}
		}
		kClaims.iMyTurns = 0; // (it loads here: it is in the colony of the source)
		// WTP: also a full transport loads into a partly filled slot of the same yield (the game merges the load into it)
		while (!isFull() || (bFillHold && getPartialYieldSpace(NO_YIELD) > 0))
		{
			int iBestRoute = -1;
			int iBestRouteValue = 0;
			// R&R mod, vetiarvind, max yield import limit - start
			int iBestRouteYieldAmount = 0;
			bool bRouteComplete = true;
			bool bImportLimitUsed = false;
			// R&R mod, vetiarvind, max yield import limit - end
			//Now, for any trade routes which this group is assigned to, try to pick up cargo here.
			for (uint i = 0; i < routes.size(); ++i)
			{
				// Erik: This is redundant. Instead of looping through all routes, just find the subset of routes to the best destination city

				const CvCity* pSourceCity = ::getCity(routes[i]->getSourceCity());
				if ((pSourceCity != NULL && pSourceCity == pPlotCity) // R&R mod, vetiarvind, max yield import limit (move plot==srcCity check outside as optmztn)
					&& (!bFillHold || canLoadYieldHere(routes[i]->getYield())) // WTP: nothing that cannot be loaded (partly filled slots of other yields)
					&& (iPass == 0 ? (routes[i]->getDestinationCity() == kBestDestination) : (aFillDestinations.find(routes[i]->getDestinationCity()) != aFillDestinations.end())))
				{
					const CvCity* pDestinationCity = ::getCity(routes[i]->getDestinationCity());
					const YieldTypes eYield = routes[i]->getYield();

					// transport feeder - start - Nightinggale
					//int iAmount = pSourceCity->getYieldStored(eYield) - pSourceCity->getMaintainLevel(eYield);
					int iAmount = pSourceCity->getYieldStored(eYield) - pSourceCity->getAutoMaintainThreshold(eYield);
					// transport feeder - end - Nightinggale


					// R&R mod, vetiarvind, max yield import limit - start
					int iOriginalAmount = iAmount;
					const bool bDestinationHasImportLimit = pDestinationCity != NULL && pDestinationCity->getImportsLimit(eYield) > 0 && !routes[i]->isPrivate(); // WTP: private: no limit
					if (bDestinationHasImportLimit)
					{
						int turnsToReach = 0;
						iOriginalAmount = iAmount = std::min(GC.getGameINLINE().getCargoYieldCapacity(), iAmount);
						const bool r1 = WTP_getRoutePathCached(this, pSourceCity, pDestinationCity, (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY), bIgnoreDanger, &turnsToReach);
						FAssertMsg(r1, "Path must be valid!");
						// Erik: If the destination can be reached in the same turn, subtract a turn
						turnsToReach = std::max(0, turnsToReach - 1);
						iAmount = estimateYieldsToLoad(pDestinationCity, iAmount, eYield, turnsToReach, aiYieldsLoaded[eYield]);
					}

					// R&R mod, vetiarvind, max yield import limit - end
					if (iAmount > 0)
					{
						int iRouteValue;
						if (bUrgency)
						{
							// (the most urgent yield is loaded first)
							iRouteValue = wtpUrgencyRouteValue(kOwner, routes[i], iAmount, kClaims);
						}
						else
						{
							int iExportValue = kOwner.AI_transferYieldValue(routes[i]->getSourceCity(), routes[i]->getYield(), -iAmount);
							int iImportValue = kOwner.AI_transferYieldValue(routes[i]->getDestinationCity(), routes[i]->getYield(), iAmount);
							iRouteValue = (iExportValue + iImportValue + 2 * std::min(iExportValue, iImportValue)) / 4;
						}

						if (iRouteValue > iBestRouteValue)
						{
							iBestRouteValue = iRouteValue;
							iBestRoute = i;
							// R&R mod, vetiarvind, max yield import limit - start
							iBestRouteYieldAmount = iAmount;
							bImportLimitUsed = bDestinationHasImportLimit;
							// R&R mod, vetiarvind, max yield import limit - end
						}
					}
				}
			} //end of for loop of routes

			if (iBestRouteValue > 0)
			{
				bool bLoadedAny = false; // WTP: a round without any load ends the loading (nothing could be loaded)
				CLLNode<IDInfo>* pUnitNode = headUnitNode();
				while (pUnitNode != NULL)
				{
					CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
					pUnitNode = nextUnitNode(pUnitNode);

					if (pLoopUnit != NULL)
					{
						if (pLoopUnit->canLoadYield(plot(), routes[iBestRoute]->getYield(), false) ) 			// R&R mod, vetiarvind, max yield import limit fix
						{
							//pLoopUnit->loadYield(routes[iBestRoute]->getYield(), false);
							int loaded = 0;
							if(bImportLimitUsed)
								loaded = pLoopUnit->loadYieldAmount(routes[iBestRoute]->getYield(), std::min(iBestRouteYieldAmount, pLoopUnit->getMaxLoadYieldAmount(routes[iBestRoute]->getYield())), false);
							else
								loaded = pLoopUnit->loadYield(routes[iBestRoute]->getYield(), false);

							// R&R mod, vetiarvind, max yield import limit - end
							aiYieldsLoaded[routes[iBestRoute]->getYield()] += loaded;
							if (loaded > 0 && bUrgency)
							{
								wtpNoteServed(pPlotCity, routes[iBestRoute]->getYield(), 1); // (picked up: the export waits no more)
							}
							bLoadedAny = (loaded > 0);
							break;
						}
					}
				}
				if (!bLoadedAny)
				{
					break;
				}
			}
			else
			{
				break;
			}
		}
		} // iPass
	}

	// WTP: an automated transport of a human player that stands in a colony with cargo and finds no destination for it (e.g. the rest of a
	// delivery that the destination did not take because of its import limit) looks for an order every turn. If there is none for
	// WTP_NO_DESTINATION_UNLOAD_TURNS turns, the import limits no longer count: it goes to the destination (of its routes for the yields on board)
	// that exceeds its import limit least (the cargo is unloaded there by force, see the start of this function). Only if there is no such
	// destination, the cargo is unloaded into the colony it stands in, and the transport goes on with its normal orders.
	static const int WTP_NO_DESTINATION_UNLOAD_TURNS = 2;
	if (isHuman() && (getAutomateType() == AUTOMATE_TRANSPORT_FULL || getAutomateType() == AUTOMATE_TRANSPORT_ROUTES) && pPlotCity != NULL && hasCargo()
		&& kBestDestination.eOwner == NO_PLAYER)
	{
		const int iNowTurn = GC.getGameINLINE().getGameTurn();
		if (m_iNoDestinationSince < 0)
		{
			m_iNoDestinationSince = iNowTurn;
		}
		else if (iNowTurn - m_iNoDestinationSince >= WTP_NO_DESTINATION_UNLOAD_TURNS)
		{
			m_iNoDestinationSince = -1;
			int iBestOverflow = MAX_INT;
			int iBestTurns = MAX_INT;
			for (uint i = 0; i < routes.size(); ++i)
			{
				CvCity* const pOverCity = ::getCity(routes[i]->getDestinationCity());
				const YieldTypes eOverYield = routes[i]->getYield();
				if (pOverCity == NULL || pOverCity == pPlotCity || routes[i]->getDestinationCity() == kEurope || aiYieldsLoaded[eOverYield] <= 0 || routes[i]->isPrivate())
				{
					continue;
				}
				std::map<IDInfo, std::pair<bool, int> >::const_iterator itOver = aGroupToDestPaths.find(routes[i]->getDestinationCity());
				if (itOver == aGroupToDestPaths.end())
				{
					int iOverTurns = 0;
					const bool bOverOk = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pOverCity->plot(), (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY), true, &iOverTurns);
					aGroupToDestPaths[routes[i]->getDestinationCity()] = std::make_pair(bOverOk, iOverTurns);
					itOver = aGroupToDestPaths.find(routes[i]->getDestinationCity());
				}
				if (!itOver->second.first || (bMaxTrip && itOver->second.second > LAND_TRANSPORT_MAX_TRIP_TURNS))
				{
					continue;
				}
				// the amount of all yields on board that this colony gets by its routes and that is over its import limit
				int iOverflow = 0;
				for (uint j = 0; j < routes.size(); ++j)
				{
					if (routes[j]->getDestinationCity() == routes[i]->getDestinationCity() && !routes[j]->isPrivate() && aiYieldsLoaded[routes[j]->getYield()] > 0)
					{
						iOverflow += aiYieldsLoaded[routes[j]->getYield()] - estimateYieldsToLoad(pOverCity, aiYieldsLoaded[routes[j]->getYield()], routes[j]->getYield(), itOver->second.second, 0);
					}
				}
				if (iOverflow < iBestOverflow || (iOverflow == iBestOverflow && itOver->second.second < iBestTurns))
				{
					iBestOverflow = iOverflow;
					iBestTurns = itOver->second.second;
					kBestDestination = routes[i]->getDestinationCity();
				}
			}
		}
		if (m_iNoDestinationSince < 0 && kBestDestination.eOwner == NO_PLAYER)
		{
			// (no destination at all: the cargo goes into the colony)
			std::vector<CvUnit*> aCargoUnits;
			CLLNode<IDInfo>* pCargoNode = plot()->headUnitNode();
			while (pCargoNode != NULL)
			{
				CvUnit* pCargoUnit = plot()->getUnitNodeLoop(pCargoNode);
				if (pCargoUnit != NULL && pCargoUnit->getYield() != NO_YIELD && pCargoUnit->getTransportUnit() != NULL
					&& pCargoUnit->getTransportUnit()->getGroup() == this && pCargoUnit->canUnload())
				{
					aCargoUnits.push_back(pCargoUnit);
				}
			}
			for (uint i = 0; i < aCargoUnits.size(); ++i)
			{
				unloadToCity(pPlotCity, aCargoUnits[i], UnloadMode::Force);
			}
			if (!hasCargo())
			{
				// (empty now: it decides again with the orders of an empty transport)
				return AI_tradeRoutes();
			}
		}
	}
	else if (kBestDestination.eOwner != NO_PLAYER || !hasCargo())
	{
		m_iNoDestinationSince = -1;
	}

	if ((kBestDestination.eOwner == NO_PLAYER) && hasCargo())
	{
		// Transport group is full and can't find any destination
		CvCity* pCity = kOwner.AI_findBestPort();
		if (pCity != NULL && !atPlot(pCity->plot()))
		{
			// check that the city is reachable
			int iTurns = 0;
			if (!WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pCity->plot(), (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY), true, &iTurns))
			{
				// no path. Bail out instead of trying to add a movement command
				// if the command to move is given, then movement will fail and this function is called again
				// in other words trying to move will cause an infinite loop (bug #416)
				return false;
			}
			kBestDestination = pCity->getIDInfo();
		}
	}

	// WTP: pick-up stop. With free cargo slots the transport stops on its way to the destination at a colony that has yields for this
	// destination (the trip over it takes at most WTP_FILL_HOLD_MAX_DETOUR_TURNS turns more). This applies to the way to a colony that
	// receives cargo as well as to the empty way to a colony whose yields are fetched (the colonies on the way that deliver to it).
	wtpTradeLap.next(WtpTiming::SLOT_TR_PICKUP);
	CvCity* pPickupStop = NULL;
	if (bFillHold && (!isFull() || getPartialYieldSpace(NO_YIELD) > 0) && kBestDestination.eOwner != NO_PLAYER && kBestDestination != kEurope)
	{
		CvCity* const pTargetCity = ::getCity(kBestDestination);
		if (pTargetCity != NULL && !atPlot(pTargetCity->plot()))
		{
			const int iPickupFlags = (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY);
			int iToTarget = 0;
			bool bTargetOk;
			std::map<IDInfo, std::pair<bool, int> >::const_iterator itTargetPath = aGroupToDestPaths.find(kBestDestination);
			if (itTargetPath != aGroupToDestPaths.end())
			{
				bTargetOk = itTargetPath->second.first;
				iToTarget = itTargetPath->second.second;
			}
			else
			{
				bTargetOk = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pTargetCity->plot(), iPickupFlags, true, &iToTarget);
				aGroupToDestPaths[kBestDestination] = std::make_pair(bTargetOk, iToTarget);
			}
			if (bTargetOk)
			{
				// free cargo space of the group in units of yield: the free slots times the capacity of a slot, plus per yield the free
				// space in its partly filled slots (a new load of the same yield is merged into them by the game)
				int iFreeSlots = 0;
				CLLNode<IDInfo>* pFreeNode = headUnitNode();
				while (pFreeNode != NULL)
				{
					CvUnit* const pFreeUnit = ::getUnit(pFreeNode->m_data);
					pFreeNode = nextUnitNode(pFreeNode);
					if (pFreeUnit != NULL && !pFreeUnit->isCargo() && pFreeUnit->cargoSpace() > pFreeUnit->getCargo())
					{
						iFreeSlots += pFreeUnit->cargoSpace() - pFreeUnit->getCargo();
					}
				}
				const int iSlotCapacity = GC.getGameINLINE().getCargoYieldCapacity();
				const int iFreeSlotCapacity = iFreeSlots * iSlotCapacity;
				const int iFreeCapacity = iFreeSlotCapacity + getPartialYieldSpace(NO_YIELD);
				const int iMinPickup = std::max(1, iSlotCapacity / WTP_PICKUP_STOP_MIN_SLOT_DIVISOR);
				std::map<int, int> aPickupAmounts; // source city ID -> units that could be loaded for the target
				std::map<int, std::vector<int> > aPickupByYield; // source city ID -> the same per yield
				for (uint i = 0; i < routes.size(); ++i)
				{
					if (routes[i]->getDestinationCity() != kBestDestination)
					{
						continue;
					}
					CvCity* const pPickupCity = ::getCity(routes[i]->getSourceCity());
					if (pPickupCity == NULL || pPickupCity == pPlotCity || pPickupCity == pTargetCity)
					{
						continue;
					}
					const YieldTypes ePickupYield = routes[i]->getYield();
					int iPickupAmount = pPickupCity->getYieldStored(ePickupYield) - pPickupCity->getAutoMaintainThreshold(ePickupYield);
					if (iPickupAmount > 0 && pTargetCity->getMaxImportAmount(ePickupYield) > 0 && !routes[i]->isPrivate())
					{
						iPickupAmount = estimateYieldsToLoad(pTargetCity, iPickupAmount, ePickupYield, iToTarget, aiYieldsLoaded[ePickupYield]);
					}
					// not more than the free slots and the partly filled slots of this yield can take
					iPickupAmount = std::min(iPickupAmount, iFreeSlotCapacity + getPartialYieldSpace(ePickupYield));
					if (iPickupAmount > 0)
					{
						aPickupAmounts[pPickupCity->getID()] += iPickupAmount;
						std::vector<int>& aiByYield = aPickupByYield[pPickupCity->getID()];
						aiByYield.resize(NUM_YIELD_TYPES, 0);
						aiByYield[ePickupYield] += iPickupAmount;
					}
				}
				// the detours of all stops on the way to the priority target together stay within the limit
				const int iDetourLeft = WTP_FILL_HOLD_MAX_DETOUR_TURNS - m_iPriorityDetour;
				int iBestPickupAmount = 0;
				int iBestPickupEfficiency = 0;
				int iBestPickupDetour = MAX_INT;
				int iBestPickupTotal = 0;
				std::vector<int> aiBestPickupYields;
				for (std::map<int, int>::const_iterator itPickup = aPickupAmounts.begin(); itPickup != aPickupAmounts.end(); ++itPickup)
				{
					// not more than the free space can be loaded
					const int iCandidateAmount = std::min(itPickup->second, iFreeCapacity);
					if (iCandidateAmount < 1)
					{
						continue;
					}
					CvCity* const pCandidate = kOwner.getCity(itPickup->first);
					if (pCandidate == NULL)
					{
						continue;
					}
					int iToCandidate = 0;
					bool bCandidateOk;
					const IDInfo kCandidate = pCandidate->getIDInfo();
					std::map<IDInfo, std::pair<bool, int> >::const_iterator itCandidatePath = aGroupToDestPaths.find(kCandidate);
					if (itCandidatePath != aGroupToDestPaths.end())
					{
						bCandidateOk = itCandidatePath->second.first;
						iToCandidate = itCandidatePath->second.second;
					}
					else
					{
						bCandidateOk = WTP_timedPath(this, WtpTiming::SLOT_TR_PATH_POS, plot(), pCandidate->plot(), iPickupFlags, true, &iToCandidate);
						aGroupToDestPaths[kCandidate] = std::make_pair(bCandidateOk, iToCandidate);
					}
					int iCandidateToTarget = 0;
					if (bCandidateOk && WTP_getRoutePathCached(this, pCandidate, pTargetCity, iPickupFlags, bIgnoreDanger, &iCandidateToTarget))
					{
						const int iDetour = std::max(0, iToCandidate + iCandidateToTarget - iToTarget);
						// the shorter detour wins, with the same detour the larger load
						// without a detour every amount counts, with a detour it has to be a quarter of a slot and the detour has to be worth it
						if (iDetour > 0 && (iCandidateAmount < iMinPickup || !isDetourWorthwhile(&aPickupByYield[itPickup->first][0])))
						{
							continue;
						}
						// slot efficiency: the units loaded per new slot that the stop needs (loads into partly filled slots need none)
						int iNewSlots = 0;
						const std::vector<int>& aiCandidateYields = aPickupByYield[itPickup->first];
						for (YieldTypes eSlotYield = FIRST_YIELD; eSlotYield < NUM_YIELD_TYPES && eSlotYield < (YieldTypes)aiCandidateYields.size(); ++eSlotYield)
						{
							const int iBeyondPartial = aiCandidateYields[eSlotYield] - getPartialYieldSpace(eSlotYield);
							if (iBeyondPartial > 0)
							{
								iNewSlots += (iBeyondPartial + iSlotCapacity - 1) / std::max(1, iSlotCapacity);
							}
						}
						const int iCandidateEfficiency = iCandidateAmount * 10 / std::max(1, iNewSlots);
						// the shorter detour wins, then the more efficient use of the slots, then the larger load
						if (iDetour <= iDetourLeft && (iDetour < iBestPickupDetour
							|| (iDetour == iBestPickupDetour && (iCandidateEfficiency > iBestPickupEfficiency
								|| (iCandidateEfficiency == iBestPickupEfficiency && iCandidateAmount > iBestPickupAmount)))))
						{
							iBestPickupEfficiency = iCandidateEfficiency;
							iBestPickupDetour = iDetour;
							iBestPickupAmount = iCandidateAmount;
							iBestPickupTotal = iDetour;
							aiBestPickupYields = aiCandidateYields;
							pPickupStop = pCandidate;
						}
					}
				}
				if (pPickupStop != NULL)
				{
					m_iPriorityDetour += iBestPickupTotal;
					m_kTooltipStop = pPickupStop->getIDInfo();
					m_aiTooltipStopYields = aiBestPickupYields;
				}
			}
		}
	}

	// WTP: waiting counts like a detour. A transport with cargo and free space (slots or partly filled slots) waits a turn at a colony if
	// the production of it for the same destination fills at least a quarter of a slot in that turn, within the detour budget, and if that is worth it
	// (see isDetourWorthwhile). Stops without a detour come first.
	if (bFillHold && pPickupStop == NULL && pPlotCity != NULL && kBestDestination.eOwner != NO_PLAYER && kBestDestination != kEurope
		&& hasCargo() && (!isFull() || getPartialYieldSpace(NO_YIELD) > 0) && WTP_FILL_HOLD_MAX_DETOUR_TURNS - m_iPriorityDetour >= 1)
	{
		CvCity* const pWaitTarget = ::getCity(kBestDestination);
		if (pWaitTarget != NULL && pWaitTarget != pPlotCity)
		{
			int iWaitToTarget = 0;
			std::map<IDInfo, std::pair<bool, int> >::const_iterator itWaitPath = aGroupToDestPaths.find(kBestDestination);
			if (itWaitPath != aGroupToDestPaths.end())
			{
				iWaitToTarget = itWaitPath->second.second;
			}
			const int iWaitSlotCapacity = GC.getGameINLINE().getCargoYieldCapacity();
			const int iWaitFreeSlots = getFreeSlotCount() * iWaitSlotCapacity;
			int aiExpected[NUM_YIELD_TYPES];
			std::fill(aiExpected, aiExpected + NUM_YIELD_TYPES, 0);
			int iExpectedTotal = 0;
			for (uint i = 0; i < routes.size(); ++i)
			{
				if (routes[i]->getDestinationCity() != kBestDestination || ::getCity(routes[i]->getSourceCity()) != pPlotCity)
				{
					continue;
				}
				const YieldTypes eWaitYield = routes[i]->getYield();
				// what the colony produces in a turn (what it stores now was loaded above as far as possible)
				int iExpected = std::max(0, pPlotCity->getYieldRate(eWaitYield));
				iExpected = std::min(iExpected, iWaitFreeSlots + getPartialYieldSpace(eWaitYield));
				if (iExpected > 0 && pWaitTarget->getMaxImportAmount(eWaitYield) > 0 && !routes[i]->isPrivate())
				{
					iExpected = estimateYieldsToLoad(pWaitTarget, iExpected, eWaitYield, iWaitToTarget + 1, aiYieldsLoaded[eWaitYield]);
				}
				if (iExpected > 0)
				{
					aiExpected[eWaitYield] += iExpected;
					iExpectedTotal += iExpected;
				}
			}
			if (iExpectedTotal >= std::max(1, iWaitSlotCapacity / WTP_PICKUP_STOP_MIN_SLOT_DIVISOR) && isDetourWorthwhile(aiExpected))
			{
				m_kPriorityTarget = kBestDestination;
				m_iPriorityDetour += 1;
				m_kTooltipStop = pPlotCity->getIDInfo();
				m_bTooltipWaiting = true;
				m_aiTooltipStopYields.assign(aiExpected, aiExpected + NUM_YIELD_TYPES);
				pushMission(MISSION_SKIP);
				if (isHuman())
				{
					std::map<IDInfo, std::pair<bool, int> >::const_iterator itBestTurns = aGroupToDestPaths.find(kBestDestination);
					updateTradeOrders(routes, routeValues, kBestDestination, (itBestTurns != aGroupToDestPaths.end()) ? itBestTurns->second.second : 0);
				}
				return true;
			}
		}
	}

	wtpTradeLap.next(WtpTiming::SLOT_TR_ORDERS);
	// the priority target is remembered while the transport goes to a pick-up stop
	m_kPriorityTarget = (pPickupStop != NULL) ? kBestDestination : IDInfo();
	if (pPickupStop == NULL)
	{
		m_iPriorityDetour = 0;
	}

	// WTP: the orders shown in the tooltip of the transport (human player only)
	if (isHuman())
	{
		std::map<IDInfo, std::pair<bool, int> >::const_iterator itBestTurns = aGroupToDestPaths.find(kBestDestination);
		updateTradeOrders(routes, routeValues, kBestDestination, (itBestTurns != aGroupToDestPaths.end()) ? itBestTurns->second.second : 0);
	}

	wtpTradeLap.next(WtpTiming::SLOT_TR_PUSH);
	//As a final step, we could consider loading yields which would be useful as parts of delivery runs...
	if (kBestDestination != kEurope)
	{
		CvCity* pBestDestinationCity = ::getCity(kBestDestination);
		if (pBestDestinationCity != NULL)
		{
			FAssert(!atPlot(pBestDestinationCity->plot()));
			// TAC - Trade Routes Advisor - koma13 - START
			//pushMission(MISSION_MOVE_TO, pBestDestinationCity->getX_INLINE(), pBestDestinationCity->getY_INLINE(), MOVE_NO_ENEMY_TERRITORY, false, false, MISSIONAI_TRANSPORT, pBestDestinationCity->plot());
			// WTP: with a pick-up stop the transport goes there first (and decides again there)
			CvCity* const pMoveCity = (pPickupStop != NULL) ? pPickupStop : pBestDestinationCity;
			pushMission(MISSION_MOVE_TO, pMoveCity->getX_INLINE(), pMoveCity->getY_INLINE(), (bIgnoreDanger ? MOVE_IGNORE_DANGER : MOVE_NO_ENEMY_TERRITORY), false, false, MISSIONAI_TRANSPORT, pMoveCity->plot());
			// TAC - Trade Routes Advisor - koma13 - END
			if (atPlot(pBestDestinationCity->plot()))
			{
				//Unload any goods if required (we can always pick them back up if this is an i+e city).
				std::vector<CvUnit*> units;

				CLLNode<IDInfo>* pUnitNode = plot()->headUnitNode();
				CvUnit* pLoopUnit;
				while (pUnitNode != NULL)
				{
					pLoopUnit = plot()->getUnitNodeLoop(pUnitNode);

					if (pLoopUnit != NULL)
					{
						const YieldTypes eYield = pLoopUnit->getYield();

						if ((eYield != NO_YIELD) && pLoopUnit->isCargo())
						{
							if (pLoopUnit->getTransportUnit()->getGroup() == this && pLoopUnit->canUnload())
							{
								units.push_back(pLoopUnit);
							}
						}
					}
				}
				for (uint i = 0; i < units.size(); ++i)
				{
					// R&R mod, vetiarvind, max yield import limit - start
					unloadToCity(pBestDestinationCity, units[i]);
					//units[i]->unload();
					// R&R mod, vetiarvind, max yield import limit - end
				}
			}
			return true;
		}
	}
	else
	{
		if (isHuman())
		{
			// Erik: Is this really ok for a coastal transport ?
			getHeadUnit()->AI_setUnitAIState(UNITAI_STATE_SAIL);
		}
	}

	return false;
}

CvUnit* CvSelectionGroupAI::AI_ejectBestDefender(CvPlot* pDefendPlot)
{
	CLLNode<IDInfo>* pEntityNode;
	CvUnit* pLoopUnit;

	pEntityNode = headUnitNode();

	CvUnit* pBestUnit = NULL;
	int iBestUnitValue = 0;

	while (pEntityNode != NULL)
	{
		pLoopUnit = ::getUnit(pEntityNode->m_data);
		pEntityNode = nextUnitNode(pEntityNode);

		if (pLoopUnit != NULL && !pLoopUnit->noDefensiveBonus())
		{
			int iValue = pLoopUnit->currEffectiveStr(pDefendPlot, NULL) * 100;

			if (pDefendPlot->isCity(true, getTeam()))
			{
				iValue *= 100 + pLoopUnit->cityDefenseModifier();
				iValue /= 100;
			}

			iValue *= 100;
			iValue /= (100 + pLoopUnit->cityAttackModifier() + pLoopUnit->getExtraCityAttackPercent());

			iValue /= 2 + pLoopUnit->getLevel();

			if (iValue > iBestUnitValue)
			{
				iBestUnitValue = iValue;
				pBestUnit = pLoopUnit;
			}
		}
	}

	if (NULL != pBestUnit && getNumUnits() > 1)
	{
		pBestUnit->joinGroup(NULL);
	}

	return pBestUnit;
}


// Protected Functions...

// R&R mod, vetiarvind, max yield import limit - start
bool CvSelectionGroupAI::getIgnoreDangerStatus() const
{
	bool bIgnoreDanger = false;

	CLLNode<IDInfo>* pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (pLoopUnit != NULL && !pLoopUnit->isCargo())
		{
			if (pLoopUnit->isIgnoreDanger())
			{
				bIgnoreDanger = true;
				break;
			}
		}
	}
	return bIgnoreDanger;
}


// R&R mod, vetiarvind, max yield import limit - end
// Private Functions...
// R&R mod, vetiarvind, max yield import limit - start
int CvSelectionGroupAI::estimateYieldsToLoad(const CvCity* pDestinationCity, int maxYieldsToLoad, YieldTypes eYield, int turnsToReach, int alreadyLoaded) const
{
	if(maxYieldsToLoad <= 0) return 0; // R&R mod, vetiarvind, max yield import limit fix
	int yieldsToLoad = maxYieldsToLoad;

	int importLimit = pDestinationCity->getMaxImportAmount(eYield);
	if(importLimit > 0)
	{
		int stored = pDestinationCity->getYieldStored(eYield);
		int yieldRate = pDestinationCity->getYieldRate(eYield);
		yieldsToLoad = std::min(yieldsToLoad,
			std::max(0, importLimit - (stored + alreadyLoaded + yieldRate * turnsToReach)));
	}
	return yieldsToLoad;
}

void CvSelectionGroupAI::unloadToCity(CvCity* pCity, CvUnit* unit, UnloadMode um)
{
	if (um == UnloadMode::NoForce && pCity->getImportsLimit(unit->getYield()) > 0)
	{
		const int totalStored = unit->getYieldStored();
		int toUnload = estimateYieldsToLoad(pCity, totalStored, unit->getYield(), 0, 0);

		// WTP: a slight excess of the import limit is allowed if the slot of the transport becomes free by it (a rest of at most
		// WTP_DETOUR_MIN_SLOT_PERCENT of a slot would keep the whole slot occupied)
		if (toUnload < totalStored && (totalStored - toUnload) * 100 <= WTP_DETOUR_MIN_SLOT_PERCENT * GC.getGameINLINE().getCargoYieldCapacity())
		{
			toUnload = totalStored;
		}

		if (toUnload <= 0)
		{
			return;
		}
		wtpNoteServed(pCity, unit->getYield(), 0); // (delivered: the import waits no more)
		if (toUnload < totalStored)
		{
			unit->unloadStoredAmount(toUnload);
		}
		else
		{
			unit->unload();
		}
	}
	else
	{
		wtpNoteServed(pCity, unit->getYield(), 0);
		unit->unload();
	}
}

// R&R mod, vetiarvind, max yield import limit - end

// <advc.003u> Based on CvSelectionGroup::getHeadUnit
CvUnitAI const* CvSelectionGroupAI::AI_getHeadUnit() const
{
	CLLNode<IDInfo> const* pNode = headUnitNode();
	return (pNode != NULL ? static_cast<CvUnitAI const*>(::getUnit(pNode->m_data)) : NULL);
}


CvUnitAI* CvSelectionGroupAI::AI_getHeadUnit()
{
	CLLNode<IDInfo>* pNode = headUnitNode();
	return (pNode != NULL ? static_cast<CvUnitAI*>(::getUnit(pNode->m_data)) : NULL);
} // </advc.003u>
