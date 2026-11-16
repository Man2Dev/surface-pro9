---
id: SP9-903
title: 'Goal: SP9 fully usable on the stock Fedora kernel and packages'
labels:
- area:meta
- kind:tracking
- priority:P1
- status:tracking
depends_on:
- SP9-101
- SP9-102
- SP9-111
- SP9-201
- SP9-202
- SP9-203
- SP9-206
- SP9-301
- SP9-302
- SP9-305
- SP9-401
- SP9-501
- SP9-601
blocks: []
related:
- SP9-602
- SP9-904
upstream: []
source: issues/src/9-meta.yaml
---

# SP9-903: Goal: SP9 fully usable on the stock Fedora kernel and packages

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| tracking | P1 | meta | tracking | partial | works | partial |

## Problem

Umbrella issue. The SP9 should work on a stock Fedora install without the linux-surface kernel or third-party
repos.

## Origin

Everything below this issue is a step toward it; the blockers are touch (out-of-tree driver), lid wake,
shutdown, cover at LUKS, iptsd/libwacom packaging and camera finishing work.

## Reports

- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": starting point
- [linux-surface#205](https://github.com/linux-surface/linux-surface/issues/205) (open issue, tracker) "Upstream status": linux-surface upstream status tracker
- [linux-surface#1419](https://github.com/linux-surface/linux-surface/issues/1419) (closed) "when this will be upstream to mainline": when will this be upstream (qzed: free time only)

## Fixes, patches and PRs

- none yet

## Possible solutions

- Work the P1 issues first; prefer small upstream patches with clear authors (gpe, mic gain, dracut, surface_hid, hid-sensor-trigger).

## Next steps

- [ ] See the dependency tree in issues/README.md.

## Upstream and people

- Upstream target: none
- People: none

## Linked issues

- Depends on: [SP9-101](SP9-101-touchscreen-and-pen-need-the-out-of-tree-ithc-driver-no-upst.md) Touchscreen and pen need the out-of-tree ITHC driver (no upstream driver for the ADL THC in legacy mode), [SP9-102](SP9-102-iptsd-is-not-packaged-in-fedora.md) iptsd is not packaged in Fedora, [SP9-111](SP9-111-libwacom-has-no-sp9-tablet-description-pen-and-touch-not-rec.md) libwacom has no SP9 tablet description (pen and touch not recognised as a tablet), [SP9-201](SP9-201-type-cover-does-not-work-at-the-luks-passphrase-prompt-dracu.md) Type Cover does not work at the LUKS passphrase prompt (dracut lacks surface_aggregator_hub), [SP9-202](SP9-202-type-cover-dead-or-slow-after-boot-sam-probe-returns-einval.md) Type Cover dead or slow after boot: SAM probe returns -EINVAL before the pin controller is ready, [SP9-203](SP9-203-boot-stalls-about-2-minutes-surface-hid-probes-the-pen-stash.md) Boot stalls about 2 minutes: surface_hid probes the pen stash node and fails with -EPROTO, [SP9-206](SP9-206-rotation-and-light-sensor-hang-in-iio-sensor-proxy-claims-ti.md) Rotation and light sensor hang in iio-sensor-proxy (claims time out, rotation freezes), [SP9-301](SP9-301-opening-the-cover-does-not-wake-the-sp9-surface-gpe-has-no-s.md) Opening the cover does not wake the SP9 (surface_gpe has no SP9 entry), [SP9-302](SP9-302-sp9-sometimes-does-not-wake-from-s2idle-or-hangs-on-the-seco.md) SP9 sometimes does not wake from s2idle (or hangs on the second suspend), [SP9-305](SP9-305-shutdown-does-not-power-off-on-mainline-s5-quirk-never-poste.md) Shutdown does not power off on mainline (S5 quirk never posted upstream), [SP9-401](SP9-401-front-camera-ov5693-returns-empty-buffers-on-mainline-7-4-2x.md) Front camera (OV5693) returns empty buffers on mainline 7.4: 2x2 binned mode with flips fails, [SP9-501](SP9-501-internal-microphone-gain-is-too-high-noisy-clipped-recording.md) Internal microphone gain is too high (noisy, clipped recordings), [SP9-601](SP9-601-installing-and-booting-fedora-on-the-sp9-with-secure-boot-nx.md) Installing and booting Fedora on the SP9 with Secure Boot (NX firmware, MOK, boot entries)
- Blocks: none
- Related: [SP9-602](SP9-602-fedora-installs-a-generic-kernel-as-default-over-kernel-surf.md) Fedora installs a generic kernel as default over kernel-surface after updates, [SP9-904](SP9-904-fix-out-of-date-linux-surface-wiki-pages-for-the-sp9.md) Fix out-of-date linux-surface wiki pages for the SP9

## Knowledge base

- [README.md](../README.md)
- [docs/roadmap.md](../docs/roadmap.md)
- [status.yaml](../status.yaml)

_Generated from `issues/src/9-meta.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
