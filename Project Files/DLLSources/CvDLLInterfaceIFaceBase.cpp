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
	// priority messages are kept in front of the others (in the order they came), the panel shows them at the top
	static bool s_bPriority = false;
	static int s_iNumPriority = 0;
	static int s_iNumPriorityPrevious = 0;
	void setPriority(bool bPriority)
	{
		s_bPriority = bPriority;
	}
	int getNumPriority()
	{
		return s_iNumPriority;
	}
	int getNumPriorityPrevious()
	{
		return s_iNumPriorityPrevious;
	}
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
		if (s_bPriority)
		{
			entries().insert(entries().begin() + s_iNumPriority, kEntry);
			s_iNumPriority++;
		}
		else
		{
			entries().push_back(kEntry);
		}
	}
	// the messages of the turn before (shown on demand by the panel)
	static std::vector<Entry>& previousEntries()
	{
		static std::vector<Entry> aEntries;
		return aEntries;
	}
	void clear()
	{
		if (!entries().empty())
		{
			previousEntries() = entries();
			s_iNumPriorityPrevious = s_iNumPriority;
		}
		entries().clear();
		s_iNumPriority = 0;
	}
	int getNumPrevious()
	{
		return (int)previousEntries().size();
	}
	const CvWString& getPreviousText(int i)
	{
		static const CvWString szEmpty;
		return (i >= 0 && i < getNumPrevious()) ? previousEntries()[i].szText : szEmpty;
	}
	int getPreviousX(int i)
	{
		return (i >= 0 && i < getNumPrevious()) ? previousEntries()[i].iX : -1;
	}
	int getPreviousY(int i)
	{
		return (i >= 0 && i < getNumPrevious()) ? previousEntries()[i].iY : -1;
	}
	// savegame: all the messages as one string (fields separated by control characters)
	static const wchar SEP_FIELD = 1;
	static const wchar SEP_ENTRY = 2;
	static const wchar SEP_SECTION = 3;
	static void appendEntries(CvWString& szData, const std::vector<Entry>& aEntries)
	{
		for (size_t i = 0; i < aEntries.size(); i++)
		{
			szData += aEntries[i].szText;
			szData += SEP_FIELD;
			szData += CvWString::format(L"%d", aEntries[i].iX);
			szData += SEP_FIELD;
			szData += CvWString::format(L"%d", aEntries[i].iY);
			szData += SEP_ENTRY;
		}
	}
	CvWString serialize()
	{
		CvWString szData;
		szData += CvWString::format(L"%d", s_iNumPriority);
		szData += SEP_SECTION;
		szData += CvWString::format(L"%d", s_iNumPriorityPrevious);
		szData += SEP_SECTION;
		appendEntries(szData, entries());
		szData += SEP_SECTION;
		appendEntries(szData, previousEntries());
		return szData;
	}
	static void parseEntries(const CvWString& szSection, std::vector<Entry>& aEntries)
	{
		aEntries.clear();
		size_t iPos = 0;
		while (iPos < szSection.length())
		{
			size_t iEnd = szSection.find(SEP_ENTRY, iPos);
			if (iEnd == CvWString::npos)
			{
				break;
			}
			CvWString szEntry = szSection.substr(iPos, iEnd - iPos);
			iPos = iEnd + 1;
			size_t iX = szEntry.rfind(SEP_FIELD);
			if (iX == CvWString::npos || iX == 0)
			{
				continue;
			}
			size_t iText = szEntry.rfind(SEP_FIELD, iX - 1);
			if (iText == CvWString::npos)
			{
				continue;
			}
			Entry kEntry;
			kEntry.szText = szEntry.substr(0, iText);
			kEntry.iX = (int)wcstol(szEntry.substr(iText + 1, iX - iText - 1).c_str(), NULL, 10);
			kEntry.iY = (int)wcstol(szEntry.substr(iX + 1).c_str(), NULL, 10);
			aEntries.push_back(kEntry);
		}
	}
	void deserialize(const CvWString& szData)
	{
		entries().clear();
		previousEntries().clear();
		s_iNumPriority = 0;
		s_iNumPriorityPrevious = 0;
		s_bPriority = false;
		if (szData.empty())
		{
			return;
		}
		CvWString aszSection[4];
		size_t iPos = 0;
		for (int i = 0; i < 4; i++)
		{
			size_t iEnd = szData.find(SEP_SECTION, iPos);
			if (iEnd == CvWString::npos)
			{
				aszSection[i] = szData.substr(iPos);
				break;
			}
			aszSection[i] = szData.substr(iPos, iEnd - iPos);
			iPos = iEnd + 1;
		}
		parseEntries(aszSection[2], entries());
		parseEntries(aszSection[3], previousEntries());
		s_iNumPriority = std::min((int)wcstol(aszSection[0].c_str(), NULL, 10), (int)entries().size());
		s_iNumPriorityPrevious = std::min((int)wcstol(aszSection[1].c_str(), NULL, 10), (int)previousEntries().size());
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
		// the sound of a message is played here because a message that is only logged has none, so every message plays its own sound as before
		if (pszSound != NULL && pszSound[0] != 0)
		{
			playGeneralSound(pszSound);
		}
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
