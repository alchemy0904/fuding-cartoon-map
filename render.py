# -*- coding: utf-8 -*-
"""加载 OpenStreetMap 矢量瓦片数据，整理成可绘制的几何图层。"""
import json, math, os
from shapely.geometry import shape
from shapely.ops import unary_union

BASE = os.path.dirname(os.path.abspath(__file__))
LON0, LAT0, LON1, LAT1 = 119.955, 27.085, 120.485, 27.415
MIDLAT = (LAT0 + LAT1) / 2
KX = math.cos(math.radians(MIDLAT))
W_KM = (LON1 - LON0) * 111.32 * KX
H_KM = (LAT1 - LAT0) * 110.57


def load(name):
    path = os.path.join(BASE, "data/geojson", name + ".geojson")
    return json.load(open(path, encoding="utf-8"))["features"]


def xy(lon, lat):
    return (lon - LON0) * 111.32 * KX, (lat - LAT0) * 110.57


def coords_xy(geom):
    if geom.geom_type == "Point":
        return [xy(geom.x, geom.y)]
    return [xy(*p) for p in geom.coords]


def poly_parts(geom):
    if geom.is_empty:
        return []
    if geom.geom_type == "Polygon":
        return [geom]
    if geom.geom_type in ("MultiPolygon", "GeometryCollection"):
        return [g for g in geom.geoms if g.geom_type == "Polygon"]
    return []


def line_parts(geom):
    if geom.is_empty:
        return []
    if geom.geom_type == "LineString":
        return [geom]
    if geom.geom_type in ("MultiLineString", "GeometryCollection"):
        return [g for g in geom.geoms if g.geom_type == "LineString"]
    return []


def _union(geoms, empty):
    return unary_union(geoms) if geoms else empty


def build():
    """返回按图层整理好的 shapely 几何。"""
    D = {}
    ocean = [shape(f["geometry"]).buffer(0) for f in load("water")
             if f["properties"].get("class") == "ocean"]
    u = unary_union(ocean)
    # 缝合相邻瓦片之间的缝隙
    D["ocean"] = u.buffer(0.0009).buffer(-0.0009).simplify(0.00012).buffer(0)

    lakes = []
    for f in load("water"):
        if f["properties"].get("class") == "ocean":
            continue
        g = shape(f["geometry"]).buffer(0)
        if g.area * 111 * 99 < 0.02:
            continue
        lakes.append(g)
    D["lakes"] = _union(lakes, shape({"type": "Polygon", "coordinates": []}))

    woods, farm, sand, res = [], [], [], []
    for f in load("landcover"):
        c = f["properties"].get("class")
        g = shape(f["geometry"]).buffer(0)
        if g.area * 111 * 99 < 0.15:
            continue
        if c == "wood":
            woods.append(g)
        elif c == "farmland":
            farm.append(g)
        elif c == "sand":
            sand.append(g)
    for f in load("landuse"):
        if f["properties"].get("class") != "residential":
            continue
        g = shape(f["geometry"]).buffer(0)
        if g.area * 111 * 99 > 0.05:
            res.append(g)
    empty = shape({"type": "Polygon", "coordinates": []})
    D["woods"] = _union(woods, empty)
    D["farm"] = _union(farm, empty)
    D["sand"] = _union(sand, empty)
    D["res"] = _union(res, empty)

    roads = {}
    for f in load("transportation"):
        c = f["properties"].get("class")
        g = shape(f["geometry"])
        if c not in ("motorway", "trunk", "primary", "secondary", "tertiary",
                     "minor", "rail", "path", "pier"):
            continue
        if g.geom_type not in ("LineString", "MultiLineString"):
            continue
        roads.setdefault(c, []).append(g)
    D["roads"] = {k: [g.simplify(0.00008) for g in v] for k, v in roads.items()}

    D["rivers"] = [shape(f["geometry"]) for f in load("waterway")
                   if shape(f["geometry"]).length * 100 >= 4]

    bounds = [shape(f["geometry"]) for f in load("boundary")
              if f["properties"].get("admin_level") == 6]
    D["boundary"] = bounds

    places, seen = [], set()
    for f in load("place"):
        p = f["properties"]
        if p.get("class") not in ("city", "town"):
            continue
        nm = p.get("name")
        if not nm or nm in seen:
            continue
        seen.add(nm)
        places.append((nm, p["class"], shape(f["geometry"])))
    D["places"] = places
    return D


D = build()
