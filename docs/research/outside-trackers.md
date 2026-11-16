# Outside the org: trackers, distro kernels, other projects (2026-11-13)

Second pass after `external-projects.md`. Sources: Red Hat Bugzilla, kernel Bugzilla, Launchpad, Fedora Discussion, kernel-ark merge requests, libcamera patchwork, GitHub repository and issue search outside `linux-surface` (title phrases, SKU strings, project-scoped queries in libwacom, dracut, iptsd, ithc-linux, thermald, fwupd, systemd, nixos-hardware), ArchWiki. 36 new repos were cloned and read (`tools/inspect_repos.py`). Tables: `data/indexes/trackers.tsv`, new entries in `data/indexes/external-repos.yaml`. Method: `tools/browser/README.md`.

## What changes the plan

1. **The SP9 front camera is not fixed by 7.4 alone.** An SP9 test on media next (Rimoli's series included): libcamera picks binned 1296x972 plus both flips, and that mode with flips gives csi2 frame sync errors, so the camera returns empty buffers (dmanresa-saes/surface-ipu6-cameras#1). The ov5693 binned-mode patch from #2252 has to go to linux-media as well.
2. **libcamera tuning for the SP9 sensors is on the list today.** Emfox Zhou posted "ipa: softisp: Add tuning data for the ov13858 and ov5693" v3 on 2026-11-13 (AWB, colour matrices and lens shading from the SP8 Windows AIQB). libcamera chooses the file by sensor name, so it lands on the SP9 too. A Tested-by from an SP9 is the easiest useful contribution. OV5693 black levels are already accepted; Hans de Goede's "do not alloc CMA DMA-buffers for camss and ipu6/7" is also pending.
3. **Fedora's kernel takes camera backports.** kernel-ark merge requests by Kate Hsuan (hpa1) and Hans de Goede carry ipu-bridge and int3472 fixes ahead of mainline, including an upside-down DMI quirk for Dell (ark !4395) and an int3472 fix restored after it was dropped (rhbz#2539811, ark !4757). Same route for SP9 quirks once a maintainer accepts them.
4. **A stock Fedora-derived kernel needs only ITHC for touch.** John-S-Reddick/bazzite-surface keeps Bazzite's kernel and adds an out-of-tree ithc.ko (quo/ithc-linux, MOK signed), iptsd and a tablet file; its README lists cover, battery, tablet switch, profiles, Wi-Fi, BT, audio and suspend as working on that kernel. That makes an ITHC kmod/akmod package (RPM Fusion or Terra) a realistic interim step. Intel's own out-of-tree THC drivers still exclude ADL and leave IPTS mode to linux-surface.
5. **Terra already ships iptsd and kernel-surface** for f43 to f45 and el10 (terrapkg/packages#16814, #17551).
6. **Third distro with the same initramfs list.** Omarchy (Arch, mkinitcpio) uses the ublue-os/hwe list minus intel_lpss. dracut-ng moved to `dracut-ng/dracut` and has no Surface issue or PR yet, so the dracut change is unclaimed.
7. **surface_gpe upstream submission has two more inputs.** The SP9 Business SKU string is `Surface_Pro_9_for_Business_2038` (Meatwo310/dotnix PR #13, tested). bugzilla.kernel.org 218923 reports an ACPI error storm and failed later suspends on an SP9 with surface_gpe loaded; have an answer for it when posting.
8. **Speakers can sound like Windows.** antoinecellerier/speaker-tuning-to-easyeffects converts the SP9's Windows Surface APO voicing (ALC274, subsystem 10EC1284) to a PipeWire filter-chain or EasyEffects preset; an SP9 user confirmed it (#113).
9. **IR camera recipe confirmed elsewhere.** rhbz#2509956: the mainline vd55g1 driver streamed on a ThinkPad after an ACPI match, an ipu-bridge entry and an int3472 vana mapping. The SP9 VD55G0 needs the same three pieces plus the type 0x02 LED GPIO (rhbz#2516222, #2468035 show that GPIO type on Dell too).
10. **Same soc_button_array bug on another vendor.** Framework Laptop 12 (rhbz#2488614) has the silent, never retried probe failure fixed for the SP9 by linux-surface 0009; mainline ed22ad5fdbdb (7.3, stable 7.2.8+) now fixes it for both.

## Smaller items

- KWin shows the mouse cursor while the pen hovers (rhbz#2524606, SP7+, patch attached): applies to SP9 with iptsd; upstream target KDE.
- libwacom aborted in `bus_to_str` on a Surface with stock F44 (rhbz#2463712), fixed in libwacom 2.18.0-2; keep that path in mind for any virtual bus proposal.
- SP9 sysinfo is already in linuxwacom/wacom-hid-descriptors (#490).
- thermald: `--adaptive` fails on SP9 (no DPTF tables); iwanders/nixos-surface has a hand-written thermal-conf.xml; intel/thermal_daemon#616 (Surface Book 3) explains why passive trips make PL1 saw.
- Display: PSR off (NixOS/nixos-hardware#941), VRR page flip errors on fullscreen (pop-os/cosmic-comp#1372), some users on xe (`xe.force_probe=46a8`).
- Secure Boot with own keys via sbctl works and does not brick (ArchWiki Microsoft_Surface_Pro_9, which also lists PCI IDs).
- UEFI downgrade 12.200.143 to 9.12.143 is possible with a repacked cab (plover43/sp9_downgrade); risky.
- Userspace workaround seen in the wild for the button race: `softdep soc_button_array pre: pinctrl_tigerlake` in modprobe.d (zeroxoneafour/linux-surface-config).

## Searched with nothing for the SP9

Launchpad (11 hits, older Surfaces), fwupd, dracut, Fedora Discussion (tag microsoft-surface: 9 topics, none SP9), linux-hardware.org (page did not render in the browser).
