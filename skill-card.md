## Description:

md-out-of-chat takes Markdown files produced by AI agents in chat (WeChat, Feishu, Slack, Discord, etc.) and turns them into a mobile-friendly web page or a phone-sized long screenshot. It fixes code-block layout breakage, table misalignment, and unreadable long text on mobile, adding syntax highlighting, language labels, and one-tap copy buttons for code blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT

## Use Case:

Users who receive Markdown content from AI agents inside instant-message apps and need to read or share it on mobile devices. Typical content includes research summaries, comparison tables, code snippets, strategy docs, and how-to guides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes HTML files and PNG screenshots to the user's local filesystem (`dist/`, or the path specified by the output argument).

Mitigation: All writes are local and explicit — the user supplies the input path and the skill produces an output file. No data is uploaded to remote services by the core script.

Risk: The optional `build_and_deploy.sh` helper invokes Python to prepare a local `dist/` folder.

Mitigation: This script is opt-in and only writes files locally. It does not upload anything.

Risk: The optional `screenshot.sh` helper uses Puppeteer + Chrome to render a local PNG from a local HTML file.

Mitigation: This script is opt-in. It blocks all external network requests during rendering and only processes locally generated HTML files.

Risk: Markdown links are rendered as `<a>` tags.

Mitigation: The renderer only allows `http:`, `https:`, and `mailto:` URL schemes; `javascript:` and other unsafe schemes are left as plain text to reduce XSS risk.

Risk: Local images (`![alt](./image.png)`) are read from the filesystem and embedded as base64.

Mitigation: By default, only image files located in the same directory as the input Markdown file or a subdirectory of it are embedded. Absolute paths and parent-directory traversal (`../`) are blocked unless the user explicitly passes `--embed-local-images=all`. Remote images are never fetched automatically and are rendered as a link placeholder.

## Reference(s):

- [GitHub Repository](https://github.com/bonniegeng-max/md-out-of-chat)
- [ClawHub Skill Page](https://clawhub.ai/bonniegeng-max/skills/md-out-of-chat)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Shell commands, Local files]

**Output Format:** [Mobile-friendly HTML page or phone-sized PNG screenshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single local `.html` file, an optional local `.png` screenshot, and shell commands to build them. A public URL is only produced when the user explicitly requests it and the host agent has a trusted deploy tool.]

## Skill Version(s):

1.3.1 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review generated HTML/screenshots before sharing, and apply their organization's safety, security, and compliance requirements before deployment.
