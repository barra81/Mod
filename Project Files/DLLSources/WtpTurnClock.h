#pragma once

#ifndef WTP_TURN_CLOCK_H
#define WTP_TURN_CLOCK_H

// WTP: the time the turn change took (shown in the interface below the clock; always on, independent of the timing log WtpTiming.h).
// Measured: everything the game does in CvGame::doTurn and CvGame::updateMoves from one start of CvGame::doTurn to the next (the AI players move, the
// cities and units are processed) = what the player waits for; the time the player needs for the own turn is not in it (updateMoves returns at once while
// the player decides). The animated fights with a human player (the engine plays the animation and the game waits) are taken out: the wall time of a fight
// is subtracted as far as it ran inside one of the two functions. Wall clock, milliseconds.
// Python asks: CyGame.getWtpTurnBlocks() (number of finished blocks of this run of the game, 0 = none yet), getWtpLastTurnMs(), getWtpLastTurnNo().
// The average since the start of the game is made in Python and kept in the savegame (the DLL starts new with every start of the program).
namespace WtpTurnClock
{
	struct Data
	{
		unsigned int iAccumMs; // time in doTurn / updateMoves in this block
		unsigned int iFightMs; // animated fight time inside of it
		int iDepth;
		unsigned int iCallStart;
		bool bFightActive;
		unsigned int iFightStart;
		int iBlocks;
		unsigned int iLastMs;
		int iLastTurn;
	};

	inline Data& data()
	{
		static Data kData = { 0, 0, 0, 0, false, 0, 0, 0, -1 };
		return kData;
	}

	inline unsigned int now()
	{
		return (unsigned int)GetTickCount();
	}

	// at the start of CvGame::doTurn: the block since the last start is finished
	inline void finishBlock(int iGameTurn)
	{
		Data& kData = data();
		if (kData.iAccumMs > 0 && iGameTurn > 1) // (the first turn change of a started game is not measured: nothing comes before it)
		{
			kData.iLastMs = (kData.iAccumMs > kData.iFightMs) ? (kData.iAccumMs - kData.iFightMs) : 0;
			kData.iLastTurn = iGameTurn;
			kData.iBlocks++;
		}
		kData.iAccumMs = 0;
		kData.iFightMs = 0;
	}

	// a savegame is loaded: what was collected is incomplete
	inline void reset()
	{
		Data& kData = data();
		kData.iAccumMs = 0;
		kData.iFightMs = 0;
		kData.iDepth = 0;
		kData.bFightActive = false;
	}

	inline void fightBegin()
	{
		Data& kData = data();
		if (!kData.bFightActive)
		{
			kData.bFightActive = true;
			kData.iFightStart = now();
		}
	}

	inline void fightEnd()
	{
		Data& kData = data();
		if (kData.bFightActive)
		{
			if (kData.iDepth > 0)
			{
				const unsigned int iEnd = now();
				const unsigned int iFrom = (kData.iFightStart > kData.iCallStart) ? kData.iFightStart : kData.iCallStart;
				kData.iFightMs += (iEnd > iFrom) ? (iEnd - iFrom) : 0;
			}
			kData.bFightActive = false;
		}
	}

	// around the bodies of CvGame::doTurn and CvGame::updateMoves
	class Scope
	{
	public:
		Scope()
		{
			Data& kData = data();
			if (kData.iDepth++ == 0)
			{
				kData.iCallStart = now();
			}
		}
		~Scope()
		{
			Data& kData = data();
			if (--kData.iDepth == 0)
			{
				const unsigned int iEnd = now();
				kData.iAccumMs += iEnd - kData.iCallStart;
				if (kData.bFightActive)
				{
					// (a fight that is still running when the function returns: its part inside is counted, the rest starts new)
					const unsigned int iFrom = (kData.iFightStart > kData.iCallStart) ? kData.iFightStart : kData.iCallStart;
					kData.iFightMs += (iEnd > iFrom) ? (iEnd - iFrom) : 0;
					kData.iFightStart = iEnd;
				}
			}
		}
	};
}

#endif
