---
id: SP9-209
title: Surface Pro Flex Keyboard untested on the SP9
labels:
- area:cover
- kind:needs-test
- priority:P3
- status:needs-test
depends_on: []
blocks: []
related:
- SP9-203
upstream: []
source: issues/src/2-cover-input.yaml
---

# SP9-209: Surface Pro Flex Keyboard untested on the SP9

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| needs-test | P3 | cover | needs-test | unknown | unknown | unknown |

## Problem

No SP9 report exists for the Flex Keyboard attached or detached (Bluetooth).

## Origin

Data points only from SP10/SP11/SP12; the tablet switch may need zero-padded source handling.

## Reports

- [linux-surface#1608](https://github.com/linux-surface/linux-surface/issues/1608) (closed issue, other) "Surface Pro 10 Support": SP10 support
- [linux-surface#2144](https://github.com/linux-surface/linux-surface/issues/2144) (open issue, other) "Surface Pro 12 Intel (MSHW0743 / Panther Lake) Linux enablement tracker": SP12 enablement tracker
- [linux-surface#1845](https://github.com/linux-surface/linux-surface/issues/1845) (open issue, patch-pending) "[SP9] Fedora 42 Hanging on boot with surface_hid": pen stash node answers only on covers with a tray

## Fixes, patches and PRs

- [linux-surface/kernel#173](https://github.com/linux-surface/kernel/issues/173) (open PR, needs-update) "platform/surface: aggregator_tabletsw: accept zero-padded source-l": aggregator_tabletsw: accept zero-padded source-list responses (needs update)

## Possible solutions

- Test if a Flex Keyboard is available.

## Next steps

- [ ] Skip unless the hardware is at hand.

## Upstream and people

- Upstream target: none
- People: zR-JB

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-203](SP9-203-boot-stalls-about-2-minutes-surface-hid-probes-the-pen-stash.md) Boot stalls about 2 minutes: surface_hid probes the pen stash node and fails with -EPROTO

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/2-cover-input.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
