---
id: SP9-901
title: Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)
labels:
- area:meta
- kind:needs-test
- priority:P1
- status:needs-test
depends_on: []
blocks:
- SP9-305
- SP9-503
- SP9-504
- SP9-605
- SP9-904
related:
- SP9-201
- SP9-203
- SP9-205
- SP9-301
- SP9-305
- SP9-503
- SP9-504
- SP9-601
- SP9-605
upstream: []
source: issues/src/9-meta.yaml
---

# SP9-901: Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| needs-test | P1 | meta | needs-test | unknown | unknown | unknown |

## Problem

Several issues wait on data from a real SP9 on the stock Fedora kernel: DMI strings, initramfs content,
buttons, shutdown, PSR, RTC, Secure Boot, boot stalls.

## Origin

The KB is built from reports by many owners on many kernels; there is no single baseline on a current stock Fedora kernel yet.

## Reports

- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": reports collected for upstreaming

## Fixes, patches and PRs

- none yet

## Possible solutions

- Capture once per kernel (stock Fedora, linux-surface), post the results publicly and link them here (docs/testing.md).

## Next steps

- [ ] Run the capture commands below on the stock Fedora kernel, then on kernel-surface.

## Commands

```
sudo dmidecode -s system-sku-number; sudo dmidecode -s system-manufacturer | od -c | head -2
grep -h -E 'HID_ID|HID_NAME' /sys/bus/hid/devices/*/uevent
lspci -nn | grep -iE '51d0|51d1|ipu|thunderbolt|51c8'
lsinitrd | grep -E 'surface|8250|lpss|pinctrl'
journalctl -k -b | grep -iE 'ithc|ipts|surface|ov5693|ov13858|vd55|int3472|soc_button|gpe'
systemd-analyze; grep . /sys/power/suspend_stats/*; timedatectl; mokutil --sb-state
uname -r; rpm -q kernel iptsd libwacom libcamera iio-sensor-proxy
```

## Upstream and people

- Upstream target: none
- People: none

## Linked issues

- Depends on: none
- Blocks: [SP9-305](SP9-305-shutdown-does-not-power-off-on-mainline-s5-quirk-never-poste.md), [SP9-503](SP9-503-display-flicker-and-resume-freezes-from-panel-self-refresh.md), [SP9-504](SP9-504-display-odds-and-ends-120-hz-black-screen-external-4k-at-30.md), [SP9-605](SP9-605-rtc-time-persistence-on-the-sp9-is-unknown-sp7-and-sp8-lose.md), [SP9-904](SP9-904-fix-out-of-date-linux-surface-wiki-pages-for-the-sp9.md)
- Related: [SP9-201](SP9-201-type-cover-does-not-work-at-the-luks-passphrase-prompt-dracu.md) Type Cover does not work at the LUKS passphrase prompt (dracut lacks surface_aggregator_hub), [SP9-203](SP9-203-boot-stalls-about-2-minutes-surface-hid-probes-the-pen-stash.md) Boot stalls about 2 minutes: surface_hid probes the pen stash node and fails with -EPROTO, [SP9-205](SP9-205-power-and-volume-buttons-dead-when-soc-button-array-probes-b.md) Power and volume buttons dead when soc_button_array probes before the pin controller, [SP9-301](SP9-301-opening-the-cover-does-not-wake-the-sp9-surface-gpe-has-no-s.md) Opening the cover does not wake the SP9 (surface_gpe has no SP9 entry), [SP9-305](SP9-305-shutdown-does-not-power-off-on-mainline-s5-quirk-never-poste.md) Shutdown does not power off on mainline (S5 quirk never posted upstream), [SP9-503](SP9-503-display-flicker-and-resume-freezes-from-panel-self-refresh.md) Display flicker and resume freezes from Panel Self Refresh, [SP9-504](SP9-504-display-odds-and-ends-120-hz-black-screen-external-4k-at-30.md) Display odds and ends: 120 Hz black screen, external 4K at 30 Hz, backlight spots after shutdown, [SP9-601](SP9-601-installing-and-booting-fedora-on-the-sp9-with-secure-boot-nx.md) Installing and booting Fedora on the SP9 with Secure Boot (NX firmware, MOK, boot entries), [SP9-605](SP9-605-rtc-time-persistence-on-the-sp9-is-unknown-sp7-and-sp8-lose.md) RTC time persistence on the SP9 is unknown (SP7 and SP8 lose clock changes)

## Knowledge base

- [docs/roadmap.md](../docs/roadmap.md)
- [docs/testing.md](../docs/testing.md)

_Generated from `issues/src/9-meta.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
