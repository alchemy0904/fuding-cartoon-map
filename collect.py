import math, json, os, requests, mapbox_vector_tile
from concurrent.futures import ThreadPoolExecutor

Z = 14
URL = "https://tiles.openfreemap.org/planet/20261011_080001_pt/{z}/{x}/{y}.pbf"
UA = {"User-Agent": "fuding-cartoon-map/1.0 (personal art project)"}
BBOX = (119.96, 27.09, 120.48, 27.41)   # w,s,e,n
EXT = 4096
N = 2 ** Z

def tilexy(lon, lat):
    return (int((lon + 180) / 360 * N),
            int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * N))

def conv(tx, ty, g):
    def pt(p):
        gx, gy = p[0], p[1]
        lon = (tx + gx / EXT) / N * 360 - 180
        lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (ty + 1 - gy / EXT) / N))))
        return [round(lon, 6), round(lat, 6)]
    t = g["type"]
    if t == "Point": return {"type": t, "coordinates": pt(g["coordinates"])}
    if t == "LineString": return {"type": t, "coordinates": [pt(p) for p in g["coordinates"]]}
    if t == "Polygon": return {"type": t, "coordinates": [[pt(p) for p in r] for r in g["coordinates"]]}
    if t == "MultiPolygon": return {"type": t, "coordinates": [[[pt(p) for p in r] for r in poly] for poly in g["coordinates"]]}
    if t == "MultiLineString": return {"type": t, "coordinates": [[pt(p) for p in line] for line in g["coordinates"]]}
    return None

def fetch(t):
    tx, ty = t
    cache = f"data/z{Z}/{tx}_{ty}.json"
    if os.path.exists(cache):
        return json.load(open(cache))
    try:
        r = requests.get(URL.format(z=Z, x=tx, y=ty), headers=UA, timeout=60)
        if r.status_code != 200:
            return {}
        dec = mapbox_vector_tile.decode(r.content, default_options={"y_coord_down": False})
    except Exception as e:
        print("fail", t, e); return {}
    out = {}
    for layer, v in dec.items():
        feats = []
        for f in v.get("features", []):
            geom = conv(tx, ty, f["geometry"])
            if not geom: continue
            props = {k: val for k, val in f["properties"].items() if k in (
                "class","subclass","name","name:zh","name:en","rank","brunnel","layer",
                "admin_level","ele","ele_ft","maritime","disputed","capital","id","intermittent")}
            feats.append({"type": "Feature", "geometry": geom, "properties": props})
        out[layer] = feats
    json.dump(out, open(cache, "w"))
    return out

x0, y0 = tilexy(BBOX[0], BBOX[3]); x1, y1 = tilexy(BBOX[2], BBOX[1])
tiles = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
print(len(tiles), "tiles", x0, x1, y0, y1)
os.makedirs(f"data/z{Z}", exist_ok=True)
layers = {}
with ThreadPoolExecutor(10) as ex:
    for data in ex.map(fetch, tiles):
        for k, v in data.items():
            layers.setdefault(k, []).extend(v)
os.makedirs("data/geojson", exist_ok=True)
for k, v in layers.items():
    json.dump({"type": "FeatureCollection", "features": v}, open(f"data/geojson/{k}.geojson", "w"), ensure_ascii=False)
    print(f"{k:22s}{len(v):6d}")
