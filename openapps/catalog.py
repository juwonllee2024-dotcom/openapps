from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


_REPO_PATTERN = re.compile(r"^[^/\s]+/[^/\s]+$")
_DEFAULT_CATALOG = Path(__file__).with_name("catalog.json")
_PLATFORMS = frozenset({"windows", "macos", "linux", "docker", "web"})
_PRICING_MODELS = frozenset({"free", "free-self-hosted", "open-core", "unknown"})
_PRIVACY_MODELS = frozenset({"local", "self-hosted", "mixed", "cloud", "unknown"})


def _string_tuple(value: Any) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(str(item).strip() for item in value)


@dataclass(frozen=True)
class InstallPlan:
    platform: str
    label: str
    command: str
    notes: str = ""

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "InstallPlan":
        return cls(
            platform=str(value.get("platform", "")).strip(),
            label=str(value.get("label", "")).strip(),
            command=str(value.get("command", "")).strip(),
            notes=str(value.get("notes", "")).strip(),
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "platform": self.platform,
            "label": self.label,
            "command": self.command,
            "notes": self.notes,
        }


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
    replaces: tuple[str, ...] = ()
    platforms: tuple[str, ...] = ()
    pricing_model: str = "unknown"
    privacy_model: str = "mixed"
    setup_minutes: int = 0
    install_plans: tuple[InstallPlan, ...] = ()

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
            "tags": _string_tuple(value.get("tags", ())),
            "replaces": _string_tuple(value.get("replaces", ())),
            "platforms": _string_tuple(value.get("platforms", ())),
            "pricing_model": str(value.get("pricing_model", "unknown")).strip(),
            "privacy_model": str(value.get("privacy_model", "mixed")).strip(),
            "setup_minutes": int(value.get("setup_minutes", 0)),
            "install_plans": tuple(
                InstallPlan.from_mapping(plan)
                for plan in value.get("install_plans", ())
                if isinstance(plan, dict)
            ),
        }
        return cls(**fields)

    @property
    def github_url(self) -> str:
        return f"https://github.com/{self.repo}"

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["tags"] = list(self.tags)
        result["replaces"] = list(self.replaces)
        result["platforms"] = list(self.platforms)
        result["install_plans"] = [plan.to_dict() for plan in self.install_plans]
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
                " ".join(self.replaces),
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


def _replacement_score(app: App, query: str) -> int:
    normalized = query.casefold().strip()
    aliases = tuple(alias.casefold() for alias in app.replaces)
    if normalized in aliases:
        return 1200
    if normalized == app.slug.casefold() or normalized == app.name.casefold():
        return 1000
    if any(normalized in alias for alias in aliases):
        return 900
    if normalized in app.slug.casefold() or normalized in app.name.casefold():
        return 800
    if normalized in {tag.casefold() for tag in app.tags}:
        return 700
    if normalized in app.search_text():
        return 300
    return 0


def search_replacements(apps: Iterable[App], query: str) -> tuple[App, ...]:
    normalized = query.casefold().strip()
    if not normalized:
        return tuple(sorted(apps, key=lambda app: app.name.casefold()))
    matches = ((app, _replacement_score(app, normalized)) for app in apps)
    return tuple(
        app
        for app, score in sorted(
            ((app, score) for app, score in matches if score),
            key=lambda item: (-item[1], item[0].name.casefold()),
        )
    )


def get_install_plan(app: App, platform: str) -> InstallPlan | None:
    normalized = platform.casefold().strip()
    if normalized == "all":
        return None
    return next(
        (plan for plan in app.install_plans if plan.platform.casefold() == normalized),
        None,
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
        for replacement in app.replaces:
            if not replacement:
                errors.append(f"empty replacement alias: {app.slug}")
        for platform in app.platforms:
            if platform not in _PLATFORMS:
                errors.append(f"invalid platform: {app.slug}: {platform}")
        if app.pricing_model not in _PRICING_MODELS:
            errors.append(f"invalid pricing model: {app.slug}")
        if app.privacy_model not in _PRIVACY_MODELS:
            errors.append(f"invalid privacy model: {app.slug}")
        if app.setup_minutes < 0:
            errors.append(f"negative setup time: {app.slug}")
        plan_platforms: set[str] = set()
        for plan in app.install_plans:
            if plan.platform not in _PLATFORMS:
                errors.append(f"invalid install platform: {app.slug}: {plan.platform}")
            if plan.platform in plan_platforms:
                errors.append(f"duplicate install platform: {app.slug}: {plan.platform}")
            plan_platforms.add(plan.platform)
            if not plan.command:
                errors.append(f"missing install command: {app.slug}: {plan.platform}")
    return errors
