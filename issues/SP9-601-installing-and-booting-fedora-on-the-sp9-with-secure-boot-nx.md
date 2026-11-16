---
id: SP9-601
title: Installing and booting Fedora on the SP9 with Secure Boot (NX firmware, MOK, boot entries)
labels:
- area:boot
- kind:needs-test
- priority:P1
- status:needs-test
depends_on: []
blocks:
- SP9-903
related:
- SP9-104
- SP9-201
- SP9-901
upstream:
- Fedora (shim, grub2)
source: issues/src/6-boot-packaging.yaml
---

# SP9-601: Installing and booting Fedora on the SP9 with Secure Boot (NX firmware, MOK, boot entries)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| needs-test | P1 | boot | needs-test | works | partial | unknown |

## Problem

Past SP9 reports: Fedora froze at the Microsoft logo after the June 2023 firmware (NX enforcement) or after
MOK enrolment; Fedora 41 ISO hung (IPU6 in 6.11); Secured-core made GRUB reset once; after a Fedora 45
dual-boot install only the Windows Boot Manager shows; MokManager does not start.

## Origin

NX: the firmware stopped allocating RWX memory; old shim/GRUB/MokManager broke (linux-surface 0001 reverts
the kernel NX_COMPAT flag). IPU6 hang fixed upstream (Gruszka, 6.13). Boot entry: Windows boot order and the
UEFI "boot configuration lock".

## Reports

- [linux-surface#1162](https://github.com/linux-surface/linux-surface/issues/1162) (open issue, workaround) "Fedora fails to boot after firmware update, freezes on Microsoft logo": Fedora freezes on Microsoft logo after firmware update (NX)
- [linux-surface#1274](https://github.com/linux-surface/linux-surface/issues/1274) (open issue, workaround) "Enrolling secureboot keys makes the device freeze on the Microsoft logo after firmware update": enrolling Secure Boot keys freezes on Microsoft logo
- [linux-surface#1453](https://github.com/linux-surface/linux-surface/issues/1453) (open issue, unsolved) "[SP9] Mokmanager does not start": SP9 MokManager does not start
- [linux-surface#1690](https://github.com/linux-surface/linux-surface/issues/1690) (open issue, could-close) "Can't boot Fedora 41 iso on SP9": Fedora 41 ISO hangs on SP9 (IPU6)
- [linux-surface#2361](https://github.com/linux-surface/linux-surface/issues/2361) (open issue, needs-info) "Fedora installation on Surface pro 9": Fedora 45 dual boot: only Windows Boot Manager after install
- [linux-surface#1070](https://github.com/linux-surface/linux-surface/issues/1070) (open issue, workaround) "Grub reboots the first time with Secured Core enabled": GRUB resets once with Secured-core on
- [linux-surface#1742](https://github.com/linux-surface/linux-surface/issues/1742) (open issue, workaround) "Surface Pro 9: cannot boot properly when secure boot is enabled": SP9 bad shim signature
- [linux-surface#1516](https://github.com/linux-surface/linux-surface/issues/1516) (open issue, could-close) "[Kernel 6.10]: Page fault in IPU6": 6.10 IPU6 page fault (fixed by Gruszka's patch)
- [NixOS/nixos-hardware#1121](https://github.com/NixOS/nixos-hardware/issues/1121) (closed) "Surface Pro 9 won't boot after a seemingly successful installation": SP9 won't boot after installation
- [discussion.fedoraproject.org/t/155740](https://discussion.fedoraproject.org/t/155740): install Fedora on a keyboardless Surface

## Fixes, patches and PRs

- [lore:20241031102321.409454-1-stanislaw.gruszka@linux.intel.com](https://lore.kernel.org/r/20241031102321.409454-1-stanislaw.gruszka@linux.intel.com): IPU6 page fault fix (in 6.13+)
- [gist:philbudden/59b47727fce722a469b0ca87e668c22e](https://gist.github.com/philbudden/59b47727fce722a469b0ca87e668c22e): firmware downgrade notes, NX explanation

## Possible solutions

- Test the current Fedora 45 ISO with Secure Boot on and current firmware; record whether stock shim/GRUB boot without 0001.
- Turn off 'Enable boot configuration lock' in UEFI before installing; check efibootmgr order after install.

## Next steps

- [ ] Part of phase 0 (SP9-901).

## Commands

```
efibootmgr -v
mokutil --sb-state
```

## Upstream and people

- Upstream target: Fedora (shim, grub2)
- People: StollD

## Linked issues

- Depends on: none
- Blocks: [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-104](SP9-104-ithc-fails-to-initialise-on-some-boots-or-units-efi-stub-dma.md) ITHC fails to initialise on some boots or units (EFI stub DMA error, legacy init -110), [SP9-201](SP9-201-type-cover-does-not-work-at-the-luks-passphrase-prompt-dracu.md) Type Cover does not work at the LUKS passphrase prompt (dracut lacks surface_aggregator_hub), [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)

## Knowledge base

- [status.yaml](../status.yaml)
- [docs/subsystems/boot-initramfs-fedora.md](../docs/subsystems/boot-initramfs-fedora.md)

_Generated from `issues/src/6-boot-packaging.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
