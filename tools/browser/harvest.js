// Browser-side harvest helpers. Paste into the devtools console (or run through a browser automation tool)
// on a page of the target origin, so requests are same-origin or CORS-allowed:
//   Red Hat / kernel Bugzilla: https://bugzilla.redhat.com/rest/version  (or bugzilla.kernel.org)
//   GitLab kernel-ark:         https://gitlab.com/cki-project/kernel-ark
//   libcamera patchwork:       https://patchwork.libcamera.org/api/projects/
//   Fedora Discussion:         https://discussion.fedoraproject.org/about
//   GitHub API:                https://github.com/robots.txt  (api.github.com pages forbid fetch through CSP)
// Each function returns TSV lines; render them with show(lines) and copy the text out.
// Long runs: start without await (fn().then(r => window.out = r)) and poll window.out.

const sleep = ms => new Promise(r => setTimeout(r, ms));

function show(lines) {
  document.body.innerHTML = '<pre id="o"></pre>';
  document.getElementById('o').textContent = lines.join('\n');
  return lines.length;
}

// Bugzilla 5 REST. Unauthenticated pages are capped at 20 results, so page with offset.
async function bugzilla(terms, field = 'short_desc') {
  const out = [], seen = new Set();
  for (const q of terms) {
    for (let off = 0; off < 200; off += 20) {
      const url = `/rest/bug?${field}=${encodeURIComponent(q)}&${field}_type=allwordssubstr` +
        '&include_fields=id,summary,status,resolution,product,component,version,creation_time,last_change_time' +
        `&limit=20&offset=${off}`;
      const bugs = ((await fetch(url).then(r => r.json()).catch(() => ({}))).bugs) || [];
      for (const b of bugs) {
        if (seen.has(b.id)) continue;
        seen.add(b.id);
        out.push([q, b.id, `${b.product} ${b.version}`, b.component,
          b.status + (b.resolution ? '/' + b.resolution : ''),
          b.creation_time.slice(0, 10), b.last_change_time.slice(0, 10), b.summary].join('\t'));
      }
      if (bugs.length < 20) break;
    }
  }
  return out;
}

// Bugzilla comments: first comment and last two, trimmed.
async function bugzillaComments(ids, n = 900) {
  const out = [];
  for (const id of ids) {
    const cs = (await fetch(`/rest/bug/${id}/comment`).then(r => r.json())).bugs[id].comments;
    out.push(`=== ${id} (${cs.length} comments)`, cs[0].text.slice(0, n));
    for (const c of cs.slice(1).slice(-2)) out.push(`-- ${c.creation_time.slice(0, 10)} ${c.text.slice(0, n)}`);
  }
  return out;
}

// GitLab merge requests of one project.
async function gitlabMRs(project, terms) {
  const out = [], seen = new Set();
  const base = `/api/v4/projects/${encodeURIComponent(project)}/merge_requests?state=all&per_page=100&in=title,description&search=`;
  for (const q of terms) {
    const mrs = await fetch(base + encodeURIComponent(q)).then(r => r.json()).catch(() => []);
    for (const m of Array.isArray(mrs) ? mrs : []) {
      if (seen.has(m.iid)) continue;
      seen.add(m.iid);
      out.push([q, '!' + m.iid, m.state, m.created_at.slice(0, 10), (m.merged_at || '').slice(0, 10),
        m.author.username, m.title].join('\t'));
    }
  }
  return out;
}

// Patchwork REST (libcamera uses /api/ without a version prefix; kernel.org uses /api/1.3/).
async function patchwork(terms, { project = 1, since = '2025-06-01T00:00:00', prefix = '/api/' } = {}) {
  const out = [], seen = new Set();
  for (const q of terms) {
    for (let p = 1; p <= 3; p++) {
      const r = await fetch(`${prefix}patches/?project=${project}&per_page=100&page=${p}&order=-date&since=${since}&q=${encodeURIComponent(q)}`);
      if (r.status !== 200) break;
      const items = await r.json();
      for (const x of items) {
        if (seen.has(x.id)) continue;
        seen.add(x.id);
        out.push([q, x.id, x.date.slice(0, 10), x.state, (x.series[0] || {}).id || '', x.submitter.name, x.name].join('\t'));
      }
      if (items.length < 100) break;
    }
  }
  return out;
}

// Discourse search (Fedora Discussion) and tag listing.
async function discourse(terms, pages = 3) {
  const out = [], seen = new Set();
  for (const q of terms) {
    for (let p = 1; p <= pages; p++) {
      const j = await fetch(`/search.json?page=${p}&q=${encodeURIComponent(q)}`).then(r => r.json()).catch(() => ({}));
      for (const t of j.topics || []) {
        if (seen.has(t.id)) continue;
        seen.add(t.id);
        out.push([q, t.id, t.created_at.slice(0, 10), (t.last_posted_at || '').slice(0, 10), t.posts_count,
          (t.tags || []).map(x => x.name || x).join(','), t.title].join('\t'));
      }
      await sleep(1500);
      if (!(j.grouped_search_result || {}).more_full_page_results) break;
    }
  }
  return out;
}

// GitHub search API, unauthenticated: 10 requests per minute. Phrase matching ignores quotes in bodies,
// so use in:title for phrases, or distinctive tokens (SKU strings, ACPI IDs).
async function githubSearch(queries, kind = 'issues') {
  const out = [];
  for (const [q, pages] of queries) {
    for (let p = 1; p <= pages; p++) {
      const r = await fetch(`https://api.github.com/search/${kind}?per_page=100&page=${p}&q=${encodeURIComponent(q)}`);
      if (r.status !== 200) { await sleep(30000); p--; continue; }
      const j = await r.json();
      for (const i of j.items) {
        out.push(kind === 'issues'
          ? [q, i.html_url.replace('https://github.com/', ''), i.state, i.created_at.slice(0, 10), i.updated_at.slice(0, 10), i.comments, i.title].join('\t')
          : [q, i.full_name, i.pushed_at.slice(0, 10), i.stargazers_count, i.description || ''].join('\t'));
      }
      await sleep(7000);
      if (j.items.length < 100) break;
    }
  }
  return out;
}

// Closed-but-unmerged PRs of one repo and their conversation. Run on https://github.com/robots.txt.
// Search API for the list (10 requests per minute), then the PR HTML page for comments (no API quota).
async function closedUnmergedPRs(repo) {
  const out = [];
  for (let p = 1; p <= 10; p++) {
    const r = await fetch(`https://api.github.com/search/issues?per_page=100&page=${p}&q=${encodeURIComponent(`repo:${repo} is:pr is:closed is:unmerged`)}`);
    if (r.status !== 200) { await sleep(30000); p--; continue; }
    const j = await r.json();
    for (const i of j.items) out.push([repo, i.number, i.user.login, i.created_at.slice(0, 10), (i.closed_at || '').slice(0, 10), i.comments, i.title].join('\t'));
    await sleep(6500);
    if (j.items.length < 100) break;
  }
  return out;
}

async function prConversation(repo, number) {
  const html = await fetch(`https://github.com/${repo}/pull/${number}`).then(r => r.text());
  const d = new DOMParser().parseFromString(html, 'text/html');
  const items = [];
  for (const sel of ['.timeline-comment', '.review-comment']) {
    for (const c of d.querySelectorAll(sel)) {
      const a = c.querySelector('.author'), b = c.querySelector('.comment-body');
      if (b) items.push([(sel === '.review-comment' ? 'R:' : '') + (a ? a.textContent.trim() : '?'), b.textContent.replace(/\s+/g, ' ').trim()]);
    }
  }
  const closedBy = [...d.querySelectorAll('.TimelineItem')].map(t => t.textContent.replace(/\s+/g, ' ').trim())
    .filter(t => /closed this/.test(t)).map(t => t.split(' closed this')[0].slice(-25));
  return { items, closedBy };
}

// One issue thread from the issue page's embedded JSON (no API quota). Run on https://github.com/robots.txt.
// The page embeds at most about 30 timeline items; when total > comments.length, fetch the rest with
// issueComments() (REST, 60 unauthenticated requests per hour).
async function issueThread(repo, number) {
  const r = await fetch(`https://github.com/${repo}/issues/${number}`);
  const d = new DOMParser().parseFromString(await r.text(), 'text/html');
  const out = { repo, number, status: r.status, title: '', state: '', stateReason: '', author: '', created: '', updated: '',
    total: 0, body: '', labels: [], comments: [], closed: [], refs: [] };
  const seen = new Set();
  const walk = o => {
    if (!o || typeof o !== 'object') return;
    if (Array.isArray(o)) { o.forEach(walk); return; }
    if (o.number && o.title && 'timelineItems' in o && !out.title) {
      Object.assign(out, { title: o.title, state: o.state || '', stateReason: o.stateReason || '', author: o.author?.login || '',
        created: (o.createdAt || '').slice(0, 10), updated: (o.updatedAt || '').slice(0, 10), total: o.totalCommentsCount || 0, body: o.body || '' });
      (o.labels?.edges || o.labels?.nodes || []).forEach(e => { const x = e.node || e; if (x?.name) out.labels.push(x.name); });
    }
    const t = o.__typename;
    if (o.id && !seen.has(o.id)) {
      if (t === 'IssueComment') { seen.add(o.id); out.comments.push([o.author?.login || '?', (o.createdAt || '').slice(0, 10), o.body || '']); }
      if (t === 'ClosedEvent') { seen.add(o.id); out.closed.push([o.actor?.login || '?', (o.createdAt || '').slice(0, 10), o.stateReason || '']); }
      if (t === 'CrossReferencedEvent') { seen.add(o.id); out.refs.push((o.source?.url || '').replace('https://github.com/', '')); }
    }
    for (const k in o) walk(o[k]);
  };
  d.querySelectorAll('script[type="application/json"]').forEach(s => { try { walk(JSON.parse(s.textContent)); } catch (e) {} });
  return out;
}

// All comments of an issue through the REST API (100 per page).
async function issueComments(repo, number, total) {
  const all = [];
  for (let p = 1; p <= Math.ceil(total / 100); p++) {
    const r = await fetch(`https://api.github.com/repos/${repo}/issues/${number}/comments?per_page=100&page=${p}`);
    if (!r.ok) throw new Error(`${repo}#${number}: HTTP ${r.status}`);
    (await r.json()).forEach(c => all.push([c.user?.login || '?', c.created_at.slice(0, 10), c.body || '']));
  }
  return all;
}

if (typeof module !== 'undefined') module.exports = { show, bugzilla, bugzillaComments, gitlabMRs, patchwork, discourse, githubSearch, closedUnmergedPRs, prConversation, issueThread, issueComments };
