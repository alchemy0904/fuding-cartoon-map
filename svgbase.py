# -*- coding: utf-8 -*-
"""Geometry -> SVG helpers for the hand-drawn Fuding map."""
import math, os
import numpy as np
from shapely.geometry import shape
from shapely.ops import unary_union
import render as R
from render import (LON0, LAT0, LON1, LAT1, KX, load, D)

W, H = 1500.0, 1043.0
KMX = (LON1 - LON0) * 111.32 * KX
KMY = (LAT1 - LAT0) * 110.57
S = W / KMX

def P(lon, lat):
    return ((lon - LON0) * 111.32 * KX * S, (LAT1 - lat) * 110.57 * S)

def d_line(g, prec=1, close=False):
    pts = list(g.coords)
    if len(pts) < 2: return ""
    s = "M" + " L".join(f"{P(x,y)[0]:.{prec}f},{P(x,y)[1]:.{prec}f}" for x, y in pts)
    return s + ("Z" if close else "")

def d_ring(ring, prec=1):
    pts = list(ring.coords)[:-1]
    if len(pts) < 3: return ""
    s = "M" + " L".join(f"{P(x,y)[0]:.{prec}f},{P(x,y)[1]:.{prec}f}" for x, y in pts)
    return s + "Z"

def d_poly(p, prec=1):
    if p.is_empty: return ""
    parts = []
    if p.geom_type == "Polygon":
        polys = [p]
    elif p.geom_type in ("MultiPolygon", "GeometryCollection"):
        polys = [g for g in p.geoms if g.geom_type == "Polygon"]
    else:
        return ""
    for q in polys:
        s = d_ring(q.exterior, prec)
        for r in q.interiors:
            s += " " + d_ring(r, prec)
        if s: parts.append(s)
    return " ".join(parts)

def clip(g):
    from shapely.geometry import box
    return g.intersection(box(LON0, LAT0, LON1, LAT1))

def simplify(g, tol):
    try: return g.simplify(tol, preserve_topology=True)
    except Exception: return g

import sys
sys.setrecursionlimit(10000)
