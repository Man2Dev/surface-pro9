---
id: SP9-402
title: 'Camera colours are washed out: no libcamera software ISP tuning for OV5693 and OV13858'
labels:
- area:camera
- kind:missing-feature
- priority:P2
- status:fix-pending
depends_on:
- SP9-401
blocks: []
related:
- SP9-401
- SP9-403
- SP9-405
upstream:
- libcamera-devel
source: issues/src/4-camera.yaml
---

# SP9-402: Camera colours are washed out: no libcamera software ISP tuning for OV5693 and OV13858

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P2 | camera | missing-feature | n/a | n/a | broken |

## Problem

With libcamera's simple pipeline and software ISP the SP9 images have wrong colours, because only an
uncalibrated tuning file exists for these sensors.

## Origin

Nobody had converted the Windows tuning (AIQB in the Surface driver package) to libcamera. Emfox Zhou did
for the SP8 and posted it (applies to the SP9 by sensor name). A generic AIQB parser stalled in review.

## Reports

- [docs/subsystems/camera.md](../docs/subsystems/camera.md): colour and tuning notes
- [linux-surface#2166](https://github.com/linux-surface/linux-surface/issues/2166) (open issue, sibling) "Surface Pro 6: OV5693 (front) and OV8865 (rear) cameras produce green output": SP6 cameras green: ISP tuning missing

## Fixes, patches and PRs

- [libcamera patchwork 28886](https://patchwork.libcamera.org/patch/28886/) (new) "[v3] ipa: softisp: Add tuning data for the ov13858 and ov5693 (Emfox Zhou, series 6354)": ipa: softisp: Add tuning data for the ov13858 and ov5693 v3 (Emfox Zhou, no replies yet)
- [libcamera patchwork 27355](https://patchwork.libcamera.org/patch/27355/) (accepted) "ipa: camera_sensor_helper: Add black levels for OV5693 (Dan Scally)": OV5693 black levels (accepted)
- [libcamera patchwork 26761](https://patchwork.libcamera.org/patch/26761/) (changes-requested) "[v4,2/2] utils: tuning: Add AIQB parser for Intel IPU6 sensors (Javier Tia, series 5948)": utils: tuning: AIQB parser for Intel IPU6 sensors (changes requested, stalled)
- [libcamera patchwork 28721](https://patchwork.libcamera.org/patch/28721/) (new) "[v2,2/2] libcamera: pipeline: simple: Do not alloc CMA DMA-buffers for camss and ipu6/7 (Hans de Goede, series 6320)": simple pipeline: no CMA DMA buffers for ipu6/7 (Hans de Goede, pending)

## Possible solutions

- Test v3 on the SP9 and reply with Tested-by; compare the SP9 AIQB with the SP8 values.

## Next steps

- [ ] Apply series 6354 to libcamera, run qcam on the SP9 front and rear cameras.

## Upstream and people

- Upstream target: libcamera-devel
- People: Emfox Zhou, Javier Tia, Hans de Goede

## Linked issues

- Depends on: [SP9-401](SP9-401-front-camera-ov5693-returns-empty-buffers-on-mainline-7-4-2x.md) Front camera (OV5693) returns empty buffers on mainline 7.4: 2x2 binned mode with flips fails
- Blocks: none
- Related: [SP9-401](SP9-401-front-camera-ov5693-returns-empty-buffers-on-mainline-7-4-2x.md) Front camera (OV5693) returns empty buffers on mainline 7.4: 2x2 binned mode with flips fails, [SP9-403](SP9-403-rear-camera-ov13858-finish-the-upstream-series-and-drop-the.md) Rear camera (OV13858): finish the upstream series and drop the broken downstream link-frequency entry, [SP9-405](SP9-405-cameras-unusable-in-browsers-and-video-calls-without-workaro.md) Cameras unusable in browsers and video calls without workarounds (v4l2loopback, 64-node limit)

## Knowledge base

- [data/indexes/trackers.tsv](../data/indexes/trackers.tsv)

_Generated from `issues/src/4-camera.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
