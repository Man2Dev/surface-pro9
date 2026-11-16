---
id: SP9-306
title: Hibernate is unavailable with Secure Boot (kernel lockdown)
labels:
- area:power
- kind:upstreaming
- priority:P2
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-307
- SP9-406
upstream:
- linux-pm / LSM
source: issues/src/3-power.yaml
---

# SP9-306: Hibernate is unavailable with Secure Boot (kernel lockdown)

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P2 | power | upstreaming | broken | works | broken |

## Problem

With Secure Boot on, the kernel's lockdown disables hibernation. linux-surface carries a
lockdown_hibernate parameter.

## Origin

Upstream refuses unsigned hibernation images under lockdown. Kelvie Wong's lockdown_hibernate RFC (2023-11,
linux-surface 0001) got no follow-up. Three upstream proposals are active in 2026: Matthew Garrett's signed
hibernation images (changes requested 2026-10), Sean Rhodes' encrypted snapshot device (v3 resend
2026-09), and a TPM2 image encryption RFC (2026-03).

## Reports

- [linux-surface discussion 2202](https://github.com/linux-surface/linux-surface/discussions/2202) (discussion) "Windows-like lid behavior on the Surface Pro 9: suspend, then hibernate after a delay": suspend-then-hibernate recipe on SP9
- [docs/research/wiki-digest.md](../docs/research/wiki-digest.md): wiki HibernateMode=reboot note

## Fixes, patches and PRs

- [patchwork.kernel.org/project/linux-pm/list/?q=lockdown&archive=both](https://patchwork.kernel.org/project/linux-pm/list/?q=lockdown&archive=both): linux-pm patchwork: Garrett, Rhodes, TPM2 RFC, Kelvie Wong RFC
- [data/indexes/patches-linux-surface-7.3.md](../data/indexes/patches-linux-surface-7.3.md): 0001 lockdown_hibernate (downstream)

## Possible solutions

- Review and test the active lockdown hibernation series instead of carrying 0001.

## Next steps

- [ ] Follow Garrett's next version; test on the SP9 when it lands in linux-next.

## Upstream and people

- Upstream target: linux-pm / LSM
- People: Matthew Garrett, Sean Rhodes

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-307](SP9-307-type-cover-dead-after-resume-from-hibernation-sam-event-enab.md) Type Cover dead after resume from hibernation (SAM event enable times out), [SP9-406](SP9-406-camera-fails-to-re-probe-after-intel-ipu6-reload-or-hibernat.md) Camera fails to re-probe after intel-ipu6 reload or hibernate

## Knowledge base

- [docs/research/upstream-efforts.md](../docs/research/upstream-efforts.md)

_Generated from `issues/src/3-power.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
