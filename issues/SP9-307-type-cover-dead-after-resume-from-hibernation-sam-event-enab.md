---
id: SP9-307
title: Type Cover dead after resume from hibernation (SAM event enable times out)
labels:
- area:power
- kind:bug
- priority:P2
- status:open
depends_on: []
blocks: []
related:
- SP9-202
- SP9-306
upstream:
- platform-driver-x86 (Maximilian Luz)
source: issues/src/3-power.yaml
---

# SP9-307: Type Cover dead after resume from hibernation (SAM event enable times out)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P2 | power | bug | broken | broken | broken |

## Problem

After resuming from S4 the cover keyboard and touchpad stay dead until the cover is detached and
reattached (SP8 report; the SP9 uses the same restore path).

## Origin

During restore, SAM event source enable requests time out (-110) because the EC is not ready yet. A retry
200 ms later succeeds (pentop, tested diagnostic patch against 6.19.8).

## Reports

- [linux-surface#2294](https://github.com/linux-surface/linux-surface/issues/2294) (open issue, patch-pending) "[SP8] Type Cover keyboard/touchpad dead after resume from hibernation": SP8 cover dead after hibernation, root cause and tested patch

## Fixes, patches and PRs

- [linux-surface#2294](https://github.com/linux-surface/linux-surface/issues/2294) (open issue, patch-pending) "[SP8] Type Cover keyboard/touchpad dead after resume from hibernation": pentop's diagnostic patch (in the issue): retry failed re-enables from a work item

## Possible solutions

- Proper fix: queue failed re-enables from ssam_serial_hub_pm_restore() to a work item, or let surface_hid re-enable its event sources on resume; send to platform-driver-x86 with pentop.

## Next steps

- [ ] Reproduce on an SP9 once hibernate works, ask pentop whether he plans to send it.

## Upstream and people

- Upstream target: platform-driver-x86 (Maximilian Luz)
- People: pentop

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-202](SP9-202-type-cover-dead-or-slow-after-boot-sam-probe-returns-einval.md) Type Cover dead or slow after boot: SAM probe returns -EINVAL before the pin controller is ready, [SP9-306](SP9-306-hibernate-is-unavailable-with-secure-boot-kernel-lockdown.md) Hibernate is unavailable with Secure Boot (kernel lockdown)

## Knowledge base

- [docs/research/open-issues.md](../docs/research/open-issues.md)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
