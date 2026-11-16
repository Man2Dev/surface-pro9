# External projects, personal repos and branches (2026-11-13)

How this was gathered: every URL in 1301 linux-surface org issues and PRs (bodies plus comments, SP9, SP8 and shared-subsystem searches) and in 308 of 319 discussions, plus the wiki, fork READMEs, fork commit messages and patch Link tags. Candidate repos were cloned shallow and read. Branches: all 85 active linux-surface forks (213 branches ahead of upstream) and 38 forks of linux-surface/kernel (79 feature branches, commits-only fetch). Tables: `data/indexes/external-repos.yaml`, `data/indexes/branches.tsv`.

## What changes the plan

1. **Initramfs module list already exists and is tested.** Universal Blue `ublue-os/hwe` ships `modules-load.d/ublue-surface.conf` for LUKS unlock with the cover: `surface_aggregator surface_aggregator_registry surface_aggregator_hub surface_hid_core 8250_dw surface_hid surface_kbd intel_lpss intel_lpss_pci pinctrl_tigerlake`. That is the evidence for the dracut-ng change (dracut today only adds `surface_aggregator_registry` and `intel_lpss_pci`). For tablet use without the cover, unl0kr (postmarketOS buffybox, arch_unl0kr) is the on-screen keyboard route; #1857 shows it needs DRM in the initramfs.
2. **SP9 lid wake has a finished patch outside the org.** dragged9698's gist "platform/surface: gpe: Tolerate padded DMI sys_vendor strings" switches DMI_SYS_VENDOR to DMI_MATCH because some SP9 firmware reports `" Microsoft Corporation"`; verified on SP9 2038 (i7-1255U), GPE 0x52. Combined with linux-surface's 0012 SP9 entry this is a complete platform-driver-x86 submission (author sign-off needed).
3. **All three SP8 cameras work in one repo, with upstreamable userspace pieces.** fildunsky/linux-surface-pro8-cameras: front OV5693, rear OV13858, IR VD55G0 (ACPI `SMO55F0`), plus six libcamera software-ISP patches and tuning tools. Upstream libcamera (mirror at 2026-11-12) has ov5693 and ov13858 sensor helpers but only `uncalibrated.yaml` for the soft ISP and no VD55G0 helper. The soft-ISP patches and SP8/SP9 tuning files are libcamera upstream candidates; SP9 uses the same sensors.
4. **VD55G0 has a vendor driver.** STMicroelectronics/vd55g0-linux-driver (GPL, device-tree based, updated 2026-07). Useful reference for the two mainline VD55G0 series.
5. **lockdown_hibernate has an identified original author.** The linux-surface 0001 patch traces to Kelvie Wong's 2022 patch (brknkfr gist), carried via kernel#158 by J. Eduardo.

## Kernel branches worth pulling into a test build

| Branch | Content | Status |
|---|---|---|
| petm5/linux `surface-devel-v7.3` | SP9 camera stack on 7.3: Lebedev VD55G0 driver + ipu-bridge entry, OV13858 config and flips, SP9 upside-down quirk, Lois Breant MIPI clock gating, int3472 extra regulators, IPU6 stream workaround, vd55g flash duty limit | best single SP9 camera branch |
| petm5/linux `vd55g0-camera-support-v2-9` | Peter Marshall's generic st-vd55g1 + VD55G0 series (latest of 10 iterations) | the series on linux-media |
| petm5/linux `sp9-cameras-6.19`, `sp9-cameras-7.0.3`, `surface-ov5693-7.2.7-1`, `surface-ov13858-7.2.7-1` | earlier SP9 camera work: ov5693 binning fix, bayer pattern on flip, mirror bits, ov13858 power management and get_selection | partly superseded by mainline 7.4 |
| petm5/linux-surface-kernel `v6.18-surface-devel-fan-ctrl` | WIP fan curve offset and fan base rpm in platform_profile | WIP |
| petm5/linux-surface-kernel `v6.18-surface-devel-battery-features` | smart charging, battery authentication status (kernel#167) | open PR |
| Cloveian/kernel `battery-charge-limit` | surface_battery charge limit support (2026-11-10) | builds on kernel#167 |
| jmmartinf/kernel `sp9-ov13858-link-freqs` | fix OVTID858 link frequency count (kernel#191) | open PR |
| jmmartinf/kernel `sp9-rear-camera-rotation` | check all DMI entries when overriding rotation (on linux-media v2) | on list |
| zR-JB/kernel `ovtid858-link-frequencies`, `mshw0040-buttons-defer`, `ssam-pos-zero-padding` | OVTID858 link freqs (kernel#174), buttons defer (now in linux-surface 0009), tabletsw zero-padded source (kernel#173, Flex Keyboard) | mixed |
| dragged9698/kernel `cameras/sp9-ov13858-hw-rotate` | ov13858 180 degree flip on SP9 (kernel#177, closed in favour of ipu-bridge) | superseded |
| loisBreant/kernel `sp9-ov5693-mipi-clock-lane-gating` | kernel#180 | superseded by 7.4 |
| CmdrShepardsPie/kernel `camera-backports-7.3`, `sam-probe-defer`, `p-h48/v7.3-surface` | Rimoli backports on 7.3, SAM defer probe, the tree behind the COPR | in COPR |
| JValdivia23/kernel `surface-ucsi-hid` | UCSI over SAM HID driver, charger power rating (kernel#184) | open PR, check on SP9 (SP9 node group has ucm_ucsi) |
| technosf/kernel `intel-thc-read-dma-72` | intel-thc-hid read DMA page count fix (kernel#185) | MTL+ only |
| wowitsjack/kernel `surface-laptop-5-s2idle-fix` | SL5 (ADL sibling) s2idle / lid fixes (PR #2011) | SL5 specific, read before reusing |

IPTS (MEI) branches (jaydens-tasty-slop, loafecho, joshuaspaulding) are for SP4 to SP7+ and do not apply to SP9.

## Patch-series fork branches with SP9 content

See `data/indexes/branches.tsv` part A (48 rows marked sp9). The most relevant: CmdrShepardsPie/linux-surface-contrib `7.3.1-pro9` (and `7.2.12-pro9`, `7.2-fixes`, `notes`), rspilk `main` and `sp8-cameras`, gattolfo98 `release/fedora-44` and `sp8-camera` (Fedora build fixes for the SP9 camera patch), PawelReich `patches/7.2-ov5693-mipi`, dixonSolutions `sp9-rear-camera-rotation`, naeemarsalan `ov5693-ipu6-sp8-front-camera`, BenediktNau `build-fedora-44-kernel-7.0` (drops the SP9 GPIO 0x10 hack now that DOVDD is upstream), RowdyRagamuffin `surface-port-7.0`, LorbusChris `arkify-copr`, orthogonaleety `f44-*`.

## Touch and pen

- iwanders/analysis-ithc-iptsd: THC analysis done on a Surface Pro 9 (Slim Pen 2 button glitch, DFT format); raw captures in its releases. The best technical background document for SP9 touch/pen.
- iptsd forks with SP9-relevant fixes not (all) upstream: AndyGozas `bundle-events-workaround` (jagged lines, #1588), wvffle stylus lift timeout (iptsd#166), LegendaryFire reconnect support and detection branches, floopflop's SL7 patch stack (touchpad oriented).

## Fedora images and packaging patterns

ublue-os/hwe (initramfs list above, rpm-ostree initramfs-etc tracking), LorbusChris/bluefin-surface (bootc images), NexGen-3D-Printing/bazzite-sdx, CmdrShepardsPie COPR, crashdummy COPR, jwrdegoede/ipu6-softisp COPR, Terra libwacom-surface, Nobara iptsd. NixOS/nixos-hardware microsoft/surface is the other distro that packages per-version patch lists and enables `CONFIG_HID_ITHC` and iptsd.

## Gone

Doridian/sb2-linux-cameras, Crashdummyy/linux-surface, Buscuit-Dev/surface-pro-10-cachyos-kernels, wowitsjack/Surface-Linux-Lid-Fix, kfechter/Linux-Surface-Copilot, thattransgal/silverblue-surface no longer resolve.
