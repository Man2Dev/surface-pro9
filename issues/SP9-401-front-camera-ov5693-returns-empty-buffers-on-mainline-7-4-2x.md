---
id: SP9-401
title: 'Front camera (OV5693) returns empty buffers on mainline 7.4: 2x2 binned mode with flips fails'
labels:
- area:camera
- kind:bug
- priority:P1
- status:fix-pending
depends_on: []
blocks:
- SP9-402
- SP9-405
- SP9-903
related:
- SP9-402
- SP9-403
- SP9-404
- SP9-405
- SP9-406
upstream:
- 'linux-media (sensor drivers: Sakari Ailus)'
source: issues/src/4-camera.yaml
---

# SP9-401: Front camera (OV5693) returns empty buffers on mainline 7.4: 2x2 binned mode with flips fails

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P1 | camera | bug | partial | partial | broken |

## Problem

Mainline 7.4 has all the SP9 front camera plumbing, but libcamera picks the binned 1296x972 mode with both
flips (the sensor is mounted 180 degrees) and that mode gives CSI-2 frame sync errors, so applications get
empty frames.

## Origin

The ov5693 driver's binned mode does not stream correctly on IPU6 when flips are on. D. Manresa wrote a fix
(#2252); it was never posted. Simon Kruse has Manresa's go-ahead to send it to linux-media but it must be
rebased on Rimoli's clock-lane gate first (do not send 548281df as is). Manresa cannot respin (hardware donated).

## Reports

- [dmanresa-saes/surface-ipu6-cameras#1](https://github.com/dmanresa-saes/surface-ipu6-cameras/issues/1) (open) "Upstreaming the ov5693 binned-mode patch: Surface Pro 9 results and credit": SP9 results on media next, upstreaming agreement
- [linux-surface#2234](https://github.com/linux-surface/linux-surface/issues/2234) (open issue, patch-pending) "ov5693 on IPU6 (Surface Pro 8): 2x-binned 1296x972 readout returns zero frames": SP8 binned mode zero-byte buffers; fails only with flips on (2026-11-10)
- [linux-surface#2154](https://github.com/linux-surface/linux-surface/issues/2154) (open issue, sibling) "Surface Go 4 IPU6 camera status: rear OV8865 detected/partially st": Surface Go 4 front camera status

## Fixes, patches and PRs

- [linux-surface#2252](https://github.com/linux-surface/linux-surface/issues/2252) (open PR, waiting) "cameras: Surface Pro 7+: make the binned OV5693 stream on IPU6, drive the IR illuminator": D. Manresa's binned-mode patch (linux-surface PR)
- [linux-surface/kernel#181](https://github.com/linux-surface/kernel/issues/181) (open PR, active) "media: Surface Pro 5 (IPU3) camera fixes: OV8865, OV5693, OV7251 IR illuminator": carries the same patch for the SP5 tree
- [linux-surface/kernel#193](https://github.com/linux-surface/kernel/issues/193) (open PR, new) "Backports the v7.4-rc1 camera work to 7.3: Sakari ipu_bridge_get_ipu6(), Rimoli's ov5693 c": backports the 7.4 camera work to 7.3 (CmdrShepardsPie)
- [torvalds/linux@df7980112cee](https://git.kernel.org/torvalds/c/df7980112cee): ov5693: Add OVTI5693 ACPI HID (Rimoli)
- [torvalds/linux@0e12587945f6](https://git.kernel.org/torvalds/c/0e12587945f6): ov5693: gate the MIPI clock lane for non-continuous clock (Rimoli)
- [torvalds/linux@8e3def7bf410](https://git.kernel.org/torvalds/c/8e3def7bf410): ipu-bridge: request non-continuous clock for ov5693 on IPU6 (Rimoli)
- [torvalds/linux@db44b1792898](https://git.kernel.org/torvalds/c/db44b1792898): ipu-bridge: SP9 upside-down sensor quirks (Rimoli)
- [lore:20261029-ov5693-fixes-v2-1-2526d7b13030@gmail.com](https://lore.kernel.org/r/20261029-ov5693-fixes-v2-1-2526d7b13030@gmail.com) (linux-media, new, Marco Ziliani, 2026-10-29) "[v2] media: i2c: ov5693: Fix mode changes, flips and autosuspend": ov5693 mode changes, flips, autosuspend (Ziliani, pending)

## Possible solutions

- When Simon Kruse posts the rebased patch, test it on the SP9 (Fedora rawhide 7.4 kernel plus patch) and reply with Tested-by.

## Next steps

- [ ] Watch linux-media for Simon Kruse's posting; until then test #2252 on 7.4.

## Upstream and people

- Upstream target: linux-media (sensor drivers: Sakari Ailus)
- People: D. Manresa, Simon Kruse, Fernando Rimoli, CmdrShepardsPie

## Linked issues

- Depends on: none
- Blocks: [SP9-402](SP9-402-camera-colours-are-washed-out-no-libcamera-software-isp-tuni.md), [SP9-405](SP9-405-cameras-unusable-in-browsers-and-video-calls-without-workaro.md), [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-402](SP9-402-camera-colours-are-washed-out-no-libcamera-software-isp-tuni.md) Camera colours are washed out: no libcamera software ISP tuning for OV5693 and OV13858, [SP9-403](SP9-403-rear-camera-ov13858-finish-the-upstream-series-and-drop-the.md) Rear camera (OV13858): finish the upstream series and drop the broken downstream link-frequency entry, [SP9-404](SP9-404-ir-camera-st-vd55g0-has-no-upstream-driver-so-no-face-login.md) IR camera (ST VD55G0) has no upstream driver, so no face login, [SP9-405](SP9-405-cameras-unusable-in-browsers-and-video-calls-without-workaro.md) Cameras unusable in browsers and video calls without workarounds (v4l2loopback, 64-node limit), [SP9-406](SP9-406-camera-fails-to-re-probe-after-intel-ipu6-reload-or-hibernat.md) Camera fails to re-probe after intel-ipu6 reload or hibernate

## Knowledge base

- [docs/subsystems/camera.md](../docs/subsystems/camera.md)
- [status.yaml](../status.yaml)

_Generated from `issues/src/4-camera.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
