# linux-surface wikis: what they say about the SP9 (2026-11-13)

Sources, all git clonable:
- `linux-surface/linux-surface.wiki` (59 pages, HEAD 0cac953e8ae5, 2026-11-12, 1279 commits). Every page was read; history of `Surface-Pro-9.md` (35 commits) was read for removed workarounds.
- `linux-surface/iptsd.wiki` (Calibrating-iptsd), `linux-surface/surface-aggregator-module.wiki` (Features, Performance-Modes), `linux-surface/kernel.wiki` (old IPTS notes). The other org repos have no wiki.

## Surface-Pro-9.md (current)

- Disable Secure Core in UEFI to boot from USB; it can be re-enabled after installing.
- Screen flicker: `i915.enable_psr=0` (#862).
- ACPI interrupt storm (lid close on AC, Thunderbolt hotplug, lid resume): `pci=hpiosize=0` (#1082).
- Erratic touch: `/etc/iptsd.d/91-calibration.conf` with `ActivationThreshold = 24`, `DeactivationThreshold = 20`, `OrientationThresholdMax = 5` (iptsd#171).
- Power and volume buttons: `soc_button_array` loads before `pinctrl_tigerlake` (#1392). Workarounds: reload `soc_button_array`, or put `pinctrl_tigerlake` in the initramfs. For dracut: `/etc/dracut.conf.d/fix_hardware_buttons.conf` with `force_drivers+=" pinctrl_tigerlake "`, then `dracut -f --regenerate-all`. (The section titled "mkinitcpio" actually gives the Debian initramfs-tools steps.)
- Power: S0ix works with very low runtime screen-off residency (0.01 % in S0ixSelftestTool); shutdown works since 6.1.12-2 (#1058); hibernate needs `HibernateMode=reboot`. A ticking noise near the charging port after the S0ix selftest was reported.

## Removed from Surface-Pro-9.md over time (still useful as history)

- 2022-11 (aj3423, Nuttapong Punpipat): suspend was random; on resume the screen froze for about 50 s with an i915 "Selective fetch area calculation failed" message, then the ticking noise. Shutdown and hibernate hung with a black screen and the device stayed on and warm. The EFI shell `reset -s` shutdown workaround moved to Intel-12th-Generation-Devices-Issues.md when the SL5 showed the same bug.
- 2023-02 (Maximilian Luz): shutdown and hibernate notes replaced by "works since 6.1.12-2" after the PCI shutdown quirk.
- 2023-03 (RalphBariz): `intel_idle.max_cstate=0` against the ACPI event spam after waking on AC; then `AllowHibernation=no` and friends in `/etc/systemd/sleep.conf`.
- 2024-07 (3xfc): both replaced by `pci=hpiosize=0`.

## Other linux-surface wiki pages that apply to the SP9

- **Disk-Encryption.md** is the maintainers' own initramfs list for keyboards behind the Surface Aggregator Module: `surface_aggregator`, `surface_aggregator_registry`, `surface_aggregator_hub`, `surface_hid_core`, `8250_dw`, plus `surface_hid` (Surface Laptop 3 / Book 3 and later; `surface_kbd` is only for Laptop 1 and 2), plus `intel_lpss` and `intel_lpss_pci` on Intel and `pinctrl_tigerlake` on Tiger Lake and later. The page lists laptops and the Book 3 but not the Pro 8 or Pro 9, whose Type Cover also goes through SAM. Its Fedora example (`add_drivers+=` in `/etc/dracut.conf.d/surface.conf`) leaves out `8250_dw`, the LPSS modules and pinctrl. On-screen keyboard at the LUKS prompt: unl0kr (BuffyBox), with a note that IPTS touch in the initramfs needs the driver, daemon and config baked in.
- **Intel-12th-Generation-Devices-Issues.md**: S5 shutdown did not work on ADL Surfaces; EFI shell `reset -s` with an efibootmgr entry and BootNext as a workaround (historical for the SP9, still current for the SL5 and SL6).
- **Surface-Laptop-5.md** (closest ADL sibling): S4 hibernate and suspend unreliable, shutdown leaves the device on (#1058 quirk not enabled for SL5). Its Debian encryption list says `pinctrl_alderlake`; on ADL-P that is wrong, the pin controller is `INTC1055` and binds `pinctrl_tigerlake` (mainline `pinctrl-tigerlake.c`; `pinctrl-alderlake.c` only covers `INTC1056`/`INTC1085` ADL-S and `INTC1057` ADL-N, e.g. the Go 4).
- **Surface-Pro-10.md**: `i915.enable_psr2_sel_fetch=0` prevents an s2idle freeze, plus a udev rule for lid/cover wake and a buttons service. Same PSR2 selective fetch family as the 2022 SP9 resume freeze.
- **Surface-Pro-8.md**: per-camera status (front works on mainline 7.4 only, rear on linux-surface 6.17+, IR has no driver), both sensors mounted upside down, no IPA tuning files so colours are washed out; 120 Hz via xrandr; some SP8 units need a UEFI downgrade for GRUB (#1179).
- **Installation-and-Setup.md**, Fedora: `dnf install --allowerasing kernel-surface iptsd libwacom-surface`, `surface-secureboot` (MOK password `surface`), `kernel-surface-default-watchdog` keeps the surface kernel default when Fedora ships a newer one; Silverblue uses a dummy high-version kernel package. Update firmware from Windows first. Ubuntu 26.04 and Debian testing: do not install libwacom-surface (#2076).
- **Secure-Boot.md**: shim + MOK, or own keys with sbsign.
- **UEFI.md**: "Enable boot configuration lock" blocks writing EFI variables, so bootloader installs fail until it is turned off.
- **Systemd.md**: `/usr/lib/systemd/system-sleep/` hook template (pre/post, with `SYSTEMD_SLEEP_ACTION` for suspend-then-hibernate).
- **Known-Issues-and-FAQ.md**: speaker hiss while headphones play: `amixer sset "Auto-Mute Mode" Disabled`; how to read S0ix residency; blacklisting `surface_gpe` if lid events wake the device in suspend (#1060).
- **Thermald-setup-and-configuration.md**: how to write `thermal-conf.xml`; only an SP4 file is provided.
- **Camera-Support.md**: SP9 row still says front OV5693 not working, rear OV13858 working, IR VD55G0 not working. Fedora libcamera package list. Firefox PipeWire camera flag and the v4l2loopback recipe.
- **Pen-DFT-data-format.md**: MPP pen DFT packet format used by iptsd (reference for any upstream pen work).
- **Supported-Devices-and-Features.md**, SP9 column: keyboard, touchpad, tablet mode, touchscreen, pen and buttons marked "requires linux-surface kernel"; hibernate with footnote 19 (ADL issues page); S0ix with footnote 21 (poor screen-off residency); battery and performance modes need 5.13+ or linux-surface; cameras not working.

## Other wikis

- **surface-aggregator-module wiki, Features.md**: SP9 supports battery status, platform profiles, type-cover/generic HID and tablet mode through SAM. Performance-Modes.md maps platform profiles to Windows modes (low-power = Battery Saver, balanced = Recommended, balanced-performance = Better Performance, performance = Best Performance).
- **iptsd wiki, Calibrating-iptsd.md**: `iptsd-calibrate $(iptsd-find-hidraw)` measures finger size and aspect; write `SizeMin/SizeMax/AspectMin/AspectMax` to `/etc/iptsd.d/90-calibration.conf`.

## Wiki pages that are out of date for the SP9 (edits to propose)

- Supported-Devices-and-Features: keyboard, touchpad and tablet mode work on mainline (SP9 SAM node group, tablet switch accepted 2023-03); cameras work on 7.4 (front needs the binned-mode patch, see `docs/subsystems/camera.md`).
- Camera-Support: SP9 row (front works on 7.4 plus the binned-mode fix, IR has driver series on linux-media).
- Disk-Encryption: add the Pro 8 and Pro 9 to the SAM keyboard list and give a complete Fedora dracut example.
- Surface-Laptop-5: `pinctrl_tigerlake`, not `pinctrl_alderlake`, on ADL-P.
- Surface-Pro-9: the "mkinitcpio" heading shows initramfs-tools commands; add the lid wake problem (#2257) and the iptsd service stopping after cold boot (iptsd#219).
