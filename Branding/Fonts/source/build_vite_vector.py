"""Build the Vite Vector display typeface as TTF, OTF and WOFF2.

Vite Vector is a monoline geometric display face: uniform stroke weight, tall
oval bowls, flat cut terminals, pointed apexes, and generous sidebearings so it
tracks out cleanly in a wordmark. Its signature is the stemless E, drawn as
three detached bars.

Glyphs are generated from editable centerline recipes. Every centerline is
expanded to an outline with mitered joins, so the result is a real closed-path
font rather than a set of overlapping rectangles.
"""

from __future__ import annotations

import base64
import math
import re
from pathlib import Path

from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont

UPM = 1000
CAP = 700
ASCENDER = 780
DESCENDER = -200

# Stroke is ~9% of the cap height, which is where the reference wordmark sits.
W = 62

# Nominal sidebearing. Round-sided glyphs get a little less so the rhythm reads
# even, which is the usual optical correction for O against H.
SB = 60
SB_ROUND = 50

# Round bowls are taller than they are wide; this is what stops the face from
# reading as generic Futura.
RX = 273
RY = 357
OVERSHOOT = 7

OUTPUT_DIR = Path(__file__).resolve().parent.parent

# Everything the header wordmark needs, for the embedded subset.
WORDMARK_TEXT = "Unreal Engine Vite"

# Writerside injects this file into <head> and gives us nowhere to host a font
# binary next to it, so the subset is inlined and refreshed from here.
THEME_FILE = OUTPUT_DIR.parent.parent / "Writerside" / "cfg" / "vite-theme.html"


# --------------------------------------------------------------------------- #
# Geometry
# --------------------------------------------------------------------------- #


def arc(cx, cy, rx, ry, start_deg, end_deg, count=None):
    """Points along an elliptical arc, inclusive of both ends."""
    if count is None:
        count = max(8, int(abs(end_deg - start_deg) / 4) + 2)
    span = end_deg - start_deg
    return [
        (
            cx + rx * math.cos(math.radians(start_deg + span * i / (count - 1))),
            cy + ry * math.sin(math.radians(start_deg + span * i / (count - 1))),
        )
        for i in range(count)
    ]


def bezier(p0, p1, p2, p3, count=20):
    points = []
    for i in range(count):
        t = i / (count - 1)
        u = 1 - t
        points.append(
            (
                u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],
            )
        )
    return points


def _intersect(a0, a1, b0, b1, vertex, limit):
    """Intersection of two offset lines, falling back to a bevel."""
    d1 = (a1[0] - a0[0], a1[1] - a0[1])
    d2 = (b1[0] - b0[0], b1[1] - b0[1])
    denominator = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(denominator) < 1e-9:
        return [a1]
    t = ((b0[0] - a0[0]) * d2[1] - (b0[1] - a0[1]) * d2[0]) / denominator
    point = (a0[0] + d1[0] * t, a0[1] + d1[1] * t)
    if math.hypot(point[0] - vertex[0], point[1] - vertex[1]) > limit:
        return [a1, b0]
    return [point]


def _offset(points, distance, miter_limit):
    segments = []
    for i in range(len(points) - 1):
        ax, ay = points[i]
        bx, by = points[i + 1]
        dx, dy = bx - ax, by - ay
        length = math.hypot(dx, dy)
        if length < 1e-9:
            continue
        nx, ny = -dy / length * distance, dx / length * distance
        segments.append(((ax + nx, ay + ny), (bx + nx, by + ny)))
    if not segments:
        return []
    out = [segments[0][0]]
    for i in range(len(segments) - 1):
        out.extend(_intersect(*segments[i], *segments[i + 1], points[i + 1], miter_limit))
    out.append(segments[-1][1])
    return out


def stroke(points, width=W, miter=4.0):
    """Expand an open centerline into a closed outline with butt caps."""
    if len(points) < 2:
        return []
    half = width / 2
    limit = half * miter
    left = _offset(points, half, limit)
    right = _offset(points, -half, limit)
    if not left or not right:
        return []
    return left + list(reversed(right))


def line(a, b, width=W):
    return stroke([a, b], width)


def hbar(y, x0, x1, width=W):
    return stroke([(x0, y), (x1, y)], width)


def vbar(x, y0, y1, width=W):
    return stroke([(x, y0), (x, y1)], width)


def ring(cx, cy, rx, ry, width=W):
    """Closed elliptical ring: clockwise outer contour, counter-clockwise inner."""
    outer = arc(cx, cy, rx + width / 2, ry + width / 2, 0, 360, 68)[:-1]
    inner = arc(cx, cy, rx - width / 2, ry - width / 2, 0, 360, 68)[:-1]
    return [list(reversed(outer)), inner]


# --------------------------------------------------------------------------- #
# Glyph recipes
#
# Coordinates are centerlines. Glyphs are normalised afterwards so that every
# one carries the same left sidebearing, which keeps the rhythm even without
# hand-tuning each advance.
# --------------------------------------------------------------------------- #

MID = CAP / 2
TOP = CAP - W / 2
BOT = W / 2
BOWL_CX = SB_ROUND + RX
BOWL_CY = MID


def glyph_recipes():
    g: dict[str, tuple[list[list[tuple[float, float]]], float]] = {}

    def put(name, contours, sidebearing=SB):
        g[name] = ([c for c in contours if len(c) >= 3], sidebearing)

    cx, cy = BOWL_CX, BOWL_CY
    crx, cry = RX - W / 2, RY - W / 2 + OVERSHOOT

    # -- Uppercase ---------------------------------------------------------- #

    put("A", [stroke([(95, 0), (323, CAP), (551, 0)]), hbar(215, 165, 481)])
    put(
        "B",
        [
            vbar(91, 0, CAP),
            stroke(arc(91, 525, 372, 175 + OVERSHOOT / 2, 90, -90)),
            stroke(arc(91, 175, 402, 175 + OVERSHOOT / 2, 90, -90)),
        ],
    )
    # Aperture on the right, terminals cut square to the arc.
    put("C", [stroke(arc(cx, cy, crx, cry, 54, 306))], SB_ROUND)
    put(
        "D",
        [
            vbar(91, 0, CAP),
            hbar(TOP, 91, 300),
            hbar(BOT, 91, 300),
            stroke(arc(300, cy, 262, cry, 90, -90)),
        ],
    )
    # The signature: no stem, three equal detached bars.
    put("E", [hbar(TOP, 60, 480), hbar(MID, 60, 480), hbar(BOT, 60, 480)])
    put("F", [vbar(91, 0, CAP), hbar(TOP, 60, 480), hbar(MID, 60, 424)])
    # Aperture in the upper right. The arc straightens into a short vertical at
    # mid-height, then turns back into the counter as the spur, so the G reads
    # as a G rather than a barred C.
    g_arc = arc(cx, cy, crx, cry, 44, 344)
    g_end = g_arc[-1][0]
    put("G", [stroke(g_arc + [(g_end, MID), (cx + 58, MID)])], SB_ROUND)
    put("H", [vbar(91, 0, CAP), vbar(539, 0, CAP), hbar(MID, 91, 539)])
    put("I", [vbar(91, 0, CAP)])
    put("J", [stroke([(429, CAP), (429, 196)] + arc(260, 196, 169, 196 + OVERSHOOT, 0, -180)[1:])])
    put("K", [vbar(91, 0, CAP), line((91, 296), (545, CAP)), line((91, 296), (560, 0))])
    put("L", [vbar(91, 0, CAP), hbar(BOT, 91, 470)])
    put("M", [stroke([(91, 0), (91, CAP), (370, 70), (649, CAP), (649, 0)])])
    put("N", [stroke([(91, 0), (91, CAP), (539, 0), (539, CAP)])])
    put("O", ring(cx, cy, RX - W / 2, RY - W / 2 + OVERSHOOT), SB_ROUND)
    put(
        "P",
        [vbar(91, 0, CAP), stroke(arc(91, 525, 402, 175 + OVERSHOOT / 2, 90, -90))],
    )
    put(
        "Q",
        ring(cx, cy, RX - W / 2, RY - W / 2 + OVERSHOOT) + [line((cx + 60, 150), (cx + 250, -46))],
        SB_ROUND,
    )
    put(
        "R",
        [
            vbar(91, 0, CAP),
            stroke(arc(91, 525, 372, 175 + OVERSHOOT / 2, 90, -90)),
            line((300, MID), (556, 0)),
        ],
    )
    s_spine = bezier((520, 588), (470, 716), (140, 712), (110, 534), 22)
    s_spine += bezier((110, 534), (78, 372), (540, 350), (540, 176), 24)[1:]
    s_spine += bezier((540, 176), (516, -12), (168, -16), (122, 128), 22)[1:]
    put("S", [stroke(s_spine)])
    put("T", [hbar(TOP, 60, 540), vbar(300, 0, TOP)])
    put(
        "U",
        [stroke([(91, CAP), (91, 190)] + arc(315, 190, 224, 190 + OVERSHOOT, 180, 360)[1:] + [(539, CAP)])],
    )
    put("V", [stroke([(95, CAP), (325, 0), (555, CAP)])])
    put("W", [stroke([(95, CAP), (255, 0), (450, 520), (645, 0), (805, CAP)])])
    put("X", [line((95, CAP), (545, 0)), line((95, 0), (545, CAP))])
    # Diagonal tail rather than a vertical stem, as in the reference lettering.
    put("Y", [line((560, CAP), (160, 0)), line((95, CAP), (377, 380))])
    put("Z", [hbar(TOP, 60, 550), line((520, TOP), (120, BOT)), hbar(BOT, 60, 550)])

    # -- Numerals ----------------------------------------------------------- #

    put("zero", ring(cx, cy, RX - W / 2, RY - W / 2 + OVERSHOOT), SB_ROUND)
    put("one", [vbar(300, 0, CAP), line((160, 596), (300, CAP))])
    put(
        "two",
        [stroke(arc(315, 492, 224, 208, 172, -12)), line((535, 448), (110, BOT)), hbar(BOT, 60, 550)],
    )
    put(
        "three",
        [
            hbar(TOP, 80, 300),
            stroke(arc(300, 522, 214, 178 - OVERSHOOT, 90, -90)),
            hbar(MID, 210, 400),
            stroke(arc(300, 178, 214, 178 + OVERSHOOT, 90, -90)),
            hbar(BOT, 80, 300),
        ],
    )
    put("four", [stroke([(470, CAP), (91, 236), (566, 236)]), vbar(470, 0, CAP)])
    put(
        "five",
        [
            hbar(TOP, 91, 520),
            vbar(91, CAP, 384),
            hbar(384, 91, 300),
            stroke(arc(300, 200, 236, 200 + OVERSHOOT, 90, -132)),
        ],
    )
    put(
        "six",
        ring(320, 216, 240, 216, W)
        + [stroke(bezier((80, 216), (72, 588), (250, 716), (520, 660), 22))],
    )
    put("seven", [hbar(TOP, 60, 560), line((542, TOP), (196, 0))])
    put("eight", ring(320, 512, 208, 176, W) + ring(320, 190, 240, 190, W))
    put(
        "nine",
        ring(320, 484, 240, 216, W)
        + [stroke(bezier((560, 484), (568, 112), (390, -16), (120, 40), 22))],
    )

    # -- Punctuation -------------------------------------------------------- #

    dot = ring(91, 34, 4, 4, W)
    put("period", dot)
    put("comma", [stroke([(100, 40), (60, -110)], W * 0.9)])
    put("colon", ring(91, 34, 4, 4, W) + ring(91, 400, 4, 4, W))
    put("semicolon", ring(91, 400, 4, 4, W) + [stroke([(100, 40), (60, -110)], W * 0.9)])
    put("hyphen", [hbar(320, 60, 380)])
    put("endash", [hbar(320, 60, 520)])
    put("emdash", [hbar(320, 60, 700)])
    put("underscore", [hbar(-90, 60, 560)])
    put("slash", [line((60, -60), (420, 760))])
    put("backslash", [line((60, 760), (420, -60))])
    put("bar", [vbar(91, -60, 760)])
    put("plus", [hbar(MID, 60, 480), vbar(270, MID - 210, MID + 210)])
    put("equal", [hbar(MID + 110, 60, 480), hbar(MID - 110, 60, 480)])
    put("asterisk", [line((91, 700), (91, 420)), line((-30, 630), (212, 490)), line((-30, 490), (212, 630))])
    put("exclam", [vbar(91, 178, CAP)] + ring(91, 34, 4, 4, W))
    put(
        "question",
        [stroke(arc(300, 502, 210, 172, 168, -22)), stroke([(510, 440), (300, 268), (300, 178)])]
        + ring(300, 34, 4, 4, W),
    )
    put("parenleft", [stroke(arc(330, MID, 250, 400, 118, 242))])
    put("parenright", [stroke(arc(60, MID, 250, 400, -62, 62))])
    put("bracketleft", [stroke([(320, 760), (91, 760), (91, -60), (320, -60)])])
    put("bracketright", [stroke([(60, 760), (289, 760), (289, -60), (60, -60)])])
    put("quotesingle", [vbar(91, 470, CAP)])
    put("quotedbl", [vbar(91, 470, CAP), vbar(251, 470, CAP)])
    put("ampersand", [stroke(bezier((560, 120), (300, -40), (60, 160), (240, 340), 20) + bezier((240, 340), (420, 520), (400, 700), (250, 700), 20)[1:] + bezier((250, 700), (110, 700), (110, 520), (560, 0), 24)[1:])])
    put("numbersign", [vbar(200, 0, CAP), vbar(400, 0, CAP), hbar(470, 60, 540), hbar(230, 60, 540)])
    put("percent", ring(160, 540, 96, 128, W) + ring(470, 160, 96, 128, W) + [line((540, CAP), (90, 0))])
    put("at", ring(cx, cy, RX - W / 2, RY - W / 2, W) + ring(cx, cy, 96, 120, W), SB_ROUND)

    put("space", [], 0)
    put(
        ".notdef",
        [stroke([(91, 0), (91, CAP), (509, CAP), (509, 0), (91, 0)])],
    )

    return g


# --------------------------------------------------------------------------- #
# Font assembly
# --------------------------------------------------------------------------- #


def normalise(recipes):
    """Shift each glyph to a uniform sidebearing and derive its advance."""
    out: dict[str, tuple[int, list]] = {}
    for name, (contours, sidebearing) in recipes.items():
        if not contours:
            out[name] = (340 if name == "space" else 500, [])
            continue
        xs = [p[0] for contour in contours for p in contour]
        shift = sidebearing - min(xs)
        moved = [[(x + shift, y) for x, y in contour] for contour in contours]
        advance = int(round(max(x for c in moved for x, _ in c) + sidebearing))
        out[name] = (advance, moved)
    return out


def draw_contours(pen, contours):
    for contour in contours:
        if len(contour) < 3:
            continue
        pen.moveTo(contour[0])
        for point in contour[1:]:
            pen.lineTo(point)
        pen.closePath()


UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGIT_NAMES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
PUNCTUATION = {
    " ": "space",
    ".": "period",
    ",": "comma",
    ":": "colon",
    ";": "semicolon",
    "-": "hyphen",
    "\u2013": "endash",
    "\u2014": "emdash",
    "_": "underscore",
    "/": "slash",
    "\\": "backslash",
    "|": "bar",
    "+": "plus",
    "=": "equal",
    "*": "asterisk",
    "!": "exclam",
    "?": "question",
    "(": "parenleft",
    ")": "parenright",
    "[": "bracketleft",
    "]": "bracketright",
    "'": "quotesingle",
    '"': "quotedbl",
    "&": "ampersand",
    "#": "numbersign",
    "%": "percent",
    "@": "at",
}


def character_map():
    cmap = {ord(letter): letter for letter in UPPERCASE}
    # Display face: lowercase code points render the uppercase designs.
    cmap.update({ord(letter.lower()): letter for letter in UPPERCASE})
    cmap.update({ord(str(i)): name for i, name in enumerate(DIGIT_NAMES)})
    cmap.update({ord(char): name for char, name in PUNCTUATION.items()})
    return cmap


FEATURES = """
languagesystem DFLT dflt;
feature kern {
    pos A V -40;
    pos A W -30;
    pos A Y -30;
    pos A T -30;
    pos F A -20;
    pos L T -25;
    pos L V -35;
    pos L Y -35;
    pos P A -20;
    pos R T -10;
    pos T A -30;
    pos T O -15;
    pos V A -40;
    pos V O -15;
    pos W A -25;
    pos Y A -35;
    pos Y O -20;
} kern;
"""


def configure(fb: FontBuilder, glyph_order, cmap, metrics):
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=ASCENDER, descent=DESCENDER, lineGap=90)
    fb.setupNameTable(
        {
            "familyName": "Vite Vector",
            "styleName": "Regular",
            "uniqueFontIdentifier": "ViteStudio:Vite Vector Regular:0.2",
            "fullName": "Vite Vector Regular",
            "psName": "ViteVector-Regular",
            "version": "Version 0.2",
            "description": "Monoline geometric display face for Unreal Engine Vite.",
            "designer": "Vite Studio",
            "manufacturer": "Vite Studio",
            "copyright": "Copyright 2026 Vite Studio. All rights reserved.",
        }
    )
    fb.setupOS2(
        sTypoAscender=ASCENDER,
        sTypoDescender=DESCENDER,
        sTypoLineGap=90,
        usWinAscent=ASCENDER,
        usWinDescent=abs(DESCENDER),
        sxHeight=CAP,
        sCapHeight=CAP,
        usWeightClass=300,
        usWidthClass=5,
        fsSelection=0x40,
    )
    fb.setupPost(italicAngle=0, underlinePosition=-120, underlineThickness=W)


def glyph_order_for(glyphs):
    return [".notdef"] + sorted(name for name in glyphs if name != ".notdef")


def build_ttf(glyphs, cmap, path):
    order = glyph_order_for(glyphs)
    metrics = {name: (advance, 0) for name, (advance, _) in glyphs.items()}
    outlines = {}
    for name, (_, contours) in glyphs.items():
        pen = TTGlyphPen(None)
        draw_contours(pen, contours)
        outlines[name] = pen.glyph()

    fb = FontBuilder(UPM, isTTF=True)
    configure(fb, order, cmap, metrics)
    fb.setupGlyf(outlines)
    fb.setupMaxp()
    fb.setupHead()
    addOpenTypeFeaturesFromString(fb.font, FEATURES)
    fb.setupDummyDSIG()
    fb.save(path)
    return path


def build_otf(glyphs, cmap, path):
    order = glyph_order_for(glyphs)
    metrics = {name: (advance, 0) for name, (advance, _) in glyphs.items()}
    charstrings = {}
    for name, (advance, contours) in glyphs.items():
        pen = T2CharStringPen(advance, None)
        draw_contours(pen, contours)
        charstrings[name] = pen.getCharString()

    fb = FontBuilder(UPM, isTTF=False)
    configure(fb, order, cmap, metrics)
    fb.setupCFF(
        "ViteVector-Regular",
        {
            "FullName": "Vite Vector Regular",
            "FamilyName": "Vite Vector",
            "Weight": "Regular",
            "version": "0.2",
            "Notice": "Copyright 2026 Vite Studio. All rights reserved.",
        },
        charstrings,
        {},
    )
    fb.setupHead()
    addOpenTypeFeaturesFromString(fb.font, FEATURES)
    fb.save(path)
    return path


def embed_in_theme(subset: Path, theme: Path = THEME_FILE):
    """Refresh the inlined subset in the Writerside theme."""
    if not theme.exists():
        return "theme not found"
    encoded = base64.b64encode(subset.read_bytes()).decode("ascii")
    original = theme.read_text(encoding="utf-8")
    patched, count = re.subn(
        r'(url\("data:font/woff2;base64,)[A-Za-z0-9+/=]*(")',
        lambda m: m.group(1) + encoded + m.group(2),
        original,
    )
    if not count:
        return "no @font-face data URI to update"
    if patched == original:
        return "already current"
    theme.write_text(patched, encoding="utf-8")
    return "updated"


def build_woff2(source: Path, path: Path, text: str | None = None):
    font = TTFont(source)
    if text:
        subsetter = Subsetter()
        subsetter.populate(text=text + text.upper() + text.lower())
        subsetter.subset(font)
    font.flavor = "woff2"
    font.save(path)
    font.close()
    return path


# --------------------------------------------------------------------------- #
# Specimen
# --------------------------------------------------------------------------- #


def render_wordmark(ttf_path: Path, png_path: Path, text=WORDMARK_TEXT.upper(), size=150, tracking=0.14):
    """Tightly cropped wordmark, for eyeballing the drawing at full scale."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None

    font = ImageFont.truetype(str(ttf_path), size)
    canvas = Image.new("RGB", (size * len(text), size * 3), "#000000")
    draw = ImageDraw.Draw(canvas)
    spacing = size * tracking
    x = size
    for char in text:
        draw.text((x, size), char, font=font, fill="#ffffff")
        x += draw.textlength(char, font=font) + spacing
    box = canvas.convert("L").point(lambda v: 255 if v > 24 else 0).getbbox()
    pad = size // 4
    canvas.crop(
        (max(0, box[0] - pad), max(0, box[1] - pad), box[2] + pad, box[3] + pad)
    ).save(png_path)
    return png_path


def render_specimen(ttf_path: Path, png_path: Path):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None

    lines = [
        ("UNREAL ENGINE VITE", 86, 0.14),
        ("ABCDEFGHIJKLM", 44, 0.10),
        ("NOPQRSTUVWXYZ", 44, 0.10),
        ("0123456789 &@#% .,:;!?()[]", 34, 0.08),
    ]
    width, height = 1400, 520
    image = Image.new("RGB", (width, height), "#000000")
    draw = ImageDraw.Draw(image)
    y = 70
    for text, size, tracking in lines:
        font = ImageFont.truetype(str(ttf_path), size)
        spacing = size * tracking
        total = sum(draw.textlength(ch, font=font) + spacing for ch in text) - spacing
        x = (width - total) / 2
        for char in text:
            draw.text((x, y), char, font=font, fill="#ffffff")
            x += draw.textlength(char, font=font) + spacing
        y += int(size * 1.85)
    image.save(png_path)
    return png_path


# --------------------------------------------------------------------------- #


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    glyphs = normalise(glyph_recipes())
    cmap = character_map()

    ttf = build_ttf(glyphs, cmap, OUTPUT_DIR / "ViteVector-Regular.ttf")
    otf = build_otf(glyphs, cmap, OUTPUT_DIR / "ViteVector-Regular.otf")
    woff2 = build_woff2(ttf, OUTPUT_DIR / "ViteVector-Regular.woff2")
    subset = build_woff2(ttf, OUTPUT_DIR / "ViteVector-Wordmark.woff2", WORDMARK_TEXT)
    specimen = render_specimen(ttf, OUTPUT_DIR / "ViteVector-Specimen.png")
    wordmark = render_wordmark(ttf, OUTPUT_DIR / "ViteVector-Wordmark.png")

    for path in (ttf, otf, woff2, subset, specimen, wordmark):
        if path:
            print(f"{path.name:36} {path.stat().st_size:>8,} bytes")
    print(f"{'theme embed':36} {embed_in_theme(subset):>8}")


if __name__ == "__main__":
    main()
