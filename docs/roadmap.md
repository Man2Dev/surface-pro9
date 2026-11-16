# Roadmap: SP9 on stock Fedora via upstream

Ordered by value per effort. Each item names the evidence and the upstream target. Status lives in `status.yaml` and the matching issue in `issues/`; when an item is done, update both in the same commit.

## Phase 0: baseline on a real SP9 (do first, SP9-901)

Run the commands in `docs/testing.md` on the stock Fedora kernel and, if available, kernel-surface. Post the results publicly and link them from the matching issues. They answer: the DMI vendor string with or without a leading space (#2257), which initramfs modules are present, whether the stock shim and GRUB boot with Secure Boot on and current firmware (NX freeze, #1162, linux-surface 0001), and the `needs-test` issues.

## Phase 1: daily-driver kernel on Fedora 44 (short term, downstream is fine)

1. Start from CmdrShepardsPie/surface-kernel-copr (linux-surface 7.3.1 + 20 SP9 fixes) or build locally: kernel-ark `kernel-7.3.x-0` + `patches/7.3` from CmdrShepardsPie/linux-surface-contrib `7.3.1-pro9` via `pkg/fedora/kernel-surface/build-linux-surface.py`.
2. Add on top, as needed for testing: kernel#169 (VD55G0, petm5), #2252 binned OV5693 mode (needed even on 7.4, see dmanresa-saes/surface-ipu6-cameras#1), D. Manresa ipu-bridge rebind v3, Ramon Miranda keyboard backlight patch, surface-gpe#7 vendor match.
3. Userspace: iptsd (linux-surface repo, Terra or Nobara), libwacom-surface via Terra, libcamera.
4. When kernel-ark moves to 7.4: drop superseded camera commits (see `data/indexes/patches-linux-surface-7.3.md`, class `superseded`) and rerun `tools/upstream_check.py` against 7.4.
5. Alternative that keeps the stock Fedora kernel: build quo/ithc-linux out of tree against kernel-devel and sign it with a MOK, as John-S-Reddick/bazzite-surface does for Bazzite; add iptsd. Cameras stay broken until 7.4 plus the binned-mode patch.
6. Known closed-issue traps to check first (`docs/research/closed-issues.md`): `pinctrl_tigerlake` must load before the SAM and button drivers (#1645, #1392); `pci=hpiosize=0` can cost lid wake (#1082), so test lid wake with and without it; UEFI battery limit or Windows smart charging when the battery stops at 50 % (#1781); `[DFT] ButtonMinMag = 20000` for Slim Pen 2 phantom buttons if iptsd 3.x's `Mpp2ButtonMinMag` is not enough (#1233).
7. Test the orphaned ITHC suspend/resume fix from closed linux-surface#2210 (`orphaned-patches/`) against touch dying after sleep; if it holds, offer it to quo/ithc-linux with the author's agreement.

## Phase 2: upstream quick wins (small, self-contained, clear owner)

| # | Change (issue) | Target list | Author to ask | Evidence |
|---|---|---|---|---|
| 1 | surface_gpe: add SP9 (all SKUs incl. Business, tolerant vendor match) (SP9-301) | platform-driver-x86 (Maximilian Luz, Hans de Goede, Ilpo Jarvinen) | Maximilian Luz (original 0012), 777HOST (surface-gpe#7), Lucrtz (surface-gpe#5), dragged9698 (gist with the DMI_MATCH vendor patch, tested on SP9 2038), Meatwo310 (Business SKU `Surface_Pro_9_for_Business_2038`, tested); base it on Maximilian Luz's SP9 + SL5 version in open linux-surface#2011 | #2257, #1919, #1910, bugzilla.kernel.org 218923 (ACPI storm with surface_gpe), `data/indexes/external-repos.yaml` |
| 2 | ALSA hda/realtek: limit internal mic gain on SP9 (SP9-501) | linux-sound / alsa-devel (Takashi Iwai) | Chris Simpson (CmdrShepardsPie) | fork 0016-sound |
| 3 | dracut: add `surface_aggregator_hub` next to `surface_aggregator_registry` in 70kernel-modules (everything else is already installed: =drivers/hid, =drivers/tty/serial, =drivers/pinctrl, intel_lpss_pci; precedent dracut 8cc89664 by Benjamin Drung). Check `lsinitrd` on the SP9 first (SP9-201) | dracut-ng/dracut (GitHub, renamed from dracut-ng/dracut-ng; no Surface issue or PR exists yet) | n/a | #1221, #1828, discussion 2024, ublue-os/hwe `ublue-surface.conf` (field-tested list in a shipping Fedora image), Omarchy mkinitcpio drop-in (same list) |
| 4 | ~~soc_button_array defer probe~~: done upstream by ed22ad5fdbdb (7.3, stable 7.2.8+), verified on SP9. Only ask linux-surface to drop 0009 (SP9-205) | n/a | n/a | #1392 (2026-10-25) |
| 5 | surface_battery: report not charging while idle on AC (related: SP9-308) | platform-driver-x86 / linux-pm | Chris Simpson | fork 0007 |
| 6 | Tested-by on pending series: EPROBE_DEFER v2 (Wu Enqiang), fan standby (Peter Marshall), keyboard backlight 045E:09AE (Ramon Miranda), battery event 0x1a, ipu-bridge rebind (D. Manresa), ov5693 fixes (Ziliani, Kruse), ov13858 series (Lebedev, Neacsu), VD55G0 (Marshall or Lebedev), SP8 upside-down (Emfox Zhou) | various | n/a | `data/indexes/upstream-submissions.tsv` |
| 7 | surface_battery: charge limit, smart charging, authentication status (SP9-309) | platform-driver-x86 | Cloveian (`battery-charge-limit`), Peter Marshall (`v6.18-surface-devel-battery-features`, kernel#167) | `data/indexes/branches.tsv` part B |
| 8 | libcamera: Tested-by from an SP9 on Emfox Zhou's 'ipa: softisp: Add tuning data for the ov13858 and ov5693' v3 (series 6354, 2026-11-13) and on Hans de Goede's 'simple: Do not alloc CMA DMA-buffers for camss and ipu6/7' (SP9-402) | libcamera-devel | n/a | `data/indexes/trackers.tsv` |
| 9 | ov5693 binned 1296x972 mode on IPU6 (needed for SP9 front camera even on 7.4) (SP9-401) | linux-media | Simon Kruse has D. Manresa's go-ahead to send it, rebased on Rimoli's clock-lane gate (dmanresa-saes/surface-ipu6-cameras#1, 2026-10-27); give an SP9 Tested-by when it is posted | #2234, #2252 |
| 10 | iptsd: review and test on SP9, then ask for merge: #219 (service stops after cold boot), #221, #224 (udev), #214, #233 (Slim Pen 2), #234/#235 (touch detection). All merge cleanly, none has a maintainer reply. Needed anyway for a solid Fedora iptsd package. (SP9-105, SP9-106, SP9-108) | linux-surface/iptsd | the PR authors | `data/indexes/open-prs.tsv` |
| 11 | iio-sensor-proxy: set hysteresis 0 for the SP9 sensor hub (or a hwdb property), so polling does not block for 5 s per read (SP9-206) | freedesktop GitLab hadess/iio-sensor-proxy#432 | CmdrShepardsPie (analysis and udev rule in #2160) | #2160 |
| 12 | surface_hid: return -ENODEV instead of -EPROTO when a node (the SP9 pen stash 01:15:02:02:00) returns an empty descriptor; check whether it removes the 2 min boot stall (SP9-203) | linux-input / platform-driver-x86 (Maximilian Luz) | qzed suggested it in #1845 | #1845 |
| 13 | surface platform_profile: clear the fan floor Windows leaves (SAM FAN 0x0b SetMinFanRpm 0) at probe (SP9-310) | platform-driver-x86 | Cloveian, petm5 | #1726 |
| 14 | surface_aggregator: retry event source enable after hibernate restore when the EC times out (-110) (SP9-307) | platform-driver-x86 | pentop (tested patch in #2294) | #2294 |
| 15 | s2idle on ADL-P: test the SOF D0 lead (snd_intel_dspcfg.dsp_driver=1, #1010) and the INTC1055 PADCFG0 lead (kernel#162) on SP9; report to SOF or Intel pinctrl with data (SP9-302) | thesofproject / linux-gpio | User25665, wowitsjack | #1010, kernel#162 |
| 16 | hid-sensor-trigger: power the sensor back on after a system suspend that started inside the autosuspend window (runtime PM left 'active') (SP9-207) | linux-iio (Jiri Kosina, Srinivas Pandruvada) | CmdrShepardsPie traced it (#2160) | #2160 |
| 17 | HID: surface-hid keyboard backlight (045E:09AE, which is the SP9 cover): Tested-by on Ramon Jesus Miranda's patch (SP9-204) | platform-driver-x86 | n/a | SP9 HID ids in status.yaml device |
| 18 | Hibernate with Secure Boot: test and review the lockdown hibernation series (Garrett signed images, Rhodes encrypted snapshot) instead of carrying linux-surface 0001 (SP9-306) | linux-pm / LSM | n/a | `docs/research/upstream-efforts.md` |
| 19 | libwacom: ask Peter Hutterer how IPTS/ITHC (BUS_VIRTUAL via iptsd uinput) and THC QuickSPI (BUS_SPI) Surfaces should be described, before sending SP9 data; earlier MEI attempts failed on the out-of-tree bus (SP9-111) | linuxwacom/libwacom | qzed (libwacom#92 history) | libwacom#89, #92, #400 |
| 20 | Fedora iptsd package review: all deps are in rawhide, no bundling (SP9-102) | Fedora package review | n/a | `status.yaml` fedora.iptsd_packaging |

## Phase 3: Fedora packaging

1. iptsd: new Fedora package review (spec base: linux-surface/iptsd `iptsd.spec`). Check bundled subprojects vs system libs (CLI11, Microsoft.GSL, spdlog, fmt, inih, eigen3).
2. libwacom: revive linuxwacom/libwacom#89. Try the UINPUT_DEVICE/UINPUT_SUBSYSTEM udev tagging route from iptsd so no BUS_VIRTUAL patch is needed; then send the SP9 data file (Stylus=true, Styli list, real size).
3. libcamera: confirm Fedora's build enables the software ISP / simple pipeline for IPU6. Upstream has ov5693 and ov13858 camera sensor helpers but only `uncalibrated.yaml` for the soft ISP and no VD55G0 helper. Candidates to send to libcamera-devel: the six soft-ISP patches and the tuning files from fildunsky/linux-surface-pro8-cameras (same sensors as SP9), loisBreant's debayer_egl patch. Ask the authors first.
4. Weak dependency or documentation so touch is complete when the ITHC driver is present.
5. Kernel backports in Fedora: once an SP9 fix is accepted in a maintainer tree, open a kernel-ark merge request (or ask Kate Hsuan / Hans de Goede) for the Fedora branch, as done for Dell's ipu-bridge upside-down quirk (ark !4395) and int3472 (!4757).
6. ITHC as an out-of-tree kmod/akmod (RPM Fusion or Terra) until it is upstream; bazzite-surface shows the build and signing steps.
7. Speakers: the Windows Surface APO voicing for the SP9 (ALC274, subsystem 10EC1284) converts to a PipeWire filter-chain (antoinecellerier/speaker-tuning-to-easyeffects); decide whether that belongs in a Fedora package or stays opt-in.

## Phase 4: hard items (need design discussion)

1. Touch (SP9-101): ITHC upstream path. Options: submit ITHC to linux-input, or extend intel-thc-hid (Even Xu, Xinpeng Sun) to ADL-P plus the Surface (IPTS-style) mode. Ask quo first (quo/ithc-linux#29). Also the intel-iommu source-id quirk.
2. Shutdown (SP9-305): root cause of EFI ResetSystem returning (#1058); propose the DMI-gated PCI quirk on linux-pci or an x86 reboot quirk.
3. ACPI interrupt storm (SP9-303) and `pci=hpiosize=0` (#1082, #1058): find what the I/O window change fixes, and why it can stop lid wake (2025-10 SP9 report in #1082).
4. Hibernate with lockdown (SP9-306; linux-surface 0001, originally by Kelvie Wong 2022): probably stays downstream.
5. Typecover hid-multitouch patches: SP9 uses SAM KIP, so not needed for SP9; leave to others.
6. Fan control: curve offset and base rpm (petm5/linux-surface-kernel `v6.18-surface-devel-fan-ctrl`, WIP) after the fan standby series lands.
7. IR camera (SP9-404): pick one VD55G0 series with the media maintainers; use STMicroelectronics/vd55g0-linux-driver and fildunsky's working SP8 setup as references.

## Issue triage (cheap, SP9-902)

17 open SP9 issues are already fixed (list in `docs/research/open-issues.md`). A comment with the fixing commit on each lets danielzgtg (Triage role since 2026-10) close them, which makes the real SP9 problems easier to find.

## Wiki fixes (cheap, visible, no review queue, SP9-904)

The linux-surface wiki is editable by any GitHub user and maintainers ask contributors to update it (danielzgtg in #2252). Pages that are wrong or out of date for the SP9 are listed at the end of `docs/research/wiki-digest.md`: support table, camera table, the Disk-Encryption module list (Pro 8/9 missing, Fedora example incomplete), the SL5 pinctrl module name, and the SP9 page (initramfs-tools steps under a mkinitcpio heading, lid wake and iptsd start-up missing).

## Ask on the discussion thread (2282)

- qzed / StollD: are surface_gpe SP9 and the PCI shutdown quirk intended for upstream, any known blocker?
- quo: ITHC upstream intent and the THC ADL story.
- Chris Simpson: OK to send mic gain and battery patches with his authorship?
- dragged9698: OK to send the surface_gpe vendor match patch with a real Signed-off-by?
- fildunsky: plan to send the libcamera soft-ISP patches and SP8 tuning upstream?
- RowdyRagamuffin: still working on the ITHC suspend/resume fix from closed #2210? (test it on SP9 first; orphaned-patches/)
- Cloveian: open the charge limit PR qzed asked for in kernel#167?
- cunninghamcard-bit: OK to resubmit iptsd#227 with your authorship after testing on SP9?
- Emfox Zhou: SP9 Windows AIQB differs from the SP8 one? (his tuning is from the SP8 driver package).
- CmdrShepardsPie: will you post the iio-sensor-proxy hysteresis change on #432, or may someone post it with your data and credit?
- pentop: plan to send the SAM restore retry upstream?
- Cloveian: send the FAN 0x0b reset with the charge limit work?
- NexGen-3D-Printing: post the SP9 battery charge logs and findings on #2232 (SP9-308)?
- Meatwo310: OK to fold the Business SKU into the upstream surface_gpe patch with a Tested-by?
