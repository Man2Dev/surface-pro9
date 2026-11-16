---
id: SP9-113
title: KWin shows the mouse cursor while the pen hovers
labels:
- area:pen
- kind:bug
- priority:P3
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-111
upstream:
- KDE KWin
source: issues/src/1-touch-pen.yaml
---

# SP9-113: KWin shows the mouse cursor while the pen hovers

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P3 | pen | bug | n/a | n/a | broken |

## Problem

In Plasma, the mouse cursor appears when the pen enters proximity, which gets in the way while writing.

## Origin

KWin treats the absolute stylus entering proximity like pointer motion. Reported on an SP7+ with a patch;
the same happens on the SP9 with iptsd.

## Reports

- [rhbz#2524606](https://bugzilla.redhat.com/show_bug.cgi?id=2524606) (NEW) "KWin shows the mouse cursor when an absolute stylus enters proximity (Surface Pro 7+, F44, iptsd)": KWin shows the mouse cursor when an absolute stylus enters proximity (patch attached)

## Fixes, patches and PRs

- [rhbz#2524606](https://bugzilla.redhat.com/show_bug.cgi?id=2524606) (NEW) "KWin shows the mouse cursor when an absolute stylus enters proximity (Surface Pro 7+, F44, iptsd)": patch attached to the Fedora bug

## Possible solutions

- Forward the patch to KDE (invent.kde.org/plasma/kwin) and test it on the SP9.

## Next steps

- [ ] Low priority.

## Upstream and people

- Upstream target: KDE KWin
- People: none

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-111](SP9-111-libwacom-has-no-sp9-tablet-description-pen-and-touch-not-rec.md) libwacom has no SP9 tablet description (pen and touch not recognised as a tablet)

## Knowledge base

- [docs/research/outside-trackers.md](../docs/research/outside-trackers.md)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
