#!/usr/bin/env python3
"""List branches of linux-surface/linux-surface forks that are ahead of every origin branch.
usage: fork_branches.py OUT.json LINUX_SURFACE_CLONE
The clone needs the fork remotes fetched (remote name owner_repo, see tools/README.md step 3).
Row: [repo, branch, last_date, ahead, sp9|sp8|'', latest patches/<ver>, tip subject]."""
import subprocess,re,json,sys
C=sys.argv[2]
def g(*a): return subprocess.run(['git']+list(a),cwd=C,capture_output=True,text=True).stdout
origin={l.split()[1] for l in g('for-each-ref','--format=%(refname:short) %(objectname)','refs/remotes/origin').split('\n') if l}
rows=[]
for l in g('for-each-ref','--sort=-committerdate','--format=%(refname:short)\t%(objectname)\t%(committerdate:short)\t%(subject)','refs/remotes').split('\n'):
    if not l or l.startswith('origin/'): continue
    ref,sha,date,subj=l.split('\t',3)
    if sha in origin or '/autoupdate/' in ref or '/dependabot/' in ref: continue
    ahead=g('rev-list','--count','--no-merges',ref,'--not','--remotes=origin').strip()
    if ahead in ('','0'): continue
    msgs=g('log','--no-merges','--format=%s%n%b',ref,'--not','--remotes=origin')
    sp9=bool(re.search(r'surface pro 9|\bsp9\b|pro ?9\b',msgs,re.I)); sp8=bool(re.search(r'surface pro 8|\bsp8\b',msgs,re.I))
    vers=sorted([v for v in g('ls-tree','--name-only',f'{ref}:patches/').split() if re.match(r'^\d+\.\d+$',v)],key=lambda v:[int(x) for x in v.split('.')])
    fork,br=ref.split('/',1)
    rows.append([fork.replace('_','/',1),br,date,ahead,'sp9' if sp9 else ('sp8' if sp8 else ''),vers[-1] if vers else '',subj[:90].replace('\t',' ')])
json.dump(rows,open(sys.argv[1],'w'))
print(len(rows),'branches')
