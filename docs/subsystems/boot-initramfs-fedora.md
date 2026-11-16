# Boot, initramfs, Secure Boot and Fedora packaging

## Booting

- Disable Secured-core in UEFI to boot from USB (wiki Surface-Pro-9). Re-enable after install if wanted.
- Firmware updates can make Fedora freeze on the Microsoft logo with enrolled keys (#1162, #1274, #1453 MokManager does not start). Firmware updated from Windows fixed several SP9 install problems (discussions 1366, 1746).
- linux-surface kernel is MOK signed; Fedora stock kernel is Secure Boot signed by Fedora.

## Keyboard in the initramfs (LUKS unlock)

- Problem: the Type Cover works in GRUB but not at the LUKS prompt (#1221 SP9 Fedora 38, #1126, #1491 NixOS, #1828 Slackware, discussion 2024 SP8 Fedora 43, #911, #1350, #2039).
- Modules needed (from #1221, #1828 and the wiki): `surface_aggregator surface_aggregator_registry surface_aggregator_hub surface_hid_core surface_hid 8250_dw intel_lpss intel_lpss_pci pinctrl_tigerlake` (pinctrl_tigerlake also fixes the button race).
- dracut master (read 2026-11-14, 04e04cfe) `modules.d/70kernel-modules/module-setup.sh` installs `=drivers/hid`, `=drivers/tty/serial`, `=drivers/pinctrl`, `intel_lpss_pci` and `surface_aggregator_registry` through `optional_hostonly`, which is empty unless `hostonly_mode=strict`. Fedora uses the default sloppy mode, so `surface_hid`, `surface_hid_core`, `8250_dw`/`8250_lpss` and `pinctrl_tigerlake` are already in its initramfs. Missing: `surface_aggregator_hub` (drivers/platform/surface), which binds the KIP hub the SP8/SP9 cover hangs off. Fedora has `SERIAL_8250_DW=y` and `SERIAL_8250_LPSS=m`.
- Field-tested list: Universal Blue `ublue-os/hwe` ships `modules-load.d/ublue-surface.conf` with `surface_aggregator surface_aggregator_registry surface_aggregator_hub surface_hid_core 8250_dw surface_hid surface_kbd intel_lpss intel_lpss_pci pinctrl_tigerlake` and tracks it with rpm-ostree initramfs-etc. Same set as above plus `surface_kbd`.
- Omarchy (Arch) uses the same list in a mkinitcpio drop-in: `pinctrl_tigerlake surface_aggregator surface_aggregator_registry surface_aggregator_hub surface_hid_core surface_hid surface_kbd intel_lpss_pci 8250_dw`.
- Without the cover (tablet only): unl0kr from postmarketOS buffybox gives an on-screen keyboard at the LUKS prompt; #1857 shows it needs the DRM driver in the initramfs.
- Upstream target: dracut (dracut-ng/dracut). Proposed change: add `surface_aggregator_hub` next to `surface_aggregator_registry`, citing 8cc89664 (Benjamin Drung, SL4) as precedent. Verify first on a Fedora initramfs: `lsinitrd | grep -E 'surface|8250|pinctrl'`.

## Fedora kernel config (kernel-ark os-build, checked 2026-11-12)

All of these are set: `SURFACE_AGGREGATOR=m`, `SURFACE_AGGREGATOR_BUS=y`, `SURFACE_AGGREGATOR_CDEV=m`, `SURFACE_AGGREGATOR_REGISTRY=m`, `SURFACE_AGGREGATOR_HUB=m`, `SURFACE_AGGREGATOR_TABLET_SWITCH=m`, `SURFACE_HID=m`, `SURFACE_KBD=m`, `SURFACE_GPE=m`, `SURFACE_PLATFORM_PROFILE=m`, `SURFACE_DTX=m`, `SURFACE_ACPI_NOTIFY=m`, `SURFACE_PRO3_BUTTON=m`, `SURFACE_HOTPLUG=m`, `SENSORS_SURFACE_FAN=m`, `SENSORS_SURFACE_TEMP=m`, `BATTERY_SURFACE=m`, `CHARGER_SURFACE=m`, `SERIAL_DEV_BUS=y`, `SERIAL_DEV_CTRL_TTYPORT=y`, `PINCTRL_TIGERLAKE=m`, `PINCTRL_ALDERLAKE=m`, `VIDEO_INTEL_IPU6=m`, `IPU_BRIDGE=m`, `VIDEO_OV5693=m`, `VIDEO_OV13858=m`, `VIDEO_VD55G1=m`, `INTEL_SKL_INT3472=m`, `INTEL_THC_HID=m`, `INTEL_QUICKSPI=m`, `INTEL_QUICKI2C=m`, `INPUT_SOC_BUTTON_ARRAY=m`, `MFD_INTEL_LPSS_PCI=y`, `SERIAL_8250_DW=y`, `SERIAL_8250_LPSS=m`, `HID_MULTITOUCH=m`, `INTEL_VSC=m`.

So nothing SP9 related is blocked by Fedora config; everything missing is missing upstream.

## Fedora packaging gaps

| Item | State | Action |
|---|---|---|
| iptsd | not in Fedora | New package review. Spec exists upstream (`iptsd.spec`). Make touch-enabling package sets pull it in (discussion 2282 comment 1). |
| libwacom SP9 data | not upstream | linuxwacom/libwacom#89; see `touch-pen.md`. |
| libcamera software ISP on IPU6 | unknown | Check the Fedora libcamera build flags and pipeline handlers; compare with jwrdegoede/ipu6-softisp COPR. |
| dracut Surface modules | partial | One module missing (surface_aggregator_hub); PR to dracut-ng/dracut, nothing filed yet. |
| linux-surface Fedora repo | f44 present now | Discussions 2296 and 1889 were 404 reports for f44/f43; the f44/f45 workflows exist in linux-surface CI. |

## Fedora kernel backports

kernel-ark merge requests carry camera fixes ahead of mainline (ark !4395 ipu-bridge upside-down quirk for Dell XPS, !4757 int3472 regulator fix, !4884 open; rhbz#2539811 shows a dropped patch being restored). Dave Olsthoorn enabled the Surface modules and OV5693 in the Fedora config (ark !962, !1084, !1614). Route for SP9 fixes once they are accepted upstream.

## Kernels you can run on Fedora today (short term)

1. linux-surface `kernel-surface` (pkg.surfacelinux.com, built with `pkg/fedora/kernel-surface/build-linux-surface.py` on kernel-ark tag `kernel-7.3.3-0`).
2. CmdrShepardsPie/surface-kernel-copr: `kernel-surface-cmdrshepardspie`, linux-surface 7.3.1 + 20 SP9 fixes, installs beside kernel-surface, signed only with the Red Hat test key (enrol your own MOK).
3. Stock Bazzite kernel + out-of-tree ITHC: John-S-Reddick/bazzite-surface.
4. Image based: ublue-os/hwe surface images, LorbusChris/bluefin-surface (bootc), NexGen-3D-Printing/bazzite-sdx.
5. Build your own from kernel-ark + the series in `data/indexes/patches-CmdrShepardsPie-7.3.1-pro9.md` with `build-linux-surface.py` (see `docs/roadmap.md`, phase 1).

## Stock Fedora kernels (Bodhi, 2026-11-14)

| Release | Stable | In testing |
|---|---|---|
| F45 | 7.3.3-300 | 7.3.4-300 |
| F44 | 7.3.3-200 | 7.3.4-200 |
| F43 | 7.3.3-100 | 7.3.4-100 |
| rawhide (F46) | 7.4.0-rc2 | |

Every stock Fedora kernel already has the button fix. Rawhide is the place to test the 7.4 camera work with no patches.
