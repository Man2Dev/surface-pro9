---
id: SP9-305
title: Shutdown does not power off on mainline (S5 quirk never posted upstream)
labels:
- area:power
- kind:upstreaming
- priority:P2
- status:open
depends_on:
- SP9-901
blocks:
- SP9-903
related:
- SP9-303
- SP9-901
upstream:
- linux-pci (Bjorn Helgaas)
- x86
source: issues/src/3-power.yaml
---

# SP9-305: Shutdown does not power off on mainline (S5 quirk never posted upstream)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P2 | power | upstreaming | broken | works | broken |

## Problem

On a stock kernel `poweroff` leaves the SP9 on and warm. linux-surface fixes it with a DMI-gated PCI quirk.

## Origin

EFI ResetSystem(EFI_RESET_SHUTDOWN) returns unless the Thunderbolt 4 and GPU PCI shutdown methods are
skipped. linux-surface 0011 ("PCI: Add quirk to prevent calling shutdown method", SP9 + SL5) was never sent
to linux-pci (patchwork search). Some users also need pci=hpiosize=0.

## Reports

- [linux-surface#1058](https://github.com/linux-surface/linux-surface/issues/1058) (open issue, workaround) "SL5/SP9 does not power off properly": SL5/SP9 does not power off properly
- [linux-surface/surface-shutdown#1](https://github.com/linux-surface/surface-shutdown/issues/1) (closed issue, fixed-kernel) "Surface Pro 9 still gets stuck on shutdown": SP9 still gets stuck on shutdown (fixed downstream)
- [linux-surface#1113](https://github.com/linux-surface/linux-surface/issues/1113) (open issue, workaround) "[SP9] Kenel panic prevents shutdown": SP9 kernel panic prevents shutdown (old)
- [linux-surface#1698](https://github.com/linux-surface/linux-surface/issues/1698) (open issue, unsolved) "Surface Laptop 6 Shutdown Issue in Ubuntu": SL6 and SP9 F41 shutdown leaves device on
- [linux-surface#1664](https://github.com/linux-surface/linux-surface/issues/1664) (open issue, workaround) "[SP10] Shutdown Doesn't Work": SP10 shutdown: pci=hpiosize=0
- [linux-surface#1864](https://github.com/linux-surface/linux-surface/issues/1864) (open issue, workaround) "[SL6] Surface Laptop 6 does not fully power off, hangs in S0ix after shutdown": SL6/SP11 power off: kernel parameter set

## Fixes, patches and PRs

- [data/indexes/patches-linux-surface-7.3.md](../data/indexes/patches-linux-surface-7.3.md): 0011-surface-shutdown, upstream class rework

## Possible solutions

- Write up the root cause and propose the DMI-gated quirk (or an x86 reboot quirk) on linux-pci; ask Bjorn Helgaas what shape is acceptable.

## Next steps

- [ ] Confirm on an SP9 with the stock Fedora kernel that poweroff fails (phase 0).

## Upstream and people

- Upstream target: linux-pci (Bjorn Helgaas), x86
- People: qzed, CheeseFM

## Linked issues

- Depends on: [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)
- Blocks: [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-303](SP9-303-acpi-gpe-interrupt-storm-on-lid-close-with-ac-pci-hpiosize-0.md) ACPI GPE interrupt storm on lid close with AC (pci=hpiosize=0 trade-off), [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
