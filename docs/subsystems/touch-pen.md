# Touchscreen and pen (ITHC + iptsd + libwacom)

Status keys: `touchscreen`, `pen`.

## Stack

1. Kernel: Intel Touch Host Controller on ADL-P, PCI `8086:51d0` / `8086:51d1`. Driven by the downstream ITHC driver (`linux-surface 0006-ithc.patch`, source of truth quo/ithc-linux) plus "iommu: intel: Disable source id verification for ITHC". ITHC exposes the raw IPTS-style HID stream as hidraw.
2. Userspace: `iptsd` (linux-surface/iptsd v3.1.1) turns heatmaps into multitouch and pen events on uinput devices `IPTSD Virtual * 045E:0C52`. Without iptsd you get single touch only.
3. libinput / libwacom: pen and touch device grouping and tablet metadata.

## Why mainline does not cover the SP9

- Mainline has `drivers/hid/intel-thc-hid` (QuickSPI, QuickI2C) since 6.14. Per quo (discussion 1581, quo/ithc-linux#29) it only supports MTL and newer and the standard HID-over-SPI/I2C protocols. quo/ithc-linux commit a82c299 (2025-05-27) stops matching MTL+ for that reason. SP9 (ADL-P) needs ITHC. Verified in v7.4-rc2 source: intel-quickspi and intel-quicki2c PCI ids cover MTL, ARL, LNL, PTL, WCL and NVL only, no ADL-P 0x51d0/0x51d1.
- StollD (discussion 1305): three different drivers are needed across Surfaces: IPTS (up to SP7+), ITHC (after that), SPI-HID (AMD). qzed (discussion 796): upstreaming waits for a stable userspace interface.
- `linux-surface 0005-ipts.patch` (MEI) is not used on SP9.

## Known issues

- Erratic touch: wiki calibration file `/etc/iptsd.d/91-calibration.conf` with `ActivationThreshold = 24`, `DeactivationThreshold = 20`, `OrientationThresholdMax = 5` (iptsd#171).
- #2367 (open, 2026-11-07): `ithc_legacy_init failed`, touch and pen dead on 6.19 / 7.2.
- iptsd udev issues on ITHC: iptsd#220, #221 (hide raw ithc input nodes), #224, #229, #219 (service stops after 6 s on cold boot).
- #1078 touch not working with EFI stub kernel; #1862 better touch without iptsd on GNOME 48 (tuning question).
- Pen: iptsd#156 (MPP v2+, Slim Pen 2, SP9 improvements, merged 2024), iptsd#166 DisableOnStylus, #1588 jagged fast lines, #1656 Slim Pen 2 disconnects, #1066 haptics (not supported).

## Outside the org

- iwanders/analysis-ithc-iptsd: THC and Slim Pen 2 analysis done on an SP9 (button glitch, DFT format, raw captures in releases). Background for iptsd#156.
- iptsd forks: AndyGozas `bundle-events-workaround` (jagged lines, #1588), wvffle stylus lift timeout (iptsd#166), LegendaryFire reconnect and detection branches.
- John-S-Reddick/bazzite-surface: SP9 touch and pen on Bazzite's own (Fedora-derived) kernel with only an out-of-tree ithc.ko (quo/ithc-linux pinned, MOK signed), iptsd and a tablet file. Everything except cameras already works on that kernel.
- intel/thc-drivers (Intel, out of tree, synced to 7.4-rc1): THC v2 on ADL adds HIDSPI, but the PCI tables stop at MTL and IPTS mode is left to linux-surface. quo/ithc-linux#34: SL5 on the same 8086:51d0 gets zero events on F44.
- Calibration data from SP9 users: xbtry/sp9lintouch (contact size 0.3 to 1.1), zeroxoneafour/linux-surface-config (DisableOnStylus, wiki thresholds).
- Desktop: KWin shows the cursor when the pen hovers (rhbz#2524606, patch attached).
- IPTS (MEI) forks of the kernel (jaydens-tasty-slop, loafecho, joshuaspaulding) target SP4 to SP7+ and do not apply.

## libwacom

- Upstream libwacom has no SP9 tablet file and no virtual bus type. libwacom-surface carries `0001-Add-support-for-BUS_VIRTUAL`, `0002-Add-support-for-Intel-Management-Engine-bus` and `0010-data-Add-Microsoft-Surface-Pro-9` (`DeviceMatch=virt|045e|0c52`, Width 275, Height 183, `Stylus=false`, Touch=true).
- The working override from discussion 2282 (copy in `docs/workarounds.md`) sets `Stylus=true`, `Styli=0xfffff;0xffffe;`, Width 274, and groups pen and touch via udev `LIBINPUT_DEVICE_GROUP="iptsd-045e-0c52"` so palm rejection works while the pen hovers.
- Upstream discussion: linuxwacom/libwacom#89 (2020), stalled not rejected.
- Observation for the upstream path: upstream libwacom `get_uinput_subsystem()` honours udev properties `UINPUT_DEVICE` and `UINPUT_SUBSYSTEM` on uinput parents. If iptsd's udev rules tag its uinput devices with a real subsystem, an upstream data file could match without BUS_VIRTUAL. Needs a test.
- Fedora: libwacom-surface conflicts with the libwacom version plasma-desktop requires; Terra ships a compatible libwacom-surface (`dnf swap libwacom libwacom-surface --allowerasing`). Arch hit the same version treadmill (discussion 2041, libwacom-surface#19, #22).

## Packaging

- iptsd is not in Fedora (src.fedoraproject.org search, 2026-11-12). linux-surface/iptsd ships `iptsd.spec` (meson, CLI11, eigen3, fmt, inih, Microsoft.GSL, spdlog, optional cairomm/SDL2 for tools). linux-surface's `kernel-surface` already pulls iptsd as a weak dependency (`pkg/fedora/kernel-surface/patches/0001-Pull-in-iptsd-as-a-weak-dependency.patch`). Nobara packages iptsd in nobara-updates. Terra ships iptsd for f43 to f45 and el10 since 2026-09 (terrapkg/packages#16814).
