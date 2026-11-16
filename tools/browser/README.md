# Browser harvest

The cloud workspace that built this repo cannot reach Bugzilla, GitLab, patchwork, Discourse or the GitHub search API, so these sources were read through a logged-out browser session. `harvest.js` holds the functions used for `data/indexes/trackers.tsv` and the GitHub parts of `data/indexes/external-repos.yaml`.

| Source | Open first | Call |
|---|---|---|
| Red Hat Bugzilla | `https://bugzilla.redhat.com/rest/version` | `bugzilla(['Surface Pro','surface_aggregator','ov5693','int3472'])`, then `bugzillaComments([id, ...])` |
| kernel Bugzilla | `https://bugzilla.kernel.org/rest/version` | same functions; keep calls short, the JSON viewer page drops long-running scripts |
| kernel-ark MRs | `https://gitlab.com/cki-project/kernel-ark` | `gitlabMRs('cki-project/kernel-ark', ['surface','ipu6','int3472','ipu-bridge'])` |
| libcamera patchwork | `https://patchwork.libcamera.org/api/projects/` | `patchwork(['ov5693','ov13858','vd55g','ipu6'])` |
| Fedora Discussion | `https://discussion.fedoraproject.org/about` | `discourse(['surface pro 9','linux-surface'])`; tag list: `/tag/microsoft-surface.json` |
| GitHub | `https://github.com/robots.txt` | `githubSearch([['"surface pro 9" in:title -org:linux-surface', 1], ['Surface_Pro_9_2038', 1]])` |
| GitHub issue threads | `https://github.com/robots.txt` | `issueThread('linux-surface/linux-surface', 1845)` reads the page's embedded JSON (no quota, up to about 30 comments); when `total > comments.length`, `issueComments(repo, n, total)` fetches all of them through REST (60 requests per hour). Used for `data/indexes/open-issues.tsv` and `data/indexes/closed-issues.tsv` |
| Launchpad | open `https://api.launchpad.net/devel/ubuntu?ws.op=searchTasks&search_text=surface%20pro%209&ws.size=75` directly | read the JSON |

Notes:
- lore.kernel.org and patchwork.kernel.org web pages sit behind a bot challenge; use the patchwork REST API (`/api/1.3/`, with a `project` parameter) instead and do not try to get around the challenge.
- GitHub issue search drops quotes in bodies ("Surface Pro 9" matches any 9), so phrase searches need `in:title`.
- The repository `dracut-ng/dracut-ng` is now `dracut-ng/dracut`.
