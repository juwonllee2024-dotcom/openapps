from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


_REPO_PATTERN = re.compile(r"^[^/\s]+/[^/\s]+$")
_DEFAULT_CATALOG = Path(__file__).with_name("catalog.json")


@dataclass(frozen=True)
class App:
    slug: str
    name: str
    repo: str
    summary: str
    category: str = "other"
    language: str = ""
    stars: int = 0
    monthly_stars: int = 0
    website: str = ""
    license: str = ""
    local_fit: str = "mixed"
    tags: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "App":
        fields = {
            "slug": str(value.get("slug", "")).strip(),
            "name": str(value.get("name", "")).strip(),
            "repo": str(value.get("repo", "")).strip(),
            "summary": str(value.get("summary", "")).strip(),
            "category": str(value.get("category", "other")).strip(),
            "language": str(value.get("language", "")).strip(),
            "stars": int(value.get("stars", 0)),
            "monthly_stars": int(value.get("monthly_stars", 0)),
            "website": str(value.get("website", "")).strip(),
            "license": str(value.get("license", "")).strip(),
            "local_fit": str(value.get("local_fit", "mixed")).strip(),
            "tags": tuple(str(tag).strip() for tag in value.get("tags", ())),
        }
        return cls(**fields)

    @property
    def github_url(self) -> str:
        return f"https://github.com/{self.repo}"

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["tags"] = list(self.tags)
        return result

    def search_text(self) -> str:
        return " ".join(
            (
                self.slug,
                self.name,
                self.repo,
                self.summary,
                self.category,
                self.language,
                self.local_fit,
                " ".join(self.tags),
            )
        ).casefold()


def load_catalog(path: Path | str | None = None) -> tuple[App, ...]:
    catalog_path = Path(path) if path is not None else _DEFAULT_CATALOG
    raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("catalog must be a JSON list")
    return tuple(App.from_mapping(item) for item in raw)


def get_app(apps: Iterable[App], slug: str) -> App:
    target = slug.casefold().strip()
    for app in apps:
        if app.slug.casefold() == target:
            return app
    raise KeyError(slug)


def _score(app: App, query: str) -> int:
    normalized = query.casefold().strip()
    if normalized == app.slug.casefold() or normalized == app.name.casefold():
        return 1000
    if normalized in app.slug.casefold() or normalized in app.name.casefold():
        return 800
    if normalized in {tag.casefold() for tag in app.tags}:
        return 700
    if normalized in app.search_text():
        return 300
    return 0


def search_apps(apps: Iterable[App], query: str) -> tuple[App, ...]:
    normalized = query.casefold().strip()
    if not normalized:
        return tuple(sorted(apps, key=lambda app: app.name.casefold()))
    matches = ((app, _score(app, normalized)) for app in apps)
    return tuple(
        app
        for app, score in sorted(
            ((app, score) for app, score in matches if score),
            key=lambda item: (-item[1], item[0].name.casefold()),
        )
    )


def validate_catalog(apps: Iterable[App]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for app in apps:
        if not app.slug:
            errors.append("missing slug")
        elif app.slug in seen:
            errors.append(f"duplicate slug: {app.slug}")
        seen.add(app.slug)
        if not app.name:
            errors.append(f"missing name: {app.slug or '<unknown>'}")
        if not app.repo:
            errors.append(f"missing repo: {app.slug or '<unknown>'}")
        elif not _REPO_PATTERN.match(app.repo):
            errors.append(f"invalid repo: {app.slug}")
        if not app.summary:
            errors.append(f"missing summary: {app.slug or '<unknown>'}")
        if app.stars < 0 or app.monthly_stars < 0:
            errors.append(f"negative stars: {app.slug}")
    return errors
