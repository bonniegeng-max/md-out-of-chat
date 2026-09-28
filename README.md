# md-out-of-chat

> **One-line positioning**: a local-first Markdown converter that turns one `.md` file into a phone-friendly HTML page people can actually open, read, and forward — no upload, no API key, no external service required.

> **Turn Markdown reports and AI chat exports into phone-friendly HTML pages.**
> **把 Markdown 报告和 AI 聊天导出，变成手机上真正能看的网页。**

---

## What it does

This skill turns a Markdown file into a phone-friendly single-page HTML that is actually readable in mobile browsers.

It is designed for one practical gap: AI assistants generate lots of `.md`, but WeChat, Feishu, Slack, Discord, and similar chat tools do a poor job rendering it on phones. Code blocks become unreadable, tables overflow, and long links feel broken. `md-out-of-chat` fixes that last mile.

## Why it is useful

- Read AI-generated reports on your phone
- Forward a chat export as a clean web page
- Share a technical note without asking the receiver to open raw Markdown
- Keep the default workflow local and private

## What makes it different

- **Local-first:** default output is a local `.html` file
- **No API key:** ready to use without account setup
- **Phone-first:** optimized for mobile reading, not desktop-only preview
- **Explicit deploy boundary:** public URL output only happens after a separate request and confirmation

## Demo first

If someone only sees one proof asset, it should be this:

- `demo.md` = example input
- `demo.png` = phone-readable output proof
- default result = a local `.html` file for mobile reading

The storefront should treat `demo.png` as conversion evidence, not just as an optional screenshot. The message is simple: **Markdown that was painful in chat becomes readable on mobile.**

## Best use cases

- weekly reports
- AI chat export reading
- technical handoff notes
- mobile review of Markdown documents
- shareable HTML pages generated from Markdown without default cloud upload

## The problem

You (or your AI agent) wrote something in Markdown. It is sitting in your chat — WeChat, Feishu, Slack, Discord, iMessage, Telegram — and **you cannot actually read it well on your phone**.

- Code blocks lose indentation and break lines
- Tables misalign into a single column
- Long text becomes painful to scan
- You cannot copy a snippet cleanly without manual selection

## The fix

Run the file through this skill. It produces:

- **A local HTML file** that opens in any mobile browser
- Proper tables and code blocks with language labels
- Copy-friendly output instead of raw Markdown friction

A public web URL is only generated when you explicitly ask for it and the agent has a trusted deploy tool.

## What md2share produces

Try it on a sample file: see `demo.md` for the input.

- **Long screenshot proof**: `demo.png`
- **Example input**: `demo.md`
- **Default result**: a local `.html` file for phone reading

| Element | Input (Markdown) | Output (HTML) |
|---------|------------------|---------------|
| Heading | `# Title` | Blue title with bottom border |
| Table | `| col | col |` | Zebra-striped, mobile-friendly |
| Code | <code>```python</code> | Dark header with language label, one-tap copy button |
| List | `- item` | Proper spacing and readable mobile layout |

> **Syntax highlighting, honestly stated**: `md2share.py` includes built-in highlighting support for 17 languages — `python`, `javascript`, `typescript`, `bash`, `sql`, `java`, `c`, `cpp`, `go`, `rust`, `php`, `ruby`, `kotlin`, `swift`, `json`, `yaml`, and `css` — plus common aliases such as `py`, `js`, `ts`, `sh`, `golang`, `rs`, `yml`, `kt`, `rb`, and `c++`. Unlisted languages still render cleanly with a language label and copy button, but without full highlighting.

## How to use

Once installed, talk to your AI agent with an explicit skill mention **and a concrete file**:

> "用 md-out-of-chat 把 `notes.md` 转成 HTML"
> "use md-out-of-chat to convert `report.md`"
> "把 `demo.md` 转成手机能看的 HTML"

### Trigger contract

- This skill only runs when the user names it explicitly **and** identifies a concrete `.md` file.
- The agent must **not** infer conversion targets from chat history or vague phrases like "转一下" / "convert this".
- Only the file(s) the user explicitly identifies are read.
- A public URL is **never** generated unless the user separately requests deployment **and** confirms it.

The default is always local-first.


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
- **No browser automation shipped** — the skill generates HTML only and contains no Puppeteer/Chrome code; no PNG output.
- **Web deploy is opt-in** — only when you explicitly request it, explicitly confirm, and your agent has a trusted deploy tool.
- **Sandboxed local images** — local images are embedded as base64 only when they live in the same directory as the `.md` file or a subdirectory of it. **Absolute paths and `../` traversal are never embedded.** Image content is validated via magic bytes before embedding, and every embedded file path is logged to stderr for auditing.
- **Remote images never auto-fetch** — they render as a link placeholder, so no network request is made.
- **No telemetry** — the script does not phone home.

- **默认本地跑** — `md2share.py` 只生成 `.html` 文件，**数据不出你电脑**
- **不内置浏览器自动化** — skill 只生成 HTML，不含 Puppeteer/Chrome 代码，不输出 PNG
- **公开链接需明确授权** — 只有在你明确要求、明确确认、且有可信部署工具时才生成
- **本地图片沙箱** — 只有与 `.md` 同目录或其子目录下的图片才会内嵌为 base64；**绝对路径和 `../` 遍历一律不内嵌**；内嵌前按文件头校验真实类型，每个内嵌路径都打到 stderr 供审计
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
- 图片支持：本地图片内嵌 base64（离线可看），沙箱到 .md 同目录及子目录，绝对路径和 `../` 一律不内嵌，内嵌前校验文件头类型并打印内嵌路径；远程图片渲染为链接占位（不自动发请求，保护隐私）
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
