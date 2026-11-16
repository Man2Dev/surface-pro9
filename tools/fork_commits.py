#!/usr/bin/env python3
import subprocess, json, collections, re, sys
def g(*a): return subprocess.run(['git']+list(a),capture_output=True,text=True).stdout
refs=[r.strip() for r in g('branch','-r','--format=%(refname:short)').split('\n') if r.strip() and not r.startswith('origin')]
commits=collections.OrderedDict()
for r in refs:
    out=g('log','--no-merges','--format=%H\x1f%an\x1f%ad\x1f%s',"--date=short",r,'--not','--remotes=origin')
    for line in out.strip().split('\n'):
        if not line: continue
        h,an,ad,s=line.split('\x1f')
        c=commits.setdefault(h,dict(sha=h,author=an,date=ad,subject=s,refs=[]))
        c['refs'].append(r)
# patch-id dedupe & files
for h,c in commits.items():
    c['files']=[f for f in g('show','--format=','--name-only',h).split('\n') if f]
    body=g('show','--format=%B','-s',h)
    diff=g('show','--format=',h)
    txt=body+diff
    c['sp9']=bool(re.search(r'surface pro 9|\bsp9\b|pro ?9\b',txt,re.I))
    c['sp8']=bool(re.search(r'surface pro 8|\bsp8\b',txt,re.I))
    c['body']=body.strip()[:600]
    c['forks']=sorted({r.split('/')[0] for r in c['refs']})
json.dump(list(commits.values()),open(sys.argv[1],'w'),indent=1)
print(len(refs),len(commits))
