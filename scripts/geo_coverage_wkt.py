"""Make the WKT geometry for a "Document geographical coverage" nanopub from an
OpenStreetMap administrative boundary — so the geometry is cited and reproducible, not
hand-written, and not the bounding box the Science Live location search stores.

    pixi run python scripts/geo_coverage_wkt.py hamburg 62782 --utm 32632

Selects the OSM relation by ID (Nominatim lookup, ODbL), keeps the largest part (the
mainland; e.g. Hamburg's Wadden Sea exclave at the Elbe mouth is dropped), drops holes,
simplifies it in a UTM zone in metres — raising the tolerance step by step until the WKT
fits the template's cap (the coverage template's `wkt` field allows 1,500 characters) — and
writes nanopubs/geo/<name>.wkt plus <name>.json (provenance).
"""

import argparse
import datetime
import hashlib
import json
from pathlib import Path

import numpy as np
import requests
import shapely
from pyproj import Transformer
from shapely.geometry import Polygon, shape

NOMINATIM = "https://nominatim.openstreetmap.org/lookup"
OUT = Path(__file__).resolve().parent.parent / "nanopubs" / "geo"


def boundary(relation: int) -> tuple[dict, shapely.Geometry]:
    r = requests.get(NOMINATIM, params={"osm_ids": f"R{relation}", "format": "json",
                                        "polygon_geojson": 1},
                     headers={"User-Agent": "forrt-replication geo-coverage"}, timeout=120)
    r.raise_for_status()
    hit = r.json()[0]
    return hit, shape(hit["geojson"])


def reproject(geom: shapely.Geometry, transformer: Transformer) -> shapely.Geometry:
    return shapely.transform(geom, lambda c: np.column_stack(transformer.transform(c[:, 0], c[:, 1])))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("relation", type=int)
    ap.add_argument("--utm", type=int, required=True, help="EPSG code of a metric CRS for the area")
    ap.add_argument("--max-chars", type=int, default=1500, help="template cap on the WKT field")
    ap.add_argument("--decimals", type=int, default=4)
    a = ap.parse_args()

    hit, geom = boundary(a.relation)
    parts = list(getattr(geom, "geoms", [geom]))
    to_m = Transformer.from_crs(4326, a.utm, always_xy=True)
    to_deg = Transformer.from_crs(a.utm, 4326, always_xy=True)
    metric = [reproject(p, to_m) for p in parts]
    main_part = Polygon(max(metric, key=lambda p: p.area).exterior)
    for tolerance in (50, 100, 150, 200, 300, 400, 500, 750, 1000, 1500, 2000):
        simple = main_part.simplify(tolerance, preserve_topology=True)
        out = reproject(simple, to_deg)
        wkt = shapely.to_wkt(out, rounding_precision=a.decimals, trim=True)
        if len(wkt) <= a.max_chars:
            break
    else:
        raise SystemExit(f"cannot fit {a.max_chars} characters")
    assert shapely.from_wkt(wkt).is_valid

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{a.name}.wkt").write_text(wkt + "\n")
    meta = {
        "name": a.name, "source": f"OpenStreetMap relation {a.relation} ({hit['display_name']})",
        "osm_url": f"https://www.openstreetmap.org/relation/{a.relation}",
        "retrieved_via": f"{NOMINATIM}?osm_ids=R{a.relation}&polygon_geojson=1",
        "retrieved_on": datetime.date.today().isoformat(), "license": "ODbL-1.0",
        "parts_in_boundary": len(parts), "kept": "largest part (mainland)",
        "simplification_m": tolerance, "max_chars": a.max_chars, "holes": "dropped",
        "metric_crs": f"EPSG:{a.utm}", "decimals": a.decimals,
        "area_km2_full_boundary": round(sum(p.area for p in metric) / 1e6, 1),
        "area_km2_kept": round(main_part.area / 1e6, 1),
        "area_km2_simplified": round(simple.area / 1e6, 1),
        "area_difference_pct": round(100 * (simple.area - main_part.area) / main_part.area, 2),
        "vertices": int(shapely.get_num_coordinates(out)), "wkt_chars": len(wkt),
        "bounds_lon_lat": [round(v, 4) for v in out.bounds],
        "wkt_sha256": hashlib.sha256(wkt.encode()).hexdigest(),
    }
    (OUT / f"{a.name}.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(meta, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
