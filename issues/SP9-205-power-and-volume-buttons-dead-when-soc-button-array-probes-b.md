---
id: SP9-205
title: Power and volume buttons dead when soc_button_array probes before the pin controller
labels:
- area:buttons
- kind:bug
- priority:P3
- status:fixed-upstream
depends_on: []
blocks: []
related:
- SP9-901
- SP9-902
- SP9-904
upstream:
- linux-input
source: issues/src/2-cover-input.yaml
---

# SP9-205: Power and volume buttons dead when soc_button_array probes before the pin controller

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fixed-upstream | P3 | buttons | bug | works | works | works |

## Problem

Power and volume buttons silently did nothing when soc_button_array loaded before pinctrl_tigerlake.

## Origin

soc_button_array ignored -EPROBE_DEFER. Fixed in mainline by ed22ad5fdbdb (7.3; stable 7.2.8, 6.18.54,
6.12.112), verified on an SP9. Kept here for traceability; linux-surface 0009 is now redundant.

## Reports

- [linux-surface#1392](https://github.com/linux-surface/linux-surface/issues/1392) (open issue, could-close) "Hardware buttons on SP9 not working anymore after updating to arch-6.7.9-1": SP9 buttons after arch 6.7.9; CmdrShepardsPie verified the fix on SP9 (2026-10-25)
- [linux-surface#1481](https://github.com/linux-surface/linux-surface/issues/1481) (open issue, workaround) "Surface Pro 7 Hardware Buttons Occassionally don't work": SP7 buttons sometimes dead
- [linux-surface#1914](https://github.com/linux-surface/linux-surface/issues/1914) (open issue, workaround) "6.17.1-surface-2 kernel on Ubuntu 25.10: Power and Volume Buttons do not work": SP8 buttons dead on Ubuntu 25.10
- [linux-surface#2144](https://github.com/linux-surface/linux-surface/issues/2144) (open issue, other) "Surface Pro 12 Intel (MSHW0743 / Panther Lake) Linux enablement tracker": SP12 MSHW0040 deferred probe
- [rhbz#2488614](https://bugzilla.redhat.com/show_bug.cgi?id=2488614) (NEW) "Framework Laptop 12: soc_button_array probe of INT33D3 fails silently at boot, never retried; manual bind works": Framework Laptop 12 same bug

## Fixes, patches and PRs

- [torvalds/linux@ed22ad5fdbdb](https://git.kernel.org/torvalds/c/ed22ad5fdbdb): Input: soc_button_array - fix MS Surface Pro 11 probe failure
- [linux-surface/kernel#172](https://github.com/linux-surface/kernel/issues/172) (closed PR, merged) "Input: soc_button_array: defer MSHW0040 probe until GPIO is ready": downstream defer patch (merged 2026-11-09, now redundant)
- [lore:20261021015004.1537738-1-dmitry.torokhov@gmail.com](https://lore.kernel.org/r/20261021015004.1537738-1-dmitry.torokhov@gmail.com) (linux-input, new, Dmitry Torokhov, 2026-10-21) "Input: soc_button_array - use resources to set up IRQ info for gpio-keys": Torokhov: use resources to set up IRQ info (cleanup)

## Possible solutions

- Nothing to send. Ask linux-surface to drop 0009 on 7.3+; close #1392.

## Next steps

- [ ] Confirm buttons on the stock Fedora kernel in phase 0 (SP9-901).

## Upstream and people

- Upstream target: linux-input
- People: Hans de Goede, CmdrShepardsPie

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check), [SP9-902](SP9-902-close-already-fixed-sp9-issues-on-linux-surface-with-links-t.md) Close already-fixed SP9 issues on linux-surface with links to the fixing commits, [SP9-904](SP9-904-fix-out-of-date-linux-surface-wiki-pages-for-the-sp9.md) Fix out-of-date linux-surface wiki pages for the SP9

## Knowledge base

- [docs/research/open-issues.md](../docs/research/open-issues.md)

_Generated from `issues/src/2-cover-input.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
