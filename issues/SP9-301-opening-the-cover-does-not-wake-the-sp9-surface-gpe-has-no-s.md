---
id: SP9-301
title: Opening the cover does not wake the SP9 (surface_gpe has no SP9 entry)
labels:
- area:lid
- kind:upstreaming
- priority:P1
- status:open
depends_on: []
blocks:
- SP9-903
related:
- SP9-302
- SP9-303
- SP9-901
upstream:
- platform-driver-x86 (Hans de Goede, Ilpo Jarvinen, Maximilian Luz)
source: issues/src/3-power.yaml
---

# SP9-301: Opening the cover does not wake the SP9 (surface_gpe has no SP9 entry)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P1 | lid | upstreaming | broken | partial | broken |

## Problem

Closing the cover suspends, but opening it does not wake the device; the power button is needed.

## Origin

The lid wake GPE (0x52) has to be armed by surface_gpe, which has entries for the SL3, SLS, SP8 and SL4
upstream but none for the SP9 or SL5. Maximilian Luz wrote the SP9 entry (linux-surface 0012) but never
posted it. The downstream entry matches DMI SKU Surface_Pro_9_2038 only, misses the Business SKU
(Surface_Pro_9_for_Business_2038), and some units report sys_vendor with a leading space, which
DMI_EXACT_MATCH rejects.

## Reports

- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": opening the cover does not wake the device
- [linux-surface#2257](https://github.com/linux-surface/linux-surface/issues/2257) (open issue, patch-pending) "surface_gpe: SP9 lid-open wake broken, DMI sys_vendor has leading space": DMI sys_vendor has a leading space on some SP9 units
- [linux-surface#1919](https://github.com/linux-surface/linux-surface/issues/1919) (open issue, patch-pending) "surface_gpe: no compatible Microsoft Surface device found on Surface Pro 9": surface_gpe finds no compatible device on SP9
- [linux-surface#1183](https://github.com/linux-surface/linux-surface/issues/1183) (open issue, workaround) "[Surface Pro 9] Cannot wake from suspend if type cover was closed.": SP9 cannot wake after closing the cover
- [linux-surface#1224](https://github.com/linux-surface/linux-surface/issues/1224) (open issue, workaround) "[SP9] Won't wake up from suspend, boot up and restarts are fine.": SP9 does not wake from suspend
- [linux-surface#1910](https://github.com/linux-surface/linux-surface/issues/1910) (open issue, unsolved) "Can't wake from suspend (NixOS, Surface Pro 9)": SP9 NixOS cannot wake
- [linux-surface/surface-gpe#3](https://github.com/linux-surface/surface-gpe/issues/3) (open issue, patch-pending) "Surface Pro 9 Business: Suspend/wake up with lid does not work properly": SP9 Business lid wake
- [kbz#218923](https://bugzilla.kernel.org/show_bug.cgi?id=218923) (NEW) "ACPI error storm and resume failure when handling lid close: Surface Pro 9 Alder Lake": ACPI error storm and resume failure on lid close (SP9)

## Fixes, patches and PRs

- [linux-surface#2011](https://github.com/linux-surface/linux-surface/issues/2011) (open PR, moved) "Add Surface Laptop 5 lid GPE + s2idle/hibernate fix (v5.4)": contains Maximilian Luz's 'gpe: Add support for Surface Pro 9 and Surface Laptop 5' (moved to kernel#162)
- [linux-surface/surface-gpe#7](https://github.com/linux-surface/surface-gpe/issues/7) (open PR, waiting) "platform/surface: gpe: Fix DMI vendor string match for Surface Pro 9": tolerate the vendor string
- [linux-surface/surface-gpe#5](https://github.com/linux-surface/surface-gpe/issues/5) (open PR, waiting) "Add support for Surface Pro 9 Business (Intel).": add the Business SKU
- [gist:dragged9698/3d520d6da566825e9880a7e8e0c7abfc](https://gist.github.com/dragged9698/3d520d6da566825e9880a7e8e0c7abfc): DMI_MATCH vendor patch, verified on SP9 2038
- [Meatwo310/dotnix#13](https://github.com/Meatwo310/dotnix/issues/13) (closed) "fix(sp9-v7): support suspend on Surface Pro 9 Business": Business SKU string, lid suspend and resume verified
- [lore:20220429180049.1282447-1-luzmaximilian@gmail.com](https://lore.kernel.org/r/20220429180049.1282447-1-luzmaximilian@gmail.com) (platform-driver-x86, accepted, Maximilian Luz, 2022-04-29) "platform/surface: gpe: Add support for Surface Pro 8": precedent: gpe support for Surface Pro 8 (accepted 2022)

## Possible solutions

- One upstream surface_gpe patch: SP9 (all SKUs, tolerant vendor match) plus SL5, GPE 0x52, Maximilian Luz as author if he agrees; rebase on Bartosz Golaszewski's 2026 platform_device conversion.

## Next steps

- [ ] Read DMI strings on an SP9, ask qzed about authorship, build and test, send to platform-driver-x86.

## Commands

```
sudo dmidecode -s system-sku-number
sudo dmidecode -s system-manufacturer | od -c | head -2
grep . /sys/firmware/acpi/interrupts/gpe52
```

## Upstream and people

- Upstream target: platform-driver-x86 (Hans de Goede, Ilpo Jarvinen, Maximilian Luz)
- People: qzed, dragged9698, 777HOST, Lucrtz, Meatwo310

## Linked issues

- Depends on: none
- Blocks: [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-302](SP9-302-sp9-sometimes-does-not-wake-from-s2idle-or-hangs-on-the-seco.md) SP9 sometimes does not wake from s2idle (or hangs on the second suspend), [SP9-303](SP9-303-acpi-gpe-interrupt-storm-on-lid-close-with-ac-pci-hpiosize-0.md) ACPI GPE interrupt storm on lid close with AC (pci=hpiosize=0 trade-off), [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)

## Knowledge base

- [status.yaml](../status.yaml)
- [docs/research/upstream-efforts.md](../docs/research/upstream-efforts.md)
- [data/indexes/external-repos.yaml](../data/indexes/external-repos.yaml)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
