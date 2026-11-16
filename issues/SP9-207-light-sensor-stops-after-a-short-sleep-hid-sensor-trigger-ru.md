---
id: SP9-207
title: Light sensor stops after a short sleep (hid-sensor-trigger runtime PM bug)
labels:
- area:sensors
- kind:bug
- priority:P2
- status:open
depends_on: []
blocks: []
related:
- SP9-206
upstream:
- linux-iio (Jiri Kosina, Srinivas Pandruvada, Jonathan Cameron)
source: issues/src/2-cover-input.yaml
---

# SP9-207: Light sensor stops after a short sleep (hid-sensor-trigger runtime PM bug)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P2 | sensors | bug | broken | broken | broken |

## Problem

With the hysteresis rule in place, the ambient light sensor sometimes returns nothing after a short
suspend; automatic brightness stops until it is toggled.

## Origin

Traced by CmdrShepardsPie with kprobes: if system suspend starts inside hid-sensor-trigger's 3 s
autosuspend window, hid_sensor_suspend() powers the sensor off but leaves runtime PM "active"; on resume
nothing powers it back on and hid_sensor_runtime_resume() is never called. No patch exists.

## Reports

- [linux-surface#2160](https://github.com/linux-surface/linux-surface/issues/2160) (open issue, workaround) "iio-sensor-proxy not working - Surface Laptop Studio (1st gen)": trace and workaround attempts (2026-10-26, 2026-10-27)

## Fixes, patches and PRs

- none yet

## Possible solutions

- Kernel fix in drivers/iio/common/hid-sensors/hid-sensor-trigger.c: mark the device suspended in the system suspend path or re-power it on resume when the buffer is re-enabled.

## Next steps

- [ ] Reproduce on an SP9, write the patch, send to linux-iio with CmdrShepardsPie's analysis credited.

## Upstream and people

- Upstream target: linux-iio (Jiri Kosina, Srinivas Pandruvada, Jonathan Cameron)
- People: CmdrShepardsPie

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-206](SP9-206-rotation-and-light-sensor-hang-in-iio-sensor-proxy-claims-ti.md) Rotation and light sensor hang in iio-sensor-proxy (claims time out, rotation freezes)

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/2-cover-input.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
