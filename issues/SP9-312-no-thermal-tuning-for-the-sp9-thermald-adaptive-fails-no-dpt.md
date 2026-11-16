---
id: SP9-312
title: No thermal tuning for the SP9 (thermald adaptive fails, no DPTF tables)
labels:
- area:fan
- kind:missing-feature
- priority:P3
- status:open
depends_on: []
blocks: []
related:
- SP9-310
upstream:
- intel/thermal_daemon
source: issues/src/3-power.yaml
---

# SP9-312: No thermal tuning for the SP9 (thermald adaptive fails, no DPTF tables)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P3 | fan | missing-feature | partial | partial | partial |

## Problem

thermald --adaptive fails on the SP9 and thermald ships no Surface configuration, so power limits and
passive cooling are not tuned as on Windows.

## Origin

No DPTF tables; thermald blacklists a zone called "Surface". A hand-written thermal-conf.xml exists
downstream.

## Reports

- [intel/thermal_daemon#616](https://github.com/intel/thermal_daemon/issues/616) (open) "Reproducing Windows-style PL1 control (skin + CPU) with thermal-conf.xml": Windows-style PL1 control on SB3 (open, unanswered)
- [linux-surface discussion 1734](https://github.com/linux-surface/linux-surface/discussions/1734) (discussion) "[SP9] Thermal/Power setup to prevent throttling": thermald setup

## Fixes, patches and PRs

- [github.com/iwanders/nixos-surface](https://github.com/iwanders/nixos-surface): hand-written thermald config (thermald/)

## Possible solutions

- Evaluate iwanders' config on the SP9; only upstream to thermald if it clearly helps.

## Next steps

- [ ] Low priority.

## Upstream and people

- Upstream target: intel/thermal_daemon
- People: iwanders, larsschellhas

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-310](SP9-310-fan-runs-at-high-speed-after-using-windows-fan-floor-left-se.md) Fan runs at high speed after using Windows (fan floor left set in SAM)

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
