## WTP: the completion of the search fields (import / export window, Trade Route Manager). One place for both, they only differ in what
## they search for (goods; transports, cities, Europe and goods) and in how the names are ranked (weight: the most used first).
##
## The names are given as a dictionary  lowercase name -> [name, weight].  The completion is made of
##  - the name that starts with the typed text (the heaviest, then the first in the alphabet): its rest is shown in grey behind the cursor,
##  - the "alternative" (shown after an arrow): the next name that starts with the text, or, when none is left, one that has a word
##    starting with it (typed "wood": Exotic Wood).
## Tab takes the completion (or the alternative when there is no completion). The text then is a name of the list and the alternative is the
## next name of the list that was there when Tab was pressed, so pressing Tab again goes through all of them (typed "peaux": first
## Peaux de chevres, then Peaux de porcs). Any other typing starts the list over.

class SearchComplete:

	def __init__(self):
		self.reset()

	def reset(self):
		self.szSuggestion = u"" # the completion (the whole text, starting with what was typed)
		self.szAlt = u"" # the alternative
		self.aCandidates = [] # the names in the order they are offered
		self.aCycle = [] # the names Tab went through
		self.iCycle = 0

	def find(self, szQuery, dCand, aSkip = None):
		self.szSuggestion = u""
		self.szAlt = u""
		self.aCandidates = []
		szLead = szQuery[:len(szQuery) - len(szQuery.lstrip())]
		szLast = szQuery.lstrip().lower()
		if len(szLast) == 0:
			self.aCycle = []
			return
		if len(self.aCycle) > 0 and szLast == self.aCycle[self.iCycle].lower():
			# the text is one of the names Tab went through: the next of them is offered
			self.aCandidates = list(self.aCycle)
			if len(self.aCycle) > 1:
				self.szAlt = self.aCycle[(self.iCycle + 1) % len(self.aCycle)]
			return
		self.aCycle = []
		aPrefix = []
		aWord = []
		for szLower in dCand.keys():
			if szLower == szLast or (aSkip is not None and szLower in aSkip):
				continue
			tEntry = (-dCand[szLower][1], szLower, dCand[szLower][0])
			if szLower[:len(szLast)] == szLast:
				aPrefix.append(tEntry)
			else:
				for szWord in szLower.replace(u"-", u" ").replace(u"'", u" ").split():
					if szWord[:len(szLast)] == szLast:
						aWord.append(tEntry)
						break
		aPrefix.sort()
		aWord.sort()
		for t in aPrefix:
			self.aCandidates.append(t[2])
		for t in aWord:
			self.aCandidates.append(t[2])
		if len(aPrefix) > 0:
			self.szSuggestion = szLead + aPrefix[0][2]
			if len(aPrefix) > 1:
				self.szAlt = aPrefix[1][2]
			elif len(aWord) > 0:
				self.szAlt = aWord[0][2]
		elif len(aWord) > 0:
			self.szAlt = aWord[0][2]

	# Tab: the new text (the completion, or the alternative), None if there is nothing to take. bAlt False: only the completion
	# (the other accept keys of a field do not go through the alternatives)
	def accept(self, szQuery, bAlt = True):
		szTarget = u""
		if len(self.szSuggestion) > len(szQuery):
			szTarget = self.szSuggestion.strip()
		elif bAlt and len(self.szAlt) > 0:
			szTarget = self.szAlt
		if len(szTarget) == 0:
			return None
		if not (len(self.aCycle) > 0 and szQuery.strip().lower() == self.aCycle[self.iCycle].lower()):
			self.aCycle = list(self.aCandidates)
		if szTarget in self.aCycle:
			self.iCycle = self.aCycle.index(szTarget)
		else:
			self.aCycle = []
		return szTarget

	# the text of the field: the typed part, the cursor, the grey rest of the completion and the alternative
	def getText(self, szQuery, szCursor):
		if len(self.szSuggestion) > len(szQuery):
			szText = u"<color=255,255,255>" + self.szSuggestion[:len(szQuery)] + u"</color>" + szCursor + u"<color=130,130,130>" + self.szSuggestion[len(szQuery):] + u"</color>"
		else:
			szText = u"<color=255,255,255>" + szQuery + u"</color>" + szCursor
		if len(self.szAlt) > 0:
			szText += u"<color=130,130,130>   -> " + self.szAlt + u"</color>"
		return szText
