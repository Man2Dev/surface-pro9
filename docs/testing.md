# Testing on a real SP9

Commands that answer the `needs-test` issues and the `unknown` entries in `status.yaml`. Run each block on the stock Fedora kernel first, then on kernel-surface if you have it, and note `uname -r` with every result.

## Reporting results

This repo holds public sources only, not per-machine folders. Post results where the problem is tracked (the linux-surface issue or discussion, or the upstream list), then add that public link to the matching issue in `issues/src/*.yaml` as a `reports` entry and rebuild with `python3 tools/build_issues.py`. Strip serial numbers and UUIDs from logs before posting.

## Baseline (SP9-901)

```
uname -r; rpm -q kernel iptsd libwacom libcamera iio-sensor-proxy
sudo dmidecode -s system-sku-number; sudo dmidecode -s system-manufacturer | od -c | head -2
grep -h -E 'HID_ID|HID_NAME' /sys/bus/hid/devices/*/uevent
lspci -nn | grep -iE '51d0|51d1|51c8|ipu|thunderbolt'
lsinitrd | grep -E 'surface|8250|lpss|pinctrl'
journalctl -k -b | grep -iE 'ithc|ipts|surface|ov5693|ov13858|vd55|int3472|soc_button|gpe'
systemd-analyze; grep . /sys/power/suspend_stats/*; mokutil --sb-state; efibootmgr -v
```

What it answers: DMI vendor string with or without a leading space (#2257, SP9-301), cover HID ids (`docs/hardware.md`), initramfs content (SP9-201), boot entries and Secure Boot state (SP9-601).

## Secure Boot and install (SP9-601)

Boot the current Fedora ISO and the installed stock kernel with Secure Boot on and current firmware. Record whether shim and GRUB start without linux-surface's 0001 (NX freeze, #1162) and whether MokManager starts (#1453).

## Boot stall (SP9-203)

```
systemd-analyze
journalctl -b -k | grep -E 'surface_hid|descriptor length'
```

## Sensors (SP9-206, SP9-207)

```
timeout 15 monitor-sensor
```

Run it again after the udev rule in `docs/workarounds.md`, and once after a short suspend.

## Second suspend hang (SP9-302)

SOF audio DSP lead from the SL5 (#1010). Check the internal microphone afterwards, legacy HDA may not drive it:

```
for i in 1 2 3; do sudo rtcwake -m mem -s 20; sleep 15; done
sudo grubby --update-kernel=DEFAULT --args="snd_intel_dspcfg.dsp_driver=1"
sudo reboot
lsmod | grep snd_sof
for i in 1 2 3; do sudo rtcwake -m mem -s 20; sleep 15; done
sudo grubby --update-kernel=DEFAULT --remove-args="snd_intel_dspcfg.dsp_driver=1"
```

## Shutdown, lid wake, display (SP9-305, SP9-301, SP9-503, SP9-504)

Power off from the desktop and check that the device is off (not drained the next day). Close and open the cover with the power button untouched. Use the stock kernel without any `i915.enable_psr` parameter for a few days and note flicker or resume freezes.

## RTC (SP9-605)

Right after a cold boot with networking off:

```
timedatectl
```

SP7 and SP8 lose RTC changes (#415, #2251); unknown for the SP9.

## Logs to attach

```
sudo dmesg -T > dmesg-boot.txt
journalctl -b -1 -k > dmesg-previous-boot.txt
```
