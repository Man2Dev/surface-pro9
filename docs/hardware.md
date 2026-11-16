# Surface Pro 9 (Intel) hardware identifiers

Identifiers that patches, quirks and udev rules match on. Source: logs posted in public issues (2026-11-14). Add a row only with a pointer to a public log.

## SAM HID nodes and PCI devices

SP9 dmesg and lspci output posted by owners in #1141, #1453, #1503 and #1919 (2023 to 2025) give the SAM HID devices behind each node of mainline's `ssam_node_group_sp9`:

| SAM node | Device | HID id |
|---|---|---|
| 01:15:02:01 | KIP keyboard | 045E:09AE |
| 01:15:02:02 | KIP pen stash | 045E:09B0 on covers with a pen tray, empty descriptor on others (#1845) |
| 01:15:02:03 | KIP touchpad | 045E:09AF |
| 01:15:02:05 | KIP firmware update | 045E:0991 or 045E:09CF, depending on the cover |
| 01:15:01:06 | SAM sensor hub | 045E:005D |

PCI: THC 8086:51d0, audio 8086:51c8 (class 0x040380, DSP present), CNVi Wi-Fi 8086:51f0.

What this settles:
- The keyboard backlight patch on platform-driver-x86 targets 045E:09AE, which is the SP9 cover. It applies to the SP9; a Tested-by is the next step.
- The pen stash node that stalls boot in #1845 is in mainline's SP9 group too, so the `-ENODEV` fix is an upstream patch, not a linux-surface one.
- The SP9 audio controller is the same 8086:51c8 as on the SL5, so the SOF "DSP stays in D0" suspend lead (#1010) applies. Both `snd_hda_intel` (Fedora 38 era) and `sof-audio-pci-intel-tgl` (2024) bind on SP9 logs, depending on kernel and config.

## Still unknown

- DMI vendor string with or without a leading space (#2257).
- SKU strings seen so far: `Surface_Pro_9_2038` and `Surface_Pro_9_for_Business_2038` (sources in `docs/roadmap.md`, quick win 1); other SKUs unconfirmed.
- Firmware versions that change behaviour (NX enforcement since 2023-06, #1162).

Commands to collect these are in `docs/testing.md`.
