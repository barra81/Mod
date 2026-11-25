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
	// the messages of one player: every human player has his own (hotseat: the panel shows those of the active player only,
	// and the messages that come while another player is active wait in his own list instead of the game's own message area)
	// priority messages are kept in front of the others (in the order they came), the panel shows them at the top
	struct PlayerMessages
	{
		std::vector<Entry> aEntries;
		std::vector<Entry> aPreviousEntries; // the messages of the turn before (shown on demand by the panel)
		int iNumPriority;
		int iNumPriorityPrevious;
		PlayerMessages() : iNumPriority(0), iNumPriorityPrevious(0) {}
		bool empty() const
		{
			return aEntries.empty() && aPreviousEntries.empty();
		}
		void reset()
		{
			aEntries.clear();
			aPreviousEntries.clear();
			iNumPriority = 0;
			iNumPriorityPrevious = 0;
		}
	};
	static bool s_bPriority = false;
	static PlayerMessages& messagesOf(PlayerTypes ePlayer)
	{
		static PlayerMessages aMessages[MAX_PLAYERS];
		static PlayerMessages kNone; // NO_PLAYER (no game yet): an empty list, nothing is kept
		if (ePlayer < 0 || ePlayer >= MAX_PLAYERS)
		{
			kNone.reset();
			return kNone;
		}
		return aMessages[ePlayer];
	}
	// the messages that the panel shows: those of the active player
	static PlayerMessages& active()
	{
		return messagesOf(GC.getGameINLINE().getActivePlayer());
	}
	void setPriority(bool bPriority)
	{
		s_bPriority = bPriority;
	}
	// the option "New message panel" of the game options (PLAYEROPTION_MODDER_1, default off)
	static bool isPanelOption(PlayerTypes ePlayer)
	{
		if (GET_PLAYER(ePlayer).isOption(PLAYEROPTION_MODDER_1))
		{
			return true;
		}
		// hotseat / PBEM: the players share one profile, and a player gets its options only when he becomes active (CvGame::setActivePlayer,
		// sendPlayerOptions, after showMissedMessages): before his first turn he does not have them. So the option of any human player counts.
		CvGame& kGame = GC.getGameINLINE();
		if (kGame.isHotSeat() || kGame.isPbem())
		{
			for (int iPlayer = 0; iPlayer < MAX_PLAYERS; iPlayer++)
			{
				const CvPlayer& kPlayer = GET_PLAYER((PlayerTypes)iPlayer);
				if (kPlayer.isHuman() && kPlayer.isOption(PLAYEROPTION_MODDER_1))
				{
					return true;
				}
			}
		}
		return false;
	}
	bool isPanelMessage(PlayerTypes ePlayer, InterfaceMessageTypes eType)
	{
		return (ePlayer > NO_PLAYER && ePlayer < MAX_PLAYERS && GET_PLAYER(ePlayer).isHuman()
			&& GC.getDefineINT("MESSAGE_PANEL_ENABLED") != 0
			&& isPanelOption(ePlayer)
			&& (eType == MESSAGE_TYPE_INFO || eType == MESSAGE_TYPE_DISPLAY_ONLY || eType == MESSAGE_TYPE_MAJOR_EVENT
				|| eType == MESSAGE_TYPE_MINOR_EVENT || eType == MESSAGE_TYPE_COMBAT_MESSAGE));
	}
	int getNumPriority()
	{
		return active().iNumPriority;
	}
	int getNumPriorityPrevious()
	{
		return active().iNumPriorityPrevious;
	}
	void add(PlayerTypes ePlayer, const CvWString& szText, int iX, int iY)
	{
		PlayerMessages& kMessages = messagesOf(ePlayer);
		Entry kEntry;
		kEntry.szText = szText;
		kEntry.iX = iX;
		kEntry.iY = iY;
		if (s_bPriority)
		{
			kMessages.aEntries.insert(kMessages.aEntries.begin() + kMessages.iNumPriority, kEntry);
			kMessages.iNumPriority++;
		}
		else
		{
			kMessages.aEntries.push_back(kEntry);
		}
	}
	void add(const CvWString& szText, int iX, int iY)
	{
		add(GC.getGameINLINE().getActivePlayer(), szText, iX, iY);
	}
	void addTop(const CvWString& szText)
	{
		PlayerMessages& kMessages = active();
		Entry kEntry;
		kEntry.szText = szText;
		kEntry.iX = -1;
		kEntry.iY = -1;
		kMessages.aEntries.insert(kMessages.aEntries.begin(), kEntry);
		kMessages.iNumPriority++;
	}
	void clear(PlayerTypes ePlayer)
	{
		PlayerMessages& kMessages = messagesOf(ePlayer);
		if (!kMessages.aEntries.empty())
		{
			kMessages.aPreviousEntries = kMessages.aEntries;
			kMessages.iNumPriorityPrevious = kMessages.iNumPriority;
		}
		kMessages.aEntries.clear();
		kMessages.iNumPriority = 0;
	}
	int getNum()
	{
		return (int)active().aEntries.size();
	}
	const CvWString& getText(int i)
	{
		static const CvWString szEmpty;
		return (i >= 0 && i < getNum()) ? active().aEntries[i].szText : szEmpty;
	}
	int getX(int i)
	{
		return (i >= 0 && i < getNum()) ? active().aEntries[i].iX : -1;
	}
	int getY(int i)
	{
		return (i >= 0 && i < getNum()) ? active().aEntries[i].iY : -1;
	}
	int getNumPrevious()
	{
		return (int)active().aPreviousEntries.size();
	}
	const CvWString& getPreviousText(int i)
	{
		static const CvWString szEmpty;
		return (i >= 0 && i < getNumPrevious()) ? active().aPreviousEntries[i].szText : szEmpty;
	}
	int getPreviousX(int i)
	{
		return (i >= 0 && i < getNumPrevious()) ? active().aPreviousEntries[i].iX : -1;
	}
	int getPreviousY(int i)
	{
		return (i >= 0 && i < getNumPrevious()) ? active().aPreviousEntries[i].iY : -1;
	}
	// savegame: all the messages as one string (fields separated by control characters)
	// format: for every player with messages SEP_PLAYER, the player id, SEP_PLAYER_DATA and the block of the player (the format of
	// the savegames before the messages per player: four sections, see appendBlock). A string without SEP_PLAYER at the start is
	// such an old block: its messages belong to the active player (the only human player the panel knew).
	static const wchar SEP_FIELD = 1;
	static const wchar SEP_ENTRY = 2;
	static const wchar SEP_SECTION = 3;
	static const wchar SEP_PLAYER = 4;
	static const wchar SEP_PLAYER_DATA = 5;
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
	static void appendBlock(CvWString& szData, const PlayerMessages& kMessages)
	{
		szData += CvWString::format(L"%d", kMessages.iNumPriority);
		szData += SEP_SECTION;
		szData += CvWString::format(L"%d", kMessages.iNumPriorityPrevious);
		szData += SEP_SECTION;
		appendEntries(szData, kMessages.aEntries);
		szData += SEP_SECTION;
		appendEntries(szData, kMessages.aPreviousEntries);
	}
	CvWString serialize()
	{
		CvWString szData;
		for (int iPlayer = 0; iPlayer < MAX_PLAYERS; iPlayer++)
		{
			const PlayerMessages& kMessages = messagesOf((PlayerTypes)iPlayer);
			if (kMessages.empty())
			{
				continue;
			}
			szData += SEP_PLAYER;
			szData += CvWString::format(L"%d", iPlayer);
			szData += SEP_PLAYER_DATA;
			appendBlock(szData, kMessages);
		}
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
	static void parseBlock(const CvWString& szData, PlayerMessages& kMessages)
	{
		kMessages.reset();
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
		parseEntries(aszSection[2], kMessages.aEntries);
		parseEntries(aszSection[3], kMessages.aPreviousEntries);
		kMessages.iNumPriority = std::max(0, std::min((int)wcstol(aszSection[0].c_str(), NULL, 10), (int)kMessages.aEntries.size()));
		kMessages.iNumPriorityPrevious = std::max(0, std::min((int)wcstol(aszSection[1].c_str(), NULL, 10), (int)kMessages.aPreviousEntries.size()));
	}
	void deserialize(const CvWString& szData)
	{
		for (int iPlayer = 0; iPlayer < MAX_PLAYERS; iPlayer++)
		{
			messagesOf((PlayerTypes)iPlayer).reset();
		}
		s_bPriority = false;
		if (szData.empty())
		{
			return;
		}
		if (szData[0] != SEP_PLAYER)
		{
			// a savegame from before the messages per player
			parseBlock(szData, active());
			return;
		}
		size_t iPos = 1;
		while (iPos <= szData.length())
		{
			size_t iEnd = szData.find(SEP_PLAYER, iPos);
			if (iEnd == CvWString::npos)
			{
				iEnd = szData.length();
			}
			CvWString szPlayer = szData.substr(iPos, iEnd - iPos);
			iPos = iEnd + 1;
			size_t iData = szPlayer.find(SEP_PLAYER_DATA);
			if (iData == CvWString::npos)
			{
				continue;
			}
			int iPlayer = (int)wcstol(szPlayer.substr(0, iData).c_str(), NULL, 10);
			if (iPlayer >= 0 && iPlayer < MAX_PLAYERS)
			{
				parseBlock(szPlayer.substr(iData + 1), messagesOf((PlayerTypes)iPlayer));
			}
		}
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
	// (every human player, not only the active one: in hotseat the messages of a player who is not active wait in his own list of the panel;
	// in the game's own message area they would all pop up at once over the panel when his turn starts, see CvPlayer::showMissedMessages)
	if (WtpHudMessages::isPanelMessage(ePlayer, eType))
	{
		WtpHudMessages::add(ePlayer, szString, coord.x(), coord.y());
		// the sound of a message is played here because a message that is only logged has none, so every message plays its own sound as before
		// (only for the active player: the others do not sit at the screen now)
		if (pszSound != NULL && pszSound[0] != 0 && ePlayer == GC.getGameINLINE().getActivePlayer())
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
