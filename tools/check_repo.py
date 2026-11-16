#!/usr/bin/env python3
"""Consistency checks for the knowledge base. Run from anywhere; exits 1 on any problem.

Checks:
  - relative Markdown links [text](path) resolve;
  - backticked repo paths (`docs/...`, `data/...`, `status.yaml`, ...) exist, with * and {a,b} globs;
  - kb: paths and quoted repo paths in YAML exist;
  - no em or en dashes in tracked text files;
  - no absolute workspace paths (home, root or scratch directories) in tracked text files;
  - YAML files parse, TSV rows have the header's column count.
"""
import glob, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP = ('issues/', 'docs/', 'data/', 'orphaned-patches/', 'tools/')
TOPFILES = ('status.yaml', 'README.md', 'AGENTS.md')
problems = []


def tracked():
    out = subprocess.run(['git', '-C', ROOT, 'ls-files'], capture_output=True, text=True, check=True).stdout
    return [f for f in out.split('\n') if f and os.path.exists(os.path.join(ROOT, f))]


def expand(p):
    m = re.search(r'\{([^}]*)\}', p)
    if m:
        return [q for alt in m.group(1).split(',') for q in expand(p[:m.start()] + alt + p[m.end():])]
    return [p]


def exists(p):
    p = p.split('#')[0].rstrip('/').rstrip('.,:;')
    for q in expand(p):
        if any(c in q for c in '*?['):
            if not glob.glob(os.path.join(ROOT, q)):
                return False
        elif not os.path.exists(os.path.join(ROOT, q)):
            return False
    return True


def looks_like_repo_path(s):
    if ' ' in s or '<' in s or s.startswith(('/', 'http')):
        return False
    return s.startswith(TOP) or s in TOPFILES


files = tracked()
text_ext = ('.md', '.yaml', '.yml', '.tsv', '.py', '.js', '.txt', '.json')
generated_json = re.compile(r'^(data/generated/|issues/issues\.json$)')

for f in files:
    if not f.endswith(text_ext) and f != '.gitignore':
        continue
    path = os.path.join(ROOT, f)
    t = open(path, encoding='utf-8').read()
    if not generated_json.match(f):
        for i, line in enumerate(t.split('\n'), 1):
            if chr(0x2014) in line or chr(0x2013) in line:
                problems.append(f'{f}:{i}: em or en dash')
            if re.search(r'(?<![\w.])/(home|root)/|(?<![\w.])/tm' r'p/claude', line):
                problems.append(f'{f}:{i}: absolute workspace path')
    if f.endswith('.md'):
        base = os.path.dirname(f)
        for m in re.finditer(r'\]\(([^)\s]+)\)', t):
            target = m.group(1)
            if re.match(r'[a-z]+:', target) or target.startswith('#'):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(ROOT, base, target.split('#')[0]))):
                problems.append(f'{f}: broken link {target}')
    if f.endswith(('.md', '.yaml', '.py')) and not f.startswith('data/indexes/patches-'):
        for m in re.finditer(r'`([^`\n]+)`', t):
            s = m.group(1)
            if looks_like_repo_path(s) and not exists(s):
                problems.append(f'{f}: missing path `{s}`')
    if f.endswith('.yaml'):
        for m in re.finditer(r'"kb:([^"|\s]+)', t):
            if not exists(m.group(1)):
                problems.append(f'{f}: missing kb path {m.group(1)}')
        for m in re.finditer(r'"((?:docs|data|issues|orphaned-patches|tools)/[^"\s|]+|status\.yaml)"', t):
            if not exists(m.group(1)):
                problems.append(f'{f}: missing path "{m.group(1)}"')

try:
    import yaml
    for f in files:
        if f.endswith('.yaml'):
            try:
                yaml.safe_load(open(os.path.join(ROOT, f)))
            except yaml.YAMLError as e:
                problems.append(f'{f}: YAML error {str(e).splitlines()[0]}')
except ImportError:
    print('PyYAML missing, YAML parse check skipped', file=sys.stderr)

for f in files:
    if not f.endswith('.tsv'):
        continue
    rows = [l for l in open(os.path.join(ROOT, f)).read().split('\n') if l and not l.startswith('# ')]
    if not rows:
        continue
    want = len(rows[0].split('\t'))
    for i, r in enumerate(rows[1:], 2):
        n = len(r.split('\t'))
        if n != want and not (r.startswith('#') and n == 1):
            problems.append(f'{f}: data row {i} has {n} columns, header has {want}')

for p in problems:
    print(p)
print(f'{len(files)} files checked, {len(problems)} problems')
sys.exit(1 if problems else 0)
