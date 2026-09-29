# Changelog

Markdown 转手机网页 · MD Out of Chat（`md-out-of-chat`）的版本变更记录。

- 最新版本：**1.5.3**
- 发布渠道：[ClawHub](https://clawhub.ai/bonniegeng-max/skills/md-out-of-chat)
- 版本数：16（含初始版本）

> 本文件由 ClawHub registry 的逐版本发布记录回溯整理生成（2026-09-29）。此后每次发版请在此追加一条。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

- 新增本 CHANGELOG.md，回溯整理 0.1.0 → 1.5.3 的历史版本记录（内容取自 ClawHub 逐版本发布记录，未改动代码）

## [1.5.3] - 2026-09-13

discoverability fix — categories and topics now set (was 'other'); description leads with a bilingual problem statement plus a Not-for clause; SKILL.md gains When-not-to-use / How-it-differs sections. No behavior change.

## [1.5.2] - 2026-09-07

md-out-of-chat v1.5.2

- Clarified activation rules: the skill now requires both explicit mention by name and explicit identification of an input file.
- Updated privacy and deployment instructions: never infer targets from chat history or invoke deployment/tools unless the user separately requests and confirms.
- Documentation improved to emphasize safety, explicit user consent, and strict scoping of file access.
- No functional/code changes; this is a documentation and behavior clarification release.

## [1.5.1] - 2026-09-07

- Improved HTML escaping for security: all Markdown text, code content, and code-fence language labels are now fully escaped to prevent injection of untrusted scripts into generated pages.
- Language labels in code blocks are further restricted to a safe character set.
- Updated privacy section to clarify HTML escaping and script-injection mitigation.
- Removed obsolete skill-card.md file.

## [1.5.0] - 2026-09-06

Differentiation release: syntax highlighting for 17 languages with aliases; auto-generated collapsible TOC for long documents. Security: image embedding fully sandboxed (all-mode removed, legacy flag deprecated), magic-bytes content validation, build script requires --force to wipe dist/.

## [1.4.0] - 2026-09-06

Security hardening: absolute local paths are never embedded as base64; --embed-local-images=all only relaxes relative traversal and every embedded path is logged to stderr. Docs aligned with implementation (no screenshot claims). SEO: keyword-rich description.

## [1.3.2] - 2026-08-30

Remove the bundled browser automation helper (screenshot.sh). Screenshots are now rendered by the host environment's own tools. Core converter unchanged.

## [1.3.1] - 2026-08-30

Sandbox local image embedding: default mode only embeds images inside the .md directory or its subdirectories; absolute paths and ../ traversal require --embed-local-images=all.

## [1.3.0] - 2026-08-30

Footnotes ([^id] superscript refs + bottom NOTES section with back-links, paper-friendly), styled horizontal rules (---/***/___), dark mode (follows system preference + manual toggle with saved choice)

## [1.2.0] - 2026-08-30

Nested lists (any depth, mixed ordered/unordered), image support (local files embedded as base64, remote images as link placeholder - no auto network request), no duplicate h1 when content already has a title, screenshot.sh auto-detects Chrome on macOS/Linux

## [1.1.4] - 2026-08-29

Fix security review findings: remove auto_push.sh, network-isolate screenshot.sh, narrow activation triggers, default to local HTML, update privacy claims

## [1.1.3] - 2026-08-29

Add clawdbot metadata JSON to SKILL.md; keep skill-card.md for review

## [1.1.2] - 2026-08-29

Publish with source-repo metadata so ClawHub can fetch skill-card.md

## [1.1.1] - 2026-08-29

Add skill-card.md for ClawHub security review; no functional changes

## [1.1.0] - 2026-08-29

Fix syntax-highlight span nesting bug; copy button reads from DOM (halves page size); add blockquote, ordered lists, task lists, styled links, inline formats and pipe escape in table cells; portable build script

## [1.0.0] - 2026-08-29

Initial publish: md to mobile-friendly HTML/screenshot skill

## [0.1.0] - 2026-08-29

Initial release — renders Markdown (.md) files into mobile-friendly web pages or images for easy sharing and viewing, especially in chat apps.

- Converts .md files to either public web URLs or phone-sized PNG screenshots.
- Web view is fully responsive: clean typography, beautiful tables, syntax-highlighted code, and mobile-first layout.
- Smart output selection: defaults to web for convenience, switches to screenshot only when clearly requested or needed.
- No cloud uploads for privacy; everything runs locally except for optional temporary link sharing.
- Simple, reliable, and designed specifically for chat and Chinese/overseas sharing scenarios.
