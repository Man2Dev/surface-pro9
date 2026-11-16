# Keyboard covers, SAM, buttons, battery, thermal, suspend, lid, shutdown

Status keys: `keyboard-typecover`, `keyboard-backlight`, `flex-keyboard`, `tablet-mode`, `battery-ac`, `thermal-fan-profile`, `buttons`, `lid-wake`, `shutdown`, `acpi-interrupt-storm`, `suspend-s0ix`, `hibernate`.

## Surface Aggregator Module (SAM)

- Mainline `surface_aggregator_registry.c`: `MSHW0343` maps to `ssam_node_group_sp9` ("Surface Pro 9, 10 and 11 (Intel/x86)"): KIP hub, battery and AC, perf profile with fan, thermal sensors, fan speed, tablet switch, KIP keyboard, pen stash, touchpad, fwupd, SAM HID sensors, UCM UCSI. SP9 SAM support was brought up in #984 (qzed, 2022 to 2023); tablet switch accepted upstream 2023-03.
- Requirements easy to miss when building your own kernel: `CONFIG_SERIAL_DEV_BUS=y` and `CONFIG_SERIAL_DEV_CTRL_TTYPORT=y` (#1136, discussion 981). Fedora sets both.
- Probe ordering bug: serial hub returns -EINVAL instead of -EPROBE_DEFER when its wakeup GPIO is not ready (#2219). Wu Enqiang v2 on platform-driver-x86 (2026-10-24), carried in linux-surface 7.3 `0007`. Older related fix: Weifeng Liu "Defer probing of SAM if serdev device is not ready" (accepted 2024). CmdrShepardsPie's kernel#182 was closed in favour of the upstream v2.

## Keyboard backlight

- Discussion 2282: backlight works on an SP9 but Plasma has no control.
- Upstream candidate: "HID: surface-hid: support keyboard backlight on Surface Pro Keyboard (045E:09AE)" (Ramon Jesus Miranda, pdx86, 2026-10-23, new). First step: confirm the SP9 keyboard HID id, then test.
- `hid-surface` (linux-surface 0015, BTN_0 / FN filter) matches BUS_HOST 045E:09AE and 09AF too; it was made for SL4 AMD (#1851) and fixed #1719 ("[SP9] FN button stops mouse input in other windows").

## Power and volume buttons

- `soc_button_array` (MSHW0040) can probe before `pinctrl_tigerlake` and give up (#1392, wiki). Fedora builds both as modules, so it can happen there.
- Workarounds: `force_drivers+=" pinctrl_tigerlake "` in `/etc/dracut.conf.d/`, or reload `soc_button_array`.
- Kernel fix: mainline ed22ad5fdbdb "Input: soc_button_array - fix MS Surface Pro 11 probe failure" (Hans de Goede; in 7.3, stable 7.2.8, 6.18.54, 6.12.112) propagates `-EPROBE_DEFER` except on Bay Trail and Cherry Trail. CmdrShepardsPie verified it on an SP9 with an initramfs that has `soc_button_array` but not `pinctrl_tigerlake` (#1392, 2026-10-25). linux-surface `0009` "defer MSHW0040 probe until GPIO is ready" (Jan Baisch, kernel#172) is now redundant, and the workarounds above are only needed on older kernels.

## Battery

- Mainline surface_battery / surface_charger work. Open: "Report not charging while idle on AC" (CmdrShepardsPie fork), "handle battery event 0x1a" (pdx86 2026-10-23), #1837 shows full while discharging, #1781, #1800, charge limit (#1580, kernel#167 smart charging).
- Branches: Cloveian/kernel `battery-charge-limit` (2026-11-10), petm5/linux-surface-kernel `v6.18-surface-devel-battery-features` (smart charging, authentication status). Desktop app with a charge limit switch: Madmaxx636/surface-companion.

## Thermal and fan

- Mainline: fan driver, fan profile, thermal sensors (Ivor Wanders, Maximilian Luz, 2024).
- linux-surface 7.3: "platform_profile: add fan power state handling" (petm5, kernel#166). Upstream "handle fan standby state" is changes-requested (2026-11-11). #1445 fan runs in suspend, #1726 fan at high speed with low temperature. Discussion 1734 thermald config. WIP fan curve offset and base rpm: petm5/linux-surface-kernel `v6.18-surface-devel-fan-ctrl`. thermald `--adaptive` fails on SP9 (no DPTF tables); hand-written config in iwanders/nixos-surface; intel/thermal_daemon#616 explains why passive trips saw PL1.

## Lid wake (surface_gpe)

- Mainline surface_gpe has SP8 (2022) but not SP9. linux-surface `0012` adds SP9 matched by `DMI_PRODUCT_SKU "Surface_Pro_9_2038"` with `lid_device_props_l52`. Never posted upstream.
- Problems: #2257 the DMI sys_vendor has a leading space on some units (fix in surface-gpe#7), #1919 "no compatible Microsoft Surface device found", SP9 Business SKU (surface-gpe#3, #5), #1811 disabling lid handling.
- Ready patch: dragged9698 gist "platform/surface: gpe: Tolerate padded DMI sys_vendor strings" (DMI_EXACT_MATCH to DMI_MATCH for the vendor, verified on SP9 2038, GPE 0x52, placeholder Signed-off-by). With 0012 this is a full submission.
- Business SKU: `Surface_Pro_9_for_Business_2038` (Meatwo310/dotnix PR #13, tested).
- bugzilla.kernel.org 218923: SP9 ACPI error storm and failed later suspends with surface_gpe loaded.

## Shutdown

- #1058 (qzed): EFI `ResetSystem(EFI_RESET_SHUTDOWN)` returns on SP9 and SL5. Downstream fix `0011` "PCI: Add quirk to prevent calling shutdown method" for TB4 USB/PCIe/NHI and GPU devices, DMI gated. Wiki: works since 6.1.12-2. Some units also need `pci=hpiosize=0`.

## ACPI interrupt storm

- Closing the lid on AC, TB hotplug, lid resume flood dmesg with ACPI errors (#1082). Wiki workaround `pci=hpiosize=0` (also fixes shutdown and wake for some SL5/SLS2/SP10 users: #1507, #1664, #1805). No root-cause fix found.

## Suspend and hibernate

- s2idle works with low PC10 residency (wiki). Wake problems: #1183, #1224, #1684, #1910, #1164. #2258 s2idle hang in pm_fs_sync (btrfs). Fan in suspend #1445.
- Hibernate under Secure Boot lockdown needs linux-surface `0001` lockdown_hibernate (downstream; original patch by Kelvie Wong, 2022, carried via kernel#158). Wiki: `HibernateMode=reboot`. Discussion 2202: suspend then hibernate recipe and camera re-probe issue.
