##############################################################################
## Random New World - map script for We the People: Resettled
##
## GENERATED FILE - do not edit. Made by Tools/MapGenerator/make_mapscript.py
## from Tools/MapGenerator/gen_random.py (Python 3, rewritten for the
## Python 2.4 of the game and packed below).
##
## Every game makes a new world: plate tectonics, mountain ranges, climate,
## rivers, set pieces, resources and landmark names, Europe in the east
## (Atlantic) and west (Pacific). The size is always 85 x 137 plots.
##############################################################################

from CvPythonExtensions import *
import CvUtil
import base64
import math

gc = CyGlobalContext()
W, H = 85, 137
TOP_LAT, BOTTOM_LAT = 70, -40
_result = None
_signs = None

_CODE = """
@CODE@
"""

_XML_FEATURES = """
@XML_FEATURES@
"""

_XML_BONUSES = """
@XML_BONUSES@
"""

## helpers begin (also run by make_mapscript.py under Python 3 for its self test: keep it valid in both)
import math
import base64
try:
	import __builtin__ as _bi
except ImportError:
	import builtins as _bi


def _unpack(text):
	data = base64.b64decode(text.replace('\n', '').strip())  # not compressed: the game's Python 2.4 has no zlib module
	if not isinstance(data, str):
		data = data.decode('utf-8')                      # Python 3 (self test); in the game it stays a plain str
	return data


def _any(seq):
	for v in seq:
		if v:
			return True
	return False


def _all(seq):
	for v in seq:
		if not v:
			return False
	return True


def _best(args, key, better):
	if len(args) == 1:
		seq = args[0]
	else:
		seq = args
	found = False
	best = None
	best_key = None
	for v in seq:
		k = key(v)
		if not found or better(k, best_key):
			best, best_key, found = v, k, True
	if not found:
		raise ValueError('arg is an empty sequence')
	return best


def _max(*args, **kw):
	key = kw.get('key')
	if key is None:
		return _bi.max(*args)
	return _best(args, key, lambda a, b: a > b)


def _min(*args, **kw):
	key = kw.get('key')
	if key is None:
		return _bi.min(*args)
	return _best(args, key, lambda a, b: a < b)


def _round(x, n=None):
	"""round() of Python 3: an int, halves to the even number."""
	if n is not None:
		return _bi.round(x, n)
	f = math.floor(x)
	d = x - f
	if d > 0.5 or (d == 0.5 and int(f) % 2 == 1):
		f += 1
	return int(f)


_NO_DEFAULT = []


def _next(it, default=_NO_DEFAULT):
	try:
		if hasattr(it, 'next'):
			return it.next()
		return it.__next__()
	except StopIteration:
		if default is _NO_DEFAULT:
			raise
		return default


def _choices(rng, population, weights=None, k=1):
	"""random.choices of Python 3 (same method: cumulative weights, bisection)."""
	n = len(population)
	if weights is None:
		return [population[int(rng.random() * n)] for i in range(k)]
	cum = []
	total = 0
	for w in weights:
		total += w
		cum.append(total)
	out = []
	for i in range(k):
		x = rng.random() * total
		lo, hi = 0, n - 1
		while lo < hi:
			mid = (lo + hi) // 2
			if x < cum[mid]:
				hi = mid
			else:
				lo = mid + 1
		out.append(population[lo])
	return out


class _Counter(dict):
	def __init__(self, data=None):
		dict.__init__(self)
		if data is not None:
			self.update(data)

	def __getitem__(self, key):
		if key in self:
			return dict.__getitem__(self, key)
		return 0

	def update(self, data):
		if hasattr(data, 'items'):
			for k, v in data.items():
				self[k] = self[k] + v
		else:
			for k in data:
				self[k] = self[k] + 1

	def most_common(self, n=None):
		items = list(self.items())
		items.sort(key=lambda kv: -kv[1])
		if n is None:
			return items
		return items[:n]


def _log(*args):
	pass


def _namespace(seed, xml):
	def read_xml(path):
		return xml[path.replace('\\', '/').split('/')[-1]]
	return {'__name__': 'random_new_world', '__file__': 'Random_New_World.py', '_SEED': seed, '_read_xml': read_xml,
	        'any': _any, 'all': _all, 'max': _max, 'min': _min, 'round': _round, 'next': _next, 'Counter': _Counter,
	        '_choices': _choices, '_log': _log}
## helpers end


def _run(seed):
	"""Generate the map; a seed whose map the generator rejects (MapRejected, e.g. a straight dug south channel) is
	followed by the next one."""
	xml = {'CIV4FeatureInfos.xml': _unpack(_XML_FEATURES), 'CIV4BonusInfos.xml': _unpack(_XML_BONUSES)}
	code = compile(_unpack(_CODE), 'Random New World generator', 'exec')
	for attempt in range(50):
		ns = _namespace(seed, xml)
		try:
			exec code in ns
			return ns
		except Exception, e:
			if e.__class__.__name__ != 'MapRejected' or attempt == 49:
				raise
			CvUtil.pyPrint('Random New World: seed %d rejected (%s)' % (seed, e))
			seed = ns['next_seed'](seed)


def _info(prefix, name):
	i = gc.getInfoTypeForString(prefix + name)
	if i < 0:
		CvUtil.pyPrint('Random New World: unknown type %s%s' % (prefix, name))
	return i


def _plot_hash():
	"""A fingerprint of the plot types, to know at the start of the game that the map is still this one."""
	mmap = gc.getMap()
	h = 0
	for i in range(mmap.numPlots()):
		h = (h * 31 + mmap.plotByIndex(i).getPlotType() + 1) % 1000000007
	return h


def getDescription():
	return "TXT_KEY_MAP_SCRIPT_RANDOM_NEW_WORLD_DESCR"


def isAdvancedMap():
	return 0


def isClimateMap():
	return 0


def isSeaLevelMap():
	return 0


def getWrapX():
	return False


def getWrapY():
	return False


def getTopLatitude():
	return TOP_LAT


def getBottomLatitude():
	return BOTTOM_LAT


def getNumCustomMapOptions():
	return 0


def getGridSize(argsList):
	"Colonization: the actual map size. Every world size gives the same 85 x 137 plots"
	if argsList[0] == -1:
		return []
	gc.getMap().setCityCatchmentRadiusMapMaker(1)           # two plot colony radius, the generator plans the sites for it
	return (W, H)


def beforeGeneration():
	gc.getMap().setCityCatchmentRadiusMapMaker(1)


def generatePlotTypes():
	global _result
	NiTextOut("Random New World: plates, ranges, climate, rivers ...")
	seed = gc.getGame().getMapRandNum(1000000000, "Random New World seed")
	_result = _run(seed)
	return list(_result['plot_type'])


def generateTerrainTypes():
	ids = {}
	out = []
	for t in _result['terrain']:
		if t not in ids:
			ids[t] = _info('TERRAIN_', t)
		out.append(ids[t])
	return out


def addRivers():
	r = _result
	mmap = gc.getMap()
	card = [CardinalDirectionTypes.CARDINALDIRECTION_NORTH, CardinalDirectionTypes.CARDINALDIRECTION_EAST,
	        CardinalDirectionTypes.CARDINALDIRECTION_SOUTH, CardinalDirectionTypes.CARDINALDIRECTION_WEST]
	for i, d in r['wofr'].items():
		mmap.plot(i % W, i // W).setWOfRiver(True, card[d])
	for i, d in r['nofr'].items():
		mmap.plot(i % W, i // W).setNOfRiver(True, card[d])


def addLakes():
	return None


def _apply_features():
	mmap = gc.getMap()
	ids = {}
	feature = _result['feature']
	for i in range(W * H):
		f = feature[i]
		if f:
			if f not in ids:
				ids[f] = _info('FEATURE_', f)
			if ids[f] >= 0:
				mmap.plotByIndex(i).setFeatureType(ids[f], 0)


def addFeatures():
	_apply_features()


def afterGeneration():
	"""The game changes water terrain and sets its own Europe before this: put the generated ones back."""
	r = _result
	mmap = gc.getMap()
	ids = {}
	terrain = r['terrain']
	for i in range(W * H):
		t = terrain[i]
		if t not in ids:
			ids[t] = _info('TERRAIN_', t)
		p = mmap.plotByIndex(i)
		if p.getTerrainType() != ids[t]:
			p.setTerrainType(ids[t], False, False)
	_apply_features()
	east = _info('EUROPE_', 'EAST')
	west = _info('EUROPE_', 'WEST')
	europe = r['europe']
	pacific = r['pacific']
	for i in range(W * H):
		p = mmap.plotByIndex(i)
		if europe[i]:
			p.setEurope(east)
		elif pacific[i]:
			p.setEurope(west)
		else:
			p.setEurope(-1)
	for i, imp in r['IMPROVEMENT'].items():
		mmap.plotByIndex(i).setImprovementType(_info('', imp))
	for i, route in r['ROUTE'].items():
		mmap.plotByIndex(i).setRouteType(_info('', route))
	# the signs can only be set once the game runs: CvEventManager.onGameStart calls placeMapSigns
	global _signs
	_signs = (_plot_hash(), list(r['SIGNS']))
	CvUtil.placePendingMapSigns = placeMapSigns


def addBonuses():
	mmap = gc.getMap()
	ids = {}
	for i, b in _result['BONUS'].items():
		if b not in ids:
			ids[b] = _info('BONUS_', b)
		if ids[b] >= 0:
			mmap.plotByIndex(i).setBonusType(ids[b])


def placeMapSigns():
	"""Called by CvEventManager.onGameStart: the landmark signs of the generated map."""
	global _signs
	pending = _signs
	_signs = None
	if not pending or pending[0] != _plot_hash():
		return                                           # another map was made since
	for x, y, caption in pending[1]:
		CyEngine().addSign(gc.getMap().plot(x, y), -1, caption)


def normalizeAddRiver():
	return None


def normalizeRemovePeaks():
	return None


def normalizeAddLakes():
	return None


def normalizeRemoveBadFeatures():
	return None


def normalizeRemoveBadTerrain():
	return None


def normalizeAddFoodBonuses():
	return None


def normalizeAddGoodTerrain():
	return None


def normalizeAddExtras():
	return None
