# Research digests

One digest per source that was read. Each digest has the snapshot date in its title, says how the source was gathered, and points to its row-level table in `data/indexes/`. Conclusions from these digests are carried into `status.yaml`, the subsystem pages and `issues/`; the digests keep the evidence.

| Digest | Source | Snapshot | Table |
|---|---|---|---|
| `discussions-digest.md` | linux-surface discussions (80 relevant of 319) | 2026-11-12 (2282: 2026-11-16) | `data/indexes/discussions.tsv` |
| `wiki-digest.md` | linux-surface, iptsd, SAM and kernel wikis, with page history | 2026-11-13 | none |
| `closed-issues.md` | 207 closed SP9 and sibling issues, read in full | 2026-11-13 | `data/indexes/closed-issues.tsv` |
| `open-issues.md` | 288 open SP9 and sibling issues, read in full | 2026-11-14 | `data/indexes/open-issues.tsv` |
| `closed-prs.md` | 70 closed, unmerged PRs by people in the org | 2026-11-13 | `data/indexes/closed-prs.tsv` |
| `open-prs.md` | 61 open PRs by people in the org | 2026-11-13 | `data/indexes/open-prs.tsv` |
| `external-projects.md` | repos, gists and branches outside the org, found from every link | 2026-11-13 | `data/indexes/external-repos.yaml`, `data/indexes/branches.tsv`, `data/indexes/gists.tsv` |
| `outside-trackers.md` | Red Hat and kernel Bugzilla, kernel-ark MRs, libcamera patchwork, other projects' issues | 2026-11-13 | `data/indexes/trackers.tsv` |
| `upstream-efforts.md` | mainline history, patchwork, upstream project trees and trackers, ITHC upstream path | 2026-11-14 | `data/indexes/upstream-efforts.tsv`, `data/indexes/upstream-submissions.tsv` |

Patch series and fork analysis have no digest; they are generated tables: `data/indexes/patches-*.md` and `data/indexes/fork-deltas.md` (see `tools/README.md`).

## Method

- GitHub repos, wikis and patch series were cloned with git and read locally.
- Bugzilla, GitLab, patchwork, Discourse and GitHub issue threads were read through a logged-out browser session with the functions in `tools/browser/harvest.js`.
- Only public sources were used. Every fact carries a pointer to its source (`docs/conventions.md`).

## Limits

The following could not be read. Nothing was done to get around verification pages.

- Reddit (r/SurfaceLinux): the browser extension refused to navigate there.
- patchwork full-text searches over long date ranges: time out. Use msgid lookups or short `since` windows instead.
- freedesktop GitLab, web pages and API (libinput, iio-sensor-proxy#432, libcamera git): verification page. The libinput quirk state comes from an installed copy of its quirk files.
