---
id: SP9-110
title: Slim Pen 2 Bluetooth link drops when idle
labels:
- area:pen
- kind:bug
- priority:P3
- status:open
depends_on: []
blocks: []
related:
- SP9-109
- SP9-505
upstream:
- BlueZ
- linux-bluetooth
source: issues/src/1-touch-pen.yaml
---

# SP9-110: Slim Pen 2 Bluetooth link drops when idle

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P3 | pen | bug | partial | partial | partial |

## Problem

The pen's Bluetooth connection (battery, buttons, haptics) disconnects when not in use.

## Origin

Unknown; a btmon capture from an SP9 exists, no analysis.

## Reports

- [linux-surface#1656](https://github.com/linux-surface/linux-surface/issues/1656) (closed issue, stale) "Surface Slim Pen 2 disconnects when not in use": Slim Pen 2 disconnects when not in use (btmon on SP9), closed without fix

## Fixes, patches and PRs

- none yet

## Possible solutions

- Compare with Windows behaviour; check btintel and BlueZ idle timeouts.

## Next steps

- [ ] Capture btmon on an SP9 when the drop happens.

## Upstream and people

- Upstream target: BlueZ, linux-bluetooth
- People: otjamin

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-109](SP9-109-slim-pen-2-haptic-feedback-is-not-supported.md) Slim Pen 2 haptic feedback is not supported, [SP9-505](SP9-505-wi-fi-and-bluetooth-instability-iwlwifi-crash-on-resume-drop.md) Wi-Fi and Bluetooth instability (iwlwifi crash on resume, dropouts, BT device drops)

## Knowledge base

- [docs/research/closed-issues.md](../docs/research/closed-issues.md)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
