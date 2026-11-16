# Conventions

## Writing style

- Public sources only: every fact must be checkable by anyone from its pointer. No per-person folders or private details.
- No em dashes or en dashes anywhere. Use commas, colons, or "to" for ranges.
- Every claim gets a pointer: an issue (`#1234` means linux-surface/linux-surface), `repo#N` for other linux-surface repos, `owner/repo#N` outside the org, a commit (`repo@sha`), a patchwork msgid, or a file path in this repo.
- Dates are ISO (YYYY-MM-DD). The snapshot date of a data file is in its header.

## Status vocabulary (status.yaml)

| value | meaning |
|---|---|
| works | stock mainline or Fedora kernel with stock userspace |
| works-ls | only with the linux-surface kernel and/or its userspace packages |
| works-fork | only with patches that live in forks or open PRs |
| partial | works with caveats or workarounds |
| broken | known not to work anywhere |
| unknown | no data, needs a test on a real SP9 |

## Upstream class (discussion 2282)

| value | meaning |
|---|---|
| upstreamable | could be sent roughly as is |
| rework | works, but needs rework first (design, code quality, justification) |
| downstream | downstream by nature (debug hacks, policy knobs, firmware workarounds, fixes to downstream-only code) |
| superseded | an equivalent change is already in mainline |
| unknown | not assessed |

## SP9 relevance (data/curated/sp9-relevance.yaml)

critical, high, medium, low, none, verify. A trailing `*` in generated tables means a keyword guess, not a curated value.

## Mainline apply check (tools/upstream_check.py)

| value | meaning |
|---|---|
| not-upstream | applies cleanly on top of the earlier commits of the series |
| upstream | reverse-applies on pristine mainline |
| partial/diverged | neither; usually means mainline changed nearby code or already has part of it. Needs a human look. |

## Attribution when upstreaming

Original author stays in `From:`. Nobody else's `Signed-off-by` is added without their agreement. If the author cannot be reached or the code needs a rewrite, write a new implementation and credit with `Suggested-by:` or `Co-developed-by:` (with consent) and a `Link:` to the original.
