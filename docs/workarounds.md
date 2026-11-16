# Workarounds on Fedora today

User-side fixes for SP9 problems that are not solved upstream yet. Each one names where it came from and which issue tracks the real fix. They are meant to become unnecessary: when an issue in `issues/` is fixed upstream, drop its workaround here.

## Touch and pen

iptsd must be installed and running, otherwise touch is single touch only (SP9-102).

libwacom with SP9 data, from Terra (SP9-111, source: discussion 2282):

```
sudo dnf swap libwacom libwacom-surface --allowerasing
```

libwacom override, so pen and touch are described as one display device (SP9-111, discussion 2282):

```
printf '%s\n' '[Device]' 'Name=Microsoft Surface Pro 9' 'DeviceMatch=virt|045e|0c52' 'Width=274' 'Height=183' 'IntegratedIn=Display;System;' 'Styli=0xfffff;0xffffe;' '' '[Features]' 'Stylus=true' 'Touch=true' 'Buttons=0' | sudo tee /etc/libwacom/surface-pro9.tablet
```

Pen and touch in one libinput device group, so palm rejection works while the pen is near the screen (SP9-106, discussion 2282):

```
printf '%s\n' 'ACTION=="add|change", SUBSYSTEM=="input", KERNEL=="event*", ATTRS{name}=="IPTSD Virtual * 045E:0C52", ENV{LIBINPUT_DEVICE_GROUP}="iptsd-045e-0c52"' | sudo tee /etc/udev/rules.d/99-iptsd-device-group.rules
sudo udevadm control --reload
sudo systemctl restart iptsd@dev-hidraw0
```

Slim Pen 2 phantom button presses (#1233, 2023, SP9-108). iptsd 3.x already has a separate MPP 2 threshold, `Mpp2ButtonMinMag`, default 50000, so try this only if phantom presses still happen:

```
printf '%s\n' '[DFT]' 'ButtonMinMag = 20000' | sudo tee /etc/iptsd.d/92-pen-buttons.conf
sudo systemctl restart iptsd@dev-hidraw0
```

## Type Cover

Cover slow or dead after boot (#1645, SP9-202): load `pinctrl_tigerlake` early. The power and volume buttons no longer need this on 7.2.8+ kernels (ed22ad5fdbdb).

```
printf '%s\n' 'force_drivers+=" pinctrl_tigerlake "' | sudo tee /etc/dracut.conf.d/surface-pinctrl.conf
sudo dracut -f --regenerate-all
```

Disable-while-typing (#67): stock libinput already tags `Microsoft Surface ... Keyboard` as internal. If it does not work, check that the quirk applies; the output should include `AttrKeyboardIntegration=internal`:

```
sudo dnf install libinput-utils
sudo libinput list-devices | grep -i surface
sudo libinput quirks list /dev/input/eventN
```

## Sensors

Rotation or light sensor hanging in iio-sensor-proxy (#2160, SP9-206). udev rule by CmdrShepardsPie, tested by him on an SP9 with Fedora 45:

```
sudo tee /etc/udev/rules.d/81-surface-sensors.rules >/dev/null <<'EOF'
ACTION=="remove", GOTO="surface_sensors_end"
SUBSYSTEM!="iio", GOTO="surface_sensors_end"
KERNEL!="iio:device*", GOTO="surface_sensors_end"
ATTR{[dmi/id]sys_vendor}=="Microsoft Corporation", ATTR{[dmi/id]product_name}=="Surface Pro 9", GOTO="surface_sensors_model"
GOTO="surface_sensors_end"
LABEL="surface_sensors_model"
KERNELS=="0019:045E:005D.*", GOTO="surface_sensors_hub"
GOTO="surface_sensors_end"
LABEL="surface_sensors_hub"
KERNELS=="HID-SENSOR-200073.*", ATTR{in_accel_hysteresis}="0"
KERNELS=="HID-SENSOR-200041.*", ATTR{in_illuminance_hysteresis}="0", ATTR{in_illuminance_hysteresis_relative}="0"
KERNELS=="HID-SENSOR-200041.*", ATTR{in_intensity_hysteresis}="0", ATTR{in_intensity_hysteresis_relative}="0"
KERNELS=="HID-SENSOR-200041.*", ATTR{in_chromaticity_hysteresis}="0", ATTR{in_chromaticity_hysteresis_relative}="0"
LABEL="surface_sensors_end"
EOF
sudo udevadm control --reload && sudo udevadm trigger --settle --action=change --subsystem-match=iio && sudo systemctl restart iio-sensor-proxy
```

## Audio

Internal microphone too loud (SP9-501):

```
amixer -c0 sset 'Internal Mic Boost' 0
```

Speaker hiss while headphones play (SP9-502):

```
amixer sset 'Auto-Mute Mode' Disabled
```

## Power and battery

Lid wake: if `pci=hpiosize=0` is on the command line, test lid wake with and without it (#1082, SP9-303):

```
cat /proc/cmdline
sudo grubby --update-kernel=DEFAULT --remove-args="pci=hpiosize=0"
```

Battery stuck near 50 % or not charging (#1781): check the battery limit in UEFI and turn off smart charging in Windows.

Stops charging on AC (#2232, SP9-308): in UEFI turn Battery Limit on, boot Linux once, reboot to UEFI, turn it off.

## Running kernel-surface

Fedora sets each new generic kernel as the default over kernel-surface (#1937, SP9-602):

```
sudo sed -i 's/^UPDATEDEFAULT=.*/UPDATEDEFAULT=no/' /etc/sysconfig/kernel
```
