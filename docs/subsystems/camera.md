# Cameras (IPU6: OV5693 front, OV13858 rear, VD55G0 IR)

Status keys: `status.yaml` features `camera-front`, `camera-rear`, `camera-ir`.

## Hardware path

- ISP: Intel IPU6 (`intel-ipu6`, `intel-ipu6-isys` in mainline). Image processing in userspace: libcamera simple pipeline with the software ISP. No Intel HAL needed.
- Sensor discovery: `ipu-bridge` builds the software-node graph from ACPI SSDB data. Power, reset, clocks and LEDs come from the `INT3472` discrete PMIC driver (`drivers/platform/x86/intel/int3472/discrete.c`).
- SP9 ACPI quirks: SSDB reports rotation 0 although both modules are mounted upside down; the front sensor has the `OVTI5693` HID (older Surfaces use `INT33BE`); one INT3472 GPIO is type 0x08 (`INT3472_GPIO_TYPE_POWER1`).

## What mainline v7.4-rc2 already has (checked in source)

| Piece | Where | Origin |
|---|---|---|
| `OVTI5693` in ov5693 ACPI match | `drivers/media/i2c/ov5693.c` | Fernando Rimoli, "media: ov5693: add OVTI5693 ACPI HID for IPU6 Surface devices" (linux-media 2026-07-08) |
| MIPI clock lane gating for non-continuous clock (`OV5693_MIPI_CTRL00_REG` 0x4800) | ov5693.c | Rimoli series "Enable the OV5693 front camera on IPU6 Surface devices" v3 (2026-09-02); same fix as PR #2171 / Arsalan Naeem, rspilk, PawelReich forks |
| `IPU_SENSOR_CONFIG_MATCH_FL(... ipu6_ov5693_ncont_clk ...)` for OVTI5693 and INT33BE | `drivers/media/pci/intel/ipu-bridge.c` | Rimoli series |
| `OVTID858` sensor config with link frequencies 540 and 270 MHz | ipu-bridge.c | Sergey Lebedev "ipu-bridge: Add OV13858 sensor config" v3 |
| SP9 front `OVTI5693` and rear `OVTID858` in `upside_down_sensor_dmi_ids` | ipu-bridge.c | Rimoli "Add upside-down sensor quirks for the Surface Pro 9" (2026-09-15), linux-surface kernel#170 (jmmartinf) and kernel#160 (gabrielstedman) are the downstream equivalents |
| ov13858 horizontal and vertical flip controls | `drivers/media/i2c/ov13858.c` | Sergey Lebedev v4 |
| `INT3472_GPIO_TYPE_POWER1` (0x08), DOVDD (0x10) handling | int3472 | Jakob Berg Jespersen POWER1 v3, Leif Skunberg DOVDD |
| `ipu_bridge_get_ipu6()` | ipu-bridge | Sakari Ailus |

Not in mainline: SP8 front rotation quirk (Emfox Zhou v2 on list 2026-11-12), VD55G0 driver, ipu-bridge rebind fix, ov5693 mode/flip/autosuspend fixes, ov13858 regulator/clock/reset handling.

Consequence for linux-surface 7.3 `0013-cameras.patch`: the "Add camera support for Surface Pro 9" (PR #1867), "front camera rotation quirks for Surface Pro 8 and 9" and "fix rear camera rotation on Surface Pro 9" commits are superseded on 7.4 (except the SP8 entry). `tools/upstream_check.py` shows them as partial/diverged against 7.4-rc2 for exactly that reason. Note PR #1867 declares `IPU_SENSOR_CONFIG("OVTID858", 4, 540000000)`, a link-frequency count of 4 with one frequency; kernel#191 fixes that.

## Open problems and where they are tracked

- Binned 1296x972 OV5693 mode returns no frames on IPU6: #2234, fix in #2252 (dmanresa-saes), verified on Pro 7+, Pro 8, Go 4.
- Front sensor fails to re-probe after intel-ipu6 unload or hibernate (software nodes leaked): discussion 2202, upstream fix "ipu-bridge: survive module unload and reuse the software nodes on rebind" (D. Manresa v3, 2026-10-26).
- ov5693 mode changes, flips, autosuspend: Marco Ziliani v2 (2026-10-29); "Use sub-device active state" and "Support control events" (Simon Kruse).
- ov13858 probe failure on link-frequency check: #1753, kernel#174, kernel#191.
- Browser freezes come from v4l2-relayd, not the camera (loisBreant, discussion 2198 comment 10).
- IPU6 creates many V4L2 nodes; WebRTC stops at 64 devices: #2242.
- IR camera VD55G0: kernel#169 (petm5), two upstream series (Peter Marshall genericize st-vd55g1 + VD55G0, Sergey Lebedev VD55G0 v2), vd55g1 fixes (Rimoli v3, George Neacsu, Jizhou Tong). IR flood LED: int3472 GPIO type 0x02 (Marco Nenciarini v8). Firmware: petm5/vd55g-firmware. Same shape as rhbz#2509956 (ThinkPad VD55G1 on ACPI: ACPI match + ipu-bridge config + int3472 vana). Vendor driver: STMicroelectronics/vd55g0-linux-driver (GPL, device tree based). Working on the SP8 (ACPI `SMO55F0`): fildunsky/linux-surface-pro8-cameras.
- IPU6 page fault regression in 6.10 (#1516) fixed upstream by Stanislaw Gruszka (lore links in github-sp9.tsv).

## Userspace

- libcamera simple pipeline + software ISP. Tuning files: OV5693 IPU6 tuning in SlyAquaGuy fork contrib; dmanresa-saes/surface-ipu6-cameras has tuning tools and a PSYS (hardware ISP) path for SP7+.
- Ready-made SP9 installers (useful for testing, not for Fedora): el-amin-dev/sp9-ov5693-dkms, loisBreant/surface-pro-9-camera (udev rules `70-sp9-dma-heap.rules`, `72-sp9-hide-ipu6.rules`, a libcamera debayer_egl patch).
- fildunsky/linux-surface-pro8-cameras: all three SP8 cameras (OV5693, OV13858, VD55G0) with six libcamera soft-ISP patches and tuning tools. Upstream libcamera has ov5693/ov13858 helpers but only `uncalibrated.yaml`, so these are upstream candidates. naeemarsalan's gist is a step by step SP8 Fedora 44 camera guide.
- Kernel branches: petm5/linux `surface-devel-v7.3` is the most complete SP9 camera branch (VD55G0, OV13858 config, upside-down quirk, MIPI clock gating, int3472 regulators). Full list in `docs/research/external-projects.md`.
- libcamera upstream status (patchwork, 2026-11-13): OV5693 black levels accepted (Dan Scally); Emfox Zhou v3 'ipa: softisp: Add tuning data for the ov13858 and ov5693' (from the SP8 Windows AIQB, applies to SP9 by sensor name) is new on the list; Hans de Goede 'simple: Do not alloc CMA DMA-buffers for camss and ipu6/7' v2 is new; Javier Tia's AIQB parser for IPU6 sensors is changes-requested; vd55g1 has a helper, vd55g0 does not.
- Front camera on upstream 7.4 still fails on SP9: libcamera chooses binned 1296x972 with both flips and that mode gives csi2 frame sync errors (dmanresa-saes/surface-ipu6-cameras#1). The binned-mode fix (#2252) is required.
- Fedora: libcamera is in Fedora; whether the Fedora build enables the software ISP for IPU6 by default needs checking (open question in `docs/roadmap.md`).

## People

Fernando Rimoli (OV5693 on IPU6 upstream), Sergey Lebedev (ov13858, VD55G0, IMX681), Peter Marshall / petm5 (VD55G0, SP9 bring-up since #1064), femito1 and el-amin-dev (SP9 front camera write-ups), D. Manresa (IPU6 Surfaces, ipu-bridge rebind), Sakari Ailus and Hans de Goede (maintainers), Jose Maria Martin (rear rotation, link freqs).
