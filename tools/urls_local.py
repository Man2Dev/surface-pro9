#!/usr/bin/env python3
"""Collect URLs from the wiki, the linux-surface repo, fork READMEs and fork commit bodies, patch Link tags and external clones.
usage: urls_local.py OUT.json WIKI_CLONE LINUX_SURFACE_CLONE EXT_DIR FORKCOMMITS.json"""
import re,os,sys,json,subprocess,collections
U=re.compile(r'https?://[^\s\)\]\>"\'`<,]+')
def norm(u):
    u=u.rstrip('.;:*')
    return u
hits=collections.defaultdict(set)
def scan(text,src):
    for u in U.findall(text): hits[norm(u)].add(src)
W=sys.argv[2]
for f in os.listdir(W):
    if f.endswith('.md'): scan(open(os.path.join(W,f),errors='ignore').read(),'wiki:'+f[:-3])
LS=sys.argv[3]
for root,_,fs in os.walk(LS):
    if '/.git' in root or '/patches' in root: continue
    for f in fs:
        if f.endswith(('.md','.txt','.py','.sh','.conf','.spec','.yml')):
            p=os.path.join(root,f); scan(open(p,errors='ignore').read(),'ls:'+os.path.relpath(p,LS))
# fork READMEs at newest branch of each fork + commit bodies
def g(*a,cwd=LS): return subprocess.run(['git']+list(a),cwd=cwd,capture_output=True,text=True).stdout
forks=sorted({r.split('/')[0] for r in g('branch','-r','--format=%(refname:short)').split() if not r.startswith('origin')})
for fk in forks:
    refs=[l for l in g('for-each-ref','--sort=-committerdate','--format=%(refname:short)',f'refs/remotes/{fk}').split('\n') if l][:3]
    for r in refs:
        for path in ['README.md','contrib/README.md']:
            t=g('show',f'{r}:{path}')
            if t and t!=g('show',f'origin/master:{path}'): scan(t,f'fork-readme:{r}:{path}')
for c in json.load(open(sys.argv[5])):
    scan(c['body'],f"fork-commit:{c['forks'][0]}@{c['sha'][:10]}")
# patches Link tags
for v in os.listdir(LS+'/patches'):
    d=LS+'/patches/'+v
    if os.path.isdir(d):
        for f in os.listdir(d):
            for l in open(os.path.join(d,f),errors='ignore'):
                if re.match(r'(Link|Closes|BugLink|Fixes|Reported-by|Tested-by):',l) or 'http' in l[:200] and l.startswith((' ','+ *','Link')): scan(l,f'patch:{v}/{f}')
E=sys.argv[4]
for r in os.listdir(E):
    for root,_,fs in os.walk(os.path.join(E,r)):
        if '/.git' in root: continue
        for f in fs:
            if f.lower().endswith(('.md','.txt','.conf')):
                p=os.path.join(root,f); scan(open(p,errors='ignore').read(),'ext:'+r+':'+os.path.relpath(p,os.path.join(E,r)))
json.dump({k:sorted(v) for k,v in hits.items()},open(sys.argv[1],'w'),indent=0)
print(len(hits))
