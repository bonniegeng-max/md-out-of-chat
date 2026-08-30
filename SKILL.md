---
name: md-out-of-chat
description: Convert a Markdown file into a mobile-friendly local HTML page or phone-sized screenshot. Safe default is local-only; a public web URL is only produced when the user explicitly asks for it or the host platform deploy tool is used. Respond in the user's current language.
version: 1.3.2
homepage: https://github.com/bonniegeng-max/md-out-of-chat
license: MIT
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["python3"],"packages":[],"env":[]}}}
---

# md-out-of-chat

**Pulling Markdown out of chat, into something people can actually read.**

AI agents live in chat (WeChat, Feishu, Slack, Discord, …) and love to write `.md`. But `.md` doesn't render well in any of those apps. Code breaks, tables misalign, links look dead. This skill is the bridge: it takes a `.md` file and turns it into a mobile-friendly, copyable, shareable view.

## Activation

Only activate this skill when the user explicitly mentions it by name (e.g. "use md-out-of-chat", "用 md-out-of-chat 转换") or clearly asks to convert a Markdown file into a readable view / screenshot. Do not activate on vague phrases like "show me this" or "转一下" alone.

## The Problem

- `.md` files **cannot be opened in WeChat** on mobile
- Code blocks **break layout** on small screens
- Tables **misalign columns** on mobile
- When you're away from your computer, you **can't view** what your assistant just made

## Input

- Path to a `.md` file
- Optional output type: `html` (local file, default), `web` (public URL only when user explicitly requests it and a deploy tool is available), or `screenshot` (render to PNG)

## Output

- Default: a local `.html` file that opens in any mobile browser
- `screenshot`: one or more PNG images at phone screen size
- `web`: a public URL **only** if the user explicitly asks for it and the assistant has a deploy tool; otherwise fall back to local HTML + screenshot

## Design Spec (Blue / White / Gray — Minimal & Clean)

### Colors
- Primary: `#1F4E79` (deep blue, used for titles & headings)
- Accent: `#3B7DD8` (bright blue, used for emphasis)
- Background: `#F5F7FA` (light gray)
- Card: `#FFFFFF` (white)
- Text: `#333333` (main) / `#666666` (secondary)
- Border: `#E1E5EB`

### Typography
- Body: `system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif`
- Code: `"SF Mono", Menlo, Monaco, Consolas, monospace`
- Base size: 16px (auto-shrinks on small screens)

## Block Rules

### Headings (h1–h6)
- Color: deep blue
- Weight: 600
- h1: 24px / h2: 20px / h3: 18px
- h1 has a 2px bottom border

### Paragraphs
- 16px, line-height 1.7
- Inline: `**bold**` → strong, `*italic*` → em, `` `code` `` → inline code

### Tables
- Column-aligned
- Header: deep blue background, white text, bold
- Zebra striping (odd / even rows)
- `white-space: nowrap` on headers
- Wraps in a scrollable container on narrow screens

### Code Blocks
- Top label shows the language (e.g. `PYTHON`, `SQL`, `BASH`)
- Syntax highlighting per language:
  - Keywords: red, bold
  - Strings: green
  - Numbers: blue
  - Comments: gray, italic
- Horizontal scroll for long lines
- Never breaks layout

### Lists
- Unordered: bullet points
- Ordered: numbered
- Task lists: `- [ ]` / `- [x]` render as checkboxes (done items struck through)
- 6px vertical spacing between items

### Blockquotes
- `>` lines render as a left-accent-border quote block, gray text

### Links
- `[text](url)` renders as styled anchor; only `http:` / `https:` / `mailto:` schemes allowed (XSS-safe)
- Long URLs wrap on mobile (`word-break: break-all`)

### Inline in table cells
- Cell content supports bold / italic / inline code / links
- `\|` escapes a literal pipe inside cells

## Output Type Decision

Default to **local HTML** for safety and privacy. Only produce a public web URL when the user explicitly asks for one and the assistant has a safe deploy path. Offer a screenshot as an alternative when the user asks for an image or when sharing as a picture is more reliable.

### Default: Local HTML

When the user asks to view a Markdown file without specifying the output type, generate a local `.html` file. Tell the user where it is and that it can be opened on a phone browser.

### When to Generate a Screenshot

Generate a screenshot only when:
- The user explicitly says "screenshot" / "image" / "图片" / "截个图"
- The user asks for a picture to send to someone
- This skill ships no browser automation script; render the PNG with the host environment's own screenshot/browser tool. If none is available, deliver local HTML and explain.

### When to Generate a Public Web URL

Generate a public URL only when:
- The user explicitly says "web" / "link" / "URL" / "公开链接"
- The assistant has a trusted, temporary deploy tool available

Never generate a public URL silently. If deployment is not available, fall back to local HTML and explain why.

## Mobile Responsive

- Body padding shrinks on `< 480px` width
- Container padding: 32px → 20px
- Code font shrinks: 14px → 13px
- Table font shrinks: 14px → 13px

## Privacy

- Runs **locally** by default. The core `md2share.py` only reads the input `.md` and writes a local `.html` file.
- `build_and_deploy.sh` only prepares a local `dist/` folder; it does not upload anything.
- Screenshots are rendered by the host environment's own browser/screenshot tool; this skill includes no browser automation code.
- A public URL is produced **only** when the user explicitly requests it and the assistant has a trusted deploy tool.
- **Local images** (`![alt](./image.png)`) are embedded as base64 by default, but **only** if they live in the same directory as the Markdown file or a subdirectory of it. Absolute paths and parent-directory traversal (`../`) are blocked unless the user explicitly passes `--embed-local-images=all`.
- **Remote images** are never fetched automatically; they are rendered as a link placeholder to avoid network requests.
- The user does not need to register any account.
- This skill **never** sends user content to external APIs without explicit consent.

## Usage Example

```bash
# 1. Write or place your .md file
# 2. Generate a local HTML file (default: local images under .md dir are embedded)
python3 md2share.py my-notes.md

# 3. (Optional) Allow embedding local images from absolute paths or outside the .md directory
python3 md2share.py my-notes.md --embed-local-images=all

# 4. (Optional) Build dist/ for deployment
./build_and_deploy.sh my-notes.md

# 5. (Optional) Screenshot: render my-notes.html with your own browser/screenshot tool
```

## Files

- `md2share.py` — Core script (md → local html)
- `build_and_deploy.sh` — Local build helper (prepares `dist/`)
- `SKILL.md` — This file

## Limitations

- MD parser supports nested lists (any depth, mixed ordered/unordered) and images (local files embedded as base64, remote images rendered as a link placeholder so no network request is made; local image embedding is sandboxed to the Markdown file's directory and its subdirectories by default)
- Footnotes: `[^id]` refs render as superscript anchors, definitions collected into a NOTES section at the bottom with back-links
- Horizontal rules (`---`, `***`, `___`) render as styled dividers
- Dark mode: follows `prefers-color-scheme` with a manual toggle that remembers the choice
- Code highlighter covers python / javascript / bash / sql out of the box; other languages render as plain text with a label
- Highlighter is regex-based (single-pass tokenize: comment → string → keyword → number, no nesting bugs)
