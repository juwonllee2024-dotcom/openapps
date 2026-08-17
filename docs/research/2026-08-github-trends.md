# GitHub trend research — August 2026

Date captured: 2026-08-16  
Primary source: [GitHub Trending — This month](https://github.com/trending?since=monthly)

## Method

The official GitHub monthly page was inspected as the primary source. It showed 25
repositories in the captured view. Descriptions and star counts below are a compact
snapshot, not a promise that counts remain current. `local_fit` is an OpenApps
classification: `self-hosted` means a server application, `local-tool` means a
desktop/CLI/library/learning resource, and `mixed` means both hosted and self-hosted
paths exist.

## Monthly trending repositories

| Repository | Theme | Stars | Stars this month | Local fit |
|---|---|---:|---:|---|
| [goauthentik/authentik](https://github.com/goauthentik/authentik) | identity | 24,882 | 1,928 | self-hosted |
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | learning | 364,275 | 57,880 | local-tool |
| [hyprwm/Hyprland](https://github.com/hyprwm/Hyprland) | desktop | 37,909 | 1,927 | local-tool |
| [cli/cli](https://github.com/cli/cli) | developer tools | 45,854 | 8,870 | local-tool |
| [paperless-ngx/paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) | documents | 44,327 | 3,033 | self-hosted |
| [jellyfin/jellyfin](https://github.com/jellyfin/jellyfin) | media | 55,859 | 5,316 | self-hosted |
| [tailscale/tailscale](https://github.com/tailscale/tailscale) | networking | 35,257 | 3,076 | mixed |
| [PostHog/posthog](https://github.com/PostHog/posthog) | analytics | 37,712 | 3,189 | mixed |
| [sundowndev/phoneinfoga](https://github.com/sundowndev/phoneinfoga) | security | 17,525 | 5,607 | local-tool |
| [DioxusLabs/dioxus](https://github.com/DioxusLabs/dioxus) | framework | 38,748 | 1,849 | local-tool |
| [traefik/traefik](https://github.com/traefik/traefik) | networking | 64,461 | 6,138 | self-hosted |
| [grokability/snipe-it](https://github.com/grokability/snipe-it) | operations | 14,825 | 3,958 | self-hosted |
| [novuhq/novu](https://github.com/novuhq/novu) | notifications | 39,592 | 4,427 | self-hosted |
| [caddyserver/caddy](https://github.com/caddyserver/caddy) | web server | 74,959 | 4,890 | self-hosted |
| [PowerShell/PowerShell](https://github.com/PowerShell/PowerShell) | developer tools | 54,919 | 8,427 | local-tool |
| [dgtlmoon/changedetection.io](https://github.com/dgtlmoon/changedetection.io) | monitoring | 33,198 | 1,966 | self-hosted |
| [formbricks/formbricks](https://github.com/formbricks/formbricks) | forms | 12,777 | 2,463 | self-hosted |
| [ClickHouse/ClickHouse](https://github.com/ClickHouse/ClickHouse) | database | 49,288 | 8,807 | self-hosted |
| [rclone/rclone](https://github.com/rclone/rclone) | storage | 59,194 | 5,318 | local-tool |
| [paperswithbacktest/awesome-systematic-trading](https://github.com/paperswithbacktest/awesome-systematic-trading) | learning | 13,387 | 1,626 | local-tool |
| [saadeghi/daisyui](https://github.com/saadeghi/daisyui) | frontend | 42,104 | 1,676 | local-tool |
| [rustdesk/rustdesk](https://github.com/rustdesk/rustdesk) | remote desktop | 121,032 | 18,505 | self-hosted |
| [schollz/croc](https://github.com/schollz/croc) | file transfer | 39,839 | 1,585 | local-tool |
| [appsmithorg/appsmith](https://github.com/appsmithorg/appsmith) | internal tools | 40,677 | 4,730 | self-hosted |
| [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) | learning | 540,315 | 51,010 | local-tool |

## Findings

1. **Self-hosting is not niche.** Authentication, documents, media, networking,
   analytics, monitoring, databases, and internal tools all appear in one monthly
   snapshot.
2. **Instant utility wins.** GitHub CLI, PowerShell, rclone, croc, and changedetection
   have a clear first command. Users can understand value before reading architecture.
3. **Learning has exceptional distribution.** The two learning repositories in the
   snapshot account for a large share of monthly stars. Searchable, copyable examples
   compound over time.
4. **One catalog is not enough.** [awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted)
   is already a very large list. OpenApps must add comparison, local fit, deployment
   planning, and validation instead of copying a directory.
5. **AI is an option, not the product boundary.** Current local-first projects often
   offer local and cloud providers. OpenApps keeps discovery and deployment planning
   useful without either.

## Product decision

Build OpenApps as a **local-first open-source app catalog and deployment-planning
tool**. Start with a deterministic CLI and a catalog that anyone can inspect or
contribute to. Add verified launchers only after manifests have reviewable metadata,
resource requirements, backup notes, and rollback behavior.

This combines the strongest signals without cloning a single trending repository:
the breadth of self-hosted software, the instant utility of CLI tools, the shareability
of curated learning repositories, and the ownership promise of local execution.

## Limits

GitHub stars are an outcome, not an engineering requirement. 100k stars cannot be
guaranteed. The project therefore optimizes for durable adoption: low install friction,
transparent data, useful output on first run, contributor-friendly manifests, and a
natural reason for every listed project to share its entry.
