---
id: SP9-603
title: linux-surface Fedora repository lags releases and recently published broken files
labels:
- area:packaging
- kind:bug
- priority:P3
- status:open
depends_on: []
blocks: []
related:
- SP9-102
- SP9-602
upstream:
- linux-surface
source: issues/src/6-boot-packaging.yaml
---

# SP9-603: linux-surface Fedora repository lags releases and recently published broken files

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P3 | packaging | bug | n/a | partial | n/a |

## Problem

The linux-surface Fedora repo has lagged almost every new Fedora release and several kernel releases; since
2026-11-12 some release files are uploaded as .rpm.blob.

## Origin

Manual packaging until 2026-10, now automated (package status #2318) with a new staging step that renames
files.

## Reports

- [linux-surface#2370](https://github.com/linux-surface/linux-surface/issues/2370) (open) "Debian repo: 7.2.14-1 packages return 404, files stored as .blob in pool": Debian and Fedora release files stored as .blob
- [linux-surface#2055](https://github.com/linux-surface/linux-surface/issues/2055) (closed issue, fixed-package) "No Fedora release since 6.18.8-1": no Fedora release since 6.18.8-1 (closed)
- [linux-surface#1888](https://github.com/linux-surface/linux-surface/issues/1888) (closed issue, fixed-package) "Fedora 43 support": Fedora 43 support (closed)
- [linux-surface#2139](https://github.com/linux-surface/linux-surface/issues/2139) (closed issue, fixed-package) "Linux Surface not working with Surface Pro 8 with Fedora 44": Fedora 44 (closed)
- [linux-surface/repo#15](https://github.com/linux-surface/repo/issues/15) (closed issue, fixed-package) "Fedora 42 Repo is missing iptsd": Fedora 42 repo missing iptsd (closed)
- [linux-surface#2082](https://github.com/linux-surface/linux-surface/issues/2082) (closed issue, fixed-package) "fedora 43 workflow (& other F?) error @ dist-configs-check": Fedora workflow config check failure (closed)

## Fixes, patches and PRs

- [linux-surface#2318](https://github.com/linux-surface/linux-surface/issues/2318) (open) "Package status": automated package status

## Possible solutions

- Report the .blob problem details on #2370 if it affects an SP9 install; long term, get the pieces into Fedora proper (SP9-102, SP9-903).

## Next steps

- [ ] Watch #2370.

## Upstream and people

- Upstream target: linux-surface
- People: qzed, danielzgtg

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-102](SP9-102-iptsd-is-not-packaged-in-fedora.md) iptsd is not packaged in Fedora, [SP9-602](SP9-602-fedora-installs-a-generic-kernel-as-default-over-kernel-surf.md) Fedora installs a generic kernel as default over kernel-surface after updates

## Knowledge base

- [docs/research/closed-issues.md](../docs/research/closed-issues.md)
- [status.yaml](../status.yaml)

_Generated from `issues/src/6-boot-packaging.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
