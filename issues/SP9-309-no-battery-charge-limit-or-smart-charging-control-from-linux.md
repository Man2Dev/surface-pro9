---
id: SP9-309
title: No battery charge limit or smart charging control from Linux
labels:
- area:battery
- kind:missing-feature
- priority:P3
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-308
- SP9-310
upstream:
- platform-driver-x86
- linux-pm (charge_types)
source: issues/src/3-power.yaml
---

# SP9-309: No battery charge limit or smart charging control from Linux

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P3 | battery | missing-feature | broken | broken | broken |

## Problem

The UEFI battery limit is a fixed 50 % on/off; Linux cannot set a charge limit or smart charging.

## Origin

No driver uses the SAM BAT charge-mode commands. Cloveian decoded them from Microsoft's
SurfaceCommonHeadersDotNet.dll (1017 SSH commands in 36 categories) and wrote a patch using the standard
charge_types and charge_control_end_threshold attributes.

## Reports

- [linux-surface#1580](https://github.com/linux-surface/linux-surface/issues/1580) (open issue, unsolved) "Battery limit": battery limit (qzed: 80 % limiter is EC controlled)

## Fixes, patches and PRs

- [linux-surface/kernel#167](https://github.com/linux-surface/kernel/issues/167) (open PR, needs-update) "Support smart charging and battery authentication status": smart charging and battery authentication status (petm5), qzed asked to split the charge limit out
- [github.com/linux-surface/kernel/compare/v7.3-surface-devel...Clovei...](https://github.com/linux-surface/kernel/compare/v7.3-surface-devel...Cloveian:kernel:battery-charge-limit): Cloveian's charge limit branch (not a PR yet)

## Possible solutions

- Ask Cloveian to open the charge limit PR; test on the SP9; then upstream to platform-driver-x86.

## Next steps

- [ ] Test Cloveian's branch on an SP9 (registers only if BAT 0x23 and 0x09 work).

## Upstream and people

- Upstream target: platform-driver-x86, linux-pm (charge_types)
- People: Cloveian, petm5, qzed, Jelle van der Waa

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-308](SP9-308-sp9-stops-charging-on-ac-needs-a-uefi-battery-limit-toggle-t.md) SP9 stops charging on AC (needs a UEFI battery limit toggle to recover), [SP9-310](SP9-310-fan-runs-at-high-speed-after-using-windows-fan-floor-left-se.md) Fan runs at high speed after using Windows (fan floor left set in SAM)

## Knowledge base

- [status.yaml](../status.yaml)
- [data/indexes/branches.tsv](../data/indexes/branches.tsv)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
