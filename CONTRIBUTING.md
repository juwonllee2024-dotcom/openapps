# Contributing to OpenApps

Thanks for helping people discover software they can run themselves.

## Development

```bash
python -m unittest discover -s tests -v
python -m openapps doctor
python -m openapps search "remote"
```

The project uses only Python's standard library at runtime.

## Adding an app

1. Add one entry to `openapps/catalog.json`.
2. Use the upstream repository as `repo`.
3. Keep `summary` factual and short.
4. Add useful tags and choose the narrowest accurate `local_fit`.
5. Run `python -m openapps doctor` and the full test suite.

Do not add credentials, private URLs, copied upstream source, or install commands
that have not been reviewed. OpenApps is a discovery layer; upstream projects keep
ownership of their code and release process.

## Pull requests

Explain what user decision the change improves. Keep unrelated catalog changes in
separate pull requests.
