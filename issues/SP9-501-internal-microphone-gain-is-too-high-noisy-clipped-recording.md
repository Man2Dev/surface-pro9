---
id: SP9-501
title: Internal microphone gain is too high (noisy, clipped recordings)
labels:
- area:audio
- kind:upstreaming
- priority:P2
- status:open
depends_on: []
blocks:
- SP9-903
related:
- SP9-502
upstream:
- linux-sound (Takashi Iwai)
source: issues/src/5-audio-display-wireless.yaml
---

# SP9-501: Internal microphone gain is too high (noisy, clipped recordings)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P2 | audio | upstreaming | broken | broken | broken |

## Problem

The SP9 internal microphone is far too loud and noisy with default mixer settings.

## Origin

Realtek ALC274 (codec 10EC0274, subsystem 10EC1284): the default 'Internal Mic Boost' is too high.
A quirk limiting it exists only in CmdrShepardsPie's fork (0016-sound); nothing was posted to alsa-devel.
The SP8 shows the same symptom; a SOF developer confirmed lowering the boost fixes it.

## Reports

- [thesofproject/linux#5509](https://github.com/thesofproject/linux/issues/5509) (open) "[TGL] Mic is not visible on Surface Pro 8 (SOF forced with dsp_driver=3)": SP8 mic: Internal Mic Boost 0 fixes it; SP8 has no DMIC
- [CmdrShepardsPie/surface-kernel-copr#10](https://github.com/CmdrShepardsPie/surface-kernel-copr/issues/10) (closed) "Carry the Surface Pro 9 mic gain fix (fixups/0004), release 2": COPR carries the SP9 mic gain fix

## Fixes, patches and PRs

- [github.com/CmdrShepardsPie/linux-surface-contrib](https://github.com/CmdrShepardsPie/linux-surface-contrib): 'ALSA: hda/realtek: Limit internal mic gain on Microsoft Surface Pro 9' (fork patch 0016)

## Possible solutions

- Post the realtek quirk to alsa-devel / linux-sound with Chris Simpson's authorship (Takashi Iwai merges these quickly).
- Workaround: amixer -c0 sset 'Internal Mic Boost' 0.

## Next steps

- [ ] Ask CmdrShepardsPie for permission, test on the SP9, send.

## Commands

```
amixer -c0 sset 'Internal Mic Boost' 0
```

## Upstream and people

- Upstream target: linux-sound (Takashi Iwai)
- People: CmdrShepardsPie, ujfalusi

## Linked issues

- Depends on: none
- Blocks: [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-502](SP9-502-speakers-sound-thin-without-the-windows-surface-apo-tuning.md) Speakers sound thin without the Windows Surface APO tuning

## Knowledge base

- [docs/subsystems/audio-display-wireless.md](../docs/subsystems/audio-display-wireless.md)
- [docs/research/upstream-efforts.md](../docs/research/upstream-efforts.md)

_Generated from `issues/src/5-audio-display-wireless.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
