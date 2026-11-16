---
id: SP9-406
title: Camera fails to re-probe after intel-ipu6 reload or hibernate
labels:
- area:camera
- kind:bug
- priority:P3
- status:fix-pending
depends_on: []
blocks: []
related:
- SP9-306
- SP9-401
upstream:
- linux-media
source: issues/src/4-camera.yaml
---

# SP9-406: Camera fails to re-probe after intel-ipu6 reload or hibernate

| Status | Priority | Area | Kind | Mainline | linux-surface | Fedora |
|---|---|---|---|---|---|---|
| fix-pending | P3 | camera | bug | broken | broken | broken |

## Problem

After unloading and reloading intel-ipu6, or after hibernation, ov5693 does not probe again.

## Origin

ipu-bridge software nodes reference the module image and are not reusable on rebind.

## Reports

- [linux-surface discussion 2202](https://github.com/linux-surface/linux-surface/discussions/2202) (discussion) "Windows-like lid behavior on the Surface Pro 9: suspend, then hibernate after a delay": camera re-probe bug after resume

## Fixes, patches and PRs

- [lore:20261026082549.662885-2-dmanresa@gmail.com](https://lore.kernel.org/r/20261026082549.662885-2-dmanresa@gmail.com) (linux-media, new, D. Manresa, 2026-10-26) "[v3] media: ipu-bridge: survive module unload and reuse the software nodes on rebind": ipu-bridge: survive module unload (D. Manresa v5, author cannot respin)

## Possible solutions

- Test v5 on the SP9 and reply with Tested-by; someone may need to carry later versions.

## Next steps

- [ ] Low priority.

## Upstream and people

- Upstream target: linux-media
- People: D. Manresa

## Linked issues

- Depends on: none
- Blocks: none
- Related: [SP9-306](SP9-306-hibernate-is-unavailable-with-secure-boot-kernel-lockdown.md) Hibernate is unavailable with Secure Boot (kernel lockdown), [SP9-401](SP9-401-front-camera-ov5693-returns-empty-buffers-on-mainline-7-4-2x.md) Front camera (OV5693) returns empty buffers on mainline 7.4: 2x2 binned mode with flips fails

## Knowledge base

- [status.yaml](../status.yaml)

_Generated from `issues/src/4-camera.yaml` by `tools/build_issues.py`. Edit the YAML, not this file._
