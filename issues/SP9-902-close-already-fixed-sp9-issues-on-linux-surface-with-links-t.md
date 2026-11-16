---
id: SP9-902
title: Close already-fixed SP9 issues on linux-surface with links to the fixing commits
labels:
- area:meta
- kind:triage
- priority:P3
- status:open
depends_on: []
blocks: []
related:
- SP9-205
upstream:
- linux-surface
source: issues/src/9-meta.yaml
---

# SP9-902: Close already-fixed SP9 issues on linux-surface with links to the fixing commits

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P3 | meta | triage | n/a | n/a | n/a |

## Problem

17 open SP9 issues on linux-surface are already fixed somewhere; they bury the real problems.

## Origin

178 of 288 open SP9/sibling issues never got a maintainer reply; danielzgtg has the Triage role since
2026-10.

## Reports

- [linux-surface#2081](https://github.com/linux-surface/linux-surface/issues/2081) (open issue, tracker) "Bus factor: Do something about the loss of activity from 3 of the": bus factor discussion; danielzgtg got Triage
- [linux-surface#1927](https://github.com/linux-surface/linux-surface/issues/1927) (open issue, tracker) "is this repo dead?": is this repo dead?

## Fixes, patches and PRs

- none yet

## Possible solutions

- Comment on each with the fix (commit or PR) so a triager can close them: #1392, #1516, #1540, #1609, #1612, #1690, #1064, #1865, #1892, kernel#165, #2056, #1753, #1078, #1872, #1126, #1277, surface-aggregator-module#59.

## Next steps

- [ ] Post as a short comment per issue with the fixing commit or PR.

## Upstream and people

- Upstream target: linux-surface
- People: danielzgtg, qzed

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-205](SP9-205-power-and-volume-buttons-dead-when-soc-button-array-probes-b.md) Power and volume buttons dead when soc_button_array probes before the pin controller

## Knowledge base

- [docs/research/open-issues.md](../docs/research/open-issues.md)
- [data/indexes/open-issues.tsv](../data/indexes/open-issues.tsv)

_Generated from `issues/src/9-meta.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
