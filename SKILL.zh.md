# md-out-of-chat

**把 Markdown 从聊天里拿出来，变成人能直接看的东西。**

AI 助手活在聊天里（微信、飞书、Slack、Discord……），最爱写 `.md`。但这些 app 都不好好渲染 `.md`：代码错位、表格对不齐、链接像死的。

这个小工具 = 桥：
- **`.md` → 手机能直接看的 HTML**
- 代码块带语言标签 + 一键复制
- 表格自适应（手机横屏不爆）
- 部署后**任何手机浏览器都能打开**

## 为什么用

- 你在 IM 跟 AI 聊，AI 给你写了一份 `.md`
- 你想看 = **手机打不开 / 看不清**
- = **用这个** → 生成手机可看的版本

## 怎么用

告诉你的 AI 助手："**把这个 md 装成我能看的**" 或 "**用 md-out-of-chat 处理一下**"。

skill 会自动决定输出方式：

| 场景 | 输出 |
|------|------|
| 内容短（< 100 字，无代码/表格） | 截图 |
| 内容长，有代码/表格 | web 链接 + 截图（兜底） |
| 明确说"发给朋友" | 截图（陌生人不敢点链接） |
| 明确说"海外/国外朋友" | 截图（链接在两边都不稳） |

## 安装

这是标准 skill，**把文件夹放到 agent 的 skills 目录**就行：

| Agent | Skills 目录 |
|-------|------------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| OpenClaw | `~/.openclaw/skills/` |
| 其他 | 任意 agent 监听的 skills/ 目录 |

```
cp -r md-out-of-chat ~/.claude/skills/
```

agent 会自动识别。

## 文件说明

- `SKILL.md` — 英文 spec（agent 读这个）
- `SKILL.zh.md` — 中文 spec（你读这个）
- `md2share.py` — 核心脚本：md → 手机友好的 HTML
- `build_and_deploy.sh` — 部署辅助脚本
- `demo.md` — 测试用的小例子
- `README.md` — 你现在看的这个（GitHub 首页展示用）

## 隐私

- **默认本地跑** — 脚本只生成 `.html` 文件，**数据不出你电脑**
- **部署可选** — 你可以部署到 assistant 自带 web server，或 Vercel/Netlify/GitHub Pages，或完全不部署
- **无任何统计上报**

## License

MIT
