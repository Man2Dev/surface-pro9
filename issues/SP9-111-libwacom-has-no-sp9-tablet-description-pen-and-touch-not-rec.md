---
id: SP9-111
title: libwacom has no SP9 tablet description (pen and touch not recognised as a tablet)
labels:
- area:pen
- kind:upstreaming
- priority:P2
- status:open
depends_on: []
blocks:
- SP9-903
related:
- SP9-101
- SP9-102
- SP9-113
upstream:
- linuxwacom/libwacom (Peter Hutterer)
source: issues/src/1-touch-pen.yaml
---

# SP9-111: libwacom has no SP9 tablet description (pen and touch not recognised as a tablet)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P2 | pen | upstreaming | n/a | works | broken |

## Problem

GNOME and Plasma tablet settings, pen mapping and palm-rejection grouping need a libwacom entry. Upstream
libwacom has none for the SP9; libwacom-surface (fork) has one but conflicts with Fedora's libwacom, which
Plasma requires.

## Origin

iptsd creates uinput devices on BUS_VIRTUAL. Upstream libwacom only accepts usb, serial, bluetooth and i2c
(its UINPUT_SUBSYSTEM override maps only to those). Two attempts to add the MEI bus were refused: Peter
Hutterer will not support buses that only exist with out-of-tree kernel code (libwacom#92, #93 in 2019;
#400 in 2021). Newer Surfaces on intel-thc-hid will show up on SPI, which libwacom does not know either.

## Reports

- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": swapping libwacom for libwacom-surface plus an override file works
- [linux-surface/libwacom-surface#13](https://github.com/linux-surface/libwacom-surface/issues/13) (closed issue, fixed-package) "Missing Pro 8 support": SP9 data added in the fork
- [linux-surface/iptsd#212](https://github.com/linux-surface/iptsd/issues/212) (closed) "libwacom-surface removes a lot of fedora 44 kde plasma packages": libwacom-surface removes many Fedora 44 KDE packages
- [linuxwacom/libwacom#89](https://github.com/linuxwacom/libwacom/issues/89) (closed) "Microsoft Surface IPTS device integration": Microsoft Surface IPTS device integration (mass-closed 2022)
- [rhbz#2463712](https://bugzilla.redhat.com/show_bug.cgi?id=2463712) (CLOSED/ERRATA) "gnome-shell crashes on startup: libwacom assertion bus_to_str on Microsoft Surface (i2c-hid touch/pen)": libwacom bus_to_str abort on a Surface (fixed 2.18.0-2)

## Fixes, patches and PRs

- [linuxwacom/libwacom#92](https://github.com/linuxwacom/libwacom/issues/92) (closed-unmerged) "Add support for Intel Management Engine bus": MEI bus support (closed by author after maintainer concerns)
- [linuxwacom/libwacom#93](https://github.com/linuxwacom/libwacom/issues/93) (closed-unmerged) "Device data for IPTS based Microsoft Surface Devices": IPTS Surface device data (closed)
- [linuxwacom/libwacom#400](https://github.com/linuxwacom/libwacom/issues/400) (closed-unmerged) "Adds Intel Management Engine Interface (MEI) Bus": MEI bus, second attempt (closed for no reply)
- [linuxwacom/libwacom#967](https://github.com/linuxwacom/libwacom/issues/967) (closed) "Switch tablet dimensions from inches to mm": tablet dimensions in mm (affects the fork's SP9 file)
- [linuxwacom/wacom-hid-descriptors#490](https://github.com/linuxwacom/wacom-hid-descriptors/issues/490) (open) "Contributing: MS Surface Pro 9": SP9 sysinfo contributed

## Possible solutions

- Ask Peter Hutterer once how IPTS/ITHC (virtual) and THC QuickSPI (SPI) Surfaces should be described; options: iptsd tags its uinput devices with UINPUT_DEVICE/UINPUT_SUBSYSTEM, or libwacom gains virtual/spi buses.
- Then send the SP9 data file (Stylus=true, Styli list, size in mm).
- Workaround now: the /etc/libwacom override plus the udev LIBINPUT_DEVICE_GROUP rule (docs/workarounds.md).

## Next steps

- [ ] Open a libwacom issue asking the bus question, linking the earlier refusals.

## Upstream and people

- Upstream target: linuxwacom/libwacom (Peter Hutterer)
- People: whot, qzed

## Linked issues

- Depends on: none
- Blocks: [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-101](SP9-101-touchscreen-and-pen-need-the-out-of-tree-ithc-driver-no-upst.md) Touchscreen and pen need the out-of-tree ITHC driver (no upstream driver for the ADL THC in legacy mode), [SP9-102](SP9-102-iptsd-is-not-packaged-in-fedora.md) iptsd is not packaged in Fedora, [SP9-113](SP9-113-kwin-shows-the-mouse-cursor-while-the-pen-hovers.md) KWin shows the mouse cursor while the pen hovers

## Knowledge base

- [docs/research/upstream-efforts.md](../docs/research/upstream-efforts.md)
- [docs/workarounds.md](../docs/workarounds.md)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
