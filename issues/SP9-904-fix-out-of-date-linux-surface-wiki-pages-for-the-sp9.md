---
id: SP9-904
title: Fix out-of-date linux-surface wiki pages for the SP9
labels:
- area:meta
- kind:docs
- priority:P3
- status:open
depends_on:
- SP9-901
blocks: []
related:
- SP9-201
- SP9-205
- SP9-903
upstream:
- linux-surface wiki
source: issues/src/9-meta.yaml
---

# SP9-904: Fix out-of-date linux-surface wiki pages for the SP9

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P3 | meta | docs | n/a | n/a | n/a |

## Problem

The support table, camera table, Disk-Encryption module list (Pro 8/9 missing, Fedora example incomplete),
the SL5 pinctrl module name and the SP9 page (initramfs-tools steps under a mkinitcpio heading, lid wake and
iptsd start-up missing) are wrong or stale.

## Origin

The wiki is editable by any GitHub user and maintainers ask contributors to update it.

## Reports

- [docs/research/wiki-digest.md](../docs/research/wiki-digest.md): list of wrong pages

## Fixes, patches and PRs

- none yet

## Possible solutions

- Edit the pages with sources from this KB.

## Next steps

- [ ] Low effort, visible; do after phase 0 confirms the facts.

## Upstream and people

- Upstream target: linux-surface wiki
- People: none

## Linked issues

- Depends on: [SP9-901](SP9-901-baseline-test-of-an-sp9-on-stock-fedora-logs-ids-initramfs-p.md) Baseline test of an SP9 on stock Fedora (logs, IDs, initramfs, per-feature check)
- Blocks: none
- Related: [SP9-201](SP9-201-type-cover-does-not-work-at-the-luks-passphrase-prompt-dracu.md) Type Cover does not work at the LUKS passphrase prompt (dracut lacks surface_aggregator_hub), [SP9-205](SP9-205-power-and-volume-buttons-dead-when-soc-button-array-probes-b.md) Power and volume buttons dead when soc_button_array probes before the pin controller, [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md) Goal: SP9 fully usable on the stock Fedora kernel and packages

## Knowledge base

- [docs/research/wiki-digest.md](../docs/research/wiki-digest.md)

_Generated from `issues/src/9-meta.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
