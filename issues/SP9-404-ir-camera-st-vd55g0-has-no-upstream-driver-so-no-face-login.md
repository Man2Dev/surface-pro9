---
id: SP9-404
title: IR camera (ST VD55G0) has no upstream driver, so no face login
labels:
- area:camera
- kind:missing-driver
- priority:P3
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-401
upstream:
- linux-media
source: issues/src/4-camera.yaml
---

# SP9-404: IR camera (ST VD55G0) has no upstream driver, so no face login

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P3 | camera | missing-driver | broken | broken | broken |

## Problem

The IR camera used for Windows Hello does not work; face login (Howdy) is impossible.

## Origin

Two competing VD55G0 series are on linux-media and maintainers have not picked one. The IR flood LED GPIO
(int3472 type 0x02) is already mapped in mainline 7.4.

## Reports

- [linux-surface discussion 2198](https://github.com/linux-surface/linux-surface/discussions/2198) (discussion) "Surface Pro 9 camera working on Linux Mint (front + rear, IPU6/ov5693) full writeup": SP9 camera discussion incl. IR
- [rhbz#2509956](https://bugzilla.redhat.com/show_bug.cgi?id=2509956) (NEW) "IR camera ST VD55G1 (ACPI TBE20A1) on ThinkPad X1 Carbon Gen 14 not enumerated: vd55g1 lacks ACPI support": ThinkPad VD55G1: three-piece recipe
- [rhbz#2516222](https://bugzilla.redhat.com/show_bug.cgi?id=2516222) (NEW) "int3472-discrete: GPIO type 0x02 unknown, IPU6 camera non-functional (Dell Pro Max 14 Premium)": int3472 GPIO type 0x02 on Dell

## Fixes, patches and PRs

- [lore:20261110195454.48176-2-lsa.uz@pm.me](https://lore.kernel.org/r/20261110195454.48176-2-lsa.uz@pm.me) (linux-media, new, Sergey Lebedev, 2026-11-10) "media: Add the ST VD55G0 global shutter sensor (v2)": Add the ST VD55G0 global shutter sensor (Lebedev, v4 dt-bindings part)
- [lore:20260918221705.323510-2-pm@petermarshall.ca](https://lore.kernel.org/r/20260918221705.323510-2-pm@petermarshall.ca) (linux-media, handled-elsewhere/new, Peter Marshall, 2026-09-18) "media: i2c: st-vd55g1: Genericize driver and add VD55G0 support (SP9 IR camera, petm5)": st-vd55g1: genericize and add VD55G0 (Marshall)
- [linux-surface/kernel#169](https://github.com/linux-surface/kernel/issues/169) (open PR, on-list) "media: i2c: st-vd55g: Genericize driver and add VD55G0 support": VD55G0 in linux-surface (petm5, on-list)
- [lore:20260401203638.1601661-5-mnencia@kcore.it](https://lore.kernel.org/r/20260401203638.1601661-5-mnencia@kcore.it) (platform-driver-x86, superseded/changes-requested/accepted, Marco Nenciarini, 2026-04-01) "[v8] platform/x86: int3472: Add support for GPIO type 0x02 (IR flood LED)": int3472 GPIO type 0x02 (IR flood LED), accepted

## Possible solutions

- Test the series the media maintainers prefer on the SP9 and reply with Tested-by.

## Next steps

- [ ] Low priority until one series is picked.

## Upstream and people

- Upstream target: linux-media
- People: Sergey Lebedev, Peter Marshall, petm5, fildunsky

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-401](SP9-401-front-camera-ov5693-returns-empty-buffers-on-mainline-7-4-2x.md) Front camera (OV5693) returns empty buffers on mainline 7.4: 2x2 binned mode with flips fails

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/4-camera.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
