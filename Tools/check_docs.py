"""Static checks for the English and Japanese manuals.

Runs without Writerside, so it catches the common breakages before the Docker
build does. Per module: the .tree parses, every tree entry has a topic file and
every topic is in the tree, every local .md link and image resolves, and the
<tldr>, <note>, <warning>, <tip>, <procedure>, <deflist>, <def> and <step>
tags balance. Across modules: the Japanese tree has the same topics in the same
order as the English one.

Exit status is 1 when any error is found. Warnings do not fail the run.

    python Tools/check_docs.py
"""
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULES = {"en": ("Writerside", "hi.tree"), "jp": ("WritersideJP", "jp.tree")}
IMAGES = os.path.join(ROOT, "Writerside", "images")
# Topic files kept in the module but deliberately left out of the tree.
UNLISTED = {"lib.md"}

errors, warnings = [], []


def topics_in(module):
    out = {}
    base = os.path.join(ROOT, module, "topics")
    for root, _, files in os.walk(base):
        for f in files:
            if f.endswith(".md"):
                out[f] = os.path.join(root, f)
    return out


def tree_order(module, tree):
    path = os.path.join(ROOT, module, tree)
    text = open(path, encoding="utf-8").read()
    # The DOCTYPE references a remote DTD; strip it so ElementTree parses offline.
    text = re.sub(r"<!DOCTYPE[^>]*>", "", text, flags=re.S)
    root = ET.fromstring(text.encode("utf-8"))
    return [el.get("topic") for el in root.iter("toc-element")]


image_files = set(os.listdir(IMAGES))
orders = {}
for loc, (module, tree) in MODULES.items():
    topics = topics_in(module)
    try:
        order = tree_order(module, tree)
    except ET.ParseError as exc:
        errors.append(f"[{loc}] {tree} does not parse: {exc}")
        continue
    orders[loc] = order
    for t in order:
        if t not in topics:
            errors.append(f"[{loc}] tree references missing topic {t}")
    for t in topics:
        if t not in order and t not in UNLISTED:
            warnings.append(f"[{loc}] topic not in tree: {t}")
    for name, path in topics.items():
        if name in UNLISTED:
            continue
        s = open(path, encoding="utf-8-sig").read()
        body = re.sub(r"```.*?```", "", s, flags=re.S)
        body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        body = re.sub(r"`[^`\n]+`", "", body)
        for m in re.finditer(r"\]\(([^)\s#]+\.md)(#[^)]*)?\)|href=\"([^\"#]+\.md)(#[^\"]*)?\"", body):
            target = m.group(1) or m.group(3)
            if "/" in target or target.startswith("http"):
                continue
            if target not in topics:
                errors.append(f"[{loc}] {name}: broken link -> {target}")
        for m in re.finditer(r"<img[^>]*src=\"([^\"]+)\"|!\[[^\]]*\]\(([^)\s]+)\)", body):
            src = m.group(1) or m.group(2)
            if src.startswith("http"):
                continue
            if src not in image_files:
                errors.append(f"[{loc}] {name}: missing image {src}")
        if body.count("<tldr>") != body.count("</tldr>"):
            errors.append(f"[{loc}] {name}: unbalanced <tldr>")
        for tag in ("note", "warning", "tip", "procedure", "deflist", "def", "step"):
            opened = len(re.findall(rf"<{tag}[ >]", body))
            closed = body.count(f"</{tag}>")
            if opened != closed:
                errors.append(f"[{loc}] {name}: <{tag}> open {opened} / close {closed}")
        if not re.match(r"﻿?# ", s):
            warnings.append(f"[{loc}] {name}: does not start with an H1")

if "en" in orders and "jp" in orders:
    if orders["en"] != orders["jp"]:
        import difflib
        diff = "\n".join(difflib.unified_diff(orders["en"], orders["jp"], "en", "jp", lineterm=""))
        errors.append("EN/JP tree order differs:\n" + diff)
    en_topics, jp_topics = set(topics_in("Writerside")), set(topics_in("WritersideJP"))
    for t in sorted(en_topics - jp_topics):
        errors.append(f"JP missing topic file {t}")
    for t in sorted(jp_topics - en_topics):
        errors.append(f"JP has extra topic file {t}")

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
