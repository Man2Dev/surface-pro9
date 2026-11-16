---
id: SP9-106
title: Erratic touch detection and weak palm rejection with default iptsd settings
labels:
- area:touch
- kind:bug
- priority:P2
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-105
- SP9-107
upstream:
- linux-surface/iptsd
source: issues/src/1-touch-pen.yaml
---

# SP9-106: Erratic touch detection and weak palm rejection with default iptsd settings

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P2 | touch | bug | n/a | partial | n/a |

## Problem

Taps need force, swipes break, palms register while writing, and DisableOnStylus leaves some touches or
splits gestures. The linux-surface wiki carries an SP9 calibration override as a workaround.

## Origin

Contact detection defaults changed in iptsd dd0c322 and are too strict for several devices; a contact
missed for a single frame ends the touch; DisableOnStylus has edge cases.

## Reports

- [linux-surface/iptsd#171](https://github.com/linux-surface/iptsd/issues/171) (open issue, workaround) "the new contact detection defaults are bad": the new contact detection defaults are bad
- [linux-surface/iptsd#173](https://github.com/linux-surface/iptsd/issues/173) (open issue, workaround) "Palm rejection for stylus users: Documentation, possibly improvements": SP9 Slim Pen 2 palm rejection: docs and proposed defaults
- [linux-surface/iptsd#166](https://github.com/linux-surface/iptsd/issues/166) (open issue, unsolved) "DisableOnStylus does not disable all touch inputs": DisableOnStylus does not disable all touch inputs
- [linux-surface/iptsd#218](https://github.com/linux-surface/iptsd/issues/218) (open issue, unsolved) "DisableOnStylus can split one touch gesture into multiple sequences": DisableOnStylus splits one gesture into several
- [linux-surface/iptsd#226](https://github.com/linux-surface/iptsd/issues/226) (closed issue, stale) "Touches are interrupted when a contact is missed for a single frame (Surface Pro 8)": touches interrupted when a contact is missed for one frame (SP8)
- [linux-surface#1862](https://github.com/linux-surface/linux-surface/issues/1862) (open issue, question) "[SP9] NOT using iptsd results in better touch, gnome 48": SP9: touch feels better without iptsd on GNOME 48
- [linux-surface#1273](https://github.com/linux-surface/linux-surface/issues/1273) (closed issue, workaround) "[SP8] No palm-rejection under linux after windows, and firmware updates EDIT: and iptsd update": palm rejection lost after iptsd update: recalibrate

## Fixes, patches and PRs

- [linux-surface/iptsd#234](https://github.com/linux-surface/iptsd/issues/234) (open PR, waiting) "contacts/detection: Add adaptive neutral mode": adaptive neutral mode
- [linux-surface/iptsd#235](https://github.com/linux-surface/iptsd/issues/235) (open PR, new) "Skip detection on frames below the deactivation threshold. Merges cleanly.": skip detection below the deactivation threshold
- [linux-surface/iptsd#214](https://github.com/linux-surface/iptsd/issues/214) (open PR, waiting) "[Feature] Toggle touchscreen at different stylus levels": DisableOnStylusLevel (by an SP9 user)
- [linux-surface/iptsd#227](https://github.com/linux-surface/iptsd/issues/227) (closed PR, promised-never-resubmitted) "contacts/tracking: Retain lost contacts for a few frames": retain lost contacts for a few frames (closed, never resubmitted)
- [orphaned-patches/iptsd-227-retain-lost-contacts.rebased-on-9c7a554.patch](../orphaned-patches/iptsd-227-retain-lost-contacts.rebased-on-9c7a554.patch): rebased copy of iptsd#227

## Possible solutions

- Workaround from the wiki: /etc/iptsd.d/91-calibration.conf with ActivationThreshold 24, DeactivationThreshold 20, OrientationThresholdMax 5; or run iptsd-calibrate.
- Test the open PRs plus the orphaned #227 on the SP9 and propose SP9 defaults upstream.

## Next steps

- [ ] Run iptsd-calibrate on an SP9 and post the result on the tracking issue.

## Commands

```
sudo iptsd-calibrate $(iptsd-find-hidraw)
```

## Upstream and people

- Upstream target: linux-surface/iptsd
- People: StollD, xieve, cunninghamcard-bit, hansakoch

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-105](SP9-105-iptsd-service-and-udev-rule-are-fragile-stops-after-cold-boo.md) iptsd service and udev rule are fragile (stops after cold boot, probes every hidraw, loses its tag), [SP9-107](SP9-107-slim-pen-2-report-rate-is-about-66-hz-jagged-fast-strokes.md) Slim Pen 2 report rate is about 66 Hz (jagged fast strokes)

## Knowledge base

- [docs/research/wiki-digest.md](../docs/research/wiki-digest.md)
- [docs/research/closed-prs.md](../docs/research/closed-prs.md)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
