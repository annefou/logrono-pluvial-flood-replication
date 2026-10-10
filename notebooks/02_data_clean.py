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
# # 02 — Data clean
#
# Builds the inputs of the risk framework for Logroño, in the shape the method
# library (`building-climate-risk`) expects, and locates the recorded flood impacts.
# Everything is written to `data/interim/logrono.gpkg` (EPSG:25830, ETRS89 / UTM 30N —
# the Cadastre's CRS; distances in ground metres).
#
# | Layer | Built from | Rule |
# |---|---|---|
# | `sections` | INE Census 2021 | 109 secciones of Logroño + indicators + proxies (§1) |
# | `buildings` | Cadastre buildings + parts | floors, residents, ground-floor residents, vulnerability indicators (§2) |
# | `urban_area`, `streets` | Cadastre urban blocks, Urban Atlas water | gaps between blocks after a 25 m closing, minus water (§3) |
# | `streets_urban_atlas` | Urban Atlas 2018 | road classes, minus water — robustness check only (§3) |
# | `water` | Urban Atlas 2018 class 50000 | river and water bodies; checked against EU-Hydro for alignment with REACHOUT (§4) |
# | `flood_rp100_{30..100}` | REACHOUT Baseline RP100 | depth ≥ threshold, polygonised on the native grid, minus water (§4) |
# | `impact_places` | press reports + Cadastre addresses + OSM | one geometry per reported place (§5) |
#
# Deviations from the paper introduced here are listed at the end (§6).

# %%
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import rasterio.features
import rasterio.windows
import building_climate_risk as bcr
import shapely
from pyproj import Transformer
from shapely.geometry import LineString, Polygon, shape

# %%
RAW = Path("../data/raw")
IMPACTS = Path("../data/impacts")
INTERIM = Path("../data/interim")
INTERIM.mkdir(parents=True, exist_ok=True)
OUT = INTERIM / "logrono.gpkg"
OUT.unlink(missing_ok=True)

CRS = "EPSG:25830"
MUNICIPALITY = "26089"          # INE code (cpro 26, cmun 089)
CLOSING_M = 25.0                # gaps narrower than 2 x 25 m between blocks are streets/squares
DEPTHS_CM = list(range(30, 101, 10))
RETURN_PERIOD = "F_RP100"       # REACHOUT Baseline, 26.77 mm in 15 min
HAZARD_MARGIN_M = 100.0         # flood polygons kept up to this distance beyond the urban area


def write(gdf: gpd.GeoDataFrame, layer: str) -> None:
    gdf.to_file(OUT, layer=layer, driver="GPKG")
    print(f"{layer}: {len(gdf):,} features")


# %% [markdown]
# ## 1. Census sections and vulnerability proxies
#
# INE's ready-made indicators are shares of the section's residents (or counts, for
# households). The paper's four indicators are counts per building; here each is a
# section-level **rate per resident**, later multiplied by the building's residents.
# TOPSIS normalises each column by its vector norm, so only relative values matter.
#
# | Paper | Proxy per resident (INE table) | Note |
# |---|---|---|
# | children < 10 (C) | `t4_1` share under 16 | broader age band |
# | elderly singles > 65 (ES) | `t22_1` one-person households × `t4_3` share over 64 / `t1_1` | single-person households of all ages, scaled by the over-64 share |
# | welfare recipients (WR) | `t10_1` unemployed/active × `t12_1` active/16+ × (1 − `t4_1`) | unemployed per resident; alternative `WR_disab` = `t13_1` disability pensioners/16+ × (1 − `t4_1`) |
# | school leavers without diploma (EDQ) | (1 − `t9_1` higher-education share of 16+) × (1 − `t4_1`) | residents 16+ without higher education |

# %%
ind = pd.read_csv(RAW / "C2021_Indicadores.csv", dtype=str)
ind = ind[(ind["cpro"] + ind["cmun"]) == MUNICIPALITY].copy()
ind["CUSEC"] = ind["cpro"] + ind["cmun"] + ind["dist"] + ind["secc"]
num = ind.drop(columns=["ccaa", "cpro", "cmun", "dist", "secc"]).set_index("CUSEC").astype(float)

adult = 1 - num["t4_1"]
rates = pd.DataFrame({
    "pop": num["t1_1"],
    "C_rate": num["t4_1"],
    "ES_rate": num["t22_1"] * num["t4_3"] / num["t1_1"],
    "WR_rate": num["t10_1"] * num["t12_1"] * adult,
    "WR_disab_rate": num["t13_1"] * adult,
    "EDQ_rate": (1 - num["t9_1"]) * adult,
    "dwellings_census": num["t18_1"],
})
sections = gpd.read_file(RAW / "ine_census2021_sections/Seccionado_2021/SECC_CE_20210101.shp",
                         where=f"CUMUN='{MUNICIPALITY}'").to_crs(CRS)
sections = sections[["CUSEC", "CDIS", "CSEC", "geometry"]].merge(rates, left_on="CUSEC", right_index=True)
assert len(sections) == 109 and int(sections["pop"].sum()) == 150_596
rates.describe().T.round(4)

# %% [markdown]
# ## 2. Buildings, residents and indicators
#
# - **Floors above ground**: the Cadastre stores them per building part
#   (`<building localId>_partN`); a building's floors = the maximum over its parts.
# - **Section**: the section containing the footprint's representative point.
# - **Residents** (`R`, exposure to mobility): the section's population shared among its
#   buildings in proportion to their Cadastre dwellings (dwellings per section match the
#   census within 1 % city-wide; median section ratio 1.00).
# - **Ground-floor residents** (`R_G`, exposure to well-being): `R / floors` for buildings
#   whose main use is residential; 0 for buildings with dwellings but another main use
#   (the paper's mixed-use rule: ground floor commercial). The open Cadastre has no
#   per-floor use, so residential buildings with shops at street level are counted as
#   residential — an overestimate in the centre (deviation; tested for robustness in 03).
# - **Indicators**: section rate × `R` (§1).
# - Ruins are dropped.

# %%
buildings = gpd.read_file(RAW / "cadastre_buildings/A.ES.SDGC.BU.26900.building.gml")
parts = gpd.read_file(RAW / "cadastre_buildings/A.ES.SDGC.BU.26900.buildingpart.gml")
parts["building"] = parts["localId"].str.split("_part").str[0]
floors = parts.groupby("building")["numberOfFloorsAboveGround"].max()

b = buildings[buildings["conditionOfConstruction"] != "ruin"].copy()
b = b.rename(columns={"localId": "ID", "currentUse": "use", "numberOfDwellings": "dwellings",
                      "value": "floor_area_m2"})
b["floors"] = b["ID"].map(floors).fillna(1).clip(lower=1).astype(int)
b["dwellings"] = b["dwellings"].fillna(0).astype(int)
b = b[["ID", "use", "dwellings", "floors", "floor_area_m2", "conditionOfConstruction", "geometry"]]
b = b.set_geometry(b.geometry.make_valid()).to_crs(CRS)

points = b.set_geometry(b.representative_point())
b["CUSEC"] = gpd.sjoin(points, sections[["CUSEC", "geometry"]], how="left",
                       predicate="within")["CUSEC"].values
b = b.merge(sections.drop(columns="geometry"), on="CUSEC", how="left")

b["R"] = bcr.allocate(sections.set_index("CUSEC")["pop"], b["CUSEC"], b["dwellings"])
b["R_G"] = bcr.residents_on_floor(b["R"], b["floors"], eligible=b["use"] == "1_residential")
for ind_col in ["C", "ES", "WR", "WR_disab", "EDQ"]:
    b[ind_col] = b[f"{ind_col}_rate"] * b["R"]
b = b.drop(columns=[c for c in b.columns if c.endswith("_rate")] + ["pop", "dwellings_census"])

print(f"{len(b):,} buildings; {int((b['R'] > 0).sum()):,} with residents; "
      f"residents allocated {b['R'].sum():,.0f} of {sections['pop'].sum():,.0f} "
      f"(unallocated: buildings outside any section)")
print(b.groupby("use", dropna=False)[["R", "R_G"]].sum().round(0))

# %% [markdown]
# ## 3. Street area and water
#
# The Cadastre has no street polygons. Inside the city, the space between urban blocks
# (*manzanas*) is streets and squares. The zoning layer's labels carry a trailing space
# (`'MANZANA '`), and six block polygons are invalid (repaired with `make_valid`).
#
# - **Urban area** = blocks closed by 25 m (buffer +25 m, then −25 m): gaps narrower than
#   ~50 m between blocks are filled. Wider corridors (e.g. the LO-20) are not street area.
# - **Streets** = urban area − blocks − water (Urban Atlas class 50000; compared with
#   EU-Hydro in §4). Building footprints are removed later by the rings themselves.
# - **Urban Atlas streets** (robustness only) = classes 12210 fast transit roads,
#   12220 other roads, minus water.

# %%
zoning = gpd.read_file(RAW / "cadastre_parcels/A.ES.SDGC.CP.26900.cadastralzoning.gml")
blocks_geom = zoning[zoning["LocalisedCharacterString"].str.strip() == "MANZANA"].geometry
blocks = shapely.union_all(blocks_geom.make_valid().to_crs(CRS).values)
urban = blocks.buffer(CLOSING_M).buffer(-CLOSING_M)

ua = gpd.read_file(RAW / "urban_atlas_2018_logrono.geojson").set_crs(CRS, allow_override=True)
water_geom = shapely.union_all(ua[ua["code_2018"] == "50000"].geometry.make_valid().values)
euhydro_river = shapely.union_all(gpd.read_file(RAW / "euhydro_river_polygons.geojson")
                                  .set_crs(CRS, allow_override=True).geometry.make_valid().values)
euhydro_inland = shapely.union_all(gpd.read_file(RAW / "euhydro_inland_water.geojson")
                                   .set_crs(CRS, allow_override=True).geometry.make_valid().values)

streets = urban.difference(blocks).difference(water_geom)
ua_roads = shapely.union_all(ua[ua["code_2018"].isin(["12210", "12220"])].geometry.make_valid().values)
streets_ua = ua_roads.difference(water_geom)

b["in_urban_area"] = b.representative_point().within(urban)
print(f"blocks {blocks.area / 1e6:.2f} km², urban area {urban.area / 1e6:.2f} km², "
      f"streets {streets.area / 1e6:.2f} km² (water removed: "
      f"{urban.difference(blocks).intersection(water_geom).area:,.0f} m²), "
      f"Urban Atlas roads {streets_ua.area / 1e6:.2f} km²")
print(f"buildings in the urban area: {int(b['in_urban_area'].sum()):,} of {len(b):,} "
      f"({b.loc[b['in_urban_area'], 'R'].sum() / b['R'].sum():.1%} of residents)")

# %% [markdown]
# ## 4. Flood extents (REACHOUT, 100-year design storm)
#
# REACHOUT's grid is in **EPSG:32632** (UTM zone 32; the model ran there, the infiltration
# layer is named `32632_Logrono_PERM_sr`), about 11° west of that zone's central meridian,
# where scale is distorted by ~1.1 %. The depths are therefore **not resampled**: each
# threshold (depth ≥ 30, 40, … 100 cm, as the paper's nested flood layers) is polygonised
# on the native 2 m grid, and only the polygons are transformed to EPSG:25830, where all
# buffers are drawn in ground metres. NoData (−9999) is dry.
#
# **Water.** SaferRAIN rains on the whole grid, so the Ebro's bed holds water too. That is
# not pluvial flooding of urban surfaces, and it would count as hazard for riverside
# buildings, so water bodies are removed from every flood layer. The water mask must line
# up with REACHOUT: the check below measures how much of the flooded Ebro channel (≥ 30 cm,
# central stretch) each candidate covers, and at which shift. Urban Atlas water and
# EU-Hydro (river surfaces + inland water, which together hold this reach of the Ebro)
# both line up with no shift and cover about the same share; EU-Hydro's river-surface
# layer alone does not. Urban Atlas is used (one product, also used for the road
# robustness check). REACHOUT itself lines up with the Cadastre: the first check shows
# water is rarer inside building footprints than outside them, and least so with no shift
# (the footprint test is computed on the native grid, footprints transformed to EPSG:32632).

# %%
def flood_polygons(tif: Path, extent_25830: Polygon, depths_cm: list[int]) -> dict[int, gpd.GeoSeries]:
    with rasterio.open(tif) as src:
        to_src = Transformer.from_crs(CRS, src.crs, always_xy=True)
        bounds = to_src.transform_bounds(*extent_25830.bounds)
        window = rasterio.windows.from_bounds(*bounds, transform=src.transform).round_offsets().round_lengths()
        depth = src.read(1, window=window, masked=True).filled(-9999)
        transform, src_crs = src.window_transform(window), src.crs
    out = {}
    for d in depths_cm:
        wet = (depth >= d / 100).astype("uint8")
        geoms = [shape(g) for g, v in rasterio.features.shapes(wet, mask=wet == 1, transform=transform)]
        out[d] = gpd.GeoSeries(geoms, crs=src_crs).to_crs(CRS)
    return out


extent = urban.buffer(HAZARD_MARGIN_M + 30).envelope
floods = flood_polygons(RAW / f"reachout/Logrono/Baseline/{RETURN_PERIOD}.tif", extent, DEPTHS_CM)

def footprint_alignment(tif: Path, footprints: gpd.GeoSeries,
                        shifts: list[tuple[int, int]]) -> pd.DataFrame:
    """Share of wet / >= 30 cm cells inside vs outside footprints, on the native grid."""
    with rasterio.open(tif) as src:
        fp = footprints.to_crs(src.crs)
        win = rasterio.windows.from_bounds(*fp.total_bounds, transform=src.transform)
        win = win.round_offsets().round_lengths()
        depth = src.read(1, window=win, masked=True).filled(0)
        transform = src.window_transform(win)
    rows = []
    for dx, dy in shifts:
        inside = rasterio.features.rasterize(
            ((g, 1) for g in fp.translate(dx, dy)), out_shape=depth.shape,
            transform=transform, dtype="uint8").astype(bool)
        rows.append({"shift_m": (dx, dy), "wet_inside": (depth[inside] > 0).mean(),
                     "wet_outside": (depth[~inside] > 0).mean(),
                     "deep_inside": (depth[inside] >= 0.3).mean(),
                     "deep_outside": (depth[~inside] >= 0.3).mean()})
    return pd.DataFrame(rows)


alignment = footprint_alignment(RAW / f"reachout/Logrono/Baseline/{RETURN_PERIOD}.tif", b.geometry,
                                [(0, 0), (4, 0), (-4, 0), (0, 4), (0, -4)])
print(alignment.round(4).to_string(index=False))
assert alignment["wet_inside"].idxmin() == 0, "REACHOUT and Cadastre footprints are misaligned"

EBRO_WINDOW = shapely.box(543500, 4701500, 547600, 4703300)
channel = shapely.union_all(floods[30].values).intersection(EBRO_WINDOW)
water_check = []
for name, w in [("Urban Atlas 50000", water_geom),
                ("EU-Hydro river + inland water", euhydro_river.union(euhydro_inland)),
                ("EU-Hydro river surfaces only", euhydro_river)]:
    w = w.intersection(EBRO_WINDOW)
    cover = {(dx, dy): channel.intersection(shapely.affinity.translate(w, dx, dy)).area / channel.area
             for dx in range(-60, 61, 10) for dy in range(-60, 61, 10)}
    best = max(cover, key=cover.get)
    water_check.append({"mask": name, "channel_covered": cover[(0, 0)], "best_shift_m": best,
                        "covered_at_best_shift": cover[best]})
water_check = pd.DataFrame(water_check)
print(water_check.round(3).to_string(index=False))
assert water_check.iloc[0]["best_shift_m"] == (0, 0) and water_check.iloc[0]["channel_covered"] > 0.7

floods = {d: gpd.GeoSeries(g.difference(water_geom), crs=CRS).explode(index_parts=False)
          for d, g in floods.items()}
floods = {d: g[~g.is_empty] for d, g in floods.items()}
for d, g in floods.items():
    print(f"depth ≥ {d} cm: {len(g):,} polygons, {g.area.sum() / 1e6:.3f} km²")

# %% [markdown]
# ## 5. Impact places
#
# Each place in `data/impacts/logrono_events.csv` gets one geometry, by an explicit rule:
#
# - **streets** — the Cadastre address points of the official thoroughfare name (e.g.
#   `CL CLAVIJO`); the Cadastre confirms *calle* Ebro exists (OSM has only Avenida del Ebro);
# - **places without an address** — OpenStreetMap ways from the committed cache
#   (`osm_features.json`): the calle Clavijo **tunnel** under the N-111 (tunnel=yes); the
#   **LO-20** (sunken, layer −1) within 60 m of the ways named *Rotonda Calle Chile*; the
#   whole LO-20 in the municipality; the Adarraga, Palacio de los Deportes and C.A.R.P.A.
#   ways; for "rotonda de club Deportivo" (no roundabout of that name in OSM) the
#   roundabouts touching *Avenida Club Deportivo* — `precision = approximate`;
# - "calle Clavijo, cerca del Palacio de Deportes" — the OSM calle Clavijo ways within
#   100 m of the Palacio de los Deportes (the nearest Clavijo address is 195 m away: that
#   stretch runs along sports grounds, with no front doors).

# %%
def cadastre_streets(gml: Path) -> gpd.GeoDataFrame:
    """Address points with their thoroughfare name (INSPIRE AD links names by xlink)."""
    ns = {"AD": "urn:x-inspire:specification:gmlas:Addresses:3.0",
          "GN": "urn:x-inspire:specification:gmlas:GeographicalNames:3.0",
          "gml": "http://www.opengis.net/gml/3.2", "xlink": "http://www.w3.org/1999/xlink"}
    root = ET.parse(gml).getroot()
    names = {tn.get(f"{{{ns['gml']}}}id"): tn.find(".//GN:text", ns).text.strip()
             for tn in root.iter(f"{{{ns['AD']}}}ThoroughfareName")}
    rows = []
    for a in root.iter(f"{{{ns['AD']}}}Address"):
        x, y = map(float, a.find(".//gml:pos", ns).text.split())
        refs = [c.get(f"{{{ns['xlink']}}}href", "").lstrip("#") for c in a.findall("AD:component", ns)]
        street = next((names[r] for r in refs if r in names), None)
        rows.append({"street": street, "geometry": shapely.Point(x, y)})
    assert rows, "no addresses parsed: check the GML namespaces"
    return gpd.GeoDataFrame(rows, crs=CRS)


def osm_ways(path: Path) -> gpd.GeoDataFrame:
    osm = json.loads(path.read_text())
    rows = [{"osm_id": e["id"], **{k: e["tags"].get(k) for k in
             ("name", "ref", "highway", "junction", "tunnel", "layer")},
             "geometry": LineString([(p["lon"], p["lat"]) for p in e["geometry"]])}
            for e in osm["elements"] if e["type"] == "way"]
    g = gpd.GeoDataFrame(rows, crs="EPSG:4326").to_crs(CRS)
    closed = g.geometry.apply(lambda l: l.is_ring and len(l.coords) > 3)
    area_ids = {40960705, 46108020, 1000277119}   # Adarraga, Palacio de los Deportes, CARPA
    g.loc[closed & g["osm_id"].isin(area_ids), "geometry"] = g.loc[
        closed & g["osm_id"].isin(area_ids), "geometry"].apply(Polygon)
    return g


addresses = cadastre_streets(RAW / "cadastre_addresses/A.ES.SDGC.AD.26900.gml")
osm = osm_ways(IMPACTS / "osm_features.json")


def street(name: str):
    pts = addresses[addresses["street"] == name]
    assert len(pts), name
    return shapely.union_all(pts.geometry.values)


def osm_union(mask: pd.Series):
    assert mask.any()
    return shapely.union_all(osm[mask].geometry.values)


ref = osm["ref"].fillna("")
lo20 = osm_union(ref.str.contains(r"(?:^|;)LO-20(?:;|$)"))
rotonda_chile = osm_union(osm["name"] == "Rotonda Calle Chile")
lo20_sunken = osm[ref.str.contains("LO-20") & (osm["layer"] == "-1")]
palacio = osm_union(osm["osm_id"] == 46108020)
club_dep = osm_union(osm["name"] == "Avenida Club Deportivo")
roundabouts = osm[osm["junction"] == "roundabout"]

PLACES = {
    "calle Clavijo, bajo la N-111": ("exact", osm_union((osm["name"] == "Calle Clavijo") & (osm["tunnel"] == "yes"))),
    "calle Clavijo": ("street", street("CL CLAVIJO")),
    "el Adarraga (Centro de Tecnificación Deportiva Javier Adarraga, Las Norias)":
        ("approximate", osm_union(osm["osm_id"] == 40960705)),
    "circunvalación LO-20": ("road", lo20),
    "calle Ebro": ("street", street("CL EBRO")),
    "avenida Colón": ("street", street("AV COLON")),
    "avenida de Colón": ("street", street("AV COLON")),
    "calle Clavijo, cerca del Palacio de Deportes":
        ("exact", osm_union((osm["name"] == "Calle Clavijo") & (osm.distance(palacio) <= 100))),
    "circunvalación LO-20, bajo la rotonda de la calle Chile":
        ("exact", shapely.union_all(lo20_sunken[lo20_sunken.distance(rotonda_chile) <= 60].geometry.values)),
    "CARPA (Urgencias), aparcamiento y salas de espera": ("exact", osm_union(osm["osm_id"] == 1000277119)),
    "calle San Gregorio": ("street", street("CL SAN GREGORIO")),
    "Paseo del Espolón": ("street", street("PS ESPOLON")),
    "rotonda de club Deportivo":
        ("approximate", shapely.union_all(roundabouts[roundabouts.intersects(club_dep)].geometry.values)),
    "avenida de Burgos": ("street", street("AV BURGOS")),
}

events = pd.read_csv(IMPACTS / "logrono_events.csv")
missing = set(events["place"]) - set(PLACES)
assert not missing, f"no location rule for: {missing}"
events["precision"] = events["place"].map(lambda p: PLACES[p][0])
impact_places = gpd.GeoDataFrame(events, geometry=[PLACES[p][1] for p in events["place"]], crs=CRS)
empty = sorted(set(impact_places.loc[impact_places.geometry.is_empty, "place"]))
assert not empty, f"empty location for: {empty}"
impact_places[["event_date", "place", "place_type", "precision", "source_kind", "geometry"]]

# %% [markdown]
# ## Write

# %%
write(sections, "sections")
write(b, "buildings")
write(gpd.GeoDataFrame(geometry=[urban], crs=CRS), "urban_area")
write(gpd.GeoDataFrame(geometry=[streets], crs=CRS), "streets")
write(gpd.GeoDataFrame(geometry=[streets_ua], crs=CRS), "streets_urban_atlas")
write(gpd.GeoDataFrame(geometry=[water_geom], crs=CRS), "water")
for d, g in floods.items():
    write(gpd.GeoDataFrame(geometry=g.values, crs=CRS), f"flood_rp100_{d}")
write(impact_places, "impact_places")

# %% [markdown]
# ## 6. Deviations from the paper introduced in this step
#
# 1. **Hazard model**: REACHOUT SaferRAIN (hydrostatic fill-and-spill with Green-Ampt
#    infiltration, no sewer network, 15-min design storm of 26.77 mm for RP100) instead of
#    the 2-D VISDOM–SWMM model with a 60-min Euler-II storm of 36 mm.
# 2. **Grid**: 2 m (paper: 1 m), in UTM zone 32; polygons, not depths, are reprojected.
# 3. **Population and social data**: census sections, shared among buildings by dwellings
#    (the paper's example used synthetic building-level data and did not disaggregate).
# 4. **Indicators**: census proxies (§1), not the paper's exact definitions.
# 5. **Ground floor**: residential main use → residents / floors; no per-floor use data.
# 6. **Streets**: gaps between Cadastre urban blocks (25 m closing) minus water, not road
#    polygons.
# 7. **Water bodies removed from the flood layers** (Urban Atlas class 50000): the
#    rain-on-grid model also fills the river bed, which is not pluvial flooding.
