# Open issues: what is still broken, and what already has a fix (2026-11-14)

All 288 open issues in the linux-surface org that were indexed as SP9 (140) or sibling (148) were read in full: every comment, with threads over 30 comments fetched through the REST API. A search for issues updated since 2026-11-11 found no new SP9 issue. Table: `data/indexes/open-issues.tsv`.

## How they stand

178 of the 288 have never had a maintainer reply, 81 of them SP9 issues. Of the SP9 set: 17 are already fixed somewhere and could be closed, 11 have a fix waiting in a PR, a gist or on a mailing list, 37 have a workaround in the thread, 19 are unsolved, 8 need information, the rest are questions, trackers or not about the SP9.

## Findings that change the plan

1. **The button race is fixed upstream.** Hans de Goede's "Input: soc_button_array - fix MS Surface Pro 11 probe failure" (ed22ad5fdbdb, in 7.3, backported to 7.2.8, 6.18.54 and 6.12.112) propagates `-EPROBE_DEFER` on everything except Bay Trail and Cherry Trail. CmdrShepardsPie tested it on an SP9 with an initramfs that has `soc_button_array` but not `pinctrl_tigerlake`: buttons bind once the pin controller loads (#1392, 2026-10-25). Checked in mainline `soc_button_array.c`. linux-surface 0009's defer patch is redundant and the roadmap item to upstream it is dropped. Stock Fedora 7.2.8+ kernels have the fix.
2. **iio-sensor-proxy hangs on the SP9 (#2160).** The SAM sensor hub reports accelerometer and light only on change (hysteresis 0.05 and 1/20), and the SAM HID transport cannot fetch an input report on request, so every sysfs read waits 5 s when the tablet is still. iio-sensor-proxy 3.6+ polls those sensors on its main thread, so claims time out and rotation freezes. A udev rule setting the hysteresis to 0 fixes it on Fedora 45 with iio-sensor-proxy 3.9. Upstream: iio-sensor-proxy#432 on freedesktop GitLab, where CmdrShepardsPie asks for someone with an account to propose the change. Easy contribution for a Fedora packager.
3. **Two-minute boots on Fedora SP9 (#1845).** `surface_hid` probes the pen stash node `01:15:02:02:00` that the SP9 SAM registry hard-codes; covers without a pen stash return an empty descriptor and the probe fails with `-EPROTO`. qzed: it should return `-ENODEV`. A small `surface_hid` patch for linux-input / platform-driver-x86, and a candidate cause for the slow cover start reported in discussion 2282.
4. **Fan stuck at high speed after Windows (#1726).** Windows sets a fan floor with SAM FAN command `0x0b` (`SetMinFanRpm`, from Microsoft's own headers per Cloveian); Linux never clears it. Sending `0x0b 0` at probe from the platform profile driver would fix it. Upstreamable next to the fan standby series.
5. **s2idle on ADL Surfaces has two concrete leads.**
   - SL5, same ADL-P PCH: the second suspend hangs because the SOF audio DSP (8086:51c8) stays in D0 after the first resume; `snd_intel_dspcfg.dsp_driver=1` (legacy HDA) fixed it (#1010). To test on the SP9; if it holds, the real fix belongs in SOF.
   - SL5: in s2idle the INTC1055 pin controller corrupts pin 213's PADCFG0, which fires GPE 0x52 and either blocks or forces wake-up (kernel#162, open, qzed prefers userspace). The SP9 uses the same pin controller and the same lid GPE.
   - Others: btrfs `pm_fs_sync` hang (#2258); wake fails when the lid moves during suspend (#1910, #1811), where logind lid handling off plus `pci=hpiosize=0` worked on an SL5.
6. **SAM event restore after hibernate (#2294, SP8).** Enabling event sources on restore times out with -110; one retry 200 ms later works and the cover comes back without reattaching. The SP9 uses the same restore path; upstreamable SAM fix from pentop's tested patch.
7. **Pen at 66 Hz (#1588).** An SP9 user processes position on every DFT window and gets about 266 to 300 Hz in iptsd; patch attached to the issue, tilt and pressure still rough. A future iptsd PR once cleaned up.
8. **Charging stops on SP9 (#2232, #1800).** Two SP9 reports: toggling the UEFI battery limit on, booting once, and off again restores charging. The firmware or EC keeps a charge state that Linux cannot reset today; relevant to kernel#167.
9. **Fedora packaging items.** A generic kernel update becomes the default despite `kernel-surface-default-watchdog`; `UPDATEDEFAULT=no` in `/etc/sysconfig/kernel` works around it (#1937). akmods with kernel-surface fixed in 9db9d9b2e1 (#1872). linux-surface packages are now built automatically for F43 to F45 (7.3.4-1, package status #2318), but since 2026-11-12 some release files are uploaded as `.rpm.blob` (#2370). iptsd's udev rule probes every hidraw node and can stall input for 6 s per node (iptsd#228, iptsd#229); worth fixing before a Fedora iptsd package ships.
10. **Boot and install.** Fedora 41 ISO hung on SP9 because of IPU6 in 6.11 (#1690, since fixed); a Fedora 45 dual-boot install shows only the Windows Boot Manager (#2361, unanswered). ITHC failed when the kernel was booted as an EFI stub (#1078, quo/ithc-linux#26); quo committed a likely fix in 2024 (18afc6f, THC register 0x1128 bit 5), so retest once before moving to a UKI. Secured-core makes GRUB reset once (#1070).

## Open SP9 problems with no fix anywhere

Touch never initialises on one SP9 unit (`ithc_legacy_init` -110, UEFI 22.107.143, #2367); touchscreen locks up while the magnetic charger is attached (#1470); external 4K at 30 Hz only (#899); shutdown backlight spots (#1725); MokManager does not start (#1453); battery stuck at full (#1837); Dock USB keyboard dead on Fedora 45 (#2371); Slim Pen 2 haptics (#1066, intel-precise-touch#27); one firmware capsule of five applied from Linux (surface-uefi-firmware#51).

## Could be closed (already fixed)

#1392 (buttons, ed22ad5fdbdb), #1516, #1540, #1609, #1612, #1690 (6.10/6.11 IPU6 boot), #1064, #1865, #1892, kernel#165, #2056 (cameras, mainline 7.4 and the 7.3 series), #1753 (ov13858 link frequency), #1078 (EFI stub, retest first), #1872 (akmods), #1126 (answered), #1277 (#1252), surface-aggregator-module#59 (thermal sensors upstream), #997, #1412. A short comment with the fixing commit would let a triager close them; danielzgtg now has the Triage role (#2081).

## Sibling lessons

RTC changes not kept on SP7/SP8: SAM holds the clock and can be set from userspace (#415, #2251); check whether the SP9 keeps time across power off. iwlwifi crash on resume on ADL-P CNVi (#1973): `iwlmvm power_scheme=1` made it rarer. Contact detection defaults from iptsd dd0c322 were too strict (iptsd#171); Slim Pen 2 dropouts need a higher `Mpp2ButtonMinMag` (iptsd#161). iptsd blocks suspend-then-hibernate (iptsd#190). SP7 s2idle hard freezes since 2026-11-12 on 7.2.15 and 7.3.3 (kernel#192); watch for the same on SP9.

## Issue threads with code behind them (2026-11-14)

- **#2160, light sensor dead after sleep.** CmdrShepardsPie traced this with kprobes to a kernel bug in `hid-sensor-trigger`. If system suspend starts inside the 3 s autosuspend window, the sensor is powered off but runtime PM stays "active", so it is never powered back on. Upstream target: linux-iio.
- **iio-sensor-proxy#432 (freedesktop GitLab).** It shows a verification page to automated access. It was not read and nothing was done to get past the page; read it in a normal browser.
- **#2294, SAM restore retry.** pentop's patch is in the issue as diagnostic quality (static state, single controller). He suggests the real fix: queue failed re-enables from `ssam_serial_hub_pm_restore()` to a work item, or let `surface_hid` re-enable its own event sources on resume.
- **#1588, pen report rate.** Muvkina's two patches are issue attachments (`higher_polling_rate.patch`, `highest_polling_rate.patch`). Also linked there: AndyGozas/iptsd `bundle-events-workaround` and the `feature/prediction` branch in linux-surface/iptsd. The attachments could not be fetched from the browser page (cross-origin).
- **kernel#162 (SL5 s2idle module).** Large and AI-generated: a PADCFG0 repair, a failsafe re-suspend, suspend-to-lock, RTC sync. Its September follow-up found that a local service disabling C8 and C10 was itself blocking S0ix on that machine. Treat it as a diagnosis of INTC1055 behaviour, not as code to carry.
- **kernel#167 and #1726, SAM command names.** Microsoft's Surface app ships `SurfaceCommonHeadersDotNet.dll`, with 1017 SSH commands in 36 categories, named and typed. Cloveian used it to:
  - find the battery charge-mode commands (BAT 0x09 and 0x0a, 0x1b, 0x22, 0x23);
  - find the fan floor (FAN 0x0b);
  - write a charge limit patch on the standard `charge_types` and `charge_control_end_threshold` attributes, tested on SP11, not yet a PR.
