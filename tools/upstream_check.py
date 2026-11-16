#!/usr/bin/env python3
"""Apply a linux-surface patches/<ver>/ series commit by commit to a mainline checkout and classify each commit:
  not-upstream      applies cleanly on top of the previously applied commits
  upstream          does not apply, but reverse-applies on pristine mainline (already merged)
  ambiguous         both
  partial/diverged  neither; hunks are applied with --reject to keep going, count of rejected hunks reported
usage: upstream_check.py <series_dir> <mainline_checkout> <out.json>
The mainline checkout can be a sparse, shallow, blobless clone (see tools/README.md)."""
import re, sys, json, subprocess, os, shutil, tempfile
series_dir, mainline, out = sys.argv[1], sys.argv[2], sys.argv[3]
S=tempfile.mkdtemp(prefix='upcheck-')
work=S+'/cumtree'
shutil.rmtree(work,ignore_errors=True)
subprocess.run(['git','-C',mainline,'worktree','prune'])
shutil.copytree(mainline,work,ignore=shutil.ignore_patterns('.git'))
subprocess.run(['git','init','-q',work]); 
res=[]
def run(args,cwd):
    r=subprocess.run(args,cwd=cwd,capture_output=True,text=True); return r.returncode,r.stdout+r.stderr
for f in sorted(os.listdir(series_dir)):
    if not f.endswith('.patch'): continue
    txt=open(os.path.join(series_dir,f),errors='replace').read()
    for ch in re.split(r'(?m)^(?=From [0-9a-f]{40} )', txt):
        if not ch.startswith('From '): continue
        sha=ch[5:45]
        subj=re.search(r'(?m)^Subject: (?:\[PATCH[^\]]*\] )?(.*(?:\n .*)*)',ch).group(1).replace('\n','')
        p=S+'/one.patch'; open(p,'w').write(ch)
        rc_rev,_=run(['git','apply','--check','-R',p],mainline)
        rc,o=run(['git','apply','--check',p],work)
        if rc==0:
            run(['git','apply',p],work); st='not-upstream'
            if rc_rev==0: st='ambiguous'
            detail=''
        elif rc_rev==0:
            st='upstream'; detail=''
        else:
            rc2,o2=run(['git','apply','--reject',p],work)
            rej=len(re.findall(r'Rejected hunk',o2)); app=len(re.findall(r'Hunk #\d+ applied cleanly',o2))
            missing=sorted(set(re.findall(r'error: (\S+): No such file',o2)))
            st='partial/diverged'; detail=f'{rej} hunks rejected'+(f', missing files: {missing}' if missing else '')
            for root,_,fs in os.walk(work):
                for x in fs:
                    if x.endswith('.rej') or x.endswith('.orig'): os.remove(os.path.join(root,x))
        res.append(dict(series=f,sha=sha,subject=subj,mainline_status=st,detail=detail))
json.dump(res,open(out,'w'),indent=1)
for r in res: print(r['series'][:20],'|',r['subject'][:72],'|',r['mainline_status'],'|',r['detail'][:110])
