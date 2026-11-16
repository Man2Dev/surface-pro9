---
id: SP9-108
title: Slim Pen 2 phantom button and eraser events
labels:
- area:pen
- kind:bug
- priority:P2
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-107
upstream:
- linux-surface/iptsd
source: issues/src/1-touch-pen.yaml
---

# SP9-108: Slim Pen 2 phantom button and eraser events

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P2 | pen | bug | n/a | partial | n/a |

## Problem

Releasing or hovering the pen triggers button 2 or eraser events, which paste, close tabs or interrupt
selections.

## Origin

Two button detection paths in iptsd (MPP2 signals and the phase-correction sign) can disagree; thresholds
were tuned for other pens.

## Reports

- [linux-surface#1233](https://github.com/linux-surface/linux-surface/issues/1233) (closed issue, config) "Slim pen 2 constant random button presses": Slim Pen 2 random button presses: [DFT] ButtonMinMag = 20000 (2023)
- [linux-surface/iptsd#178](https://github.com/linux-surface/iptsd/issues/178) (open issue, unsolved) "[SB3, SG2] Erratic Button/Eraser Signals After Pen Release": erratic button/eraser after pen release in iptsd 3.0.x
- [linux-surface/iptsd#195](https://github.com/linux-surface/iptsd/issues/195) (open issue, unsolved) "MPP stylus causes "missing/bad" frames": MPP stylus missing/bad frames; two detection paths
- [linux-surface/iptsd#161](https://github.com/linux-surface/iptsd/issues/161) (open issue, workaround) "Random dropouts with Surface Pen 2 on Arch": Slim Pen 2 dropouts: raise Mpp2ButtonMinMag

## Fixes, patches and PRs

- [linux-surface/iptsd#233](https://github.com/linux-surface/iptsd/issues/233) (open PR, active) "daemon: debounce rubber and button flags to avoid spurious stylus lifts": debounce eraser and button flags for MPP 2 pens

## Possible solutions

- Test iptsd#233 on the SP9; keep the DFT threshold override only if needed.

## Next steps

- [ ] Post a Tested-by on iptsd#233.

## Upstream and people

- Upstream target: linux-surface/iptsd
- People: 06FallingLight90, tmarkov

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-107](SP9-107-slim-pen-2-report-rate-is-about-66-hz-jagged-fast-strokes.md) Slim Pen 2 report rate is about 66 Hz (jagged fast strokes)

## Knowledge base

- [docs/research/closed-issues.md](../docs/research/closed-issues.md)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
