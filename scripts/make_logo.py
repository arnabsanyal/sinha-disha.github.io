#!/usr/bin/env python3
"""
Generate the site logo and favicon SVGs from exact geometry.

The mark is a "D" for Disha, drawn as a band that holds water: inside the D
sits a ripple and a body of water, a nod to her work on urban flooding and
coastal wetlands. Every band (the D, the ripple) is T units thick and every
gap between parts is G units wide, so the mark stays crisp at any size.
Edit PALETTES and re-run to recolour it.

Usage: python3 scripts/make_logo.py
"""

import math
import os

# Geometry (top-left of the D at the origin, y pointing down)
H = 300.0            # height of the D
R = H / 2            # radius of the bowl
L = 112.0            # x where the straight top/bottom edges meet the bowl
T = 27.0             # band thickness
G = 13.5             # gap between parts
INNER = T + G        # offset of the water's container from the outer edge

RIPPLE_Y = 112.0     # centre line of the ripple band (top edge = RIPPLE_Y - T/2)
WATER_Y = RIPPLE_Y + T + G   # mean water level, one gap below the ripple
AMP = 9.0            # wave amplitude
WAVELEN = 120.0      # wave length
PHASE = 0.0
STEP = 4.0           # sampling step along x for the wave curves

PAD = 12.0           # padding around the mark in logo.svg

# (main, accent) colours for each file
PALETTES = {
    "logo.svg": ("#effcf9", "#2dd4bf"),       # for dark backgrounds
    "logo-dark.svg": ("#073b3a", "#0d9488"),  # for light backgrounds
}
FAVICON = {"file": "favicon.svg", "tile": "#0b3b3a", "colors": PALETTES["logo.svg"]}
TITLE = "Disha Sinha"
OUT_DIR = os.path.join("assets", "img")


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def d_shape(d):
    """Closed path of the D outline inset by d (clockwise)."""
    r = R - d
    return (f"M{fmt(d)} {fmt(d)}H{fmt(L)}"
            f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(L)} {fmt(H - d)}"
            f"H{fmt(d)}Z")


def wave_y(x, base):
    return base + AMP * math.sin(2 * math.pi * x / WAVELEN + PHASE)


def wave_points(base, x0, x1, reverse=False):
    n = int(math.ceil((x1 - x0) / STEP))
    xs = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    if reverse:
        xs.reverse()
    return [(x, wave_y(x, base)) for x in xs]


def poly(points):
    return "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}"
                   for i, (x, y) in enumerate(points))


def mark(main, accent, clip_id):
    x0, x1 = 0.0, L + R
    # Ripple: a wavy band of thickness T
    top = wave_points(RIPPLE_Y - T / 2, x0, x1)
    bot = wave_points(RIPPLE_Y + T / 2, x0, x1, reverse=True)
    ripple = poly(top) + poly(bot)[0].replace("M", "L") + poly(bot)[1:] + "Z"
    # Water: everything below the water line
    surf = wave_points(WATER_Y, x0, x1)
    water = poly(surf) + f"L{fmt(x1)} {fmt(H)}L{fmt(x0)} {fmt(H)}Z"
    return (
        f'<defs><clipPath id="{clip_id}"><path d="{d_shape(INNER)}"/></clipPath></defs>'
        f'<path fill="{main}" fill-rule="evenodd" d="{d_shape(0)}{d_shape(T)}"/>'
        f'<g fill="{accent}" clip-path="url(#{clip_id})">'
        f'<path d="{ripple}"/><path d="{water}"/></g>'
    )


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text + "\n")
    print("wrote", path)


def main():
    w, h = L + R, H
    for name, (main_c, accent) in PALETTES.items():
        vb = f"{fmt(-PAD)} {fmt(-PAD)} {fmt(w + 2 * PAD)} {fmt(h + 2 * PAD)}"
        cid = "w-" + name.split(".")[0]
        write(os.path.join(OUT_DIR, name),
              f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img">'
              f'<title>{TITLE}</title>{mark(main_c, accent, cid)}</svg>')

    # Favicon: the mark centred on a rounded tile
    size = 512.0
    scale = 0.62 * size / h
    tx = (size - w * scale) / 2
    ty = (size - h * scale) / 2
    main_c, accent = FAVICON["colors"]
    write(os.path.join(OUT_DIR, FAVICON["file"]),
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img">'
          f'<title>{TITLE}</title>'
          f'<rect width="512" height="512" rx="112.64" fill="{FAVICON["tile"]}"/>'
          f'<g transform="translate({fmt(tx)} {fmt(ty)}) scale({scale:.5f})">'
          f'{mark(main_c, accent, "w-fav")}</g></svg>')


if __name__ == "__main__":
    main()
