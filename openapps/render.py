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


def render_html(apps: Iterable[App]) -> str:
    cards: list[str] = []
    for app in apps:
        tags = " ".join(
            f'<span class="tag">{html.escape(tag)}</span>' for tag in app.tags
        )
        cards.append(
            "\n".join(
                [
                    '<article class="card">',
                    f'<h2><a href="{html.escape(app.github_url)}">{html.escape(app.name)}</a></h2>',
                    f'<p>{html.escape(app.summary)}</p>',
                    f'<div class="meta">{html.escape(app.category)} · {html.escape(app.local_fit)}</div>',
                    f'<div class="tags">{tags}</div>',
                    "</article>",
                ]
            )
        )
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OpenApps catalog</title>
  <style>
    :root { color-scheme: dark; font-family: Inter, system-ui, sans-serif; }
    body { background: #0d1117; color: #e6edf3; margin: 0; }
    main { max-width: 1100px; margin: 0 auto; padding: 48px 20px; }
    h1 { font-size: clamp(2.2rem, 6vw, 4.8rem); letter-spacing: -0.06em; margin: 0 0 12px; }
    .lede { color: #8b949e; font-size: 1.1rem; max-width: 680px; margin-bottom: 34px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
    .card { background: #161b22; border: 1px solid #30363d; border-radius: 16px; padding: 20px; }
    h2 { font-size: 1.2rem; margin: 0 0 10px; }
    a { color: #58a6ff; text-decoration: none; }
    p { color: #c9d1d9; min-height: 4.5em; line-height: 1.5; }
    .meta { color: #8b949e; font-size: .85rem; }
    .tags { margin-top: 14px; }
    .tag { background: #21262d; border-radius: 999px; color: #8b949e; display: inline-block; font-size: .75rem; margin: 3px 3px 0 0; padding: 4px 8px; }
  </style>
</head>
<body><main>
  <h1>OpenApps</h1>
  <p class="lede">Discover open-source software you can run yourself. No account required. No model required.</p>
  <section class="grid">
""" + "\n".join(cards) + """
  </section>
</main></body></html>
"""
