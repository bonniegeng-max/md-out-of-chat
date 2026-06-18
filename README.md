# md-out-of-chat

> **Pulling Markdown out of chat, into something people can actually read.**
> **把 Markdown 从聊天里拿出来，变成人能直接看的东西。**

---

## 30-Second Pitch · 30 秒介绍

**中文**：在 IM 里（微信/飞书/Slack）跟 AI 聊，AI 给你写了一份 markdown，**但手机端根本看不了**。这个 skill 解决的就是这个 —— 把 .md 转成手机浏览器能直接打开的网页版：表格对齐、代码带语言标签 + 一键复制。告诉你的 AI "用 md-out-of-chat 装一下"，**它给你一个链接，微信里点开就能看**。本地跑，数据不外传。

**English**: Ever get a Markdown file in chat and not be able to read it on your phone? Code breaks, tables misalign, you can't copy a snippet. This skill turns any `.md` file into a mobile-friendly web page with proper tables, syntax-highlighted code blocks, and one-tap copy. Just say "show me this as md-out-of-chat" to your AI agent, and you get a link that opens in any phone browser. Local by default, no data uploaded.

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

- **A web URL** — opens in any mobile browser, with proper tables, code blocks with language labels and **one-tap copy**
- **Or a long screenshot** — if the user is abroad, or you just want to share as-is

- **一个 web 链接** — 任何手机浏览器都能打开，表格对齐、代码带语言标签 + **一键复制**
- **或一张长图截图** — 如果用户在国外，或者你想"原样分享"

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

Once installed, talk to your AI agent naturally:

> "把这份 md 装成我能看的"
> "show me this as md-out-of-chat"
> "用 md-out-of-chat 处理一下"
> "转一下，** 我在手机上看"

The agent decides the right output based on content and your situation:

| 场景 · Scenario | 输出 · Output |
|-----------------|---------------|
| 短，无代码/表格 · Short, no code/table | 截图 · Screenshot |
| 有代码/表格 · Has code/table | Web URL + 截图兜底 |
| "发给朋友" · Send to friend | 截图 · Screenshot |
| "海外/国外" · Send abroad | 截图 · Screenshot |
| 默认（国内用户）· Default (China) | Web URL + 截图 |

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
- **Default = web URL + screenshot together** — most other tools force you to pick one.
- **Copy button on every code block** — read the code on your phone, copy with one tap.
- **Multi-agent** — same SKILL.md works for Claude Code, Codex, OpenClaw, Copilot, etc.
- **Local by default** — no analytics, no cloud, no login.

---

## Files · 文件

- `SKILL.md` — English spec (the one the agent reads)
- `SKILL.zh.md` — 中文 spec (你读这个)
- `md2share.py` — the core script: md → mobile-friendly HTML
- `build_and_deploy.sh` — helper to build and prep for deployment
- `demo.md` — a tiny example to test with
- `LICENSE` — MIT
- `README.md` — 你现在看的这个

---

## Privacy · 隐私

- **Local by default** — script only produces a `.html` file. Nothing leaves your machine.
- **Web deploy is opt-in** — you can deploy to the assistant's built-in web server, or to Vercel/Netlify/GitHub Pages, or not at all.
- **No telemetry** — the script does not phone home.

- **默认本地跑** — 脚本只生成 `.html` 文件，**数据不出你电脑**
- **部署可选** — 你可以部署到 assistant 自带 web server，或 Vercel/Netlify/GitHub Pages，或完全不部署
- **无任何统计上报**

---

## Status · 状态

✅ Core features done:
- 标题 / 段落 / 表格 / 代码块（带语言标签 + 语法高亮）/ 列表 / 粗体 / 斜体
- 代码块一键复制按钮（3 状态：Copy → Copying... → Copied! → 2 秒回 Copy）
- 蓝白灰简约风格
- 移动端适配
- 中文字体（Noto CJK）
- **HTML → PNG 长图截图**（`./screenshot.sh`，可选）

🟡 Coming next:
- 引用 blockquote
- 有序列表 ol
- 链接样式化
- 任务列表 - [ ]

---

## Why "out of chat"? · 为什么叫 "out of chat"

Because that's exactly what it does. Markdown **lives well** in chat (AI writes it freely), but **dies** in chat rendering. This skill gets it out, into somewhere a human can actually read it.

因为这就是它做的事。Markdown **在聊天里写得很爽**（AI 信手拈来），但在聊天里**渲染得很惨**。这个 skill 把它拿出来，放到一个人能好好看的地方。

---

## License

MIT — see `LICENSE`.
