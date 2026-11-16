---
id: SP9-604
title: Firmware updates (UEFI, SAM, Type Cover) only work from Windows
labels:
- area:firmware
- kind:missing-feature
- priority:P3
- status:open
depends_on: []
blocks: []
related: []
upstream:
- fwupd
- linux-surface/surface-uefi-firmware
source: issues/src/6-boot-packaging.yaml
---

# SP9-604: Firmware updates (UEFI, SAM, Type Cover) only work from Windows

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P3 | firmware | missing-feature | n/a | partial | broken |

## Problem

Surface firmware is not on LVFS; linux-surface's repack scripts are work in progress and applied only one of
five capsules on an SP9. The Type Cover firmware update node (SAM HID 01:15:02:05) has no fwupd support.

## Origin

Microsoft ships firmware as Windows driver packages; fwupd has a Microsoft CFU plugin only for a USB travel
hub (045E:09BC).

## Reports

- [linux-surface/surface-uefi-firmware#51](https://github.com/linux-surface/surface-uefi-firmware/issues/51) (open issue, unsolved) "failed to run update on reboot: expected 10.162.52737 and got 178441729": SP9 update applied one of five capsules
- [linux-surface/surface-uefi-firmware#48](https://github.com/linux-surface/surface-uefi-firmware/issues/48) (open issue, sibling) "repack.sh packs the wrong payload for components with a Payload/ subdir": repack.sh packs the wrong payload for SurfaceME
- [linux-surface discussion 1746](https://github.com/linux-surface/linux-surface/discussions/1746) (discussion) "[Pro9] No touch or keyboard after 6.12.7": SP9 issues fixed by updating firmware from Windows
- [fwupd/fwupd#10669](https://github.com/fwupd/fwupd/issues/10669) (open) "Updating Microsoft Surface Pro 3 KEK/DB CAs to Microsoft 2023 versions breaks boot at UEFI stage": SP3 KEK/DB update breaks boot (caution)

## Fixes, patches and PRs

- [github.com/fwupd/fwupd/tree/main/plugins/cfu](https://github.com/fwupd/fwupd/tree/main/plugins/cfu): fwupd Microsoft CFU plugin

## Possible solutions

- Keep a Windows install or WinPE stick for firmware; later, ask fwupd whether the cover's SAM HID node speaks CFU.

## Next steps

- [ ] Low priority; record firmware versions in phase 0.

## Upstream and people

- Upstream target: fwupd, linux-surface/surface-uefi-firmware
- People: nicheosala, technobirb

## Linked issues

- Depends on: none
- Blocks: none
- Related: none

## Knowledge base

- [docs/research/upstream-efforts.md](../docs/research/upstream-efforts.md)

_Generated from `issues/src/6-boot-packaging.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
