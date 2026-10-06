"""Join hard-wrapped lines in Japanese sources where the break falls between two
CJK characters.

Browsers render a line break inside a paragraph as a space. Between Japanese
characters that space is visible (Chromium does not apply the CSS Text segment
break rules that would drop it), so a paragraph wrapped at 120 columns in the
source shows stray gaps on the page. This rewrites the sources so that every
CJK-to-CJK break is removed, leaving breaks next to Latin text alone.

    python Tools/join_cjk_lines.py            # rewrite in place
    python Tools/join_cjk_lines.py --check    # exit 1 if anything would change

Fenced code blocks (```) and <code-block> elements are left untouched.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGETS = [
    (os.path.join(ROOT, "WritersideJP", "topics"), ".md"),
    (os.path.join(ROOT, "ViteTech", "src", "pages", "ja"), ".html"),
]

CJK = "　-〿぀-ヿ㐀-䶿一-鿿＀-￯"
ENDS_CJK = re.compile(f"[{CJK}]$")
STARTS_CJK = re.compile(f"^[{CJK}]")
# Full-width punctuation never takes a space after it (or before it), whatever
# the neighbouring character is.
CJK_PUNCT = "、。，．：；！？）」』】"
ENDS_PUNCT = re.compile(f"[{CJK_PUNCT}]$")
STARTS_PUNCT = re.compile(f"^[{CJK_PUNCT}]")
# A line starting like this opens a new block (list item, heading, table row,
# HTML element, attribute block, quote or fence) and must never be joined.
BLOCK_START = re.compile(r"^(\d+\.\s|[-*+]\s|#|\||<|\{|>|```)")


def join(text):
    lines = text.split("\n")
    out = []
    in_fence = False
    in_code_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if "<code-block" in stripped:
            in_code_block = True
        if in_fence or in_code_block:
            out.append(line)
            if "</code-block>" in stripped:
                in_code_block = False
            continue
        prev = out[-1].rstrip() if out else ""
        joinable = not BLOCK_START.match(stripped) and (
            (STARTS_CJK.match(stripped) and ENDS_CJK.search(prev))
            or ENDS_PUNCT.search(prev)
            or (STARTS_PUNCT.match(stripped) and prev)
        )
        if (out and stripped and joinable
                and not out[-1].lstrip().startswith(("#", "|", "```"))):
            out[-1] = out[-1].rstrip() + stripped
            continue
        out.append(line)
    return "\n".join(out)


def main():
    check = "--check" in sys.argv
    changed = []
    for folder, ext in TARGETS:
        for dirpath, _, files in os.walk(folder):
            for name in files:
                if not name.endswith(ext):
                    continue
                path = os.path.join(dirpath, name)
                with open(path, encoding="utf-8-sig") as fh:
                    text = fh.read()
                new = join(text)
                if new != text:
                    changed.append(os.path.relpath(path, ROOT))
                    if not check:
                        with open(path, "w", encoding="utf-8", newline="\n") as fh:
                            fh.write(new)
    for path in changed:
        print(("would change " if check else "joined ") + path)
    print(f"{len(changed)} file(s)")
    if check and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
