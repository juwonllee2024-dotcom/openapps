# OpenApps

> Discover open-source software you can run yourself.

OpenApps is a local-first catalog and launcher foundation for open-source apps.
It helps you answer three questions quickly:

1. What can I use instead of this SaaS product?
2. Can I run it on my machine or server?
3. What should I read before I install it?

No account. No model. No cloud dependency for the catalog.

## Quick start

```bash
python -m pip install -e .

openapps search "remote"
openapps show rustdesk
openapps list --category documents
openapps render --format html --output openapps.html
openapps doctor
```

Open `openapps.html` in any browser to browse the catalog locally.

## What works today

- Offline JSON catalog with 25 repositories from GitHub's monthly trending list.
- Case-insensitive search across names, summaries, categories, and tags.
- Human-readable Markdown, machine-readable JSON, and zero-dependency HTML output.
- Catalog validation for duplicate slugs, malformed repository names, missing fields, and invalid counts.
- Exportable app briefs for sharing or reviewing before deployment.
- GitHub Action that keeps catalog quality checked on every change.

## Why this exists

Lists are good at discovery. They are bad at the moment after discovery: comparison,
deployment fit, updates, backups, and safe migration.

OpenApps starts with a transparent, version-controlled catalog. The next layer is a
verified deployment format that can generate a plan for Docker, native binaries,
package managers, or a remote host. Installation will stay opt-in and reviewable.

## Roadmap

- `openapps install`: verified, reviewable deployment plans.
- OS, CPU, memory, storage, license, and maintenance filters.
- Backup and upgrade recipes with explicit rollback steps.
- Import/export between local machines and self-hosted servers.
- Community-maintained app manifests with CI validation.
- Optional AI explanations through user-selected providers; never required.

## Design principles

- Local-first: catalog search works without network access.
- Upstream-first: link to original projects; do not mirror their code.
- Safe by default: discovery and planning never execute installation commands.
- Reproducible: catalog entries are plain JSON and changes are reviewable.
- Provider-neutral: useful with no AI, local AI, or any cloud provider.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Add one catalog entry, run `openapps doctor`,
and include the upstream source link.

## Research

The initial product direction is documented in
[`docs/research/2026-08-github-trends.md`](docs/research/2026-08-github-trends.md).

## License

MIT. See [LICENSE](LICENSE).
