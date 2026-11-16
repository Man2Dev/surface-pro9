# Tools

All scripts are Python 3 (PyYAML needed for the build_* scripts). Run from the repo root unless noted.

| Script | Input | Output |
|---|---|---|
| `parse_patches.py OUT.json SERIES/*.patch` | a linux-surface `patches/<ver>/` dir | per-commit metadata: author, date, subject, files, Link/Fixes tags, SP9/SP8 mentions |
| `upstream_check.py SERIES_DIR MAINLINE OUT.json` | series dir, mainline checkout | per-commit apply result against mainline (cumulative) |
| `build_patch_index.py VER PARSED.json CHECK.json LABEL` | the two JSONs + `data/curated/sp9-relevance.yaml` | `data/indexes/patches-<label>.{yaml,md}` |
| `fork_commits.py OUT.json` | run inside a linux-surface clone with fork remotes fetched | all commits in forks that are not in origin |
| `fork_delta.py REF VER [BASE]` | inside the clone | commits in REF's `patches/VER` not in BASE's |
| `all_fork_deltas.py OUT.json` | inside the clone | patch commits carried by any fork and absent from all upstream patch dirs |
| `build_fork_delta_md.py` | `data/generated/fork-deltas.json` + curated YAML | `data/indexes/fork-deltas.md` |
| `fork_branches.py OUT.json LS_CLONE` | linux-surface clone with fork remotes | branches ahead of all origin branches (part A) |
| `kernel_fork_branches.py OUT.json KERNEL_CLONE LS_CLONE` | linux-surface/kernel clone with `f_<owner>_<repo>` remotes | novel commits per feature branch (part B) |
| `build_branches_tsv.py A.json B.json OUT.tsv` | the two outputs above | `data/indexes/branches.tsv` |
| `urls_local.py OUT.json WIKI LS EXT FORKCOMMITS.json` | wiki, linux-surface and external clones, `fork_commits.py` output | every URL and where it was seen |
| `agg_urls.py IN.json OUT.json` | `urls_local.py` output plus browser-harvested URLs | URLs grouped by GitHub repo and host |
| `closed_pr_novel.py LS_CLONE OUT.json N [N ...]` | linux-surface clone with `git fetch origin '+refs/pull/*/head:refs/pr/*'` | patch subjects a PR adds that no `patches/` dir on master carries |
| `build_issues.py` | `issues/src/*.yaml` + `data/indexes/*.tsv` | `issues/SP9-*.md`, `issues/README.md`, `issues/refs.md`, `issues/issues.json` |
| `inspect_repos.py LIST OUT.json [CLONE_DIR]` | owner/repo list | branches, last commit, license, README head, SP9 keyword hits (clones are not executed) |
| `check_repo.py` | the whole repo | broken links and paths, dashes, absolute workspace paths, YAML parse errors, TSV column counts (run before every commit) |

## Full refresh

```
# 1. sources
git clone https://github.com/linux-surface/linux-surface.git ls
mkdir mainline && cd mainline && git init -q && git remote add o https://github.com/torvalds/linux.git
git config core.sparseCheckout true
python3 - <<'EOF'   # sparse paths = every file touched by the series
import json,glob
fs=set()
for p in glob.glob('../kb/data/generated/*parsed.json'):
    for c in json.load(open(p)): fs|=set(c['files'])
open('.git/info/sparse-checkout','w').write('\n'.join(sorted(fs)+['MAINTAINERS','drivers/bluetooth/','sound/hda/codecs/realtek/'])+'\n')
EOF
git fetch -q --depth=1 --filter=blob:none o master && git checkout -q FETCH_HEAD && cd ..

# 2. series metadata and mainline check
python3 kb/tools/parse_patches.py kb/data/generated/linux-surface-7.3.parsed.json ls/patches/7.3/*.patch
python3 -I kb/tools/upstream_check.py ls/patches/7.3 mainline kb/data/generated/linux-surface-7.3.mainline-check.json
python3 kb/tools/build_patch_index.py 7.3 kb/data/generated/linux-surface-7.3.parsed.json kb/data/generated/linux-surface-7.3.mainline-check.json "linux-surface 7.3"

# 3. forks (list active forks from https://github.com/linux-surface/linux-surface/forks?include=active&period=1y)
cd ls
for f in $(cat ../forks.txt); do git remote add $(echo $f|tr / _) https://github.com/$f.git; done
git fetch --all --no-tags -q
python3 ../kb/tools/all_fork_deltas.py ../kb/data/generated/fork-deltas.json
cd .. && python3 kb/tools/build_fork_delta_md.py
```

Paths in the new-file sparse list may move between kernel versions (btusb.c moved to btusb_main.c in 7.4): a "missing files" note in the check output means look by hand.

## External repos and branches

```
# kernel forks: list from https://github.com/linux-surface/kernel/forks, one remote per fork
cd kernel && git remote add f_owner_repo https://github.com/owner/repo.git
git ls-remote --heads f_owner_repo           # pick feature branches
git fetch --depth=40 --filter=tree:0 f_owner_repo +refs/heads/B:refs/remotes/f_owner_repo/B   # one at a time
cd .. && python3 kb/tools/kernel_fork_branches.py kb/data/generated/kernel-fork-feature-branches.json kernel ls
python3 kb/tools/fork_branches.py kb/data/generated/linux-surface-fork-branches.json ls
python3 kb/tools/build_branches_tsv.py kb/data/generated/linux-surface-fork-branches.json kb/data/generated/kernel-fork-feature-branches.json kb/indexes/branches.tsv
# links: local sources, then add the browser-harvested issue/discussion URLs and aggregate
python3 kb/tools/urls_local.py urls.json wiki ls ext forkcommits.json
python3 kb/tools/agg_urls.py urls.json kb/data/generated/urls-local-sources.json
python3 -I kb/tools/inspect_repos.py repos.txt inspect.json ext
```

`data/indexes/external-repos.yaml` is curated by hand from `inspect.json` and the READMEs; `data/generated/external-repos-inspect.json` keeps the raw record (READMEs cut to 600 characters).

## Bug trackers and other projects

See `tools/browser/README.md`: `harvest.js` holds the Bugzilla, GitLab, patchwork, Discourse and GitHub search helpers used for `data/indexes/trackers.tsv`. New repos found there are inspected with `inspect_repos.py`.

## GitHub and patchwork harvests

The issue, PR, discussion and patchwork indexes were harvested in a logged-in browser:
- issues and PRs: `https://api.github.com/search/issues?per_page=100&q=org:linux-surface <term>` (unauthenticated, 10 requests per minute), then each page's embedded JSON for comments and cross references;
- discussions: `https://github.com/search?q=org:linux-surface&type=discussions` with `Accept: application/json`;
- patchwork: `https://patchwork.kernel.org/api/1.3/patches/?project=<p>&q=<term>&since=2021-06-01T00:00:00`.
Search terms are listed in the header of each TSV. With a GitHub token, `gh api` can reproduce the same in a script.
