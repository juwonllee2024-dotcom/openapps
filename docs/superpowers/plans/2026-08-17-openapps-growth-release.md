# OpenApps Growth Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox ([ ] / [x]) syntax for tracking.

**Goal:** Publish a real local demo, a reproducible recording of tested user flows, and an installable GitHub Release so OpenApps can be tried and shared without cloning the repository.

**Architecture:** Reuse the existing standard-library renderer to generate docs/index.html for GitHub Pages. Add a development-only recording script that runs the real CLI through sys.executable -m openapps, captures its outputs, and renders a terminal GIF plus transcript. Keep release artifacts outside git and attach them to a tagged GitHub Release after the branch is merged.

**Tech Stack:** Python 3.11+, standard library runtime, Pillow and ffmpeg for local artifact generation, GitHub Actions Pages deployment, setuptools wheel/sdist.

## Global Constraints

- Do not add Pillow or ffmpeg as runtime dependencies.
- The recording must execute the actual CLI commands and preserve their captured output in a text transcript.
- The GIF and transcript must be generated from a clean worktree using the current source.
- The Pages site must be static and must not collect analytics or make runtime network requests.
- Release validation must install the built wheel into a temporary virtual environment without reaching PyPI.
- Preserve all existing tests and the safety boundary: OpenApps never executes catalog install commands.

---

### Task 1: Add reproducible demo and Pages assets

**Files:**
- Create: scripts/record_demo.py
- Create: docs/index.html by running the existing renderer
- Create: .github/workflows/pages.yml
- Test: tests/test_catalog.py

**Interfaces:**
- scripts/record_demo.py --output-dir assets runs four real flows and writes assets/openapps-demo.gif and assets/openapps-demo-transcript.txt.
- The Pages workflow deploys the checked-in docs/ directory on pushes to main.
- README must link to https://juwonllee2024-dotcom.github.io/openapps/ and embed assets/openapps-demo.gif.

- [ ] Step 1: Write failing documentation/asset assertions

Assert that README contains the demo URL and GIF path, and that the workflow contains actions/configure-pages, actions/upload-pages-artifact, and actions/deploy-pages.

- [ ] Step 2: Run the focused assertions and confirm they fail

Run: rtk py -m unittest tests.test_catalog.DocumentationTests -v

Expected: FAIL because no public demo link or recording path exists yet.

- [ ] Step 3: Implement the workflow, recording script, and generated demo page

The script must capture these real commands:

    python -m openapps replace notion
    python -m openapps plan rustdesk --platform all
    python -m openapps share rustdesk
    python -m openapps render --format html --output docs/index.html

Render each captured result as a terminal-style Pillow frame, save an animated GIF, and save the exact command/output transcript. Run the script from the repository root so docs/index.html is the real storefront.

- [ ] Step 4: Run focused assertions and the recording script

Run: rtk py -m unittest tests.test_catalog.DocumentationTests -v

Expected: PASS.

Run: rtk py scripts/record_demo.py --output-dir assets

Expected: the GIF and transcript exist and the transcript contains AppFlowy, RustDesk, and the generated docs/index.html path.

- [ ] Step 5: Commit demo assets and workflow

    rtk git add scripts/record_demo.py docs/index.html .github/workflows/pages.yml assets/openapps-demo.gif assets/openapps-demo-transcript.txt tests/test_catalog.py README.md
    rtk git commit -m "feat: add public demo and tested product recording"

### Task 2: Add release validation and build artifacts

**Files:**
- Create: scripts/verify_release.ps1
- Modify: README.md
- Test: tests/test_catalog.py

**Interfaces:**
- scripts/verify_release.ps1 -WheelPath <path> creates a temporary venv, installs only the wheel from the local directory, runs python -m openapps doctor, and runs python -m openapps replace notion.
- README includes install instructions for the GitHub Release asset and a visible latest-release link.

- [ ] Step 1: Write failing documentation assertions for release install

Assert README contains the GitHub releases URL, pip install, and openapps replace notion.

- [ ] Step 2: Run the focused test and confirm the release section is missing

Run: rtk py -m unittest tests.test_catalog.DocumentationTests -v

Expected: FAIL on the release URL assertion.

- [ ] Step 3: Add the verifier and release instructions

Build with python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist, run the verifier against the wheel, and document the exact local install command using the release asset. The verifier must remove only its own temporary venv under the worktree.

- [ ] Step 4: Build and test the wheel

Run: rtk py -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist

Expected: a wheel named openapps_catalog-0.2.0-py3-none-any.whl.

Run: rtk powershell -NoProfile -ExecutionPolicy Bypass -File scripts/verify_release.ps1 -WheelPath <wheel path>

Expected: doctor reports 27 valid apps and replacement search returns AppFlowy.

- [ ] Step 5: Commit release tooling

    rtk git add scripts/verify_release.ps1 README.md tests/test_catalog.py
    rtk git commit -m "feat: add release install verification"

### Task 3: Full verification, publish, and release

**Files:**
- Verify: all changed files, generated assets, GitHub Actions, and release assets

- [ ] Step 1: Run the full local suite and artifact checks

Run: rtk py -m unittest discover -s tests -v

Expected: all tests pass.

Run: rtk py -m openapps doctor

Expected: Catalog valid: 27 apps.

Run: rtk powershell -NoProfile -Command "Get-Item assets/openapps-demo.gif,assets/openapps-demo-transcript.txt,docs/index.html | Select-Object Name,Length"

Expected: all three artifacts exist and the GIF has nonzero size.

- [ ] Step 2: Push and merge the growth branch

Push codex/openapps-growth, create a PR targeting main, wait for CI, and merge only after checks pass.

- [ ] Step 3: Enable and verify GitHub Pages

Configure Pages to deploy through the workflow, verify the workflow succeeds, and confirm the public URL serves the generated storefront.

- [ ] Step 4: Create GitHub Release v0.2.0

Build and locally verify the wheel, then create v0.2.0 with the wheel and sdist attached. Release notes must link the demo, GIF, and tested CLI flows.

- [ ] Step 5: Report evidence

Report the release URL, Pages URL, demo GIF path, test count, wheel verification result, and any external limitation such as Pages propagation delay. Do not claim virality; report the public distribution assets and measurable next actions.
