# Closed but unmerged pull requests (2026-11-13)

All 115 closed, unmerged PRs in the linux-surface org were listed; 70 are from people (the rest are update bots). Each PR page was read for the closing comments, the PR heads were fetched with git and compared with every `patches/` dir on master and with mainline v7.4-rc3. Table: `data/indexes/closed-prs.tsv`. Orphaned code: `orphaned-patches/`.

## How these PRs usually end

Most "unmerged" PRs did land. The maintainers apply changes in `linux-surface/kernel` or by hand and then close the PR ("Integrated into the kernel repos. Patches will be updated here soon"), which GitHub counts as unmerged. Of the 70, 47 landed in some form (integrated, moved to the right repo, or superseded by an upstream patch, a newer PR or the maintainer's own update), 11 were duplicates, rejected, obsolete or in the wrong repo, 8 were withdrawn or abandoned, and 4 left code behind with a follow-up that never came (below). Since 2026-10 a daily job rebases the patch series automatically (qzed in #2362), so rebase PRs are no longer needed.

## Promised follow-ups that never came

| PR | What it fixes | SP9 | State of the code |
|---|---|---|---|
| linux-surface#2210 (RowdyRagamuffin, 2026-07) | 7.0 series for SP9; author said he would resubmit, never did. Its one useful piece: "drivers/hid/ithc: Fix PM suspend/resume to preserve hid_device across s2idle" | direct | `orphaned-patches/linux-surface-2210-ithc-pm-preserve-hid-device.patch` applies to the v7.3-surface ITHC (dry run). Not built or tested here; AI-assisted, author reported unresolved errors in the wider series. Relevant to touch dying after sleep (sebanc/brunch#2202 on SP9, #2367). |
| iptsd#227 (cunninghamcard-bit, 2026-10) | Keep a lost contact for a few frames so swipes do not break when the heatmap misses one frame (iptsd#226, SP8) | sibling (same ITHC/iptsd path) | Author said he would resubmit after testing, never did. Rebases cleanly on iptsd master 9c7a554 (`git am -3`); saved as `orphaned-patches/iptsd-227-retain-lost-contacts.rebased-on-9c7a554.patch`. Not built here. |
| kernel#74 (MaxLeiter, 2020) | apds9960 proximity `near_level` | none (SB3, SL3, SP7) | ACPI ID was taken; maintainer invited a new PR for the rest, none came. |
| kernel#105 (nakato, 2021) | SAM GPIO interrupt reconfigure on probe (AMD SL4 power draw) | none | Author agreed it was a hack and meant to raise it with the GPIO maintainers; no trace. |

Followed up as promised: kernel#183 became kernel#188 (open), linux-surface#2155 became #2156 (open), #1544 became kernel#158, #1770 became #1790, kernel#119 was re-sent and is in the series.

## Closed PRs whose threads matter for the SP9

- #2171 (ov5693 MIPI_CTRL00): replaced by Fernando Rimoli's upstream series; the thread holds the SP9, SP8, SP7+ and Go 4 test data, the bit sweeps that showed only bit 5 is needed, and the SP9 report that 7.2.11-surface-1 still had no front camera frames.
- kernel#177 (ov13858 flip on SP9): rejected because the fix belongs in the ipu-bridge quirk; mainline v7.4 has it.
- kernel#182 and #1430 (SAM probe deferral): both superseded by upstream patches (Wu Enqiang v2, Hans de Goede 2024).
- #2233 (7.2 series): an SP9 test report on Fedora 43 with Secure Boot, and an SP5 user's commit that makes all three IPU3 cameras and the IR illuminator work (in his fork, never sent).
- kernel#132: quo said he will not upstream ITHC himself and would hand it over; ITHC needs formatting work first. Relevant to the touch upstreaming plan.
- libwacom-surface#26: libwacom 2.19+ measures tablets in millimetres. The fix (5851f1c) moved the SP9 file to Width 275 / Height 183; tablet files still in inches (bazzite-surface ships Width=10, Height=6) are wrong on current libwacom.

## Mainline check made along the way

v7.4-rc3 int3472 now maps GPIO type 0x02 (STROBE) to `ir_flood`, 0x08 (POWER1) to `dvdd` and 0x10 to `dovdd`, so the IR flood LED and the SP7+/SP10 supply pins no longer need downstream code.
