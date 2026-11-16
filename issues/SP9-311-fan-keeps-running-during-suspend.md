---
id: SP9-311
title: Fan keeps running during suspend
labels:
- area:fan
- kind:bug
- priority:P2
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-302
- SP9-310
upstream:
- platform-driver-x86
source: issues/src/3-power.yaml
---

# SP9-311: Fan keeps running during suspend

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P2 | fan | bug | broken | works | broken |

## Problem

If the fan is spinning when the SP9 suspends, it keeps running for a while; on Windows it always stops.
Discussion 2282 reports it after power-button suspends without the cover.

## Origin

The platform profile driver does not put the fan into standby on suspend. linux-surface 7.3 carries Peter
Marshall's fix (kernel#166); the upstream version got changes requested.

## Reports

- [linux-surface#1445](https://github.com/linux-surface/linux-surface/issues/1445) (open issue, unsolved) "[Surface Pro 9] Fan still running during suspend": SP9 fan still running during suspend
- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": fan keeps running after power-button suspend

## Fixes, patches and PRs

- [linux-surface/kernel#166](https://github.com/linux-surface/kernel/issues/166) (closed PR, merged) "platform/surface: platform_profile: add fan power state handling": platform_profile: add fan power state handling (merged downstream 2026-11-09)
- [lore:20261111020916.3557508-2-pm@petermarshall.ca](https://lore.kernel.org/r/20261111020916.3557508-2-pm@petermarshall.ca) (platform-driver-x86, changes-requested, Peter Marshall, 2026-11-11) "platform/surface: platform_profile: handle fan standby state": upstream version, changes requested

## Possible solutions

- Help the upstream version through review (test on SP9, reply with Tested-by).

## Next steps

- [ ] Test on an SP9 with the linux-surface 7.3 kernel.

## Upstream and people

- Upstream target: platform-driver-x86
- People: Peter Marshall

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-302](SP9-302-sp9-sometimes-does-not-wake-from-s2idle-or-hangs-on-the-seco.md) SP9 sometimes does not wake from s2idle (or hangs on the second suspend), [SP9-310](SP9-310-fan-runs-at-high-speed-after-using-windows-fan-floor-left-se.md) Fan runs at high speed after using Windows (fan floor left set in SAM)

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
