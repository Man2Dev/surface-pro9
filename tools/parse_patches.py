#!/usr/bin/env python3
import re, sys, json, os, email.header
def parse(path):
    txt=open(path,errors='replace').read()
    parts=re.split(r'(?m)^From ([0-9a-f]{40}) ', txt)
    out=[]
    for i in range(1,len(parts),2):
        sha=parts[i]; body=parts[i+1]
        hdr,_,rest=body.partition('\n\n')
        h={}
        cur=None
        for line in hdr.split('\n'):
            if line[:1] in ' \t' and cur: h[cur]+=' '+line.strip(); continue
            m=re.match(r'([A-Za-z-]+): (.*)',line)
            if m: cur=m.group(1); h[cur]=m.group(2)
        subj=re.sub(r'^\[PATCH[^\]]*\]\s*','',h.get('Subject',''))
        msg,_,diff=rest.partition('\n---\n')
        files=sorted(set(re.findall(r'(?m)^diff --git a/(\S+)',diff)))
        tags={k:re.findall(r'(?mi)^'+k+r':\s*(.+)$',msg) for k in ['Link','Patchset','Signed-off-by','Fixes','Closes','BugLink','Reviewed-by','Tested-by','Co-developed-by']}
        stat=re.search(r'(\d+) files? changed.*',diff)
        dl=diff.lower()
        sp9 = bool(re.search(r'surface pro 9|pro9|\bsp9\b',body,re.I))
        sp8 = bool(re.search(r'surface pro 8|\bsp8\b',body,re.I))
        out.append(dict(sha=sha,author=h.get('From',''),date=h.get('Date',''),subject=subj,
          series=os.path.basename(path),files=files,stat=stat.group(0) if stat else '',
          mentions_sp9=sp9,mentions_sp8=sp8,
          tags={k:v for k,v in tags.items() if v and k!='Signed-off-by'},
          signed_off=tags['Signed-off-by'],
          message=msg.strip()[:1500]))
    return out
allc=[]
for p in sorted(sys.argv[2:]): allc+=parse(p)
json.dump(allc,open(sys.argv[1],'w'),indent=1,ensure_ascii=False)
print(len(allc))
