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

Risk: The optional `build_and_deploy.sh` and `screenshot.sh` helpers invoke local tools (Python, Puppeteer, Chrome) to generate artifacts.

Mitigation: These scripts are opt-in; the user must explicitly run them. `screenshot.sh` only renders locally generated HTML files and does not fetch external URLs.

Risk: The optional `auto_push.sh` helper pushes the repository to GitHub.

Mitigation: The script requires the user to set `GITHUB_TOKEN` explicitly; it will not run without it and only pushes to the configured user's own repository.

Risk: Markdown links are rendered as `<a>` tags.

Mitigation: The renderer only allows `http:`, `https:`, and `mailto:` URL schemes; `javascript:` and other unsafe schemes are left as plain text to reduce XSS risk.

## Reference(s):

- [GitHub Repository](https://github.com/bonniegeng-max/md-out-of-chat)
- [ClawHub Skill Page](https://clawhub.ai/bonniegeng-max/skills/md-out-of-chat)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Shell commands, Local files]

**Output Format:** [Mobile-friendly HTML page or phone-sized PNG screenshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a single `.html` file in a `dist/` folder, a `.png` long screenshot, and shell commands to build or deploy them.]

## Skill Version(s):

1.1.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review generated HTML/screenshots before sharing, and apply their organization's safety, security, and compliance requirements before deployment.
