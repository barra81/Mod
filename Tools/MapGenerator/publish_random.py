"""Generate the playable Random New World maps (seeds 1 to 6), validate them and copy them to PrivateMaps.

python Tools/MapGenerator/publish_random.py

Seed 1 -> PrivateMaps/Random New World Massive.ColonizationWBSave
Seed 2 -> PrivateMaps/Random New World 2 Massive.ColonizationWBSave
Seed N (3-6) -> PrivateMaps/Random New World N Massive.ColonizationWBSave
Previews of each seed stay in Tools/MapGenerator/out_random/seed<N>.
Afterwards the in-game map script PrivateMaps/Random_New_World.py is rebuilt (make_mapscript.py, with its self test on seed 1).
"""
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PRIVATE = os.path.join(HERE, '..', '..', 'PrivateMaps')
NAME = 'Random New World Massive.ColonizationWBSave'
SEEDS = {1: NAME}
SEEDS.update((seed, 'Random New World %d Massive.ColonizationWBSave' % seed) for seed in range(2, 7))

for seed, target in sorted(SEEDS.items()):
    out = os.path.join(HERE, 'out_random', 'seed%d' % seed)
    subprocess.check_call([sys.executable, '-I', os.path.join(HERE, 'gen_random.py'), str(seed), out])
    wb = os.path.join(out, NAME)
    subprocess.check_call([sys.executable, '-I', os.path.join(HERE, 'validate.py'), wb])
    shutil.copyfile(wb, os.path.join(PRIVATE, target))
    print('seed', seed, '->', os.path.normpath(os.path.join(PRIVATE, target)))

subprocess.check_call([sys.executable, '-I', os.path.join(HERE, 'make_mapscript.py'), '--test=1'])
