---
name: md-out-of-chat
description: Turn Markdown reports, AI chat exports, and technical notes into phone-friendly single-page HTML. Built for WeChat / Feishu / Slack / Discord workflows where raw `.md` is painful to read on mobile. Local-first, no upload, no API key, and public deployment only after explicit confirmation.
version: 1.5.3
homepage: https://github.com/bonniegeng-max/md-out-of-chat
license: MIT
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["python3"],"packages":[],"env":[]}}}
---
# md-out-of-chat

**Turn Markdown reports and chat exports into phone-friendly HTML pages.**

AI assistants are excellent at producing Markdown, but chat apps are terrible at rendering it on phones. In WeChat, Feishu, Slack, Discord, and similar tools, code blocks break layout, tables overflow, and links become painful to scan. `md-out-of-chat` fixes that last mile: it takes a Markdown file you explicitly provide and turns it into a mobile-friendly single-page HTML that people can actually open, read, and forward.

Use this when a report, note, proposal, or AI-generated chat export needs to be **read on a phone, forwarded to someone else, or reviewed away from a laptop**.

This skill is **not** a note-taking app, **not** a live Markdown editor, and **not** an image generator. By default it creates a local HTML file. A public web URL is produced only when the user explicitly asks for it and confirms before deployment.

## Activation

Only activate this skill when **both** conditions hold:

1. the user explicitly mentions this skill by name, or clearly asks to convert a Markdown file into a phone-friendly HTML page
2. the user identifies a concrete input — a `.md` file path, an attached file, or a file explicitly selected in the conversation

Do not activate on vague phrases alone ("show me this", "转一下", "convert this"), and never infer conversion targets from chat history. Only read the file(s) the user explicitly identified. Never deploy, publish, or invoke other tools unless the user separately requests and confirms that action.

## Why people install it

- Chat apps render `.md` badly on mobile.
- Teams still need to read AI-generated reports on phones.
- The output must be easy to open, copy, and forward.
- Many users want a safe local default instead of uploading documents to a third-party service.

## Best use cases

- weekly reports
- AI chat export reading
- technical handoff notes
- mobile review of Markdown documents
- shareable HTML pages generated from Markdown without default cloud upload

## The problem

- `.md` files are hard to read inside WeChat and similar chat apps on mobile
- Code blocks break layout on small screens
- Tables become painful to scan
- Good content exists, but people still cannot read it comfortably on phones

## Input

- Path to a `.md` file
- Optional output type: `html` (local file, default) or `web` (public URL — see the strict conditions below)

## Output

- Default: a local `.html` file that opens in any mobile browser
- `web`: a public URL **only** if the user explicitly asks for it, explicitly confirms before anything is deployed, and the assistant has a trusted deploy tool; otherwise fall back to local HTML
- This skill **does not** generate PNG screenshots or images. If the user asks for an image, explain that rendering an HTML file to PNG is up to the host environment's own tools — do not invoke other tools automatically.

## Not the same as

- **A Markdown viewer or note-taking app** — it converts one file you name into a page you can open on a phone. It is not a live editor, and it does not keep a library.
- **An image generator** — no PNG/JPG output. If a picture is needed, that belongs to the host environment's own tools.
- **A publish tool** — local HTML is the default. A public URL is produced only after an explicit, separately confirmed request.


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

Default to **local HTML** for safety and privacy. Only produce a public web URL when the user explicitly asks for one, explicitly confirms, and the assistant has a safe deploy path. Do not generate screenshots — this skill produces HTML only.

### Default: Local HTML

When the user asks to view a Markdown file without specifying the output type, generate a local `.html` file. Tell the user where it is and that it can be opened on a phone browser.

### About Images / Screenshots

This skill does **not** render PNGs. If the user asks for a screenshot:
- Tell them the HTML file is ready and can be opened in any mobile browser.
- If the host environment has its own screenshot/browser tool, the user can ask for it separately — do not invoke other tools automatically on this skill's behalf.

### When to Generate a Public Web URL

Generate a public URL only when **all** of these hold:
- The user explicitly says "web" / "link" / "URL" / "公开链接"
- The user explicitly confirms deployment before anything is published
- The assistant has a trusted, temporary deploy tool available

Never generate a public URL silently. If deployment is not available, fall back to local HTML and explain why. `build_and_deploy.sh` is **off by default** — run it only after the user explicitly asks for a deployable folder.

## Mobile Responsive

- Body padding shrinks on `< 480px` width
- Container padding: 32px → 20px
- Code font shrinks: 14px → 13px
- Table font shrinks: 14px → 13px

## Privacy

- Runs **locally** by default. The core `md2share.py` only reads the input `.md` and writes a local `.html` file.
- `build_and_deploy.sh` only prepares a local `dist/` folder; it does not upload anything and is **off by default**.
- This skill includes no browser automation code and does not generate screenshots.
- A public URL is produced **only** when the user explicitly requests it, explicitly confirms, and the assistant has a trusted deploy tool.
- **Local images** (`![alt](./image.png)`) are embedded as base64 **only** if they live in the same directory as the Markdown file or a subdirectory of it. **Absolute paths and directory traversal (`../`) are never embedded.** Image files are validated by content (magic bytes) before embedding, and every embedded file path is logged to stderr so the user can audit exactly what was read.
- **Remote images** are never fetched automatically; they are rendered as a link placeholder to avoid network requests.
- **Generated HTML is fully escaped.** All Markdown text, code content, and code-fence language labels are HTML-escaped before being written into the output page (language labels are additionally restricted to a safe character set), so untrusted Markdown cannot inject scripts into the generated page.
- The user does not need to register any account.
- This skill **never** sends user content to external APIs without explicit consent.

## Usage Example

```bash
# 1. Write or place your .md file
# 2. Generate a local HTML file (default: local images under .md dir are embedded)
python3 md2share.py my-notes.md

# 3. (Optional, only on explicit request) Build dist/ for deployment
./build_and_deploy.sh my-notes.md
```

## Files

- `md2share.py` — Core script (md → local html)
- `build_and_deploy.sh` — Optional local build helper (prepares `dist/`; off by default)
- `SKILL.md` — This file

## Limitations

- MD parser supports nested lists (any depth, mixed ordered/unordered) and images (local images embedded as base64 only from the Markdown file's directory or its subdirectories; absolute paths and `../` traversal are never embedded; image content is validated via magic bytes before embedding; every embedded path is logged to stderr; remote images rendered as a link placeholder so no network request is made)
- No screenshot/PNG output — this skill produces HTML only
- Footnotes: `[^id]` refs render as superscript anchors, definitions collected into a NOTES section at the bottom with back-links
- Table of contents: when the document has 3+ h2 headings, a collapsible TOC with anchor links is generated at the top (mobile-friendly, dark-mode aware)
- Horizontal rules (`---`, `***`, `___`) render as styled dividers
- Dark mode: follows `prefers-color-scheme` with a manual toggle that remembers the choice
- Code highlighter covers python / javascript / typescript / bash / sql / java / c / cpp / go / rust / php / ruby / kotlin / swift / json / yaml / css out of the box (with common aliases: py, js, ts, sh, golang, rs, yml, kt, rb, c++); other languages render as plain text with a label
- Highlighter is regex-based (single-pass tokenize: comment → string → keyword → number, no nesting bugs)
