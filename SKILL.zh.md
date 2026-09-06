# md-out-of-chat

**把 Markdown 从聊天里拿出来，变成人能直接看的东西。**

AI 助手活在聊天里（微信、飞书、Slack、Discord……），最爱写 `.md`。但这些 app 都不好好渲染 `.md`：代码错位、表格对不齐、链接像死的。

这个小工具 = 桥：
- **`.md` → 手机能直接看的本地 HTML**
- 代码块带语言标签 + 一键复制
- 表格自适应（手机横屏不爆）
- 默认本地运行，公开链接必须用户明确请求

## 触发条件

只在用户明确提到 skill 名字，或清楚表达"把这份 md 转成手机可看的 HTML"时才激活。不要仅凭 "转一下" 这种模糊短语触发。

## 为什么用

- 你在 IM 跟 AI 聊，AI 给你写了一份 `.md`
- 你想看 = **手机打不开 / 看不清**
- = **用 md-out-of-chat 转换** → 生成手机可看的版本

## 怎么用

告诉你的 AI 助手："**用 md-out-of-chat 转换这份 md**" 或 "**把这份 md 转成手机能看的 HTML**"。

skill 默认输出本地 HTML；公开链接只在用户明确要求、明确确认且有部署工具时生成；本 skill 不生成截图/图片。

| 场景 | 输出 |
|------|------|
| 没有特别说明 | 本地 HTML |
| 明确说"截图/图片" | 解释：HTML 已生成，转 PNG 由宿主自带工具完成，不自动调其他工具 |
| 明确说"公开链接/URL"、确认部署且有部署工具 | web 链接 |

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
- `md2share.py` — 核心脚本：md → 本地 HTML
- `build_and_deploy.sh` — 本地构建辅助（只生成 dist/，不上传）
- `demo.md` — 测试用的小例子
- `README.md` — GitHub 首页展示用

## 隐私

- **默认本地跑** — 核心脚本只生成 `.html` 文件，**数据不出你电脑**
- 本 skill 不生成截图，也不内置任何浏览器自动化代码
- 公开链接**只在用户明确要求、明确确认、且 assistant 有可信部署工具时**才生成；`build_and_deploy.sh` 默认不跑
- 本地图片（`![alt](./image.png)`）只有和 `.md` 同目录或其子目录下的才会内嵌为 base64；**绝对路径和 `../` 遍历一律不内嵌**；内嵌前按文件头（magic bytes）校验真实类型，且每个内嵌路径都打到 stderr 供审计
- 远程图片不会自动下载，只会渲染成链接占位
- **无任何统计上报**

## License

MIT
