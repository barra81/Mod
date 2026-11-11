/*  <advc.127> Cut and pasted from CvDLLInterfaceIFaceBase.h; this function
	is getting too large for an inline definition. */

#include "CvGameCoreDLL.h"
#include "CvDLLInterfaceIFaceBase.h" // </advc.127>
#include "CvGame.h"
#include "CvPlayer.h"
#include "CvPlot.h"
#include "CvTalkingHeadMessage.h"

// Uncomment this to silence all message output
//#define NO_ADDMESSAGE

namespace WtpHudMessages
{
	struct Entry
	{
		CvWString szText;
		int iX;
		int iY;
	};
	static std::vector<Entry>& entries()
	{
		static std::vector<Entry> aEntries;
		return aEntries;
	}
	void add(const CvWString& szText, int iX, int iY)
	{
		Entry kEntry;
		kEntry.szText = szText;
		kEntry.iX = iX;
		kEntry.iY = iY;
		entries().push_back(kEntry);
	}
	void clear()
	{
		entries().clear();
	}
	int getNum()
	{
		return (int)entries().size();
	}
	const CvWString& getText(int i)
	{
		static const CvWString szEmpty;
		return (i >= 0 && i < getNum()) ? entries()[i].szText : szEmpty;
	}
	int getX(int i)
	{
		return (i >= 0 && i < getNum()) ? entries()[i].iX : -1;
	}
	int getY(int i)
	{
		return (i >= 0 && i < getNum()) ? entries()[i].iY : -1;
	}
}

void CvDLLInterfaceIFaceBase::addPlayerMessage(PlayerTypes ePlayer, bool bForce, int iLength, CvWString szString,
		Coordinates coord, LPCTSTR pszSound, InterfaceMessageTypes eType,
		LPCSTR pszIcon, ColorTypes eFlashColor,
		bool bShowOffScreenArrows, bool bShowOnScreenArrows)
{
#ifndef NO_ADDMESSAGE
	// WTP: the message panel (MESSAGE_PANEL_ENABLED in GlobalDefinesAlt.xml) keeps the messages of the turn for the human player. With
	// MESSAGE_PANEL_HIDE_ENGINE_DISPLAY the game's own message area does not show them (log only, they expire as before, see CvTalkingHeadMessage)
	if (ePlayer != NO_PLAYER && ePlayer == GC.getGameINLINE().getActivePlayer() && GET_PLAYER(ePlayer).isHuman()
		&& GC.getDefineINT("MESSAGE_PANEL_ENABLED") != 0
		&& (eType == MESSAGE_TYPE_INFO || eType == MESSAGE_TYPE_DISPLAY_ONLY || eType == MESSAGE_TYPE_MAJOR_EVENT
			|| eType == MESSAGE_TYPE_MINOR_EVENT || eType == MESSAGE_TYPE_COMBAT_MESSAGE))
	{
		WtpHudMessages::add(szString, coord.x(), coord.y());
		if (GC.getDefineINT("MESSAGE_PANEL_HIDE_ENGINE_DISPLAY") != 0)
		{
			iLength = WTP_HUD_MESSAGE_LENGTH_BASE + (int)eType;
			eType = MESSAGE_TYPE_LOG_ONLY;
		}
	}
	addMessage(ePlayer, bForce, iLength, szString,
		coord, pszSound, eType, pszIcon, eFlashColor,
		bShowOffScreenArrows, bShowOnScreenArrows);
#endif
}

void CvDLLInterfaceIFaceBase::addAllPlayersMessage(bool bForce, int iLength, CvWString szString,
		Coordinates coord, LPCTSTR pszSound, InterfaceMessageTypes eType,
		LPCSTR pszIcon, ColorTypes eFlashColor,
		bool bShowOffScreenArrows, bool bShowOnScreenArrows)
{
	for (PlayerTypes ePlayer = FIRST_PLAYER; ePlayer < NUM_PLAYER_TYPES; ++ePlayer)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER(ePlayer);
		if (kLoopPlayer.isAlive())
		{
			if (coord.plot()->isRevealed(kLoopPlayer.getTeam(), false))
			{
				addPlayerMessage(kLoopPlayer.getID(), bForce, iLength, szString, coord, pszSound, eType,
																		pszIcon, eFlashColor, bShowOffScreenArrows, bShowOnScreenArrows);
			}
		}
	}
}

void CvDLLInterfaceIFaceBase::addOtherPlayersMessage(PlayerTypes eExcludePlayer, bool bForce, int iLength, CvWString szString,
		Coordinates coord, LPCTSTR pszSound, InterfaceMessageTypes eType,
		LPCSTR pszIcon, ColorTypes eFlashColor,
		bool bShowOffScreenArrows, bool bShowOnScreenArrows)
{
	for (PlayerTypes ePlayer = FIRST_PLAYER; ePlayer < NUM_PLAYER_TYPES; ++ePlayer)
	{
		CvPlayer& kLoopPlayer = GET_PLAYER(ePlayer);
		if (ePlayer != eExcludePlayer && kLoopPlayer.isAlive())
		{
			if (coord.plot()->isRevealed(kLoopPlayer.getTeam(), false))
			{
				addPlayerMessage(kLoopPlayer.getID(), bForce, iLength, szString, coord, pszSound, eType,
																		pszIcon, eFlashColor, bShowOffScreenArrows, bShowOnScreenArrows);
			}
		}
	}
}
