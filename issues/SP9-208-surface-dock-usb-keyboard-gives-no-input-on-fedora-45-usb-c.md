---
id: SP9-208
title: Surface Dock USB keyboard gives no input on Fedora 45; USB-C UCSI over SAM missing
labels:
- area:usb
- kind:bug
- priority:P3
- status:open
depends_on: []
blocks: []
related: []
upstream:
- linux-usb (typec/ucsi)
source: issues/src/2-cover-input.yaml
---

# SP9-208: Surface Dock USB keyboard gives no input on Fedora 45; USB-C UCSI over SAM missing

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P3 | usb | bug | partial | partial | partial |

## Problem

A USB keyboard behind the Surface Dock (Surface Connect) is detected but gives no input on Fedora 45.
USB-C UCSI (charger and role reporting) over the SAM HID node has no driver.

## Origin

Unknown for the dock keyboard. UCSI: the SP9 group has ssam_node_hid_sam_ucm_ucsi but no consumer driver.

## Reports

- [linux-surface#2371](https://github.com/linux-surface/linux-surface/issues/2371) (open issue, unsolved) "Surface Pro 9 Fedora 45 Dock USB no input from keyboard": SP9 Fedora 45 dock USB keyboard no input

## Fixes, patches and PRs

- [linux-surface/kernel#184](https://github.com/linux-surface/kernel/issues/184) (open PR, active) "usb: typec: ucsi: Add Surface UCSI-over-HID driver & charger Artg support": UCSI over SAM HID driver (active, tested by qzed on Pro X)

## Possible solutions

- Test kernel#184 on the SP9.

## Next steps

- [ ] Low priority; collect lsusb -t and evtest from the dock case.

## Upstream and people

- Upstream target: linux-usb (typec/ucsi)
- People: JValdivia23, qzed

## Linked issues

- Depends on: none
- Blocks: none
- Related: none

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/2-cover-input.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
