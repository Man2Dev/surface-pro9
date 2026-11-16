# Closed issues: what was solved and how (2026-11-13)

207 closed issues across the linux-surface org were read in full (every comment plus the close event): 129 mention the SP9, 78 are siblings with the same hardware path (SP8, SL5, SP10, ITHC or iptsd). Table: `data/indexes/closed-issues.tsv`. Closed issues already in `github-sp9.tsv` only had their last comment there; this pass reads the whole thread.

## How they end

91 have no lesson for the SP9 (other devices, old packaging, Ubuntu or NixOS builds). Of the rest: 29 fixed by a package or repo change, 20 closed with a workaround, 16 fixed in the kernel, 8 by a kernel or initramfs config change, 9 were setup mistakes (usually iptsd missing or the wrong kernel), 2 firmware, 1 hardware, 20 informational. 11 were closed without a fix (stale), mostly by their authors; those still describe open problems.

## Lessons for a stock Fedora SP9

Keyboard, Type Cover, initramfs
- `CONFIG_SERIAL_DEV_BUS=y` and `CONFIG_SERIAL_DEV_CTRL_TTYPORT=y` (built in) are required for the cover (#1136). kernel-ark has both.
- Module order matters: on SP9 the cover died after 6.12.4 until `pinctrl_tigerlake` was loaded first in the initrd (#1645). Same root cause as the SAM serial hub probe ordering (#2219, fix posted upstream) and the button race (#1392). One more argument for putting `pinctrl_tigerlake` in the dracut module.
- SP9 LUKS list that worked (#1491, NixOS, from jf049): `surface_aggregator surface_aggregator_registry surface_aggregator_hub surface_hid_core surface_hid surface_battery surface_charger surface_fan 8250_dw intel_lpss intel_lpss_pci pinctrl_tigerlake`. The battery, charger and fan modules are not needed to type but avoid errors from the registry. Silverblue: fixed through silverblue-docs (#1350). SP8 on Fedora: Clevis plus TPM2 as a fallback when the cover does not come up (#2039). Fedora 41 report #1709 was closed unanswered.
- Disable-while-typing needs the cover tagged as an internal keyboard (#67). That landed in upstream libinput: `50-system-microsoft.quirks` tags `*Microsoft Surface *Keyboard*` (for example `Microsoft Surface 045E:09AE Keyboard`) on DMI vendor Microsoft Corporation as internal. The DMI modalias drops spaces (`ascii_filter` in `drivers/firmware/dmi-id.c`), so the leading space some SP9 units have in sys_vendor (#2257) does not break it. Nothing to upstream.
- Covers that drop out with "unknown device posture" were worn connectors (#2036).

Boot
- 6.10 hangs and panics on SP9 (kernel#157, #1533, #1537, #1541, #1555) were IPU6: blacklisting `intel_ipu6` and `intel_ipu6_isys` (underscores, #1516) worked; #1560 closed as fixed in 6.15. Keep in mind when testing camera kernels.
- 6.10.3 invalid opcode traps needed the GDS mitigation off (#1534), all Intel models.
- Secure Boot: GRUB fonts and gfxmode need signed modules (#1320).

Battery and power
- Battery stuck near 50 % or not charging is the UEFI battery limit or Windows smart charging, not the driver (#348, #354, SP9 #1781). Check UEFI first.
- A leftover `blacklist-intel_lpss.conf` from old guides breaks SAM and battery (#464).
- Intel Thread Director patches broke wake on ADL/RPL including SP9 and were removed (#1084, #1120, #1188). Any future ITD backport needs an SP9 suspend test.
- SP9 fan spinning on rotation or video was ITHC, fixed for 6.5 (#1252).
- `pci=hpiosize=0` (#1082) stops the ACPI error spam but, per a 2025-10 SP9 report in the same thread, opening the cover then no longer wakes the device. That ties `acpi-interrupt-storm` to `lid-wake`: test both together. #1446 used TLP plus blacklisting `surface_gpe` instead, which also gives up lid wake.
- SP9 wake: #1684 worked for one user on a self-built 6.12.12 and stayed broken on F41 for another; #1161 closed without a fix.
- Spontaneous shutdowns were SAM firmware (#999). S0ix broken after reboot fixed by current intel microcode (#2279). Shutdown hang fixed by the PCI quirk (surface-shutdown#1, #1058).

Touch and pen
- Touch and pen "not working" is almost always iptsd missing or the stock kernel (#1156, #1330, #1848, #987); `/dev/ipts` no longer exists, iptsd uses hidraw (`iptsd-find-hidraw`).
- Slim Pen 2 random button presses: `ButtonMinMag = 20000` under `[DFT]` in an `/etc/iptsd.d/` file (#1233, 2023). iptsd 3.x has since added `Mpp2ButtonMinMag` (default 50000) for MPP 2 pens, so the workaround may no longer be needed; open iptsd#233 debounces the flags in code.
- Palm rejection lost after an iptsd update: recalibrate (#1273); low polling: `iptsd-calibrate` (#2269, the script in that thread is AI-written).
- Touch dead after resume is the most repeated unsolved problem: iptsd#122, #1171 (mentions quo's ITHC DMA fix b51f328), #1799 (SP10), all closed without a fix. Orphaned fix candidate: `orphaned-patches/linux-surface-2210-ithc-pm-preserve-hid-device.patch`.
- Slim Pen 2 drops its Bluetooth link when idle (#1656, btmon capture on SP9), no fix.
- systemd device tag for the ITHC node (iptsd#9) is the same family as open iptsd#224.

libwacom
- SP9 tablet data came in libwacom-surface#13; X11 needed xf86-input-wacom PR #352 (libwacom-surface#8); libinput 1.28.1 broke a release (libwacom-surface#19, #1727); libwacom-surface 2.20.0-1 fixes Ubuntu 26.04 (#2076).

Wireless and desktop
- Wi-Fi dropouts on SP9: separate 2.4 and 5 GHz SSIDs (#1405). BT disconnects: remove and re-pair (#1988); BT mouse drops (#1018, #1178).
- Long KDE Wayland login delay came from iio-sensor-proxy (#1969).
- 120 Hz, rotation and ambient light work on SP9 (#1096).

Fedora packaging (history, useful for new Fedora packages)
- The linux-surface Fedora repo regularly lags new Fedora releases (repo#9, #1578, #1735, #1888, #2139, repo#15 missing iptsd for F42) and kernel releases (#1972, #2055). CI config check broke on `CONFIG_SCSI_UFSHCD` (#2082) and on runner loss (#2143).
- Package design lessons: the running kernel was removed on update (#122), dnf protected kernels (#1163), default-kernel path/service (#1165, #1054, now kernel-surface-default-watchdog), Silverblue metadata expiry (#1197).

## Feeds into

`status.yaml` (keyboard-typecover, battery-ac, lid-wake, acpi-interrupt-storm, suspend-s0ix, touchscreen, pen, boot-secure-boot), `docs/roadmap.md`, `docs/workarounds.md` (workarounds to try).
