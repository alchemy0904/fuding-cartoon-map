# -*- coding: utf-8 -*-
"""Hand-drawn illustration primitives returning SVG snippets."""
import math, random
from svgbase import P

INK = "#25403E"
INK_S = "#3E5C58"
PAPER = "#FBF1DC"
GREEN = "#BCD69A"
GREEN_D = "#6E9455"
GOLD = "#E8A23A"
ACC = "#C9452F"
STONE = "#E9DFCB"
STONE_D = "#B9A98C"

def g(inner, extra=""):
    return f'<g {extra}>{inner}</g>'

# ---------- cloud ----------
def cloud(x, y, s=1.0, op=0.95):
    d = (f"M{x-46*s:.1f},{y:.1f} "
         f"a{15*s:.1f},{15*s:.1f} 0 0 1 {9*s:.1f},{-26*s:.1f} "
         f"a{19*s:.1f},{19*s:.1f} 0 0 1 {36*s:.1f},{-7*s:.1f} "
         f"a{17*s:.1f},{17*s:.1f} 0 0 1 {28*s:.1f},{11*s:.1f} "
         f"a{13*s:.1f},{13*s:.1f} 0 0 1 {-2*s:.1f},{22*s:.1f} Z")
    return (f'<path d="{d}" fill="#FFFDF8" stroke="{INK}" stroke-width="1.5" '
            f'stroke-linejoin="round" opacity="{op}"/>')

# ---------- sun ----------
def sun(x, y, r=26):
    rays = []
    for i in range(12):
        a = i * math.pi / 6
        x1, y1 = x + math.cos(a)*(r+6), y + math.sin(a)*(r+6)
        x2, y2 = x + math.cos(a)*(r+14), y + math.sin(a)*(r+14)
        rays.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" />')
    return (f'<g stroke="{GOLD}" stroke-width="2.6" stroke-linecap="round">{"".join(rays)}</g>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F6C86A" stroke="{GOLD}" stroke-width="2"/>')

# ---------- pine ----------
def pine(x, y, s=1.0, seed=0):
    rng = random.Random(seed)
    w = 13*s; h = 24*s
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})" stroke="{INK}" stroke-width="1.1">'
            f'<path d="M0,0 l0,-8" stroke="{STONE_D}" stroke-width="2.4"/>'
            f'<path d="M0,-6 L-9,-6 L0,-20 Z" fill="{GREEN}" stroke-linejoin="round"/>'
            f'<path d="M0,-13 L-7.5,-13 L0,-24 Z" fill="{GREEN}" stroke-linejoin="round"/>'
            f'<path d="M0,-19 L-5.5,-19 L0,-28 Z" fill="{GREEN}" stroke-linejoin="round"/>'
            f'</g>')

# ---------- broadleaf tree ----------
def tree(x, y, s=1.0):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})" stroke="{INK}" stroke-width="1.1">'
            f'<path d="M0,0 l0,-9" stroke="{STONE_D}" stroke-width="2.6"/>'
            f'<circle cx="0" cy="-14" r="9" fill="{GREEN}"/>'
            f'<circle cx="-6" cy="-10" r="6" fill="{GREEN}"/>'
            f'<circle cx="6" cy="-10" r="6" fill="{GREEN}"/>'
            f'</g>')

# ---------- house ----------
def house(x, y, s=1.0, rot=0, col="#FFF8EA", roof="#E9B98D"):
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({s})" '
            f'stroke="{INK}" stroke-width="1.15" stroke-linejoin="round">'
            f'<path d="M-9,0 L-9,-8 L9,-8 L9,0 Z" fill="{col}"/>'
            f'<path d="M-12,-8 L0,-17 L12,-8 Z" fill="{roof}"/>'
            f'<rect x="-2.2" y="-5.4" width="4.4" height="5.4" fill="{INK}" stroke="none" opacity="0.55"/>'
            f'</g>')

# ---------- boat ----------
def boat(x, y, s=1.0, sail=True, flip=False):
    f = "scale(-1,1)" if flip else ""
    return (f'<g transform="translate({x:.1f},{y:.1f}) {f} scale({s})" stroke="{INK}" '
            f'stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round">'
            f'<path d="M-20,0 Q0,10 20,0 L14,6 Q0,13 -14,6 Z" fill="#D9683F"/>'
            f'<path d="M-20,0 L20,0" stroke-width="1.8"/>'
            + (f'<path d="M0,0 L0,-30" stroke-width="1.8"/>'
               f'<path d="M2,-29 Q18,-20 2,-8 Z" fill="{PAPER}"/>'
               f'<path d="M-2,-24 Q-14,-17 -2,-7 Z" fill="#F3D9A9"/>' if sail else "")
            + f'</g>')

# ---------- fish ----------
def fish(x, y, s=1.0, flip=False):
    f = "scale(-1,1)" if flip else ""
    return (f'<g transform="translate({x:.1f},{y:.1f}) {f} scale({s})" stroke="{INK}" stroke-width="1.2" '
            f'stroke-linejoin="round"><path d="M-12,0 Q0,-8 12,0 Q0,8 -12,0 Z" fill="#F0C98F"/>'
            f'<path d="M-12,0 L-19,-6 L-17,0 L-19,6 Z" fill="#F0C98F"/>'
            f'<circle cx="7" cy="-1.5" r="1.2" fill="{INK}" stroke="none"/></g>')

# ---------- wave ----------
def wave(x, y, s=1.0, op=0.9, col="#E4F5F6"):
    return (f'<path d="M{x-14*s:.1f},{y:.1f} q{7*s:.1f},{-6*s:.1f} {14*s:.1f},0 t{14*s:.1f},0" '
            f'fill="none" stroke="{col}" stroke-width="{1.6*s:.2f}" stroke-linecap="round" opacity="{op}"/>')

# ---------- seagull ----------
def gull(x, y, s=1.0):
    return (f'<path d="M{x-10*s:.1f},{y:.1f} q{5*s:.1f},{-6*s:.1f} {10*s:.1f},0 q{5*s:.1f},{-6*s:.1f} {10*s:.1f},0" '
            f'fill="none" stroke="{INK_S}" stroke-width="{1.6*s:.2f}" stroke-linecap="round"/>')

# ---------- tea leaf ----------
def tea_leaf(x, y, s=1.0, rot=0, col="#8FB03F"):
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({s})" stroke="{INK}" stroke-width="1">'
            f'<path d="M0,10 C-9,4 -9,-8 0,-14 C9,-8 9,4 0,10 Z" fill="{col}"/>'
            f'<path d="M0,9 L0,-12" stroke="#4E6B22" stroke-width="0.9"/>'
            f'</g>')

# ---------- mountain (granite pillars, for Taimu) ----------
def taimu(x, y, s=1.0, seed=5):
    parts = []
    parts.append(f'<path d="M-100,0 Q-78,-24 -58,-20 Q-34,-32 -12,-16 Q10,-28 34,-20 Q60,-26 80,-4 L96,0 Z" '
                 f'fill="#CBDFAC" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>')
    specs = [(-50, 74, 64), (0, 104, 80), (50, 80, 66)]
    for cx, h, w in specs:
        d = (f"M{cx-w/2},0 L{cx-w*0.13:.1f},{-h*0.90:.1f} "
             f"Q{cx-w*0.02:.1f},{-h*1.02:.1f} {cx+w*0.04:.1f},{-h*0.99:.1f} "
             f"Q{cx+w*0.12:.1f},{-h*0.97:.1f} {cx+w*0.13:.1f},{-h*0.90:.1f} L{cx+w/2},0 Z")
        parts.append(f'<path d="{d}" fill="#EDE3CE" stroke="{INK}" stroke-width="1.9" stroke-linejoin="round"/>')
        sd = f"M{cx+w*0.05:.1f},0 L{cx+w*0.13:.1f},{-h*0.90:.1f} L{cx+w*0.02:.1f},{-h*0.99:.1f} L{cx+w/2},0 Z"
        parts.append(f'<path d="{sd}" fill="#C0AF93" opacity="0.32" stroke="none"/>')
        for k in range(2):
            yy = -h*0.32 - k*h*0.22
            parts.append(f'<path d="M{cx-w*0.10:.1f},{yy:.1f} q{w*0.10:.1f},{-3:.1f} {w*0.20:.1f},{-1:.1f}" fill="none" stroke="#B9A98C" stroke-width="0.9" opacity="0.5"/>')
    for px, pp in [(-78, .55), (-60, .45), (64, .55), (80, .45)]:
        parts.append(pine(px, 2, pp, seed=px))
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s})">{"".join(parts)}</g>'
# ---------- soft hill ----------
def hill(x, y, w, h, col="#D3E3B6", edge=INK_S, op=1.0):
    d = (f"M{-w/2:.1f},0 C{-w*0.34:.1f},{-h*0.75:.1f} {-w*0.16:.1f},{-h:.1f} 0,{-h:.1f} "
         f"C{w*0.18:.1f},{-h:.1f} {w*0.36:.1f},{-h*0.7:.1f} {w/2:.1f},0 Z")
    return (f'<g transform="translate({x:.1f},{y:.1f})">'
            f'<path d="{d}" fill="{col}" stroke="{edge}" stroke-width="1.5" stroke-linejoin="round" opacity="{op}"/>'
            f'<path d="M{-w*0.18:.1f},{-h*0.55:.1f} q{w*0.10:.1f},{-h*0.18:.1f} {w*0.20:.1f},0" fill="none" stroke="{edge}" stroke-width="0.8" opacity="0.5"/>'
            f'</g>')

# ---------- tea terrace ----------
def tea_rows(x, y, w=90, rows=4, s=1.0):
    parts = [f'<path d="M{x-w/2-6:.1f},{y+6:.1f} q{w/2:.1f},{-14:.1f} {w+12:.1f},0 q{-w/2:.1f},{16:.1f} {-w-12:.1f},0 Z" '
             f'fill="#C3DA9B" opacity="0.55" stroke="none"/>']
    for i in range(rows):
        yy = y - i*10*s
        ww = w * (1 - i*0.10)
        parts.append(f'<path d="M{x-ww/2:.1f},{yy:.1f} q{ww/4:.1f},-8 {ww/2:.1f},0 q{ww/4:.1f},8 {ww/2:.1f},0" '
                     f'fill="none" stroke="{GREEN_D}" stroke-width="{2.0*s:.1f}" opacity="{0.5+0.06*i:.2f}" stroke-linecap="round"/>')
        n = max(3, int(ww/16))
        for k in range(n):
            bx = x - ww/2 + (k+0.5)*ww/n
            parts.append(f'<circle cx="{bx:.1f}" cy="{yy-3*i*0.0-2:.1f}" r="{2.1*s:.1f}" fill="{GREEN_D}" opacity="0.75"/>')
    return f'<g>{"".join(parts)}</g>'
# ---------- pagoda ----------
def pagoda(x, y, s=1.0):
    parts = [f'<path d="M-14,0 L14,0 L10,-8 L-10,-8 Z" fill="#EFE2CC" stroke="{INK}" stroke-width="1.3"/>']
    for i, (w, yy) in enumerate([(12,-8),(9,-18),(6,-27),(3,-35)]):
        parts.append(f'<rect x="{-w/2:.1f}" y="{yy-7:.1f}" width="{w}" height="7" fill="#EFE2CC" stroke="{INK}" stroke-width="1.2"/>')
        parts.append(f'<path d="M{-w/2-4:.1f},{yy-7:.1f} L{w/2+4:.1f},{yy-7:.1f} L{w/2:.1f},{yy-10:.1f} L{-w/2:.1f},{yy-10:.1f} Z" fill="{ACC}" stroke="{INK}" stroke-width="1.1"/>')
    parts.append(f'<path d="M0,-42 L0,-50" stroke="{INK}" stroke-width="1.4"/>')
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s})">{"".join(parts)}</g>'

# ---------- lighthouse ----------
def lighthouse(x, y, s=1.0):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round">'
            f'<path d="M-9,0 L-6,-34 L6,-34 L9,0 Z" fill="#FFF9EC"/>'
            f'<path d="M-7.2,-12 L7.2,-12 L8,-20 L-8,-20 Z" fill="{ACC}" stroke="none"/>'
            f'<rect x="-6" y="-42" width="12" height="8" fill="#F6C86A"/>'
            f'<path d="M-8,-42 L8,-42 L0,-50 Z" fill="{ACC}"/>'
            f'<path d="M-2,-46 L-16,-54 M2,-46 L16,-54" stroke="{GOLD}" stroke-width="1.6" stroke-linecap="round"/>'
            f'</g>')

# ---------- compass ----------
def compass(cx, cy, r=42):
    pts = []
    for i in range(8):
        a = i*math.pi/4 - math.pi/2
        rr = r if i % 2 == 0 else r*0.42
        pts.append(f"{cx + math.cos(a)*rr:.1f},{cy + math.sin(a)*rr:.1f}")
    star = " ".join(pts)
    return (f'<g stroke="{INK}" stroke-width="1.3">'
            f'<circle cx="{cx}" cy="{cy}" r="{r+9}" fill="{PAPER}" fill-opacity="0.9"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r+9}" fill="none"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r+3}" fill="none" stroke-width="0.8" opacity="0.6"/>'
            f'<polygon points="{star}" fill="{ACC}" stroke-linejoin="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{PAPER}"/>'
            f'</g>'
            f'<text x="{cx}" y="{cy-r-16}" font-size="13" font-weight="700" text-anchor="middle" fill="{INK}">N</text>')

# ---------- mountain ridge ----------
def ridge(x, y, w=220, h=60, n=5, seed=1, col="#D3E3B6", edge=None):
    import random
    rng = random.Random(seed)
    edge = edge or INK_S
    step = w / n
    d = f"M{x-w/2:.1f},{y:.1f} "
    for i in range(n):
        px = x - w/2 + step*(i+0.5)
        ph = h * rng.uniform(0.55, 1.0)
        d += f"Q{px-step*0.32:.1f},{y-ph*0.86:.1f} {px:.1f},{y-ph:.1f} "
        d += f"Q{px+step*0.32:.1f},{y-ph*0.86:.1f} {px+step:.1f},{y:.1f} "
    d += "Z"
    shade = ""
    for i in range(n):
        px = x - w/2 + step*(i+0.5)
        ph = h * rng.uniform(0.5, 0.8)
        shade += f'<path d="M{px:.1f},{y-ph*0.55:.1f} q{step*0.16:.1f},{-ph*0.18:.1f} {step*0.3:.1f},{-ph*0.1:.1f}" fill="none" stroke="{edge}" stroke-width="0.9" opacity="0.45"/>'
    return (f'<path d="{d}" fill="{col}" stroke="{edge}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<g>{shade}</g>')

# ---------- tea house ----------
def teahouse(x, y, s=1.0):
    p = []
    # 屋顶
    p.append(f'<path d="M-104,-90 Q-54,-106 0,-106 Q54,-106 104,-90 L96,-78 Q48,-90 0,-90 Q-48,-90 -96,-78 Z" '
             f'fill="#7A6A57" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>')
    for i in range(-4,5):
        p.append(f'<path d="M{i*20:.1f},-102 L{i*19:.1f},-91" stroke="#5E5142" stroke-width="1.2" opacity="0.7"/>')
    p.append(f'<path d="M-104,-90 Q-112,-94 -116,-101 M104,-90 Q112,-94 116,-101" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
    # 墙体
    p.append(f'<rect x="-86" y="-84" width="172" height="76" fill="#F7E8CB" stroke="{INK}" stroke-width="2.2"/>')
    for yy in (-64,-44,-24):
        p.append(f'<line x1="-86" y1="{yy}" x2="86" y2="{yy}" stroke="#D9BE93" stroke-width="1.1"/>')
    # 门
    p.append(f'<rect x="-24" y="-62" width="48" height="54" fill="#8B5E3C" stroke="{INK}" stroke-width="1.8"/>')
    p.append(f'<line x1="0" y1="-62" x2="0" y2="-8" stroke="#5F3C24" stroke-width="1.4"/>')
    p.append(f'<line x1="-24" y1="-44" x2="24" y2="-44" stroke="#5F3C24" stroke-width="1"/>')
    # 窗
    for wx in (-64, 30):
        p.append(f'<rect x="{wx}" y="-72" width="34" height="30" fill="#FFF6DE" stroke="{INK}" stroke-width="1.6"/>')
        for k in range(1,3):
            p.append(f'<line x1="{wx+k*34/3:.1f}" y1="-72" x2="{wx+k*34/3:.1f}" y2="-42" stroke="#B98F5E" stroke-width="1"/>')
        p.append(f'<line x1="{wx}" y1="-57" x2="{wx+34}" y2="-57" stroke="#B98F5E" stroke-width="1"/>')
    # 匾额
    p.append(f'<rect x="-30" y="-84" width="60" height="15" rx="2" fill="#9E3222" stroke="{INK}" stroke-width="1.2"/>')
    p.append(f'<text x="0" y="-72.8" font-size="10" fill="#FFF0D2" text-anchor="middle" letter-spacing="3" font-weight="700">同顺泰</text>')
    # 灯笼
    for lx in (-72, 72):
        p.append(f'<line x1="{lx}" y1="-90" x2="{lx}" y2="-82" stroke="{INK}" stroke-width="1.4"/>')
        p.append(f'<ellipse cx="{lx}" cy="-74" rx="7.5" ry="9" fill="#D4482F" stroke="{INK}" stroke-width="1.4"/>')
        p.append(f'<line x1="{lx}" y1="-65" x2="{lx}" y2="-58" stroke="#C9A227" stroke-width="1.6"/>')
        p.append(f'<line x1="{lx-4}" y1="-82" x2="{lx+4}" y2="-82" stroke="#C9A227" stroke-width="2"/>')
    # 茶旗
    p.append(f'<line x1="100" y1="-84" x2="100" y2="-140" stroke="{INK}" stroke-width="2.2"/>')
    p.append(f'<path d="M100,-138 L128,-131 L100,-120 Z" fill="#5C7F3A" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    p.append(f'<text x="109" y="-126" font-size="8" fill="#FFF6E2" text-anchor="middle" font-weight="700" transform="rotate(-8 109 -126)">茶</text>')
    # 台阶与茶丛
    p.append(f'<line x1="-92" y1="-6" x2="92" y2="-6" stroke="{INK}" stroke-width="2"/>')
    p.append(f'<line x1="-84" y1="-1" x2="84" y2="-1" stroke="{INK}" stroke-width="1.4" opacity="0.7"/>')
    p.append(f'<circle cx="-100" cy="-10" r="11" fill="#9DBB68" stroke="{INK}" stroke-width="1.4"/>')
    p.append(f'<circle cx="104" cy="-10" r="10" fill="#9DBB68" stroke="{INK}" stroke-width="1.4"/>')
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s})">{"".join(p)}</g>'
