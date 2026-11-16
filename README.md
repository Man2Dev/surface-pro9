# Surface Pro 9 on Fedora: upstreaming knowledge base

Map of everything that affects the Surface Pro 9 (Intel) on Linux: what works in mainline, what lives in linux-surface, what lives only in forks and open PRs, what was posted upstream, and what to do next. The goal is an SP9 that works on a stock Fedora install with no external repo, by getting fixes upstream (kernel, dracut, libwacom, libcamera, iio-sensor-proxy, Fedora packages). Context: discussion linux-surface/linux-surface#2282.

Built from public sources only. Snapshot: 2026-11-12 to 2026-11-14 (per-source dates in `docs/research/README.md`). Mainline reference: v7.4-rc2. linux-surface reference: patches/7.3 (BASE v7.3.4).

## Start here

| You want | Read |
|---|---|
| What is broken and what to do about it | `issues/README.md`: 54 issues, one per problem, with to-do list by priority and dependency tree |
| The state of one feature, machine readable | `status.yaml` |
| The plan, in order | `docs/roadmap.md` |
| To make your SP9 work today | `docs/workarounds.md` |
| To test something on an SP9 | `docs/testing.md` |
| Background on one area | `docs/subsystems/` (camera, touch-pen, keyboard-sam-power, boot-initramfs-fedora, audio-display-wireless), `docs/hardware.md` |
| The evidence behind a claim | `docs/research/` (digests) and `data/indexes/` (tables) |
| To work on the repo as an agent or script | `AGENTS.md` |

## Headline findings

Touch and pen
- The big downstream block. ITHC (ADL-P THC in legacy mode) was never posted to linux-input; mainline intel-thc-hid covers only MTL and newer, and quo will not carry ITHC upstream under a pseudonym. A Fedora-derived kernel plus an out-of-tree ITHC module already gives full touch (bazzite-surface).
- Most "touch not working" reports were iptsd missing. iptsd is not in Fedora, no review request exists, and all its dependencies are in rawhide. Seven small iptsd PRs that fix start-up and pen problems merge cleanly and have no maintainer reply.
- libwacom has no SP9 data upstream and refused out-of-tree buses twice (libwacom#92, #400). The real unsolved bug is touch dying after resume (closed stale three times); an orphaned ITHC suspend fix from closed #2210 is in `orphaned-patches/`.

Type Cover, buttons, sensors
- The SP9 button race is fixed in mainline (ed22ad5fdbdb, 7.3 and stable 7.2.8+).
- dracut needs only `surface_aggregator_hub` for the cover at the LUKS prompt; everything else is already installed in Fedora's default mode.
- New upstream candidates from open threads: a `surface_hid` -ENODEV fix for the 2 min Fedora boot stall (#1845), iio-sensor-proxy hysteresis 0 for the SP9 sensor hub (#2160), and a `hid-sensor-trigger` runtime PM fix (#2160). The keyboard backlight patch on platform-driver-x86 targets 045E:09AE, the SP9 cover, and wants a Tested-by.

Power
- Everything Maximilian Luz sent for the SAM landed. What stayed downstream for the SP9 was never posted: the surface_gpe lid wake entry and the PCI shutdown quirk. A maintainer SP9 + SL5 lid wake patch sits in open linux-surface#2011, and a ready vendor match patch in a gist.
- Further candidates: clearing the fan floor Windows leaves (#1726, SAM FAN 0x0b), a SAM restore retry after hibernate (#2294), and two s2idle leads from the SL5 (SOF DSP in D0, #1010; INTC1055 PADCFG0, kernel#162). `pci=hpiosize=0` can cost lid wake (#1082); battery stuck at 50 % is a UEFI or Windows setting (#1781).

Cameras
- Mostly upstream in 7.4: OVTI5693 HID, OV5693 clock gating on IPU6, ipu-bridge configs and the SP9 upside-down quirks. The front camera still needs the ov5693 binned-mode patch (owner found, not posted yet). libcamera tuning for both sensors was posted on 2026-11-13 and wants a Tested-by. IR (VD55G0) is on linux-media in two competing series.

Audio, display, wireless
- Realtek mic gain quirk exists only in a fork and was never sent. The speakers need the Windows APO voicing, which converts to a PipeWire filter chain.

Fedora and process
- Fedora's kernel config already enables everything needed; the gaps are upstream code, one dracut module and missing Fedora packages. Fedora takes camera backports through kernel-ark merge requests.
- The most complete SP9 consolidation is CmdrShepardsPie/linux-surface-contrib (7.3.1-pro9) with a COPR; the best SP9 camera branch is petm5/linux `surface-devel-v7.3`.
- The linux-surface Fedora repo has lagged almost every Fedora release. 178 of 288 open SP9 and sibling issues never got a maintainer reply, and 17 open SP9 issues are already fixed.

## Layout

```
README.md              this file
AGENTS.md              rules and formats for agents and scripts
status.yaml            per-feature status, stable feature keys (machine readable)
issues/                one Markdown issue per problem, generated from issues/src/*.yaml
docs/
  roadmap.md           what to do, in order, with issue ids
  workarounds.md       user-side fixes on Fedora today
  testing.md           commands to test on an SP9 and how to report results
  hardware.md          SP9 identifiers (SAM HID nodes, PCI ids, SKUs)
  conventions.md       vocabulary, reference syntax, attribution rules
  subsystems/          one page per area
  research/            digests of each source that was read, with dates, method and limits
data/
  indexes/             evidence tables (TSV, YAML) and generated patch and fork views
  curated/             hand-maintained classification (edit, then regenerate)
  generated/           raw tool output (JSON)
orphaned-patches/      code from closed PRs that exists nowhere else, with original authorship
tools/                 scripts that produce data/ and issues/
```
