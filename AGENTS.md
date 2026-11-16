# Instructions for agents

## Where things live

| Layer | Path | Edit by hand |
|---|---|---|
| Per-feature state | `status.yaml` (feature keys are stable ids) | yes |
| Per-problem issues | `issues/src/*.yaml` (source), `issues/*.md`, `issues/issues.json` (generated) | source only |
| Plan | `docs/roadmap.md` | yes |
| Explanations | `docs/subsystems/*.md`, `docs/hardware.md`, `docs/workarounds.md`, `docs/testing.md` | yes |
| Evidence digests | `docs/research/*.md` (index with dates and limits in `docs/research/README.md`) | yes |
| Evidence tables | `data/indexes/*.tsv`, `data/indexes/*.yaml` | yes, except `patches-*` and `fork-deltas.md` |
| Generated views | `data/indexes/patches-*.{yaml,md}`, `data/indexes/fork-deltas.md`, `data/generated/` | no, rerun `tools/` |
| Curated input | `data/curated/sp9-relevance.yaml` | yes |
| Orphaned code | `orphaned-patches/` | no, keep original authorship |

## Read order

1. `issues/README.md` for the problems and their priorities, or `status.yaml` for a feature.
2. `docs/roadmap.md` for the order of work.
3. The subsystem page in `docs/subsystems/` for the area you work on.
4. Evidence: the digest in `docs/research/` for the source, then its table in `data/indexes/` (the digest index says which table belongs to which source).

## Keeping layers in sync

- `issues/` is generated: edit `issues/src/*.yaml` and run `python3 tools/build_issues.py`. It fails on unknown issue ids, bad reference syntax or missing KB paths. Reference syntax is documented at the top of the script and in `issues/README.md`.
- A new finding goes into the subsystem page or digest with a pointer, then into `status.yaml`, then into the matching issue YAML; if it is actionable, also into `docs/roadmap.md` with the issue id.
- Run `python3 tools/check_repo.py` before committing; it must report 0 problems.
- Test results from a real SP9: post them publicly where the problem is tracked, then link that post from the issue (`docs/testing.md`).

## Identifier formats

- `#N`: linux-surface/linux-surface issue, PR or discussion N.
- `repo#N`: another repo in the linux-surface org (`kernel#169`, `iptsd#171`, `surface-gpe#7`).
- `owner/repo#N`: outside the org.
- `repo@sha` or `owner/repo@sha`: a commit (10+ hex chars).
- `lore:<list>/<msgid>` or a bare msgid in `upstream-submissions.tsv`: open as `https://lore.kernel.org/r/<msgid>`.
- `SP9-NNN`: an issue in `issues/`. Hundreds digit is the area: 1 touch and pen, 2 cover, input and sensors, 3 power, 4 camera, 5 audio, display and wireless, 6 boot, packaging and firmware, 9 meta.

## File formats

- TSV files: lines starting with `# ` (hash + space) are comments, then one header line, then rows. Tab separated, no quoting. Strip comment lines with `grep -v '^# '` (not `^#`: linux-surface ids start with `#`), then parse as TSV. Trailing empty columns are padded.
- YAML: `status.yaml`, `issues/src/*.yaml`, `data/indexes/repos.yaml`, `data/indexes/external-repos.yaml`, `data/indexes/patches-*.yaml`, `data/curated/sp9-relevance.yaml`.
- Generated files say so in their header. Do not edit them by hand: change the input or the curated YAML and rerun the tool.

## Updating

- New patch series version: run the pipeline in `tools/README.md`, then review rows whose `sp9_relevance` is `unclassified` and add them to `data/curated/sp9-relevance.yaml`.
- Keep the snapshot date in file headers and in `docs/research/README.md` current when you refresh a source.

## Rules

- Public data only. No per-person folders, no private contact details, no unpublished logs. Cite people by their public handle and only for what they posted publicly.
- No em dashes or en dashes in anything you write here. Use commas, colons, or "to".
- Never state that something is upstream without a source check (`tools/upstream_check.py` or reading the mainline file) or a merged commit id.
- Credit authors. When proposing to upstream someone's patch, keep their authorship and ask them first (see `docs/conventions.md`).
- Commit with a descriptive message; do not add AI attribution trailers.
- lore.kernel.org and patchwork web pages sit behind a bot challenge. Do not try to get around it. The patchwork REST API (`https://patchwork.kernel.org/api/1.3/patches/?project=<p>&q=<text>`) answers without it.
