# OpenApps SaaS Replacement MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add intent-based SaaS replacement discovery, safe install-plan output, shareable summaries, and a polished static storefront while preserving OpenApps’ local-only Python foundation.

**Architecture:** Extend the existing typed catalog with replacement aliases and optional install-plan metadata. Keep ranking and validation in `catalog.py`, command behavior in `cli.py`, and all storefront/share presentation in `render.py`. The generated storefront is one static HTML file with inline, local-only JavaScript; no server, account, network call, or command execution is added.

**Tech Stack:** Python 3.11+, standard library only, `unittest`, JSON, generated HTML/CSS/inline JavaScript, GitHub Actions.

## Global Constraints

- Preserve Python 3.11+ support and the current standard-library-only runtime.
- Preserve existing `list`, `search`, `show`, `doctor`, `render`, and `export` command behavior.
- Keep all terminal output encodable on Windows CP949.
- Install plans are display data. OpenApps must never invoke a shell, download a file, elevate privileges, or modify the user’s machine.
- HTML must escape catalog values and must not make remote requests.
- New public behavior follows test-driven development: write one failing test, run it, implement the minimum, run the focused test, then run the full suite.
- Work only in `codex/openapps-saas-replacement` and commit each completed task with a focused message.

---

### Task 1: Extend the catalog model and validation

**Files:**
- Modify: `openapps/catalog.py`
- Test: `tests/test_catalog.py`

**Interfaces:**
- Add frozen dataclass `InstallPlan(platform: str, label: str, command: str, notes: str = "")` with `from_mapping()` and `to_dict()` helpers.
- Extend `App` with defaults: `replaces: tuple[str, ...] = ()`, `platforms: tuple[str, ...] = ()`, `pricing_model: str = "unknown"`, `privacy_model: str = "mixed"`, `setup_minutes: int = 0`, and `install_plans: tuple[InstallPlan, ...] = ()`.
- Add `search_replacements(apps: Iterable[App], query: str) -> tuple[App, ...]` as the intent-search entry point.
- Add `get_install_plan(app: App, platform: str) -> InstallPlan | None` with exact platform matching and an `all` platform that returns `None`.

**Allowed values:**
- Platforms: `windows`, `macos`, `linux`, `docker`, `web`.
- Pricing models: `free`, `free-self-hosted`, `open-core`, `unknown`.
- Privacy models: `local`, `self-hosted`, `mixed`, `cloud`, `unknown`.

- [ ] **Step 1: Write failing model and validation tests**

```python
def test_app_round_trips_replacement_and_install_plan_metadata():
    app = App.from_mapping({
        "slug": "demo",
        "name": "Demo",
        "repo": "owner/demo",
        "summary": "Demo app",
        "replaces": ["PaidApp"],
        "platforms": ["docker"],
        "pricing_model": "free-self-hosted",
        "privacy_model": "self-hosted",
        "setup_minutes": 12,
        "install_plans": [{
            "platform": "docker",
            "label": "Docker",
            "command": "docker compose up -d",
            "notes": "Review storage first.",
        }],
    })

    payload = app.to_dict()

    self.assertEqual(payload["replaces"], ["PaidApp"])
    self.assertEqual(payload["install_plans"][0]["platform"], "docker")
    self.assertEqual(app.setup_minutes, 12)


def test_validation_rejects_invalid_comparison_metadata():
    app = App(
        slug="bad",
        name="Bad",
        repo="owner/bad",
        summary="Bad metadata",
        platforms=("amiga",),
        pricing_model="paid",
        privacy_model="secret",
        setup_minutes=-1,
        install_plans=(InstallPlan("docker", "Docker", ""),),
    )

    errors = validate_catalog((app,))

    self.assertIn("invalid platform: bad: amiga", errors)
    self.assertIn("invalid pricing model: bad", errors)
    self.assertIn("invalid privacy model: bad", errors)
    self.assertIn("negative setup time: bad", errors)
    self.assertIn("missing install command: bad: docker", errors)
```

- [ ] **Step 2: Run the focused tests and confirm they fail because the fields and validators are missing**

Run: `rtk py -m unittest tests.test_catalog.CatalogTests.test_app_round_trips_replacement_and_install_plan_metadata tests.test_catalog.CatalogTests.test_validation_rejects_invalid_comparison_metadata -v`

Expected: FAIL with missing `App` metadata or validation behavior.

- [ ] **Step 3: Implement the dataclass fields, mapping conversion, serialization, and validation constants**

Normalize string lists by stripping whitespace. Serialize tuples as JSON lists. Add validation for empty replacement aliases, unsupported platforms, invalid pricing/privacy values, negative setup time, duplicate install-plan platforms, and empty install commands. Keep old catalog JSON valid through the declared defaults.

- [ ] **Step 4: Run the focused tests and then the existing suite**

Run: `rtk py -m unittest tests.test_catalog.CatalogTests.test_app_round_trips_replacement_and_install_plan_metadata tests.test_catalog.CatalogTests.test_validation_rejects_invalid_comparison_metadata -v`

Expected: PASS.

Run: `rtk py -m unittest discover -s tests -v`

Expected: 10 existing tests plus the new model tests pass.

- [ ] **Step 5: Commit the model change**

```bash
rtk git add openapps/catalog.py tests/test_catalog.py
rtk git commit -m "feat: add replacement metadata to catalog"
```

### Task 2: Add intent search, safe plans, and share output

**Files:**
- Modify: `openapps/catalog.py`
- Modify: `openapps/cli.py`
- Modify: `openapps/render.py`
- Test: `tests/test_catalog.py`

**Interfaces:**
- `search_replacements()` gives exact replacement aliases score 1200, exact app names 1000, partial aliases 900, partial names 800, exact tags 700, and generic text 300.
- `get_install_plan(app, platform)` returns the matching `InstallPlan` or `None`; `all` deliberately returns `None` so the CLI can print all available plans.
- `render_share(app: App) -> str` returns Markdown with the app name, replacement aliases, privacy/pricing metadata, upstream URL, and a short safety note.
- CLI commands:
  - `openapps replace QUERY [--json]`
  - `openapps plan SLUG [--platform {windows,macos,linux,docker,web,all}]`
  - `openapps share SLUG`

- [ ] **Step 1: Write failing search, plan, share, and CLI tests**

```python
def test_replacement_alias_exact_match_beats_generic_match(self):
    apps = (
        App(slug="generic", name="Generic", repo="o/generic", summary="notion notes"),
        App(slug="replacement", name="Replacement", repo="o/replacement", summary="A notes app", replaces=("Notion",)),
    )

    results = search_replacements(apps, "notion")

    self.assertEqual(results[0].slug, "replacement")


def test_plan_command_prints_reviewable_data_without_running_it(self):
    output = io.StringIO()
    with redirect_stdout(output):
        exit_code = main(["plan", "demo", "--platform", "docker"])

    self.assertEqual(exit_code, 0)
    self.assertIn("docker compose up -d", output.getvalue())
    self.assertIn("Review", output.getvalue())


def test_share_command_prints_upstream_markdown(self):
    output = io.StringIO()
    with redirect_stdout(output):
        exit_code = main(["share", "rustdesk"])

    self.assertEqual(exit_code, 0)
    self.assertIn("https://github.com/rustdesk/rustdesk", output.getvalue())
    self.assertIn("OpenApps", output.getvalue())
```

Use a temporary catalog override or a small test `App` fixture for the plan test so it does not depend on an external command or network.

- [ ] **Step 2: Run the focused tests and confirm the new commands fail**

Run: `rtk py -m unittest tests.test_catalog.CatalogTests.test_replacement_alias_exact_match_beats_generic_match tests.test_catalog.CliTests.test_plan_command_prints_reviewable_data_without_running_it tests.test_catalog.CliTests.test_share_command_prints_upstream_markdown -v`

Expected: FAIL because the new command parsers and rendering functions do not exist.

- [ ] **Step 3: Implement ranking and CLI behavior**

Include `replaces` in generic search text. Make `replace` use the intent scorer and the existing JSON/text row formats. Make `plan` return exit code 2 for an unknown slug or unsupported platform, print all known plans for `all`, and print an upstream-guidance message when no verified plan exists. Make `share` return exit code 2 for an unknown slug. Do not import `subprocess`, `os.system`, or any installer library.

- [ ] **Step 4: Run focused tests, then the full suite**

Run: `rtk py -m unittest tests.test_catalog.CatalogTests.test_replacement_alias_exact_match_beats_generic_match tests.test_catalog.CliTests.test_plan_command_prints_reviewable_data_without_running_it tests.test_catalog.CliTests.test_share_command_prints_upstream_markdown -v`

Expected: PASS.

Run: `rtk py -m unittest discover -s tests -v`

Expected: all tests pass.

- [ ] **Step 5: Commit the CLI feature**

```bash
rtk git add openapps/catalog.py openapps/cli.py openapps/render.py tests/test_catalog.py
rtk git commit -m "feat: add replacement plans and share output"
```

### Task 3: Curate the first replacement journeys

**Files:**
- Modify: `openapps/catalog.json`
- Modify: `tests/test_catalog.py`
- Modify: `docs/catalog-format.md`

**Interfaces:**
- Add two catalog entries: `appflowy` for the Notion journey and `nextcloud` for the Dropbox journey.
- Add replacement aliases to existing entries: RustDesk → TeamViewer/AnyDesk, PostHog → Google Analytics/Mixpanel, Formbricks → Typeform/SurveyMonkey, Jellyfin → Plex/Emby, Appsmith → Retool, Authentik → Okta/Auth0, and changedetection.io → Visualping.
- Keep all 27 entries valid and make each replacement journey show at least one result.

- [ ] **Step 1: Write the failing data-journey test**

```python
def test_high_intent_replacement_queries_have_results(self):
    apps = load_catalog()

    for query in ("notion", "dropbox", "teamviewer", "google analytics", "typeform", "plex", "retool", "okta"):
        with self.subTest(query=query):
            self.assertTrue(search_replacements(apps, query), query)
```

- [ ] **Step 2: Run it and confirm the existing catalog lacks at least one journey**

Run: `rtk py -m unittest tests.test_catalog.CatalogTests.test_high_intent_replacement_queries_have_results -v`

Expected: FAIL before the metadata is added.

- [ ] **Step 3: Add metadata and document the contributor schema**

Add explicit `replaces`, platform, pricing, privacy, and setup metadata to the selected entries. Add AppFlowy and Nextcloud with upstream repository links and no invented install command. Document the new fields, allowed values, and the rule that commands must come from reviewed upstream instructions.

- [ ] **Step 4: Run the journey test and catalog doctor**

Run: `rtk py -m unittest tests.test_catalog.CatalogTests.test_high_intent_replacement_queries_have_results -v`

Expected: PASS.

Run: `rtk py -m openapps doctor`

Expected: `Catalog valid: 27 apps`.

- [ ] **Step 5: Commit the curated journeys**

```bash
rtk git add openapps/catalog.json tests/test_catalog.py docs/catalog-format.md
rtk git commit -m "feat: curate popular SaaS replacement journeys"
```

### Task 4: Build the shareable static storefront

**Files:**
- Modify: `openapps/render.py`
- Modify: `tests/test_catalog.py`

**Interfaces:**
- Keep `render_html(apps)` as the public entry point.
- Render a hero with the exact promise `Stop paying for software you can own.` and the question `What do you want to replace?`.
- Embed escaped catalog JSON under a dedicated script data block and use inline JavaScript only for query filtering, platform/privacy filters, selected-card display, URL query updates, and copy buttons.

- [ ] **Step 1: Write failing storefront tests**

```python
def test_storefront_contains_product_promise_and_replacement_controls(self):
    html = render_html(load_catalog())

    self.assertIn("Stop paying for software you can own.", html)
    self.assertIn("What do you want to replace?", html)
    self.assertIn('placeholder="Notion, Dropbox, TeamViewer..."', html)
    self.assertIn("copyShare", html)
    self.assertIn("privacy_model", html)


def test_storefront_escapes_catalog_values_inside_cards_and_data(self):
    app = App(
        slug="demo",
        name="<Demo>",
        repo="owner/demo",
        summary="A </script><script>alert(1)</script> tool",
        replaces=("PaidApp",),
    )

    html = render_html((app,))

    self.assertIn("&lt;Demo&gt;", html)
    self.assertNotIn("</script><script>alert(1)", html)
```

- [ ] **Step 2: Run the focused tests and confirm the current renderer fails them**

Run: `rtk py -m unittest tests.test_catalog.CliTests.test_storefront_contains_product_promise_and_replacement_controls tests.test_catalog.CliTests.test_storefront_escapes_catalog_values_inside_cards_and_data -v`

Expected: FAIL because the current page has no replacement UI and does not have a safe JSON data block.

- [ ] **Step 3: Implement the static storefront**

Use responsive CSS, visible focus states, buttons with text labels, a compact card grid, and a selected-app plan panel. Use `json.dumps(..., ensure_ascii=False)` and neutralize `</` before embedding JSON. All user-visible catalog values must also pass `html.escape`. The browser code must work from a `file://` page and must not fetch remote data.

- [ ] **Step 4: Run focused and full tests, then render a real artifact**

Run: `rtk py -m unittest tests.test_catalog.CliTests.test_storefront_contains_product_promise_and_replacement_controls tests.test_catalog.CliTests.test_storefront_escapes_catalog_values_inside_cards_and_data -v`

Expected: PASS.

Run: `rtk py -m unittest discover -s tests -v`

Expected: all tests pass.

Run: `rtk py -m openapps render --format html --output openapps.html`

Expected: the command writes `openapps.html` in the worktree.

- [ ] **Step 5: Commit the storefront**

```bash
rtk git add openapps/render.py tests/test_catalog.py
rtk git commit -m "feat: add local replacement storefront"
```

### Task 5: Rewrite the public explanation and contributor path

**Files:**
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `openapps/__init__.py`

**Interfaces:**
- Above the README fold, communicate the promise, target user, three-command demo, safety boundary, and a link to the generated storefront workflow.
- Use this copy as the primary headline: `Stop paying for software you can own.`
- Use this subhead: `Find an open-source alternative to the software you already use — then get a reviewable setup plan in seconds.`
- Explain that OpenApps discovers and plans; it does not silently install or execute commands.
- Update the package version to `0.2.0`.

- [ ] **Step 1: Write documentation assertions as a small test**

Add a `DocumentationTests` class in `tests/test_catalog.py` that reads `README.md` and asserts the two exact headline/subhead strings, the `openapps replace notion` example, and the safety phrase `never executes installation commands`.

- [ ] **Step 2: Run the documentation test and confirm it fails against the old README**

Run: `rtk py -m unittest tests.test_catalog.DocumentationTests -v`

Expected: FAIL because the old README does not contain the new product explanation.

- [ ] **Step 3: Rewrite README and contributor guidance**

Add a hero, concrete replacement examples, CLI demo, local HTML demo, feature table, trust/safety section, roadmap, contribution instructions, and a “why this is different” section focused on decision-to-plan rather than another list. Keep claims verifiable and do not promise virality or guaranteed savings.

- [ ] **Step 4: Run documentation and full tests**

Run: `rtk py -m unittest tests.test_catalog.DocumentationTests -v`

Expected: PASS.

Run: `rtk py -m unittest discover -s tests -v`

Expected: all tests pass.

- [ ] **Step 5: Commit the public explanation**

```bash
rtk git add README.md CONTRIBUTING.md openapps/__init__.py tests/test_catalog.py
rtk git commit -m "docs: position openapps as an open-source app store"
```

### Task 6: Final verification and handoff

**Files:**
- Verify: all changed files and Git history

- [ ] **Step 1: Run the complete test suite and catalog checks**

Run: `rtk py -m unittest discover -s tests -v`

Expected: all tests pass with zero failures.

Run: `rtk py -m openapps doctor`

Expected: `Catalog valid: 27 apps`.

- [ ] **Step 2: Exercise the user journey from the command line**

Run: `rtk openapps replace notion`

Expected: AppFlowy appears as a result.

Run: `rtk openapps plan rustdesk --platform all`

Expected: a non-executing upstream-guidance or verified-plan message.

Run: `rtk openapps share rustdesk`

Expected: Markdown with the RustDesk GitHub URL.

- [ ] **Step 3: Inspect the diff and generated artifact**

Run: `rtk git diff main...HEAD --check`

Expected: no whitespace errors.

Run: `rtk git status -sb`

Expected: clean worktree after the generated `openapps.html` is ignored.

- [ ] **Step 4: Commit only if verification is clean**

If all checks pass, use `rtk git log --oneline --decorate -8` and report the branch, commits, test count, catalog count, and exact user commands. Do not claim a viral outcome; report the shipped product and remaining distribution work.

