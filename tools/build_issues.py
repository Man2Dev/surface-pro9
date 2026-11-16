#!/usr/bin/env python3
"""Render issues/src/*.yaml into one Markdown issue per problem, plus indexes.

Outputs (all generated, do not edit by hand):
  issues/SP9-NNN-<slug>.md   one issue per problem, with YAML front matter
  issues/README.md           table, area tree, dependency tree, Mermaid graph
  issues/refs.md             every external reference and the issues citing it
  issues/issues.json         title/body/labels per issue, for a later GitHub import

Reference syntax in the YAML ("REF | note"):
  #N                      linux-surface/linux-surface issue or PR N
  disc#N                  linux-surface/linux-surface discussion N
  <repo>#N                repo in the linux-surface org (kernel#169, iptsd#219)
  owner/repo#N            issue or PR in another GitHub repo
  owner/repo              a GitHub repository
  lore:<msgid>            mailing-list message (lore.kernel.org/r/<msgid>)
  mainline:<sha>          torvalds/linux commit
  commit:owner/repo@sha   GitHub commit
  gist:owner/id           GitHub gist
  rhbz#N, kbz#N           Red Hat / kernel.org Bugzilla
  ark!N                   Fedora kernel-ark merge request
  lcpw:N                  libcamera patchwork patch
  fdo:group/project#N     freedesktop GitLab issue
  url:https://...         any URL
  kb:path                 file in this knowledge base

Titles and states are looked up in data/indexes/*.tsv when the reference is known there.
Usage: python3 tools/build_issues.py   (run from the repository root)
"""
import csv, glob, json, os, re, sys
from collections import defaultdict

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDIR = os.path.join(ROOT, 'issues')
FIELDS = ['id', 'title', 'area', 'kind', 'status', 'priority', 'layers', 'problem', 'origin', 'reports',
          'fixes', 'solutions', 'next', 'upstream', 'people', 'depends_on', 'related', 'kb']
GH_ORG = 'https://github.com/linux-surface'


def tsv(name):
    path = os.path.join(ROOT, 'data', 'indexes', name)
    if not os.path.exists(path):
        return []
    lines = [l for l in open(path, encoding='utf-8') if not l.startswith('# ')]
    return list(csv.DictReader(lines, delimiter='\t'))


def load_lookup():
    """ref -> (state text, title)"""
    lk = {}
    kind_name = {'I': 'issue', 'PR': 'PR', 'PR+m': 'PR, merged'}
    state_name = {'O': 'open', 'C': 'closed', 'NP': 'closed, not planned'}
    for f in ('github-sp9.tsv', 'github-related.tsv'):
        for r in tsv(f):
            k = r['id']
            st = state_name.get(r['state'], r['state'])
            kn = kind_name.get(r['kind'], r['kind'])
            lk.setdefault(k, (f'{st} {kn}', r['title']))
    for r in tsv('open-issues.tsv'):
        lk[r['id']] = (f"open issue, {r['class']}", r['title'])
    for r in tsv('closed-issues.tsv'):
        lk[r['id']] = (f"closed issue, {r['outcome']}", r['title'])
    for r in tsv('open-prs.tsv'):
        k = ('#' if r['repo'] == 'linux-surface' else r['repo'] + '#') + r['pr']
        old = lk.get(k, ('', ''))
        lk[k] = (f"open PR, {r['state']}", old[1] or r['note'][:90])
    for r in tsv('closed-prs.tsv'):
        k = ('#' if r['repo'] == 'linux-surface' else r['repo'] + '#') + r['pr']
        old = lk.get(k, ('', ''))
        lk[k] = (f"closed PR, {r['outcome']}", old[1] or r['note'][:90])
    for r in tsv('discussions.tsv'):
        lk['disc#' + r['n']] = ('discussion', r['title'])
    for r in tsv('upstream-submissions.tsv'):
        lk['lore:' + r['msgid']] = (f"{r['list']}, {r['state']}, {r['author']}, {r['date']}", r['subject'])
    for r in tsv('trackers.tsv'):
        src, ref = r['source'], r['ref']
        key = {'rhbz': 'rhbz#', 'kbz': 'kbz#', 'ark': 'ark', 'lcpw': 'lcpw:', 'gh': ''}.get(src)
        if key is None:
            continue
        k = key + ref
        if src == 'gh' and ref.startswith('linux-surface/'):
            repo, n = ref[len('linux-surface/'):].split('#')
            k = ('#' if repo == 'linux-surface' else repo + '#') + n
        lk.setdefault(k, (r['state'], r['title']))
    return lk


def resolve(ref):
    """Return (label, url) for a reference token."""
    if ref.startswith('kb:'):
        p = ref[3:]
        return p, '../' + p
    if ref.startswith('url:'):
        u = ref[4:]
        label = re.sub(r'^https?://(www\.)?', '', u)
        return (label if len(label) < 70 else label[:67] + '...'), u
    if ref.startswith('lore:'):
        return ref, 'https://lore.kernel.org/r/' + ref[5:]
    if ref.startswith('mainline:'):
        return 'torvalds/linux@' + ref[9:], 'https://git.kernel.org/torvalds/c/' + ref[9:]
    if ref.startswith('commit:'):
        repo, sha = ref[7:].split('@')
        return f'{repo}@{sha}', f'https://github.com/{repo}/commit/{sha}'
    if ref.startswith('gist:'):
        return ref, 'https://gist.github.com/' + ref[5:]
    if ref.startswith('rhbz#'):
        return ref, 'https://bugzilla.redhat.com/show_bug.cgi?id=' + ref[5:]
    if ref.startswith('kbz#'):
        return ref, 'https://bugzilla.kernel.org/show_bug.cgi?id=' + ref[4:]
    if ref.startswith('ark!'):
        return 'kernel-ark' + ref[3:], 'https://gitlab.com/cki-project/kernel-ark/-/merge_requests/' + ref[4:]
    if ref.startswith('lcpw:'):
        return 'libcamera patchwork ' + ref[5:], f'https://patchwork.libcamera.org/patch/{ref[5:]}/'
    if ref.startswith('fdo:'):
        proj, n = ref[4:].split('#')
        return ref[4:], f'https://gitlab.freedesktop.org/{proj}/-/issues/{n}'
    if ref.startswith('disc#'):
        return 'linux-surface discussion ' + ref[5:], f'{GH_ORG}/linux-surface/discussions/{ref[5:]}'
    m = re.fullmatch(r'#(\d+)', ref)
    if m:
        return 'linux-surface#' + m.group(1), f'{GH_ORG}/linux-surface/issues/{m.group(1)}'
    m = re.fullmatch(r'([A-Za-z0-9_.-]+)#(\d+)', ref)
    if m:
        return f'linux-surface/{m.group(1)}#{m.group(2)}', f'{GH_ORG}/{m.group(1)}/issues/{m.group(2)}'
    m = re.fullmatch(r'([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)#(\d+)', ref)
    if m:
        return ref, f'https://github.com/{m.group(1)}/issues/{m.group(2)}'
    m = re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', ref)
    if m:
        return ref, 'https://github.com/' + ref
    raise ValueError(f'unknown reference syntax: {ref!r}')


def slug(s, n=60):
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return s[:n].rstrip('-')


def main():
    issues = []
    for f in sorted(glob.glob(os.path.join(IDIR, 'src', '*.yaml'))):
        for it in yaml.safe_load(open(f, encoding='utf-8')) or []:
            it['_src'] = os.path.relpath(f, ROOT)
            issues.append(it)
    errors = []
    byid = {}
    for it in issues:
        for k in FIELDS:
            it.setdefault(k, [] if k in ('reports', 'fixes', 'solutions', 'next', 'upstream', 'people',
                                         'depends_on', 'related', 'kb') else '')
        if it['id'] in byid:
            errors.append('duplicate id ' + it['id'])
        byid[it['id']] = it
    for it in issues:
        for k in ('depends_on', 'related'):
            for d in it[k]:
                if d not in byid:
                    errors.append(f"{it['id']}: {k} points at unknown {d}")
        for p in it['kb']:
            if not os.path.exists(os.path.join(ROOT, p.split('#')[0])):
                errors.append(f"{it['id']}: kb path missing {p}")
    lk = load_lookup()
    blocks = defaultdict(list)
    related_back = defaultdict(set)
    for it in issues:
        for d in it['depends_on']:
            blocks[d].append(it['id'])
        for r in it['related']:
            related_back[r].add(it['id'])
    for it in issues:
        it['_file'] = f"{it['id']}-{slug(it['title'])}.md"

    refindex = defaultdict(lambda: {'issues': [], 'label': '', 'url': '', 'state': '', 'title': ''})
    unknown_kb = []

    def ref_line(entry, iid, role):
        ref, _, note = [x.strip() for x in entry.partition('|')]
        try:
            label, url = resolve(ref)
        except ValueError as e:
            errors.append(f'{iid}: {e}')
            return f'- {entry}'
        if ref.startswith('kb:') and not os.path.exists(os.path.join(ROOT, ref[3:])):
            unknown_kb.append(f'{iid}: {ref}')
        st, title = lk.get(ref, ('', ''))
        meta = ', '.join(x for x in (st,) if x)
        rec = refindex[ref]
        rec.update(label=label, url=url, state=st or rec['state'], title=title or rec['title'])
        rec['issues'].append((iid, role))
        parts = [f'[{label}]({url})']
        if meta:
            parts.append(f'({meta})')
        if title:
            parts.append(f'"{title}"')
        line = '- ' + ' '.join(parts)
        if note:
            line += ': ' + note
        return line

    def link(i):
        return f'[{i}]({byid[i]["_file"]})'

    for it in issues:
        iid = it['id']
        lay = it['layers'] or {}
        labels = [f"area:{it['area']}", f"kind:{it['kind']}", f"priority:{it['priority']}", f"status:{it['status']}"]
        fm = {'id': iid, 'title': it['title'], 'labels': labels, 'depends_on': it['depends_on'],
              'blocks': sorted(blocks[iid]), 'related': sorted(set(it['related']) | related_back[iid]),
              'upstream': it['upstream'], 'source': it['_src']}
        out = ['---', yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000).strip(), '---', '',
               f"# {iid}: {it['title']}", '',
               '| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |',
               '|---|---|---|---|---|---|---|',
               f"| {it['status']} | {it['priority']} | {it['area']} | {it['kind']} | {lay.get('mainline', '')} | "
               f"{lay.get('linux_surface', '')} | {lay.get('fedora', '')} |", '',
               '## Problem', '', it['problem'].strip(), '',
               '## Origin', '', it['origin'].strip(), '']
        out += ['## Reports', '']
        out += [ref_line(e, iid, 'report') for e in it['reports']] or ['- none recorded']
        out += ['', '## Fixes, patches and PRs', '']
        out += [ref_line(e, iid, 'fix') for e in it['fixes']] or ['- none yet']
        out += ['', '## Possible solutions', ''] + [f'- {s}' for s in it['solutions']]
        out += ['', '## Next steps', ''] + [f'- [ ] {s}' for s in it['next']]
        if it.get('commands'):
            out += ['', '## Commands', '', '```', it['commands'].rstrip(), '```']
        out += ['', '## Upstream and people', '',
                '- Upstream target: ' + (', '.join(it['upstream']) or 'none'),
                '- People: ' + (', '.join(str(p) for p in it['people']) or 'none')]
        out += ['', '## Linked issues', '']
        out.append('- Depends on: ' + (', '.join(f'{link(d)} {byid[d]["title"]}' for d in it['depends_on']) or 'none'))
        out.append('- Blocks: ' + (', '.join(link(b) for b in sorted(blocks[iid])) or 'none'))
        rel = sorted(set(it['related']) | related_back[iid])
        out.append('- Related: ' + (', '.join(f'{link(r)} {byid[r]["title"]}' for r in rel) or 'none'))
        out += ['', '## Knowledge base', ''] + [f'- [{p}](../{p})' for p in it['kb']]
        out += ['', f"_Generated from `{it['_src']}` by `tools/build_issues.py`. Edit the YAML, not this file._", '']
        it['_body'] = '\n'.join(out[out.index(f"# {iid}: {it['title']}") + 1:])
        open(os.path.join(IDIR, it['_file']), 'w', encoding='utf-8').write('\n'.join(out))

    # remove stale generated files
    keep = {it['_file'] for it in issues}
    for f in glob.glob(os.path.join(IDIR, 'SP9-*.md')):
        if os.path.basename(f) not in keep:
            os.remove(f)

    # README
    areas = defaultdict(list)
    for it in issues:
        areas[it['area']].append(it)
    prio = {'P1': 0, 'P2': 1, 'P3': 2}
    r = ['# SP9 issue tracker (Markdown)', '',
         'One file per tangible problem, linking every report, patch, PR and upstream submission we found to it.',
         'Generated from `issues/src/*.yaml` by `tools/build_issues.py`; edit the YAML and rerun.',
         'Each file has YAML front matter (id, title, labels, depends_on, blocks, related) so it can be parsed or',
         'imported into GitHub later; `issues.json` has title, body and labels per issue.', '',
         f'{len(issues)} issues. Status: ' + ', '.join(f"{s} {n}" for s, n in sorted(
             defaultdict(int, {}).items())) , '']
    counts = defaultdict(int)
    for it in issues:
        counts[it['status']] += 1
    r[-2] = f'{len(issues)} issues. Status: ' + ', '.join(f'{s} {n}' for s, n in sorted(counts.items()))
    r += ['Status vocabulary: `open` (problem, no fix posted), `fix-pending` (a fix exists in a PR, branch or on a',
          'list), `needs-test` (needs data from a real SP9), `fixed-upstream` (kept for traceability), `tracking`.', '',
          'Reference index (every external link and the issues citing it): [refs.md](refs.md).', '',
          '## All issues', '',
          '| ID | Title | Area | Priority | Status | Mainline | linux-surface | Fedora |',
          '|---|---|---|---|---|---|---|---|']
    for it in sorted(issues, key=lambda x: (prio.get(x['priority'], 9), x['id'])):
        lay = it['layers'] or {}
        r.append(f"| {link(it['id'])} | {it['title']} | {it['area']} | {it['priority']} | {it['status']} | "
                 f"{lay.get('mainline', '')} | {lay.get('linux_surface', '')} | {lay.get('fedora', '')} |")
    r += ['', '## To-do (next steps by priority)', '',
          'Every open next step, highest priority first. Tick them in the issue files (or here) as they get done.', '']
    for pr in ('P1', 'P2', 'P3'):
        r.append(f'### {pr}')
        r.append('')
        for it in sorted(issues, key=lambda x: x['id']):
            if it['priority'] != pr or it['status'] == 'fixed-upstream':
                continue
            for step in it['next']:
                r.append(f"- [ ] {link(it['id'])} {step}")
        r.append('')
    r += ['## By area', '']
    for a in sorted(areas):
        r.append(f'- **{a}**')
        for it in sorted(areas[a], key=lambda x: x['id']):
            r.append(f"  - {link(it['id'])} {it['title']} ({it['priority']}, {it['status']})")
    r += ['', '## Dependency tree', '', 'Root issues (nothing depends on them being done first) expanded through `depends_on`:', '']
    seen = set()

    def tree(i, depth):
        it = byid[i]
        r.append('  ' * depth + f"- {link(i)} {it['title']} ({it['status']})")
        if i in seen:
            return
        seen.add(i)
        for d in it['depends_on']:
            tree(d, depth + 1)
    roots = [i for i in byid if not blocks[i] and byid[i]['depends_on']]
    for i in sorted(roots):
        tree(i, 0)
    r += ['', '## Graph', '', '```mermaid', 'graph LR']
    for it in issues:
        r.append(f"  {it['id'].replace('-', '_')}[\"{it['id']} {it['area']}\"]")
    for it in issues:
        for d in it['depends_on']:
            r.append(f"  {it['id'].replace('-', '_')} --> {d.replace('-', '_')}")
    r += ['```', '', '## Reference syntax used in the YAML', '', '```', __doc__.split('Reference syntax in the YAML ("REF | note"):')[1].split('Titles and states')[0].strip('\n'), '```', '']
    open(os.path.join(IDIR, 'README.md'), 'w', encoding='utf-8').write('\n'.join(r))

    # refs.md
    rr = ['# Reference index', '',
          'Every external reference cited by an issue, with the issues that cite it and in which role.', '',
          '| Reference | State | Title | Cited by |', '|---|---|---|---|']
    def sortkey(k):
        return (resolve(k)[0].split('#')[0], [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', k)])
    for k in sorted(refindex, key=sortkey):
        v = refindex[k]
        cites = ', '.join(sorted({f'{link(i)} ({role})' for i, role in v['issues']}))
        title = (v['title'] or '').replace('|', '/')
        rr.append(f"| [{v['label']}]({v['url']}) | {v['state']} | {title} | {cites} |")
    open(os.path.join(IDIR, 'refs.md'), 'w', encoding='utf-8').write('\n'.join(rr) + '\n')

    json.dump([{'id': it['id'], 'title': f"{it['id']}: {it['title']}",
                'labels': [f"area:{it['area']}", f"kind:{it['kind']}", f"priority:{it['priority']}", f"status:{it['status']}"],
                'file': 'issues/' + it['_file'], 'body': it['_body']} for it in issues],
              open(os.path.join(IDIR, 'issues.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

    for e in unknown_kb:
        errors.append('missing kb file ' + e)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print(f'{len(issues)} issues, {len(refindex)} distinct references')


if __name__ == '__main__':
    main()
