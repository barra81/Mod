# Python 2.4: run the generator of the in-game map script like the game does (_run), with timing and progress
import sys, re, time
src = open(sys.argv[1]).read()
h = src[src.index('## helpers begin'):src.index('## helpers end')]
ns = {}
exec h in ns
def blob(name):
	return ns['_unpack'](re.search(name + ' = """(.*?)"""', src, re.S).group(1))
xml = {'CIV4FeatureInfos.xml': blob('_XML_FEATURES'), 'CIV4BonusInfos.xml': blob('_XML_BONUSES')}
code = compile(blob('_CODE'), 'Random New World generator', 'exec')
t0 = time.time()
def log(*args):
	sys.stdout.write('%6.1f %s\n' % (time.time() - t0, ' '.join([str(a) for a in args])[:160]))
	sys.stdout.flush()
for seed in [int(a) for a in sys.argv[2:]]:
	t0 = time.time()
	g = ns['_namespace'](seed, xml)
	g['_log'] = log
	exec code in g
	log('seed', seed, 'done')
