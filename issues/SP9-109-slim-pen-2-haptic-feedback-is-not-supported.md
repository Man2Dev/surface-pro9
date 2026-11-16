---
id: SP9-109
title: Slim Pen 2 haptic feedback is not supported
labels:
- area:pen
- kind:missing-feature
- priority:P3
- status:open
depends_on: []
blocks: []
related:
- SP9-110
upstream:
- linux-input
source: issues/src/1-touch-pen.yaml
---

# SP9-109: Slim Pen 2 haptic feedback is not supported

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P3 | pen | missing-feature | broken | broken | broken |

## Problem

The Slim Pen 2 vibrates on Windows; on Linux it never does.

## Origin

Haptics go over the pen's Bluetooth HID link (output report 65, Simple Haptics Controller). An old kernel
series for HID simple haptics never merged; a test program made the pen vibrate.

## Reports

- [linux-surface#1066](https://github.com/linux-surface/linux-surface/issues/1066) (open issue, unsolved) "Stylus haptic feedback support": stylus haptic feedback support (SP9)
- [linux-surface/intel-precise-touch#27](https://github.com/linux-surface/intel-precise-touch/issues/27) (open issue, unsolved) "Slim Pen 2 Haptic Feedback": Slim Pen 2 haptic feedback

## Fixes, patches and PRs

- [lore:20221007182945.1654046-1-acz@semihalf.com](https://lore.kernel.org/r/20221007182945.1654046-1-acz@semihalf.com): HID simple haptic controller series (Semihalf, 2022), never merged

## Possible solutions

- Revive the HID haptic series upstream, or drive report 65 from userspace via hidraw.

## Next steps

- [ ] Low priority; collect the HID descriptor of the pen over Bluetooth.

## Upstream and people

- Upstream target: linux-input
- People: petm5, xieve, Rongronggg9

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-110](SP9-110-slim-pen-2-bluetooth-link-drops-when-idle.md) Slim Pen 2 Bluetooth link drops when idle

## Knowledge base

- [docs/research/open-issues.md](../docs/research/open-issues.md)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
