---
id: SP9-303
title: ACPI GPE interrupt storm on lid close with AC (pci=hpiosize=0 trade-off)
labels:
- area:suspend
- kind:bug
- priority:P2
- status:open
depends_on: []
blocks: []
related:
- SP9-301
- SP9-302
- SP9-305
upstream:
- linux-pci
- linux-acpi
source: issues/src/3-power.yaml
---

# SP9-303: ACPI GPE interrupt storm on lid close with AC (pci=hpiosize=0 trade-off)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P2 | suspend | bug | partial | partial | partial |

## Problem

Closing the cover while on AC (also Thunderbolt hotplug, lid resume) floods dmesg with ACPI errors and
can break later suspends. The wiki workaround pci=hpiosize=0 stops it, but an SP9 user reports that it
then also stops lid wake.

## Origin

Unknown; hpiosize=0 changes the PCI hotplug I/O window. Same family as kbz#218923.

## Reports

- [linux-surface#1082](https://github.com/linux-surface/linux-surface/issues/1082) (closed issue, workaround) "[SP9] ACPI error spam in dmesg after closing the type cover with the device plugged in": SP9 ACPI error spam after closing the cover on AC; trade-off reported 2025-10
- [linux-surface#1446](https://github.com/linux-surface/linux-surface/issues/1446) (closed issue, workaround) "Surface pro 9 ACPI errors during sleep": SP9 ACPI errors during sleep (TLP plus surface_gpe blacklist)
- [kbz#218923](https://bugzilla.kernel.org/show_bug.cgi?id=218923) (NEW) "ACPI error storm and resume failure when handling lid close: Surface Pro 9 Alder Lake": ACPI error storm and resume failure (SP9)

## Fixes, patches and PRs

- none yet

## Possible solutions

- Find what the I/O window change fixes (ACPI tables, hotplug bridge resources) and file it on bugzilla.kernel.org / linux-pci.
- Test lid wake with and without hpiosize=0 once SP9-301 is fixed.

## Next steps

- [ ] Capture /sys/firmware/acpi/interrupts and dmesg on lid close with AC, with and without hpiosize=0.

## Upstream and people

- Upstream target: linux-pci, linux-acpi
- People: petm5, gtxg16

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-301](SP9-301-opening-the-cover-does-not-wake-the-sp9-surface-gpe-has-no-s.md) Opening the cover does not wake the SP9 (surface_gpe has no SP9 entry), [SP9-302](SP9-302-sp9-sometimes-does-not-wake-from-s2idle-or-hangs-on-the-seco.md) SP9 sometimes does not wake from s2idle (or hangs on the second suspend), [SP9-305](SP9-305-shutdown-does-not-power-off-on-mainline-s5-quirk-never-poste.md) Shutdown does not power off on mainline (S5 quirk never posted upstream)

## Knowledge base

- [status.yaml](../status.yaml)
- [docs/research/wiki-digest.md](../docs/research/wiki-digest.md)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
