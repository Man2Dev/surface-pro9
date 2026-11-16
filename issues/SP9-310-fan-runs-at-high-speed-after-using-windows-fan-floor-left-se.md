---
id: SP9-310
title: Fan runs at high speed after using Windows (fan floor left set in SAM)
labels:
- area:fan
- kind:bug
- priority:P2
- status:open
depends_on: []
blocks: []
related:
- SP9-309
- SP9-311
- SP9-312
upstream:
- platform-driver-x86
source: issues/src/3-power.yaml
---

# SP9-310: Fan runs at high speed after using Windows (fan floor left set in SAM)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P2 | fan | bug | broken | broken | broken |

## Problem

After Windows has run, the SP9 fan can stay around 3800 rpm at low temperature under Linux.

## Origin

Windows sets a minimum fan speed with SAM FAN command 0x0b (SetMinFanRpm); Linux never clears it
(petm5's serial trace, Cloveian's decoding; FAN 0x17 reads it back).

## Reports

- [linux-surface#1726](https://github.com/linux-surface/linux-surface/issues/1726) (open issue, patch-pending) "Surface Pro 9: Fan running at high speed (~3800 RPM) despite low temperatures": SP9 fan at ~3800 rpm despite low temperature

## Fixes, patches and PRs

- none yet

## Possible solutions

- Send FAN 0x0b with 0 at probe from surface_platform_profile (small upstream patch next to the fan standby series).
- Workaround: boot Windows and let the fan stop, or send the command with the SAM debug scripts.

## Next steps

- [ ] Read FAN 0x17 on an SP9 via surface_aggregator_cdev to see if a floor is set.

## Upstream and people

- Upstream target: platform-driver-x86
- People: petm5, Cloveian, Peter Marshall

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-309](SP9-309-no-battery-charge-limit-or-smart-charging-control-from-linux.md) No battery charge limit or smart charging control from Linux, [SP9-311](SP9-311-fan-keeps-running-during-suspend.md) Fan keeps running during suspend, [SP9-312](SP9-312-no-thermal-tuning-for-the-sp9-thermald-adaptive-fails-no-dpt.md) No thermal tuning for the SP9 (thermald adaptive fails, no DPTF tables)

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
