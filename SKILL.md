---
name: md-out-of-chat
description: 把 AI 在聊天里写出的 Markdown 转成手机能直接看的网页或长图。解决微信/飞书/Slack 里 .md 打不开、代码错位、表格对不齐的问题。输出带语法高亮、语言标签和一键复制按钮的移动端 HTML，或手机尺寸长截图。本地运行，数据不出本机。当用户说"把这个 md 转成能看的""我在手机上看""转一下发给朋友"时使用。
version: 1.1.0
homepage: https://github.com/bonniegeng-max/md-out-of-chat
license: MIT
---

# md-out-of-chat

**Pulling Markdown out of chat, into something people can actually read.**

AI agents live in chat (WeChat, Feishu, Slack, Discord, …) and love to write `.md`. But `.md` doesn't render well in any of those apps. Code breaks, tables misalign, links look dead. This skill is the bridge: it takes a `.md` file and turns it into a mobile-friendly, copyable, shareable view.

## The Problem

- `.md` files **cannot be opened in WeChat** on mobile
- Code blocks **break layout** on small screens
- Tables **misalign columns** on mobile
- When you're away from your computer, you **can't view** what your assistant just made

## Input

- Path to a `.md` file
- Type: `web` (deploy to public URL) or `screenshot` (render to PNG)

## Output

- `web` → Public URL, opens in any mobile browser
- `screenshot` → One or more PNG images at phone screen size

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

## Output Type Decision (Cost × Effect × Audience)

The right output depends on **who you're sharing with** and **what they need to do** with the content.

### Default: Always Generate Web URL

When the user says "show me this" without specifying output type, the assistant should **default to web URL**. This is the safest choice because:
- It works for both personal reading and sharing
- It supports copy / quote / highlight
- The user can ask for a screenshot afterward if they need one

### When to Switch to Screenshot (Without Asking)

The assistant may switch to a screenshot **only** when:
- The content is very short (< 100 chars) AND has no code or table
- The user explicitly says "screenshot" / "image" / "图片" / "截个图"
- The user says "send to a friend" / "发给朋友" (signals they care about share-ability)

### Never Ask "Is This For You or For Someone Else?"

This question is annoying because the user often hasn't thought it through. The assistant should:
- **Make a sensible default** (web URL)
- **Tell the user** what it chose and why, in one line
- **Offer the alternative** without forcing a choice

**Good response:**
> "我帮你生成了 web 链接：https://....  （如果你想要截图也可以告诉我）"

**Bad response:**
> "你想自己看还是给别人看？要不要截图？"

### When In Doubt: Generate Both, But Tell the User

If the content is borderline (e.g. 200 chars with one small table), the assistant can:
- Generate the web URL
- Also screenshot the first screen
- Tell the user "两个都给你了"

### The "国内用户 + 兜底" Pattern

For the most common case (a user in China, default assumption), the safest output is:
1. **Web URL** as the primary (rich, copy-able, fast in China)
2. **A screenshot of the first screen** as backup (works even when network is flaky)

This costs the assistant almost nothing extra (both are generated locally) and removes a whole class of "your link didn't load" complaints.

### When the User Is Likely Overseas

If the user mentions anything that suggests they are outside China (海外 / abroad / 给国外朋友看), the assistant should:
- **Prefer screenshot over link** — because links in China-platforms are slow abroad, and links on Vercel/Netlify are slow in China; a screenshot has zero network dependency once delivered
- Optionally also generate a Vercel/Netlify link as a secondary option
- Tell the user "我给你截图了，** 想看完整版可点这个链接"

## Mobile Responsive

- Body padding shrinks on `< 480px` width
- Container padding: 32px → 20px
- Code font shrinks: 14px → 13px
- Table font shrinks: 14px → 13px

## Privacy

- Runs **locally**, no data uploaded to any cloud
- `web` deployment uses the assistant's built-in server with a **temporary URL**
- The user does not need to register any account
- This skill **never** sends user content to external APIs without explicit consent

## Usage Example

```bash
# 1. Write or place your .md file
# 2. Run the build script
./build_and_deploy.sh my-notes.md my-view

# 3. Deploy via your platform's deploy tool
#    dist_dir = ./dist
# 4. Get the URL and open on phone
```

## Files

- `md2share.py` — Core script (md → html)
- `build_and_deploy.sh` — Build + deploy helper
- `SKILL.md` — This file

## Limitations

- Simple MD parser (no nested lists, no footnotes, no images yet)
- Code highlighter covers python / javascript / bash / sql out of the box; other languages render as plain text with a label
- Highlighter is regex-based (single-pass tokenize: comment → string → keyword → number, no nesting bugs)
