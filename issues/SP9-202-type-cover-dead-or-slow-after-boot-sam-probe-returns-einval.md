---
id: SP9-202
title: 'Type Cover dead or slow after boot: SAM probe returns -EINVAL before the pin controller is ready'
labels:
- area:cover
- kind:bug
- priority:P1
- status:fix-pending
depends_on: []
blocks:
- SP9-903
related:
- SP9-201
- SP9-203
- SP9-204
- SP9-307
upstream:
- platform-driver-x86 (Hans de Goede, Ilpo Jarvinen)
- Fedora kernel-ark
source: issues/src/2-cover-input.yaml
---

# SP9-202: Type Cover dead or slow after boot: SAM probe returns -EINVAL before the pin controller is ready

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P1 | cover | bug | partial | works | partial |

## Problem

Sometimes the cover keyboard and touchpad do not work after boot (or only after reattaching or a
suspend cycle). Discussion 2282 reports the cover taking a moment to start after attaching.

## Origin

When surface_aggregator probes before pinctrl_tigerlake has bound the wakeup GPIO, ssam_irq_setup()
returns -EINVAL instead of -EPROBE_DEFER, so the probe is never retried. Wu Enqiang's v2 fix is accepted
in platform-driver-x86 and should reach 7.5 and stable.

## Reports

- [linux-surface#2219](https://github.com/linux-surface/linux-surface/issues/2219) (open issue, patch-pending) "surface_serial_hub: probe fails with -EINVAL instead of -EPROBE_DEFER when the wakeup GPIO is not ready": surface_serial_hub -EINVAL instead of -EPROBE_DEFER (confirmed on SP9)
- [linux-surface#1645](https://github.com/linux-surface/linux-surface/issues/1645) (closed issue, config) "[SP9[NixOS] Keyboard&Trackpad not working after upgrade to 6.12.4": SP9 NixOS keyboard dead after 6.12.4 until pinctrl_tigerlake loaded first
- [linux-surface#1651](https://github.com/linux-surface/linux-surface/issues/1651) (open issue, needs-info) "Keyboard and touchpad are unresponsive sometime on boot and after session": SP9 keyboard and touchpad sometimes dead at boot or after resume
- [linux-surface#2064](https://github.com/linux-surface/linux-surface/issues/2064) (open issue, unsolved) "Keyboard not always available after boot": keyboard not always available after boot
- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": cover takes a moment after attaching

## Fixes, patches and PRs

- [lore:20261024054921.48209-1-janussss@163.com](https://lore.kernel.org/r/20261024054921.48209-1-janussss@163.com) (platform-driver-x86, changes-requested/accepted, Wu Enqiang, 2026-10-24) "[v2] surface: aggregator: propagate -EPROBE_DEFER from ssam_irq_setup()": Wu Enqiang v2, accepted in platform-driver-x86
- [linux-surface/kernel#182](https://github.com/linux-surface/kernel/issues/182) (closed PR, superseded-upstream) "platform/surface: aggregator: Defer probe while the wakeup GPIO is unavailable": CmdrShepardsPie's variant, closed in favour of v2
- [lore:20240505130800.2546640-2-weifeng.liu.z@gmail.com](https://lore.kernel.org/r/20240505130800.2546640-2-weifeng.liu.z@gmail.com) (platform-driver-x86, superseded/accepted, Weifeng Liu, 2024-05-05) "Defer probing of SAM if serdev device is not ready": earlier defer-probe series (2024)

## Possible solutions

- Until the fix is in Fedora's kernel: load pinctrl_tigerlake early (dracut force_drivers).

## Next steps

- [ ] Check when the accepted patch reaches Fedora's kernel; ask for a kernel-ark backport if it misses 7.4.

## Commands

```
printf '%s\n' 'force_drivers+=" pinctrl_tigerlake "' | sudo tee /etc/dracut.conf.d/surface-pinctrl.conf
sudo dracut -f --regenerate-all
```

## Upstream and people

- Upstream target: platform-driver-x86 (Hans de Goede, Ilpo Jarvinen), Fedora kernel-ark
- People: Wu Enqiang, CmdrShepardsPie

## Linked issues

- Depends on: none
- Blocks: [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-201](SP9-201-type-cover-does-not-work-at-the-luks-passphrase-prompt-dracu.md) Type Cover does not work at the LUKS passphrase prompt (dracut lacks surface_aggregator_hub), [SP9-203](SP9-203-boot-stalls-about-2-minutes-surface-hid-probes-the-pen-stash.md) Boot stalls about 2 minutes: surface_hid probes the pen stash node and fails with -EPROTO, [SP9-204](SP9-204-keyboard-backlight-cannot-be-controlled-from-the-desktop.md) Keyboard backlight cannot be controlled from the desktop, [SP9-307](SP9-307-type-cover-dead-after-resume-from-hibernation-sam-event-enab.md) Type Cover dead after resume from hibernation (SAM event enable times out)

## Knowledge base

- [status.yaml](../status.yaml)
- [data/indexes/upstream-submissions.tsv](../data/indexes/upstream-submissions.tsv)

_Generated from `issues/src/2-cover-input.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
