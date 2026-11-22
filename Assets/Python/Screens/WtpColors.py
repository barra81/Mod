## WTP: the colors of import, export and the raw material states: THE one place for them. Everything that marks goods as exported, imported,
## scarce or missing uses these values, in python through code() / tag(), and the same numbers are in these other places:
##  - the legends of the tooltips (CIV4GameText_TAC_utf8.xml: TXT_KEY_WTP_TIP_STORED_COLORS, ..._PRODUCED_COLORS, ..._PRODUCED_LEGEND_*: [COLOR:r:g:b:a])
##  - the frames around the goods of the import / export window (Assets/Art/interface/screens/traderoutes/WTPFrame*.dds: textures of one pixel)
## If a value changes here, the XML legends and the frame textures have to change with it (see the table in the description of the commit
## that introduced this file).
## A group is a tuple (red, green, blue, alpha); tag() puts a text in it for the text of the game.

RAW_MISSING = (255, 0, 0, 255) # raw materials missing, output reduced
RAW_SCARCE = (255, 140, 0, 255) # raw materials scarce, import needed
RAW_IMPORT_SET = (255, 200, 110, 255) # raw material import set
IMPORT = RAW_IMPORT_SET # the import (the same light orange as "import set")
EXPORT = (255, 240, 0, 255) # the export: golden yellow (the goods of the stored line, the frames, the words in the traders list)

def code(tColor):
	return u"%d,%d,%d,%d" % tColor

def tag(tColor, szText):
	return u"<color=" + code(tColor) + u">" + szText + u"</color>"
