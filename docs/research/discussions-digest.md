# Digest of the discussions that were read in full (2026-11-12, discussion 2282 rechecked 2026-11-16)

Only facts that matter for the SP9 map. Index of all scanned discussions: `data/indexes/discussions.tsv`.

## 2282 Collecting scattered SP9 fixes for upstreaming

- Goal: SP9 works on stock Fedora with no external repo, all fixes upstream (kernel, dracut, libcamera, libwacom). Scope: SP9 + Keyboard, Flex Keyboard, pen.
- Examples raised: #1221 dracut drop-in for LUKS; PR #2171 (MIPI_CTRL00 0x4800 = 0x2d) and PR #1867 (OVTI5693 HID); Plasma keyboard backlight control missing.
- Opening post: iptsd must be a hard or weak dependency of any touch-enabling package set; confirmed on SP9 (no missing patch, just the daemon).
- orthogonaleety: real development used to happen in linux-surface/kernel; recently non-maintainers patch the generated `patches/` files directly (for example #2233). Upstreaming should start from the original kernel commits and credit their authors. Example of rework need: linux-surface/kernel@da5d45c uses a `driver_info` flag bit (30 of 32 used, linux-surface's 29 collided with mainline).
- orthogonaleety fork: Fedora 44 builds on branches `f44-*`, tested on SP8, carries all upstream patches as of 6.19 forward-ported, tracks Apiznel.
- Three-state model adopted: upstreamable as is, needs rework, downstream by nature. libwacom-surface is code plus data (bus support patch), libwacom#89 stalled.
- davidbitterlich: soft fork, Bazzite 44 container builds, SP8, offers testing.
- orthogonaleety, how to read his fork: every GitHub release means built, installed and working on his SP8; the release's workflow run names the branch. Each new minor version copies the previous `patches/<ver>` dir, so a patch's history continues in the previous version's dir. Scope: all linux-surface patches as of 6.19 carried forward, Apiznel treated as upstream, no features added or dropped.
- Terra repo + `dnf swap libwacom libwacom-surface --allowerasing`; libwacom override and udev pen/touch group recipe for palm rejection (copy in `docs/workarounds.md`).
- Type Cover problems reported on an SP9: (1) delay after attaching before it works, (2) sometimes a black screen when booting without the cover until it is attached, (3) opening the cover does not wake the device, (4) power button suspend without the cover sometimes incomplete with the fan running, while closing the cover suspends fine. Mapped to known issues and fixes in `status.yaml` (keyboard-typecover, lid-wake, suspend-s0ix).
- NexGen-3D-Printing (2026-11-16): Madmaxx636/surface-companion fixes mostly work on Fedora 44 and 45; his fork NexGen-3D-Printing/SDX-Control-Centre (an rpm for Bazzite-DX that also runs on Fedora, developed and tested on an SP9) and the image NexGen-3D-Printing/bazzite-sdx carry all Surface packages, "all fully working on a SP9". He is logging and debugging the SP9 battery charge bug, present on Fedora 44 and 45 and Bazzite 45 (SP9-308). He also fixed the third-party Dexnor keyboard case (NexGen-3D-Printing/Dexnor-Keyboard-Linux), outside this repo's first-party scope.
- What those repos contain (cloned 2026-11-16): surface-companion is a desktop front end over existing interfaces (`charge_control_end_threshold`, `kbd_backlight` LEDs, lid `power/wakeup`, logind), plus a fixes catalog: an initramfs module list with `surface_aggregator_hub` (SP9-201) and an Auto-Mute Mode unit (SP9-502). SDX-Control-Centre renames it and drops the package flows for image-based Bazzite; no new hardware code. bazzite-sdx marks the SP9 confirmed with `kernel-surface` 7.2.15-1.surface.fc45 (2026-11-09); no battery work committed yet. Dexnor fixes are userspace: BlueZ applies the case's PPCP latency of 35 (dropped keys), and the touchpad latches BTN_LEFT without a release.
- Questions in the thread with no reply there: whether the OVTI5693 HID and MIPI_CTRL00 went to linux-media (answer from this repo: both are in v7.4-rc2 through Rimoli's series, see `docs/subsystems/camera.md`), whether maintainers intend to upstream, and whether a Pro 9 keyboard backlight issue exists (none found).

## 2198 Surface Pro 9 camera working on Linux Mint (femito1)

- Front OV5693 + rear OV13858 working on linux-surface 6.19.8, libcamera 0.7.1 from source. Four separate breakages out of the box.
- petm5: same fix by writing 0x20 to 0x4800 at startup. femito1: 0x2 plus any bit works.
- petm5 generalised the VD55G1 driver to the VD55G family with VD55G0 support; IR camera streaming alongside front and rear (first on SP9). Streams at width 384 px or less do not stream (IPU6 issue), temporary workaround patch in kernel#169. Links: petm5/linux compare ranges, petm5/vd55g-firmware, kernel#180, #2227.
- el-amin-dev: confirms #2171 fixes front on 6.19.8-surface-3; repo el-amin-dev/sp9-ov5693-dkms.
- loisBreant (SP9 i7-1255U, Ubuntu 24.04, 7.2.11-surface-1, libcamera 0.7.2): browser freezes come from v4l2-relayd; one-shot installer loisBreant/surface-pro-9-camera.

## 2202 Windows-like lid behaviour on SP9 (femito1)

- After unloading and reloading intel-ipu6 (for example a hibernate hook), ov5693 fails to re-probe: ipu-bridge only builds the graph on first cold probe and intel-ipu6 remove leaks the software nodes. Rear ov13858 unaffected (link-frequencies from its own _DSD). Links Rimoli's OVTI5693 patch on lore. Upstream fix later posted by D. Manresa.

## 1746 [Pro9] No touch or keyboard after 6.12.7

- Resolved by reinstall; firmware updates from Windows suggested; another user runs 6.14.3 on Nobara fine.

## 2041 input dead on SP9 (Arch)

- Cause: libwacom-surface 2.17 too old for libinput (LIBWACOM_2.18 symbol). libwacom-surface#22.

## 1734 [SP9] Thermal/Power setup to prevent throttling

- Arch + KDE: powerdevil, power-profiles-daemon, thermald, surface-control; config that stops throttling to 400 MHz.

## 1691 Nobara on SP9

- Nobara includes Surface patches; keyboard, touch, audio, brightness work out of the box.

## 1290 / 1291 SP9 sleep

- Hibernate does not wake with the power button and drains battery; Lucrtz: matches the ACPI interrupt storm, fixed by the wiki workaround.

## 1073 SP9 second display

- qzed (2023): shutdown has an in-kernel workaround now; petm5: USB-C display works.

## 1042 SP9 Fedora 37 touch

- Old ITHC DKMS route; StollD: install `kernel-surface-devel`; module signing needed with Secure Boot.

## 1366 Unable to install Linux on SP9

- USB boot issues caused by firmware; disable Secured-core; Microsoft-only CA vs third-party CA.

## 1462 SP9 kernel 6.8.8 keyboard ghosting (Kubuntu)

## Upstream status threads: 2012, 1581, 1441, 1687, 1305, 796, 1618, 1731

- qzed (1581): biggest non-upstream parts are touchscreen and cameras. quo: upstream THC driver only MTL and up (quo/ithc-linux#29).
- qzed (1441): keyboard and touchpad of SLS1 upstream since 5.16; SAM support is generally upstream.
- StollD (1305): IPTS, ITHC, SPI-HID needed across models.
- andy-shev (1731): one camera patch obsolete since 6.14.

## SP8 sibling threads: 1899, 1610, 1373, 981, 1157, 1132, 1093, 1288, 1649, 1646

- 1157: qzed: SP8 lacked a libwacom tablet file (libwacom-surface#13). 981: missing surface_hid and SERIAL_DEV_BUS=y on a custom kernel. 1132: freezes fixed with split_lock_detect=off. 1899: SP8 camera upside down on 6.17.1.

## Fedora and distro images: 2296, 1889, 2089, 2184, 2374, 2368

- f43/f44 repo 404 reports (now f44 exists). 2089: build-ark.py and per-arch config issues (#2082). Silverblue image (thattransgal), Bazzite-SDX (NexGen-3D-Printing), Surface Companion app (Madmaxx636).

## 2253 Surface Pro 7+ all three cameras (dmanresa-saes)

- IPU6 PSYS hardware ISP with Microsoft's .aiqb calibration; repo dmanresa-saes/surface-ipu6-cameras; intel/ipu6-camera-hal#182; relevant method for SP9 OV5693.
