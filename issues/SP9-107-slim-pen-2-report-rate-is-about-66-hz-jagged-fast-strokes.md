---
id: SP9-107
title: Slim Pen 2 report rate is about 66 Hz (jagged fast strokes)
labels:
- area:pen
- kind:bug
- priority:P2
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-106
- SP9-108
upstream:
- linux-surface/iptsd
source: issues/src/1-touch-pen.yaml
---

# SP9-107: Slim Pen 2 report rate is about 66 Hz (jagged fast strokes)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P2 | pen | bug | n/a | partial | n/a |

## Problem

Fast pen strokes come out jagged; measured pen event rate on the SP9 is about 66 Hz.

## Origin

iptsd only emits a position for some DFT window types. An SP9 user processes position on every DFT window
(Position, MPP2 position, pressure and an unknown type) and reaches about 266 to 300 Hz.

## Reports

- [linux-surface#1588](https://github.com/linux-surface/linux-surface/issues/1588) (open issue, patch-pending) "Surface Pen Jagged Fast Lines (low poll rate)": Surface Pen jagged fast lines (low poll rate), SP9 data and patches
- [linux-surface/iptsd#213](https://github.com/linux-surface/iptsd/issues/213) (open issue, sibling) "SP8: Stylus handwriting stroke start/stop lagging and low pulling": SP8 stroke lag and low polling rate

## Fixes, patches and PRs

- [github.com/user-attachments/files/30677702/highest_polling_rate.patch](https://github.com/user-attachments/files/30677702/highest_polling_rate.patch): Muvkina's patch (attachment in #1588), tilt and pressure still rough
- [AndyGozas/iptsd](https://github.com/AndyGozas/iptsd): branch bundle-events-workaround

## Possible solutions

- Clean up Muvkina's patch (tilt, pressure, eraser rate) and send it as an iptsd PR with the author.

## Next steps

- [ ] Apply the patch to iptsd master, measure with evhz on the SP9, report in #1588.

## Upstream and people

- Upstream target: linux-surface/iptsd
- People: Muvkina, StollD

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-106](SP9-106-erratic-touch-detection-and-weak-palm-rejection-with-default.md) Erratic touch detection and weak palm rejection with default iptsd settings, [SP9-108](SP9-108-slim-pen-2-phantom-button-and-eraser-events.md) Slim Pen 2 phantom button and eraser events

## Knowledge base

- [docs/research/open-issues.md](../docs/research/open-issues.md)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
