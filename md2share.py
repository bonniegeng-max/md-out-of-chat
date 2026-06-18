"""
md2view - MD 转 HTML
输入：.md 文件路径
输出：.html 文件（蓝白灰简约风格 + 表格对齐 + 代码高亮）
"""
import sys
import re
import html
from pathlib import Path

def parse_md(md_text):
    """简单 MD 解析器：标题/段落/表格/代码块/列表"""
    lines = md_text.split('\n')
    blocks = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 代码块
        if line.strip().startswith('```'):
            lang = line.strip()[3:].strip() or 'text'
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            blocks.append({'type': 'code', 'lang': lang, 'content': '\n'.join(code_lines)})
            i += 1
            continue
        
        # 标题
        m = re.match(r'^(#{1,6})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            blocks.append({'type': 'h', 'level': level, 'content': m.group(2).strip()})
            i += 1
            continue
        
        # 表格（必须前后有空行）
        if '|' in line and i + 1 < len(lines) and re.match(r'^\|?\s*[-:|\s]+\|?$', lines[i+1]):
            header = [c.strip() for c in line.strip('|').split('|')]
            i += 2  # 跳过分隔行
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip('|').split('|')])
                i += 1
            blocks.append({'type': 'table', 'header': header, 'rows': rows})
            continue
        
        # 列表
        if re.match(r'^\s*[-*]\s+', line):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*]\s+', lines[i]):
                items.append(re.sub(r'^\s*[-*]\s+', '', lines[i]))
                i += 1
            blocks.append({'type': 'ul', 'items': items})
            continue
        
        # 空行
        if not line.strip():
            i += 1
            continue
        
        # 普通段落（合并连续行）
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,6}\s|```|\||\s*[-*]\s)', lines[i]):
            para.append(lines[i])
            i += 1
        blocks.append({'type': 'p', 'content': ' '.join(para).strip()})
    
    return blocks

def highlight_code(code, lang):
    """简单代码高亮（关键字 + 字符串 + 注释）"""
    # HTML 转义
    code = html.escape(code)
    
    keywords_map = {
        'python': ['def', 'class', 'import', 'from', 'return', 'if', 'else', 'elif', 'for', 'while', 'in', 'is', 'not', 'and', 'or', 'try', 'except', 'finally', 'with', 'as', 'lambda', 'pass', 'break', 'continue', 'yield', 'async', 'await', 'True', 'False', 'None', 'self'],
        'javascript': ['function', 'const', 'let', 'var', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'class', 'extends', 'new', 'this', 'super', 'import', 'export', 'from', 'async', 'await', 'try', 'catch', 'finally', 'throw', 'typeof', 'instanceof', 'true', 'false', 'null', 'undefined'],
        'bash': ['if', 'then', 'fi', 'else', 'elif', 'for', 'while', 'do', 'done', 'case', 'esac', 'function', 'return', 'echo', 'export', 'local'],
        'sql': ['SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'ON', 'GROUP', 'BY', 'ORDER', 'HAVING', 'LIMIT', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE', 'DROP', 'ALTER', 'AS', 'AND', 'OR', 'NOT', 'NULL', 'IS'],
    }
    
    keywords = keywords_map.get(lang.lower(), [])

    # 把所有 HTML 转义（避免被字符串正则误伤）
    code = code.replace('&', '\x00AMP\x00').replace('<', '\x00LT\x00').replace('>', '\x00GT\x00')

    # 高亮关键字（用 \x01N\x01 包裹）
    for kw in sorted(keywords, key=len, reverse=True):
        code = re.sub(r'\b' + re.escape(kw) + r'\b', '\x01K\x01' + kw + '\x01E\x01', code)

    # 高亮字符串
    code = re.sub(r'("[^"\n]*"|\'[^\'\n]*\')', '\x01S\x01\1\x01E\x01', code)

    # 高亮数字
    code = re.sub(r'\b(\d+\.?\d*)\b', '\x01N\x01\1\x01E\x01', code)

    # 高亮注释
    if lang.lower() in ('python', 'bash', 'javascript'):
        code = re.sub(r'(#[^\n]*)', '\x01C\x01\1\x01E\x01', code)
    if lang.lower() in ('sql'):
        code = re.sub(r'(--[^\n]*)', '\x01C\x01\1\x01E\x01', code)

    # 把占位符换回 HTML
    repl = {
        '\x00AMP\x00': '&amp;',
        '\x00LT\x00': '&lt;',
        '\x00GT\x00': '&gt;',
        '\x01K\x01': '<span class="kw">',
        '\x01S\x01': '<span class="str">',
        '\x01N\x01': '<span class="num">',
        '\x01C\x01': '<span class="cmt">',
        '\x01E\x01': '</span>',
    }
    for k, v in repl.items():
        code = code.replace(k, v)

    return code

def render_html(blocks, title="md2view"):
    """渲染 blocks 为 HTML"""
    parts = []
    parts.append(f'<h1 class="title">{html.escape(title)}</h1>')
    
    for b in blocks:
        if b['type'] == 'h':
            lvl = b['level']
            tag = f'h{lvl}'
            parts.append(f'<{tag} class="{tag}">{html.escape(b["content"])}</{tag}>')
        elif b['type'] == 'p':
            # 内联处理：**bold** *italic* `code`
            text = html.escape(b['content'])
            text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
            text = re.sub(r'`([^`]+)`', r'<code class="inline">\1</code>', text)
            parts.append(f'<p>{text}</p>')
        elif b['type'] == 'ul':
            parts.append('<ul>')
            for item in b['items']:
                text = html.escape(item)
                text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
                parts.append(f'<li>{text}</li>')
            parts.append('</ul>')
        elif b['type'] == 'code':
            code_html = highlight_code(b['content'], b['lang'])
            lang_label = b['lang'].upper() if b['lang'] else 'TEXT'
            block_id = f'code-{len(parts)}'
            # 原始代码（用于复制）= 去 HTML 标签
            raw_code = b['content']
            import html as _html
            raw_escaped = _html.escape(raw_code).replace("'", "&#39;")
            parts.append(
                f'<div class="code-block" data-code-id="{block_id}">'
                f'<div class="code-header">'
                f'<span class="code-lang">{lang_label}</span>'
                f'<button class="copy-btn" data-code="{raw_escaped}">Copy</button>'
                f'</div>'
                f'<pre><code>{code_html}</code></pre>'
                f'</div>'
            )
        elif b['type'] == 'table':
            parts.append('<div class="table-wrap"><table>')
            parts.append('<thead><tr>')
            for h in b['header']:
                parts.append(f'<th>{html.escape(h)}</th>')
            parts.append('</tr></thead>')
            parts.append('<tbody>')
            for ri, row in enumerate(b['rows']):
                cls = 'odd' if ri % 2 else 'even'
                parts.append(f'<tr class="{cls}">')
                for c in row:
                    parts.append(f'<td>{html.escape(c)}</td>')
                parts.append('</tr>')
            parts.append('</tbody></table></div>')
    
    return '\n'.join(parts)

def build_page(content_html, title="md2view"):
    """完整 HTML 页面（蓝白灰风格）"""
    css = """
:root {
  --primary: #1F4E79;
  --accent: #3B7DD8;
  --bg: #F5F7FA;
  --card: #FFFFFF;
  --text: #333333;
  --text-light: #666666;
  --border: #E1E5EB;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  padding: 20px;
  -webkit-text-size-adjust: 100%;
}
.container {
  max-width: 720px;
  margin: 0 auto;
  background: var(--card);
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(31, 78, 121, 0.08);
  padding: 32px 24px;
}
.title {
  color: var(--primary);
  font-size: 28px;
  font-weight: 700;
  border-bottom: 2px solid var(--primary);
  padding-bottom: 12px;
  margin-bottom: 24px;
}
h1, h2, h3, h4, h5, h6 {
  color: var(--primary);
  margin: 24px 0 12px;
  font-weight: 600;
}
h1 { font-size: 24px; }
h2 { font-size: 20px; }
h3 { font-size: 18px; }
p {
  margin: 12px 0;
  font-size: 16px;
}
strong { color: var(--primary); font-weight: 600; }
em { color: var(--accent); }
ul {
  margin: 12px 0 12px 24px;
}
li { margin: 6px 0; }
code.inline {
  background: #EEF2F7;
  color: var(--primary);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 14px;
}
.code-block {
  margin: 16px 0;
  background: #F8FAFC;
  border-left: 3px solid var(--primary);
  border-radius: 6px;
  overflow: hidden;
}
.code-block {
  position: relative;
}
.code-header {
  background: var(--primary);
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
}
.code-lang {
  padding: 0 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
}
.copy-btn {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 3px 10px;
  font-size: 12px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 8px;
  font-family: inherit;
  transition: all 0.2s;
}
.copy-btn:hover { background: rgba(255, 255, 255, 0.25); }
.copy-btn.copying { background: #3B7DD8; border-color: #3B7DD8; }
.copy-btn.copied { background: #27AE60; border-color: #27AE60; }
.copy-btn.copied::after { content: ' ✓'; }
.code-block pre {
  padding: 16px;
  overflow-x: auto;
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 14px;
  line-height: 1.6;
}
.code-block code .kw { color: #C0392B; font-weight: 600; }
.code-block code .str { color: #27AE60; }
.code-block code .num { color: #2980B9; }
.code-block code .cmt { color: #7F8C8D; font-style: italic; }
.table-wrap {
  margin: 16px 0;
  overflow-x: auto;
  border-radius: 6px;
  border: 1px solid var(--border);
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
th {
  background: var(--primary);
  color: #fff;
  padding: 10px 12px;
  text-align: left;
  font-weight: 600;
  white-space: nowrap;
}
td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
}
tr.odd { background: #FAFBFC; }
tr.even { background: #FFFFFF; }
tr:hover { background: #EEF2F7; }
@media (max-width: 480px) {
  body { padding: 12px; }
  .container { padding: 20px 16px; }
  .title { font-size: 22px; }
  th, td { padding: 8px 10px; font-size: 13px; }
}
"""
    js = """
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const code = btn.dataset.code
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/&lt;span[^&]*&gt;/g, '')
      .replace(/&lt;\\/span&gt;/g, '');
    btn.classList.add('copying');
    btn.textContent = 'Copying...';
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(code);
      } else {
        const ta = document.createElement('textarea');
        ta.value = code;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      }
      btn.classList.remove('copying');
      btn.classList.add('copied');
      btn.textContent = 'Copied!';
      setTimeout(() => {
        btn.classList.remove('copied');
        btn.textContent = 'Copy';
      }, 2000);
    } catch (e) {
      btn.classList.remove('copying');
      btn.textContent = 'Failed';
      setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
    }
  });
});
"""
    title_esc = html.escape(title)
    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"zh-CN\">\n"
        "<head>\n"
        "<meta charset=\"UTF-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "<title>" + title_esc + "</title>\n"
        "<style>" + css + "</style>\n"
        "</head>\n"
        "<body>\n"
        "<div class=\"container\">\n"
        + content_html + "\n"
        "</div>\n"
        "<script>" + js + "</script>\n"
        "</body>\n"
        "</html>\n"
    )

def main():
    if len(sys.argv) < 2:
        print("用法: python md2html.py <md文件> [输出html]")
        sys.exit(1)
    
    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"找不到: {md_path}")
        sys.exit(1)
    
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else md_path.with_suffix('.html')
    
    md_text = md_path.read_text(encoding='utf-8')
    blocks = parse_md(md_text)
    content = render_html(blocks, title=md_path.stem)
    html_doc = build_page(content, title=md_path.stem)
    
    output_path.write_text(html_doc, encoding='utf-8')
    print(f"✅ 已生成: {output_path}")

if __name__ == '__main__':
    main()
