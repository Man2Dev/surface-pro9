#!/usr/bin/env python3
import subprocess, re, json, sys, collections
def g(*a): return subprocess.run(['git']+list(a),capture_output=True,text=True).stdout
def subs(r, ver):
    out={}
    for f in [f for f in g('ls-tree','--name-only',f'{r}:patches/{ver}/').split('\n') if f.endswith('.patch')]:
        txt=g('show',f'{r}:patches/{ver}/{f}')
        for ch in re.split(r'(?m)^(?=From [0-9a-f]{40} )',txt):
            if not ch.startswith('From '): continue
            m=re.search(r'(?m)^Subject: (?:\[PATCH[^\]]*\] )?(.*(?:\n .*)*)',ch)
            s=re.sub(r'\s+',' ',m.group(1)).strip() if m else '?'
            a=re.search(r'(?m)^From: (.*)',ch); a=a.group(1) if a else ''
            links=re.findall(r'(?mi)^(?:Link|Closes|BugLink): *(\S+)',ch)
            out[s]=dict(file=f,author=a,links=links)
    return out
up=set()
for ver in g('ls-tree','--name-only','origin/master:patches/').split():
    up|=set(subs('origin/master',ver))
# also older upstream versions from history of master (deleted dirs)
for ver in ['6.1','6.2','6.3','6.4','6.5','6.7','6.8','7.0','7.1']:
    c=g('log','-1','--format=%H','origin/master','--',f'patches/{ver}').strip()
    if c: up|=set(subs(c+'^',ver)) if False else set()
forks=sorted({r.split('/')[0] for r in g('branch','-r','--format=%(refname:short)').split() if not r.startswith('origin')})
agg=collections.OrderedDict()
for fk in forks:
    refs=g('for-each-ref','--sort=-committerdate','--format=%(refname:short) %(committerdate:short)',f'refs/remotes/{fk}').split('\n')
    seen=0
    for line in refs[:6]:
        if not line.strip(): continue
        r,d=line.split()
        vers=[v for v in g('ls-tree','--name-only',f'{r}:patches/').split() if re.match(r'^v?\d+\.\d+$',v)]
        if not vers: continue
        ver=sorted(vers,key=lambda v:[int(x) for x in v.lstrip('v').split('.')])[-1]
        for s,v in subs(r,ver).items():
            if s in up: continue
            e=agg.setdefault(s,dict(subject=s,author=v['author'],links=v['links'],file=v['file'],where=[]))
            e['where'].append(f'{r}@{ver} ({d})')
json.dump(list(agg.values()),open(sys.argv[1],'w'),indent=1)
print(len(up),len(agg))
