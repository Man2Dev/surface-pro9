---
id: SP9-602
title: Fedora installs a generic kernel as default over kernel-surface after updates
labels:
- area:packaging
- kind:bug
- priority:P3
- status:open
depends_on: []
blocks: []
related:
- SP9-603
- SP9-903
upstream:
- linux-surface packaging
source: issues/src/6-boot-packaging.yaml
---

# SP9-602: Fedora installs a generic kernel as default over kernel-surface after updates

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| open | P3 | packaging | bug | n/a | partial | n/a |

## Problem

When Fedora's kernel updates, it becomes the default boot entry and the surface kernel is skipped, despite
kernel-surface-default-watchdog.

## Origin

/etc/sysconfig/kernel UPDATEDEFAULT=yes makes new-kernel-pkg set every new kernel as default.

## Reports

- [linux-surface#1937](https://github.com/linux-surface/linux-surface/issues/1937) (open issue, workaround) "[Fedora KDE 43] Generic kernel sets to default after updating kernel": Fedora KDE 43: generic kernel set as default
- [linux-surface#1327](https://github.com/linux-surface/linux-surface/issues/1327) (open issue, workaround) "[SP9] Fedora 38 Latest Surface kernel not selected upon update": SP9 Fedora 38: surface kernel not selected after update
- [linux-surface#1054](https://github.com/linux-surface/linux-surface/issues/1054) (closed issue, fixed-package) "Fedora Default Kernel Updater doesn't work at all": Fedora default kernel updater (closed, history)

## Fixes, patches and PRs

- none yet

## Possible solutions

- UPDATEDEFAULT=no plus the watchdog; or fix the watchdog in linux-surface packaging.
- Goal state makes this moot: run the stock Fedora kernel (SP9-903).

## Next steps

- [ ] Only matters while running kernel-surface.

## Commands

```
sudo sed -i 's/^UPDATEDEFAULT=.*/UPDATEDEFAULT=no/' /etc/sysconfig/kernel
```

## Upstream and people

- Upstream target: linux-surface packaging
- People: none

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-603](SP9-603-linux-surface-fedora-repository-lags-releases-and-recently-p.md) linux-surface Fedora repository lags releases and recently published broken files, [SP9-903](SP9-903-goal-sp9-fully-usable-on-the-stock-fedora-kernel-and-package.md) Goal: SP9 fully usable on the stock Fedora kernel and packages

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/6-boot-packaging.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
