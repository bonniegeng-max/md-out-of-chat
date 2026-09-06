"""
md2view - MD 转 HTML
输入：.md 文件路径
输出：.html 文件（蓝白灰简约风格 + 表格对齐 + 代码高亮）
"""
import sys
import re
import html
import base64
import os
from pathlib import Path

IMG_MIME = {
    '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
    '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml',
    '.bmp': 'image/bmp',
}

# 本地图片内嵌策略：'auto' 只允许 .md 同目录及子目录；'all' 显式放开限制
EMBED_LOCAL_IMAGES = 'auto'

def split_row(line):
    """按未转义的 | 切分表格行，支持 \\| 转义"""
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    cells = re.split(r'(?<!\\)\|', line)
    return [c.strip().replace('\\|', '|') for c in cells]

def parse_md(md_text):
    """简单 MD 解析器：标题/段落/表格/代码块/列表/引用块"""
    lines = md_text.split('\n')
    blocks = []
    footnotes = []
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

        # 分隔线
        if re.match(r'^\s*(?:-{3,}|\*{3,}|_{3,})\s*$', line):
            blocks.append({'type': 'hr'})
            i += 1
            continue

        # 脚注定义 [^id]: text
        m = re.match(r'^\s*\[\^(\w+)\]:\s*(.+)$', line)
        if m:
            footnotes.append({'id': m.group(1), 'text': m.group(2).strip()})
            i += 1
            continue

        # 引用块
        if re.match(r'^\s*>', line):
            quote_lines = []
            while i < len(lines) and re.match(r'^\s*>', lines[i]):
                quote_lines.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            blocks.append({'type': 'quote', 'content': ' '.join(quote_lines).strip()})
            continue

        # 表格（必须前后有空行）
        if '|' in line and i + 1 < len(lines) and re.match(r'^\|?\s*[-:|\s]+\|?$', lines[i+1]):
            header = split_row(line)
            i += 2  # 跳过分隔行
            rows = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip():
                rows.append(split_row(lines[i]))
                i += 1
            blocks.append({'type': 'table', 'header': header, 'rows': rows})
            continue

        # 列表（无序/有序/任务/嵌套，统一解析）
        if re.match(r'^\s*(?:[-*]|\d+\.)\s+', line):
            items = []
            list_re = re.compile(r'^(\s*)([-*]|\d+\.)\s+(.*)$')
            while i < len(lines) and lines[i].strip():
                m = list_re.match(lines[i])
                if not m:
                    break
                indent = len(m.group(1).replace('\t', '    '))
                ordered = not m.group(2).startswith(('-', '*'))
                text = m.group(3).strip()
                task = None
                if not ordered:
                    tm = re.match(r'^\[( |x|X)\]\s+(.*)$', text)
                    if tm:
                        task = 'done' if tm.group(1).lower() == 'x' else 'todo'
                        text = tm.group(2)
                items.append({'indent': indent, 'ordered': ordered, 'text': text, 'task': task})
                i += 1
            blocks.append({'type': 'list', 'items': items})
            continue

        # 空行
        if not line.strip():
            i += 1
            continue

        # 普通段落（合并连续行）
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r'^(#{1,6}\s|```|\||\s*[-*]\s|\s*\d+\.\s|\s*>)', lines[i]):
            para.append(lines[i])
            i += 1
        blocks.append({'type': 'p', 'content': ' '.join(para).strip()})

    return blocks, footnotes

LANG_ALIASES = {
    'py': 'python', 'js': 'javascript', 'ts': 'typescript',
    'sh': 'bash', 'shell': 'bash', 'zsh': 'bash',
    'c++': 'cpp', 'cc': 'cpp', 'cxx': 'cpp',
    'golang': 'go', 'rs': 'rust', 'yml': 'yaml', 'kt': 'kotlin', 'rb': 'ruby',
}

def highlight_code(code, lang):
    """单遍 tokenize 高亮：注释 → 字符串 → 关键字 → 数字，互不嵌套错乱"""
    lang_l = LANG_ALIASES.get((lang or '').lower(), (lang or '').lower())

    keywords_map = {
        'python': ['def', 'class', 'import', 'from', 'return', 'if', 'else', 'elif', 'for', 'while', 'in', 'is', 'not', 'and', 'or', 'try', 'except', 'finally', 'with', 'as', 'lambda', 'pass', 'break', 'continue', 'yield', 'async', 'await', 'True', 'False', 'None', 'self'],
        'javascript': ['function', 'const', 'let', 'var', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'class', 'extends', 'new', 'this', 'super', 'import', 'export', 'from', 'async', 'await', 'try', 'catch', 'finally', 'throw', 'typeof', 'instanceof', 'true', 'false', 'null', 'undefined'],
        'typescript': ['function', 'const', 'let', 'var', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'class', 'extends', 'implements', 'interface', 'type', 'enum', 'namespace', 'readonly', 'public', 'private', 'protected', 'new', 'this', 'super', 'import', 'export', 'from', 'async', 'await', 'try', 'catch', 'finally', 'throw', 'typeof', 'instanceof', 'keyof', 'true', 'false', 'null', 'undefined'],
        'bash': ['if', 'then', 'fi', 'else', 'elif', 'for', 'while', 'do', 'done', 'case', 'esac', 'function', 'return', 'echo', 'export', 'local'],
        'sql': ['SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'ON', 'GROUP', 'BY', 'ORDER', 'HAVING', 'LIMIT', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE', 'DROP', 'ALTER', 'AS', 'AND', 'OR', 'NOT', 'NULL', 'IS'],
        'java': ['public', 'private', 'protected', 'class', 'interface', 'extends', 'implements', 'static', 'final', 'void', 'new', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'try', 'catch', 'finally', 'throw', 'throws', 'import', 'package', 'boolean', 'int', 'long', 'double', 'float', 'char', 'byte', 'short', 'null', 'true', 'false', 'this', 'super', 'abstract', 'synchronized', 'instanceof', 'enum'],
        'c': ['int', 'char', 'float', 'double', 'void', 'long', 'short', 'unsigned', 'signed', 'struct', 'union', 'enum', 'typedef', 'static', 'const', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'sizeof', 'goto', 'extern', 'register', 'volatile', 'NULL'],
        'cpp': ['int', 'char', 'float', 'double', 'void', 'long', 'short', 'unsigned', 'signed', 'struct', 'union', 'enum', 'typedef', 'static', 'const', 'return', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'sizeof', 'class', 'public', 'private', 'protected', 'virtual', 'namespace', 'using', 'template', 'typename', 'new', 'delete', 'this', 'bool', 'true', 'false', 'nullptr', 'override', 'try', 'catch', 'throw'],
        'go': ['package', 'import', 'func', 'var', 'const', 'type', 'struct', 'interface', 'map', 'chan', 'go', 'defer', 'if', 'else', 'for', 'range', 'switch', 'case', 'default', 'return', 'break', 'continue', 'nil', 'true', 'false', 'string', 'int', 'int64', 'float64', 'bool', 'byte', 'rune', 'error', 'select', 'fallthrough'],
        'rust': ['fn', 'let', 'mut', 'const', 'static', 'struct', 'enum', 'impl', 'trait', 'use', 'pub', 'mod', 'match', 'if', 'else', 'loop', 'while', 'for', 'in', 'return', 'break', 'continue', 'self', 'Self', 'Some', 'None', 'Ok', 'Err', 'where', 'as', 'dyn', 'async', 'await', 'unsafe', 'move', 'ref', 'true', 'false'],
        'php': ['function', 'class', 'public', 'private', 'protected', 'static', 'echo', 'print', 'return', 'if', 'else', 'elseif', 'foreach', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'new', 'extends', 'implements', 'interface', 'trait', 'namespace', 'use', 'const', 'true', 'false', 'null', 'try', 'catch', 'finally', 'throw', 'instanceof', 'global', 'array'],
        'ruby': ['def', 'end', 'class', 'module', 'if', 'elsif', 'else', 'unless', 'while', 'until', 'for', 'do', 'then', 'require', 'require_relative', 'attr_accessor', 'attr_reader', 'attr_writer', 'nil', 'true', 'false', 'self', 'puts', 'print', 'lambda', 'proc', 'yield', 'rescue', 'ensure', 'begin', 'return', 'break', 'continue', 'case', 'when', 'raise', 'new'],
        'kotlin': ['fun', 'val', 'var', 'class', 'object', 'interface', 'data', 'sealed', 'when', 'if', 'else', 'for', 'while', 'return', 'break', 'continue', 'null', 'true', 'false', 'is', 'in', 'as', 'companion', 'override', 'open', 'abstract', 'lateinit', 'init', 'suspend', 'import', 'package', 'private', 'public', 'internal', 'protected', 'this', 'super'],
        'swift': ['func', 'let', 'var', 'class', 'struct', 'enum', 'protocol', 'extension', 'if', 'else', 'guard', 'for', 'while', 'repeat', 'switch', 'case', 'default', 'return', 'break', 'continue', 'in', 'nil', 'true', 'false', 'self', 'Self', 'init', 'deinit', 'import', 'as', 'is', 'throws', 'rethrows', 'try', 'catch', 'async', 'await', 'some', 'any', 'where', 'static', 'public', 'private', 'internal', 'override', 'final'],
        'json': ['true', 'false', 'null'],
        'yaml': ['true', 'false', 'null', 'yes', 'no', 'on', 'off'],
        'css': ['important', 'media', 'supports', 'keyframes', 'import', 'font-face', 'root'],
    }

    comment_pat = {
        'python': r'#[^\n]*',
        'bash': r'#[^\n]*',
        'yaml': r'#[^\n]*',
        'ruby': r'#[^\n]*',
        'javascript': r'//[^\n]*|/\*[\s\S]*?\*/',
        'typescript': r'//[^\n]*|/\*[\s\S]*?\*/',
        'java': r'//[^\n]*|/\*[\s\S]*?\*/',
        'c': r'//[^\n]*|/\*[\s\S]*?\*/',
        'cpp': r'//[^\n]*|/\*[\s\S]*?\*/',
        'go': r'//[^\n]*|/\*[\s\S]*?\*/',
        'rust': r'//[^\n]*|/\*[\s\S]*?\*/',
        'php': r'//[^\n]*|#[^\n]*|/\*[\s\S]*?\*/',
        'sql': r'--[^\n]*',
        'css': r'/\*[\s\S]*?\*/',
    }.get(lang_l)

    keywords = keywords_map.get(lang_l, [])

    alts = []
    if comment_pat:
        alts.append(f'(?P<cmt>{comment_pat})')
    alts.append(r"(?P<str>\"[^\"\n]*\"|'[^'\n]*'|`[^`\n]*`)")
    if keywords:
        kw_alt = '|'.join(re.escape(k) for k in sorted(keywords, key=len, reverse=True))
        alts.append(rf'(?P<kw>\b(?:{kw_alt})\b)')
    alts.append(r'(?P<num>\b\d+\.?\d*\b)')

    pattern = re.compile('|'.join(alts))

    out = []
    pos = 0
    for m in pattern.finditer(code):
        out.append(html.escape(code[pos:m.start()]))
        if m.group('cmt') is not None:
            cls = 'cmt'
        elif m.group('str') is not None:
            cls = 'str'
        elif m.group('kw') is not None:
            cls = 'kw'
        else:
            cls = 'num'
        out.append(f'<span class="{cls}">{html.escape(m.group(0))}</span>')
        pos = m.end()
    out.append(html.escape(code[pos:]))

    return ''.join(out)

def check_image_magic(path):
    """校验文件头部 magic bytes 是否与声明扩展名匹配，防止伪装成图片的文件被内嵌"""
    ext = path.suffix.lower()
    try:
        with open(path, 'rb') as f:
            head = f.read(16)
    except OSError:
        return False
    if ext == '.png':
        return head.startswith(b'\x89PNG\r\n\x1a\n')
    if ext in ('.jpg', '.jpeg'):
        return head.startswith(b'\xff\xd8')
    if ext == '.gif':
        return head.startswith(b'GIF87a') or head.startswith(b'GIF89a')
    if ext == '.webp':
        return head[:4] == b'RIFF' and head[8:12] == b'WEBP'
    if ext == '.bmp':
        return head.startswith(b'BM')
    if ext == '.svg':
        return b'<' in head[:64]
    return True


def resolve_image_path(url, base_dir):
    """解析图片路径；返回 (absolute_path, allowed)。

    - 远程图片：返回 (None, False)
    - 本地图片：resolve 后只允许 .md 同目录及子目录（沙箱内），
      绝对路径和目录遍历一律拒绝
    - 不存在或格式不支持：返回 (resolved_path, False)
    """
    if re.match(r'^(https?:)', url, re.I):
        return None, False
    if not base_dir:
        return None, False
    try:
        p = Path(url)
        base_resolved = base_dir.resolve()
        if p.is_absolute():
            # 绝对路径永不内嵌：防止把任意位置的本地文件打包进输出 HTML
            return p.resolve(), False
        resolved = (base_resolved / p).resolve()
        return resolved, resolved.is_relative_to(base_resolved)
    except (OSError, ValueError):
        pass
    return None, False


def render_inline(text, base_dir=None):
    """内联处理：**bold** *italic* `code` [link](url) ![img](path) [^fn]"""
    text = html.escape(text)

    # 脚注引用 [^id] → 上标角标
    text = re.sub(r'\[\^(\w+)\]',
                  lambda m: f'<sup class="fn-ref" id="fnref-{m.group(1)}"><a href="#fn-{m.group(1)}">{m.group(1)}</a></sup>',
                  text)

    # 图片 ![alt](url) —— 本地图片内嵌 base64（离线可看），远程图片渲染为链接占位（不自动发请求）
    def img_repl(m):
        alt, url = m.group(1), m.group(2)
        resolved, allowed = resolve_image_path(url, base_dir)
        if resolved is None:
            label = alt or url
            return (f'<span class="img-ext">🖼 <a href="{url}" target="_blank" '
                    f'rel="noopener">{label}</a></span>')
        if allowed and resolved.exists() and resolved.suffix.lower() in IMG_MIME \
                and check_image_magic(resolved):
            data = base64.b64encode(resolved.read_bytes()).decode()
            # 透明度：把每个实际内嵌的本地文件路径打到 stderr
            print(f"[md2share] embedded local image: {resolved}", file=sys.stderr)
            return (f'<img class="md-img" src="data:{IMG_MIME[resolved.suffix.lower()]};'
                    f'base64,{data}" alt="{alt}">')
        # 不可访问或越界的本地图片保持原样，避免静默吞掉
        return m.group(0)
    text = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)\)', img_repl, text)

    # 链接 [text](url) —— 只放行安全协议
    def link_repl(m):
        label, url = m.group(1), m.group(2)
        if re.match(r'^(https?:|mailto:)', url, re.I):
            return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'
        return m.group(0)
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link_repl, text)

    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code class="inline">\1</code>', text)
    return text

def build_list_tree(items):
    """把缩进的扁平列表项组成树"""
    def parse(idx, indent):
        nodes = []
        while idx < len(items) and items[idx]['indent'] >= indent:
            it = items[idx]
            if it['indent'] == indent:
                idx += 1
                children = []
                if idx < len(items) and items[idx]['indent'] > indent:
                    children, idx = parse(idx, items[idx]['indent'])
                nodes.append({**it, 'children': children})
            else:
                # 比当前层级更深且没有同层节点兜着，挂到上一个节点下
                sub, idx = parse(idx, items[idx]['indent'])
                if nodes:
                    nodes[-1]['children'].extend(sub)
                else:
                    nodes.extend(sub)
        return nodes, idx
    if not items:
        return []
    tree, _ = parse(0, items[0]['indent'])
    return tree

def render_list(nodes, base_dir=None):
    """递归渲染嵌套列表"""
    if not nodes:
        return ''
    tag = 'ol' if nodes[0]['ordered'] else 'ul'
    parts = [f'<{tag}>']
    for n in nodes:
        if n.get('task'):
            cls = 'task-done' if n['task'] == 'done' else 'task-todo'
            box = '☑' if n['task'] == 'done' else '☐'
            parts.append(f'<li class="{cls}"><span class="cbx">{box}</span> {render_inline(n["text"], base_dir)}')
        else:
            parts.append(f'<li>{render_inline(n["text"], base_dir)}')
        if n['children']:
            parts.append(render_list(n['children'], base_dir))
        parts.append('</li>')
    parts.append(f'</{tag}>')
    return ''.join(parts)

def render_html(blocks, title="md2view", base_dir=None, footnotes=None):
    """渲染 blocks 为 HTML；title 为 None 时不注入文件名标题（正文已有 h1）

    h2/h3 数量 >= 3 时自动生成可折叠目录（锚点跳转，暗色适配）。
    """
    # 给 h2/h3 分配锚点 id，并构建 TOC
    toc_entries = []
    sec_n = 0
    for b in blocks:
        if b['type'] == 'h' and b['level'] in (2, 3):
            sec_n += 1
            b['_id'] = f'sec-{sec_n}'
            toc_entries.append((b['level'], b['_id'], b['content']))

    parts = []
    if title is not None:
        parts.append(f'<h1 class="title">{html.escape(title)}</h1>')

    # 目录：h2 >= 3 个才生成（短文档不需要跳转）
    h2_count = sum(1 for lvl, _, _ in toc_entries if lvl == 2)
    if h2_count >= 3:
        parts.append('<details class="toc"><summary>目录 · Contents</summary><nav>')
        for lvl, sec_id, content in toc_entries:
            cls = 'toc-h3' if lvl == 3 else 'toc-h2'
            parts.append(
                f'<a class="{cls}" href="#{sec_id}">{html.escape(content)}</a>'
            )
        parts.append('</nav></details>')

    for b in blocks:
        if b['type'] == 'h':
            lvl = b['level']
            tag = f'h{lvl}'
            sec_id = b.get('_id')
            id_attr = f' id="{sec_id}"' if sec_id else ''
            parts.append(f'<{tag} class="{tag}"{id_attr}>{render_inline(b["content"], base_dir)}</{tag}>')
        elif b['type'] == 'p':
            parts.append(f'<p>{render_inline(b["content"], base_dir)}</p>')
        elif b['type'] == 'quote':
            parts.append(f'<blockquote>{render_inline(b["content"], base_dir)}</blockquote>')
        elif b['type'] == 'hr':
            parts.append('<hr class="md-hr">')
        elif b['type'] == 'list':
            parts.append(render_list(build_list_tree(b['items']), base_dir))
        elif b['type'] == 'code':
            code_html = highlight_code(b['content'], b['lang'])
            lang_label = b['lang'].upper() if b['lang'] else 'TEXT'
            parts.append(
                f'<div class="code-block">'
                f'<div class="code-header">'
                f'<span class="code-lang">{lang_label}</span>'
                f'<button class="copy-btn">Copy</button>'
                f'</div>'
                f'<pre><code>{code_html}</code></pre>'
                f'</div>'
            )
        elif b['type'] == 'table':
            parts.append('<div class="table-wrap"><table>')
            parts.append('<thead><tr>')
            for h in b['header']:
                parts.append(f'<th>{render_inline(h, base_dir)}</th>')
            parts.append('</tr></thead>')
            parts.append('<tbody>')
            for ri, row in enumerate(b['rows']):
                cls = 'odd' if ri % 2 else 'even'
                parts.append(f'<tr class="{cls}">')
                for c in row:
                    parts.append(f'<td>{render_inline(c, base_dir)}</td>')
                parts.append('</tr>')
            parts.append('</tbody></table></div>')

    if footnotes:
        parts.append('<section class="footnotes">')
        parts.append('<div class="fn-title">NOTES · 注释</div>')
        for fn in footnotes:
            parts.append(
                f'<div class="fn-item" id="fn-{fn["id"]}">'
                f'<span class="fn-num">[{fn["id"]}]</span> {render_inline(fn["text"], base_dir)}'
                f'<a class="fn-back" href="#fnref-{fn["id"]}"> ↩</a></div>'
            )
        parts.append('</section>')

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
a {
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid rgba(59, 125, 216, 0.35);
  word-break: break-all;
}
blockquote {
  margin: 16px 0;
  padding: 10px 16px;
  border-left: 4px solid var(--accent);
  background: #EEF2F7;
  color: var(--text-light);
  border-radius: 0 6px 6px 0;
}
ul, ol {
  margin: 12px 0 12px 24px;
}
ul ul, ul ol, ol ul, ol ol { margin: 6px 0 6px 20px; }
li { margin: 6px 0; }
.md-img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 8px 0;
  border: 1px solid var(--border);
}
.img-ext {
  display: inline-block;
  background: #EEF2F7;
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 14px;
}
li.task-done, li.task-todo { list-style: none; margin-left: -20px; }
li.task-done { color: var(--text-light); text-decoration: line-through; }
li.task-done .cbx { text-decoration: none; }
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
.md-hr {
  border: none;
  height: 2px;
  background: linear-gradient(to right, transparent, var(--border) 15%, var(--accent) 50%, var(--border) 85%, transparent);
  margin: 28px 0;
}
/* ---- TOC 目录 ---- */
details.toc {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  margin: 20px 0;
  overflow: hidden;
}
details.toc summary {
  cursor: pointer;
  padding: 12px 18px;
  font-size: 13px;
  font-weight: 600;
  color: var(--primary);
  letter-spacing: 1px;
  user-select: none;
  list-style: none;
}
details.toc summary::-webkit-details-marker { display: none; }
details.toc summary::before { content: '▸ '; }
details.toc[open] summary::before { content: '▾ '; }
details.toc nav {
  display: flex;
  flex-direction: column;
  padding: 4px 18px 14px;
}
details.toc a {
  color: var(--text);
  text-decoration: none;
  font-size: 14px;
  line-height: 1.5;
  padding: 5px 0;
  border-bottom: 1px dashed var(--border);
}
details.toc a:last-child { border-bottom: none; }
details.toc a.toc-h3 {
  padding-left: 18px;
  font-size: 13px;
  color: var(--text-light);
}
h2[id], h3[id] { scroll-margin-top: 12px; }
.footnotes {
  margin-top: 32px;
  padding-top: 16px;
  border-top: 1px dashed var(--border);
}
.fn-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-light);
  letter-spacing: 2px;
  margin-bottom: 8px;
}
.fn-item {
  font-size: 13px;
  color: var(--text-light);
  margin: 6px 0;
  line-height: 1.6;
}
.fn-num { color: var(--accent); font-weight: 600; }
sup.fn-ref { font-size: 12px; }
sup.fn-ref a { border: none; text-decoration: none; font-weight: 600; }
.fn-back { border: none; }
.theme-toggle {
  position: fixed;
  top: 16px;
  right: 16px;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--text);
  font-size: 16px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  z-index: 99;
}
/* 暗色模式：跟随系统 + 可手动切换 */
@media (prefers-color-scheme: dark) {
  body:not(.light) {
    --primary: #8AB6E8; --accent: #5C9BE0;
    --bg: #14181D; --card: #1E242B;
    --text: #D8DEE6; --text-light: #97A2AE; --border: #39434E;
  }
  body:not(.light) .code-block { background: #161B21; }
  body:not(.light) blockquote,
  body:not(.light) code.inline,
  body:not(.light) .img-ext { background: #232B34; }
  body:not(.light) tr.odd { background: #23282F; }
  body:not(.light) tr.even { background: #1E242B; }
  body:not(.light) tr:hover { background: #2A323C; }
}
body.dark {
  --primary: #8AB6E8; --accent: #5C9BE0;
  --bg: #14181D; --card: #1E242B;
  --text: #D8DEE6; --text-light: #97A2AE; --border: #39434E;
}
body.dark .code-block { background: #161B21; }
body.dark blockquote,
body.dark code.inline,
body.dark .img-ext { background: #232B34; }
body.dark tr.odd { background: #23282F; }
body.dark tr.even { background: #1E242B; }
body.dark tr:hover { background: #2A323C; }
@media (max-width: 480px) {
  body { padding: 12px; }
  .container { padding: 20px 16px; }
  .title { font-size: 22px; }
  th, td { padding: 8px 10px; font-size: 13px; }
}
"""
    js = """
// 主题切换（跟随系统 + 手动覆盖，记忆选择）
(function () {
  const saved = (() => { try { return localStorage.getItem('md2view-theme'); } catch (e) { return null; } })();
  if (saved === 'dark') document.body.classList.add('dark');
  else if (saved === 'light') document.body.classList.add('light');
  const toggle = document.createElement('button');
  toggle.className = 'theme-toggle';
  const updateIcon = () => { toggle.textContent = document.body.classList.contains('dark') ? '☀️' : '🌙'; };
  toggle.addEventListener('click', () => {
    if (document.body.classList.contains('dark')) {
      document.body.classList.remove('dark'); document.body.classList.add('light');
    } else {
      document.body.classList.remove('light'); document.body.classList.add('dark');
    }
    try { localStorage.setItem('md2view-theme', document.body.classList.contains('dark') ? 'dark' : 'light'); } catch (e) {}
    updateIcon();
  });
  updateIcon();
  document.body.appendChild(toggle);
})();
document.querySelectorAll('.copy-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const pre = btn.closest('.code-block') && btn.closest('.code-block').querySelector('pre');
    const code = pre ? pre.textContent : '';
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

def parse_cli(argv):
    """解析命令行参数。格式: md2share.py <md> [output] [--embed-local-images=auto]

    --embed-local-images=all 已弃用（v1.5.0 起内嵌始终沙箱在 .md 目录内）；
    传入 all 时按 auto 处理并打印弃用提示，保证旧调用不报错。
    """
    global EMBED_LOCAL_IMAGES
    positional = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--embed-local-images' or a.startswith('--embed-local-images='):
            if '=' in a:
                val = a.split('=', 1)[1]
            elif i + 1 < len(argv):
                i += 1
                val = argv[i]
            else:
                print("用法: python md2share.py <md文件> [输出html] [--embed-local-images=auto]")
                sys.exit(1)
            if val not in ('auto', 'all'):
                print("用法: python md2share.py <md文件> [输出html] [--embed-local-images=auto]")
                sys.exit(1)
            if val == 'all':
                print("[md2share] --embed-local-images=all 已弃用（v1.5.0）："
                      "图片内嵌始终限制在 .md 文件所在目录及子目录", file=sys.stderr)
                val = 'auto'
            EMBED_LOCAL_IMAGES = val
        elif a.startswith('-'):
            print(f"未知选项: {a}")
            print("用法: python md2share.py <md文件> [输出html] [--embed-local-images=auto]")
            sys.exit(1)
        else:
            positional.append(a)
        i += 1
    return positional


def main():
    positional = parse_cli(sys.argv[1:])
    if len(positional) < 1:
        print("用法: python md2share.py <md文件> [输出html] [--embed-local-images=auto]")
        sys.exit(1)

    md_path = Path(positional[0])
    if not md_path.exists():
        print(f"找不到: {md_path}")
        sys.exit(1)

    output_path = Path(positional[1]) if len(positional) > 1 else md_path.with_suffix('.html')

    md_text = md_path.read_text(encoding='utf-8')
    blocks, footnotes = parse_md(md_text)
    # 正文自带 h1 时不再注入文件名标题，避免双标题
    has_h1 = any(b['type'] == 'h' and b['level'] == 1 for b in blocks)
    title = None if has_h1 else md_path.stem
    content = render_html(blocks, title=title, base_dir=md_path.parent,
                          footnotes=footnotes)
    html_doc = build_page(content, title=md_path.stem)

    output_path.write_text(html_doc, encoding='utf-8')
    print(f"✅ 已生成: {output_path}")

if __name__ == '__main__':
    main()
