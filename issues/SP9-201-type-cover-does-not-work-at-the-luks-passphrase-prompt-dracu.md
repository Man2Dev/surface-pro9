---
id: SP9-201
title: Type Cover does not work at the LUKS passphrase prompt (dracut lacks surface_aggregator_hub)
labels:
- area:cover
- kind:upstreaming
- priority:P1
- status:open
depends_on: []
blocks:
- SP9-903
related:
- SP9-202
- SP9-601
- SP9-901
- SP9-904
upstream:
- dracut-ng/dracut
source: issues/src/2-cover-input.yaml
---

# SP9-201: Type Cover does not work at the LUKS passphrase prompt (dracut lacks surface_aggregator_hub)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P1 | cover | upstreaming | works | works | broken |

## Problem

With an encrypted root, the Type Cover keyboard is dead at the LUKS prompt on Fedora, so the disk cannot
be unlocked without a USB keyboard.

## Origin

The cover keyboard and touchpad are children of the SAM KIP hub, bound by `surface_aggregator_hub`.
dracut master already installs `=drivers/hid` (surface_hid, surface_hid_core), `=drivers/tty/serial`
(8250_dw, 8250_lpss), `=drivers/pinctrl`, `intel_lpss_pci` and `surface_aggregator_registry` in the default
(sloppy) hostonly mode, but not `surface_aggregator_hub` (read 2026-11-14, dracut 04e04cfe). A second cause,
the SAM probe race, is SP9-202.

## Reports

- [linux-surface#1221](https://github.com/linux-surface/linux-surface/issues/1221) (open issue, patch-pending) "[SP9] Start Fedora 38 LUKS with Surface Pro Signature Keyboard [SOLVED]": SP9 Fedora 38 LUKS with Signature Keyboard (solved with modules)
- [linux-surface#1126](https://github.com/linux-surface/linux-surface/issues/1126) (open issue, could-close) "Keyboard not detected in initramfs on Debian.": SP9 Debian keyboard not in initramfs
- [linux-surface#1491](https://github.com/linux-surface/linux-surface/issues/1491) (closed issue, config) "[SurfacePro9][NixOS] Keyboard doesn't work for unlock of encrypted drive at boot": SP9 NixOS LUKS module list
- [linux-surface#1709](https://github.com/linux-surface/linux-surface/issues/1709) (closed issue, stale) "Trying to get my keybord working on Fedora 41 with disk encryption": Fedora 41 LUKS keyboard (unanswered)
- [linux-surface#2039](https://github.com/linux-surface/linux-surface/issues/2039) (closed issue, workaround) "SP8: Type Cover not working at LUKS prompt + post-boot fix (Fedora, surface_serial_hub IRQ bug)": SP8 Fedora: cover dead at LUKS (surface_serial_hub IRQ bug), Clevis plus TPM2 fallback
- [linux-surface#911](https://github.com/linux-surface/linux-surface/issues/911) (closed issue, config) "[SP8] Keyboard does not work on LUKS password entry": SP8 LUKS module list
- [linux-surface#1350](https://github.com/linux-surface/linux-surface/issues/1350) (closed issue, config) "SP8 Type Cover not detected during disk encryption": SP8 Silverblue LUKS
- [rhbz#1322128](https://bugzilla.redhat.com/show_bug.cgi?id=1322128) (CLOSED/WORKSFORME) "Surface Pro 3/4 Type Cover does not work at the LUKS prompt": SP3/4 Type Cover at LUKS (old)
- [omacom/omarchy#14195](https://github.com/omacom/omarchy/issues/14195) (open) "Fix AMD Surface keyboard support at the LUKS prompt": Omarchy LUKS keyboard module list

## Fixes, patches and PRs

- [dracut-ng/dracut@8cc89664](https://github.com/dracut-ng/dracut/commit/8cc89664): precedent: add surface_aggregator_registry for Surface Laptop 4 (Benjamin Drung, 2023)
- [ublue-os/surface#29](https://github.com/ublue-os/surface/issues/29) (closed) "fix: add initramfs modules": Universal Blue initramfs module list
- [Madmaxx636/surface-companion](https://github.com/Madmaxx636/surface-companion): app fix with the same module list, surface_aggregator_hub included (disc#2282, 2026-11-16)

## Possible solutions

- One-line dracut PR: add surface_aggregator_hub next to surface_aggregator_registry in 70kernel-modules, citing 8cc89664.
- Local workaround now: add_drivers+=" surface_aggregator_hub " in /etc/dracut.conf.d and regenerate.
- Tablet without cover: unl0kr on-screen keyboard (#1857).

## Next steps

- [ ] Check what Fedora's initramfs contains on an SP9, then open the dracut PR.

## Commands

```
lsinitrd | grep -E 'surface|8250|pinctrl|lpss'
printf '%s\n' 'add_drivers+=" surface_aggregator_hub "' | sudo tee /etc/dracut.conf.d/surface-hub.conf
sudo dracut -f --regenerate-all
```

## Upstream and people

- Upstream target: dracut-ng/dracut
- People: Benjamin Drung

## Linked issues

- Depends on: none
- Blocks: [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-202](SP9-202-type-cover-dead-or-slow-after-boot-sam-probe-returns-einval.md) Type Cover dead or slow after boot: SAM probe returns -EINVAL before the pin controller is ready, [SP9-601](SP9-601-installing-and-booting-fedora-on-the-sp9-with-secure-boot-nx.md) Installing and booting Fedora on the SP9 with Secure Boot (NX firmware, MOK, boot entries), [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check), [SP9-904](SP9-904-fix-out-of-date-linux-surface-wiki-pages-for-the-sp9.md) Fix out-of-date linux-surface wiki pages for the SP9

## Knowledge base

- [docs/subsystems/boot-initramfs-fedora.md](../docs/subsystems/boot-initramfs-fedora.md)
- [docs/research/upstream-efforts.md](../docs/research/upstream-efforts.md)

_Generated from `issues/src/2-cover-input.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
