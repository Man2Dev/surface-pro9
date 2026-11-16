#!/usr/bin/env python3
"""List novel commits on feature branches fetched into a linux-surface/kernel clone as remotes named f_<owner>_<repo>.
usage: kernel_fork_branches.py OUT.json KERNEL_CLONE LINUX_SURFACE_CLONE
Fetch branches with: git fetch --depth=40 --filter=tree:0 f_<owner>_<repo> +refs/heads/<b>:refs/remotes/f_<owner>_<repo>/<b> (one at a time, shallow repos lock)."""
import subprocess,re,json,os,glob,sys
def g(*a,cwd=sys.argv[2]): return subprocess.run(['git']+list(a),cwd=cwd,capture_output=True,text=True).stdout
known=set()
for f in glob.glob(sys.argv[3]+'/patches/*/*.patch'):
    for m in re.finditer(r'(?m)^Subject: (?:\[PATCH[^\]]*\] )?(.*(?:\n .*)*)',open(f,errors='ignore').read()):
        known.add(re.sub(r'\s+',' ',m.group(1)).strip())
out=[]
for line in g('for-each-ref','--format=%(refname:short)','refs/remotes').split():
    if not line.startswith('f_'): continue
    log=g('log','-40','--format=%H%x1f%ad%x1f%an%x1f%s%x1f%b%x1e','--date=short',line)
    novel=[];stop=False
    for c in log.split('\x1e'):
        c=c.strip()
        if not c: continue
        h,d,a,s,b=(c.split('\x1f')+['']*5)[:5]
        if re.search(r'commit [0-9a-f]{40} upstream|upstream commit [0-9a-f]{40}',b) or re.match(r'Linux \d+\.\d+',s): stop=True; break
        if s.startswith('Merge'): continue
        novel.append(dict(sha=h[:12],date=d,author=a,subject=s,known=s in known,sp9=bool(re.search(r'surface pro 9|\bsp9\b|pro ?9\b',s+b,re.I)),links=re.findall(r'(?mi)^(?:Link|Closes):\s*(\S+)',b)))
    fork,br=line[2:].split('/',1)
    fork=fork.replace('_','/',1)
    out.append(dict(repo=fork,branch=br,commits=novel,reached_stable=stop))
json.dump(out,open(sys.argv[1],'w'),indent=1)
for o in out:
    nk=[c for c in o['commits'] if not c['known']]
    print(f"== {o['repo']} {o['branch']}  top={len(o['commits'])} novel={len(nk)} stable_reached={o['reached_stable']}")
    for c in nk[:12]: print('   ',c['date'],c['sha'][:10],'SP9' if c['sp9'] else '   ',c['author'][:18],'|',c['subject'][:90])
