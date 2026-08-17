import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from openapps.catalog import App, get_app, load_catalog, search_apps, validate_catalog
from openapps.cli import _app_rows, main
from openapps.render import render_html, render_markdown


class CatalogTests(unittest.TestCase):
    def test_bundled_catalog_is_valid_and_contains_monthly_trending_repositories(self):
        apps = load_catalog()

        self.assertEqual(len(apps), 25)
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

    def test_validation_rejects_duplicate_slugs_and_missing_repository(self):
        apps = (
            App(slug="same", name="One", repo="owner/repo", summary="x"),
            App(slug="same", name="Two", repo="", summary="x"),
        )

        errors = validate_catalog(apps)

        self.assertIn("duplicate slug: same", errors)
        self.assertIn("missing repo: same", errors)

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

    def test_doctor_reports_valid_catalog(self):
        output = io.StringIO()

        with redirect_stdout(output):
            exit_code = main(["doctor"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Catalog valid: 25 apps", output.getvalue())

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


if __name__ == "__main__":
    unittest.main()
