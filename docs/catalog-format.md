# Catalog format

Each entry in [`openapps/catalog.json`](../openapps/catalog.json) is intentionally
plain JSON so it can be edited without a database or a service.

Required fields:

- `slug`: stable lowercase identifier used by the CLI.
- `name`: display name.
- `repo`: canonical `owner/repository` path.
- `summary`: one-sentence description.
- `category`: discovery filter.
- `local_fit`: `self-hosted`, `local-tool`, or `mixed`.
- `tags`: searchable terms.

Trend fields are snapshots and must include the capture date in the surrounding
research document when updated.
