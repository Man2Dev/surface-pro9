---
id: SP9-105
title: iptsd service and udev rule are fragile (stops after cold boot, probes every hidraw, loses its tag)
labels:
- area:touch
- kind:bug
- priority:P1
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-102
- SP9-106
upstream:
- linux-surface/iptsd
source: issues/src/1-touch-pen.yaml
---

# SP9-105: iptsd service and udev rule are fragile (stops after cold boot, probes every hidraw, loses its tag)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P1 | touch | bug | n/a | partial | n/a |

## Problem

iptsd@.service can stop itself about 6 s after a cold boot; the udev rule runs iptsd-check-device on every
hidraw node, which can stall input for seconds or lock the user out at the lock screen; a udev change
event drops the systemd tag so the service loses its device; raw ITHC input nodes duplicate iptsd's events.

## Origin

`StopWhenUnneeded=yes` in the unit, an udev rule matching `ACTION=="add"` only, and a probe that is not
limited to ITHC/IPTS devices. All have small fixes posted as PRs with no maintainer reply.

## Reports

- [linux-surface/iptsd#228](https://github.com/linux-surface/iptsd/issues/228) (open issue, patch-pending) "iptsd-check-device causes 6s bus timeout on AMD Surface Laptop 4 SPI touchscreen": iptsd-check-device causes 6 s bus timeout on AMD SL4 SPI touchscreen
- [linux-surface/iptsd#229](https://github.com/linux-surface/iptsd/issues/229) (open issue, patch-pending) "udev rule probes every hidraw node, including USB HID; a blocking probe": udev rule probes every hidraw node incl. USB; blocking probe locks out the lock screen
- [linux-surface/iptsd#163](https://github.com/linux-surface/iptsd/issues/163) (open issue, patch-pending) "iptsd@.service unit file loses access to the ipts device unit service": service loses access to the device after a change event
- [linux-surface/iptsd#220](https://github.com/linux-surface/iptsd/issues/220) (open issue, patch-pending) "udev: Ignore raw Intel Touch Host Controller input nodes to prevent dupl": duplicate raw ITHC input nodes and 16:9 distortion
- [linux-surface#2299](https://github.com/linux-surface/linux-surface/issues/2299) (open issue, workaround) "ipts: controller fails to resume with -EAGAIN after a short suspend": IPTS resume -EAGAIN leaves iptsd unkillable (OnFailure= recovery)

## Fixes, patches and PRs

- [linux-surface/iptsd#219](https://github.com/linux-surface/iptsd/issues/219) (open PR, waiting) "iptsd@.service stops itself ~6s after start on cold boot due to StopWhenUnneeded": remove StopWhenUnneeded=yes (service stops ~6 s after cold boot)
- [linux-surface/iptsd#221](https://github.com/linux-surface/iptsd/issues/221) (open PR, waiting) "udev: hide raw ithc input nodes duplicated by iptsd": hide raw ITHC input nodes
- [linux-surface/iptsd#224](https://github.com/linux-surface/iptsd/issues/224) (open PR, waiting) "udev: Keep the systemd tag across change events": keep the systemd tag across change events

## Possible solutions

- Review and test the three PRs on the SP9; ask the iptsd maintainer (StollD) to merge; carry them in the Fedora package meanwhile.
- Restrict the udev probe to known THC/IPTS hidraw parents.

## Next steps

- [ ] Test #219, #221 and #224 together on the SP9 and post Tested-by on each PR.

## Upstream and people

- Upstream target: linux-surface/iptsd
- People: StollD, L0g0ff, luqqas96, fildunsky, sangesi

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-102](SP9-102-iptsd-is-not-packaged-in-fedora.md) iptsd is not packaged in Fedora, [SP9-106](SP9-106-erratic-touch-detection-and-weak-palm-rejection-with-default.md) Erratic touch detection and weak palm rejection with default iptsd settings

## Knowledge base

- [docs/research/open-prs.md](../docs/research/open-prs.md)
- [data/indexes/open-prs.tsv](../data/indexes/open-prs.tsv)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
