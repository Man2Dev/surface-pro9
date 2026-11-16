---
id: SP9-206
title: Rotation and light sensor hang in iio-sensor-proxy (claims time out, rotation freezes)
labels:
- area:sensors
- kind:bug
- priority:P1
- status:open
depends_on: []
blocks:
- SP9-903
related:
- SP9-207
upstream:
- iio-sensor-proxy (freedesktop GitLab)
- systemd hwdb
source: issues/src/2-cover-input.yaml
---

# SP9-206: Rotation and light sensor hang in iio-sensor-proxy (claims time out, rotation freezes)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P1 | sensors | bug | partial | partial | broken |

## Problem

With iio-sensor-proxy 3.6+ (Fedora ships 3.9) the SP9 accelerometer and light sensor claims time out,
screen rotation freezes and `systemctl stop iio-sensor-proxy` hangs.

## Origin

The SAM sensor hub (045E:005D) reports accel and light only on change (in_accel_hysteresis 0.05, light 1 /
relative 20) and surface_hid cannot fetch input reports on request, so every sysfs raw read waits 5 s when
the tablet is still. iio-sensor-proxy 3.6+ polls these sensors on its main thread.

## Reports

- [linux-surface#2160](https://github.com/linux-surface/linux-surface/issues/2160) (open issue, workaround) "iio-sensor-proxy not working - Surface Laptop Studio (1st gen)": iio-sensor-proxy not working (SLS); CmdrShepardsPie's SP9 analysis and udev rule
- [hadess/iio-sensor-proxy#432](https://gitlab.freedesktop.org/hadess/iio-sensor-proxy/-/issues/432): upstream issue (not readable from here)
- [linux-surface#1969](https://github.com/linux-surface/linux-surface/issues/1969) (closed issue, workaround) "Long delay to login in KDE-Plasma/Wayland": long KDE Wayland login delay from iio-sensor-proxy
- [linux-surface#1141](https://github.com/linux-surface/linux-surface/issues/1141) (open issue, workaround) "SP9: Screen rotation only works with typecover attached on Fedora 38": SP9 rotation only with cover attached

## Fixes, patches and PRs

- none yet

## Possible solutions

- udev rule setting the hub's hysteresis attributes to 0 (CmdrShepardsPie, tested on SP9 with Fedora 45); copy in docs/workarounds.md.
- Upstream: iio-sensor-proxy sets hysteresis 0 itself, or a hwdb property marks such sensors.

## Next steps

- [ ] Confirm on an SP9, then comment on iio-sensor-proxy#432 with the measurements, crediting CmdrShepardsPie.

## Upstream and people

- Upstream target: iio-sensor-proxy (freedesktop GitLab), systemd hwdb
- People: CmdrShepardsPie, hadess

## Linked issues

- Depends on: none
- Blocks: [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-207](SP9-207-light-sensor-stops-after-a-short-sleep-hid-sensor-trigger-ru.md) Light sensor stops after a short sleep (hid-sensor-trigger runtime PM bug)

## Knowledge base

- [docs/workarounds.md](../docs/workarounds.md)
- [status.yaml](../status.yaml)

_Generated from `issues/src/2-cover-input.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
