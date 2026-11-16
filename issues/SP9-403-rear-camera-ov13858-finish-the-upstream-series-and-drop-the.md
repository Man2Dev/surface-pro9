---
id: SP9-403
title: 'Rear camera (OV13858): finish the upstream series and drop the broken downstream link-frequency entry'
labels:
- area:camera
- kind:upstreaming
- priority:P2
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-401
- SP9-402
upstream:
- linux-media
source: issues/src/4-camera.yaml
---

# SP9-403: Rear camera (OV13858): finish the upstream series and drop the broken downstream link-frequency entry

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P2 | camera | upstreaming | partial | partial | broken |

## Problem

The rear camera probes on 7.4 (sensor config, upside-down quirk), but flip controls, regulator handling,
colorspace and gain cap are still pending, and the linux-surface 7.3 entry declares four link frequencies
with only one listed, which breaks probing (-22).

## Origin

Downstream PR 1867 entry IPU_SENSOR_CONFIG("OVTID858", 4, 540000000) versus mainline (2, 540 and 270 MHz).

## Reports

- [linux-surface#1753](https://github.com/linux-surface/linux-surface/issues/1753) (open issue, could-close) "Surface Pro 9 Camera probing failed: ov13858 i2c-OVTID858:00 probe failed": SP9 ov13858 probe failed with -22
- [linux-surface#2227](https://github.com/linux-surface/linux-surface/issues/2227) (open PR, needs-update) "cameras: fix Surface Pro 8 and 9 rear OV13858 rotation (180 degrees)": SP8/SP9 rear rotation, red/blue swap in an earlier version

## Fixes, patches and PRs

- [torvalds/linux@2ee01a094aba](https://git.kernel.org/torvalds/c/2ee01a094aba): ipu-bridge: Add OV13858 sensor config (Lebedev)
- [linux-surface/kernel#191](https://github.com/linux-surface/kernel/issues/191) (open PR, waiting) "media: ipu-bridge: fix the OVTID858 link frequency count": fix the OVTID858 link frequency count
- [linux-surface/kernel#174](https://github.com/linux-surface/kernel/issues/174) (open PR, stalled) "media: intel/ipu-bridge: fix OVTID858 link frequencies": same fix, competing
- [linux-surface/kernel#170](https://github.com/linux-surface/kernel/issues/170) (closed PR, merged) "Surface Pro 9: fix rear camera rotation": SP9 rear camera rotation (merged downstream)
- [lore:20260930073308.56811-1-lsa.uz@pm.me](https://lore.kernel.org/r/20260930073308.56811-1-lsa.uz@pm.me) (linux-media, new, Sergey Lebedev, 2026-09-30) "[v4] media: i2c: ov13858: add horizontal and vertical flip controls": ov13858 flip controls v4
- [lore:20261016210246.58562-1-lsa.uz@pm.me](https://lore.kernel.org/r/20261016210246.58562-1-lsa.uz@pm.me) (linux-media, new, Sergey Lebedev, 2026-10-16) "[v4] media: i2c: ov13858: add regulator, clock and reset GPIO handling": ov13858 regulator, clock and reset GPIO v4
- [lore:20261016-ov13858-colorspace-v1-1-51f0379ada0c@gmail.com](https://lore.kernel.org/r/20261016-ov13858-colorspace-v1-1-51f0379ada0c@gmail.com) (linux-media, new, George Neacsu, 2026-10-16) "media: i2c: ov13858: Set the colorspace in the pad format": ov13858 colorspace
- [lore:20261002093507.43584-1-lsa.uz@pm.me](https://lore.kernel.org/r/20261002093507.43584-1-lsa.uz@pm.me) (linux-media, new, Sergey Lebedev, 2026-10-02) "[v2] media: i2c: ov13858: cap analogue gain at 15.5x": ov13858 gain cap

## Possible solutions

- On 7.4 drop the downstream entry; test the pending ov13858 patches on the SP9 and send Tested-by.

## Next steps

- [ ] Test on Fedora rawhide 7.4 plus the pending series.

## Upstream and people

- Upstream target: linux-media
- People: Sergey Lebedev, George Neacsu, jmmartinf

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-401](SP9-401-front-camera-ov5693-returns-empty-buffers-on-mainline-7-4-2x.md) Front camera (OV5693) returns empty buffers on mainline 7.4: 2x2 binned mode with flips fails, [SP9-402](SP9-402-camera-colours-are-washed-out-no-libcamera-software-isp-tuni.md) Camera colours are washed out: no libcamera software ISP tuning for OV5693 and OV13858

## Knowledge base

- [docs/subsystems/camera.md](../docs/subsystems/camera.md)

_Generated from `issues/src/4-camera.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
