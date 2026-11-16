---
id: SP9-302
title: SP9 sometimes does not wake from s2idle (or hangs on the second suspend)
labels:
- area:suspend
- kind:bug
- priority:P1
- status:open
depends_on: []
blocks:
- SP9-903
related:
- SP9-103
- SP9-301
- SP9-303
- SP9-304
- SP9-311
upstream:
- thesofproject/linux
- 'linux-gpio (Intel pinctrl: Andy Shevchenko, Mika Westerberg)'
source: issues/src/3-power.yaml
---

# SP9-302: SP9 sometimes does not wake from s2idle (or hangs on the second suspend)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P1 | suspend | bug | partial | partial | partial |

## Problem

Intermittently the SP9 does not resume from s2idle; only a long power-button press helps. Several users
report it gets worse when the cover is opened or closed during suspend.

## Origin

Not settled. Two concrete leads from the Surface Laptop 5 (same Alder Lake-P platform):
(1) the SOF audio DSP 8086:51c8 stays in D0 after the first resume and the second suspend hangs; forcing
legacy HDA (snd_intel_dspcfg.dsp_driver=1) fixed it (#1010); the SP9 has the same audio controller.
(2) INTC1055 pin 213 PADCFG0 gets corrupted in s2idle and fires GPE 0x52 (kernel#162), the SP9 lid GPE.
History: Intel Thread Director patches once broke wake on ADL and were removed (#1120).

## Reports

- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": power-button suspend without cover sometimes incomplete, fan keeps running
- [linux-surface#1164](https://github.com/linux-surface/linux-surface/issues/1164) (open issue, unsolved) "[SP9] Can't turn on tablet when it's suspended": SP9 cannot turn on when suspended
- [linux-surface#1224](https://github.com/linux-surface/linux-surface/issues/1224) (open issue, workaround) "[SP9] Won't wake up from suspend, boot up and restarts are fine.": SP9 won't wake from suspend
- [linux-surface#1910](https://github.com/linux-surface/linux-surface/issues/1910) (open issue, unsolved) "Can't wake from suspend (NixOS, Surface Pro 9)": SP9 wake fails if the lid moves during suspend
- [linux-surface#1811](https://github.com/linux-surface/linux-surface/issues/1811) (open issue, workaround) "(Surface Pro 9) Disable the lid open/close functionality": SP9 disable lid open/close handling
- [linux-surface#1805](https://github.com/linux-surface/linux-surface/issues/1805) (open issue, patch-pending) "After updating I can't wake up suspended device [SL5]": SL5 and SP9 cannot wake after update
- [linux-surface#1684](https://github.com/linux-surface/linux-surface/issues/1684) (closed issue, stale) "(SP9) Cannot wake from sleep": SP9 cannot wake from sleep (closed)
- [linux-surface#1010](https://github.com/linux-surface/linux-surface/issues/1010) (open issue, workaround) "Surface Laptop 5 does not sleep well": SL5 sleep: SOF DSP root cause and dsp_driver=1 fix
- [kbz#216854](https://bugzilla.kernel.org/show_bug.cgi?id=216854) (NEW) "Surface Laptop 5: trouble waking from suspend by opening the lid, ACPI errors": SL5 trouble waking by opening the lid
- [linux-surface/kernel#192](https://github.com/linux-surface/kernel/issues/192) (open issue, needs-info) "Surface Pro 7: s2idle suspend hard freezes since Nov 12, no resume": SP7 s2idle hard freeze since 2026-11-12 (watch for SP9)

## Fixes, patches and PRs

- [linux-surface/kernel#162](https://github.com/linux-surface/kernel/issues/162) (open PR, stalled) "platform/surface: Add s2idle/hibernate fix for Surface Laptop 5": SL5 s2idle fix module (PADCFG0 repair), stalled; qzed prefers userspace
- [linux-surface#1120](https://github.com/linux-surface/linux-surface/issues/1120) (closed issue, fixed-kernel) "Wake from suspend failing on alder/raptor lake": Thread Director patches removed (history)

## Possible solutions

- Test lead 1 on the SP9 with an rtcwake loop and dsp_driver=1; if it holds, report to SOF instead of keeping the parameter.
- Test lead 2 by reading PADCFG0 of pin 213 before and after s2idle (kernel#162 has the method).
- Workaround reported on SL5: logind lid handling off plus pci=hpiosize=0.

## Next steps

- [ ] Run the rtcwake loop with and without dsp_driver=1 on an SP9 (commands in docs/testing.md).

## Commands

```
for i in 1 2 3; do sudo rtcwake -m mem -s 20; sleep 15; done
grep . /sys/power/suspend_stats/*
```

## Upstream and people

- Upstream target: thesofproject/linux, linux-gpio (Intel pinctrl: Andy Shevchenko, Mika Westerberg)
- People: User25665, wowitsjack, dmusican

## Linked issues

- Depends on: none
- Blocks: [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-103](SP9-103-touch-and-pen-stop-working-after-suspend-resume.md) Touch and pen stop working after suspend/resume, [SP9-301](SP9-301-opening-the-cover-does-not-wake-the-sp9-surface-gpe-has-no-s.md) Opening the cover does not wake the SP9 (surface_gpe has no SP9 entry), [SP9-303](SP9-303-acpi-gpe-interrupt-storm-on-lid-close-with-ac-pci-hpiosize-0.md) ACPI GPE interrupt storm on lid close with AC (pci=hpiosize=0 trade-off), [SP9-304](SP9-304-s2idle-hangs-for-minutes-entering-suspend-on-btrfs-pm-fs-syn.md) s2idle hangs for minutes entering suspend on btrfs (pm_fs_sync), [SP9-311](SP9-311-fan-keeps-running-during-suspend.md) Fan keeps running during suspend

## Knowledge base

- [status.yaml](../status.yaml)
- [docs/research/open-issues.md](../docs/research/open-issues.md)
- [docs/testing.md](../docs/testing.md)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
