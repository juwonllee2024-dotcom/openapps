# OpenApps SaaS Replacement MVP Design

**Date:** 2026-08-17  
**Status:** Proposed  
**Goal:** Turn OpenApps from a static repository catalog into a local-first, shareable “open-source App Store” that helps a general user replace a paid SaaS product in about one minute.

## Product promise

> Stop paying for software you can own.

The first audience is a general user who knows the paid product they want to replace, but does not know which open-source alternative is trustworthy or how to start it. OpenApps will answer that question without an account, model, cloud service, or automatic shell execution.

The primary loop is:

```text
name a paid app → compare open-source alternatives → review an install plan → share the result
```

This is intentionally broader than local-model software. Local AI can appear as one category later, but it is not a requirement or the product identity.

## Alternatives considered

### Catalog 2.0

Improve the existing search, filters, and HTML cards. This is low risk and quick, but remains a directory and gives users little reason to return or share it.

### Open-source App Store — selected

Add intent-based replacement search, comparison metadata, reviewable install plans, and shareable output while preserving the current standard-library-only Python foundation. This creates a clear user outcome without taking on the security and platform cost of automatic installation.

### One-click installer

Execute Docker or native installation commands. This could create stronger utility, but arbitrary command execution, operating-system differences, permissions, backups, and rollback make it unsafe for the first viral-facing release. The MVP will generate plans only; execution is a later, separately designed feature.

## MVP user experience

### CLI

Existing commands remain compatible. Add:

```bash
openapps replace notion
openapps plan appflowy --platform docker
openapps share appflowy
openapps render --format html --output openapps.html
```

`replace` ranks entries by replacement aliases, name, category, tags, and summary. An exact alias such as `notion` must rank its intended alternatives before generic text matches.

`plan` prints a reviewable plan containing the selected app, target platform, prerequisites, upstream link, and an install command when a verified command is available. It never invokes a shell, downloads a file, changes the machine, or requires network access.

`share` prints a short Markdown block suitable for an issue, README, chat, or social post. It must link to the upstream repository and clearly label OpenApps as a discovery/planning tool.

### Generated HTML

The existing zero-dependency renderer becomes a usable local storefront:

- hero headline and one-sentence promise above the fold;
- search field with examples such as “Notion”, “Dropbox”, and “TeamViewer”;
- intent filters for category, platform, privacy model, and setup time;
- cards showing “replaces”, license, platform, setup estimate, and privacy model;
- a visible install-plan panel with a copy button;
- a “share this alternative” action that copies safe Markdown;
- keyboard-accessible controls, mobile layout, and no remote assets;
- escaped catalog values and no execution of catalog content as code.

The page remains a single static HTML file. Inline JavaScript is limited to filtering, rendering selected cards, copying text, and updating the URL query string; it does not make network requests.

## Catalog contract

Extend each catalog entry with these fields:

```json
{
  "replaces": ["Notion"],
  "platforms": ["windows", "macos", "linux", "docker"],
  "pricing_model": "free-self-hosted",
  "privacy_model": "self-hosted",
  "setup_minutes": 10,
  "install_plans": [
    {
      "platform": "docker",
      "label": "Docker Compose",
      "command": "docker compose up -d",
      "notes": "Review the upstream compose file and configure storage before running."
    }
  ]
}
```

The existing 25 entries keep working through explicit defaults, but entries surfaced in replacement results must have complete comparison metadata. Validation rejects malformed platform names, negative setup times, duplicate install platforms, empty commands, and invalid privacy/pricing values. Install commands are display data only and are never passed to a subprocess.

The first high-intent replacement set will cover eight recognizable searches with verified upstream metadata: Notion, Dropbox, TeamViewer, Google Analytics, Typeform, Plex, Retool, and Okta. The catalog may add the relevant upstream projects rather than pretending that an unrelated repository is a direct replacement.

## Architecture

- `openapps/catalog.py`: typed catalog fields, validation, intent-aware ranking, and install-plan lookup.
- `openapps/cli.py`: `replace`, `plan`, and `share` command handlers; preserve existing commands.
- `openapps/render.py`: static storefront markup, CSS, and small local-only browser behavior.
- `openapps/catalog.json`: curated entries and replacement metadata.
- `tests/test_catalog.py`: catalog, ranking, plan, share, and renderer behavior.
- `README.md`: new promise, visual quick start, user examples, safety boundary, and contribution path.
- `docs/catalog-format.md`: contributor-facing schema and safe command rules.

No runtime dependency or remote service is added. The project continues to support Python 3.11+ and Windows terminals.

## Safety and failure behavior

- Unknown replacement queries return a helpful empty state and suggest category search; they do not fail with a traceback.
- Unknown slugs and unsupported platforms return exit code 2 with an actionable message.
- Missing install metadata produces an upstream-guidance plan instead of an invented command.
- HTML escapes names, summaries, links, tags, and commands before insertion.
- OpenApps never executes, downloads, elevates, or silently modifies the user's machine.
- Every install plan tells the user to inspect upstream instructions before running anything.

## Growth loop

The product is designed around a repeatable, honest share loop:

1. A user searches for a paid product they already know.
2. OpenApps gives them a concrete alternative and a plan they can use immediately.
3. `share` produces a compact, link-backed explanation for teammates or communities.
4. Contributors add missing alternatives and improve metadata through reviewable JSON changes.
5. The README and generated pages expose common replacement intents so each useful answer can be discovered independently.

The MVP will not claim guaranteed savings, universal compatibility, or “one-click” installation. Trust is part of the growth strategy.

## Acceptance criteria

- A fresh checkout can run `openapps replace notion` and return a relevant alternative before generic matches.
- A fresh checkout can run `openapps plan <known-slug> --platform docker` and receive a safe, non-executing plan.
- `openapps share <known-slug>` emits valid Markdown with an upstream link and no raw shell execution.
- Generated HTML visibly communicates the product promise, supports local filtering, and contains no unescaped catalog content.
- Catalog validation covers all new fields and reports actionable errors.
- Existing list/search/show/doctor/render/export behavior remains green.
- README explains the value in the first screenful and includes a copy-paste demo.
- Unit tests cover every new public behavior and pass on Windows with CP949-compatible text output.

## Explicitly out of scope

- automatic installation or uninstallation;
- accounts, analytics, tracking pixels, or a hosted backend;
- paid listings, affiliate links, or unverifiable popularity claims;
- a full native GUI or browser extension;
- a promise of 100k stars or guaranteed virality.

