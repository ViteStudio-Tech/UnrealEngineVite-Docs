"""Build the original Vite Vector display typeface as TTF and OTF.

The glyphs are generated from editable geometric stroke recipes. The font is
intentionally a display face: uppercase letters, numerals, basic punctuation,
and lowercase code points mapped to the uppercase designs.
"""

from __future__ import annotations

import math
from pathlib import Path

from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.ttGlyphPen import TTGlyphPen


UPM = 1000
CAP_HEIGHT = 700
ASCENDER = 800
DESCENDER = -200
STROKE = 34
OUTPUT_DIR = Path(__file__).resolve().parent.parent


def line_shape(a: tuple[float, float], b: tuple[float, float], width: float = STROKE):
    """Return a rectangular outline centered on segment a-b."""
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    if not length:
        return []
    nx, ny = -dy / length * width / 2, dx / length * width / 2
    return [
        (ax + nx, ay + ny),
        (bx + nx, by + ny),
        (bx - nx, by - ny),
        (ax - nx, ay - ny),
    ]


def stroke_path(points: list[tuple[float, float]], width: float = STROKE):
    """Expand an open centerline into one continuous outline."""
    if len(points) < 2:
        return []
    left: list[tuple[float, float]] = []
    right: list[tuple[float, float]] = []
    for index, point in enumerate(points):
        if index == 0:
            tangent = (points[1][0] - point[0], points[1][1] - point[1])
        elif index == len(points) - 1:
            tangent = (point[0] - points[index - 1][0], point[1] - points[index - 1][1])
        else:
            tangent = (
                points[index + 1][0] - points[index - 1][0],
                points[index + 1][1] - points[index - 1][1],
            )
        length = math.hypot(*tangent)
        nx, ny = -tangent[1] / length * width / 2, tangent[0] / length * width / 2
        left.append((point[0] + nx, point[1] + ny))
        right.append((point[0] - nx, point[1] - ny))
    return left + list(reversed(right))


def arc_points(
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    start_degrees: float,
    end_degrees: float,
    count: int = 28,
):
    return [
        (
            cx + rx * math.cos(math.radians(start_degrees + (end_degrees - start_degrees) * i / (count - 1))),
            cy + ry * math.sin(math.radians(start_degrees + (end_degrees - start_degrees) * i / (count - 1))),
        )
        for i in range(count)
    ]


def cubic_points(p0, p1, p2, p3, count=18):
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


def rounded_rect_points(x0, y0, x1, y1, radius, steps=6):
    points = []
    corners = [
        (x1 - radius, y1 - radius, 0, 90),
        (x0 + radius, y1 - radius, 90, 180),
        (x0 + radius, y0 + radius, 180, 270),
        (x1 - radius, y0 + radius, 270, 360),
    ]
    for cx, cy, start, end in corners:
        points.extend(arc_points(cx, cy, radius, radius, start, end, steps)[1 if points else 0 :])
    return points


def ring(x0, y0, x1, y1, radius, thickness=STROKE):
    outer = rounded_rect_points(x0, y0, x1, y1, radius)
    inner = rounded_rect_points(
        x0 + thickness,
        y0 + thickness,
        x1 - thickness,
        y1 - thickness,
        max(1, radius - thickness),
    )
    return [outer, list(reversed(inner))]


def strokes(*segments, width=STROKE):
    return [line_shape(a, b, width) for a, b in segments]


def glyph_recipes():
    """Return {glyph_name: (advance_width, contours)}."""
    g: dict[str, tuple[int, list[list[tuple[float, float]]]]] = {}

    def put(name, width, contours):
        g[name] = (width, [c for c in contours if c])

    # Core uppercase alphabet.
    put("A", 680, strokes(((70, 0), (330, 700)), ((330, 700), (610, 0)), ((175, 270), (500, 270))))
    put(
        "B",
        650,
        strokes(((70, 0), (70, 700)), ((70, 700), (410, 700)), ((70, 350), (410, 350)), ((70, 0), (410, 0)))
        + [
            stroke_path(arc_points(405, 525, 160, 175, 90, -90)),
            stroke_path(arc_points(405, 175, 160, 175, 90, -90)),
        ],
    )
    put("C", 650, [stroke_path(arc_points(330, 350, 270, 350, 45, 315, 36))])
    put(
        "D",
        680,
        strokes(((70, 0), (70, 700)), ((70, 700), (390, 700)), ((70, 0), (390, 0)))
        + [stroke_path(arc_points(390, 350, 210, 350, 90, -90, 34))],
    )
    put("E", 620, strokes(((70, 0), (70, 700)), ((70, 700), (570, 700)), ((70, 350), (455, 350)), ((70, 0), (570, 0))))
    put("F", 610, strokes(((70, 0), (70, 700)), ((70, 700), (570, 700)), ((70, 350), (455, 350))))
    put(
        "G",
        680,
        [stroke_path(arc_points(345, 350, 280, 350, 45, 315, 36))]
        + strokes(((350, 340), (620, 340)), ((605, 340), (605, 115))),
    )
    put("H", 680, strokes(((70, 0), (70, 700)), ((610, 0), (610, 700)), ((70, 350), (610, 350))))
    put("I", 250, strokes(((125, 0), (125, 700))))
    put(
        "J",
        600,
        strokes(((80, 700), (540, 700)), ((540, 700), (540, 185)))
        + [stroke_path(arc_points(305, 185, 235, 185, 0, -180, 24))],
    )
    put("K", 650, strokes(((70, 0), (70, 700)), ((70, 330), (570, 700)), ((70, 330), (600, 0))))
    put("L", 600, strokes(((70, 700), (70, 0)), ((70, 0), (550, 0))))
    put("M", 820, strokes(((60, 0), (60, 700)), ((60, 700), (410, 250)), ((410, 250), (760, 700)), ((760, 700), (760, 0))))
    put("N", 720, strokes(((70, 0), (70, 700)), ((70, 700), (650, 0)), ((650, 0), (650, 700))))
    put("O", 690, ring(60, 0, 630, 700, 125))
    put(
        "P",
        650,
        strokes(((70, 0), (70, 700)), ((70, 700), (405, 700)), ((70, 350), (405, 350)))
        + [stroke_path(arc_points(405, 525, 165, 175, 90, -90))],
    )
    put("Q", 700, ring(60, 0, 630, 700, 125) + strokes(((410, 190), (660, -60))))
    put(
        "R",
        680,
        strokes(((70, 0), (70, 700)), ((70, 700), (405, 700)), ((70, 350), (405, 350)), ((350, 350), (630, 0)))
        + [stroke_path(arc_points(405, 525, 165, 175, 90, -90))],
    )
    s_curve = cubic_points((550, 620), (420, 735), (70, 700), (90, 430), 20)
    s_curve += cubic_points((90, 430), (110, 250), (560, 355), (550, 80), 22)[1:]
    put("S", 650, [stroke_path(s_curve)])
    put("T", 650, strokes(((50, 700), (600, 700)), ((325, 700), (325, 0))))
    u_path = [(70, 700), (70, 180)] + arc_points(330, 180, 260, 180, 180, 360, 26)[1:] + [(590, 700)]
    put("U", 660, [stroke_path(u_path)])
    # The signature double-vector V remains monochrome in standard OpenType.
    put(
        "V",
        680,
        strokes(
            ((55, 700), (330, 0)),
            ((330, 0), (625, 700)),
            ((130, 700), (330, 135)),
            ((330, 135), (550, 700)),
            width=27,
        ),
    )
    put(
        "W",
        840,
        strokes(((50, 700), (205, 0)), ((205, 0), (410, 510)), ((410, 510), (615, 0)), ((615, 0), (790, 700))),
    )
    put("X", 680, strokes(((60, 700), (620, 0)), ((620, 700), (60, 0))))
    put("Y", 680, strokes(((60, 700), (335, 360)), ((620, 700), (335, 360)), ((335, 360), (335, 0))))
    put("Z", 650, strokes(((60, 700), (590, 700)), ((590, 700), (60, 0)), ((60, 0), (590, 0))))

    # Numerals.
    put("zero", 650, ring(60, 0, 590, 700, 125) + strokes(((170, 90), (485, 610)), width=24))
    put("one", 420, strokes(((205, 0), (205, 700)), ((95, 590), (205, 700)), ((90, 0), (330, 0))))
    put(
        "two",
        620,
        [stroke_path(arc_points(310, 525, 240, 175, 160, -20, 22))]
        + strokes(((535, 465), (70, 0)), ((70, 0), (560, 0))),
    )
    put(
        "three",
        620,
        strokes(((80, 700), (375, 700)), ((215, 350), (395, 350)), ((80, 0), (375, 0)))
        + [
            stroke_path(arc_points(375, 525, 160, 175, 90, -90, 18)),
            stroke_path(arc_points(375, 175, 160, 175, 90, -90, 18)),
        ],
    )
    put("four", 650, strokes(((460, 0), (460, 700)), ((460, 700), (70, 230)), ((70, 230), (580, 230))))
    put(
        "five",
        620,
        strokes(((550, 700), (90, 700)), ((90, 700), (90, 370)), ((90, 370), (375, 370)), ((80, 0), (375, 0)))
        + [stroke_path(arc_points(375, 185, 175, 185, 90, -90, 20))],
    )
    put(
        "six",
        640,
        [stroke_path(arc_points(325, 185, 245, 185, 0, 360, 30)), stroke_path(cubic_points((80, 185), (70, 600), (240, 710), (530, 670), 24))],
    )
    put("seven", 620, strokes(((60, 700), (570, 700)), ((570, 700), (170, 0))))
    put(
        "eight",
        640,
        [stroke_path(arc_points(320, 520, 225, 180, 0, 360, 28)), stroke_path(arc_points(320, 175, 245, 175, 0, 360, 28))],
    )
    put(
        "nine",
        640,
        [stroke_path(arc_points(315, 515, 245, 185, 0, 360, 30)), stroke_path(cubic_points((560, 515), (570, 100), (400, -10), (110, 30), 24))],
    )

    # Basic punctuation.
    put("period", 240, [ring(94, 0, 146, 52, 14, 18)[0]])
    put("colon", 240, [ring(94, 450, 146, 502, 14, 18)[0], ring(94, 70, 146, 122, 14, 18)[0]])
    put("slash", 450, strokes(((60, -40), (390, 740))))
    put("plus", 520, strokes(((60, 350), (460, 350)), ((260, 550), (260, 150))))
    put("hyphen", 450, strokes(((70, 300), (380, 300))))
    put("underscore", 570, strokes(((60, -70), (510, -70))))
    put("exclam", 240, strokes(((120, 700), (120, 160))) + [ring(94, 0, 146, 52, 14, 18)[0]])
    put("question", 590, [stroke_path(arc_points(290, 525, 230, 175, 160, -20, 22))] + strokes(((505, 465), (295, 255)), ((295, 255), (295, 160))) + [ring(269, 0, 321, 52, 14, 18)[0]])
    put("parenleft", 330, [stroke_path(arc_points(300, 350, 190, 380, 110, 250, 26))])
    put("parenright", 330, [stroke_path(arc_points(30, 350, 190, 380, -70, 70, 26))])
    put("space", 330, [])
    put(".notdef", 650, ring(70, 0, 580, 700, 40) + strokes(((100, 80), (550, 620)), ((100, 620), (550, 80)), width=20))
    return g


def draw_contours(pen, contours):
    for contour in contours:
        if len(contour) < 3:
            continue
        pen.moveTo(contour[0])
        for point in contour[1:]:
            pen.lineTo(point)
        pen.closePath()


def character_map():
    cmap = {ord(letter): letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    cmap.update({ord(letter.lower()): letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"})
    digit_names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    cmap.update({ord(str(index)): name for index, name in enumerate(digit_names)})
    cmap.update(
        {
            ord(" "): "space",
            ord("."): "period",
            ord(":"): "colon",
            ord("/"): "slash",
            ord("+"): "plus",
            ord("-"): "hyphen",
            ord("_"): "underscore",
            ord("!"): "exclam",
            ord("?"): "question",
            ord("("): "parenleft",
            ord(")"): "parenright",
        }
    )
    return cmap


FEATURES = """
languagesystem DFLT dflt;
feature kern {
    pos A V -45;
    pos A W -35;
    pos A Y -35;
    pos F A -25;
    pos L T -20;
    pos L V -35;
    pos L Y -40;
    pos R T -15;
    pos T A -35;
    pos T E -15;
    pos T O -20;
    pos V A -45;
    pos V E -15;
    pos V I -10;
    pos V T -20;
    pos W A -30;
    pos Y A -40;
    pos Y E -20;
    pos Y O -25;
} kern;
"""


def configure_common(fb: FontBuilder, glyph_order, cmap, metrics):
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=ASCENDER, descent=DESCENDER, lineGap=100)
    fb.setupNameTable(
        {
            "familyName": "Vite Vector",
            "styleName": "Regular",
            "uniqueFontIdentifier": "ViteStudio:Vite Vector Regular:0.1",
            "fullName": "Vite Vector Regular",
            "psName": "ViteVector-Regular",
            "version": "Version 0.1",
            "description": "Original geometric display face for Unreal Engine Vite.",
            "designer": "Vite Studio",
            "manufacturer": "Vite Studio",
            "copyright": "Copyright 2026 Vite Studio. All rights reserved.",
        }
    )
    fb.setupOS2(
        sTypoAscender=ASCENDER,
        sTypoDescender=DESCENDER,
        sTypoLineGap=100,
        usWinAscent=ASCENDER,
        usWinDescent=abs(DESCENDER),
        sxHeight=CAP_HEIGHT,
        sCapHeight=CAP_HEIGHT,
        usWeightClass=300,
        usWidthClass=7,
        fsSelection=0x40,
    )
    fb.setupPost(italicAngle=0, underlinePosition=-110, underlineThickness=24)


def build_ttf(recipes, cmap):
    glyph_order = [".notdef"] + [name for name in recipes if name != ".notdef"]
    metrics = {name: (advance, 0) for name, (advance, _) in recipes.items()}
    glyphs = {}
    for name, (_, contours) in recipes.items():
        pen = TTGlyphPen(None)
        draw_contours(pen, contours)
        glyphs[name] = pen.glyph()

    fb = FontBuilder(UPM, isTTF=True)
    configure_common(fb, glyph_order, cmap, metrics)
    fb.setupGlyf(glyphs)
    fb.setupMaxp()
    fb.setupHead()
    addOpenTypeFeaturesFromString(fb.font, FEATURES)
    fb.setupDummyDSIG()
    path = OUTPUT_DIR / "ViteVector-Regular.ttf"
    fb.save(path)
    return path


def build_otf(recipes, cmap):
    glyph_order = [".notdef"] + [name for name in recipes if name != ".notdef"]
    metrics = {name: (advance, 0) for name, (advance, _) in recipes.items()}
    charstrings = {}
    for name, (advance, contours) in recipes.items():
        pen = T2CharStringPen(advance, None)
        draw_contours(pen, contours)
        charstrings[name] = pen.getCharString()

    fb = FontBuilder(UPM, isTTF=False)
    configure_common(fb, glyph_order, cmap, metrics)
    fb.setupCFF(
        "ViteVector-Regular",
        {
            "FullName": "Vite Vector Regular",
            "FamilyName": "Vite Vector",
            "Weight": "Regular",
            "version": "0.1",
            "Notice": "Copyright 2026 Vite Studio. All rights reserved.",
        },
        charstrings,
        {},
    )
    fb.setupHead()
    addOpenTypeFeaturesFromString(fb.font, FEATURES)
    path = OUTPUT_DIR / "ViteVector-Regular.otf"
    fb.save(path)
    return path


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    recipes = glyph_recipes()
    cmap = character_map()
    ttf = build_ttf(recipes, cmap)
    otf = build_otf(recipes, cmap)
    print(f"Built {ttf}")
    print(f"Built {otf}")


if __name__ == "__main__":
    main()
