#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan Markdown under this repo and emit a single self-contained study.html
(left nav + search + random topic). Re-run after editing .md files.
"""
from __future__ import annotations

import hashlib
import re
import sys
from collections import defaultdict
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "study.html"

SKIP_NAMES = {"GITHUB_推送说明.md"}

META = ROOT / "study_html_meta.txt"


def load_branding() -> tuple[str, str, str]:
    """(document <title>, sidebar h1, tagline). Optional study_html_meta.txt: up to 3 non-empty lines."""
    h1 = "面经题库"
    tag = "侧栏目录 · 全文搜索 · 随机一篇"
    doc_title = "面经 · 学习页"
    if META.is_file():
        parts = [ln.strip() for ln in META.read_text(encoding="utf-8").splitlines() if ln.strip()][:3]
        if parts:
            h1 = parts[0]
        if len(parts) >= 2:
            tag = parts[1]
        if len(parts) >= 3:
            doc_title = parts[2]
        else:
            doc_title = f"{h1} · 学习页"
    else:
        readme = ROOT / "README.md"
        if readme.is_file():
            for line in readme.read_text(encoding="utf-8").splitlines():
                if line.startswith("# "):
                    h1 = line[2:].strip()
                    break
        doc_title = f"{h1} · 学习页"
    return doc_title, h1, tag


def try_import_markdown():
    try:
        import markdown  # noqa: F401

        return True
    except ImportError:
        return False


def collect_md_files() -> list[Path]:
    files: list[Path] = []
    for p in ROOT.rglob("*.md"):
        if ".git" in p.parts:
            continue
        if p.name in SKIP_NAMES:
            continue
        files.append(p)
    return files


def rel_posix(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def doc_anchor(rel: str) -> str:
    """Stable HTML id fragment (ASCII) from relative path."""
    h = hashlib.sha256(rel.encode("utf-8")).hexdigest()[:20]
    return f"doc-{h}"


def file_sort_key(rel: str) -> tuple:
    """Numeric-aware order within a folder (e.g. 86 before 100)."""
    stem = Path(rel).stem
    m = re.match(r"^(\d+)-", stem)
    n = int(m.group(1)) if m else 0
    return (n, stem)


def module_key(rel: str) -> tuple:
    """Sort: README & 漫游指南 first, then 01-.. 13-.., 真题, other."""
    if rel == "README.md":
        return (0, 0, rel)
    if rel.endswith("题漫游指南.md"):
        return (1, 0, rel)
    parts = rel.split("/")
    if len(parts) == 1:
        return (4, 0, rel)
    folder = parts[0]
    m = re.match(r"^(\d{2})-", folder)
    if m:
        return (2, int(m.group(1)), file_sort_key(rel))
    if folder == "真题":
        return (2, 99, file_sort_key(rel))
    return (2, 50, file_sort_key(rel))


def resolve_md_href(source_rel: str, href: str) -> str | None:
    href = href.split("#", 1)[0].strip()
    if not href.endswith(".md"):
        return None
    base = ROOT / Path(source_rel).parent
    target = (base / href).resolve()
    try:
        target_rel = target.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return None
    return target_rel


def rewrite_md_links(md: str, source_rel: str, path_to_anchor: dict[str, str]) -> str:
    def repl(m: re.Match) -> str:
        text, url = m.group(1), m.group(2)
        if "://" in url or url.startswith("#"):
            return m.group(0)
        tr = resolve_md_href(source_rel, url)
        if tr and tr in path_to_anchor:
            frag = path_to_anchor[tr]
            return f"[{text}](#{frag})"
        return m.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, md)


def strip_yaml_front_matter(text: str) -> str:
    if not text.startswith("---"):
        return text
    lines = text.splitlines()
    if len(lines) < 2:
        return text
    for i in range(1, min(len(lines), 200)):
        if lines[i].strip() == "---":
            return "\n".join(lines[i + 1 :])
    return text


def html_escape_attr(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def protect_math_tokens(md_text: str) -> str:
    r"""
    Insert raw HTML for math before Markdown runs, so \_, ^, etc. are not parsed as Markdown.
    Display $$...$$ becomes a block <div> (valid block-level HTML for CommonMark).
    Inline $...$ becomes <span> (valid inside runs).
    """
    def repl_display(m: re.Match) -> str:
        esc = html_escape_attr(m.group(1).strip())
        return f'\n\n<div class="math-render math-display" data-latex="{esc}"></div>\n\n'

    md_text = re.sub(r"\$\$([\s\S]*?)\$\$", repl_display, md_text)

    def repl_inline(m: re.Match) -> str:
        esc = html_escape_attr(m.group(1).strip())
        return f'<span class="math-render math-inline" data-latex="{esc}"></span>'

    md_text = re.sub(r"(?<!\$)\$(?!\$)((?:[^$\\]|\\.)+?)\$(?!\$)", repl_inline, md_text)
    return md_text


def fix_display_math_paragraphs(html: str) -> str:
    """Python-Markdown may wrap block <div> in <p>; unwrap display formulas."""
    return re.sub(
        r'<p>\s*<div class="math-render math-display"([^>]*)></div>\s*</p>',
        r'<div class="math-render math-display"\1></div>',
        html,
    )


def md_to_html(md_text: str) -> str:
    import markdown

    return markdown.markdown(
        md_text,
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            "markdown.extensions.nl2br",
            "markdown.extensions.sane_lists",
        ],
    )


def sidebar_title(rel: str) -> str:
    name = Path(rel).stem
    return name


def main() -> int:
    if not try_import_markdown():
        print("Installing markdown...", file=sys.stderr)
        import subprocess

        subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown", "-q"])

    import markdown  # noqa: F401

    files = collect_md_files()
    rels = sorted({rel_posix(p) for p in files}, key=module_key)
    path_to_anchor = {r: doc_anchor(r) for r in rels}

    by_folder: dict[str, list[str]] = defaultdict(list)
    for r in rels:
        folder = str(Path(r).parent) if "/" in r or "\\" in r else "(根目录)"
        if folder == ".":
            folder = "(根目录)"
        by_folder[folder].append(r)

    articles_html: list[str] = []
    nav_items: list[str] = []

    for folder in sorted(by_folder.keys(), key=lambda x: (x == "(根目录)", x)):
        rels_in = sorted(by_folder[folder], key=module_key)
        sub: list[str] = []
        for r in rels_in:
            aid = path_to_anchor[r]
            title = escape(sidebar_title(r))
            sub.append(f'<li><a class="nav-link" href="#{aid}" data-title="{title}">{title}</a></li>')
        nav_items.append(
            f'<details class="mod" open><summary class="mod-sum">{escape(folder)}</summary><ul>{"".join(sub)}</ul></details>'
        )

    for r in rels:
        p = ROOT / r
        raw = p.read_text(encoding="utf-8")
        raw = strip_yaml_front_matter(raw)
        raw = rewrite_md_links(raw, r, path_to_anchor)
        raw = protect_math_tokens(raw)
        body = fix_display_math_paragraphs(md_to_html(raw))
        aid = path_to_anchor[r]
        label = escape(r)
        articles_html.append(
            f'<article class="paper" id="{aid}" data-path="{escape(r)}">'
            f'<header class="paper-hd"><span class="path">{label}</span></header>'
            f'<div class="paper-bd md">{body}</div></article>'
        )

    articles_joined = "\n".join(articles_html)
    nav_joined = "\n".join(nav_items)

    doc_title, h1_txt, tag_txt = load_branding()

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(doc_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400..700;1,400..700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin>
<style>
:root {{
  --font-ui: "Plus Jakarta Sans", "PingFang SC", "Microsoft YaHei", sans-serif;
  --font-body: "Source Serif 4", "Noto Serif SC", "Songti SC", "Georgia", serif;
  --bg0: #08090d;
  --bg1: #12151f;
  --panel: rgba(22, 26, 38, 0.92);
  --panel-border: rgba(120, 200, 255, 0.12);
  --text: #eef2f8;
  --muted: #8b95a8;
  --accent: #3ee0c9;
  --accent2: #a78bfa;
  --border: rgba(255, 255, 255, 0.08);
  --card: rgba(255, 255, 255, 0.035);
  --card-hover: rgba(255, 255, 255, 0.05);
  --code-bg: rgba(0, 0, 0, 0.35);
  --shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
  --radius: 18px;
  --radius-sm: 10px;
  --math-color: #e8ecf4;
}}
html.light {{
  --bg0: #f3f1ec;
  --bg1: #faf8f4;
  --panel: rgba(255, 255, 255, 0.95);
  --panel-border: rgba(15, 118, 110, 0.15);
  --text: #1c1917;
  --muted: #57534e;
  --accent: #0d9488;
  --accent2: #6d28d9;
  --border: rgba(28, 25, 23, 0.08);
  --card: #ffffff;
  --card-hover: #fafaf9;
  --code-bg: #f0ebe3;
  --shadow: 0 12px 40px rgba(28, 25, 23, 0.08);
  --math-color: #1c1917;
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  font-family: var(--font-ui);
  background: var(--bg0);
  background-image:
    radial-gradient(ellipse 120% 80% at 100% 0%, rgba(62, 224, 201, 0.12), transparent 50%),
    radial-gradient(ellipse 80% 60% at 0% 100%, rgba(167, 139, 250, 0.1), transparent 45%),
    linear-gradient(180deg, var(--bg1) 0%, var(--bg0) 100%);
  color: var(--text);
  line-height: 1.5;
  height: 100vh;
  overflow: hidden;
}}
html.light body {{
  background-image:
    radial-gradient(ellipse 100% 70% at 100% 0%, rgba(13, 148, 136, 0.08), transparent 50%),
    linear-gradient(180deg, #fffefb 0%, var(--bg0) 100%);
}}
.layout {{
  display: grid;
  grid-template-columns: minmax(260px, 300px) 1fr;
  height: 100vh;
  gap: 0;
}}
aside {{
  background: var(--panel);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-right: 1px solid var(--panel-border);
  display: flex;
  flex-direction: column;
  min-height: 0;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.2);
}}
.aside-hd {{
  padding: 1.25rem 1.1rem 1rem;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(135deg, rgba(62, 224, 201, 0.08) 0%, transparent 60%);
}}
.aside-hd h1 {{
  margin: 0 0 0.35rem;
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  background: linear-gradient(90deg, var(--text), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
html.light .aside-hd h1 {{
  background: linear-gradient(90deg, #134e4a, #0f766e);
  -webkit-background-clip: text;
  background-clip: text;
}}
.aside-hd .tagline {{
  font-size: 0.72rem;
  color: var(--muted);
  font-weight: 500;
  margin-bottom: 0.75rem;
}}
.tools {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}}
.tools input {{
  flex: 1 1 120px;
  min-width: 0;
  padding: 0.55rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--card);
  color: var(--text);
  font-size: 0.8125rem;
  font-family: var(--font-ui);
  transition: border-color 0.2s, box-shadow 0.2s;
}}
.tools input:focus {{
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(62, 224, 201, 0.2);
}}
html.light .tools input:focus {{
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.2);
}}
button {{
  cursor: pointer;
  border: 1px solid var(--border);
  background: var(--card);
  color: var(--text);
  border-radius: var(--radius-sm);
  padding: 0.55rem 0.85rem;
  font-size: 0.8125rem;
  font-family: var(--font-ui);
  font-weight: 600;
  transition: transform 0.15s, border-color 0.2s, background 0.2s;
}}
button:hover {{
  border-color: var(--accent);
  color: var(--accent);
  background: var(--card-hover);
}}
button:active {{ transform: scale(0.97); }}
.nav-scroll {{
  flex: 1;
  overflow: auto;
  padding: 0.75rem 0.65rem 2rem;
}}
.nav-scroll::-webkit-scrollbar {{ width: 6px; }}
.nav-scroll::-webkit-scrollbar-thumb {{
  background: var(--border);
  border-radius: 99px;
}}
.mod {{
  margin-bottom: 0.35rem;
  border-radius: var(--radius-sm);
  overflow: hidden;
}}
.mod-sum {{
  cursor: pointer;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--accent);
  padding: 0.5rem 0.4rem;
  user-select: none;
  list-style: none;
}}
.mod-sum::-webkit-details-marker {{ display: none; }}
.mod ul {{
  list-style: none;
  margin: 0.15rem 0 0.5rem 0.35rem;
  padding: 0;
}}
.nav-link {{
  display: block;
  padding: 0.4rem 0.5rem;
  border-radius: 8px;
  color: var(--muted);
  text-decoration: none;
  font-size: 0.8125rem;
  font-weight: 500;
  transition: color 0.15s, background 0.15s;
}}
.nav-link:hover {{
  background: var(--card-hover);
  color: var(--text);
}}
.nav-link.hidden {{ display: none; }}
main {{
  overflow: auto;
  min-height: 0;
  padding: 1.75rem 1.5rem 4rem;
}}
main::-webkit-scrollbar {{ width: 8px; }}
main::-webkit-scrollbar-thumb {{
  background: rgba(62, 224, 201, 0.25);
  border-radius: 99px;
}}
html.light main::-webkit-scrollbar-thumb {{
  background: rgba(13, 148, 136, 0.35);
}}
.paper {{
  max-width: 40rem;
  margin: 0 auto 2.5rem;
  scroll-margin-top: 1.25rem;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 0;
  overflow: hidden;
  transition: box-shadow 0.25s, border-color 0.25s;
}}
.paper:hover {{
  border-color: rgba(62, 224, 201, 0.25);
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.35);
}}
html.light .paper:hover {{
  border-color: rgba(13, 148, 136, 0.25);
}}
.paper-hd {{
  padding: 0.85rem 1.35rem;
  background: linear-gradient(90deg, rgba(62, 224, 201, 0.1), rgba(167, 139, 250, 0.06));
  border-bottom: 1px solid var(--border);
}}
.path {{
  font-size: 0.7rem;
  font-family: var(--font-ui);
  font-weight: 500;
  color: var(--muted);
  word-break: break-all;
  letter-spacing: 0.02em;
}}
.paper-bd {{
  padding: 1.35rem 1.5rem 1.6rem;
}}
.md {{
  font-family: var(--font-body);
  font-size: 1.0625rem;
  line-height: 1.75;
  letter-spacing: 0.01em;
}}
.md h1 {{
  font-family: var(--font-ui);
  font-size: 1.5rem;
  font-weight: 700;
  margin-top: 0;
  letter-spacing: -0.03em;
  line-height: 1.3;
}}
.md h2 {{
  font-family: var(--font-ui);
  font-size: 1.15rem;
  font-weight: 700;
  margin-top: 1.65em;
  padding-bottom: 0.35em;
  border-bottom: 2px solid transparent;
  border-image: linear-gradient(90deg, var(--accent), var(--accent2)) 1;
  letter-spacing: -0.02em;
}}
.md h3 {{
  font-family: var(--font-ui);
  font-size: 1.02rem;
  font-weight: 600;
  margin-top: 1.25em;
  color: var(--accent);
}}
.md p {{ margin: 0.85em 0; }}
.md ul, .md ol {{ margin: 0.75em 0; padding-left: 1.35em; }}
.md li {{ margin: 0.35em 0; }}
.md hr {{
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
  margin: 2rem 0;
}}
.md code {{
  font-family: ui-monospace, "Cascadia Code", "Consolas", monospace;
  background: var(--code-bg);
  padding: 0.12em 0.4em;
  border-radius: 6px;
  font-size: 0.86em;
  border: 1px solid var(--border);
}}
.md pre {{
  background: var(--code-bg);
  padding: 1rem 1.15rem;
  border-radius: var(--radius-sm);
  overflow: auto;
  border: 1px solid var(--border);
  font-size: 0.88rem;
  line-height: 1.55;
}}
.md pre code {{
  background: none;
  padding: 0;
  border: none;
  font-size: inherit;
}}
.md table {{
  border-collapse: collapse;
  width: 100%;
  font-size: 0.92rem;
  font-family: var(--font-ui);
  border-radius: var(--radius-sm);
  overflow: hidden;
  margin: 1em 0;
}}
.md th, .md td {{
  border: 1px solid var(--border);
  padding: 0.55rem 0.75rem;
}}
.md th {{
  background: rgba(62, 224, 201, 0.12);
  font-weight: 600;
  text-align: left;
}}
html.light .md th {{
  background: rgba(13, 148, 136, 0.12);
}}
.md blockquote {{
  margin: 1.1em 0;
  padding: 0.65rem 1rem 0.65rem 1.1rem;
  border-left: 4px solid var(--accent2);
  background: rgba(167, 139, 250, 0.08);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  color: var(--muted);
  font-style: italic;
}}
.md a {{
  color: var(--accent);
  font-weight: 600;
  text-decoration: none;
  border-bottom: 1px solid rgba(62, 224, 201, 0.35);
  transition: color 0.15s, border-color 0.15s;
}}
.md a:hover {{
  color: var(--accent2);
  border-bottom-color: var(--accent2);
}}
html.light .md a {{
  color: #0f766e;
}}
.math-inline {{
  display: inline;
  vertical-align: middle;
}}
.math-inline .katex {{
  font-size: 1.08em;
  color: var(--math-color) !important;
}}
.math-display {{
  margin: 1.35rem 0;
  overflow-x: auto;
  text-align: center;
}}
.math-display .katex {{
  color: var(--math-color) !important;
}}
.hidden-mod {{ display: none; }}
</style>
</head>
<body>
<div class="layout">
  <aside>
    <div class="aside-hd">
      <h1>{escape(h1_txt)}</h1>
      <div class="tagline">{escape(tag_txt)}</div>
      <div class="tools">
        <input type="search" id="q" placeholder="筛选标题…" autocomplete="off">
        <button type="button" id="btnRand">随机一篇</button>
        <button type="button" id="btnTheme">浅色</button>
      </div>
    </div>
    <nav class="nav-scroll" id="nav">{nav_joined}</nav>
  </aside>
  <main id="main">{articles_joined}</main>
</div>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin></script>
<script>
(function() {{
  function renderKatex() {{
    if (typeof katex === 'undefined') return;
    document.querySelectorAll('.math-render:not([data-katex-done])').forEach(function(el) {{
      var tex = el.getAttribute('data-latex');
      if (!tex) return;
      try {{
        katex.render(tex, el, {{
          displayMode: el.classList.contains('math-display'),
          throwOnError: false,
          strict: false
        }});
        el.setAttribute('data-katex-done', '1');
      }} catch (err) {{
        el.textContent = tex;
      }}
    }});
  }}
  renderKatex();

  const links = Array.from(document.querySelectorAll('.nav-link'));
  const articles = Array.from(document.querySelectorAll('.paper'));
  const idToArticle = Object.fromEntries(articles.map(a => [a.id, a]));
  const q = document.getElementById('q');
  const btnRand = document.getElementById('btnRand');
  const btnTheme = document.getElementById('btnTheme');

  function filterNav() {{
    const term = (q.value || '').trim().toLowerCase();
    document.querySelectorAll('.mod').forEach(mod => {{
      let any = false;
      mod.querySelectorAll('.nav-link').forEach(a => {{
        const t = (a.dataset.title || a.textContent || '').toLowerCase();
        const show = !term || t.includes(term);
        a.classList.toggle('hidden', !show);
        if (show) any = true;
      }});
      mod.classList.toggle('hidden-mod', !any);
    }});
  }}
  q.addEventListener('input', filterNav);

  document.getElementById('nav').addEventListener('click', function(e) {{
    const a = e.target.closest('a.nav-link');
    if (!a) return;
    const id = a.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }});

  btnRand.addEventListener('click', function() {{
    const visibleLinks = links.filter(a => !a.classList.contains('hidden'));
    const pool = visibleLinks.length ? visibleLinks : links;
    const a = pool[Math.floor(Math.random() * pool.length)];
    if (!a) return;
    const id = a.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) {{
      el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      history.replaceState(null, '', '#' + id);
    }}
  }});

  function applyTheme(light) {{
    document.documentElement.classList.toggle('light', light);
    btnTheme.textContent = light ? '深色' : '浅色';
    try {{ localStorage.setItem('studyTheme', light ? 'light' : 'dark'); }} catch (e) {{}}
  }}
  btnTheme.addEventListener('click', function() {{
    applyTheme(!document.documentElement.classList.contains('light'));
  }});
  try {{
    const s = localStorage.getItem('studyTheme');
    if (s === 'light') applyTheme(true);
  }} catch (e) {{}}

  if (location.hash && idToArticle[location.hash.slice(1)]) {{
    setTimeout(() => idToArticle[location.hash.slice(1)].scrollIntoView(), 0);
  }}
}})();
</script>
</body>
</html>"""

    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT} ({len(html) // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
