"""Generate the vector illustrations used on the Vite Technology site.

Vertis and Hair FX have no captures yet, so their visuals are drawn here:
deterministic (fixed seeds), resolution-independent and small. Run from
anywhere; output goes to ../public/assets/img.

    python ViteTech/tools/make_art.py
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "assets", "img")


def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    print(f"{name}: {len(svg) // 1024} KB")


# --------------------------------------------------------------------------
# Vertis: one surface at three LOD densities, morphing into each other
# --------------------------------------------------------------------------

def icosphere(subdiv):
    t = (1 + 5 ** 0.5) / 2
    verts = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t),
             (0, -1, -t), (0, 1, -t), (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    verts = [normalise(v) for v in verts]
    faces = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4),
             (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8),
             (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    for _ in range(subdiv):
        cache, nf = {}, []

        def mid(a, b):
            key = (min(a, b), max(a, b))
            if key not in cache:
                va, vb = verts[a], verts[b]
                verts.append(normalise(((va[0] + vb[0]) / 2, (va[1] + vb[1]) / 2, (va[2] + vb[2]) / 2)))
                cache[key] = len(verts) - 1
            return cache[key]

        for a, b, c in faces:
            ab, bc, ca = mid(a, b), mid(b, c), mid(c, a)
            nf += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
        faces = nf
    return verts, faces


def normalise(v):
    n = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    return (v[0] / n, v[1] / n, v[2] / n)


def displace(v):
    # A rock-like surface: low-frequency lumps so the silhouette changes
    # visibly between LODs.
    x, y, z = v
    d = 1 + 0.10 * math.sin(3.1 * x + 1.3) * math.cos(2.7 * y) + 0.07 * math.sin(5.3 * z + 0.4) \
        + 0.04 * math.cos(7.9 * x * y + 2.0)
    return (x * d, y * d, z * d)


def rotate(v, ax, ay):
    x, y, z = v
    cy, sy = math.cos(ay), math.sin(ay)
    x, z = x * cy + z * sy, -x * sy + z * cy
    cx, sx = math.cos(ax), math.sin(ax)
    y, z = y * cx - z * sx, y * sx + z * cx
    return (x, y, z)


def mesh_svg(subdiv, cx, cy, r, stroke, opacity, fill_alpha):
    verts, faces = icosphere(subdiv)
    pts = [rotate(displace(v), -0.35, 0.6) for v in verts]
    light = normalise((-0.5, -0.7, 0.6))
    polys = []
    for a, b, c in faces:
        pa, pb, pc = pts[a], pts[b], pts[c]
        ux, uy, uz = pb[0] - pa[0], pb[1] - pa[1], pb[2] - pa[2]
        vx, vy, vz = pc[0] - pa[0], pc[1] - pa[1], pc[2] - pa[2]
        nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
        if nz <= 0:
            continue
        n = normalise((nx, ny, nz))
        shade = max(0.0, n[0] * light[0] + n[1] * light[1] + n[2] * light[2])
        depth = (pa[2] + pb[2] + pc[2]) / 3
        coords = " ".join(f"{cx + p[0] * r:.1f},{cy + p[1] * r:.1f}" for p in (pa, pb, pc))
        polys.append((depth, coords, shade))
    polys.sort()
    out = []
    for _, coords, shade in polys:
        a = fill_alpha * (0.25 + 0.75 * shade)
        out.append(f'<polygon points="{coords}" fill="rgba(47,224,192,{a:.3f})" stroke="{stroke}" '
                   f'stroke-opacity="{opacity}" stroke-width="0.7" stroke-linejoin="round"/>')
    return "\n".join(out)


def vertis():
    w, h = 1600, 900
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
             f'aria-labelledby="t d"><title id="t">Vertis LOD transition</title>'
             f'<desc id="d">One surface shown at three levels of detail, from dense to coarse, '
             f'connected by morph arrows to show continuous, pop-free transitions.</desc>',
             '<defs><radialGradient id="bg" cx="50%" cy="45%" r="70%">'
             '<stop offset="0" stop-color="#0d1d1c"/><stop offset="1" stop-color="#050607"/></radialGradient>'
             '<linearGradient id="arrow" x1="0" x2="1"><stop offset="0" stop-color="#2fe0c0" stop-opacity="0"/>'
             '<stop offset="1" stop-color="#2fe0c0"/></linearGradient>'
             '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
             '<path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".035"/></pattern></defs>',
             f'<rect width="{w}" height="{h}" fill="url(#bg)"/><rect width="{w}" height="{h}" fill="url(#grid)"/>']
    lods = [(3, 330, "#9ff7e7", 0.55, 0.85, "LOD 0"), (2, 800, "#6cecd4", 0.7, 0.75, "LOD 1"),
            (1, 1270, "#2fe0c0", 0.9, 0.65, "LOD 2")]
    for subdiv, cx, stroke, op, fa, label in lods:
        parts.append(mesh_svg(subdiv, cx, 430, 190, stroke, op, fa * 0.5))
        parts.append(f'<text x="{cx}" y="720" fill="#c3cbd1" font-family="JetBrains Mono, Consolas, monospace" '
                     f'font-size="22" text-anchor="middle" letter-spacing="3">{label}</text>')
    for x0 in (545, 1015):
        parts.append(f'<path d="M{x0} 430 h40" stroke="url(#arrow)" stroke-width="3"/>'
                     f'<path d="M{x0 + 40} 422 l12 8 -12 8" fill="none" stroke="#2fe0c0" stroke-width="3" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>')
    parts.append('<text x="800" y="800" fill="#8e99a1" font-family="Inter, Segoe UI, sans-serif" font-size="22" '
                 'text-anchor="middle">Continuous transitions between baked levels of detail</text></svg>')
    write("vertis-lod.svg", "\n".join(parts))


# --------------------------------------------------------------------------
# Hair FX: flowing strands with anisotropic highlight bands
# --------------------------------------------------------------------------

def hairfx():
    rnd = random.Random(7)
    w, h = 1600, 900
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
             f'aria-labelledby="t d"><title id="t">Hair FX strands</title>'
             f'<desc id="d">Hundreds of flowing hair strands with a bright primary highlight band and a '
             f'warmer secondary band, illustrating strand-based hair shading.</desc>',
             '<defs><radialGradient id="hbg" cx="62%" cy="40%" r="75%">'
             '<stop offset="0" stop-color="#1c1610"/><stop offset="1" stop-color="#050607"/></radialGradient>'
             '<linearGradient id="strand" x1="0" y1="0" x2="1" y2="1">'
             '<stop offset="0" stop-color="#3b2a1a"/><stop offset=".38" stop-color="#7a5a36"/>'
             '<stop offset=".46" stop-color="#f4dcab"/><stop offset=".52" stop-color="#8d6a42"/>'
             '<stop offset=".68" stop-color="#c79a5f"/><stop offset=".74" stop-color="#5c4128"/>'
             '<stop offset="1" stop-color="#22170e"/></linearGradient></defs>',
             f'<clipPath id="frame"><rect width="{w}" height="{h}"/></clipPath>',
             f'<rect width="{w}" height="{h}" fill="url(#hbg)"/><g clip-path="url(#frame)">']
    for i in range(420):
        t = i / 420
        x0 = -100 + t * 1150 + rnd.uniform(-30, 30)
        y0 = -60 + rnd.uniform(-40, 40)
        sway = 260 + 160 * math.sin(t * 5.2)
        x1, y1 = x0 + sway * 0.6 + rnd.uniform(-40, 40), 260 + rnd.uniform(-30, 30)
        x2, y2 = x0 + sway * 1.4 + rnd.uniform(-60, 60), 600 + rnd.uniform(-40, 40)
        x3, y3 = x0 + sway * 1.9 + rnd.uniform(-90, 90), 960 + rnd.uniform(-30, 60)
        width = rnd.uniform(0.6, 2.1)
        alpha = rnd.uniform(0.35, 0.95)
        parts.append(f'<path d="M{x0:.1f} {y0:.1f} C{x1:.1f} {y1:.1f} {x2:.1f} {y2:.1f} {x3:.1f} {y3:.1f}" '
                     f'fill="none" stroke="url(#strand)" stroke-width="{width:.2f}" stroke-opacity="{alpha:.2f}" '
                     f'stroke-linecap="round"/>')
    # A few stray flyaway strands catch the light.
    for _ in range(18):
        x0, y0 = rnd.uniform(700, 1300), rnd.uniform(80, 500)
        parts.append(f'<path d="M{x0:.1f} {y0:.1f} q{rnd.uniform(60, 160):.1f} {rnd.uniform(-60, 60):.1f} '
                     f'{rnd.uniform(160, 320):.1f} {rnd.uniform(-20, 120):.1f}" fill="none" stroke="#f6e3bd" '
                     f'stroke-width=".7" stroke-opacity=".55" stroke-linecap="round"/>')
    parts.append("</g></svg>")
    write("hairfx-strands.svg", "\n".join(parts))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    vertis()
    hairfx()
