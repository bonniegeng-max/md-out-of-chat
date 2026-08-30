# md-out-of-chat

> **Pulling Markdown out of chat, into something people can actually read.**
> **把 Markdown 从聊天里拿出来，变成人能直接看的东西。**

---

## 30-Second Pitch · 30 秒介绍

**中文**：在 IM 里（微信/飞书/Slack）跟 AI 聊，AI 给你写了一份 markdown，**但手机端根本看不了**。这个 skill 解决的就是这个 —— 把 .md 转成手机浏览器能直接打开的本地网页版：表格对齐、代码带语言标签 + 一键复制。告诉你的 AI "用 md-out-of-chat 转换这份 md"，**它生成一个本地 HTML 文件，手机上点开就能看**。本地跑，数据不外传。

**English**: Ever get a Markdown file in chat and not be able to read it on your phone? Code breaks, tables misalign, you can't copy a snippet. This skill turns any `.md` file into a mobile-friendly web page with proper tables, syntax-highlighted code blocks, and one-tap copy. Just say "use md-out-of-chat to convert this" to your AI agent, and you get a local HTML file that opens in any phone browser. Local by default, no data uploaded.

---

## The Problem · 问题

You (or your AI agent) wrote something in Markdown. It's sitting in your chat — WeChat, Feishu, Slack, Discord, iMessage, Telegram — and **you can't actually read it on your phone**.

- Code blocks lose indentation and break lines
- Tables misalign into a single column
- Long text scrolls forever
- You can't copy a snippet without manual selection

你在 IM 里（微信、飞书、Slack、Discord……）跟 AI 写了一份 `.md`，**但手机端根本看不了**：
- 代码错位、缩进丢失
- 表格对不齐
- 长文本滚不动
- 想复制一段代码 = **得手选每一行**

---

## The Fix · 解决

Run the file through this skill. It produces:

把文件过一遍这个 skill，你得到：

- **A local HTML file** — opens in any mobile browser, with proper tables, code blocks with language labels and **one-tap copy**
- **Or a long screenshot** — when you explicitly ask for an image, or want to share as-is

- **一个本地 HTML 文件** — 任何手机浏览器都能打开，表格对齐、代码带语言标签 + **一键复制**
- **或一张长图截图** — 当你明确要图片，或想"原样分享"

A public web URL is only generated when you explicitly ask for it and your agent has a trusted deploy tool.

---

## What md2share Produces · 输出效果

Try it on a sample file: see `demo.md` for the input.

- **Live web demo**: [Click to view](https://2uf0a7axwwwr.space.minimaxi.com) (h1/h2 headings, code blocks with language labels, copy buttons, mobile-friendly tables)
- **Long screenshot**: see `demo.png` in this repo (a 750×2750 phone-shaped snapshot, Chinese + English fully rendered)

| Element | Input (Markdown) | Output (HTML + Screenshot) |
|---------|------------------|----------------------------|
| Heading | `# Title` | Blue title with bottom border |
| Table | `\| col \| col \|` | Zebra-striped, mobile-friendly |
| Code | ` ```python ` | Dark header with language label, syntax highlight, one-tap copy |
| Chinese | `你好，世界` | Renders correctly (Noto CJK fonts pre-installed) |

| Element | Input (Markdown) | Output (HTML) |
|---------|------------------|---------------|
| Heading | `# Title` | Blue title with bottom border |
| Table | `\| col \| col \|` | Zebra-striped, mobile-friendly |
| Code | ` ```python ` | Dark header with language label, one-tap copy button |
| List | `- item` | Bulleted with proper spacing |

---

## How to Use · 怎么用

Once installed, talk to your AI agent with an explicit skill mention:

> "用 md-out-of-chat 转换这份 md"
> "use md-out-of-chat to convert this markdown"
> "把这份 md 转成手机能看的 HTML"

The agent decides the right output based on your explicit request:

| 场景 · Scenario | 输出 · Output |
|-----------------|---------------|
| 没有特别说明 · No specific output requested | 本地 HTML · Local HTML file |
| "截图/图片" · "screenshot/image" | 截图 · Screenshot |
| "公开链接/URL" 且有部署工具 · "public link/URL" with deploy tool | Web URL |
| "发给朋友" · "send to friend" | 先问用户要截图还是链接 · Ask user: screenshot or link |

The default is always local-first. A public URL is never generated silently.

---

## Install · 安装

This is a standard skill. Drop the folder into your agent's skills directory:

标准 skill。把文件夹放到 agent 的 skills 目录：

| Agent | Path |
|-------|------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| GitHub Copilot | `.github/skills/` (per repo) |

```bash
cp -r md-out-of-chat ~/.claude/skills/
```

The agent picks it up automatically. No registration, no API key, no cloud account.

agent 自动识别。**不用注册、API key、云账号**。

---

## Who This Is For · 适合谁

- **You live in chat with your AI** — WeChat, Feishu, Slack, Discord, iMessage, Telegram
- **Your AI writes Markdown** — research summaries, code snippets, comparison tables, strategy docs
- **You read on your phone** — and Markdown doesn't render well there
- **You want copy-able code** — not screenshots of code

你跟 AI 在 IM 里聊、**AI 用 markdown 给你写东西**、**你在手机上看**、**想复制代码**。

Not for: pure desktop workflows, or if you never read on mobile.

不适合：纯桌面工作流，或者你从来不在手机上看。

---

## What Makes It Different · 跟别的区别

There are other "md to html" skills (`awesome-copilot/markdown-to-html`, `haidang1810/md2html`). md-out-of-chat is different because:

- **Built for IM** — not for "I want to publish a blog post". The output is sized for chat-shared links.
- **Local-first** — default output is a local HTML file; public URL only with explicit opt-in.
- **Copy button on every code block** — read the code on your phone, copy with one tap.
- **Multi-agent** — same SKILL.md works for Claude Code, Codex, OpenClaw, Copilot, etc.
- **No analytics, no cloud, no login**.

---

## Files · 文件

- `SKILL.md` — English spec (the one the agent reads)
- `SKILL.zh.md` — 中文 spec (你读这个)
- `md2share.py` — the core script: md → local mobile-friendly HTML
- `build_and_deploy.sh` — helper to build a local `dist/` folder
- `demo.md` — a tiny example to test with
- `LICENSE` — MIT
- `README.md` — 你现在看的这个

---

## Privacy · 隐私

- **Local by default** — `md2share.py` only produces a `.html` file. Nothing leaves your machine unless you explicitly ask for a public URL.
- **No browser automation shipped** — screenshots, if you need one, are rendered by your own browser/screenshot tool; the skill contains no Puppeteer/Chrome code.
- **Web deploy is opt-in** — only when you explicitly request it and your agent has a trusted deploy tool.
- **Sandboxed local images** — local images are embedded as base64 only when they live in the same directory as the `.md` file or a subdirectory of it. Absolute paths and `../` traversal are blocked unless you pass `--embed-local-images=all`.
- **Remote images never auto-fetch** — they render as a link placeholder, so no network request is made.
- **No telemetry** — the script does not phone home.

- **默认本地跑** — `md2share.py` 只生成 `.html` 文件，**数据不出你电脑**
- **不内置浏览器自动化** — 需要截图时用你自己的浏览器/截图工具渲染，skill 内不含 Puppeteer/Chrome 代码
- **公开链接需明确授权** — 只有在你明确要求、且有可信部署工具时才生成
- **本地图片沙箱** — 只有与 `.md` 同目录或其子目录下的图片才会内嵌为 base64；绝对路径和 `../` 会被拦截，除非显式加 `--embed-local-images=all`
- **远程图片不自动下载** — 只渲染为链接占位，不会发起网络请求
- **无任何统计上报**

---

## Status · 状态

✅ Core features done:
- 标题 / 段落 / 表格 / 代码块（带语言标签 + 语法高亮）/ 列表 / 粗体 / 斜体
- 引用 blockquote / 有序列表 / 任务列表 `- [ ]` / 链接样式化
- 表格 cell 内联格式（粗体/斜体/行内代码/链接）+ `\|` 转义
- 代码块一键复制按钮（3 状态：Copy → Copying... → Copied! → 2 秒回 Copy）
- 语法高亮重写为单遍 tokenize（注释→字符串→关键字→数字），修复了字符串内关键字误高亮和 span 嵌套错乱
- 默认本地 HTML 输出，公开链接需用户明确授权
- 蓝白灰简约风格
- 移动端适配
- 中文字体（Noto CJK）
- 嵌套列表（任意层级，有序/无序混排）
- 图片支持：本地图片内嵌 base64（离线可看），默认沙箱到 .md 同目录及子目录，绝对路径和 `../` 被拦截；远程图片渲染为链接占位（不自动发请求，保护隐私）
- 正文自带 `# 标题` 时不再叠加文件名标题
- 截图输出由宿主环境自带工具完成（v1.3.2 起不再内置 screenshot.sh，避免浏览器自动化代码）
- 脚注 `[^id]`：正文渲染为上标角标，可点击跳转，底部 NOTES 区汇总并支持回跳（论文/技术文档友好）
- 分隔线 `---` / `***` / `___` 渲染为渐变样式分隔线
- 暗色模式：跟随系统 `prefers-color-scheme`，右上角可手动切换并记住选择

🟡 Coming next:
- Mermaid 图表渲染

---

## Why "out of chat"? · 为什么叫 "out of chat"

Because that's exactly what it does. Markdown **lives well** in chat (AI writes it freely), but **dies** in chat rendering. This skill gets it out, into somewhere a human can actually read it.

因为这就是它做的事。Markdown **在聊天里写得很爽**（AI 信手拈来），但在聊天里**渲染得很惨**。这个 skill 把它拿出来，放到一个人能好好看的地方。

---

## License

MIT — see `LICENSE`.
