from __future__ import annotations

import html
import json
from typing import Iterable

from .catalog import App


def render_markdown(app: App) -> str:
    lines = [
        f"# {app.name}",
        "",
        f"> {app.summary}",
        "",
        f"- Repository: [{app.repo}]({app.github_url})",
        f"- Category: {app.category}",
        f"- Local fit: {app.local_fit}",
    ]
    if app.language:
        lines.append(f"- Language: {app.language}")
    if app.license:
        lines.append(f"- License: {app.license}")
    if app.website:
        lines.append(f"- Website: {app.website}")
    if app.tags:
        lines.append(f"- Tags: {', '.join(app.tags)}")
    lines.extend(
        [
            "",
            "## Next step",
            "",
            f"Read the upstream installation guide at {app.github_url}.",
            "",
        ]
    )
    return "\n".join(lines)


def render_share(app: App) -> str:
    replacements = ", ".join(app.replaces) if app.replaces else "an existing tool"
    setup = f"about {app.setup_minutes} minutes" if app.setup_minutes else "an upstream-guided setup"
    return "\n".join(
        [
            f"## {app.name}: an open-source alternative",
            "",
            f"I found {app.name} through OpenApps as an alternative to {replacements}.",
            f"- Privacy: {app.privacy_model}",
            f"- Pricing: {app.pricing_model}",
            f"- Setup: {setup}",
            f"- Upstream: {app.github_url}",
            "",
            "OpenApps provides discovery and reviewable plans; it never executes installation commands.",
            "",
        ]
    )


def render_json(apps: Iterable[App]) -> str:
    return json.dumps([app.to_dict() for app in apps], indent=2, ensure_ascii=False) + "\n"


def _initial_card(app: App) -> str:
    replacements = ", ".join(app.replaces) if app.replaces else "Open-source pick"
    platforms = ", ".join(app.platforms) if app.platforms else "Check upstream"
    return "\n".join(
        [
            f'<article class="card" data-slug="{html.escape(app.slug, quote=True)}">',
            f'  <div class="card-kicker">{html.escape(app.category)} / {html.escape(app.privacy_model)}</div>',
            f'  <h2><a href="{html.escape(app.github_url, quote=True)}" target="_blank" rel="noreferrer">{html.escape(app.name)}</a></h2>',
            f'  <p>{html.escape(app.summary)}</p>',
            f'  <p class="replaces"><strong>Replaces:</strong> {html.escape(replacements)}</p>',
            f'  <p class="card-meta">{html.escape(platforms)}</p>',
            f'  <button class="card-select" type="button" data-slug="{html.escape(app.slug, quote=True)}">Compare this app</button>',
            "</article>",
        ]
    )


def render_html(apps: Iterable[App]) -> str:
    app_list = tuple(apps)
    initial_cards = "\n".join(_initial_card(app) for app in app_list)
    payload = json.dumps(
        [app.to_dict() for app in app_list],
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("</", "<\\/").replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")

    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Find open-source alternatives to the software you already use.">
  <title>OpenApps — software you can own</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #080b12;
      --panel: #111827;
      --panel-2: #172033;
      --line: #29364d;
      --text: #f7f9fc;
      --muted: #9aa9c2;
      --accent: #8bffb0;
      --accent-2: #70d7ff;
      --warning: #ffd479;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    * { box-sizing: border-box; }
    body { background: radial-gradient(circle at top right, #172b45 0, var(--bg) 42rem); color: var(--text); margin: 0; }
    main { max-width: 1240px; margin: 0 auto; padding: 32px 22px 72px; }
    a { color: inherit; }
    button, input, select { font: inherit; }
    button { cursor: pointer; }
    .hero { padding: 62px 0 38px; max-width: 900px; }
    .eyebrow { color: var(--accent); font-size: .75rem; font-weight: 800; letter-spacing: .16em; margin: 0 0 16px; text-transform: uppercase; }
    h1 { font-size: clamp(3rem, 9vw, 7.4rem); letter-spacing: -.075em; line-height: .92; margin: 0; max-width: 860px; }
    .lede { color: var(--muted); font-size: clamp(1.05rem, 2vw, 1.35rem); line-height: 1.55; margin: 24px 0 30px; max-width: 730px; }
    .search-shell { background: rgba(17, 24, 39, .88); border: 1px solid var(--line); border-radius: 24px; box-shadow: 0 22px 70px rgba(0, 0, 0, .28); padding: 18px; }
    .search-shell label { display: block; font-size: .9rem; font-weight: 750; margin-bottom: 9px; }
    .search-row { display: flex; gap: 10px; }
    .search-row input { background: #0a0f1a; border: 1px solid #40506b; border-radius: 13px; color: var(--text); flex: 1; min-width: 0; padding: 15px 16px; outline: none; }
    .search-row input:focus, select:focus, button:focus-visible { border-color: var(--accent-2); box-shadow: 0 0 0 3px rgba(112, 215, 255, .2); outline: none; }
    .examples { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
    .example { background: transparent; border: 1px solid var(--line); border-radius: 999px; color: var(--muted); padding: 7px 11px; }
    .example:hover { border-color: var(--accent); color: var(--text); }
    .trust-row { color: var(--muted); display: flex; flex-wrap: wrap; gap: 18px; margin-top: 22px; }
    .trust-row span::before { color: var(--accent); content: "✓"; margin-right: 7px; }
    .workspace { align-items: start; display: grid; gap: 20px; grid-template-columns: minmax(0, 1.65fr) minmax(290px, .75fr); }
    .results-panel, .detail-panel { background: rgba(17, 24, 39, .72); border: 1px solid var(--line); border-radius: 22px; padding: 18px; }
    .results-head { align-items: center; display: flex; justify-content: space-between; margin-bottom: 16px; }
    .results-head h2 { font-size: 1rem; margin: 0; }
    .results-count { color: var(--muted); font-size: .85rem; }
    .filters { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
    select { background: #0a0f1a; border: 1px solid var(--line); border-radius: 10px; color: var(--text); padding: 9px 11px; }
    .grid { display: grid; gap: 13px; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }
    .card { background: linear-gradient(145deg, rgba(23, 32, 51, .98), rgba(15, 23, 42, .96)); border: 1px solid var(--line); border-radius: 18px; display: flex; flex-direction: column; min-height: 275px; padding: 17px; }
    .card:hover { border-color: #53688d; transform: translateY(-2px); transition: border-color .15s ease, transform .15s ease; }
    .card-kicker { color: var(--accent-2); font-size: .72rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
    .card h2 { font-size: 1.25rem; letter-spacing: -.025em; margin: 12px 0 8px; }
    .card h2 a { text-decoration: none; }
    .card h2 a:hover { color: var(--accent); }
    .card p { color: var(--muted); line-height: 1.48; margin: 0 0 11px; }
    .card .replaces { color: var(--text); font-size: .84rem; margin-top: auto; }
    .card-meta { font-size: .78rem; }
    .card-select { background: rgba(139, 255, 176, .1); border: 1px solid rgba(139, 255, 176, .42); border-radius: 10px; color: var(--accent); margin-top: 9px; padding: 9px 10px; text-align: left; }
    .card-select:hover { background: rgba(139, 255, 176, .18); }
    .detail-panel { position: sticky; top: 18px; }
    .detail-panel h2 { font-size: 1.65rem; letter-spacing: -.04em; margin: 0 0 10px; }
    .detail-copy { color: var(--muted); line-height: 1.55; }
    .stat-grid { display: grid; gap: 8px; grid-template-columns: 1fr 1fr; margin: 18px 0; }
    .stat { background: #0b1220; border: 1px solid var(--line); border-radius: 12px; padding: 10px; }
    .stat small { color: var(--muted); display: block; font-size: .7rem; margin-bottom: 4px; text-transform: uppercase; }
    .plan-box { background: rgba(255, 212, 121, .08); border: 1px solid rgba(255, 212, 121, .35); border-radius: 14px; margin: 16px 0; padding: 13px; }
    .plan-box strong { color: var(--warning); display: block; margin-bottom: 7px; }
    .plan-box code { background: #080b12; border-radius: 7px; display: block; overflow-wrap: anywhere; padding: 9px; }
    .plan-box p { color: var(--muted); font-size: .82rem; line-height: 1.45; margin: 9px 0 0; }
    .detail-actions { display: flex; flex-wrap: wrap; gap: 9px; }
    .primary, .secondary { border-radius: 10px; padding: 10px 13px; text-decoration: none; }
    .primary { background: var(--accent); border: 1px solid var(--accent); color: #07110a; font-weight: 800; }
    .secondary { background: transparent; border: 1px solid var(--line); color: var(--text); }
    .empty { color: var(--muted); padding: 34px 4px; text-align: center; }
    .footer-note { color: var(--muted); font-size: .83rem; line-height: 1.5; margin-top: 22px; }
    .sr-only { height: 1px; margin: -1px; overflow: hidden; position: absolute; width: 1px; clip: rect(0, 0, 0, 0); }
    @media (max-width: 850px) {
      .workspace { grid-template-columns: 1fr; }
      .detail-panel { position: static; }
    }
    @media (max-width: 520px) {
      main { padding-left: 14px; padding-right: 14px; }
      .hero { padding-top: 38px; }
      .search-row { display: block; }
      .search-row input { width: 100%; }
    }
  </style>
</head>
<body>
<main>
  <header class="hero">
    <p class="eyebrow">Open source, without the guesswork</p>
    <h1>Stop paying for software you can own.</h1>
    <p class="lede">Find an open-source alternative to the software you already use — then get a reviewable setup plan in seconds.</p>
    <div class="search-shell">
      <label for="query">What do you want to replace?</label>
      <div class="search-row">
        <input id="query" type="search" placeholder="Notion, Dropbox, TeamViewer..." autocomplete="off">
      </div>
      <div class="examples" aria-label="Example searches">
        <button class="example" type="button" data-example="Notion">Notion</button>
        <button class="example" type="button" data-example="Dropbox">Dropbox</button>
        <button class="example" type="button" data-example="TeamViewer">TeamViewer</button>
        <button class="example" type="button" data-example="Google Analytics">Google Analytics</button>
      </div>
    </div>
    <div class="trust-row" aria-label="Product principles">
      <span>Local-first</span><span>No account</span><span>No model required</span><span>Never auto-installs</span>
    </div>
  </header>

  <section class="workspace" aria-label="Open-source alternatives">
    <div class="results-panel">
      <div class="results-head">
        <h2>Shortlist your next app</h2>
        <span class="results-count" id="results-count"></span>
      </div>
      <div class="filters">
        <label class="sr-only" for="platform">Platform</label>
        <select id="platform">
          <option value="">Any platform</option>
          <option value="windows">Windows</option>
          <option value="macos">macOS</option>
          <option value="linux">Linux</option>
          <option value="docker">Docker</option>
          <option value="web">Web</option>
        </select>
        <label class="sr-only" for="privacy">Privacy model</label>
        <select id="privacy">
          <option value="">Any privacy model</option>
          <option value="local">Local</option>
          <option value="self-hosted">Self-hosted</option>
          <option value="mixed">Mixed</option>
          <option value="cloud">Cloud</option>
        </select>
      </div>
      <div class="grid" id="catalog-grid">""" + initial_cards + """</div>
      <p class="empty" id="empty-state" hidden>No matching alternative yet. Try a product name, category, or tag.</p>
      <p class="footer-note">OpenApps points to upstream projects. Always review their documentation, license, and security posture before deployment.</p>
    </div>

    <aside class="detail-panel" id="detail-panel" aria-live="polite">
      <p class="eyebrow">Your next move</p>
      <h2 id="detail-title">Choose an alternative</h2>
      <p class="detail-copy" id="detail-copy">Search above, then compare an app to see its privacy model, setup estimate, and reviewable plan.</p>
      <div id="detail-content"></div>
      <div class="detail-actions">
        <button class="primary" id="copy-share" type="button" hidden>Copy share text</button>
        <a class="secondary" id="upstream-link" href="#" target="_blank" rel="noreferrer" hidden>Open upstream</a>
      </div>
    </aside>
  </section>

  <noscript><p class="footer-note">JavaScript is needed for local filtering. The catalog is still available through the OpenApps CLI.</p></noscript>
</main>

<script id="catalog-data" type="application/json">""" + payload + """</script>
<script>
(() => {
  const apps = JSON.parse(document.getElementById("catalog-data").textContent);
  const queryInput = document.getElementById("query");
  const platformInput = document.getElementById("platform");
  const privacyInput = document.getElementById("privacy");
  const grid = document.getElementById("catalog-grid");
  const count = document.getElementById("results-count");
  const empty = document.getElementById("empty-state");
  const detailTitle = document.getElementById("detail-title");
  const detailCopy = document.getElementById("detail-copy");
  const detailContent = document.getElementById("detail-content");
  const upstreamLink = document.getElementById("upstream-link");
  const copyButton = document.getElementById("copy-share");
  let selectedSlug = null;

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (character) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;"
    }[character]));
  }

  function pretty(value) {
    return String(value || "unknown").replaceAll("-", " ").replace(/\\b\\w/g, (character) => character.toUpperCase());
  }

  function score(app, needle) {
    if (!needle) return 1;
    const aliases = (app.replaces || []).map((value) => String(value).toLowerCase());
    const name = String(app.name || "").toLowerCase();
    const slug = String(app.slug || "").toLowerCase();
    const text = JSON.stringify(app).toLowerCase();
    if (aliases.includes(needle)) return 1200;
    if (needle === name || needle === slug) return 1000;
    if (aliases.some((value) => value.includes(needle))) return 900;
    if (name.includes(needle) || slug.includes(needle)) return 800;
    if ((app.tags || []).some((value) => String(value).toLowerCase() === needle)) return 700;
    return text.includes(needle) ? 300 : 0;
  }

  function matches(app, needle, platform, privacy) {
    const platformMatch = !platform || (app.platforms || []).includes(platform);
    const privacyMatch = !privacy || app.privacy_model === privacy;
    return platformMatch && privacyMatch && score(app, needle) > 0;
  }

  function shareText(app) {
    const replacements = (app.replaces || []).join(", ") || "an existing tool";
    const setup = app.setup_minutes ? "about " + app.setup_minutes + " minutes" : "an upstream-guided setup";
    return "I found " + app.name + " through OpenApps as an alternative to " + replacements + ".\n\n" +
      "- Privacy: " + app.privacy_model + "\n" +
      "- Pricing: " + app.pricing_model + "\n" +
      "- Setup: " + setup + "\n" +
      "- Upstream: " + app.github_url + "\n\n" +
      "OpenApps provides discovery and reviewable plans; it never executes installation commands.";
  }

  function cardTemplate(app) {
    const replacements = (app.replaces || []).length ? (app.replaces || []).join(", ") : "Open-source pick";
    const platforms = (app.platforms || []).length ? (app.platforms || []).map(pretty).join(", ") : "Check upstream";
    return '<article class="card">' +
      '<div class="card-kicker">' + escapeHtml(pretty(app.category)) + " / " + escapeHtml(pretty(app.privacy_model)) + '</div>' +
      '<h2><a href="' + escapeHtml(app.github_url) + '" target="_blank" rel="noreferrer">' + escapeHtml(app.name) + '</a></h2>' +
      '<p>' + escapeHtml(app.summary) + '</p>' +
      '<p class="replaces"><strong>Replaces:</strong> ' + escapeHtml(replacements) + '</p>' +
      '<p class="card-meta">' + escapeHtml(platforms) + '</p>' +
      '<button class="card-select" type="button" data-slug="' + escapeHtml(app.slug) + '">Compare this app</button>' +
      '</article>';
  }

  function selectApp(slug) {
    const app = apps.find((candidate) => candidate.slug === slug);
    if (!app) return;
    selectedSlug = slug;
    detailTitle.textContent = app.name;
    detailCopy.textContent = app.summary;
    const plan = (app.install_plans || [])[0];
    const planHtml = plan
      ? '<div class="plan-box"><strong>' + escapeHtml(plan.label) + ' — review before running</strong><code>' + escapeHtml(plan.command) + '</code><p>' + escapeHtml(plan.notes || "Inspect the upstream documentation, storage, and credentials first.") + '</p></div>'
      : '<div class="plan-box"><strong>Upstream-guided setup</strong><p>No verified command is bundled for this app yet. Open the upstream guide and review it before running anything.</p></div>';
    detailContent.innerHTML =
      '<div class="stat-grid">' +
      '<div class="stat"><small>Replaces</small><span>' + escapeHtml((app.replaces || []).join(", ") || "Existing tool") + '</span></div>' +
      '<div class="stat"><small>Privacy</small><span>' + escapeHtml(pretty(app.privacy_model)) + '</span></div>' +
      '<div class="stat"><small>Pricing</small><span>' + escapeHtml(pretty(app.pricing_model)) + '</span></div>' +
      '<div class="stat"><small>Setup</small><span>' + escapeHtml(app.setup_minutes ? app.setup_minutes + " min" : "Varies") + '</span></div>' +
      '</div>' + planHtml;
    upstreamLink.href = app.github_url;
    upstreamLink.hidden = false;
    copyButton.hidden = false;
    copyButton.onclick = () => copyShare();
  }

  async function copyShare() {
    if (!selectedSlug) return;
    const app = apps.find((candidate) => candidate.slug === selectedSlug);
    if (!app) return;
    const original = copyButton.textContent;
    try {
      await navigator.clipboard.writeText(shareText(app));
      copyButton.textContent = "Copied";
    } catch (error) {
      copyButton.textContent = "Copy unavailable";
    }
    window.setTimeout(() => { copyButton.textContent = original; }, 1600);
  }
  window.copyShare = copyShare;

  function updateUrl(needle) {
    try {
      const url = new URL(window.location.href);
      if (needle) url.searchParams.set("q", needle);
      else url.searchParams.delete("q");
      window.history.replaceState({}, "", url);
    } catch (error) {
      // file:// pages can disallow history updates; filtering still works.
    }
  }

  function renderCards() {
    const needle = queryInput.value.trim().toLowerCase();
    const platform = platformInput.value;
    const privacy = privacyInput.value;
    const filtered = apps
      .filter((app) => matches(app, needle, platform, privacy))
      .sort((left, right) => score(right, needle) - score(left, needle) || left.name.localeCompare(right.name));
    grid.innerHTML = filtered.map(cardTemplate).join("");
    grid.querySelectorAll("[data-slug]").forEach((button) => {
      button.addEventListener("click", () => selectApp(button.dataset.slug));
    });
    count.textContent = filtered.length + (filtered.length === 1 ? " match" : " matches");
    empty.hidden = filtered.length !== 0;
    updateUrl(needle);
  }

  queryInput.addEventListener("input", renderCards);
  platformInput.addEventListener("change", renderCards);
  privacyInput.addEventListener("change", renderCards);
  document.querySelectorAll("[data-example]").forEach((button) => {
    button.addEventListener("click", () => {
      queryInput.value = button.dataset.example;
      renderCards();
      queryInput.focus();
    });
  });

  try {
    const initialQuery = new URL(window.location.href).searchParams.get("q");
    if (initialQuery) queryInput.value = initialQuery;
  } catch (error) {
    // Ignore unavailable URL state on local files.
  }
  renderCards();
})();
</script>
</body>
</html>
"""
