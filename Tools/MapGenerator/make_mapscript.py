"""Build the in-game map script "PrivateMaps/Random New World.py" from gen_random.py.

python Tools/MapGenerator/make_mapscript.py

The game runs map scripts with its own Python 2.4. gen_random.py (with noise.py and place_names.py) is Python 3, so this
script rewrites it into Python 2.4 code with the ast module and packs it into the map script, which runs it with exec when
a game starts. The output part of gen_random.py (WBSave, previews, statistics) is left out: the map script hands the result
to the game directly (plot types, terrain, rivers, features, Europe, resources, ruins and roads, landmark signs).

Rewrites: conditional expressions -> (c and [a] or [b])[0]; set literals, set and dict comprehensions -> set()/dict();
math.floor/ceil -> int(...); print(...) -> _log(...); rng.choices(...) -> _choices(rng, ...); open(path).read() of the game
XML -> _read_xml(path). Builtins Python 2.4 lacks or handles differently (any, all, next, round, max/min with key, Counter)
are given to the code by the map script; true division comes from "from __future__ import division".
A check afterwards refuses the output if a construct newer than Python 2.4 is left.

Run it again after every change to gen_random.py (publish_random.py does it).
"""
import ast
import base64
import os
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.normpath(os.path.join(HERE, '..', '..'))
TARGET = os.path.join(MOD, 'PrivateMaps', 'Random New World.py')
OUTPUT_MARK = '# ---------------------------------------------------------------- output'
XML_FILES = {
    'CIV4FeatureInfos.xml': os.path.join(MOD, 'Assets', 'XML', 'Terrain', 'CIV4FeatureInfos.xml'),
    'CIV4BonusInfos.xml': os.path.join(MOD, 'Assets', 'XML', 'Terrain', 'CIV4BonusInfos.xml'),
}
SKIP_IMPORTS = {'noise', 'png', 'place_names'}


def read(name):
    with open(os.path.join(HERE, name), encoding='utf-8') as f:
        return f.read()


class Py24(ast.NodeTransformer):
    def visit_IfExp(self, node):
        self.generic_visit(node)
        pick = ast.BoolOp(op=ast.Or(), values=[
            ast.BoolOp(op=ast.And(), values=[node.test, ast.List(elts=[node.body], ctx=ast.Load())]),
            ast.List(elts=[node.orelse], ctx=ast.Load())])
        return ast.Subscript(value=pick, slice=ast.Constant(0), ctx=ast.Load())

    def visit_Set(self, node):
        self.generic_visit(node)
        return ast.Call(func=ast.Name('set', ast.Load()), args=[ast.List(elts=node.elts, ctx=ast.Load())], keywords=[])

    def visit_SetComp(self, node):
        self.generic_visit(node)
        return ast.Call(func=ast.Name('set', ast.Load()), args=[ast.GeneratorExp(node.elt, node.generators)], keywords=[])

    def visit_DictComp(self, node):
        self.generic_visit(node)
        pair = ast.Tuple(elts=[node.key, node.value], ctx=ast.Load())
        return ast.Call(func=ast.Name('dict', ast.Load()), args=[ast.GeneratorExp(pair, node.generators)], keywords=[])

    def visit_Call(self, node):
        self.generic_visit(node)
        f = node.func
        if isinstance(f, ast.Name) and f.id == 'print':
            node.func = ast.Name('_log', ast.Load())
            node.keywords = []
            return node
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == 'math' and f.attr in ('floor', 'ceil'):
            return ast.Call(func=ast.Name('int', ast.Load()), args=[node], keywords=[])
        if isinstance(f, ast.Attribute) and f.attr == 'choices':
            return ast.Call(func=ast.Name('_choices', ast.Load()), args=[f.value] + node.args, keywords=node.keywords)
        # open(path, encoding=...).read() -> _read_xml(path)
        if (isinstance(f, ast.Attribute) and f.attr == 'read' and isinstance(f.value, ast.Call)
                and isinstance(f.value.func, ast.Name) and f.value.func.id == 'open'):
            return ast.Call(func=ast.Name('_read_xml', ast.Load()), args=f.value.args[:1], keywords=[])
        return node

    def visit_Assign(self, node):
        self.generic_visit(node)
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name == 'SEED':
                node.value = ast.Name('_SEED', ast.Load())
            elif name == 'OUT':
                node.value = ast.Constant(None)
        return node

    def visit_Import(self, node):
        return node

    def visit_ImportFrom(self, node):
        if node.module in SKIP_IMPORTS:
            return None
        if node.module == 'collections':
            node.names = [a for a in node.names if a.name != 'Counter']
            if not node.names:
                return None
        return node

    def visit_Expr(self, node):
        # sys.path.insert(...) is not needed: the helper modules are part of the code
        v = node.value
        if (isinstance(v, ast.Call) and isinstance(v.func, ast.Attribute) and v.func.attr == 'insert'
                and isinstance(v.func.value, ast.Attribute) and v.func.value.attr == 'path'):
            return None
        self.generic_visit(node)
        return node


FORBIDDEN_NODES = (ast.IfExp, ast.Set, ast.SetComp, ast.DictComp, ast.With, ast.JoinedStr, ast.Nonlocal, ast.NamedExpr,
                   ast.YieldFrom, ast.AnnAssign, ast.AsyncFunctionDef, ast.Await)
NEW_METHODS = {'format', 'partition', 'rpartition', 'isdisjoint', 'choices', 'most_common_', 'bit_length', 'casefold'}


def check_py24(tree):
    """Raise if the tree still has syntax or calls that Python 2.4 does not know."""
    problems = []
    for n in ast.walk(tree):
        line = getattr(n, 'lineno', '?')
        if isinstance(n, FORBIDDEN_NODES):
            problems.append('%s: %s' % (line, type(n).__name__))
        if isinstance(n, ast.Try) and n.handlers and n.finalbody:
            problems.append('%s: try/except/finally' % line)
        if isinstance(n, ast.ExceptHandler) and n.name:
            problems.append('%s: except ... as' % line)
        if isinstance(n, (ast.List, ast.Tuple)) and any(isinstance(e, ast.Starred) for e in n.elts):
            problems.append('%s: starred display or assignment' % line)
        if isinstance(n, ast.Dict) and None in n.keys:
            problems.append('%s: ** in dict display' % line)
        if isinstance(n, ast.FunctionDef) and (n.args.kwonlyargs or n.args.posonlyargs or n.returns or n.decorator_list):
            problems.append('%s: function signature' % line)
        if isinstance(n, ast.Call):
            stars = [i for i, a in enumerate(n.args) if isinstance(a, ast.Starred)]
            if stars and (len(stars) > 1 or stars[0] != len(n.args) - 1 or n.keywords):
                problems.append('%s: *args not last or with keywords' % line)
            f = n.func
            if isinstance(f, ast.Attribute):
                if f.attr in NEW_METHODS:
                    problems.append('%s: .%s()' % (line, f.attr))
                if f.attr in ('startswith', 'endswith') and n.args and not isinstance(n.args[0], ast.Constant):
                    problems.append('%s: .%s() with a non-literal (tuple?) argument' % (line, f.attr))
                if f.attr in ('union', 'intersection', 'difference', 'update') and len(n.args) > 1:
                    problems.append('%s: .%s() with several arguments' % (line, f.attr))
                if isinstance(f.value, ast.Name) and f.value.id == 'os' and f.attr == 'makedirs':
                    problems.append('%s: os.makedirs' % line)
            if isinstance(f, ast.Name):
                if f.id in ('open', 'print', 'exec', 'enumerate') and (f.id != 'enumerate' or len(n.args) > 1):
                    problems.append('%s: %s()' % (line, f.id))
                if f.id in ('max', 'min', 'sorted') and any(k.arg == 'default' for k in n.keywords):
                    problems.append('%s: %s(default=)' % (line, f.id))
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and any(ord(c) > 127 for c in n.value):
            problems.append('%s: non-ASCII string' % line)
        if isinstance(n, ast.Constant) and isinstance(n.value, bytes):
            problems.append('%s: bytes literal' % line)
        if isinstance(n, ast.Name) and n.id in ('__file__',):
            pass
    if problems:
        raise SystemExit('not Python 2.4:\n  ' + '\n  '.join(problems))


def convert():
    gen = read('gen_random.py')
    cut = gen.find(OUTPUT_MARK)
    if cut < 0:
        raise SystemExit('output mark not found in gen_random.py')
    parts = [read('noise.py'), read('place_names.py'), gen[:cut]]
    body = []
    for src in parts:
        tree = Py24().visit(ast.parse(src))
        ast.fix_missing_locations(tree)
        body.extend(tree.body)
    module = ast.Module(body=body, type_ignores=[])
    check_py24(module)
    code = 'from __future__ import division\n' + ast.unparse(module) + '\n'
    return code


def pack(text):
    data = base64.b64encode(zlib.compress(text.encode('utf-8'), 9)).decode('ascii')
    return '\n'.join(data[i:i + 100] for i in range(0, len(data), 100))


RESULT_KEYS = ('plot_type', 'terrain', 'feature', 'wofr', 'nofr', 'europe', 'pacific', 'BONUS', 'IMPROVEMENT', 'ROUTE', 'SIGNS')


def self_test(code, seed):
    """Run the rewritten code (with the helpers of the map script) and gen_random.py itself under Python 3 with the
    same seed: the results must be the same, else a rewrite changed the meaning."""
    import io
    import contextlib
    template = read('mapscript_template.py')
    helpers = template[template.index('## helpers begin'):template.index('## helpers end')]
    hns = {}
    exec(compile(helpers, 'helpers', 'exec'), hns)
    xml = {}
    for name, path in XML_FILES.items():
        with open(path, encoding='utf-8') as f:
            xml[name] = f.read()
    ns = hns['_namespace'](seed, xml)
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, 'converted', 'exec'), ns)
    gen = read('gen_random.py')
    ons = {'__name__': 'gen_random', '__file__': os.path.join(HERE, 'gen_random.py')}
    argv = sys.argv
    sys.argv = ['gen_random.py', str(seed), os.path.join(HERE, 'out_random', 'selftest')]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(gen[:gen.find(OUTPUT_MARK)], 'gen_random', 'exec'), ons)
    finally:
        sys.argv = argv
    bad = [k for k in RESULT_KEYS if ns[k] != ons[k]]
    if bad:
        raise SystemExit('self test seed %d: the rewritten code differs in %s' % (seed, ', '.join(bad)))
    print('self test seed %d: same result as gen_random.py' % seed)


def main():
    code = convert()
    for arg in sys.argv[1:]:
        if arg.startswith('--test='):
            for seed in arg[7:].split(','):
                self_test(code, int(seed))
    xml = {}
    for name, path in XML_FILES.items():
        with open(path, encoding='utf-8') as f:
            xml[name] = f.read()
    template = read('mapscript_template.py')
    out = template.replace('@CODE@', pack(code))
    out = out.replace('@XML_FEATURES@', pack(xml['CIV4FeatureInfos.xml']))
    out = out.replace('@XML_BONUSES@', pack(xml['CIV4BonusInfos.xml']))
    with open(TARGET, 'w', encoding='ascii', newline='\r\n') as f:
        f.write(out)
    if '--dump' in sys.argv:
        with open(os.path.join(HERE, 'out_random', 'mapscript_code.py'), 'w', encoding='utf-8') as f:
            f.write(code)
    print('map script ->', os.path.normpath(TARGET), '(%d lines of generator code, %d KB)' % (code.count('\n'), len(out) // 1024))


if __name__ == '__main__':
    main()
