---
id: SP9-204
title: Keyboard backlight cannot be controlled from the desktop
labels:
- area:cover
- kind:missing-feature
- priority:P2
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-202
upstream:
- platform-driver-x86
source: issues/src/2-cover-input.yaml
---

# SP9-204: Keyboard backlight cannot be controlled from the desktop

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P2 | cover | missing-feature | broken | broken | broken |

## Problem

The cover backlight works with Fn keys but Plasma shows no keyboard backlight control.

## Origin

surface_hid exposes no LED class device for the KIP keyboard (045E:09AE). A patch adding it is on
platform-driver-x86, with no review yet.

## Reports

- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": backlight works but Plasma has no control
- [linux-surface#469](https://github.com/linux-surface/linux-surface/issues/469) (closed issue, other) "Keyboard backlight cannot be turned on": keyboard backlight cannot be turned on (older device)

## Fixes, patches and PRs

- [lore:20261023173213.6219-1-ramonjesusmiranda@gmail.com](https://lore.kernel.org/r/20261023173213.6219-1-ramonjesusmiranda@gmail.com) (platform-driver-x86, new, Ramon Jesus Miranda, 2026-10-23) "HID: surface-hid: support keyboard backlight on Surface Pro Keyboard (045E:09AE)": HID: surface-hid: support keyboard backlight on Surface Pro Keyboard (045E:09AE)

## Possible solutions

- Test the patch on the SP9 (its cover is 045E:09AE) and reply with Tested-by.

## Next steps

- [ ] Build a kernel with the patch, check /sys/class/leds and Plasma, reply on-list.

## Upstream and people

- Upstream target: platform-driver-x86
- People: Ramon Jesus Miranda

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-202](SP9-202-type-cover-dead-or-slow-after-boot-sam-probe-returns-einval.md) Type Cover dead or slow after boot: SAM probe returns -EINVAL before the pin controller is ready

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/2-cover-input.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
