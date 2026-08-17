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

Replacement fields make an entry useful for intent search. They are optional for
legacy entries, but required before an entry is promoted as a replacement result:

- `replaces`: names of products the project can replace or serve as an alternative to.
- `platforms`: one or more of `windows`, `macos`, `linux`, `docker`, or `web`.
- `pricing_model`: `free`, `free-self-hosted`, `open-core`, or `unknown`.
- `privacy_model`: `local`, `self-hosted`, `mixed`, `cloud`, or `unknown`.
- `setup_minutes`: a conservative whole-number setup estimate.
- `install_plans`: optional reviewable plans with `platform`, `label`, `command`, and `notes`.

Install commands are display data only. OpenApps never executes them. Add a
command only when it comes from reviewed upstream documentation, and keep the
notes explicit about storage, credentials, permissions, or other prerequisites.

Trend fields are snapshots and must include the capture date in the surrounding
research document when updated.
