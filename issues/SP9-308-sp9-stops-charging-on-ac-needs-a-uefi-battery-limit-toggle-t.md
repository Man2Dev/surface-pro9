---
id: SP9-308
title: SP9 stops charging on AC (needs a UEFI battery limit toggle to recover)
labels:
- area:battery
- kind:bug
- priority:P2
- status:open
depends_on: []
blocks: []
related:
- SP9-309
upstream:
- platform-driver-x86 / linux-pm
source: issues/src/3-power.yaml
---

# SP9-308: SP9 stops charging on AC (needs a UEFI battery limit toggle to recover)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P2 | battery | bug | partial | partial | partial |

## Problem

At some point the SP9 stops charging and slowly discharges on AC (USB-C and Surface Connect alike);
rebooting into UEFI and toggling Battery Limit on and off restores charging. Separately, the battery can
report full while discharging.

## Origin

Firmware/EC charge state (Windows smart charging or the UEFI limit) that Linux cannot reset today. The
kernel side has no control over charge modes yet (SP9-309).

## Reports

- [linux-surface#2232](https://github.com/linux-surface/linux-surface/issues/2232) (open issue, workaround) "Surface Laptop 5 intermittently stops charging": SL5 stops charging; two SP9 confirmations
- [linux-surface#1781](https://github.com/linux-surface/linux-surface/issues/1781) (closed issue, workaround) "Surface Pro 9 charging stopped working after Ubuntu 24.04 updates (June 3, 2025)": SP9 charging stopped (Windows smart charging, closed)
- [linux-surface#1800](https://github.com/linux-surface/linux-surface/issues/1800) (open issue, workaround) "battery/ not charging": not charging: turn off UEFI battery limit (SP9)
- [linux-surface#1837](https://github.com/linux-surface/linux-surface/issues/1837) (open issue, needs-info) "Battery indicates full, even when actually discharging (Surface Pro 9)": SP9 battery shows full while discharging
- [linux-surface#348](https://github.com/linux-surface/linux-surface/issues/348) (closed issue, workaround) "Surface Pro 7 not battery status": battery near 50 %: UEFI limit (closed)
- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": NexGen-3D-Printing debugging the SP9 battery charge bug on Fedora 44/45 and Bazzite 45 (2026-11-16)

## Fixes, patches and PRs

- [lore:20261023173215.6233-1-ramonjesusmiranda@gmail.com](https://lore.kernel.org/r/20261023173215.6233-1-ramonjesusmiranda@gmail.com) (platform-driver-x86, new, Ramon Jesus Miranda, 2026-10-23) "power: supply: surface_battery: handle battery event 0x1a": surface_battery: handle battery event 0x1a (pending)

## Possible solutions

- Workaround: UEFI Battery Limit on, boot once, off again.
- Use BAT 0x09/0x0a (GetUserChargeMode/SetUserChargeMode) from the Surface command headers to read and reset the mode from Linux (SP9-309).

## Next steps

- [ ] When it happens on an SP9, capture /sys/class/power_supply/* before toggling UEFI.
- [ ] Ask NexGen-3D-Printing to post his logs and findings on #2232, so they sit with the other SP9 reports.

## Upstream and people

- Upstream target: platform-driver-x86 / linux-pm
- People: halfnathan1200, NexGen-3D-Printing, Cloveian

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-309](SP9-309-no-battery-charge-limit-or-smart-charging-control-from-linux.md) No battery charge limit or smart charging control from Linux

## Knowledge base

- [status.yaml](../status.yaml)
- [docs/research/closed-issues.md](../docs/research/closed-issues.md)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
