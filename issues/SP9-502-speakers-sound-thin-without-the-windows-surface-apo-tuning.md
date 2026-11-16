---
id: SP9-502
title: Speakers sound thin without the Windows Surface APO tuning
labels:
- area:audio
- kind:missing-feature
- priority:P3
- status:open
depends_on: []
blocks: []
related:
- SP9-501
upstream:
- Fedora (new package)
- PipeWire
source: issues/src/5-audio-display-wireless.yaml
---

# SP9-502: Speakers sound thin without the Windows Surface APO tuning

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P3 | audio | missing-feature | partial | partial | partial |

## Problem

The speakers work but sound tinny compared to Windows. Speaker hiss while headphones play is a separate
small issue (Auto-Mute Mode).

## Origin

Windows applies a Surface audio processing object (SurfaceAPO_1284.json); Linux has no equivalent preset.

## Reports

- [linux-surface#168](https://github.com/linux-surface/linux-surface/issues/168) (open issue, workaround) "Sound is Tinny and hollow - SB2 15"": sound tinny; petm5 posted an SP9 impulse response; StollD suggests an asahi-audio style package
- [antoinecellerier/speaker-tuning-to-easyeffects#113](https://github.com/antoinecellerier/speaker-tuning-to-easyeffects/issues/113) (closed) "Microsoft Surface Pro 9": SP9 user confirms the converted preset sounds much better

## Fixes, patches and PRs

- [github.com/antoinecellerier/speaker-tuning-to-easyeffects](https://github.com/antoinecellerier/speaker-tuning-to-easyeffects): converts the Windows APO to a PipeWire filter chain or EasyEffects preset

## Possible solutions

- Ship the converted SP9 preset as an opt-in Fedora package (filter-chain config matched by DMI), in the asahi-audio style.
- Hiss: amixer sset 'Auto-Mute Mode' Disabled.

## Next steps

- [ ] Try the preset on an SP9; decide whether a package is worth it.

## Upstream and people

- Upstream target: Fedora (new package), PipeWire
- People: antoinecellerier, petm5, StollD

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-501](SP9-501-internal-microphone-gain-is-too-high-noisy-clipped-recording.md) Internal microphone gain is too high (noisy, clipped recordings)

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/5-audio-display-wireless.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
