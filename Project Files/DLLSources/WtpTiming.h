#pragma once

#ifndef WTP_TIMING_H
#define WTP_TIMING_H

// WTP: lightweight turn timing + runtime settings (no rebuild needed to switch).
//
// Writes "WTP_Timing.txt" into the mod folder: one block per turn change with the time (ms) spent in the big parts of the
// turn processing (inclusive times, nested parts overlap on purpose, e.g. path searches are also part of the unit AI).
// Only the main thread is measured, worker threads are ignored, so the timing itself never touches shared data.
//
// Reads "WTP_Settings.txt" from the mod folder at every turn change (created with defaults when missing), so values can be
// changed while the game is running:
//   PathfinderParallel=1     1 = child nodes of the path search are expanded with TBB, 0 = always serial (default, faster in the measurements)
//   PathfinderMinChildren=0  parallel only when at least this many child nodes have to be expanded in one step
//
// Remove the following define to compile all timing out. The settings keep working.
#define WTP_TIMING

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
		SLOT_COUNT
	};

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
		"  in AI_doTurnPre: AI_logStatusSummary"
	};

	struct Data
	{
		bool bInit;
		DWORD iMainThread;
		__int64 iFrequency;
		__int64 aiTicks[SLOT_COUNT];
		__int64 aiCalls[SLOT_COUNT];
		int aiDepth[SLOT_COUNT];
		__int64 aiUnitTicks[2][NUM_UNITAI_TYPES + 1];
		__int64 aiUnitCalls[2][NUM_UNITAI_TYPES + 1];
		int iPathfinderParallel;
		int iPathfinderMinChildren;
	};

	inline Data& data()
	{
		static Data kData; // zero initialized
		if (!kData.bInit)
		{
			kData.bInit = true;
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
	class Scope
	{
	public:
		explicit Scope(Slot eSlot) : m_eSlot(eSlot), m_iStart(0), m_bActive(false)
		{
			Data& kData = data();
			if (kData.iMainThread != 0 && kData.iMainThread == GetCurrentThreadId())
			{
				m_bActive = true;
				if (kData.aiDepth[m_eSlot]++ == 0)
				{
					m_iStart = now();
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
					kData.aiTicks[m_eSlot] += now() - m_iStart;
				}
			}
		}
	private:
		Slot m_eSlot;
		__int64 m_iStart;
		bool m_bActive;
	};

	// one entry per unit AI type (natives separately)
	class UnitScope
	{
	public:
		UnitScope(int iUnitAI, bool bNative) : m_iUnitAI(iUnitAI), m_iNative(bNative ? 1 : 0), m_iStart(0), m_bActive(false)
		{
			Data& kData = data();
			if (kData.iMainThread != 0 && kData.iMainThread == GetCurrentThreadId())
			{
				if (m_iUnitAI < 0 || m_iUnitAI >= NUM_UNITAI_TYPES)
				{
					m_iUnitAI = NUM_UNITAI_TYPES;
				}
				m_bActive = true;
				m_iStart = now();
			}
		}
		~UnitScope()
		{
			if (m_bActive)
			{
				Data& kData = data();
				kData.aiUnitCalls[m_iNative][m_iUnitAI]++;
				kData.aiUnitTicks[m_iNative][m_iUnitAI] += now() - m_iStart;
			}
		}
	private:
		int m_iUnitAI;
		int m_iNative;
		__int64 m_iStart;
		bool m_bActive;
	};
#else
	class Scope
	{
	public:
		explicit Scope(Slot) {}
	};
	class UnitScope
	{
	public:
		UnitScope(int, bool) {}
	};
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
			return;
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
				fprintf(f, "=== Turn change at game turn %d | PathfinderParallel=%d PathfinderMinChildren=%d ===\n",
					iGameTurn, kData.iPathfinderParallel, kData.iPathfinderMinChildren);
				fprintf(f, "ms\tcalls\tms/call\tname (inclusive, parts overlap)\n");
				for (int i = 0; i < SLOT_COUNT; i++)
				{
					if (kData.aiCalls[i] > 0)
					{
						const double dTotal = (double)kData.aiTicks[i] * dMs;
						fprintf(f, "%.1f\t%I64d\t%.3f\t%s\n", dTotal, kData.aiCalls[i], dTotal / (double)kData.aiCalls[i], g_aszSlotNames[i]);
					}
				}
				for (int iNative = 0; iNative < 2; iNative++)
				{
					for (int iAI = 0; iAI <= NUM_UNITAI_TYPES; iAI++)
					{
						if (kData.aiUnitCalls[iNative][iAI] > 0)
						{
							const double dTotal = (double)kData.aiUnitTicks[iNative][iAI] * dMs;
							const char* szType = (iAI < NUM_UNITAI_TYPES) ? GC.getUnitAIInfo((UnitAITypes)iAI).getType() : "unknown";
							fprintf(f, "%.1f\t%I64d\t%.3f\tCvUnitAI::AI_update unitAI %s%s\n", dTotal, kData.aiUnitCalls[iNative][iAI],
								dTotal / (double)kData.aiUnitCalls[iNative][iAI], szType, iNative ? " (native)" : "");
						}
					}
				}
				fprintf(f, "\n");
				fclose(f);
			}
		}

		memset(kData.aiTicks, 0, sizeof(kData.aiTicks));
		memset(kData.aiCalls, 0, sizeof(kData.aiCalls));
		memset(kData.aiUnitTicks, 0, sizeof(kData.aiUnitTicks));
		memset(kData.aiUnitCalls, 0, sizeof(kData.aiUnitCalls));
		// aiDepth is not reset, scopes may be open (flush runs inside nothing, but stay safe)
#endif
	}
}

#endif // WTP_TIMING_H
