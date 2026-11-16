---
id: SP9-605
title: RTC time persistence on the SP9 is unknown (SP7 and SP8 lose clock changes)
labels:
- area:firmware
- kind:needs-test
- priority:P3
- status:needs-test
depends_on:
- SP9-901
blocks: []
related:
- SP9-901
upstream: []
source: issues/src/6-boot-packaging.yaml
---

# SP9-605: RTC time persistence on the SP9 is unknown (SP7 and SP8 lose clock changes)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| needs-test | P3 | firmware | needs-test | unknown | unknown | unknown |

## Problem

On the SP7 and SP8, time set from Linux does not persist across power off; the clock lives in SAM. No SP9
data.

## Origin

The firmware loads the CMOS RTC from the SAM clock at power on; on SP8 it can be set from userspace.

## Reports

- [linux-surface#415](https://github.com/linux-surface/linux-surface/issues/415) (open issue, workaround) "SP7: RTC changes don't persist across reboot": SP7 RTC changes don't persist
- [linux-surface#1497](https://github.com/linux-surface/linux-surface/issues/1497) (open issue, workaround) "Surface Pro 8 loses system time on power off": SP8 loses system time on power off
- [linux-surface#2251](https://github.com/linux-surface/linux-surface/issues/2251) (open issue, workaround) "Surface Pro 8: RTC resets at every boot. Workaround: set the SAM clock": SP8: set the SAM clock from userspace (workaround)
- [linux-surface#1658](https://github.com/linux-surface/linux-surface/issues/1658) (open issue, workaround) "BUG: rtc can't be changed from system": RTC can't be changed from the system

## Fixes, patches and PRs

- none yet

## Possible solutions

- If the SP9 is affected, use the SP8 userspace method (#2251) and consider a SAM RTC driver upstream.

## Next steps

- [ ] Run timedatectl right after a cold boot with networking off.

## Commands

```
timedatectl
```

## Upstream and people

- Upstream target: none
- People: nicheosala, danielzgtg

## Linked issues

- Depends on: [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)
- Blocks: none
- Related: [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)

## Knowledge base

- [docs/testing.md](../docs/testing.md)

_Generated from `issues/src/6-boot-packaging.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
