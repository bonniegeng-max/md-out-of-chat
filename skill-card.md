## Description:

md-out-of-chat turns Markdown reports, AI chat exports, and technical notes into a phone-friendly local web page that people can actually open, read, and forward on mobile. It is built for WeChat / Feishu / Slack / Discord style workflows where raw `.md` is painful to read on phones.

Core value:
- Local-first, no upload by default
- No API key required
- Easy to open in any mobile browser
- Public URL only after an explicit request and confirmation

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT

## Use Case:

Users who receive Markdown content from AI agents inside instant-message apps and need to read, review, or forward it on mobile devices. Typical content includes reports, research summaries, comparison tables, code snippets, strategy docs, technical handoff notes, and chat exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes HTML files to the user's local filesystem.

Mitigation: All writes are local and explicit — the user supplies the input path and the skill produces an output file. No data is uploaded by default.

Risk: The optional `build_and_deploy.sh` helper prepares a local `dist/` folder and may be used in a deploy workflow.

Mitigation: This path is opt-in and should only be used after the user explicitly asks for a deployable or public result.

Risk: Markdown links are rendered as `<a>` tags.

Mitigation: Only safe URL schemes should be rendered as clickable links; unsafe schemes should remain plain text.

Risk: Local images may be embedded into the output page.

Mitigation: Embedding should remain limited to images in the Markdown file's directory or subdirectories, while absolute paths and parent-directory traversal stay blocked.

## Reference(s):

- [GitHub Repository](https://github.com/bonniegeng-max/md-out-of-chat)
- [ClawHub Skill Page](https://clawhub.ai/bonniegeng-max/skills/md-out-of-chat)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Shell commands, Local files]

**Output Format:** [Mobile-friendly HTML page only; this skill does not generate PNG screenshots or images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local `.html` file by default. A public URL is only produced when the user explicitly requests it, explicitly confirms, and the host agent has a trusted deploy tool.]

## Skill Version(s):

1.5.3

## Ethical Considerations:

Users should review generated HTML before sharing it publicly and apply their own security, privacy, and compliance requirements before deployment or forwarding.
