---
id: SP9-104
title: ITHC fails to initialise on some boots or units (EFI stub DMA error, legacy init -110)
labels:
- area:touch
- kind:bug
- priority:P2
- status:needs-test
depends_on:
- SP9-101
blocks: []
related:
- SP9-101
- SP9-103
- SP9-601
upstream:
- quo/ithc-linux
source: issues/src/1-touch-pen.yaml
---

# SP9-104: ITHC fails to initialise on some boots or units (EFI stub DMA error, legacy init -110)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| needs-test | P2 | touch | bug | n/a | partial | n/a |

## Problem

Two failure modes are reported on the SP9: with the kernel booted as an EFI stub, ITHC reports
"invalid dma rx data" and touch never starts; on one unit `ithc_legacy_init` times out with -110 on every
boot and touch has never worked. A third report: touch locks up while the magnetic charger is attached.

## Origin

EFI stub: quo found bit 5 of THC register 0x1128 set only on working boots and committed 18afc6f
(2024-04, "hopefully fixed"). Legacy init -110 (UEFI 22.107.143, 7.2.15): unknown, no maintainer reply.
Charger lock-up: unknown.

## Reports

- [linux-surface#1078](https://github.com/linux-surface/linux-surface/issues/1078) (open issue, could-close) "[SP9] Touchscreen not working with efi stub kernel": SP9 touch dead when booted as EFI stub (still open)
- [quo/ithc-linux#26](https://github.com/quo/ithc-linux/issues/26) (closed) "Driver fails to initialize when booting with EFISTUB (invalid dma rx data)": same bug on SP9, quo's register analysis, closed after 18afc6f
- [linux-surface#2367](https://github.com/linux-surface/linux-surface/issues/2367) (open issue, unsolved) "Surface Pro 9 (Intel): touchscreen and pen dead, ithc_legacy_init failed": SP9 ithc_legacy_init failed with -110 on every boot
- [linux-surface#1470](https://github.com/linux-surface/linux-surface/issues/1470) (open issue, unsolved) "Touchscreen locks up if Surface charger is attached": touchscreen locks up while the magnetic charger is attached

## Fixes, patches and PRs

- [quo/ithc-linux@18afc6f](https://github.com/quo/ithc-linux/commit/18afc6f): likely fix for the EFI stub case

## Possible solutions

- Retest EFI stub / UKI boot on the SP9 with current ITHC before Fedora moves to UKIs; close #1078 if it works.

## Next steps

- [ ] Boot an SP9 once through a UKI or efibootmgr EFI stub entry and check `dmesg | grep ithc`.

## Upstream and people

- Upstream target: quo/ithc-linux
- People: quo

## Linked issues

- Depends on: [SP9-101](SP9-101-touchscreen-and-pen-need-the-out-of-tree-ithc-driver-no-upst.md) Touchscreen and pen need the out-of-tree ITHC driver (no upstream driver for the ADL THC in legacy mode)
- Blocks: none
- Related: [SP9-101](SP9-101-touchscreen-and-pen-need-the-out-of-tree-ithc-driver-no-upst.md) Touchscreen and pen need the out-of-tree ITHC driver (no upstream driver for the ADL THC in legacy mode), [SP9-103](SP9-103-touch-and-pen-stop-working-after-suspend-resume.md) Touch and pen stop working after suspend/resume, [SP9-601](SP9-601-installing-and-booting-fedora-on-the-sp9-with-secure-boot-nx.md) Installing and booting Fedora on the SP9 with Secure Boot (NX firmware, MOK, boot entries)

## Knowledge base

- [docs/research/upstream-efforts.md](../docs/research/upstream-efforts.md)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
