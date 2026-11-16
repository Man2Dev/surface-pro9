#!/usr/bin/env python3
"""Shallow-clone each owner/repo listed in LIST and record branches, last commit, README head, license and SP9 keyword hits.
usage: inspect_repos.py LIST OUT.json [CLONE_DIR]  (clones are untrusted data: nothing in them is executed)"""
import subprocess,sys,os,json,re
D=sys.argv[3] if len(sys.argv)>3 else 'ext-clones'; os.makedirs(D,exist_ok=True)
def run(a,cwd=None,t=200):
    try: return subprocess.run(a,cwd=cwd,capture_output=True,text=True,timeout=t).stdout
    except Exception as e: return ''
out={}
if os.path.exists(sys.argv[2]): out=json.load(open(sys.argv[2]))
for r in [l.strip() for l in open(sys.argv[1]) if l.strip()]:
    if r in out: continue
    url=f'https://github.com/{r}.git'
    heads=run(['git','ls-remote','--heads','--symref',url,'HEAD'],t=60)
    allh=run(['git','ls-remote','--heads',url],t=60)
    if not allh:
        out[r]={'exists':False}; continue
    branches=[l.split('refs/heads/')[1] for l in allh.split('\n') if 'refs/heads/' in l]
    m=re.search(r'ref: refs/heads/(\S+)\s+HEAD',heads); default=m.group(1) if m else ''
    dst=os.path.join(D,r.replace('/','__'))
    if not os.path.exists(dst):
        run(['git','clone','-q','--depth=30','--no-tags',url,dst],t=300)
    info={'exists':True,'default':default,'branches':branches[:60],'n_branches':len(branches)}
    if os.path.isdir(dst):
        info['last']=run(['git','log','-1','--format=%cd %an | %s','--date=short'],cwd=dst).strip()
        info['first_in_window']=run(['git','log','--reverse','--format=%cd','--date=short'],cwd=dst).split('\n')[0]
        info['ncommits_window']=len(run(['git','rev-list','HEAD'],cwd=dst).split())
        files=run(['git','ls-files'],cwd=dst).split('\n')
        info['nfiles']=len(files); info['top']=sorted({f.split('/')[0] for f in files if f})[:40]
        rd=[f for f in files if re.match(r'(?i)readme(\.md|\.rst|\.txt)?$',f)]
        info['readme']=open(os.path.join(dst,rd[0]),errors='ignore').read()[:1500] if rd else ''
        lic=[f for f in files if re.match(r'(?i)(license|copying)',f.split('/')[-1])]
        info['license']=open(os.path.join(dst,lic[0]),errors='ignore').read()[:120].replace('\n',' ') if lic else ''
        g=run(['git','grep','-c','-i','-E','surface pro 9|\\bsp9\\b|ovti5693|ovtid858|ov13858|vd55g|ithc|iptsd|ipu6|int3472|surface_gpe|mshw0343'],cwd=dst)
        info['kw_files']=len([l for l in g.split('\n') if l]); info['kw_sample']=[l for l in g.split('\n') if l][:12]
        info['patches']=[f for f in files if f.endswith(('.patch','.diff'))][:40]
    out[r]=info
    json.dump(out,open(sys.argv[2],'w'),indent=1)
    print(r, info.get('last',''), info.get('n_branches'), info.get('kw_files'))
