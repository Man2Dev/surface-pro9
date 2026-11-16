---
id: SP9-112
title: Package ITHC as a signed out-of-tree module (akmod/kmod) for the stock Fedora kernel
labels:
- area:touch
- kind:packaging
- priority:P2
- status:open
depends_on: []
blocks: []
related:
- SP9-101
- SP9-102
upstream:
- RPM Fusion or Terra
source: issues/src/1-touch-pen.yaml
---

# SP9-112: Package ITHC as a signed out-of-tree module (akmod/kmod) for the stock Fedora kernel

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P2 | touch | packaging | n/a | n/a | broken |

## Problem

Until ITHC is upstream (SP9-101), touch on the stock Fedora kernel needs the module built out of tree. No
Fedora-side package does that today.

## Origin

bazzite-surface shows it works: quo/ithc-linux built against the distro kernel-devel and signed with a MOK
gives full touch while everything else runs on the stock kernel.

## Reports

- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": goal: stock Fedora without the linux-surface kernel

## Fixes, patches and PRs

- [github.com/John-S-Reddick/bazzite-surface](https://github.com/John-S-Reddick/bazzite-surface): builds and MOK-signs quo/ithc-linux for Bazzite's Fedora-based kernel
- [quo/ithc-linux](https://github.com/quo/ithc-linux): the out-of-tree driver

## Possible solutions

- An akmod in RPM Fusion or Terra (Fedora itself does not accept kernel modules), with akmods signing via the user's MOK.

## Next steps

- [ ] Write an akmod spec from bazzite-surface's build steps; test with Secure Boot on an SP9.

## Upstream and people

- Upstream target: RPM Fusion or Terra
- People: quo

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-101](SP9-101-touchscreen-and-pen-need-the-out-of-tree-ithc-driver-no-upst.md) Touchscreen and pen need the out-of-tree ITHC driver (no upstream driver for the ADL THC in legacy mode), [SP9-102](SP9-102-iptsd-is-not-packaged-in-fedora.md) iptsd is not packaged in Fedora

## Knowledge base

- [docs/research/outside-trackers.md](../docs/research/outside-trackers.md)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
