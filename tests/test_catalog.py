import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from openapps.catalog import (
    App,
    InstallPlan,
    get_app,
    load_catalog,
    search_apps,
    search_replacements,
    validate_catalog,
)
from openapps.cli import _app_rows, main
from openapps.render import render_html, render_markdown, render_share


class CatalogTests(unittest.TestCase):
    def test_bundled_catalog_is_valid_and_contains_monthly_trending_repositories(self):
        apps = load_catalog()

        self.assertEqual(len(apps), 27)
        self.assertEqual(validate_catalog(apps), [])
        self.assertEqual(get_app(apps, "rustdesk").repo, "rustdesk/rustdesk")

    def test_search_ranks_exact_name_before_description_matches(self):
        apps = load_catalog()

        results = search_apps(apps, "rustdesk")

        self.assertEqual(results[0].slug, "rustdesk")

    def test_search_is_case_insensitive_and_matches_tags(self):
        apps = load_catalog()

        results = search_apps(apps, "REMOTE")

        self.assertIn("rustdesk", {app.slug for app in results})

    def test_replacement_alias_exact_match_beats_generic_match(self):
        apps = (
            App(slug="generic", name="Generic", repo="o/generic", summary="notion notes"),
            App(
                slug="replacement",
                name="Replacement",
                repo="o/replacement",
                summary="A notes app",
                replaces=("Notion",),
            ),
        )

        results = search_replacements(apps, "notion")

        self.assertEqual(results[0].slug, "replacement")

    def test_high_intent_replacement_queries_have_results(self):
        apps = load_catalog()

        for query in (
            "notion",
            "dropbox",
            "teamviewer",
            "google analytics",
            "typeform",
            "plex",
            "retool",
            "okta",
        ):
            with self.subTest(query=query):
                self.assertTrue(search_replacements(apps, query), query)

    def test_validation_rejects_duplicate_slugs_and_missing_repository(self):
        apps = (
            App(slug="same", name="One", repo="owner/repo", summary="x"),
            App(slug="same", name="Two", repo="", summary="x"),
        )

        errors = validate_catalog(apps)

        self.assertIn("duplicate slug: same", errors)
        self.assertIn("missing repo: same", errors)

    def test_app_round_trips_replacement_and_install_plan_metadata(self):
        app = App.from_mapping(
            {
                "slug": "demo",
                "name": "Demo",
                "repo": "owner/demo",
                "summary": "Demo app",
                "replaces": ["PaidApp"],
                "platforms": ["docker"],
                "pricing_model": "free-self-hosted",
                "privacy_model": "self-hosted",
                "setup_minutes": 12,
                "install_plans": [
                    {
                        "platform": "docker",
                        "label": "Docker",
                        "command": "docker compose up -d",
                        "notes": "Review storage first.",
                    }
                ],
            }
        )

        payload = app.to_dict()

        self.assertEqual(payload["replaces"], ["PaidApp"])
        self.assertEqual(payload["install_plans"][0]["platform"], "docker")
        self.assertEqual(app.setup_minutes, 12)

    def test_validation_rejects_invalid_comparison_metadata(self):
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

    def test_renderers_keep_links_and_escape_html(self):
        app = App(
            slug="demo",
            name="<Demo>",
            repo="owner/demo",
            summary="A <useful> tool",
            website="https://example.com/?q=1&x=2",
        )

        markdown = render_markdown(app)
        html = render_html((app,))

        self.assertIn("https://github.com/owner/demo", markdown)
        self.assertIn("&lt;Demo&gt;", html)
        self.assertNotIn("<useful>", html)


class CliTests(unittest.TestCase):
    def test_search_json_outputs_machine_readable_results(self):
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["search", "database", "--json"])

        payload = json.loads(output.getvalue())

        self.assertEqual(exit_code, 0)
        self.assertTrue(any(item["slug"] == "clickhouse" for item in payload))

    def test_show_unknown_app_returns_nonzero_without_traceback(self):
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["show", "does-not-exist"])

        self.assertEqual(exit_code, 2)
        self.assertIn("Unknown app: does-not-exist", output.getvalue())

    def test_plan_command_prints_reviewable_data_without_running_it(self):
        app = App(
            slug="demo",
            name="Demo",
            repo="owner/demo",
            summary="Demo app",
            install_plans=(
                InstallPlan(
                    "docker",
                    "Docker",
                    "docker compose up -d",
                    "Review storage first.",
                ),
            ),
        )
        output = io.StringIO()

        with patch("openapps.cli.load_catalog", return_value=(app,)), redirect_stdout(output):
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

    def test_doctor_reports_valid_catalog(self):
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["doctor"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Catalog valid: 27 apps", output.getvalue())

    def test_text_rows_are_encodable_on_windows_cp949(self):
        app = App(slug="demo", name="Demo", repo="owner/demo", summary="A tool")

        rendered = _app_rows((app,))

        rendered.encode("cp949")
        self.assertIn(" - A tool", rendered)

    def test_render_and_export_write_requested_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            html_path = directory_path / "catalog.html"
            export_path = directory_path / "rustdesk"

            self.assertEqual(main(["render", "--format", "html", "--output", str(html_path)]), 0)
            self.assertEqual(main(["export", "rustdesk", "--output", str(export_path)]), 0)

            self.assertIn("OpenApps", html_path.read_text(encoding="utf-8"))
            self.assertIn("RustDesk", (export_path / "README.md").read_text(encoding="utf-8"))
            self.assertTrue((export_path / "app.json").exists())

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

        self.assertIn('id="catalog-data"', html)
        self.assertIn("&lt;Demo&gt;", html)
        self.assertNotIn("</script><script>alert(1)", html)


if __name__ == "__main__":
    unittest.main()
