---
id: SP9-103
title: Touch and pen stop working after suspend/resume
labels:
- area:touch
- kind:bug
- priority:P1
- status:open
depends_on:
- SP9-101
blocks: []
related:
- SP9-101
- SP9-104
- SP9-302
upstream:
- quo/ithc-linux
- linux-surface
source: issues/src/1-touch-pen.yaml
---

# SP9-103: Touch and pen stop working after suspend/resume

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P1 | touch | bug | n/a | partial | broken |

## Problem

After s2idle resume the touchscreen and pen sometimes stay dead until iptsd or the ITHC module is
restarted. It is the most repeated unsolved touch problem across the linux-surface trackers.

## Origin

Suspected: ITHC tears down and recreates the hid_device on suspend, and iptsd holding the old hidraw
node can deadlock or keep a dead handle (quo, quo/ithc-linux#20; linux-surface#2210 patch description).
Firefox-only loss of touch after sleep (#1402) looks like a separate userspace problem.

## Reports

- [linux-surface#1171](https://github.com/linux-surface/linux-surface/issues/1171) (closed issue, stale) "Touch and pen stopped working after resume from sleep": touch and pen dead after resume; mentions quo's DMA fix b51f328 (closed not planned)
- [linux-surface/iptsd#122](https://github.com/linux-surface/iptsd/issues/122) (closed issue, stale) "Touch and pen stop working after sleep": touch and pen stop after sleep (closed not planned)
- [linux-surface#1799](https://github.com/linux-surface/linux-surface/issues/1799) (closed issue, stale) "[SP10] Dead touchscreen on arch 6.15 kernel": SP10 dead touchscreen after resume (closed without fix)
- [sebanc/brunch#2202](https://github.com/sebanc/brunch/issues/2202) (closed) "Multi touch and pen don't work after sleep mode on Surface Pro 9": SP9 multitouch and pen dead after sleep
- [linux-surface#273](https://github.com/linux-surface/linux-surface/issues/273) (open issue, workaround) "Touchscreen stops working after Resume": touch after resume on older devices; quo explains hidraw recreation
- [linux-surface#1402](https://github.com/linux-surface/linux-surface/issues/1402) (open issue, workaround) "Firefox does not detect touch input after sleep": SP9: only Firefox loses touch after sleep
- [quo/ithc-linux#20](https://github.com/quo/ithc-linux/issues/20) (closed) "Touch screen not working after suspend": SP8 touch after suspend; quo switched to full shutdown and reinit on suspend

## Fixes, patches and PRs

- [linux-surface#2210](https://github.com/linux-surface/linux-surface/issues/2210) (closed PR, promised-never-resubmitted) "Add Linux 7.0 patch series for Surface Pro 9": closed PR carrying 'ithc: Fix PM suspend/resume to preserve hid_device across s2idle' (author never resubmitted)
- [orphaned-patches/linux-surface-2210-ithc-pm-preserve-hid-device.patch](../orphaned-patches/linux-surface-2210-ithc-pm-preserve-hid-device.patch): the extracted patch, applies to v7.3-surface ITHC (dry run), untested

## Possible solutions

- Test the orphaned #2210 patch on the SP9 with an rtcwake loop; if it holds, offer it to quo/ithc-linux with the author's agreement.
- Workaround: restart iptsd from a systemd sleep hook after resume.

## Next steps

- [ ] Reproduce on an SP9 and capture dmesg plus iptsd journal across 10 suspend cycles.

## Commands

```
for i in $(seq 10); do sudo rtcwake -m mem -s 20; sleep 15; journalctl -b -u 'iptsd@*' --since '-1min' | tail -3; done
```

## Upstream and people

- Upstream target: quo/ithc-linux, linux-surface
- People: quo, RowdyRagamuffin

## Linked issues

- Depends on: [SP9-101](SP9-101-touchscreen-and-pen-need-the-out-of-tree-ithc-driver-no-upst.md) Touchscreen and pen need the out-of-tree ITHC driver (no upstream driver for the ADL THC in legacy mode)
- Blocks: none
- Related: [SP9-101](SP9-101-touchscreen-and-pen-need-the-out-of-tree-ithc-driver-no-upst.md) Touchscreen and pen need the out-of-tree ITHC driver (no upstream driver for the ADL THC in legacy mode), [SP9-104](SP9-104-ithc-fails-to-initialise-on-some-boots-or-units-efi-stub-dma.md) ITHC fails to initialise on some boots or units (EFI stub DMA error, legacy init -110), [SP9-302](SP9-302-sp9-sometimes-does-not-wake-from-s2idle-or-hangs-on-the-seco.md) SP9 sometimes does not wake from s2idle (or hangs on the second suspend)

## Knowledge base

- [docs/research/closed-prs.md](../docs/research/closed-prs.md)
- [docs/research/closed-issues.md](../docs/research/closed-issues.md)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
