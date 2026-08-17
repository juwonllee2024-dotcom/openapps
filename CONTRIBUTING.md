# Contributing to OpenApps

Thanks for helping people find software they can own.

## Development

    python -m unittest discover -s tests -v
    python -m openapps doctor
    python -m openapps replace notion
    python -m openapps render --format html --output openapps.html

The project uses only Python’s standard library at runtime.

## Adding an app

1. Add one entry to openapps/catalog.json.
2. Use the upstream repository as repo.
3. Keep summary factual and short.
4. Add useful tags and choose the narrowest accurate local_fit.
5. If the project is a replacement, add exact names to replaces.
6. Add platforms, pricing_model, privacy_model, and a conservative setup_minutes estimate.
7. Add an install_plans command only when it is copied from reviewed upstream documentation.
8. Run python -m openapps doctor and the full test suite.

Install commands are display data. OpenApps never executes installation commands.
Do not add credentials, private URLs, copied upstream source, or unverifiable
pricing and compatibility claims. Upstream projects keep ownership of their code
and release process.

## Pull requests

Explain which user decision the change improves. Include the upstream source for
new metadata and keep unrelated catalog changes in separate pull requests.
