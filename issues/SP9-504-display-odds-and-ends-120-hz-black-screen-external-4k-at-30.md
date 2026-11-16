---
id: SP9-504
title: 'Display odds and ends: 120 Hz black screen, external 4K at 30 Hz, backlight spots after shutdown'
labels:
- area:display
- kind:bug
- priority:P3
- status:needs-test
depends_on:
- SP9-901
blocks: []
related:
- SP9-503
- SP9-901
upstream:
- drm/i915
source: issues/src/5-audio-display-wireless.yaml
---

# SP9-504: Display odds and ends: 120 Hz black screen, external 4K at 30 Hz, backlight spots after shutdown

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| needs-test | P3 | display | bug | partial | partial | partial |

## Problem

Single reports: selecting 120 Hz gave a black screen on one SP9 (2024); external 4K over USB-C limited to
30 Hz; white backlight spots after shutdown (SP8/SP9); brightness curve not linear.

## Origin

Unknown; each has only one or two reports.

## Reports

- [linux-surface#825](https://github.com/linux-surface/linux-surface/issues/825) (open issue, workaround) "SP8 120Hz mode not available": SP8/SP9 120 Hz (xrandr mode and rate together)
- [linux-surface#899](https://github.com/linux-surface/linux-surface/issues/899) (open issue, unsolved) "Surface Book 3 HDMI 2.0-capable USB C port only supporting 4k30hz max": external 4K at 30 Hz (SP9 confirmation)
- [linux-surface#1725](https://github.com/linux-surface/linux-surface/issues/1725) (open issue, unsolved) "[SP8,SP9] Shutdown causes backlight bleeding / ghosting spots on the display": SP8/SP9 shutdown backlight spots
- [linux-surface#1200](https://github.com/linux-surface/linux-surface/issues/1200) (open issue, question) "SP9 Display brightness mapping": SP9 brightness mapping

## Fixes, patches and PRs

- none yet

## Possible solutions

- Retest each on current Fedora; close or report to drm/i915 with data.

## Next steps

- [ ] Part of phase 0.

## Upstream and people

- Upstream target: drm/i915
- People: none

## Linked issues

- Depends on: [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)
- Blocks: none
- Related: [SP9-503](SP9-503-display-flicker-and-resume-freezes-from-panel-self-refresh.md) Display flicker and resume freezes from Panel Self Refresh, [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/5-audio-display-wireless.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
