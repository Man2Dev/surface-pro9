# Open pull requests (2026-11-13)

All 64 open PRs in the linux-surface org were listed; 61 are from people. Each PR page was read for reviews and maintainer comments, and the heads were fetched with git. Table: `data/indexes/open-prs.tsv` (21 matter directly for the SP9).

## The pattern

Maintainer attention is thin. Only 13 of the 61 have any reply from qzed, StollD or danielzgtg, and none of the SP9 camera, lid or iptsd PRs has had a code review. qzed's standing request is to send kernel changes to `linux-surface/kernel`, where he now generates the patch series automatically; PRs against `linux-surface/linux-surface` that touch kernel code wait until they are moved. danielzgtg plans to jump from 6.18/6.19 straight to 7.3 as a possible LTS, skipping 7.0 (#2156).

## Open PRs that matter for the SP9

Kernel (`linux-surface/kernel`):
- **#193 (CmdrShepardsPie, today)** backports the v7.4-rc1 camera work to 7.3: Sakari's `ipu_bridge_get_ipu6()`, Rimoli's ov5693 clock-lane gate and per-IPU configs, Lebedev's ov13858 flip controls. With it the 7.3 kernel matches 7.4 for the SP9 cameras, and #180 and the 0x4800 write in #181 become redundant.
- **#181 (rylos)** carries D. Manresa's "ov5693: make the 2x2-binned mode stream on IPU6", which the SP9 front camera still needs on 7.4 (also in linux-surface#2252).
- **#191 and #174** fix the downstream OVTID858 link frequency entry; mainline 7.4 already has it right.
- **#169 (petm5)** VD55G0 IR camera; the series is on linux-media.
- **#167 (petm5)** smart charging and battery authentication: qzed reviewed it and asked Cloveian to send the charge limit as its own patch. Cloveian has the branch (`battery-charge-limit`, 2026-11-10) but no PR yet.
- **#173 (zR-JB)** Flex Keyboard tablet switch: qzed asked for changes in August, author agreed, nothing pushed since.
- **#184 (JValdivia23)** UCSI over SAM HID: the only SP9-relevant PR with active maintainer work (qzed tested it on the Pro X and read the SP9 SQ3 Windows driver).

Patch series and out-of-tree repos:
- **linux-surface#2011** contains Maximilian Luz's own "gpe: Add support for Surface Pro 9 and Surface Laptop 5", with an SL5 entry (GPE 0x52) that the shipped 0012 lacks. With surface-gpe#7 (vendor string) and surface-gpe#5 (Business SKU) this is everything for one upstream surface_gpe patch covering all SP9 SKUs and the SL5.
- **linux-surface#2227** SP8/SP9 rear rotation; mainline 7.4 has the SP9 quirk, the thread documents a red/blue swap bug in an earlier version.

iptsd, all mergeable on master today with no maintainer reply:
- **#219** remove `StopWhenUnneeded=yes`: the service stops itself about 6 s after a cold boot.
- **#221** hide the raw ITHC input nodes that duplicate iptsd's events (iptsd#220).
- **#224** keep the systemd tag across udev change events.
- **#214** `DisableOnStylusLevel` (by an SP9 user who runs it).
- **#233** debounce eraser and button flags for MPP 2 pens (Slim Pen 2).
- **#234** adaptive neutral mode, **#235** skip detection below the deactivation threshold: both aim at the erratic touch the wiki calibration works around.

These iptsd changes matter for the Fedora package: they are the difference between touch that starts reliably and touch that needs a restart, and they are small enough to review.

## Competing or duplicate work

- ov5693 clock lane: kernel#180, #181 (0x4800 write), #193, all superseded by Rimoli's upstream series.
- OVTID858 link frequencies: kernel#174 and #191.
- IPTS (MEI, SP4 to SP7) stop path: kernel#178, #187, #188.
