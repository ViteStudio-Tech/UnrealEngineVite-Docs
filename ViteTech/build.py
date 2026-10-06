"""Build the Vite Technology site.

Pages are written as HTML fragments in src/pages/<locale>/ and wrapped here
in the shared header, footer and metadata, so twelve pages cannot drift
apart. Output goes to public/ (English) and public/jp/ (Japanese), next to
the static assets in public/assets/.

    python ViteTech/build.py

No dependencies beyond the Python standard library. The docs workflow runs
this before publishing public/ under /tech/ on GitHub Pages.

Page fragments start with a front-matter comment:

    <!--
    title: Vite ReSTIR
    description: One sentence for search results and link previews.
    nav: restir
    product: restir
    image: assets/img/restir-attic.jpg
    -->

and may use these placeholders:

    {{assets}}      relative path to public/assets/
    {{docs}}        absolute URL of the manual in the page's language
    {{icon:name}}   an inline SVG icon from ICONS below
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src", "pages")
OUT = os.path.join(HERE, "public")

SITE_URL = "https://vitestudio-tech.github.io/UnrealEngineVite-Docs/tech/"
DOCS_URL = "https://vitestudio-tech.github.io/UnrealEngineVite-Docs/"

PAGES = ["index", "restir", "vitex-physics", "brdf", "vertis", "hair-fx"]

PRODUCTS = [
    ("restir", "restir.html"),
    ("vitex", "vitex-physics.html"),
    ("brdf", "brdf.html"),
    ("vertis", "vertis.html"),
    ("hairfx", "hair-fx.html"),
]

LOCALES = {
    "en": {
        "lang": "en",
        "out": "",
        "assets": "assets/",
        "docs": DOCS_URL,
        "other": "ja",
        "other_label": "日本語",
        "other_title": "日本語で表示",
        "skip": "Skip to content",
        "menu": "Menu",
        "nav_label": "Primary",
        "brand_family": "Technology",
        "names": {
            "restir": "ReSTIR", "vitex": "ViteX Physics", "brdf": "BRDF",
            "vertis": "Vertis", "hairfx": "Hair FX",
        },
        "docs_label": "Docs",
        "contact": "Partner with us",
        "footer_blurb": "Rendering, physics and geometry technology from the team behind Unreal Engine Vite.",
        "footer_tech": "Technology",
        "footer_engine": "Engine",
        "footer_company": "Studio",
        "full_names": {
            "restir": "Vite ReSTIR", "vitex": "ViteX Physics", "brdf": "Vite BRDF",
            "vertis": "Vite Vertis", "hairfx": "Vite Hair FX",
        },
        "engine_links": [
            ("Unreal Engine Vite manual", DOCS_URL),
            ("Release notes", DOCS_URL + "release-notes.html"),
            ("Projects and demos", DOCS_URL + "projectsanddemos.html"),
            ("Engine on GitHub", "https://github.com/GapingPixel/UnrealEngineVite-PhysX"),
        ],
        "company_links": [
            ("Discord", "https://discord.gg/n9zQrYFhMb"),
            ("Updates on X", "https://x.com/theredpix"),
            ("Sample projects", "https://github.com/orgs/ViteStudio-Tech/repositories"),
            ("Support development", "https://ko-fi.com/vitestudio"),
        ],
        "legal": "Unreal Engine is a trademark of Epic Games, Inc. NVIDIA, PhysX, Flex, Flow and Blast are "
                 "trademarks of NVIDIA Corporation. AMD and TressFX are trademarks of Advanced Micro Devices, Inc. "
                 "All other trademarks are the property of their respective owners.",
    },
    "ja": {
        "lang": "ja",
        "out": "jp/",
        "assets": "../assets/",
        "docs": DOCS_URL + "jp/",
        "other": "en",
        "other_label": "English",
        "other_title": "View in English",
        "skip": "本文へスキップ",
        "menu": "メニュー",
        "nav_label": "メインメニュー",
        "brand_family": "Technology",
        "names": {
            "restir": "ReSTIR", "vitex": "ViteX Physics", "brdf": "BRDF",
            "vertis": "Vertis", "hairfx": "Hair FX",
        },
        "docs_label": "ドキュメント",
        "contact": "提携のご相談",
        "footer_blurb": "Unreal Engine Vite の開発チームによる、レンダリング・物理・ジオメトリ技術。",
        "footer_tech": "テクノロジー",
        "footer_engine": "エンジン",
        "footer_company": "スタジオ",
        "full_names": {
            "restir": "Vite ReSTIR", "vitex": "ViteX Physics", "brdf": "Vite BRDF",
            "vertis": "Vite Vertis", "hairfx": "Vite Hair FX",
        },
        "engine_links": [
            ("Unreal Engine Vite マニュアル", DOCS_URL + "jp/"),
            ("リリースノート", DOCS_URL + "jp/release-notes.html"),
            ("プロジェクトとデモ", DOCS_URL + "jp/projectsanddemos.html"),
            ("GitHub のエンジンリポジトリ", "https://github.com/GapingPixel/UnrealEngineVite-PhysX"),
        ],
        "company_links": [
            ("Discord", "https://discord.gg/n9zQrYFhMb"),
            ("X での最新情報", "https://x.com/theredpix"),
            ("サンプルプロジェクト", "https://github.com/orgs/ViteStudio-Tech/repositories"),
            ("開発を支援する", "https://ko-fi.com/vitestudio"),
        ],
        "legal": "Unreal Engine は Epic Games, Inc. の商標です。NVIDIA、PhysX、Flex、Flow、Blast は NVIDIA Corporation の"
                 "商標です。AMD および TressFX は Advanced Micro Devices, Inc. の商標です。その他の商標はそれぞれの所有者に"
                 "帰属します。",
    },
}

# 24x24 stroke icons, drawn to one grid so they sit together in feature lists.
ICONS = {
    "rays": '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>',
    "path": '<path d="M3 20 9 9l5 6 7-11"/><circle cx="9" cy="9" r="1.6"/><circle cx="14" cy="15" r="1.6"/>',
    "stack": '<ellipse cx="12" cy="6" rx="7" ry="2.6"/><path d="M5 6v6c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6V6M5 12v6c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6v-6"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "grid": '<rect x="3.5" y="3.5" width="17" height="17" rx="1.5"/><path d="M9.2 3.5v17M14.8 3.5v17M3.5 9.2h17M3.5 14.8h17"/>',
    "gauge": '<path d="M4.5 17a8.5 8.5 0 1 1 15 0"/><path d="M12 13.5 16 8.5"/><circle cx="12" cy="14" r="1.3"/>',
    "cube": '<path d="M12 2.8 20 7.2v9.6L12 21.2 4 16.8V7.2z"/><path d="M4 7.2 12 11.6l8-4.4M12 11.6v9.6"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="1.5"/><path d="M9.5 9.5h5v5h-5zM9 2.5V6M15 2.5V6M9 18v3.5M15 18v3.5M2.5 9H6M2.5 15H6M18 9h3.5M18 15h3.5"/>',
    "drop": '<path d="M12 3s6 6.6 6 11a6 6 0 0 1-12 0c0-4.4 6-11 6-11z"/>',
    "flame": '<path d="M12 21c-3.9 0-6.5-2.6-6.5-6.2 0-3.9 3.4-5.7 3.9-9.8 2.6 1.6 4 3.9 4 6.1.9-.6 1.6-1.8 1.8-3.2 2 1.6 3.3 4.2 3.3 6.9 0 3.6-2.6 6.2-6.5 6.2z"/>',
    "plug": '<path d="M9 3v5M15 3v5M6.5 8h11v3.5a5.5 5.5 0 0 1-11 0zM12 17v4"/>',
    "layers": '<path d="M12 3 21 8l-9 5-9-5zM3 12.5l9 5 9-5M3 17l9 5 9-5"/>',
    "face": '<circle cx="12" cy="12" r="8.5"/><path d="M8.8 14.6c1.8 1.8 4.6 1.8 6.4 0"/><circle cx="9" cy="10" r=".9"/><circle cx="15" cy="10" r=".9"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    "mesh": '<path d="M3 19 12 4l9 15z"/><path d="M7.5 11.5h9M12 4l-4.5 15M12 4l4.5 15"/>',
    "morph": '<path d="M4 8h12l-3-3M20 16H8l3 3"/>',
    "strand": '<path d="M5 3c4 4-2 7 2 11s-1 6 1 7M12 3c4 4-2 7 2 11s-1 6 1 7M19 3c-2 3 1 6-1 9s1 6 0 9"/>',
    "wind": '<path d="M3 9h11a3 3 0 1 0-3-3M3 15h15a3 3 0 1 1-3 3M3 12h7"/>',
    "shield": '<path d="M12 3 19.5 6v5.5c0 4.6-3.2 8.2-7.5 9.5-4.3-1.3-7.5-4.9-7.5-9.5V6z"/><path d="m8.8 12 2.2 2.2 4.2-4.4"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M8 8h8v8H8z"/>',
    "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "switch": '<rect x="2.5" y="7" width="19" height="10" rx="5"/><circle cx="16.5" cy="12" r="3"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "external": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
}


def icon(name):
    if name not in ICONS:
        sys.exit(f"unknown icon {name}")
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
            + ICONS[name] + "</svg>")


def parse(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"\s*<!--(.*?)-->", text, flags=re.S)
    if not m:
        sys.exit(f"{path}: missing front matter")
    meta = {}
    for line in m.group(1).strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    for key in ("title", "description"):
        if key not in meta:
            sys.exit(f"{path}: front matter needs {key}")
    return meta, text[m.end():]


def href_for(page, locale):
    return "index.html" if page == "index" else f"{page}.html"


def header(loc, page, nav):
    L = LOCALES[loc]
    other = LOCALES[L["other"]]
    other_href = ("jp/" if loc == "en" else "../") + href_for(page, loc)
    links = []
    for key, href in PRODUCTS:
        current = ' aria-current="page"' if nav == key else ""
        links.append(f'<a class="nav__link" href="{href}"{current}>{html.escape(L["names"][key])}</a>')
    links.append(f'<a class="nav__link" href="{L["docs"]}">{html.escape(L["docs_label"])}</a>')
    links.append(f'<a class="nav__lang" href="{other_href}" lang="{other["lang"]}" hreflang="{other["lang"]}" '
                 f'title="{html.escape(L["other_title"])}">{L["other_label"]}</a>')
    return f"""<a class="skip-link" href="#main">{html.escape(L['skip'])}</a>
<header class="site-header">
    <div class="wrap">
        <a class="brand" href="index.html" aria-label="Vite Technology">
            <span class="brand__mark">VITE</span><span class="brand__family">{L['brand_family']}</span>
        </a>
        <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="{html.escape(L['menu'])}">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        </button>
        <nav class="nav" id="site-nav" aria-label="{html.escape(L['nav_label'])}">
            {chr(10).join('            ' + l for l in links).strip()}
        </nav>
    </div>
</header>"""


def footer(loc):
    L = LOCALES[loc]
    tech = "\n".join(f'<li><a href="{href}">{html.escape(L["full_names"][key])}</a></li>' for key, href in PRODUCTS)
    engine = "\n".join(f'<li><a href="{u}">{html.escape(t)}</a></li>' for t, u in L["engine_links"])
    company = "\n".join(f'<li><a href="{u}" rel="noopener">{html.escape(t)}</a></li>' for t, u in L["company_links"])
    return f"""<footer class="site-footer">
    <div class="wrap">
        <div class="footer-grid">
            <div>
                <a class="brand" href="index.html" aria-label="Vite Technology"><span class="brand__mark">VITE</span><span class="brand__family">{L['brand_family']}</span></a>
                <p style="margin:16px 0 0;max-width:36ch">{html.escape(L['footer_blurb'])}</p>
            </div>
            <div><h2>{html.escape(L['footer_tech'])}</h2><ul>{tech}</ul></div>
            <div><h2>{html.escape(L['footer_engine'])}</h2><ul>{engine}</ul></div>
            <div><h2>{html.escape(L['footer_company'])}</h2><ul>{company}</ul></div>
        </div>
        <div class="footer-legal">
            <span>&copy; <span data-year>2026</span> Vite Studio</span>
            <span style="max-width:80ch">{html.escape(L['legal'])}</span>
        </div>
    </div>
</footer>"""


def asset_version(rel):
    """Short content hash appended to CSS/JS URLs so a deploy is never served stale."""
    import hashlib
    with open(os.path.join(OUT, "assets", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


def render(loc, page):
    L = LOCALES[loc]
    meta, body = parse(os.path.join(SRC, loc, page + ".html"))
    body = body.replace("{{assets}}", L["assets"]).replace("{{docs}}", L["docs"])
    body = re.sub(r"\{\{icon:([a-z]+)\}\}", lambda m: icon(m.group(1)), body)
    leftover = re.findall(r"\{\{[^}]*\}\}", body)
    if leftover:
        sys.exit(f"{loc}/{page}: unresolved placeholders {leftover}")

    product = meta.get("product", "")
    body_attr = f' data-product="{product}"' if product else ""
    url_en = SITE_URL + href_for(page, "en")
    url_ja = SITE_URL + "jp/" + href_for(page, "ja")
    canonical = url_en if loc == "en" else url_ja
    image = SITE_URL + meta.get("image", "assets/img/hero-apartment.jpg")
    title = meta["title"] if page == "index" else f"{meta['title']} — Vite Technology"

    return f"""<!doctype html>
<html lang="{L['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(meta['description'])}">
<meta name="theme-color" content="#050607">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" hreflang="ja" href="{url_ja}">
<link rel="alternate" hreflang="x-default" href="{url_en}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Vite Technology">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(meta['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="64x64" href="{L['assets']}img/favicon-64.png">
<link rel="apple-touch-icon" href="{L['assets']}img/touch-icon-180.png">
<link rel="preload" href="{L['assets']}fonts/ViteVector-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{L['assets']}css/site.css?v={asset_version('css/site.css')}">
</head>
<body{body_attr}>
{header(loc, page, meta.get('nav', ''))}
<main id="main">
{body.strip()}
</main>
{footer(loc)}
<script src="{L['assets']}js/site.js?v={asset_version('js/site.js')}" defer></script>
</body>
</html>
"""


def main():
    count = 0
    for loc, L in LOCALES.items():
        out_dir = os.path.join(OUT, L["out"])
        os.makedirs(out_dir, exist_ok=True)
        for page in PAGES:
            src = os.path.join(SRC, loc, page + ".html")
            if not os.path.exists(src):
                print(f"skip {loc}/{page} (no source)")
                continue
            with open(os.path.join(out_dir, href_for(page, loc)), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(render(loc, page))
            count += 1
    print(f"built {count} pages")


if __name__ == "__main__":
    main()
