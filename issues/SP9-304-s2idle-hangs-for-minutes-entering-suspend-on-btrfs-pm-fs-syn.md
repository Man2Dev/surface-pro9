---
id: SP9-304
title: s2idle hangs for minutes entering suspend on btrfs (pm_fs_sync)
labels:
- area:suspend
- kind:bug
- priority:P3
- status:open
depends_on: []
blocks: []
related:
- SP9-302
upstream:
- linux-btrfs
- linux-pm
source: issues/src/3-power.yaml
---

# SP9-304: s2idle hangs for minutes entering suspend on btrfs (pm_fs_sync)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P3 | suspend | bug | partial | partial | partial |

## Problem

Closing the lid starts suspend but the machine wedges for 10+ minutes in pm_fs_sync / sync_inodes_sb on a
btrfs root (Fedora's default filesystem).

## Origin

Unknown; stuck writeback before suspend. Not Surface specific in mechanism.

## Reports

- [linux-surface#2258](https://github.com/linux-surface/linux-surface/issues/2258) (open issue, unsolved) "SP9: s2idle hang in pm_fs_sync / sync_inodes_sb (btrfs), frozen UI until hard reset": SP9 s2idle hang in pm_fs_sync with btrfs

## Fixes, patches and PRs

- none yet

## Possible solutions

- Reproduce on Fedora btrfs; if reproducible, report to linux-btrfs / linux-pm with the hung task trace.

## Next steps

- [ ] Watch for 'blocked for more than 122 seconds' in the journal of an affected SP9.

## Upstream and people

- Upstream target: linux-btrfs, linux-pm
- People: dragged9698

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-302](SP9-302-sp9-sometimes-does-not-wake-from-s2idle-or-hangs-on-the-seco.md) SP9 sometimes does not wake from s2idle (or hangs on the second suspend)

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
