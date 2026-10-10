# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 01 — Data download
#
# All inputs are open and fetched here; no credentials are needed.
#
# | Component | Source | Licence |
# |---|---|---|
# | Hazard | REACHOUT pluvial flood maps for Logroño, Staccione and Pal (2024), Zenodo [10.5281/zenodo.14035876](https://doi.org/10.5281/zenodo.14035876) — cited by Vogelbacher et al. (2026, Sect. 4.3.2) as a basis for transfer | CC BY 4.0 |
# | Buildings | Spanish Cadastre, INSPIRE Buildings, municipality 26900 (Logroño), ATOM bulk download | CC BY 4.0 |
# | Street area | Spanish Cadastre, INSPIRE Cadastral Parcels (cadastral zoning = urban blocks) | CC BY 4.0 |
| Street names (locating reported impacts) | Spanish Cadastre, INSPIRE Addresses (address points + thoroughfare names) | CC BY 4.0 |
# | Social vulnerability | INE, Censo de Población y Viviendas 2021, indicators per sección censal + section boundaries (01/01/2021) | INE terms (reuse with attribution) |
| Water mask | Copernicus EU-Hydro River Network Database v1.3, [10.2909/393359a7-7ebd-4a52-80ac-1a18d5f3db9c](https://doi.org/10.2909/393359a7-7ebd-4a52-80ac-1a18d5f3db9c) — river surfaces and inland water | Copernicus (free, full and open) |
| Streets (robustness check) | Copernicus Urban Atlas 2018, FUA ES018L2 Logroño, [10.2909/9911fe21-57f6-46fb-ae26-d76e7bb6378f](https://doi.org/10.2909/9911fe21-57f6-46fb-ae26-d76e7bb6378f) | Copernicus (free, full and open) |
#
# Only the `Baseline` scenario is extracted from the REACHOUT archive (seven
# return periods, ~44 MB of the 12.5 GB unzipped). The archive is checked against
# the MD5 Zenodo publishes. The Cadastre and INE publish no checksums and
# regenerate their files over time, so the source log (`data/raw/sources.json`)
# records each file's SHA-256 and the server's `Last-Modified` date — that is the
# exact version this run used.
#
# The two Copernicus layers are queried from the EEA's public ArcGIS map services
# over the municipality's extent (no login), returned in EPSG:25830. IGN's
# hydrography services were unreachable on 2026-10-10 (timeouts / HTTP 504), so
# EU-Hydro is the water source.
#
# Recorded flood impacts are curated by hand from press reports and versioned in
# the repository (`data/impacts/`), not downloaded here. Places without an address
# (the N-111 underpass of calle Clavijo, the LO-20 under the calle Chile roundabout,
# named facilities) are located with OpenStreetMap: the Overpass query below is run
# once and its response committed as `data/impacts/osm_features.json` (ODbL), so
# later runs use the same features; set `REFRESH_OSM = True` to query again.

# %%
import datetime
import hashlib
import json
import zipfile
from pathlib import Path

import requests

# %%
RAW_DIR = Path("../data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

REACHOUT = {"record": "14035876", "doi": "10.5281/zenodo.14035876",
            "file": "PluvialFloodMap_Logrono.zip", "scenario": "Baseline"}

CATASTRO = "https://www.catastro.hacienda.gob.es/INSPIRE"
WEB_SOURCES = [
    {"name": "cadastre_buildings", "license": "CC-BY-4.0",
     "url": f"{CATASTRO}/Buildings/26/26900-LOGRO%C3%91O/A.ES.SDGC.BU.26900.zip",
     "extract": ["A.ES.SDGC.BU.26900.building.gml", "A.ES.SDGC.BU.26900.buildingpart.gml",
                 "A.ES.SDGC.BU.MD.26900.xml"]},
    {"name": "cadastre_parcels", "license": "CC-BY-4.0",
     "url": f"{CATASTRO}/CadastralParcels/26/26900-LOGRO%C3%91O/A.ES.SDGC.CP.26900.zip",
     "extract": ["A.ES.SDGC.CP.26900.cadastralzoning.gml", "A.ES.SDGC.CP.MD..26900.xml"]},
    {"name": "cadastre_addresses", "license": "CC-BY-4.0",
     "url": f"{CATASTRO}/Addresses/26/26900-LOGRO%C3%91O/A.ES.SDGC.AD.26900.zip",
     "extract": ["A.ES.SDGC.AD.26900.gml", "A.ES.SDGC.AD.MD.26900.xml"]},
    {"name": "ine_census2021_indicators", "license": "INE (reuse with attribution)",
     "url": "https://www.ine.es/censos2021/C2021_Indicadores.csv"},
    {"name": "ine_census2021_indicator_definitions", "license": "INE (reuse with attribution)",
     "url": "https://www.ine.es/censos2021/indicadores_seccen_c2021.xlsx"},
    {"name": "ine_census2021_sections", "license": "INE (reuse with attribution)",
     "url": "https://www.ine.es/censos2021/Cartografia_secc.zip",
     "extract": "Seccionado_2021/"},
]


# Municipality extent (Cadastre zoning, EPSG:25830), used for the map-service queries.
EXTENT_25830 = (537600, 4697500, 554120, 4707640)
EEA = "https://image.discomap.eea.europa.eu/arcgis/rest/services"
MAP_SERVICE_SOURCES = [
    {"name": "euhydro_river_polygons", "doi": "10.2909/393359a7-7ebd-4a52-80ac-1a18d5f3db9c",
     "layer": f"{EEA}/EUHydro/EUHydro_RiverNetworkDatabase/MapServer/19", "where": "1=1"},
    {"name": "euhydro_inland_water", "doi": "10.2909/393359a7-7ebd-4a52-80ac-1a18d5f3db9c",
     "layer": f"{EEA}/EUHydro/EUHydro_RiverNetworkDatabase/MapServer/2", "where": "1=1"},
    {"name": "urban_atlas_2018_logrono", "doi": "10.2909/9911fe21-57f6-46fb-ae26-d76e7bb6378f",
     "layer": f"{EEA}/UrbanAtlas/UA_UrbanAtlas_2018/MapServer/2", "where": "fua_code='ES018L2'"},
]


IMPACTS_DIR = Path("../data/impacts")
REFRESH_OSM = False
OVERPASS = ["https://overpass-api.de/api/interpreter",
            "https://overpass.private.coffee/api/interpreter"]
OSM_BBOX = "42.40,-2.55,42.50,-2.38"  # south, west, north, east
OSM_QUERY = f"""[out:json][timeout:120];
(
  way["highway"]["name"~"^(Calle Clavijo|Avenida Club Deportivo)$"]({OSM_BBOX});
  way["highway"]["ref"~"(^|;)(N-111|LO-20)(;|$)"]({OSM_BBOX});
  way["junction"="roundabout"]({OSM_BBOX});
  way(id:40960705,46108020,1000277119);
);
out geom tags;"""
# way 40960705 "Adarraga" (car park, Paseo de las Norias); 46108020 Palacio de los
# Deportes; 1000277119 C.A.R.P.A. (clinic) — identified with Nominatim, 2026-10-10.


# %%
def _digest(path: Path, algo: str) -> str:
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, out: Path) -> dict:
    """Stream a URL to disk; return the response headers that identify the version."""
    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(out, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 16):
                f.write(chunk)
        return {"last_modified": r.headers.get("Last-Modified")}


def extract(archive: Path, members, dest: Path) -> list[str]:
    """Extract named members, or every member under a directory prefix (str)."""
    with zipfile.ZipFile(archive) as z:
        names = ([n for n in z.namelist() if n.startswith(members) and not n.endswith("/")]
                 if isinstance(members, str) else members)
        for n in names:
            z.extract(n, dest)
    return names


def query_layer(layer: str, where: str, out: Path, page: int = 1000) -> int:
    """Page through an ArcGIS map-service layer over EXTENT_25830; write GeoJSON."""
    params = {"where": where, "geometry": ",".join(map(str, EXTENT_25830)),
              "geometryType": "esriGeometryEnvelope", "inSR": 25830, "outSR": 25830,
              "outFields": "*", "orderByFields": "OBJECTID", "f": "geojson",
              "resultRecordCount": page}
    features, offset = [], 0
    while True:
        r = requests.get(f"{layer}/query", params={**params, "resultOffset": offset}, timeout=300)
        r.raise_for_status()
        batch = r.json()
        features += batch["features"]
        if len(batch["features"]) < page:
            break
        offset += page
    collection = {"type": "FeatureCollection", "features": features,
                  "crs": {"type": "name", "properties": {"name": "EPSG:25830"}}}
    out.write_text(json.dumps(collection))
    return len(features)


def overpass(query: str, attempts: int = 3) -> dict:
    """Run an Overpass query, trying each endpoint, with back-off (the service rate-limits)."""
    import time
    for attempt in range(attempts):
        for url in OVERPASS:
            try:
                r = requests.post(url, data={"data": query}, timeout=180,
                                  headers={"User-Agent": "logrono-pluvial-flood-replication"})
                r.raise_for_status()
                return {"endpoint": url, **r.json()}
            except (requests.RequestException, ValueError):
                continue
        time.sleep(30 * (attempt + 1))
    raise RuntimeError("Overpass unavailable; retry later (the committed cache is used otherwise)")


# %% [markdown]
# ## Hazard — REACHOUT (Zenodo, MD5-verified)

# %%
record = requests.get(f"https://zenodo.org/api/records/{REACHOUT['record']}", timeout=60).json()
entry = next(f for f in record["files"] if f["key"] == REACHOUT["file"])
algo, expected = entry["checksum"].split(":", 1)
archive = RAW_DIR / REACHOUT["file"]
if not (archive.exists() and _digest(archive, algo) == expected):
    fetch(entry["links"]["self"], archive)
assert _digest(archive, algo) == expected, f"{archive.name}: {algo} mismatch"

prefix = f"Logrono/{REACHOUT['scenario']}/"
with zipfile.ZipFile(archive) as z:
    tifs = sorted(n for n in z.namelist() if n.startswith(prefix) and n.endswith(".tif"))
extract(archive, tifs, RAW_DIR / "reachout")
print(f"{REACHOUT['file']}: {algo} OK; extracted {len(tifs)} rasters:", [Path(t).name for t in tifs])

hazard_log = {
    "doi": REACHOUT["doi"],
    "title": record["metadata"]["title"],
    "version": record["metadata"].get("version"),
    "license": record["metadata"]["license"]["id"],
    "creators": [c["name"] for c in record["metadata"]["creators"]],
    "file": REACHOUT["file"], "url": entry["links"]["self"], "md5": expected,
    "extracted": [{"name": t, "sha256": _digest(RAW_DIR / "reachout" / t, "sha256")} for t in tifs],
}

# %% [markdown]
# ## Buildings, street blocks and census (Cadastre ATOM, INE)

# %%
web_log = []
for src in WEB_SOURCES:
    out = RAW_DIR / Path(src["url"]).name
    headers = fetch(src["url"], out)
    rec = {"name": src["name"], "url": src["url"], "license": src["license"],
           "file": out.name, "bytes": out.stat().st_size,
           "sha256": _digest(out, "sha256"), **headers}
    if "extract" in src:
        names = extract(out, src["extract"], RAW_DIR / src["name"])
        rec["extracted"] = [{"name": n, "sha256": _digest(RAW_DIR / src["name"] / n, "sha256")}
                            for n in names]
    web_log.append(rec)
    print(f"{src['name']}: {rec['bytes']:,} bytes, Last-Modified {rec['last_modified']}")

# %% [markdown]
# ## Water mask and Urban Atlas (Copernicus, EEA map services)

# %%
service_log = []
for src in MAP_SERVICE_SOURCES:
    out = RAW_DIR / f"{src['name']}.geojson"
    n = query_layer(src["layer"], src["where"], out)
    service_log.append({**src, "extent_epsg25830": EXTENT_25830, "features": n,
                        "file": out.name, "sha256": _digest(out, "sha256")})
    print(f"{src['name']}: {n} features")

# %% [markdown]
# ## OpenStreetMap features for impact places (committed cache)

# %%
osm_path = IMPACTS_DIR / "osm_features.json"
if REFRESH_OSM or not osm_path.exists():
    osm = overpass(OSM_QUERY)
    osm["query"] = OSM_QUERY
    osm_path.write_text(json.dumps(osm, ensure_ascii=False, indent=1))
osm = json.loads(osm_path.read_text())
osm_log = {"file": str(osm_path), "sha256": _digest(osm_path, "sha256"),
           "osm_base": osm["osm3s"]["timestamp_osm_base"], "endpoint": osm["endpoint"],
           "elements": len(osm["elements"]), "license": "ODbL-1.0"}
print(f"OSM: {osm_log['elements']} ways, data as of {osm_log['osm_base']}")

# %% [markdown]
# ## Source log

# %%
with open(RAW_DIR / "sources.json", "w") as f:
    json.dump({"accessed_on": datetime.date.today().isoformat(),
               "hazard": hazard_log, "web": web_log, "map_services": service_log,
               "osm": osm_log}, f, indent=2)

print(f"Logged 1 Zenodo record, {len(web_log)} web source(s) and "
      f"{len(service_log)} map-service layer(s) to {RAW_DIR / 'sources.json'}")
