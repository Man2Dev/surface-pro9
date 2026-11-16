# Orphaned code from closed pull requests

Code that only exists in closed, unmerged PRs whose authors promised a follow-up that never came. Kept here with the original authorship so it is not lost. Neither patch was built or tested in this repo. Ask the author before sending either one anywhere, and keep their From and Signed-off-by.

| File | Source | Applies to | Status |
|---|---|---|---|
| `linux-surface-2210-ithc-pm-preserve-hid-device.patch` | linux-surface/linux-surface#2210, patch 0010 of the 7.0 series (RowdyRagamuffin) | `drivers/hid/ithc/ithc-main.c` in linux-surface/kernel v7.3-surface (`patch -p1 --dry-run` clean) | AI-assisted; author closed the PR with unresolved errors in the wider series |
| `iptsd-227-retain-lost-contacts.rebased-on-9c7a554.patch` | linux-surface/iptsd#227 (cunninghamcard-bit) | iptsd master 9c7a554 (`git am -3` clean, only the context lines moved) | Not built; adds tracking options to etc/iptsd.conf |

Test the ITHC patch on an SP9 kernel build:

```
cd linux-surface-kernel
git checkout v7.3-surface
git am /path/to/orphaned-patches/linux-surface-2210-ithc-pm-preserve-hid-device.patch
```

Test the iptsd patch:

```
git clone https://github.com/linux-surface/iptsd.git && cd iptsd
git am /path/to/orphaned-patches/iptsd-227-retain-lost-contacts.rebased-on-9c7a554.patch
meson setup build && ninja -C build
```
