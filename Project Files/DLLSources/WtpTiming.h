#pragma once

#ifndef WTP_TIMING_H
#define WTP_TIMING_H

#include <time.h>

// WTP: lightweight turn timing + runtime settings (no rebuild needed to switch).
//
// ===========================================================================================================================
// WHAT THIS IS FOR
// ===========================================================================================================================
// In the late game the turn change (all AI players move, cities and units are processed) took 45-70 seconds. This file measures
// where that time goes, so changes can be judged by numbers instead of guesses. It only measures; it changes no game logic.
//
// Output: "WTP_Timing.txt" in the mod folder (appended, one block per turn change, header "=== Turn change at game turn N ... ===").
// The first turn change after the start of the game is not measured; a one-line note "# game started | session=.." stands in the file instead.
// A block covers everything measured since the previous report; the report is written at the start of CvGame::doTurn and the
// turn number in the header is the game turn at that moment.
// Only the main thread is measured; worker threads (TBB) are ignored, so the timing never touches shared data.
// All times are wall clock, in milliseconds. "Inclusive" means a part contains the parts nested in it (they overlap on purpose).
//
// ===========================================================================================================================
// FILE STRUCTURE (made so that logs from many games / players can be merged and still be told apart)
// ===========================================================================================================================
//   ##### WTP timing session | session=.. | started=.. | version=.. | built=.. | build flags:.. | logical cpus=.. | timing format=2 #####
//       one line per start of the game: session id (unique per game start), start time, mod revision (git hash or release version),
//       compile date, compiler flags (e.g. FINAL_RELEASE), number of logical CPUs of the machine.
//   install: game=Colonization.exe version=.. | mod folder=.. | mod release version (changelog.txt)=.. | mod DLL: size, modified
//   files: <folder> <n> files, <bytes>, hash .., last change <time> (<file>)    (Assets\XML, Assets\Python, Assets\Art, PrivateMaps)
//       the game version (file version of the exe, which tells Steam / GOG / patch level apart), the name of the mod folder, the
//       release version of the mod and which DLL is installed, and per folder the number of files, the total size, a hash over
//       (path, size) of all files and the file changed last. The same mod revision with untouched files gives the same numbers,
//       so a different number (or a recent "last change") means the player changed, added or removed files, which can matter for
//       the results (modified XML / Python). Compiled .pyc files are ignored. Not covered: the CustomAssets folder in the user's
//       documents (it can override mod files), other mods, the contents of the files (only name and size are compared).
//   === Turn change at game turn N | PathfinderParallel=.. | format 2 | session=.. | time=.. | version=.. ===
//       one block per turn change. The header repeats session, wall clock time and version, so a block is attributable even if the
//       file was cut or several files were pasted together. Lines starting with "=== Turn change" start a block, "---" lines start
//       a section of a block, "#####" starts a session. Fields are tab separated, the first columns are numbers.
//   The block header also has game=<fingerprint> and continuity=<ok | first report of this session | savegame loaded | other game |
//       turn went back | skipped N turns>. The turn number is the game's own turn (CvGame::getGameTurn), NOT a counter of the log,
//       so playing another savegame in between shows up as a jump or a drop of the turn number. The load of a savegame
//       (CvGame::read) throws away what was collected before and marks the next block "savegame loaded"; a block with a changed
//       fingerprint (different settings / map size / players) is marked "other game". Such blocks carry a "note:" line and should be
//       left out of comparisons and trends (right after a load the caches are empty, so they are slower, not faster).
//       Only the time spent in the measured functions is counted, not the time the human needs for the own turn.
//   Animated fights with a human player (CvUnit::isCombatVisible): the engine plays the animation and the game waits for it. How
//       much of that wait falls into the measured parts depends on the engine, so the log does not guess: it marks every part
//       that overlapped a fight (a fight was running at its start or end, or began / ended inside it) and sums those times in
//       the columns "fight overlap ms" (timed parts, unit AI updates), in the rows "overlapped" of the updateMoves histogram and in
//       the column "animated fight" of the slowest unit updates. The block header has the number of animated fights, a "note:" line
//       the animation wall time. To compare blocks without the influence of fights, subtract the overlap columns or skip blocks
//       with fights.
//   settings: speed=.. handicap=.. world=.. climate=.. sea level=.. multiplayer=..
//       the game settings (XML type names), because the same code behaves very differently on a small and a huge map.
//   When the layout of the report changes, "format" is increased. Parse by the section headers, not by line numbers.
//
// ===========================================================================================================================
// HOW TO READ A BLOCK (report format 2)
// ===========================================================================================================================
//   game:                        map size, living players by type (H human, A AI colony, K king, N native), cities, units.
//   --- timed parts              ms, calls, ms/call and "max ms" (the longest single call) of the big parts of the turn
//                                (see enum Slot / g_aszSlotNames). A long single call can freeze the screen (assumption, not verified in
//                                the engine): the screen can probably only be redrawn between two calls of CvGame::updateMoves.
//   --- single updateMoves calls histogram of the single CvGame::updateMoves calls by duration: how often the screen stood
//                                still for < 50 ms, < 200 ms, < 1 s, < 5 s, longer. (The engine calls updateMoves again and again;
//                                CvUnitAI::AI_update may return true to "wait until the next slice".)
//   --- unit AI updates          CvUnitAI::AI_update per unit AI type (natives separate): total, calls, per call, max.
//   --- path searches by ...     KmodPathFinder::GeneratePath, attributed to the unit AI type that was running when the search
//                                was asked for (only the outermost search is timed, nested ones are not added twice). The line
//                                "paths outside of a unit AI update" is everything else (workforce plan, trade routes, ...).
//   --- slowest single ...       the 8 slowest single unit updates: owner, unit id, plot, unit AI and how much of it was path search.
//   --- per player               per player: doTurn, AI_doTurnPre, AI_doTurnPost, AI_unitUpdate, workforce plan, each as
//                                "ms / calls / longest single call". Use it to see how the cost grows with the number of players.
//   --- counters                 size of the workforce plan problem: colonies, free colonists (workers), free jobs, rounds of
//                                step 3, colony scans in step 3 (the cost of step 3 grows with these).
// The slots SLOT_WF_S0..S5 split CvPlayerAI::AI_doWorkforcePlan into its steps (0 experts without raw material, 1 jobs, 2 workforce,
// 3 set-up of the target plan, 4 seats now, 5 carry out); SLOT_WF_PLAN is the greedy loop of step 3 itself.
//
// ===========================================================================================================================
// WHAT WAS FOUND AND CHANGED SO FAR (history, newest last; numbers are from one late game save, 3 European AIs + natives)
// ===========================================================================================================================
//  1. Pathfinding: KmodPathFinder can expand child nodes with TBB (setting PathfinderParallel). Measured: serial is about 25-30%
//     faster in the late game, so the default is 0 (serial). Pathfinding is still the largest single item (about 16 s per turn
//     change with 250,000-370,000 searches), but the count does not grow steadily with the turns (noisy, no trend).
//  2. AI_doWorkforcePlan (CvPlayerAI, the AI's plan which colonist works which job) was the part that GREW: turns 385-402 went
//     from 26.7 s to 42.4 s (+59%), about 60% of the whole turn change (46 s -> 70 s). Only the European AIs run it, 9-14 s each.
//  3. First suspect, the travel times of the colonies (AI_wfUpdateTravel), was cached; the log showed 0.0 ms for it from turn 398
//     while the plan time kept growing, so it was NOT the cause.
//  4. Cause: step 3 chose ONE (colonist, job) pair per round and scanned all free colonists against all free jobs of all colonies
//     in every round: cost ~ colonists x colonists x jobs. Fix: the candidates are kept per colony and only the colonies an
//     assignment touched are scanned again (the chosen pairs are the same as with the full scan, tie breaks included; checked with
//     a model on random cases, not with the real game). Measured afterwards (turn 404, the only turn logged with the fix):
//     workforce plan 42.4 s -> 4.0 s, turn change 70.5 s -> 28.8 s.
//  5. What is left in the late game (turn 404): AI unit updates 20 s of 29 s; pathfinding ~16 s (285,000 searches);
//     UNITAI_TRANSPORT_SEA ~8 s (125 calls, ~64 ms each) is the biggest unit AI type; CvSelectionGroupAI::AI_tradeRoutes ~6 s.
//     Next candidate: where the sea transports' path searches come from (see "path searches by the unit AI").
//  6. Considered and rejected for now: running AI players or AI_doWorkforcePlan in parallel threads. The game state (map, units,
//     the shared random number generator, the engine's drawing and Python calls) is shared and not thread safe, the order of the
//     players is part of the game rules, and the workforce plan costs only about 1 s per player after the fix. Only read-only
//     computations could be split (as TBB already does for the city job search).
//  7. The long times matter more with more AI players (the tester plays with only 3 opponents because of the turn time): the plan
//     scales about linearly with the number of European AIs, so the per player table is there to measure that.
//
// ===========================================================================================================================
// SETTINGS
// ===========================================================================================================================
// Reads "WTP_Settings.txt" from the mod folder at every turn change (created with defaults when missing), so values can be
// changed while the game is running:
//   PathfinderParallel=1     1 = child nodes of the path search are expanded with TBB, 0 = always serial (default, faster in the measurements)
//   PathfinderMinChildren=0  parallel only when at least this many child nodes have to be expanded in one step
//
// This logging is meant to stay in the mod permanently: it is the basis for judging performance changes and for evaluating logs
// sent in by other players. It is cheap (a few clock reads per call, main thread only, one file write per turn change).
// To switch it off in the code, remove (or comment out) the following define: all Scope / Lap / UnitScope / PlayerScope /
// count / note* calls then compile to nothing and WTP_Timing.txt is no longer written. The settings (WTP_Settings.txt) keep working.
#define WTP_TIMING

// the revision string of the build (defined in CvInitCore.cpp from the autogenerated AutoGitVersion.h)
extern const char* szGitVersion;

namespace WtpTiming
{
	enum Slot
	{
		SLOT_GAME_DOTURN,
		SLOT_GAME_UPDATEMOVES,
		SLOT_MAP_DOTURN,
		SLOT_TEAM_DOTURN,
		SLOT_PLAYER_DOTURN,
		SLOT_PLAYER_DOTURNUNITS,
		SLOT_AI_DOTURNPRE,
		SLOT_AI_DOTURNPOST,
		SLOT_AI_DOTURNUNITSPRE,
		SLOT_AI_DOTURNUNITSPOST,
		SLOT_AI_UNITUPDATE,
		SLOT_CITY_DOTURN,
		SLOT_CITYAI_DOTURN,
		SLOT_ASSIGN_WORKING_PLOTS,
		SLOT_TRADE_ROUTES,
		SLOT_PATH_GENERATE,
		SLOT_PRE_DOCOUNTER,
		SLOT_PRE_DOENEMYUNITDATA,
		SLOT_PRE_DOEMOTIONS,
		SLOT_PRE_DOUNITAIWEIGHTS,
		SLOT_PRE_DOMILITARY,
		SLOT_PRE_DOSTRATEGY,
		SLOT_PRE_UPDATEYIELDVALUES,
		SLOT_PRE_DOCITIZENRELOCATION,
		SLOT_PRE_DOPEACEWARSHIPS,
		SLOT_PRE_UPDATEFULLSTORAGE,
		SLOT_PRE_DOWORKFORCEPLAN,
		SLOT_PRE_DORECLAIMTERRITORY,
		SLOT_PRE_DOSURPLUSPIONEERS,
		SLOT_PRE_DONATIVEMERCDEFENSE,
		SLOT_PRE_LOGSTATUSSUMMARY,
		SLOT_WF_TRAVEL,
		SLOT_WF_PLAN,
		SLOT_WF_S0,
		SLOT_WF_S1,
		SLOT_WF_S2,
		SLOT_WF_S3SETUP,
		SLOT_WF_S4,
		SLOT_WF_S5,
		SLOT_COUNT
	};

	// timed per player (table "per player")
	enum PlayerSlot
	{
		PS_DOTURN,
		PS_AI_DOTURNPRE,
		PS_AI_DOTURNPOST,
		PS_AI_UNITUPDATE,
		PS_WORKFORCEPLAN,
		PS_COUNT
	};

	static const char* const g_aszPlayerSlotNames[PS_COUNT] =
	{
		"doTurn",
		"AI_doTurnPre",
		"AI_doTurnPost",
		"AI_unitUpdate",
		"WorkforcePlan"
	};

	// counters (summed over the turn change)
	enum Counter
	{
		CNT_WF_PLANS,
		CNT_WF_COLONIES,
		CNT_WF_WORKERS,
		CNT_WF_JOBS,
		CNT_WF_ROUNDS,
		CNT_WF_COLONY_SCANS,
		CNT_COUNT
	};

	static const char* const g_aszCounterNames[CNT_COUNT] =
	{
		"workforce plans made (one per AI player)",
		"colonies in the plans",
		"free colonists (workers) in the plans",
		"free jobs in the plans",
		"rounds of step 3 (one pair assigned per round)",
		"colony scans in step 3 (colonies searched again after an assignment)"
	};

	// buckets of the single updateMoves calls (ms, upper limits)
	enum { FREEZE_BUCKETS = 5 };
	static const int g_aiFreezeLimit[FREEZE_BUCKETS] = { 50, 200, 1000, 5000, 0 };

	enum { TOP_UNITS = 8 };

	static const char* const g_aszSlotNames[SLOT_COUNT] =
	{
		"CvGame::doTurn",
		"CvGame::updateMoves",
		"CvMap::doTurn",
		"CvTeam::doTurn",
		"CvPlayer::doTurn",
		"CvPlayer::doTurnUnits",
		"CvPlayerAI::AI_doTurnPre",
		"CvPlayerAI::AI_doTurnPost",
		"CvPlayerAI::AI_doTurnUnitsPre",
		"CvPlayerAI::AI_doTurnUnitsPost",
		"CvPlayerAI::AI_unitUpdate",
		"CvCity::doTurn",
		"CvCityAI::AI_doTurn",
		"CvPlayerAI::AI_assignWorkingPlots",
		"CvSelectionGroupAI::AI_tradeRoutes",
		"KmodPathFinder::GeneratePath (all path searches)",
		"  in AI_doTurnPre: AI_doCounter",
		"  in AI_doTurnPre: AI_doEnemyUnitData",
		"  in AI_doTurnPre: AI_doEmotions",
		"  in AI_doTurnPre: AI_doUnitAIWeights",
		"  in AI_doTurnPre: AI_doMilitary",
		"  in AI_doTurnPre: AI_doStrategy",
		"  in AI_doTurnPre: AI_updateYieldValues",
		"  in AI_doTurnPre: AI_doCitizenRelocation",
		"  in AI_doTurnPre: AI_doPeaceWarships",
		"  in AI_doTurnPre: AI_updateFullStorage",
		"  in AI_doTurnPre: AI_doWorkforcePlan",
		"  in AI_doTurnPre: AI_doReclaimTerritory",
		"  in AI_doTurnPre: AI_doSurplusPioneers",
		"  in AI_doTurnPre: AI_doNativeMercDefense",
		"  in AI_doTurnPre: AI_logStatusSummary",
		"    in AI_doWorkforcePlan: AI_wfUpdateTravel (travel times of the colonies)",
		"    in AI_doWorkforcePlan: target plan (step 3, pairs of colonist and job)",
		"      workforce plan step 0 (experts without raw material)",
		"      workforce plan step 1 (jobs, incl. travel times)",
		"      workforce plan step 2 (workforce)",
		"      workforce plan step 3 set-up (before the pairs are chosen)",
		"      workforce plan step 4 (seats now)",
		"      workforce plan step 5 (carry out)"
	};

	struct Data
	{
		bool bInit;
		DWORD iMainThread;
		__int64 iFrequency;
		__int64 aiTicks[SLOT_COUNT];
		__int64 aiCalls[SLOT_COUNT];
		int aiDepth[SLOT_COUNT];
		__int64 aiMaxTicks[SLOT_COUNT];
		__int64 aiUnitTicks[2][NUM_UNITAI_TYPES + 1];
		__int64 aiUnitCalls[2][NUM_UNITAI_TYPES + 1];
		__int64 aiUnitMaxTicks[2][NUM_UNITAI_TYPES + 1];
		// path searches by the unit AI that was running (index NUM_UNITAI_TYPES: unknown type)
		__int64 aiUnitPathTicks[2][NUM_UNITAI_TYPES + 1];
		__int64 aiUnitPathCalls[2][NUM_UNITAI_TYPES + 1];
		__int64 aiUnitPathMaxTicks[2][NUM_UNITAI_TYPES + 1];
		__int64 iNoUnitPathTicks;
		__int64 iNoUnitPathCalls;
		__int64 iNoUnitPathMaxTicks;
		// the unit AI that is running now (-1: none) and the running totals of the path searches (for the slowest-units table)
		int iCurUnitAI;
		int iCurNative;
		__int64 iPathTicksRun;
		__int64 iPathCallsRun;
		// single updateMoves calls
		__int64 aiFreezeCalls[FREEZE_BUCKETS];
		__int64 aiFreezeTicks[FREEZE_BUCKETS];
		// Animated fights with a human player (isCombatVisible): the engine plays the animation while the game waits. A part
		// "overlaps" a fight when a fight was running at its start or end or began / ended inside it. The times of such parts are
		// summed separately so that they can be left out when numbers are compared.
		bool bFightActive;
		__int64 iFightStart;
		__int64 iFightEpoch; // +1 at every begin and end of a fight
		__int64 iFightCount;
		__int64 iFightWallTicks; // wall time from the start to the end of the animated fights
		__int64 aiFightTicks[SLOT_COUNT];
		__int64 aiFightCalls[SLOT_COUNT];
		__int64 aiUnitFightTicks[2][NUM_UNITAI_TYPES + 1];
		__int64 aiUnitFightCalls[2][NUM_UNITAI_TYPES + 1];
		__int64 aiFreezeFightCalls[FREEZE_BUCKETS];
		__int64 aiFreezeFightTicks[FREEZE_BUCKETS];
		// the slowest single unit updates
		struct TopUnit
		{
			__int64 iTicks;
			__int64 iPathTicks;
			__int64 iPathCalls;
			int iUnitAI;
			int iNative;
			int iOwner;
			int iID;
			int iX;
			int iY;
			bool bFight; // overlapped an animated fight with a human
		};
		TopUnit aTopUnits[TOP_UNITS];
		int iNumTopUnits;
		// per player
		__int64 aiPlayerTicks[PS_COUNT][MAX_PLAYERS];
		__int64 aiPlayerCalls[PS_COUNT][MAX_PLAYERS];
		__int64 aiPlayerMaxTicks[PS_COUNT][MAX_PLAYERS];
		bool abPlayerInfo[MAX_PLAYERS];
		char acPlayerType[MAX_PLAYERS];
		int aiPlayerCities[MAX_PLAYERS];
		int aiPlayerUnits[MAX_PLAYERS];
		char aszPlayerName[MAX_PLAYERS][40];
		int iMapWidth;
		int iMapHeight;
		__int64 aiCounter[CNT_COUNT];
		// identification of the log (see the comment at the top: session, game settings)
		char szSession[48];
		int iLastTurn; // game turn of the previous report, -1: none yet
		unsigned int iLastFingerprint;
		bool bSaveLoaded; // a savegame was loaded since the last report
		bool bSessionWritten;
		bool bGameInfo;
		bool bMultiplayer;
		char szGameSpeed[48];
		char szHandicap[48];
		char szWorldSize[48];
		char szClimate[48];
		char szSeaLevel[48];
		int iPathfinderParallel;
		int iPathfinderMinChildren;
	};

	inline Data& data()
	{
		static Data kData; // zero initialized
		if (!kData.bInit)
		{
			kData.bInit = true;
			kData.iCurUnitAI = -1;
			kData.iCurNative = 0;
			kData.iLastTurn = -1;
			kData.iPathfinderParallel = 0; // measured: serial is about 25-30% faster in the late game
			kData.iPathfinderMinChildren = 0;
			LARGE_INTEGER kFreq;
			kFreq.QuadPart = 0;
			QueryPerformanceFrequency(&kFreq);
			kData.iFrequency = (kFreq.QuadPart > 0) ? kFreq.QuadPart : 1;
		}
		return kData;
	}

	inline __int64 now()
	{
		LARGE_INTEGER kNow;
		kNow.QuadPart = 0;
		QueryPerformanceCounter(&kNow);
		return kNow.QuadPart;
	}

	// settings, used by the path finder (read on the main thread only at turn change, plain ints are fine)
	inline bool pathfinderParallel(size_t iNumChildren)
	{
		const Data& kData = data();
		return kData.iPathfinderParallel != 0 && (int)iNumChildren >= kData.iPathfinderMinChildren;
	}

#ifdef WTP_TIMING
	inline void addFreeze(__int64 iTicks, bool bFight)
	{
		Data& kData = data();
		const double dMs = 1000.0 * (double)iTicks / (double)kData.iFrequency;
		int iBucket = FREEZE_BUCKETS - 1;
		for (int i = 0; i < FREEZE_BUCKETS - 1; i++)
		{
			if (dMs < (double)g_aiFreezeLimit[i])
			{
				iBucket = i;
				break;
			}
		}
		if (bFight)
		{
			kData.aiFreezeFightCalls[iBucket]++;
			kData.aiFreezeFightTicks[iBucket] += iTicks;
		}
		else
		{
			kData.aiFreezeCalls[iBucket]++;
			kData.aiFreezeTicks[iBucket] += iTicks;
		}
	}

	// the animated fight with a human starts / ends (CvUnit::updateCombat, CvUnit::setCombatUnit)
	inline void fightBegin()
	{
		Data& kData = data();
		if (kData.iMainThread != 0 && kData.iMainThread == GetCurrentThreadId() && !kData.bFightActive)
		{
			kData.bFightActive = true;
			kData.iFightStart = now();
			kData.iFightEpoch++;
		}
	}

	inline void fightEnd()
	{
		Data& kData = data();
		if (kData.bFightActive && kData.iMainThread == GetCurrentThreadId())
		{
			kData.bFightActive = false;
			kData.iFightCount++;
			kData.iFightWallTicks += now() - kData.iFightStart;
			kData.iFightEpoch++;
		}
	}

	// a path search (outermost call) ended: add it to the unit AI that asked for it
	inline void addPathSearch(__int64 iTicks)
	{
		Data& kData = data();
		kData.iPathTicksRun += iTicks;
		kData.iPathCallsRun++;
		if (kData.iCurUnitAI >= 0)
		{
			kData.aiUnitPathTicks[kData.iCurNative][kData.iCurUnitAI] += iTicks;
			kData.aiUnitPathCalls[kData.iCurNative][kData.iCurUnitAI]++;
			if (iTicks > kData.aiUnitPathMaxTicks[kData.iCurNative][kData.iCurUnitAI])
			{
				kData.aiUnitPathMaxTicks[kData.iCurNative][kData.iCurUnitAI] = iTicks;
			}
		}
		else
		{
			kData.iNoUnitPathTicks += iTicks;
			kData.iNoUnitPathCalls++;
			if (iTicks > kData.iNoUnitPathMaxTicks)
			{
				kData.iNoUnitPathMaxTicks = iTicks;
			}
		}
	}

	class Scope
	{
	public:
		explicit Scope(Slot eSlot) : m_eSlot(eSlot), m_iStart(0), m_iEpoch(0), m_bFightAtOpen(false), m_bActive(false)
		{
			Data& kData = data();
			if (kData.iMainThread != 0 && kData.iMainThread == GetCurrentThreadId())
			{
				m_bActive = true;
				if (kData.aiDepth[m_eSlot]++ == 0)
				{
					m_iStart = now();
					m_iEpoch = kData.iFightEpoch;
					m_bFightAtOpen = kData.bFightActive;
				}
			}
		}
		~Scope()
		{
			if (m_bActive)
			{
				Data& kData = data();
				kData.aiCalls[m_eSlot]++;
				if (--kData.aiDepth[m_eSlot] == 0)
				{
					const __int64 iTicks = now() - m_iStart;
					kData.aiTicks[m_eSlot] += iTicks;
					if (iTicks > kData.aiMaxTicks[m_eSlot])
					{
						kData.aiMaxTicks[m_eSlot] = iTicks;
					}
					const bool bFight = m_bFightAtOpen || kData.bFightActive || kData.iFightEpoch != m_iEpoch;
					if (bFight)
					{
						kData.aiFightTicks[m_eSlot] += iTicks;
						kData.aiFightCalls[m_eSlot]++;
					}
					if (m_eSlot == SLOT_GAME_UPDATEMOVES)
					{
						addFreeze(iTicks, bFight);
					}
					else if (m_eSlot == SLOT_PATH_GENERATE)
					{
						addPathSearch(iTicks);
					}
				}
			}
		}
	private:
		Slot m_eSlot;
		__int64 m_iStart;
		__int64 m_iEpoch;
		bool m_bFightAtOpen;
		bool m_bActive;
	};

	// consecutive parts of one function: next() ends the part that runs and starts the next one, the destructor ends the last one
	// (also on an early return). Use it for slots that are not nested in a Scope of the same slot.
	class Lap
	{
	public:
		explicit Lap(Slot eSlot) : m_eSlot(eSlot), m_iStart(0), m_bActive(false)
		{
			open();
		}
		void next(Slot eSlot)
		{
			close();
			m_eSlot = eSlot;
			open();
		}
		~Lap()
		{
			close();
		}
	private:
		void open()
		{
			Data& kData = data();
			if (kData.iMainThread != 0 && kData.iMainThread == GetCurrentThreadId())
			{
				m_bActive = true;
				m_iStart = now();
			}
		}
		void close()
		{
			if (m_bActive)
			{
				Data& kData = data();
				const __int64 iTicks = now() - m_iStart;
				kData.aiCalls[m_eSlot]++;
				kData.aiTicks[m_eSlot] += iTicks;
				if (iTicks > kData.aiMaxTicks[m_eSlot])
				{
					kData.aiMaxTicks[m_eSlot] = iTicks;
				}
				m_bActive = false;
			}
		}
		Slot m_eSlot;
		__int64 m_iStart;
		bool m_bActive;
	};

	// one entry per unit AI type (natives separately)
	class UnitScope
	{
	public:
		UnitScope(int iUnitAI, bool bNative, int iOwner, int iID, int iX, int iY)
			: m_iUnitAI(iUnitAI), m_iNative(bNative ? 1 : 0), m_iOwner(iOwner), m_iID(iID), m_iX(iX), m_iY(iY), m_iStart(0),
			m_iPathTicks(0), m_iPathCalls(0), m_iEpoch(0), m_bFightAtOpen(false), m_iPrevAI(-1), m_iPrevNative(0), m_bActive(false)
		{
			Data& kData = data();
			if (kData.iMainThread != 0 && kData.iMainThread == GetCurrentThreadId())
			{
				if (m_iUnitAI < 0 || m_iUnitAI >= NUM_UNITAI_TYPES)
				{
					m_iUnitAI = NUM_UNITAI_TYPES;
				}
				m_bActive = true;
				m_iPrevAI = kData.iCurUnitAI;
				m_iPrevNative = kData.iCurNative;
				kData.iCurUnitAI = m_iUnitAI;
				kData.iCurNative = m_iNative;
				m_iPathTicks = kData.iPathTicksRun;
				m_iPathCalls = kData.iPathCallsRun;
				m_iEpoch = kData.iFightEpoch;
				m_bFightAtOpen = kData.bFightActive;
				m_iStart = now();
			}
		}
		~UnitScope()
		{
			if (m_bActive)
			{
				Data& kData = data();
				const __int64 iTicks = now() - m_iStart;
				kData.aiUnitCalls[m_iNative][m_iUnitAI]++;
				kData.aiUnitTicks[m_iNative][m_iUnitAI] += iTicks;
				if (iTicks > kData.aiUnitMaxTicks[m_iNative][m_iUnitAI])
				{
					kData.aiUnitMaxTicks[m_iNative][m_iUnitAI] = iTicks;
				}
				kData.iCurUnitAI = m_iPrevAI;
				kData.iCurNative = m_iPrevNative;
				const bool bFight = m_bFightAtOpen || kData.bFightActive || kData.iFightEpoch != m_iEpoch;
				if (bFight)
				{
					kData.aiUnitFightTicks[m_iNative][m_iUnitAI] += iTicks;
					kData.aiUnitFightCalls[m_iNative][m_iUnitAI]++;
				}

				// the slowest single updates: keep the TOP_UNITS longest
				int iSlot = -1;
				if (kData.iNumTopUnits < TOP_UNITS)
				{
					iSlot = kData.iNumTopUnits++;
				}
				else
				{
					__int64 iMin = kData.aTopUnits[0].iTicks;
					int iMinIndex = 0;
					for (int i = 1; i < TOP_UNITS; i++)
					{
						if (kData.aTopUnits[i].iTicks < iMin)
						{
							iMin = kData.aTopUnits[i].iTicks;
							iMinIndex = i;
						}
					}
					if (iTicks > iMin)
					{
						iSlot = iMinIndex;
					}
				}
				if (iSlot >= 0)
				{
					Data::TopUnit& kTop = kData.aTopUnits[iSlot];
					kTop.iTicks = iTicks;
					kTop.iPathTicks = kData.iPathTicksRun - m_iPathTicks;
					kTop.iPathCalls = kData.iPathCallsRun - m_iPathCalls;
					kTop.iUnitAI = m_iUnitAI;
					kTop.iNative = m_iNative;
					kTop.iOwner = m_iOwner;
					kTop.iID = m_iID;
					kTop.iX = m_iX;
					kTop.iY = m_iY;
					kTop.bFight = bFight;
				}
			}
		}
	private:
		int m_iUnitAI;
		int m_iNative;
		int m_iOwner;
		int m_iID;
		int m_iX;
		int m_iY;
		__int64 m_iStart;
		__int64 m_iPathTicks;
		__int64 m_iPathCalls;
		__int64 m_iEpoch;
		bool m_bFightAtOpen;
		int m_iPrevAI;
		int m_iPrevNative;
		bool m_bActive;
	};

	// time of one part per player
	class PlayerScope
	{
	public:
		PlayerScope(PlayerSlot eSlot, int iPlayer) : m_eSlot(eSlot), m_iPlayer(iPlayer), m_iStart(0), m_bActive(false)
		{
			Data& kData = data();
			if (kData.iMainThread != 0 && kData.iMainThread == GetCurrentThreadId() && iPlayer >= 0 && iPlayer < MAX_PLAYERS)
			{
				m_bActive = true;
				m_iStart = now();
			}
		}
		~PlayerScope()
		{
			if (m_bActive)
			{
				Data& kData = data();
				const __int64 iTicks = now() - m_iStart;
				kData.aiPlayerCalls[m_eSlot][m_iPlayer]++;
				kData.aiPlayerTicks[m_eSlot][m_iPlayer] += iTicks;
				if (iTicks > kData.aiPlayerMaxTicks[m_eSlot][m_iPlayer])
				{
					kData.aiPlayerMaxTicks[m_eSlot][m_iPlayer] = iTicks;
				}
			}
		}
	private:
		PlayerSlot m_eSlot;
		int m_iPlayer;
		__int64 m_iStart;
		bool m_bActive;
	};

	inline void count(Counter eCounter, __int64 iValue)
	{
		Data& kData = data();
		if (kData.iMainThread != 0 && kData.iMainThread == GetCurrentThreadId())
		{
			kData.aiCounter[eCounter] += iValue;
		}
	}

	// called at the start of the turn change (CvGame::doTurn) for every living player, before flush
	inline void notePlayer(int iPlayer, char cType, int iCities, int iUnits, const char* szName)
	{
		Data& kData = data();
		if (iPlayer >= 0 && iPlayer < MAX_PLAYERS)
		{
			kData.abPlayerInfo[iPlayer] = true;
			kData.acPlayerType[iPlayer] = cType;
			kData.aiPlayerCities[iPlayer] = iCities;
			kData.aiPlayerUnits[iPlayer] = iUnits;
			strncpy(kData.aszPlayerName[iPlayer], (szName != NULL) ? szName : "", sizeof(kData.aszPlayerName[iPlayer]) - 1);
			kData.aszPlayerName[iPlayer][sizeof(kData.aszPlayerName[iPlayer]) - 1] = 0;
		}
	}

	inline void noteMap(int iWidth, int iHeight)
	{
		Data& kData = data();
		kData.iMapWidth = iWidth;
		kData.iMapHeight = iHeight;
	}

	inline void copyName(char* szTo, size_t iSize, const char* szFrom)
	{
		strncpy(szTo, (szFrom != NULL) ? szFrom : "", iSize - 1);
		szTo[iSize - 1] = 0;
	}

	// called together with noteMap: the settings of the game (type names from the XML, e.g. GAMESPEED_NORMAL)
	inline void noteGame(const char* szGameSpeed, const char* szHandicap, const char* szWorldSize, const char* szClimate, const char* szSeaLevel, bool bMultiplayer)
	{
		Data& kData = data();
		kData.bGameInfo = true;
		kData.bMultiplayer = bMultiplayer;
		copyName(kData.szGameSpeed, sizeof(kData.szGameSpeed), szGameSpeed);
		copyName(kData.szHandicap, sizeof(kData.szHandicap), szHandicap);
		copyName(kData.szWorldSize, sizeof(kData.szWorldSize), szWorldSize);
		copyName(kData.szClimate, sizeof(kData.szClimate), szClimate);
		copyName(kData.szSeaLevel, sizeof(kData.szSeaLevel), szSeaLevel);
	}
#else
	class Scope
	{
	public:
		explicit Scope(Slot) {}
	};
	class Lap
	{
	public:
		explicit Lap(Slot) {}
		void next(Slot) {}
	};
	class UnitScope
	{
	public:
		UnitScope(int, bool, int, int, int, int) {}
	};
	class PlayerScope
	{
	public:
		PlayerScope(PlayerSlot, int) {}
	};
	inline void count(Counter, __int64) {}
	inline void notePlayer(int, char, int, int, const char*) {}
	inline void noteMap(int, int) {}
	inline void noteGame(const char*, const char*, const char*, const char*, const char*, bool) {}
	inline void noteSaveLoaded() {}
	inline void fightBegin() {}
	inline void fightEnd() {}
#endif

#ifdef WTP_TIMING
	// clears everything that is collected for the next report (the player info is noted again before every report and cleared by flush)
	inline void resetAccumulators()
	{
		Data& kData = data();
		memset(kData.aiTicks, 0, sizeof(kData.aiTicks));
		memset(kData.aiCalls, 0, sizeof(kData.aiCalls));
		memset(kData.aiMaxTicks, 0, sizeof(kData.aiMaxTicks));
		memset(kData.aiUnitTicks, 0, sizeof(kData.aiUnitTicks));
		memset(kData.aiUnitCalls, 0, sizeof(kData.aiUnitCalls));
		memset(kData.aiUnitMaxTicks, 0, sizeof(kData.aiUnitMaxTicks));
		memset(kData.aiUnitPathTicks, 0, sizeof(kData.aiUnitPathTicks));
		memset(kData.aiUnitPathCalls, 0, sizeof(kData.aiUnitPathCalls));
		memset(kData.aiUnitPathMaxTicks, 0, sizeof(kData.aiUnitPathMaxTicks));
		kData.iNoUnitPathTicks = 0;
		kData.iNoUnitPathCalls = 0;
		kData.iNoUnitPathMaxTicks = 0;
		kData.iPathTicksRun = 0;
		kData.iPathCallsRun = 0;
		memset(kData.aiFreezeCalls, 0, sizeof(kData.aiFreezeCalls));
		memset(kData.aiFreezeTicks, 0, sizeof(kData.aiFreezeTicks));
		memset(kData.aiFreezeFightCalls, 0, sizeof(kData.aiFreezeFightCalls));
		memset(kData.aiFreezeFightTicks, 0, sizeof(kData.aiFreezeFightTicks));
		memset(kData.aiFightTicks, 0, sizeof(kData.aiFightTicks));
		memset(kData.aiFightCalls, 0, sizeof(kData.aiFightCalls));
		memset(kData.aiUnitFightTicks, 0, sizeof(kData.aiUnitFightTicks));
		memset(kData.aiUnitFightCalls, 0, sizeof(kData.aiUnitFightCalls));
		kData.iFightCount = 0;
		kData.iFightWallTicks = 0;
		kData.iNumTopUnits = 0;
		memset(kData.aiPlayerTicks, 0, sizeof(kData.aiPlayerTicks));
		memset(kData.aiPlayerCalls, 0, sizeof(kData.aiPlayerCalls));
		memset(kData.aiPlayerMaxTicks, 0, sizeof(kData.aiPlayerMaxTicks));
		memset(kData.aiCounter, 0, sizeof(kData.aiCounter));
	}

	// called when a savegame is read (CvGame::read): what was collected so far belongs to the game that was played before, so it is
	// dropped, and the next report is marked as the first one after a load
	inline void noteSaveLoaded()
	{
		Data& kData = data();
		kData.bSaveLoaded = true;
		kData.bFightActive = false;
		resetAccumulators();
	}

	// ---- installation info for the session line (once per start of the game; plain Win32, no extra libraries) ----

	struct FolderScan
	{
		int iFiles;
		__int64 iBytes;
		unsigned int iHash;
		FILETIME kNewest;
		std::string szNewest;
	};

	inline unsigned int hashText(unsigned int iHash, const std::string& szText)
	{
		for (size_t i = 0; i < szText.size(); i++)
		{
			char c = szText[i];
			if (c >= 'A' && c <= 'Z')
			{
				c = (char)(c - 'A' + 'a');
			}
			if (c == '/')
			{
				c = '\\';
			}
			iHash ^= (unsigned int)(unsigned char)c;
			iHash *= 16777619u;
		}
		return iHash;
	}

	// counts the files of a folder (recursive): number, bytes, a hash of (relative path, size) summed over all files (so the order of the
	// directory does not matter) and the file that was changed last. Compiled python files (.pyc/.pyo) are left out, the game writes them.
	inline void scanFolder(const std::string& szRoot, const std::string& szRel, FolderScan& kScan, int iDepth)
	{
		if (iDepth > 16)
		{
			return;
		}
		WIN32_FIND_DATAA kFind;
		HANDLE hFind = FindFirstFileA((szRoot + szRel + "*").c_str(), &kFind);
		if (hFind == INVALID_HANDLE_VALUE)
		{
			return;
		}
		do
		{
			const std::string szName = kFind.cFileName;
			if (szName == "." || szName == "..")
			{
				continue;
			}
			if (kFind.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
			{
				scanFolder(szRoot, szRel + szName + "\\", kScan, iDepth + 1);
				continue;
			}
			if (szName.size() > 4)
			{
				const std::string szEnd = szName.substr(szName.size() - 4);
				if (szEnd == ".pyc" || szEnd == ".pyo" || szEnd == ".PYC")
				{
					continue;
				}
			}
			kScan.iFiles++;
			kScan.iBytes += ((__int64)kFind.nFileSizeHigh << 32) | (__int64)kFind.nFileSizeLow;
			unsigned int iFileHash = hashText(2166136261u, szRel + szName);
			iFileHash ^= (unsigned int)kFind.nFileSizeLow;
			iFileHash *= 16777619u;
			iFileHash ^= (unsigned int)kFind.nFileSizeHigh;
			iFileHash *= 16777619u;
			kScan.iHash += iFileHash;
			if (CompareFileTime(&kFind.ftLastWriteTime, &kScan.kNewest) > 0)
			{
				kScan.kNewest = kFind.ftLastWriteTime;
				kScan.szNewest = szRel + szName;
			}
		} while (FindNextFileA(hFind, &kFind));
		FindClose(hFind);
	}

	inline std::string fileTimeText(const FILETIME& kTime)
	{
		char szText[40];
		szText[0] = 0;
		FILETIME kLocal;
		SYSTEMTIME kSystemTime;
		if (FileTimeToLocalFileTime(&kTime, &kLocal) && FileTimeToSystemTime(&kLocal, &kSystemTime))
		{
			_snprintf(szText, sizeof(szText) - 1, "%04d-%02d-%02d %02d:%02d:%02d", (int)kSystemTime.wYear, (int)kSystemTime.wMonth,
				(int)kSystemTime.wDay, (int)kSystemTime.wHour, (int)kSystemTime.wMinute, (int)kSystemTime.wSecond);
			szText[sizeof(szText) - 1] = 0;
		}
		return szText;
	}

	// size and last write time of a file, "missing" when it is not there
	inline std::string fileInfoText(const std::string& szFile)
	{
		WIN32_FILE_ATTRIBUTE_DATA kData;
		memset(&kData, 0, sizeof(kData));
		if (!GetFileAttributesExA(szFile.c_str(), GetFileExInfoStandard, &kData))
		{
			return "missing";
		}
		char szText[128];
		_snprintf(szText, sizeof(szText) - 1, "%lu bytes, modified %s", (unsigned long)kData.nFileSizeLow, fileTimeText(kData.ftLastWriteTime).c_str());
		szText[sizeof(szText) - 1] = 0;
		return szText;
	}

	// file version of an exe / dll (the game version of Colonization.exe), read with version.dll loaded on demand
	inline std::string fileVersionText(const char* szFile)
	{
		struct FixedInfo
		{
			DWORD dwSignature;
			DWORD dwStrucVersion;
			DWORD dwFileVersionMS;
			DWORD dwFileVersionLS;
			DWORD dwProductVersionMS;
			DWORD dwProductVersionLS;
		};
		typedef DWORD (WINAPI *SizeFn)(const char*, DWORD*);
		typedef BOOL (WINAPI *InfoFn)(const char*, DWORD, DWORD, void*);
		typedef BOOL (WINAPI *QueryFn)(const void*, const char*, void**, unsigned int*);

		std::string szResult = "unknown";
		HMODULE hVersion = LoadLibraryA("version.dll");
		if (hVersion == NULL)
		{
			return szResult;
		}
		SizeFn pSize = (SizeFn)GetProcAddress(hVersion, "GetFileVersionInfoSizeA");
		InfoFn pInfo = (InfoFn)GetProcAddress(hVersion, "GetFileVersionInfoA");
		QueryFn pQuery = (QueryFn)GetProcAddress(hVersion, "VerQueryValueA");
		if (pSize != NULL && pInfo != NULL && pQuery != NULL)
		{
			DWORD iHandle = 0;
			const DWORD iSize = pSize(szFile, &iHandle);
			if (iSize > 0 && iSize < 1000000)
			{
				std::vector<char> aBuffer(iSize);
				if (pInfo(szFile, 0, iSize, &aBuffer[0]))
				{
					void* pValue = NULL;
					unsigned int iLength = 0;
					if (pQuery(&aBuffer[0], "\\", &pValue, &iLength) && pValue != NULL && iLength >= sizeof(FixedInfo))
					{
						const FixedInfo* pFixed = (const FixedInfo*)pValue;
						char szText[96];
						_snprintf(szText, sizeof(szText) - 1, "%u.%u.%u.%u (product %u.%u.%u.%u)",
							(unsigned int)(pFixed->dwFileVersionMS >> 16), (unsigned int)(pFixed->dwFileVersionMS & 0xFFFF),
							(unsigned int)(pFixed->dwFileVersionLS >> 16), (unsigned int)(pFixed->dwFileVersionLS & 0xFFFF),
							(unsigned int)(pFixed->dwProductVersionMS >> 16), (unsigned int)(pFixed->dwProductVersionMS & 0xFFFF),
							(unsigned int)(pFixed->dwProductVersionLS >> 16), (unsigned int)(pFixed->dwProductVersionLS & 0xFFFF));
						szText[sizeof(szText) - 1] = 0;
						szResult = szText;
					}
				}
			}
		}
		FreeLibrary(hVersion);
		return szResult;
	}

	// the first line "Version ..." of changelog.txt of the mod folder (the release version of the mod)
	inline std::string changelogVersion(const std::string& szBase)
	{
		std::string szVersion = "unknown";
		FILE* f = fopen((szBase + "changelog.txt").c_str(), "r");
		if (f != NULL)
		{
			char szLine[256];
			while (fgets(szLine, sizeof(szLine), f) != NULL)
			{
				if (strncmp(szLine, "Version ", 8) == 0)
				{
					szVersion = szLine + 8;
					while (!szVersion.empty() && (szVersion[szVersion.size() - 1] == '\n' || szVersion[szVersion.size() - 1] == '\r' || szVersion[szVersion.size() - 1] == ' '))
					{
						szVersion.erase(szVersion.size() - 1);
					}
					break;
				}
			}
			fclose(f);
		}
		return szVersion;
	}

	// the lines "install:" and "files:" after the session line: game version, mod folder, mod release version, DLL, and the
	// files of the mod (to see whether the player changed anything: same revision + untouched install = same numbers)
	inline void writeInstallInfo(FILE* f, const std::string& szBase)
	{
		char szExe[MAX_PATH + 1];
		szExe[0] = 0;
		GetModuleFileNameA(NULL, szExe, MAX_PATH);
		szExe[MAX_PATH] = 0;
		const char* szExeName = strrchr(szExe, '\\');
		szExeName = (szExeName != NULL) ? szExeName + 1 : szExe;

		std::string szFolder = szBase;
		while (!szFolder.empty() && (szFolder[szFolder.size() - 1] == '\\' || szFolder[szFolder.size() - 1] == '/'))
		{
			szFolder.erase(szFolder.size() - 1);
		}
		const size_t iSlash = szFolder.find_last_of("\\/");
		const std::string szFolderName = (iSlash == std::string::npos) ? szFolder : szFolder.substr(iSlash + 1);

		fprintf(f, "install: game=%s version=%s, %s | mod folder=%s | mod release version (changelog.txt)=%s | mod DLL: %s\n",
			szExeName, fileVersionText(szExe).c_str(), fileInfoText(szExe).c_str(), szFolderName.c_str(),
			changelogVersion(szBase).c_str(), fileInfoText(szBase + "Assets\\CvGameCoreDLL.dll").c_str());

		static const char* const aszFolders[] = { "Assets\\XML\\", "Assets\\Python\\", "Assets\\Art\\", "PrivateMaps\\" };
		for (int i = 0; i < 4; i++)
		{
			FolderScan kScan;
			kScan.iFiles = 0;
			kScan.iBytes = 0;
			kScan.iHash = 0;
			kScan.kNewest.dwLowDateTime = 0;
			kScan.kNewest.dwHighDateTime = 0;
			scanFolder(szBase, aszFolders[i], kScan, 0);
			if (kScan.iFiles == 0)
			{
				fprintf(f, "files: %s none\n", aszFolders[i]);
				continue;
			}
			fprintf(f, "files: %s %d files, %I64d bytes, hash %08x, last change %s (%s)\n", aszFolders[i], kScan.iFiles, kScan.iBytes,
				kScan.iHash, fileTimeText(kScan.kNewest).c_str(), kScan.szNewest.c_str());
		}
	}
#endif

	inline void readSettings(const char* szFile)
	{
		Data& kData = data();
		FILE* f = fopen(szFile, "r");
		if (f == NULL)
		{
			// create the file with defaults so it can be found and edited
			f = fopen(szFile, "w");
			if (f != NULL)
			{
				fprintf(f, "PathfinderParallel=%d\n", kData.iPathfinderParallel);
				fprintf(f, "PathfinderMinChildren=%d\n", kData.iPathfinderMinChildren);
				fclose(f);
			}
			return;
		}
		char szLine[256];
		while (fgets(szLine, sizeof(szLine), f) != NULL)
		{
			int iValue = 0;
			if (sscanf(szLine, "PathfinderParallel=%d", &iValue) == 1)
			{
				kData.iPathfinderParallel = iValue;
			}
			else if (sscanf(szLine, "PathfinderMinChildren=%d", &iValue) == 1)
			{
				kData.iPathfinderMinChildren = iValue;
			}
		}
		fclose(f);
	}

	// Call at the start of CvGame::doTurn (main thread): writes the report for everything since the last call, resets, reloads settings.
	inline void flush(int iGameTurn)
	{
		Data& kData = data();
		std::string szBase = gDLL->getModName();

		readSettings((szBase + "WTP_Settings.txt").c_str());

#ifdef WTP_TIMING
		const bool bFirst = (kData.iMainThread == 0);
		kData.iMainThread = GetCurrentThreadId();
		if (bFirst)
		{
			// one id per start of the game (process): lets blocks from several logs / sessions be told apart
			_snprintf(kData.szSession, sizeof(kData.szSession) - 1, "%lx-%lx", (unsigned long)time(NULL), (unsigned long)GetCurrentProcessId());
			kData.szSession[sizeof(kData.szSession) - 1] = 0;
			kData.bSaveLoaded = false;
			// The first turn change of a started game is not measured (nothing came before it, and the first turn after the start of the game
			// takes longer anyway). Only a note, so that nobody wonders why no block follows after the first turn.
			FILE* const pNote = fopen((szBase + "WTP_Timing.txt").c_str(), "a");
			if (pNote != NULL)
			{
				fprintf(pNote, "# game started | session=%s | version=%s | the turn change at game turn %d is not measured (first turn change after the start of the game); the blocks follow from the next turn change on\n",
					kData.szSession, (szGitVersion != NULL) ? szGitVersion : "?", iGameTurn);
				fclose(pNote);
			}
			return;
		}

		char szTime[32];
		{
			time_t kTime = time(NULL);
			const struct tm* pTime = localtime(&kTime);
			szTime[0] = 0;
			if (pTime != NULL)
			{
				strftime(szTime, sizeof(szTime), "%Y-%m-%d %H:%M:%S", pTime);
			}
		}

		bool bAny = false;
		for (int i = 0; i < SLOT_COUNT; i++)
		{
			bAny = bAny || kData.aiCalls[i] > 0;
		}
		if (bAny)
		{
			FILE* f = fopen((szBase + "WTP_Timing.txt").c_str(), "a");
			if (f != NULL)
			{
				const double dMs = 1000.0 / (double)kData.iFrequency;
				if (!kData.bSessionWritten)
				{
					// once per start of the game: build and machine
					kData.bSessionWritten = true;
					SYSTEM_INFO kSystem;
					memset(&kSystem, 0, sizeof(kSystem));
					GetSystemInfo(&kSystem);
					std::string szBuild;
#ifdef FINAL_RELEASE
					szBuild += " FINAL_RELEASE";
#endif
#ifdef NDEBUG
					szBuild += " NDEBUG";
#endif
#ifdef FASSERT_ENABLE
					szBuild += " FASSERT_ENABLE";
#endif
#ifdef HARDCODE_XML_VALUES
					szBuild += " HARDCODE_XML_VALUES";
#endif
#ifdef PROFILING_ENABLED
					szBuild += " PROFILING_ENABLED";
#endif
					fprintf(f, "##### WTP timing session | session=%s | started=%s | version=%s | built=%s %s | build flags:%s | logical cpus=%lu | timing format=2 #####\n",
						kData.szSession, szTime, (szGitVersion != NULL) ? szGitVersion : "?", __DATE__, __TIME__,
						szBuild.empty() ? " (none)" : szBuild.c_str(), (unsigned long)kSystem.dwNumberOfProcessors);
					writeInstallInfo(f, szBase);
				}
				// Is this block comparable with the previous one? The turn number is the game's own (CvGame::getGameTurn), not a
				// counter of the log. A fingerprint of the game (settings, map size, which civilization the human plays) and the load of a
				// savegame tell when another game or save was played in between.
				unsigned int iFingerprint = 2166136261u;
				iFingerprint = hashText(iFingerprint, kData.szGameSpeed);
				iFingerprint = hashText(iFingerprint, kData.szHandicap);
				iFingerprint = hashText(iFingerprint, kData.szWorldSize);
				iFingerprint = hashText(iFingerprint, kData.szClimate);
				iFingerprint = hashText(iFingerprint, kData.szSeaLevel);
				iFingerprint = (iFingerprint ^ (unsigned int)kData.iMapWidth) * 16777619u;
				iFingerprint = (iFingerprint ^ (unsigned int)kData.iMapHeight) * 16777619u;
				for (int iP = 0; iP < MAX_PLAYERS; iP++)
				{
					// (only the human players: AI players die during a game, that must not look like another game)
					if (kData.abPlayerInfo[iP] && kData.acPlayerType[iP] == 'H')
					{
						iFingerprint = (iFingerprint ^ (unsigned int)(iP + 1)) * 16777619u;
						iFingerprint = hashText(iFingerprint, kData.aszPlayerName[iP]);
					}
				}
				char szContinuity[128];
				bool bComparable = true;
				if (kData.iLastTurn < 0)
				{
					strcpy(szContinuity, "first report of this session");
				}
				else if (kData.bSaveLoaded)
				{
					_snprintf(szContinuity, sizeof(szContinuity) - 1, "savegame loaded (turn %d before)", kData.iLastTurn);
					bComparable = false;
				}
				else if (iFingerprint != kData.iLastFingerprint)
				{
					_snprintf(szContinuity, sizeof(szContinuity) - 1, "other game (settings or players differ, turn %d before)", kData.iLastTurn);
					bComparable = false;
				}
				else if (iGameTurn <= kData.iLastTurn)
				{
					_snprintf(szContinuity, sizeof(szContinuity) - 1, "turn went back (turn %d before)", kData.iLastTurn);
					bComparable = false;
				}
				else if (iGameTurn > kData.iLastTurn + 1)
				{
					_snprintf(szContinuity, sizeof(szContinuity) - 1, "skipped %d turns (turn %d before)", iGameTurn - kData.iLastTurn - 1, kData.iLastTurn);
				}
				else
				{
					strcpy(szContinuity, "ok");
				}
				szContinuity[sizeof(szContinuity) - 1] = 0;
				fprintf(f, "=== Turn change at game turn %d | PathfinderParallel=%d PathfinderMinChildren=%d | format 2 | session=%s | time=%s | version=%s | game=%08x | continuity=%s | animated fights with a human=%I64d ===\n",
					iGameTurn, kData.iPathfinderParallel, kData.iPathfinderMinChildren, kData.szSession, szTime,
					(szGitVersion != NULL) ? szGitVersion : "?", iFingerprint, szContinuity, kData.iFightCount);
				if (!bComparable)
				{
					fprintf(f, "note: another game or savegame; the time of this block is not comparable with the blocks before (caches are empty after a load, so it is usually slower, not faster)\n");
				}
				if (kData.iFightCount > 0)
				{
					fprintf(f, "note: %I64d animated fight(s) with a human player in this block (%.0f ms from start to end of the animation). Parts that overlapped a fight are summed in the columns 'fight overlap'; subtract them to compare with blocks without fights.\n",
						kData.iFightCount, (double)kData.iFightWallTicks * 1000.0 / (double)kData.iFrequency);
				}
				kData.iLastTurn = iGameTurn;
				kData.iLastFingerprint = iFingerprint;
				kData.bSaveLoaded = false;
				if (kData.bGameInfo)
				{
					fprintf(f, "settings: speed=%s handicap=%s world=%s climate=%s sea level=%s multiplayer=%d\n",
						kData.szGameSpeed, kData.szHandicap, kData.szWorldSize, kData.szClimate, kData.szSeaLevel, kData.bMultiplayer ? 1 : 0);
				}

				// the game
				int iNumPlayers = 0;
				int iCities = 0;
				int iUnits = 0;
				for (int iP = 0; iP < MAX_PLAYERS; iP++)
				{
					if (kData.abPlayerInfo[iP])
					{
						iNumPlayers++;
						iCities += kData.aiPlayerCities[iP];
						iUnits += kData.aiPlayerUnits[iP];
					}
				}
				fprintf(f, "game: map %d x %d, %d living players (H human, A AI colony, K king, N native), %d cities, %d units\n",
					kData.iMapWidth, kData.iMapHeight, iNumPlayers, iCities, iUnits);

				fprintf(f, "--- timed parts\nms\tcalls\tms/call\tmax ms (longest single call)\tfight overlap ms (part of ms that overlapped an animated fight with a human)\tname (inclusive, parts overlap)\n");
				for (int i = 0; i < SLOT_COUNT; i++)
				{
					if (kData.aiCalls[i] > 0)
					{
						const double dTotal = (double)kData.aiTicks[i] * dMs;
						fprintf(f, "%.1f\t%I64d\t%.3f\t%.1f\t%.1f\t%s\n", dTotal, kData.aiCalls[i], dTotal / (double)kData.aiCalls[i],
							(double)kData.aiMaxTicks[i] * dMs, (double)kData.aiFightTicks[i] * dMs, g_aszSlotNames[i]);
					}
				}

				fprintf(f, "--- single CvGame::updateMoves calls by duration (the screen is frozen during one call)\ncalls\tms\tduration\tanimated fight with a human\n");
				for (int iFight = 0; iFight < 2; iFight++)
				{
					for (int i = 0; i < FREEZE_BUCKETS; i++)
					{
						const __int64 iCalls = iFight ? kData.aiFreezeFightCalls[i] : kData.aiFreezeCalls[i];
						const __int64 iTicks = iFight ? kData.aiFreezeFightTicks[i] : kData.aiFreezeTicks[i];
						if (iCalls > 0)
						{
							if (i < FREEZE_BUCKETS - 1)
							{
								fprintf(f, "%I64d\t%.1f\t< %d ms\t%s\n", iCalls, (double)iTicks * dMs, g_aiFreezeLimit[i], iFight ? "overlapped" : "no");
							}
							else
							{
								fprintf(f, "%I64d\t%.1f\t>= %d ms\t%s\n", iCalls, (double)iTicks * dMs, g_aiFreezeLimit[FREEZE_BUCKETS - 2], iFight ? "overlapped" : "no");
							}
						}
					}
				}

				fprintf(f, "--- unit AI updates\nms\tcalls\tms/call\tmax ms\tfight overlap ms\tname\n");
				for (int iNative = 0; iNative < 2; iNative++)
				{
					for (int iAI = 0; iAI <= NUM_UNITAI_TYPES; iAI++)
					{
						if (kData.aiUnitCalls[iNative][iAI] > 0)
						{
							const double dTotal = (double)kData.aiUnitTicks[iNative][iAI] * dMs;
							const char* szType = (iAI < NUM_UNITAI_TYPES) ? GC.getUnitAIInfo((UnitAITypes)iAI).getType() : "unknown";
							fprintf(f, "%.1f\t%I64d\t%.3f\t%.1f\t%.1f\tCvUnitAI::AI_update unitAI %s%s\n", dTotal, kData.aiUnitCalls[iNative][iAI],
								dTotal / (double)kData.aiUnitCalls[iNative][iAI], (double)kData.aiUnitMaxTicks[iNative][iAI] * dMs,
								(double)kData.aiUnitFightTicks[iNative][iAI] * dMs, szType, iNative ? " (native)" : "");
						}
					}
				}

				fprintf(f, "--- path searches by the unit AI that asked for them (outermost searches; ms only counted once)\nms\tcalls\tms/call\tmax ms\tname\n");
				for (int iNative = 0; iNative < 2; iNative++)
				{
					for (int iAI = 0; iAI <= NUM_UNITAI_TYPES; iAI++)
					{
						if (kData.aiUnitPathCalls[iNative][iAI] > 0)
						{
							const double dTotal = (double)kData.aiUnitPathTicks[iNative][iAI] * dMs;
							const char* szType = (iAI < NUM_UNITAI_TYPES) ? GC.getUnitAIInfo((UnitAITypes)iAI).getType() : "unknown";
							fprintf(f, "%.1f\t%I64d\t%.3f\t%.1f\tpaths in unitAI %s%s\n", dTotal, kData.aiUnitPathCalls[iNative][iAI],
								dTotal / (double)kData.aiUnitPathCalls[iNative][iAI], (double)kData.aiUnitPathMaxTicks[iNative][iAI] * dMs,
								szType, iNative ? " (native)" : "");
						}
					}
				}
				if (kData.iNoUnitPathCalls > 0)
				{
					const double dTotal = (double)kData.iNoUnitPathTicks * dMs;
					fprintf(f, "%.1f\t%I64d\t%.3f\t%.1f\tpaths outside of a unit AI update (workforce plan, trade routes, advisor, ...)\n", dTotal,
						kData.iNoUnitPathCalls, dTotal / (double)kData.iNoUnitPathCalls, (double)kData.iNoUnitPathMaxTicks * dMs);
				}

				if (kData.iNumTopUnits > 0)
				{
					// sort the slowest unit updates, longest first
					for (int i = 0; i < kData.iNumTopUnits; i++)
					{
						for (int j = i + 1; j < kData.iNumTopUnits; j++)
						{
							if (kData.aTopUnits[j].iTicks > kData.aTopUnits[i].iTicks)
							{
								Data::TopUnit kTmp = kData.aTopUnits[i];
								kData.aTopUnits[i] = kData.aTopUnits[j];
								kData.aTopUnits[j] = kTmp;
							}
						}
					}
					fprintf(f, "--- slowest single unit updates\nms\tpath ms\tpath calls\towner\tunit id\tplot x,y\tanimated fight with a human\tunitAI\n");
					for (int i = 0; i < kData.iNumTopUnits; i++)
					{
						const Data::TopUnit& kTop = kData.aTopUnits[i];
						const char* szType = (kTop.iUnitAI < NUM_UNITAI_TYPES) ? GC.getUnitAIInfo((UnitAITypes)kTop.iUnitAI).getType() : "unknown";
						fprintf(f, "%.1f\t%.1f\t%I64d\t%d\t%d\t%d,%d\t%s\t%s%s\n", (double)kTop.iTicks * dMs, (double)kTop.iPathTicks * dMs,
							kTop.iPathCalls, kTop.iOwner, kTop.iID, kTop.iX, kTop.iY, kTop.bFight ? "overlapped" : "no", szType, kTop.iNative ? " (native)" : "");
					}
				}

				fprintf(f, "--- per player (ms / calls / longest single call ms)\nid\ttype\tcivilization\tcities\tunits");
				for (int s2 = 0; s2 < PS_COUNT; s2++)
				{
					fprintf(f, "\t%s", g_aszPlayerSlotNames[s2]);
				}
				fprintf(f, "\n");
				for (int iP = 0; iP < MAX_PLAYERS; iP++)
				{
					bool bPlayerAny = false;
					for (int s2 = 0; s2 < PS_COUNT; s2++)
					{
						bPlayerAny = bPlayerAny || kData.aiPlayerCalls[s2][iP] > 0;
					}
					if (bPlayerAny && kData.abPlayerInfo[iP])
					{
						fprintf(f, "%d\t%c\t%s\t%d\t%d", iP, kData.acPlayerType[iP], kData.aszPlayerName[iP], kData.aiPlayerCities[iP], kData.aiPlayerUnits[iP]);
						for (int s2 = 0; s2 < PS_COUNT; s2++)
						{
							fprintf(f, "\t%.1f / %I64d / %.1f", (double)kData.aiPlayerTicks[s2][iP] * dMs, kData.aiPlayerCalls[s2][iP],
								(double)kData.aiPlayerMaxTicks[s2][iP] * dMs);
						}
						fprintf(f, "\n");
					}
				}

				bool bCounter = false;
				for (int i = 0; i < CNT_COUNT; i++)
				{
					bCounter = bCounter || kData.aiCounter[i] != 0;
				}
				if (bCounter)
				{
					fprintf(f, "--- counters\n");
					for (int i = 0; i < CNT_COUNT; i++)
					{
						fprintf(f, "%I64d\t%s\n", kData.aiCounter[i], g_aszCounterNames[i]);
					}
				}
				fprintf(f, "\n");
				fclose(f);
			}
		}

		resetAccumulators();
		kData.bFightActive = false; // (a fight does not last over a turn change; also guards against a missed end)
		memset(kData.abPlayerInfo, 0, sizeof(kData.abPlayerInfo));
		// aiDepth is not reset, scopes may be open (flush runs inside nothing, but stay safe)
#endif
	}
}

#endif // WTP_TIMING_H
