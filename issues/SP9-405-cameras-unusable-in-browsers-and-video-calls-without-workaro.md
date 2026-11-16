---
id: SP9-405
title: Cameras unusable in browsers and video calls without workarounds (v4l2loopback, 64-node limit)
labels:
- area:camera
- kind:bug
- priority:P2
- status:open
depends_on:
- SP9-401
blocks: []
related:
- SP9-401
- SP9-402
upstream:
- PipeWire / browsers
source: issues/src/4-camera.yaml
---

# SP9-405: Cameras unusable in browsers and video calls without workarounds (v4l2loopback, 64-node limit)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P2 | camera | bug | partial | partial | partial |

## Problem

Browsers and Zoom/Teams do not see libcamera cameras directly; people use v4l2loopback or relays, and
intel-ipu6-isys registers 64 video nodes, which pushes a loopback device past WebRTC's limit.

## Origin

IPU6 needs libcamera; apps need PipeWire camera support (Firefox/Chromium flags) or a V4L2 bridge.

## Reports

- [linux-surface#2242](https://github.com/linux-surface/linux-surface/issues/2242) (open issue, workaround) "WebRTC / Zoom: V4L2 64-device limit on IPU6 Surface devices drops virtual camera": V4L2 64-device limit drops the loopback camera
- [linux-surface#1893](https://github.com/linux-surface/linux-surface/issues/1893) (open issue, other) "Surface Pro 8 camera support": SP8 front camera in Firefox and Chromium through PipeWire on a stock kernel
- [linux-surface discussion 2198](https://github.com/linux-surface/linux-surface/discussions/2198) (discussion) "Surface Pro 9 camera working on Linux Mint (front + rear, IPU6/ov5693) full writeup": relay and loopback recipes

## Fixes, patches and PRs

- [luqqas96/surface-zoom-bridge](https://github.com/luqqas96/surface-zoom-bridge): LD_PRELOAD shim and dual loopback bridge

## Possible solutions

- Prefer the PipeWire camera portal (Firefox media.webrtc.camera.allow-pipewire, Chromium flag); document it for Fedora.

## Next steps

- [ ] Test PipeWire camera access in Firefox on an SP9 once SP9-401 works.

## Upstream and people

- Upstream target: PipeWire / browsers
- People: luqqas96, nicheosala

## Linked issues

- Depends on: [SP9-401](SP9-401-front-camera-ov5693-returns-empty-buffers-on-mainline-7-4-2x.md) Front camera (OV5693) returns empty buffers on mainline 7.4: 2x2 binned mode with flips fails
- Blocks: none
- Related: [SP9-401](SP9-401-front-camera-ov5693-returns-empty-buffers-on-mainline-7-4-2x.md) Front camera (OV5693) returns empty buffers on mainline 7.4: 2x2 binned mode with flips fails, [SP9-402](SP9-402-camera-colours-are-washed-out-no-libcamera-software-isp-tuni.md) Camera colours are washed out: no libcamera software ISP tuning for OV5693 and OV13858

## Knowledge base

- [docs/subsystems/camera.md](../docs/subsystems/camera.md)

_Generated from `issues/src/4-camera.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
