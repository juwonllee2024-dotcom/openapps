<!-- JUWON-PORTFOLIO-INTRO:START -->
# OpenApps / GitHub Automation

![OpenApps / GitHub Automation — portfolio visual](docs/portfolio-preview.svg)

*Portfolio introduction card, not a screenshot of a running application.*

*포트폴리오 소개 카드입니다. 실행 화면 캡처가 아닙니다.*

## English

A local-first catalog for finding, comparing, and reviewing open-source alternatives. It produces reviewable setup plans; it does not silently install the recommended software.

[View JUWON's portfolio](https://jupt.pages.dev/) · [Browse the project collection](https://jupt.pages.dev/projects)

**Scope:** This README presents the repository's documented intent and recorded visual evidence. It does not certify that every feature is complete, deployed, or currently working. Follow the original setup, safety, and license documentation below.

## 한국어

직접 실행할 수 있는 오픈소스 앱을 발견·검색·비교하는 로컬 카탈로그.

[JUWON 포트폴리오 보기](https://jupt.pages.dev/) · [전체 프로젝트 보기](https://jupt.pages.dev/projects)

**확인 범위:** 저장소의 문서상 목적과 기록된 화면 근거를 소개합니다. 모든 기능의 완성·배포·현재 정상 작동을 보증하지 않습니다. 설치법·안전 주의사항·라이선스는 아래 기존 문서를 확인하세요.
<!-- JUWON-PORTFOLIO-INTRO:END -->

---

## Original documentation / 기존 문서

# 🚀 OpenApps

> **💸 Stop paying for software you can own.**

🔍 Find an open-source alternative to the software you already use — then get a reviewable setup plan in seconds.

🧭 OpenApps is a local-first open-source App Store for people who want to replace paid software without handing their data to another directory, account, or AI service.

    🚀 name the paid app  →  🔍 compare alternatives  →  🛡️ review the setup  →  📤 share the find

⭐ If OpenApps saves you time, star the repo and share an alternative you trust.

## ⚡ Try it in under a minute

    python -m pip install -e .

    # 🔍 What can replace the software I already use?
    openapps replace notion

    # 🛡️ What should I review before setup?
    openapps plan appflowy --platform all

    # 📤 Share a useful answer with a teammate
    openapps share appflowy

    # 🌐 Open the local visual storefront
    openapps render --format html --output openapps.html

🌐 Open openapps.html in any browser. Search examples include Notion, Dropbox, TeamViewer, Google Analytics, Typeform, Plex, Retool, and Okta.

## 💡 Why OpenApps?

Most software lists stop at “here is a link.” The expensive part comes next:

- 🖥️ Is this actually a fit for my device or server?
- 🔒 Is my data local, self-hosted, or sent to a cloud?
- ⏱️ How hard is the first setup?
- 🛡️ What should I inspect before I run anything?

✨ OpenApps turns that moment into a short, transparent decision. The catalog is plain JSON, the search works offline, and every upstream project stays linked to its original source.

## ✅ What works today

- 🔍 Intent search: openapps replace notion ranks replacement aliases before generic text matches.
- 📊 Comparison metadata: replacements, platforms, pricing model, privacy model, and setup estimate.
- 🛡️ Reviewable plans: commands are shown for inspection only; OpenApps never executes installation commands.
- 📤 Shareable briefs: copy a concise Markdown explanation with an upstream link.
- 🌐 Local storefront: responsive static HTML with search, filters, comparison cards, and copy-to-share behavior.
- 🧰 27 curated projects, including eight high-intent SaaS replacement journeys.
- 🔐 No account, model, cloud dependency, tracking pixel, or runtime dependency outside Python’s standard library.

## 🛡️ Trust boundary

OpenApps is a discovery and planning layer. It never executes installation commands, downloads software, elevates privileges, or silently changes your machine. A plan is a suggestion to review against the upstream project’s current documentation.

⚠️ Always check the upstream license, release notes, security guidance, storage requirements, and backup plan before deployment.

## 🧰 Commands

| Command | Use |
| --- | --- |
| openapps replace QUERY | Find open-source alternatives to a paid product or use case |
| openapps search QUERY | Search every catalog field |
| openapps show SLUG | Read a Markdown app brief |
| openapps plan SLUG | Print a non-executing setup plan |
| openapps share SLUG | Print a shareable Markdown summary |
| openapps render --format html --output openapps.html | Generate the local storefront |
| openapps doctor | Validate catalog metadata |

## 🌟 The difference

OpenApps is not a paid placement marketplace and not a scraped software mirror. It is a reviewable map from a familiar product to an upstream open-source project, with enough context to make the next decision safely.

## 🗺️ Roadmap

- Verified platform-specific setup plans with upstream source references.
- OS, CPU, memory, storage, license, and maintenance filters.
- Backup, upgrade, and rollback recipes.
- Community-maintained manifests with CI validation.
- A hosted, privacy-respecting storefront built from the same public catalog.

## 🤝 Contributing

Add a useful alternative, correct metadata, or improve the decision flow. Start with [CONTRIBUTING.md](CONTRIBUTING.md) and [the catalog format](docs/catalog-format.md). Every trustworthy contribution makes the map better.

## 🔎 Research

The initial catalog direction is documented in [the GitHub trends research note](docs/research/2026-08-github-trends.md).

## 📄 License

MIT. See [LICENSE](LICENSE).

## 🌐 Try the live demo

**[Open the OpenApps storefront](https://juwonllee2024-dotcom.github.io/openapps/)** in your browser. It is the same static catalog you can generate locally, with no account and no runtime cloud dependency.

![OpenApps real CLI smoke test](assets/openapps-demo.gif)

This recording was generated from real `replace`, `plan`, `share`, and `render` commands in this repository. Read the exact output in [the smoke-test transcript](assets/openapps-demo-transcript.txt).

## 📦 Install a release

Download the latest tested wheel from [GitHub Releases](https://github.com/juwonllee2024-dotcom/openapps/releases/latest), then run:

    python -m pip install openapps_catalog-0.2.0-py3-none-any.whl
    openapps replace notion

Each release is checked in a clean temporary virtual environment with [`scripts/verify_release.ps1`](scripts/verify_release.ps1) before it is published.
