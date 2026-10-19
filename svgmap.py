# -*- coding: utf-8 -*-
import math, os, sys, subprocess, random
import numpy as np
from shapely.geometry import shape, Point
from shapely.ops import unary_union
from shapely.prepared import prep
from svgbase import W, H, S, P, d_line, d_poly, d_ring, clip, simplify
import render as R
from render import D, load, poly_parts, line_parts, LON0, LAT0, LON1, LAT1

PAPER   = "#FBF1DC"
PAPER2  = "#F2E2C3"
SEA     = "#86CBD6"
SEA_D   = "#4C9DAE"
SEA_L   = "#DDF1F2"
INK     = "#25403E"
INK_S   = "#3E5C58"
GREEN   = "#C9DFA7"
GREEN_D = "#6E9455"
FARM    = "#EBE2B4"
SAND    = "#F2DAA8"
ROAD    = "#FFFDF7"
ROAD_C  = "#D6BD94"
ACC     = "#C9452F"
ACC_D   = "#9E3222"
GOLD    = "#E8A23A"
TEAL    = "#2B6C6A"
URBAN   = "#F3DFC0"
STONE   = "#E9DFCB"
STONE_D = "#B9A98C"
GREY    = "#5A6A67"

OCEAN = D["ocean"]
OCEAN_PREP = prep(OCEAN)
SEA_BOUNDS = OCEAN.bounds

out = []
def A(s): out.append(s)

def esc(t):
    return (t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

# ---------------------------------------------------------------- defs
DEFS = f"""
<defs>
  <filter id="rough" x="-3%" y="-3%" width="106%" height="106%">
    <feTurbulence type="fractalNoise" baseFrequency="0.013" numOctaves="3" seed="9" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="rough2" x="-3%" y="-3%" width="106%" height="106%">
    <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="3" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="1.6" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="4" seed="11" result="n"/>
    <feColorMatrix in="n" type="saturate" values="0"/>
    <feComponentTransfer><feFuncA type="linear" slope="0.5"/></feComponentTransfer>
    <feBlend in="SourceGraphic" in2="n" mode="multiply"/>
  </filter>
  <radialGradient id="vign" cx="50%" cy="45%" r="72%">
    <stop offset="55%" stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#5a3d1e" stop-opacity="0.16"/>
  </radialGradient>
  <pattern id="waves" width="46" height="30" patternUnits="userSpaceOnUse">
    <path d="M4,18 q7,-7 14,0 t14,0" fill="none" stroke="{SEA_L}" stroke-width="1.5" stroke-linecap="round" opacity="0.65"/>
    <path d="M26,8 q6,-5 12,0" fill="none" stroke="{SEA_L}" stroke-width="1.2" stroke-linecap="round" opacity="0.45"/>
  </pattern>
  <clipPath id="frameClip"><rect x="0" y="0" width="{W}" height="{H}" rx="0"/></clipPath>
</defs>
"""

# ---------------------------------------------------------------- paper
def paper():
    A(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    rng = random.Random(4)
    for _ in range(26):
        cx, cy = rng.uniform(0, W), rng.uniform(0, H)
        rx, ry = rng.uniform(70, 180), rng.uniform(45, 110)
        A(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{rng.choice(["#F7E9CD","#F5E3C1","#FAEFD8"])}" opacity="0.35"/>')

# ---------------------------------------------------------------- sea
def sea():
    p = d_poly(OCEAN.buffer(0.0008).buffer(-0.0008), 1)
    A(f'<path d="{p}" fill="{SEA_L}" stroke="{SEA_L}" stroke-width="11" stroke-linejoin="round"/>')
    A(f'<path d="{p}" fill="{SEA}" stroke="none"/>')
    A(f'<path d="{p}" fill="none" stroke="{SEA_D}" stroke-width="1.1" opacity="0.22"/>')
    A(f'<path d="{p}" fill="none" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>')


def lakes():
    parts = []
    for q in poly_parts(D["lakes"]):
        if q.area * 111 * 99 < 0.03: continue
        parts.append(d_poly(q, 1))
    if not parts: return
    d = " ".join(parts)
    A(f'<path d="{d}" fill="{SEA}" stroke="{INK}" stroke-width="1.3" fill-rule="evenodd" stroke-linejoin="round"/>')

def rivers():
    for g in D["rivers"]:
        for ln in line_parts(g):
            if ln.length < 0.018: continue
            d = d_line(ln, 1)
            if d:
                A(f'<path d="{d}" fill="none" stroke="{INK_S}" stroke-width="3.0" stroke-linecap="round"/>')
                A(f'<path d="{d}" fill="none" stroke="{SEA}" stroke-width="1.7" stroke-linecap="round"/>')

# ---------------------------------------------------------------- land cover
def landcover():
    woods = [q for q in poly_parts(D["woods"]) if q.area*111*99 > 0.7]
    d = " ".join(d_poly(q, 1) for q in woods)
    if d:
        A(f'<path d="{d}" fill="{GREEN}" fill-opacity="0.7" stroke="{GREEN_D}" stroke-width="0.8" stroke-opacity="0.5" fill-rule="evenodd" stroke-linejoin="round"/>')
    farms = [q for q in poly_parts(D["farm"]) if q.area*111*99 > 0.5]
    d = " ".join(d_poly(q, 1) for q in farms)
    if d:
        A(f'<path d="{d}" fill="{FARM}" fill-opacity="0.75" stroke="none" fill-rule="evenodd"/>')
    sands = list(poly_parts(D["sand"]))
    d = " ".join(d_poly(q, 1) for q in sands)
    if d:
        A(f'<path d="{d}" fill="{SAND}" fill-opacity="0.9" stroke="none" fill-rule="evenodd"/>')

def urban():
    parts = [q for q in poly_parts(D["res"]) if q.area*111*99 > 0.06]
    d = " ".join(d_poly(q, 1) for q in parts)
    if d:
        A(f'<path d="{d}" fill="{URBAN}" fill-opacity="0.85" stroke="#E2C69A" stroke-width="0.7" fill-rule="evenodd" stroke-linejoin="round"/>')

# ---------------------------------------------------------------- roads
RS = [("motorway", 6.2, 2.3), ("trunk", 5.6, 2.0), ("primary", 4.8, 1.75),
      ("secondary", 3.6, 1.25), ("tertiary", 2.6, 0.9)]

RS = [("motorway", 7.6, 4.6, "#F2BE74", "#CE8B45"),
      ("trunk", 6.4, 3.8, "#F7CE90", "#D9A05C"),
      ("primary", 5.2, 1.9, "#FFF9E6", "#D6B78C"),
      ("secondary", 3.8, 1.2, "#FFFDF7", "#DCC5A2"),
      ("tertiary", 2.6, 0.85, "#FFFDF7", "#E2CFAF")]

LAND_ONLY = OCEAN.buffer(0.0006)

def roads():
    for c, cw, fw, fill, casing in RS:
        ds = []
        for g in D["roads"].get(c, []):
            try: g = g.difference(LAND_ONLY)
            except Exception: pass
            for ln in line_parts(g):
                d = d_line(ln, 1)
                if d: ds.append(d)
        if not ds: continue
        d = " ".join(ds)
        A(f'<path d="{d}" fill="none" stroke="{casing}" stroke-width="{cw}" stroke-linecap="round" stroke-linejoin="round"/>')
        A(f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{fw}" stroke-linecap="round" stroke-linejoin="round"/>')


def rail():
    ds = [d_line(ln, 1) for g in D["roads"].get("rail", []) for ln in line_parts(g)]
    d = " ".join(x for x in ds if x)
    if not d: return
    A(f'<path d="{d}" fill="none" stroke="{GREY}" stroke-width="2.2" stroke-linecap="butt"/>')
    A(f'<path d="{d}" fill="none" stroke="{PAPER}" stroke-width="1.0" stroke-dasharray="3.5 3.5"/>')

# ---------------------------------------------------------------- labels
def label(x, y, t, size=13, color=INK, weight=600, anchor="middle", halo=3.2,
          spacing=0.5, italic=False, opacity=1, rotate=None):
    tr = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate else ""
    it = ' font-style="italic"' if italic else ""
    s = (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" font-weight="{weight}" '
         f'text-anchor="{anchor}" letter-spacing="{spacing}" stroke="{PAPER}" stroke-width="{halo}" '
         f'paint-order="stroke fill" stroke-linejoin="round" opacity="{opacity}"{it}{tr}>{esc(t)}</text>')
    A(s)
    return s

TOWNS = [
    ("福鼎市区", 120.2115, 27.330, 22, INK, "middle", 0, 0),
    ("白琳镇",   120.1712, 27.1830, 13, INK, "start", 30, 20),
    ("点头镇",   120.1757, 27.2365, 13, INK, "middle", 0, -12),
    ("沙埕镇",   120.4166, 27.1665, 13, INK, "middle", 0, -12),
    ("前岐镇",   120.3184, 27.3127, 12, INK_S, "middle", 0, -10),
    ("店下镇",   120.3243, 27.1606, 12, INK_S, "middle", 0, 16),
    ("磻溪镇",   120.1131, 27.1557, 11, INK_S, "middle", 0, 14),
    ("管阳镇",   120.0293, 27.2558, 11, INK_S, "middle", 0, 14),
    ("贯岭镇",   120.2279, 27.3925, 11, INK_S, "middle", 0, -10),
    ("叠石乡",   120.1046, 27.3936, 10, INK_S, "middle", 0, -8),
]

def towns():
    for name, lon, lat, size, col, anchor, dx, dy in TOWNS:
        x, y = P(lon, lat)
        x += dx; y += dy
        if name == "福鼎市区":
            A(f'<rect x="{x-70:.1f}" y="{y-26:.1f}" width="140" height="46" rx="23" fill="{PAPER}" '
              f'stroke="{INK}" stroke-width="1.5" opacity="0.96"/>')
            label(x, y-4, name, size=19, color=INK, anchor="middle")
            label(x, y+13, "桐山溪 · 福鼎肉片", size=8.5, color=TEAL, anchor="middle")
            continue
        A(f'<circle cx="{x:.1f}" cy="{y-4:.1f}" r="2.6" fill="{ACC}" stroke="{PAPER}" stroke-width="1.1"/>')
        label(x, y, name, size=size, color=col, anchor="middle")

# ---------------------------------------------------------------- title/frame etc (placeholder)
def title():
    x, y = 62, 96
    A(f'<g id="title">')
    A(f'<path d="M40,40 h360 a14,14 0 0 1 14,14 v96 a14,14 0 0 1 -14,14 h-360 a14,14 0 0 1 -14,-14 v-96 a14,14 0 0 1 14,-14z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4" opacity="0.96"/>')
    label(70, 88, "福鼎", 52, INK, "start", 0, 2)
    label(175, 88, "山海茶旅图", 30, INK, "start", 0, 2)
    label(72, 116, "FUDING  ·  A HAND-DRAWN TOUR MAP", 9, INK_S, "start", 2)
    A('</g>')

def frame():
    A(f'<rect x="12" y="12" width="{W-24}" height="{H-24}" fill="none" stroke="{INK}" stroke-width="3"/>')
    A(f'<rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="{GOLD}" stroke-width="1.2" opacity="0.8"/>')

# ---------------------------------------------------------------- build

def notes():
    g = []
    X, Y = P(120.2115, 27.330)
    X, Y = P(120.1757, 27.2365)
    label(X, Y+22, "白茶原产地", 8.8, TEAL, "middle", 0, 2.4)
    X, Y = P(120.4166, 27.1665)
    label(X, Y+20, "避风良港 · 海鲜", 8.6, TEAL, "middle", 0, 2.4)
    # 太姥山题签
    X, Y = P(120.1830, 27.1246)
    g.append(f'<rect x="{X-52:.1f}" y="{Y+22:.1f}" width="30" height="17" rx="4" fill="{GOLD}" stroke="{INK}" stroke-width="1.2"/>')
    g.append(f'<text x="{X-37:.1f}" y="{Y+34.5:.1f}" font-size="10" font-weight="700" fill="#3A2A12" text-anchor="middle">5A</text>')
    label(X+12, Y+35, "太姥山", 23, INK, "start", 0, 1.5)
    label(X+13, Y+53, "海上仙都 · 九鲤湖 · 国兴寺", 8.8, TEAL, "start", 0, 2)
    # 海湾与海面
    g.append(f'<text x="1004" y="614" font-size="15" fill="{TEAL}" text-anchor="middle" font-style="italic" '
             f'letter-spacing="5" opacity="0.85" transform="rotate(14 1004 614)" stroke="{SEA_L}" stroke-width="3" paint-order="stroke fill">沙埕港</text>')
    # 嵛山岛指示
    g.append(f'<g opacity="0.9"><text x="1440" y="806" font-size="9.5" fill="{INK_S}" text-anchor="end" '
             f'stroke="{PAPER}" stroke-width="3" paint-order="stroke fill">嵛山岛</text>'
             f'<text x="1440" y="820" font-size="8" fill="{TEAL}" text-anchor="end" stroke="{PAPER}" stroke-width="2.6" paint-order="stroke fill">→ 18 km</text></g>')
    return "".join(g)

def build(path="output/fuding-map.svg", html="output/fuding-map.html"):
    del out[:]
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    A(DEFS)
    A(f'<defs><filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>'
      f'<clipPath id="insetClip"><circle cx="{INS_CX}" cy="{INS_CY}" r="{INS_R}"/></clipPath>'
      f'<clipPath id="mapClip"><rect x="26" y="26" width="{W-52}" height="{H-52}"/></clipPath></defs>')
    paper()
    A('<g clip-path="url(#mapClip)">')
    A('<g filter="url(#rough)">')
    sea(); lakes(); landcover(); urban(); roads(); rail(); rivers()
    A('</g>')
    A('<g filter="url(#rough2)">')
    A(mountains()); A(trees()); A(settlements()); A(sea_deco())
    A('</g>')
    A(sky())
    towns()
    A(notes())
    A(shop_marker())
    A('</g>')
    A(leader())
    A(inset())
    A(title_block())
    A(deco.compass(1408, 128, 38))
    A(legend())
    A(scalebar())
    frame()
    A(f'<rect width="{W}" height="{H}" fill="url(#vign)" pointer-events="none"/>')
    A('</svg>')
    svg = "\n".join(out)
    open(path, "w").write(svg)
    html_doc = f"""<!doctype html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;padding:0;background:#FBF1DC;}} svg{{display:block}}</style></head>
<body>{svg}</body></html>"""
    open(html, "w").write(html_doc)
    return path, html


# ================================================================ decorations
import deco
import random as _rnd

def _in_sea_xy(x, y):
    lon = LON0 + x / S / (111.32 * R.KX)
    lat = LAT1 - y / S / 110.57
    return OCEAN_PREP.contains(Point(lon, lat))

def settlements():
    towns = [
        (120.2115, 27.328, 40, 54, 1.0),   # 福鼎市区
        (120.1712, 27.1830, 22, 8, 0.9),   # 白琳
        (120.1757, 27.2365, 20, 7, 0.9),   # 点头
        (120.4166, 27.1665, 30, 9, 0.95),  # 沙埕
        (120.3184, 27.3127, 26, 7, 0.9),   # 前岐
        (120.3243, 27.1606, 24, 6, 0.85),  # 店下
        (120.1131, 27.1557, 20, 4, 0.8),   # 磻溪
        (120.0293, 27.2558, 18, 4, 0.8),   # 管阳
        (120.2279, 27.3925, 18, 4, 0.8),   # 贯岭
        (120.1046, 27.3936, 16, 3, 0.75),  # 叠石
    ]
    g = []
    rng = _rnd.Random(21)
    for lon, lat, rad, n, s in towns:
        cx, cy = P(lon, lat)
        for i in range(n):
            a = rng.uniform(0, math.tau); rr = rng.uniform(4, rad)
            x, y = cx + math.cos(a)*rr, cy + math.sin(a)*rr*0.72
            if _in_sea_xy(x, y): continue
            if abs(x-cx) < 6 and abs(y-cy) < 6 and i < 2: continue
            g.append(deco.house(x, y, s*rng.uniform(.75,1.05), rng.choice([0,0,90,8,-8]),
                                roof=rng.choice(["#E9B98D","#DFA176","#E7C08B","#CFA07A"])))
    return "".join(g)

def mountains():
    g = []
    g.append(deco.ridge(*P(120.060, 27.225), w=250, h=62, n=5, seed=2))
    g.append(deco.ridge(*P(120.120, 27.100), w=220, h=52, n=4, seed=5))
    g.append(deco.ridge(*P(120.035, 27.130), w=200, h=46, n=4, seed=7))
    g.append(deco.ridge(*P(120.150, 27.398), w=240, h=48, n=5, seed=9))
    g.append(deco.taimu(*P(120.1830, 27.1246), s=0.95, seed=8))
    return "".join(g)


def trees():
    g = []
    rng = _rnd.Random(33)
    woods = [q for q in poly_parts(D["woods"]) if q.area*111*99 > 1.2]
    n = 0
    for q in woods:
        minx, miny, maxx, maxy = q.bounds
        for _ in range(14):
            lon = rng.uniform(minx, maxx); lat = rng.uniform(miny, maxy)
            if not q.contains(Point(lon, lat)): continue
            x, y = P(lon, lat)
            if x < 30 or x > W-30 or y < 30 or y > H-30: continue
            if abs(x-589) < 60 and abs(y-737) < 60: continue
            g.append(deco.pine(x, y, rng.uniform(.55,.85), seed=n) if n % 3 else deco.tree(x, y, rng.uniform(.55,.8)))
            n += 1
            if n > 90: break
        if n > 90: break
    return "".join(g)

def tea_fields():
    g = []
    for lon, lat, w in [(120.155, 27.245, 92), (120.147, 27.222, 80), (120.205, 27.205, 70),
                        (120.120, 27.175, 78), (120.060, 27.230, 70)]:
        x, y = P(lon, lat)
        g.append(deco.tea_rows(x, y, w=w, rows=4, s=0.95))
    return "".join(g)

def sea_deco():
    g = []
    rng = _rnd.Random(12)
    # 波浪
    placed = 0
    for _ in range(400):
        x, y = rng.uniform(760, 1480), rng.uniform(300, 1000)
        if not _in_sea_xy(x, y): continue
        g.append(deco.wave(x, y, rng.uniform(.8,1.4), op=rng.uniform(.5,.9)))
        placed += 1
        if placed >= 46: break
    # 渔船
    for lon, lat, s, flip in [(120.395, 27.262, 1.05, False), (120.352, 27.196, .9, True),
                              (120.455, 27.170, 1.0, False), (120.300, 27.150, .8, True)]:
        x, y = P(lon, lat)
        if _in_sea_xy(x, y): g.append(deco.boat(x, y, s, flip=flip))
    # 鱼
    for lon, lat, s, flip in [(120.430, 27.235, 1.0, False), (120.395, 27.120, .9, True)]:
        x, y = P(lon, lat)
        if _in_sea_xy(x, y): g.append(deco.fish(x, y, s, flip=flip))
    # 海鸥
    for x, y, s in [(880, 470, .9), (915, 495, .75), (850, 505, .65), (1250, 430, .8)]:
        g.append(deco.gull(x, y, s))
    # 灯塔（沙埕口）
    x, y = P(120.448, 27.197)
    g.append(deco.lighthouse(x, y, 1.0))
    return "".join(g)

def sky():
    g = []
    g.append(deco.sun(1155, 92, 24))
    g.append(deco.cloud(1000, 150, 1.15))
    g.append(deco.cloud(330, 236, .85))
    g.append(deco.cloud(1330, 470, .75))
    g.append(deco.cloud(120, 480, .8))
    return "".join(g)

def legend():
    x, y, w, h = 1108, 852, 350, 168
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{PAPER}" '
         f'stroke="{INK}" stroke-width="2" opacity="0.97"/>',
         f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="{h-12}" rx="8" fill="none" '
         f'stroke="{GOLD}" stroke-width="0.9" opacity="0.7"/>',
         f'<text x="{x+22}" y="{y+30}" font-size="13" font-weight="700" fill="{INK}" letter-spacing="2">图 例  LEGEND</text>']
    items = [
        ("pin", "合作商铺 · 同顺泰老茶馆"),
        ("peak", "太姥山景区（5A）"),
        ("tea", "白茶原产地"),
        ("boat", "渔港 · 海岛"),
        ("rail", "温福铁路 / 车站"),
    ]
    for i, (kind, text) in enumerate(items):
        iy = y + 54 + i*22
        if kind == "pin":
            g.append(f'<path d="M{x+24},{iy-12} a7,7 0 1 1 0.1,0 L{x+24},{iy+1} Z" fill="{ACC}" stroke="{INK}" stroke-width="1"/>')
        elif kind == "peak":
            g.append(f'<path d="M{x+15},{iy} L{x+24},{iy-14} L{x+33},{iy} Z" fill="{STONE}" stroke="{INK}" stroke-width="1"/>')
        elif kind == "tea":
            g.append(deco.tea_leaf(x+24, iy-5, .55, 0))
        elif kind == "boat":
            g.append(f'<path d="M{x+15},{iy} q9,5 18,0 l-3,4 q-6,3 -12,0 Z" fill="{ACC}" stroke="{INK}" stroke-width="1"/>')
        else:
            g.append(f'<line x1="{x+14}" y1="{iy-4}" x2="{x+34}" y2="{iy-4}" stroke="{GREY}" stroke-width="2.4"/>')
            g.append(f'<line x1="{x+14}" y1="{iy-4}" x2="{x+34}" y2="{iy-4}" stroke="{PAPER}" stroke-width="1" stroke-dasharray="3 3"/>')
        g.append(f'<text x="{x+48}" y="{iy}" font-size="11.5" fill="{INK_S}">{esc(text)}</text>')
    return "".join(g)

def scalebar():
    x0, y0, km = 390, 992, 10
    px = km * S
    g = [f'<line x1="{x0}" y1="{y0}" x2="{x0+px}" y2="{y0}" stroke="{INK}" stroke-width="2"/>']
    for i in range(km+1):
        xx = x0 + i*S
        hh = 6 if i % 5 == 0 else 3
        g.append(f'<line x1="{xx:.1f}" y1="{y0-hh}" x2="{xx:.1f}" y2="{y0+hh}" stroke="{INK}" stroke-width="1.2"/>')
    for xx, t in [(x0,"0"), (x0+px/2,"5 km"), (x0+px,"10 km")]:
        g.append(f'<text x="{xx:.1f}" y="{y0+18}" font-size="10" fill="{INK_S}" text-anchor="middle" stroke="{PAPER}" stroke-width="3" paint-order="stroke fill">{t}</text>')
    return "".join(g)


SHOP_LON, SHOP_LAT = 120.163244, 27.181777
SHOP_X, SHOP_Y = P(SHOP_LON, SHOP_LAT)

def pin(x, y, s=1.0, col=ACC):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round">'
            f'<path d="M0,0 C-15,-17 -21,-27 -21,-37 A21,21 0 1 1 21,-37 C21,-27 15,-17 0,0 Z" fill="{col}"/>'
            f'<circle cx="0" cy="-37" r="14.5" fill="#FFF7E6" stroke-width="1.6"/>'
            f'<path d="M0,-29 C-6,-33 -6,-41 0,-46 C6,-41 6,-33 0,-29 Z" fill="#7FA33E" stroke-width="1"/>'
            f'<path d="M0,-30 L0,-45" stroke="#3E5A1E" stroke-width="0.9"/>'
            f'</g>')


def shop_marker():
    x, y = SHOP_X, SHOP_Y
    g = ['<g id="shop-marker">']
    g.append(f'<ellipse cx="{x:.1f}" cy="{y+3:.1f}" rx="17" ry="5" fill="#8a5a3a" opacity="0.18"/>')
    for rr in (30, 43):
        g.append(f'<circle cx="{x:.1f}" cy="{y-8:.1f}" r="{rr}" fill="none" stroke="{GOLD}" '
                 f'stroke-width="1.3" stroke-dasharray="4 6" opacity="0.45"/>')
    g.append(pin(x, y, 1.15))
    tw = 150
    top = y - 78
    g.append(f'<g transform="translate({x:.1f},{top:.1f})">'
             f'<path d="M{-tw/2},0 h{tw} a7,7 0 0 1 7,7 v15 a7,7 0 0 1 -7,7 h{-tw/2+14} l-14,9 l-12,-9 h{-tw/2+12} a7,7 0 0 1 -7,-7 v-15 a7,7 0 0 1 7,-7 z" '
             f'fill="{ACC}" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>'
             f'<text x="0" y="20" font-size="14" font-weight="700" fill="#FFF8E8" '
             f'text-anchor="middle" letter-spacing="1">同顺泰老茶馆</text>'
             f'</g>')
    g.append('</g>')
    return "".join(g)


INS_CX, INS_CY, INS_R = 218, 818, 136
INS_SCALE = 330.0

def PI(lon, lat):
    return (INS_CX + (lon - SHOP_LON) * 111.32 * R.KX * INS_SCALE,
            INS_CY - (lat - SHOP_LAT) * 110.57 * INS_SCALE)

def _inset_road_paths():
    from shapely.geometry import box as _box
    b = _box(SHOP_LON-0.009, SHOP_LAT-0.008, SHOP_LON+0.009, SHOP_LAT+0.008)
    out = []
    for c, w, fill, casing in [("secondary", 8.0, ROAD, ROAD_C),
                               ("tertiary", 5.6, ROAD, ROAD_C),
                               ("minor", 3.6, "#F8EFDD", "#E4D2B2")]:
        for g in D["roads"].get(c, []):
            gg = g.intersection(b)
            for ln in line_parts(gg):
                pts = [PI(x, y) for x, y in ln.coords]
                d = "M" + " L".join(f"{a:.1f},{bb:.1f}" for a, bb in pts)
                out.append((c, d, w, fill, casing))
    return out

def inset():
    cx, cy, r = INS_CX, INS_CY, INS_R
    g = ['<g id="inset">']
    g.append(f'<circle cx="{cx+5}" cy="{cy+8}" r="{r}" fill="#6b4a2a" opacity="0.22" filter="url(#soft)"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}"/>')
    g.append('<g clip-path="url(#insetClip)">')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FBF3E1"/>')
    # 放射底纹
    for i in range(24):
        a = i*math.tau/24
        x1, y1 = cx + math.cos(a)*r*0.72, cy + math.sin(a)*r*0.72
        x2, y2 = cx + math.cos(a)*r, cy + math.sin(a)*r
        g.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#EAD9B8" stroke-width="1.1"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.72:.1f}" fill="#FBF3E1"/>')
    # 茶舍插画
    g.append(deco.teahouse(cx, cy+16, 0.86))
    # 文字
    g.append(f'<text x="{cx}" y="{cy+62}" font-size="19" font-weight="800" fill="{ACC}" text-anchor="middle" '
             f'letter-spacing="1.5">同顺泰老茶馆</text>')
    g.append(f'<text x="{cx}" y="{cy+82}" font-size="10" fill="{INK_S}" text-anchor="middle" '
             f'letter-spacing="0.8">福鼎市白琳镇玉琳西路 291 号</text>')
    g.append(f'<text x="{cx}" y="{cy+101}" font-size="9" fill="{TEAL}" text-anchor="middle" '
             f'letter-spacing="2">老白茶 · 冷萃茶 · 茶点</text>')
    g.append('</g>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r-7}" fill="none" stroke="{GOLD}" stroke-width="1.3" opacity="0.9"/>')
    g.append(f'<g transform="translate({cx},{cy-r-1})">'
             f'<rect x="-38" y="-13" width="76" height="26" rx="13" fill="{GOLD}" stroke="{INK}" stroke-width="1.8"/>'
             f'<text x="0" y="4" font-size="11.5" font-weight="700" fill="#3A2A12" text-anchor="middle" letter-spacing="2">合作商铺</text></g>')
    g.append(f'<g transform="translate({cx},{cy+r+2})">'
             f'<rect x="-54" y="-2" width="108" height="18" rx="9" fill="{INK}"/>'
             f'<text x="0" y="11" font-size="8.5" fill="#FFF6E2" text-anchor="middle" letter-spacing="1.5">白琳镇 · 白茶古镇</text></g>')
    g.append('</g>')
    return "".join(g)



def leader():
    x1, y1 = SHOP_X - 22, SHOP_Y - 18
    x2, y2 = INS_CX + 128, INS_CY + 8
    mx, my = (x1+x2)/2 + 8, (y1+y2)/2 + 26
    return (f'<path d="M{x1:.1f},{y1:.1f} Q{mx:.1f},{my:.1f} {x2:.1f},{y2:.1f}" fill="none" '
            f'stroke="{ACC}" stroke-width="1.8" stroke-dasharray="7 5" opacity="0.8"/>'
            f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="3.2" fill="{ACC}"/>'
            f'<path d="M{x2:.1f},{y2:.1f} l-9,-1 l2,8 Z" fill="{ACC}"/>')


def title_block():
    x, y, w, h = 38, 42, 468, 152
    g = [f'<g transform="rotate(-1.1 {x} {y})">',
         f'<rect x="{x+5}" y="{y+6}" width="{w}" height="{h}" rx="12" fill="#6b4a2a" opacity="0.16" filter="url(#soft)"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="2.6"/>',
         f'<rect x="{x+7}" y="{y+7}" width="{w-14}" height="{h-14}" rx="8" fill="none" stroke="{GOLD}" stroke-width="1.1" opacity="0.85"/>',
         f'<text x="{x+30}" y="{y+82}" font-size="56" font-weight="800" fill="{INK}" letter-spacing="2">福鼎</text>',
         f'<text x="{x+160}" y="{y+80}" font-size="29" font-weight="700" fill="{INK}" letter-spacing="3">山海茶旅图</text>',
         f'<text x="{x+32}" y="{y+112}" font-size="9.5" fill="{INK_S}" letter-spacing="2.4">FUDING · 山海之间 · 一杯白茶</text>',
         f'<text x="{x+32}" y="{y+130}" font-size="8.6" fill="{INK_S}" letter-spacing="1.6" opacity="0.8">手绘旅游示意图 · 景点与道路经艺术化处理</text>',
         '</g>']
    # 茶印
    g.append(f'<g transform="translate({x+404},{y+72}) rotate(8)">'
             f'<rect x="-23" y="-23" width="46" height="46" rx="6" fill="{ACC}" stroke="{ACC_D}" stroke-width="1"/>'
             f'<rect x="-19" y="-19" width="38" height="38" rx="4" fill="none" stroke="#FFF3DC" stroke-width="1" opacity="0.7"/>'
             f'<text x="0" y="10" font-size="26" font-weight="700" fill="#FFF6E4" text-anchor="middle">茶</text></g>')
    return "".join(g)

def shoot(png="output/fuding-map.png"):
    CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--user-data-dir=/tmp/chrome-prof", "--crash-dumps-dir=/tmp/chrome-crash",
                    "--force-device-scale-factor=2", f"--window-size={int(W)},{int(H)}",
                    f"--screenshot={png}", f"file://{os.path.abspath('output/fuding-map.html')}"],
                   check=True, capture_output=True)
    return png

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    build(); print("built", os.path.getsize("output/fuding-map.svg")//1024, "KB")
    print(shoot())

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    build(); print("built", os.path.getsize("output/fuding-map.svg")//1024, "KB")
    print(shoot())
