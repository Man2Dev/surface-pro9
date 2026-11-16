---
id: SP9-101
title: Touchscreen and pen need the out-of-tree ITHC driver (no upstream driver for the ADL THC in legacy mode)
labels:
- area:touch
- kind:missing-driver
- priority:P1
- status:open
depends_on: []
blocks:
- SP9-103
- SP9-104
- SP9-903
related:
- SP9-102
- SP9-103
- SP9-104
- SP9-111
- SP9-112
upstream:
- linux-input (Jiri Kosina, Benjamin Tissoires)
- Intel THC maintainers (Even Xu, Xinpeng Sun)
source: issues/src/1-touch-pen.yaml
---

# SP9-101: Touchscreen and pen need the out-of-tree ITHC driver (no upstream driver for the ADL THC in legacy mode)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P1 | touch | missing-driver | broken | works | broken |

## Problem

On a stock kernel the SP9 touchscreen and Slim Pen 2 do not work at all. The touch controller is the
Alder Lake-P Touch Host Controller (PCI 8086:51d0), which only the downstream `ithc` driver
(linux-surface 0006, quo/ithc-linux) drives. With ITHC but without iptsd, touch is single-touch only.

## Origin

Intel never upstreamed THC support for Alder Lake. Intel's `intel-thc-hid` (QuickSPI/QuickI2C, mainline
since 6.14, Even Xu) only claims Meteor Lake and newer. The SP9 runs its THC in legacy mode
("no ACPI config, using legacy mode", seen in #2367), which `intel-thc-hid` does not implement. quo,
who wrote ITHC, will not submit it under a pseudonym (quo/ithc-linux#7), and nobody else has posted it.
No IPTS or ITHC patch has ever reached linux-input (patchwork search, 2026-11-14).

## Reports

- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": single touch without iptsd
- [linux-surface#1330](https://github.com/linux-surface/linux-surface/issues/1330) (closed issue, user-setup) "surface pro 9 touchscreen and pen not working": SP9 touch and pen dead: iptsd missing
- [linux-surface#1848](https://github.com/linux-surface/linux-surface/issues/1848) (closed issue, user-setup) "surface pro 9 - pen not working, no /dev/ipts/ directory": SP9 pen dead: no /dev/ipts (UAPI moved to hidraw)
- [linux-surface#1156](https://github.com/linux-surface/linux-surface/issues/1156) (closed issue, user-setup) "Pen from Surface pro 9 under Fedora 38 install?": Fedora 38 SP9 pen needs linux-surface kernel plus iptsd
- [linux-surface#818](https://github.com/linux-surface/linux-surface/issues/818) (open issue, sibling) "SP8 touchscreen and pen support": SP8 touch and pen support history
- [quo/ithc-linux#34](https://github.com/quo/ithc-linux/issues/34) (open) "No touch input on Surface Laptop 5 (Alder Lake, 8086:51d0): device created but zero events, even with poll=1": SL5 (same 8086:51d0) gets zero events on Fedora 44
- [intel/thc-drivers#1](https://github.com/intel/thc-drivers/issues/1) (open) "Multi-touch not working on Surface Laptop 7 with Intel THC driver": Intel's out-of-tree THC drivers, Surface report unanswered

## Fixes, patches and PRs

- [quo/ithc-linux#7](https://github.com/quo/ithc-linux/issues/7) (open) "Rolling into the kernel?": upstreaming tracker, open since 2022
- [quo/ithc-linux#29](https://github.com/quo/ithc-linux/issues/29) (open) "Official Intel QuickSPI Linux driver": Intel QuickSPI driver: ADL QuickSPI easy, legacy mode needs ithc-legacy.c merged
- [quo/ithc-linux#33](https://github.com/quo/ithc-linux/issues/33) (open) "Improve error recovery, locking, and shutdown behavior (PR)": PR: error recovery and locking; quo's review sets the bar for an upstream version
- [linux-surface/kernel#132](https://github.com/linux-surface/kernel/issues/132) (closed PR, superseded-pr) "HID based IPTS and ITHC support": HID based IPTS and ITHC support in linux-surface (downstream, 2022)
- [patchwork.kernel.org/project/linux-input/list/?series=909501](https://patchwork.kernel.org/project/linux-input/list/?series=909501): Intel THC drivers v2 (Even Xu), mainline 6.14, MTL and newer only

## Possible solutions

- Short term on stock Fedora: build quo/ithc-linux out of tree and sign it with a MOK, as John-S-Reddick/bazzite-surface does; package it as an akmod/kmod (RPM Fusion or Terra) until it is upstream.
- Long term option A: someone carries ITHC to linux-input as a HID transport driver after the cleanup quo listed (kernel style, error handling, full re-init on error).
- Long term option B: merge ITHC's legacy mode into Intel's intel-thc-hid and add the ADL PCI IDs; ask Even Xu and Xinpeng Sun (Intel) whether they would take it.

## Next steps

- [ ] Ask quo whether he would accept someone else submitting ITHC or the legacy-mode merge with his authorship (quo/ithc-linux#7).
- [ ] Ask Intel (Even Xu) on linux-input whether legacy-mode THC (ADL, TGL) is welcome in intel-thc-hid.

## Upstream and people

- Upstream target: linux-input (Jiri Kosina, Benjamin Tissoires), Intel THC maintainers (Even Xu, Xinpeng Sun)
- People: quo, StollD, Even Xu

## Linked issues

- Depends on: none
- Blocks: [SP9-103](SP9-103-touch-and-pen-stop-working-after-suspend-resume.md), [SP9-104](SP9-104-ithc-fails-to-initialise-on-some-boots-or-units-efi-stub-dma.md), [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-102](SP9-102-iptsd-is-not-packaged-in-fedora.md) iptsd is not packaged in Fedora, [SP9-103](SP9-103-touch-and-pen-stop-working-after-suspend-resume.md) Touch and pen stop working after suspend/resume, [SP9-104](SP9-104-ithc-fails-to-initialise-on-some-boots-or-units-efi-stub-dma.md) ITHC fails to initialise on some boots or units (EFI stub DMA error, legacy init -110), [SP9-111](SP9-111-libwacom-has-no-sp9-tablet-description-pen-and-touch-not-rec.md) libwacom has no SP9 tablet description (pen and touch not recognised as a tablet), [SP9-112](SP9-112-package-ithc-as-a-signed-out-of-tree-module-akmod-kmod-for-t.md) Package ITHC as a signed out-of-tree module (akmod/kmod) for the stock Fedora kernel

## Knowledge base

- [status.yaml](../status.yaml)
- [docs/subsystems/touch-pen.md](../docs/subsystems/touch-pen.md)
- [docs/research/upstream-efforts.md](../docs/research/upstream-efforts.md)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
