# Upstream efforts: what landed, what is moving, what stalled, what failed (2026-11-14)

This pass looked at upstream itself rather than at linux-surface:
- the mainline history of the Surface drivers;
- every relevant patchwork project;
- the upstream trees of dracut, libwacom, systemd hwdb, fwupd and thermald (cloned and read);
- GitHub issues and PRs in those projects and in Intel's and SOF's repos;
- the libcamera patchwork;
- repology, Fedora package metadata and Red Hat Bugzilla.

Row-by-row table: `data/indexes/upstream-efforts.tsv` (58 efforts: 21 landed, 1 accepted, 13 pending, 6 stale, 4 failed, 11 never sent).

Not reachable: freedesktop GitLab (libinput, iio-sensor-proxy, libcamera git), Reddit. The libinput quirk state comes from an installed copy of its quirk files.

## The overall picture

1. **The kernel side splits in two.**
   - Everything Maximilian Luz sent upstream landed: the SAM core, the registry, KIP hub, HID transport, the SP9 node group (2022-11), the SP9 tablet switch (2023-03) and SP9 thermal sensors (2024-03).
   - His last upstream registry work was 2024-08. New models since then come from other people (Dale Whinham, Lukas Hetzenecker, Harrison Vanderbyl, Gopikrishna Garmidi, Jerome de Bretagne), so outside contributors get Surface patches merged without trouble.
   - What he kept downstream for the SP9 was never posted: the surface_gpe SP9/SL5 entry and the PCI no-shutdown quirk. He did send gpe entries for the SL3 15", SLS, SP8 and SL4 13" in 2020 to 2022, so the SP9 gpe patch follows an accepted pattern.
2. **Cameras are the success story of 2026.**
   - Rimoli, Lebedev, Sakari Ailus, Hans de Goede, Nenciarini and Jakob Berg moved the SP9 camera path into mainline 7.4 within three months.
   - What remains: Manresa's binned-mode patch (Simon Kruse has agreed to send it), the ov13858 and VD55G0 series, and the libcamera tuning.
   - linux-media patchwork shows merged patches as "new", so check the media tree, not the patchwork state.
3. **Touch has never been sent anywhere.**
   - No IPTS or ITHC patch has ever reached linux-input.
   - Intel's intel-thc-hid (Even Xu, mainline 6.14) covers Meteor Lake and newer only.
   - quo, who wrote ITHC, will not upstream under a pseudonym. Someone else has to carry ITHC, or merge its legacy mode into intel-thc-hid (`ithc-legacy.c`; the SP9 runs legacy mode).
   - Intel's out-of-tree thc-drivers repo has an unanswered Surface report (intel/thc-drivers#1).
4. **libwacom refused twice, for a clear reason.**
   - qzed's MEI bus and IPTS data (#92, #93, 2019) were closed by him after Peter Hutterer said he would not take buses that only exist with out-of-tree code; the bus id would first have to be in `linux/input.h`.
   - kasperk81's retry (#400, 2021) was closed for no reply, and the tracking issue #89 was mass-closed in 2022.
   - Upstream today accepts only usb, serial, bluetooth and i2c. It has a `UINPUT_DEVICE`/`UINPUT_SUBSYSTEM` override, but that only maps to those four buses.
   - The only Surface tablets in upstream are the Go and Go 2, which have real I2C Wacom digitizers.
   - So an SP9 entry needs either a bus libwacom accepts or a different approach (iptsd tagging its uinput devices). Newer Surfaces on intel-thc-hid will show up on SPI, which libwacom does not know either. That is a gap to raise once, for all Surfaces.
5. **dracut is closer than the KB said.** The dracut master was read:
   - `70kernel-modules` installs `=drivers/hid`, `=drivers/tty/serial`, `=drivers/pinctrl`, `intel_lpss_pci` and `surface_aggregator_registry`.
   - The last was added by Benjamin Drung (Canonical) in 2023 for the Surface Laptop 4 keyboard.
   - In dracut's default mode (`hostonly_mode` sloppy, Fedora's default) these go in regardless of the host, so `surface_hid`, `surface_hid_core`, `8250_dw`, `8250_lpss` and `pinctrl_tigerlake` are already in a Fedora initramfs.
   - The one module missing for the SP8 and SP9 covers is `surface_aggregator_hub`, the KIP hub that the keyboard and touchpad hang off.
   - That makes the dracut PR a one-word change, citing Drung's commit as precedent. Confirm with `lsinitrd | grep -E 'surface|8250|pinctrl'` on an SP9 first (SP9-901).
   - The SAM probe race that also broke the cover at LUKS (#2039, #2219) is fixed upstream by Wu Enqiang's accepted patch.
6. **Hibernate under Secure Boot has a real upstream route now.**
   - Kelvie Wong's `lockdown_hibernate` RFC (2023-11, carried as linux-surface 0001) got no follow-up.
   - In 2026 there are three active proposals: Matthew Garrett's signed hibernation images (changes requested, 2026-10), Sean Rhodes' encrypted snapshot device (v3 resend, 2026-09) and a TPM2 image encryption RFC.
   - Following those is better than reviving 0001.

## Smaller findings

- **systemd hwdb.**
  - USB Type Covers (045E:09C0) were marked as internal touchpads in 2026-08 (systemd#43262).
  - SL2/SL3 touchpads have resolution fixes in `60-evdev.hwdb`. The SL3 entry matches `045E:09AF`, the same id as the SP9 touchpad, but only on `pnSurfaceLaptop3`. If the SP9 touchpad reports a wrong resolution, an SP9 line goes there.
  - There is no Surface accelerometer mount matrix entry.
- **libinput.** Its Microsoft quirk already tags `Microsoft Surface ... Keyboard` and `... Cover` as internal, which covers the SP9 cover. Nothing to send.
- **fwupd.**
  - It has a Microsoft CFU plugin with a `surface` version format, used for the USB-C Travel Hub (045E:09BC).
  - The SP9 cover exposes a SAM HID firmware update node (01:15:02:05, 045E:0991 or 09CF). Nothing in fwupd talks to it.
  - UEFI capsules for the SP9 still need the linux-surface repack scripts (surface-uefi-firmware, with its own open bugs #48 and #51).
- **Audio.**
  - No SP9 mic gain patch was ever posted to alsa-devel.
  - In thesofproject/linux#5509 (SP8), the SOF developer says the SP8 has no DMIC and should use legacy HDA. The fix there was lowering `Internal Mic Boost`, the same symptom as the SP9 mic gain quirk in CmdrShepardsPie's fork.
  - alsa-ucm-conf has Surface profiles only for the ARM models.
- **thermald** blacklists a zone named `Surface` and ships no Surface configs. intel/thermal_daemon#616 (SB3, PL1 control with thermal-conf.xml) is open and unanswered.
- **libcamera.**
  - Black levels for OV5693 landed (2026-07).
  - Emfox Zhou's tuning v3 has no replies.
  - Javier Tia's AIQB parser for IPU6 tuning stalled after changes were requested (2026-05). It would let Surface Windows tuning be converted in tree.
  - Armin Felder's OV08x40 tuning has waited since 2026-09, so expect slow review for tuning files.
- **Packaging.**
  - iptsd is packaged only in AUR, nixpkgs, Solus and Terra; libwacom-surface only in AUR, nixpkgs and Terra (repology).
  - Red Hat Bugzilla has no review request for either.
  - Every iptsd build dependency exists in Fedora rawhide: cli11-devel, eigen3-devel 5.0.1 (the version iptsd's wrap pins), fmt-devel, inih-cpp, guidelines-support-library-devel, spdlog-devel, plus sdl2-compat and cairomm for the optional tools. So a Fedora package needs no bundling.
  - Fedora rawhide ships iio-sensor-proxy 3.9, the version that hangs on the SP9 sensors (#2160).
- **Fedora kernel bug.** rhbz#2419833 (2025-12, NEW) is an abrt report of a WARNING in `surface/aggregator/controller.c` on a stock Fedora kernel. Worth reading before sending SAM patches.
- **Universal Blue.** The Surface images in ublue-os/hwe show signs of neglect: an unanswered "can't rebase to surface images" issue since 2024-02, and an F41 surface kernel-cache PR open since 2024-10. Bazzite users report the Surface kernel conflicting with its own kernel (bazzite#5112, #5476). The downstream Fedora variants do not replace upstreaming.

## What this changes in the plan

- Roadmap row 3 (dracut) shrinks to adding `surface_aggregator_hub`.
- New concrete targets:
  - an SP9 Tested-by on the keyboard backlight patch;
  - following the lockdown hibernation series instead of carrying 0001;
  - raising the libwacom bus question for IPTS/ITHC and THC/SPI devices once, with Peter Hutterer, before writing data files.
- Unchanged and still never sent: surface_gpe SP9, the PCI shutdown quirk, the ALC274 mic gain quirk, the surface_hid pen stash fix, the hid-sensor-trigger resume fix. These are the cleanest first patches.

## ITHC upstream path (quo/ithc-linux, 2026-11-14)

All 34 issues and PRs listed, key threads read.

- #26 (SP9, EFI stub `invalid dma rx data`): quo saw THC register 0x1128 bit 5 set only on working boots and committed 18afc6f in 2024-04 as a likely fix. linux-surface #1078, the same bug, is still open.
- #29: Intel's QuickSPI driver (intel-thc-hid, mainline since 6.14) covers MTL and newer. quo: ADL QuickSPI support would be easy, but older devices need `ithc-legacy.c` merged in. The SP9 runs its THC in legacy mode (`no ACPI config, using legacy mode`, #2367).
- #7: quo will not upstream under a pseudonym, so someone else has to carry ITHC or the legacy merge.
- PR #33 (SLS2, 2026): quo's review says real error recovery needs a full re-init (`devres_release_group()` and `ithc_start()`) with proper locking. That is the bar for any upstream version.
- #34: the Surface Laptop 5 (same 8086:51d0) gets zero touch events on Fedora 44; unanswered.

## Recheck of submission states (2026-11-14)

Every patchwork row since 2026-07 was rechecked by msgid: no state changed since 2026-11-12. Wu Enqiang's EPROBE_DEFER v2 is accepted in platform-driver-x86. The fan standby series is still changes-requested. Keyboard backlight and battery event 0x1a are still new. Only one new Surface patch has appeared since 2026-11-11: Antoine Pichot's ipu-bridge rotation quirk for the SB2 and SP7+ (sibling). linux-media rows stay "new" in patchwork even after merging, so mainline is the reference for camera patches.

## People and trees (2026-11-14)

- **D. Manresa's ov5693 binned-mode patch.** Simon Kruse has Manresa's go-ahead to send it upstream with Manresa's authorship (dmanresa-saes/surface-ipu6-cameras#1). He must rebase it on Rimoli's clock-lane gate first. It was not on linux-media as of 2026-11-13.
- **linux-surface/kernel merges on 2026-11-09:**
  - fan power state (#166)
  - ov5693 gain (#168)
  - SP9 rear camera rotation (#170)
  - SP12 registry (#171)
  - soc_button_array defer (#172), now redundant with mainline
- **Still open:** CmdrShepardsPie's 7.3 camera backport (#193), UCSI over SAM HID (#184).
- **libcamera tuning v3** (Emfox Zhou, series 6354): no replies yet.
