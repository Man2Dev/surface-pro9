#!/usr/bin/env python3
# usage: fork_delta.py <ref> <ver> [baseref]  -> prints commits (subject/author) in ref's patches/<ver> not in baseref's
import subprocess, re, sys, json
ref, ver = sys.argv[1], sys.argv[2]; base = sys.argv[3] if len(sys.argv)>3 else 'origin/master'
def g(*a): return subprocess.run(['git']+list(a),capture_output=True,text=True).stdout
def commits(r):
    out={}
    files=[f for f in g('ls-tree','--name-only',f'{r}:patches/{ver}/').split('\n') if f.endswith('.patch')]
    for f in files:
        txt=g('show',f'{r}:patches/{ver}/{f}')
        for ch in re.split(r'(?m)^(?=From [0-9a-f]{40} )',txt):
            if not ch.startswith('From '): continue
            m=re.search(r'(?m)^Subject: (?:\[PATCH[^\]]*\] )?(.*(?:\n .*)*)',ch)
            s=re.sub(r'\s+',' ',m.group(1)) if m else '?'
            a=re.search(r'(?m)^From: (.*)',ch); a=a.group(1) if a else ''
            links=re.findall(r'(?mi)^(?:Link|Closes|BugLink): *(\S+)',ch)
            out[s]=dict(file=f,author=a,links=links,sha=ch[5:45])
    return out
A=commits(ref); B=commits(base)
extra=[dict(subject=s,**v) for s,v in A.items() if s not in B]
missing=[s for s in B if s not in A]
print(json.dumps(dict(ref=ref,ver=ver,base=base,n_ref=len(A),n_base=len(B),extra=extra,missing_vs_base=missing),indent=1))
