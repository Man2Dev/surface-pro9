# Audio, display, Wi-Fi and Bluetooth, sensors, USB-C

## Audio

- Speakers work on stock kernels (feature matrix).
- Internal microphone gain is too high. Fix "ALSA: hda/realtek: Limit internal mic gain on Microsoft Surface Pro 9" (Chris Simpson) is only in CmdrShepardsPie/linux-surface-contrib `patches/7.3/0016-sound.patch`. Not on alsa-devel. Mainline `sound/hda/codecs/realtek/alc269.c` has no SP9 quirk (only "Microsoft Surface Pro 2/3").
- IDs (speaker-tuning-to-easyeffects#113): Realtek ALC274, codec 10EC0274, subsystem 10EC1284, controller subsystem 8086:7270, speaker pin 0x1b = 0x90170110.
- Speaker voicing: Windows applies the Surface APO (SurfaceAPO_1284.json) after Dolby. antoinecellerier/speaker-tuning-to-easyeffects converts it to EasyEffects or a PipeWire filter-chain; the SP9 is its reference device and a user reports much better sound.
- SP8 with SOF forced (dsp_driver=3) loses the mic (thesofproject/linux#5509); keep the legacy HDA driver.

## Display

- Flicker: `i915.enable_psr=0` (wiki Surface-Pro-9, from #862; also NixOS/nixos-hardware#941).
- VRR page flip failures on fullscreen (pop-os/cosmic-comp#1372). Some SP9 users run xe (`i915.force_probe=!46a8 xe.force_probe=46a8`).
- #1200 brightness mapping (perceived brightness non-linear, qzed explains), #1725 backlight bleeding after shutdown (SP8, SP9), #899 USB-C display limited to 4K30, #1641 external display drops (i915 issue 13479).

## Wi-Fi and Bluetooth (Intel AX211)

- Upstream iwlwifi/btintel. No linux-surface patches apply (mwifiex/ath10k patches are for other Surfaces).
- Reports: #1503 Wi-Fi switches off instantly, #1405 dropouts, #1794 AX211 firmware, #1178 and #1302 BT mouse drops (#1018 points to a solution in #1178), #1988 BT disconnects, #1973 iwlwifi crash on resume on ADL-P CNVi.

## Sensors

- Accelerometer and ambient light come through SAM HID sensors (in the SP9 node group). iio-sensor-proxy interplay: #1141 rotation only with cover, #2160.

## USB-C, docks

- UCSI over SAM (`ssam_node_hid_sam_ucm_ucsi`). kernel#184 UCSI-over-HID driver (open, SPX focus). #2371 Fedora 45: dock USB keyboard gives no input (open, 2026-11-08).
