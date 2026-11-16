---
id: SP9-203
title: 'Boot stalls about 2 minutes: surface_hid probes the pen stash node and fails with -EPROTO'
labels:
- area:cover
- kind:bug
- priority:P1
- status:open
depends_on: []
blocks:
- SP9-903
related:
- SP9-202
- SP9-209
- SP9-901
upstream:
- linux-input / platform-driver-x86 (Maximilian Luz)
source: issues/src/2-cover-input.yaml
---

# SP9-203: Boot stalls about 2 minutes: surface_hid probes the pen stash node and fails with -EPROTO

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P1 | cover | bug | broken | broken | broken |

## Problem

On Fedora 42/43 the SP9 sits at a black screen for about two minutes before reaching the desktop;
blacklisting surface_hid removes the delay but also the keyboard. Possibly related to the black screen
when booting without the cover.

## Origin

Mainline's ssam_node_group_sp9 lists the KIP pen stash node 01:15:02:02:00. Covers with a pen tray answer
with HID 045E:09B0; covers without one return an empty descriptor, surface_hid fails with -EPROTO
("unexpected descriptor length: got 0, expected 9"). qzed: it should return -ENODEV and refuse quietly.
Why that costs two minutes is not explained yet.

## Reports

- [linux-surface#1845](https://github.com/linux-surface/linux-surface/issues/1845) (open issue, patch-pending) "[SP9] Fedora 42 Hanging on boot with surface_hid": SP9 Fedora 42 hanging on boot with surface_hid (also Fedora 43, SP3)
- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": black screen without cover until the cover is attached

## Fixes, patches and PRs

- none yet

## Possible solutions

- Patch surface_hid to treat an empty descriptor as -ENODEV (small upstream patch to linux-input / platform-driver-x86).
- Find what blocks for two minutes (udev settle, a waiting firmware request) with systemd-analyze and a timed journal.

## Next steps

- [ ] Check an affected boot log, then write and test the patch.

## Commands

```
systemd-analyze blame | head -20
journalctl -b -k | grep -E 'surface_hid|descriptor length'
```

## Upstream and people

- Upstream target: linux-input / platform-driver-x86 (Maximilian Luz)
- People: qzed, AegerUSA

## Linked issues

- Depends on: none
- Blocks: [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-202](SP9-202-type-cover-dead-or-slow-after-boot-sam-probe-returns-einval.md) Type Cover dead or slow after boot: SAM probe returns -EINVAL before the pin controller is ready, [SP9-209](SP9-209-surface-pro-flex-keyboard-untested-on-the-sp9.md) Surface Pro Flex Keyboard untested on the SP9, [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)

## Knowledge base

- [status.yaml](../status.yaml)
- [docs/hardware.md](../docs/hardware.md)

_Generated from `issues/src/2-cover-input.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
