---
id: SP9-505
title: Wi-Fi and Bluetooth instability (iwlwifi crash on resume, dropouts, BT device drops)
labels:
- area:wireless
- kind:bug
- priority:P3
- status:needs-test
depends_on: []
blocks: []
related:
- SP9-110
upstream:
- iwlwifi (Intel)
- BlueZ
source: issues/src/5-audio-display-wireless.yaml
---

# SP9-505: Wi-Fi and Bluetooth instability (iwlwifi crash on resume, dropouts, BT device drops)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| needs-test | P3 | wireless | bug | partial | partial | partial |

## Problem

Reports of iwlwifi crashing on resume on Alder Lake-P CNVi, Wi-Fi dropping on connect, and Bluetooth mice
disconnecting.

## Origin

Mostly generic Intel AX211 / iwlwifi firmware issues, not Surface-specific; BT mouse drops are autosuspend.

## Reports

- [linux-surface#1973](https://github.com/linux-surface/linux-surface/issues/1973) (open issue, workaround) "iwlwifi crash on resume from suspend - Alder Lake-P CNVi WiFi": iwlwifi crash on resume (ADL-P CNVi): iwlmvm power_scheme=1 made it rarer
- [linux-surface#1503](https://github.com/linux-surface/linux-surface/issues/1503) (open issue, workaround) "[SP9] Wi-Fi instantly switches off when trying to connect to anything": SP9 Wi-Fi off on connect: pinning linux-firmware 20240610 helped (2024)
- [linux-surface#1405](https://github.com/linux-surface/linux-surface/issues/1405) (closed issue, workaround) "SP9 w Ubuntu 22.04 WiFi dropouts": SP9 dropouts: separate 2.4 and 5 GHz SSIDs (closed)
- [linux-surface#1178](https://github.com/linux-surface/linux-surface/issues/1178) (open issue, workaround) "Bluetooth mouse's connection drops quickly": SP9 BT mouse drops: autosuspend rule
- [linux-surface#1988](https://github.com/linux-surface/linux-surface/issues/1988) (closed issue, workaround) "[SP9] Bluetooth keeps disconnecting": SP9 BT disconnects: re-pair (closed)
- [linux-surface#1794](https://github.com/linux-surface/linux-surface/issues/1794) (open issue, workaround) "WiFi Is Not Working on Surface Pro with Intel AX211": SP9 Debian 12 AX211 after kernel swap

## Fixes, patches and PRs

- none yet

## Possible solutions

- If it reproduces on current Fedora, report to iwlwifi (Intel) with firmware version; not a Surface upstreaming item.

## Next steps

- [ ] Watch during daily use.

## Upstream and people

- Upstream target: iwlwifi (Intel), BlueZ
- People: none

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-110](SP9-110-slim-pen-2-bluetooth-link-drops-when-idle.md) Slim Pen 2 Bluetooth link drops when idle

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/5-audio-display-wireless.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
