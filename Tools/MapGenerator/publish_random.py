"""Generate and validate the Random New World test worlds (seeds 1 to 6) and rebuild the in-game map script.

python Tools/MapGenerator/publish_random.py

The worlds are not part of the mod any more (user 2026-11-23: the in-game map script PrivateMaps/Random_New_World.py
replaced them): each seed is written with its previews to Tools/MapGenerator/out_random/seed<N> and validated there.
Afterwards PrivateMaps/Random_New_World.py is rebuilt (make_mapscript.py, with its self test on seed 1).
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = 'Random New World Massive.ColonizationWBSave'

for seed in range(1, 7):
    out = os.path.join(HERE, 'out_random', 'seed%d' % seed)
    subprocess.check_call([sys.executable, '-I', os.path.join(HERE, 'gen_random.py'), str(seed), out])
    wb = os.path.join(out, NAME)
    subprocess.check_call([sys.executable, '-I', os.path.join(HERE, 'validate.py'), wb])
    print('seed', seed, '->', os.path.normpath(wb))

subprocess.check_call([sys.executable, '-I', os.path.join(HERE, 'make_mapscript.py'), '--test=1'])
