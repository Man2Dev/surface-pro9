#!/usr/bin/env python3
"""For PR heads fetched as refs/pr/N in a linux-surface clone, list patch subjects a PR adds that no patches/ dir
on origin/master carries, plus non-patch files touched.
usage: closed_pr_novel.py LS_CLONE OUT.json N [N ...]"""
import subprocess,re,json,sys
C=sys.argv[1]
def g(*a): return subprocess.run(['git']+list(a),cwd=C,capture_output=True,text=True,errors='replace').stdout
SUBJ=re.compile(r'(?m)^Subject: (?:\[PATCH[^\]]*\] )?(.*(?:\n [^\n]*)*)')
def subjects(text): return {re.sub(r'\s+',' ',m.group(1)).strip() for m in SUBJ.finditer(text)}
known=set()
for f in g('ls-tree','-r','--name-only','origin/master','patches/').split():
    if f.endswith('.patch'): known|=subjects(g('show','origin/master:'+f))
out={}
for n in sys.argv[3:]:
    ref=f'refs/pr/{n}'
    if not g('rev-parse','-q','--verify',ref).strip(): out[n]={'missing':True}; continue
    mb=g('merge-base',ref,'origin/master').strip()
    files=g('diff','--name-only',mb,ref).split()
    novel=set();other=[];changed=[]
    for f in files:
        if f.startswith('patches/') and f.endswith('.patch'):
            txt=g('show',f'{ref}:{f}')
            s=subjects(txt); novel|=(s-known)
            if subprocess.run(['git','cat-file','-e',f'{mb}:{f}'],cwd=C,capture_output=True).returncode==0:
                changed.append(f)
        else: other.append(f)
    out[n]={'novel_subjects':sorted(novel),'modified_existing_patch_files':changed,'other_files':other[:20],
            'commits':[l for l in g('log','--format=%h %an: %s',f'{mb}..{ref}').splitlines()][:20]}
json.dump(out,open(sys.argv[2],'w'),indent=1)
print(sum(len(v.get('novel_subjects',[])) for v in out.values()),'novel subjects in',len(out),'PRs')
