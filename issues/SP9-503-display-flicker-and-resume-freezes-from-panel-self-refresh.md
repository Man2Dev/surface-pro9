---
id: SP9-503
title: Display flicker and resume freezes from Panel Self Refresh
labels:
- area:display
- kind:bug
- priority:P2
- status:needs-test
depends_on:
- SP9-901
blocks: []
related:
- SP9-504
- SP9-901
upstream:
- drm/i915 (freedesktop GitLab)
source: issues/src/5-audio-display-wireless.yaml
---

# SP9-503: Display flicker and resume freezes from Panel Self Refresh

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| needs-test | P2 | display | bug | partial | partial | partial |

## Problem

Screen flicker and random freezes are worked around with i915.enable_psr=0; in 2022 the SP9 wiki recorded a
roughly 50 s frozen screen after resume with an i915 "Selective fetch area calculation failed" message.

## Origin

i915 PSR / PSR2 selective fetch on this panel; the SP10 wiki still uses i915.enable_psr2_sel_fetch=0.

## Reports

- [linux-surface#862](https://github.com/linux-surface/linux-surface/issues/862) (closed issue, workaround) "SP8 - Screen flickering": SP8 flicker: i915.enable_psr=0
- [linux-surface#1208](https://github.com/linux-surface/linux-surface/issues/1208) (open issue, workaround) "SP7: Occasional hard freezes / stutters / lag": SP7 freezes fixed by i915.enable_psr=0
- [NixOS/nixos-hardware#941](https://github.com/NixOS/nixos-hardware/issues/941) (closed) "New hardware config: Surface Pro 9": SP9 config disables PSR
- [pop-os/cosmic-comp#1372](https://github.com/pop-os/cosmic-comp/issues/1372) (closed) "Page flip errors on Surface Pro 9 when fullscreening window (VRR)": SP9 VRR page flip errors

## Fixes, patches and PRs

- none yet

## Possible solutions

- Test the stock Fedora kernel without any PSR parameter; if flicker or resume freezes appear, report to drm/i915 with the panel EDID.

## Next steps

- [ ] Include in the phase 0 test (SP9-901).

## Upstream and people

- Upstream target: drm/i915 (freedesktop GitLab)
- People: none

## Linked issues

- Depends on: [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)
- Blocks: none
- Related: [SP9-504](SP9-504-display-odds-and-ends-120-hz-black-screen-external-4k-at-30.md) Display odds and ends: 120 Hz black screen, external 4K at 30 Hz, backlight spots after shutdown, [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)

## Knowledge base

- [docs/research/wiki-digest.md](../docs/research/wiki-digest.md)
- [status.yaml](../status.yaml)

_Generated from `issues/src/5-audio-display-wireless.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
