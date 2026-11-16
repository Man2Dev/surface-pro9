#!/usr/bin/env python3
"""Aggregate urls_local.py output by GitHub repo and by host. usage: agg_urls.py IN.json OUT.json"""
import json,re,sys,collections
d=json.load(open(sys.argv[1]))
repos=collections.defaultdict(set); hosts=collections.defaultdict(set)
NOISE={'orgs','settings','sponsors','features','about','login','apps','marketplace','notifications','topics','users','site','search','pulls','issues','explore','enterprise','pricing','security','collections','trending','customer-stories'}
for u,src in d.items():
    m=re.match(r'https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)',u)
    if m:
        o,r=m.group(1),m.group(2).removesuffix('.git')
        if o.lower() in NOISE: continue
        repos[f'{o}/{r}'].update(src)
        continue
    m=re.match(r'https?://([^/]+)',u)
    if m: hosts[m.group(1).lower()].update(src)
out={'repos':{k:sorted(v) for k,v in repos.items()},'hosts':{k:sorted(v) for k,v in hosts.items()}}
json.dump(out,open(sys.argv[2],'w'))
for k,v in sorted(repos.items(),key=lambda kv:-len(kv[1])):
    if k.lower().startswith('linux-surface/'): continue
    print(len(v),k,'|',';'.join(sorted(v))[:140])
print('---HOSTS')
for k,v in sorted(hosts.items(),key=lambda kv:-len(kv[1]))[:60]: print(len(v),k,'|',';'.join(sorted(v))[:100])
