# -*- coding: utf-8 -*-
"""Short slugs for filenames: NNN-slug.md. One per question, safe for filenames."""
import re

def _sanitize(s):
    s = s.replace("`", "").replace("'", "").replace('"', "")
    for c in r'/\:*?"<>|':
        s = s.replace(c, "-")
    s = re.sub(r'\s+', '-', s).strip('- ')
    return s[:38] if len(s) > 38 else s

def _slug(q):
    # Prefer part before first ？ or ?
    for sep in ["？", "?"]:
        if sep in q:
            q = q.split(sep)[0].strip()
    return _sanitize(q)

# Generated from questions_data.QUESTIONS; index 0 = question 1.
def get_slugs():
    from questions_data import QUESTIONS
    return [_slug(q) for q in QUESTIONS]

if __name__ == "__main__":
    for i, s in enumerate(get_slugs(), 1):
        print(f"{i:03d} {s}")
