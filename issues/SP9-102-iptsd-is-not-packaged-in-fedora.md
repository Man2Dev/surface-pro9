---
id: SP9-102
title: iptsd is not packaged in Fedora
labels:
- area:touch
- kind:packaging
- priority:P1
- status:open
depends_on: []
blocks:
- SP9-903
related:
- SP9-101
- SP9-105
- SP9-111
- SP9-112
- SP9-603
upstream:
- Fedora package review
source: issues/src/1-touch-pen.yaml
---

# SP9-102: iptsd is not packaged in Fedora

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P1 | touch | packaging | n/a | works | broken |

## Problem

Multitouch and pen on the SP9 need the iptsd daemon. Fedora does not ship it; users take it from the
linux-surface repo or Terra.

## Origin

Nobody filed a Fedora package review (Red Hat Bugzilla search, 2026-11-14). Repology lists iptsd only in
AUR, nixpkgs, Solus and Terra. Every build dependency is already in Fedora rawhide: cli11-devel,
eigen3-devel 5.0.1 (the version iptsd's wrap pins), fmt-devel, inih-cpp, guidelines-support-library-devel,
spdlog-devel; the optional tools need sdl2-compat and cairomm. No bundling is needed.

## Reports

- [linux-surface discussion 2282](https://github.com/linux-surface/linux-surface/discussions/2282) (discussion) "Collecting scattered SP9 fixes for upstreaming, links welcome": iptsd has to come from a third-party repo
- [linux-surface/repo#15](https://github.com/linux-surface/repo/issues/15) (closed issue, fixed-package) "Fedora 42 Repo is missing iptsd": linux-surface Fedora 42 repo was missing iptsd
- [ublue-os/bazzite#3426](https://github.com/ublue-os/bazzite/issues/3426) (closed) "iptsd daemon missing for Microsoft Surface hardware": iptsd daemon missing on Bazzite

## Fixes, patches and PRs

- [terrapkg/packages#16814](https://github.com/terrapkg/packages/issues/16814) (closed) "add: iptsd": Terra iptsd package (spec reference)
- [linux-surface/iptsd#120](https://github.com/linux-surface/iptsd/issues/120) (open issue, tracker) "Announcements and updates for downstreams": upstream announcements for downstream packagers

## Possible solutions

- Package iptsd for Fedora from upstream 3.1.1 against system libraries; ship the udev rule and iptsd@.service; split the debug tools into a subpackage.
- Fix the udev and service issues first or carry them as patches (SP9-105).

## Next steps

- [ ] Write the spec, build in mock against rawhide, file a Review Request in Red Hat Bugzilla.

## Commands

```
git clone https://github.com/linux-surface/iptsd
fedpkg --release rawhide mockbuild
```

## Upstream and people

- Upstream target: Fedora package review
- People: StollD

## Linked issues

- Depends on: none
- Blocks: [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md)
- Related: [SP9-101](SP9-101-touchscreen-and-pen-need-the-out-of-tree-ithc-driver-no-upst.md) Touchscreen and pen need the out-of-tree ITHC driver (no upstream driver for the ADL THC in legacy mode), [SP9-105](SP9-105-iptsd-service-and-udev-rule-are-fragile-stops-after-cold-boo.md) iptsd service and udev rule are fragile (stops after cold boot, probes every hidraw, loses its tag), [SP9-111](SP9-111-libwacom-has-no-sp9-tablet-description-pen-and-touch-not-rec.md) libwacom has no SP9 tablet description (pen and touch not recognised as a tablet), [SP9-112](SP9-112-package-ithc-as-a-signed-out-of-tree-module-akmod-kmod-for-t.md) Package ITHC as a signed out-of-tree module (akmod/kmod) for the stock Fedora kernel, [SP9-603](SP9-603-linux-surface-fedora-repository-lags-releases-and-recently-p.md) linux-surface Fedora repository lags releases and recently published broken files

## Knowledge base

- [status.yaml](../status.yaml)
- [data/indexes/upstream-efforts.tsv](../data/indexes/upstream-efforts.tsv)

_Generated from `issues/src/1-touch-pen.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
