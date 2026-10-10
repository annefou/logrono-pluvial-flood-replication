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
# # 03 — Risk for Logroño and comparison with recorded flood impacts
#
# **Method**: `building-climate-risk` v0.2.0 (pinned in `pixi.toml`), the open
# implementation that reproduces the authors' Hamburg example (37/37 classes), with the
# paper's settings: TOPSIS weights children 0.3 / elderly singles 0.7, welfare 0.5 /
# education 0.5, SVI 0.5 / 0.5; threshold 0.25 × mean, exponent 2; HWB ring 2 m over
# depths ≥ 30…100 cm; HMA rings 5 / 15 / 30 m at 30 cm; three iterated-mean classes.
#
# 1. Hazards and risk per building (100-year design storm).
# 2. Robustness of the hotspots to the choices made for Logroño.
# 3. **The test** (the paper: building-level resolution "has the potential to
#    significantly enhance the accuracy of urban risk assessments"): are the places where
#    recorded storms caused flooding more flooded in the model than other streets?
#
# This notebook only measures. Interpretation belongs in the Outcome.

# %%
import json
import platform
from importlib.metadata import version
from pathlib import Path

import building_climate_risk as bcr
import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from building_climate_risk.hazards import pluvial

# %%
INTERIM = Path("../data/interim")
RESULTS = Path("../results")
RESULTS.mkdir(parents=True, exist_ok=True)
GPKG = INTERIM / "logrono.gpkg"
CRS = "EPSG:25830"
DEPTHS_CM = list(range(30, 101, 10))
RNG = np.random.default_rng(20261010)
N_PERMUTATIONS = 10_000

SPEC = {
    "vulnerability": {"sensitivity": {"columns": ["C", "ES"], "weights": [0.3, 0.7]},
                      "coping": {"columns": ["WR", "EDQ"], "weights": [0.5, 0.5]},
                      "svi_weights": [0.5, 0.5], "threshold": 0.25, "exponent": 2.0},
    "risks": {"PFRWB": {"exposure": "R_G", "hazard": "HWB"},
              "PFRMA": {"exposure": "R", "hazard": "HMA"}},
    "classes": {"iterations": 3},
}


def layer(name: str) -> gpd.GeoDataFrame:
    return gpd.read_file(GPKG, layer=name)


def tiled(geoms: gpd.GeoSeries, size: float = 100.0) -> gpd.GeoSeries:
    """Cut city-wide polygons into ``size`` m tiles so each ring meets only small pieces
    (same area and geometry once re-merged locally; much faster overlays)."""
    whole = shapely.union_all(geoms.values)
    x0, y0, x1, y1 = whole.bounds
    xs, ys = np.meshgrid(np.arange(x0, x1, size), np.arange(y0, y1, size))
    grid = shapely.box(xs, ys, xs + size, ys + size).ravel()
    pieces = shapely.intersection(whole, grid)
    pieces = pieces[~shapely.is_empty(pieces)]
    return gpd.GeoSeries(pieces, crs=geoms.crs)


buildings = layer("buildings")
streets = tiled(layer("streets").geometry)
water = tiled(layer("water").geometry)
floods = {d: layer(f"flood_rp100_{d}").geometry for d in DEPTHS_CM}
print(f"{len(buildings):,} buildings, {int((buildings['R'] > 0).sum()):,} with residents")

# %% [markdown]
# ## 1. Hazards and risk (RP100)
#
# Hazards are computed for every building (the impact test uses them near any place).
# Risk is assessed over the **buildings with residents** — the population the classes
# describe, as in the paper's example, where every building is residential. For the 0.6 %
# of residents outside the urban area there is no street area, so their mobility hazard
# rests on the 5 m ring only (`streets_available = False`).

# %%
def hazards(footprints: gpd.GeoSeries, street_area: gpd.GeoSeries) -> pd.DataFrame:
    fr = pluvial.mobility_fractions(footprints, floods[30], street_area)
    return pd.DataFrame({"HWB": pluvial.hazard_wellbeing(footprints, floods, buffer=2.0),
                         "HMA": pluvial.hazard_mobility(fr), **fr}, index=footprints.index)


hz = hazards(buildings.geometry, streets)
buildings = buildings.join(hz)
print(hz[["HWB", "HMA"]].describe().round(3).T)

# %%
residents = buildings[buildings["R"] > 0].copy()
base = bcr.assess(residents, {"HWB": residents["HWB"], "HMA": residents["HMA"]}, SPEC)
residents = residents.join(base[["Sensitivity", "CopingCapacity", "SVI", "SVPF",
                                 "PFRWB", "PFRWB_class", "PFRMA", "PFRMA_class"]])
residents["streets_available"] = residents["in_urban_area"]

class_counts = pd.DataFrame({r: residents[f"{r}_class"].value_counts().reindex(range(5), fill_value=0)
                             for r in SPEC["risks"]})
class_counts.index = bcr.CLASS_NAMES
print(class_counts)
residents.to_file(RESULTS / "logrono_risk.gpkg", layer="buildings", driver="GPKG")
residents.drop(columns="geometry").to_csv(RESULTS / "risk_buildings.csv", index=False)

# %% [markdown]
# ## 2. Robustness of the hotspots
#
# Each variant changes one choice and reruns the assessment. A hotspot is a building in
# the "high" or "very high" class. Reported: Spearman rank correlation of the risk index
# with the baseline, and the share of baseline hotspots that remain hotspots.
#
# | Variant | Change |
# |---|---|
# | `WR_disability` | welfare proxy = disability pensioners instead of unemployment |
# | `weights_text` | sensitivity weights children 0.7 / elderly singles 0.3 (the paper's text of Sect. 3.1.1) |
# | `ground_floor_shops` | no ground-floor residents in Urban Atlas continuous urban fabric (class 11100), where ground floors are mostly shops |
# | `streets_urban_atlas` | street area = Urban Atlas roads instead of Cadastre block gaps (HMA recomputed) |

# %%
def variant_spec(**changes) -> dict:
    spec = json.loads(json.dumps(SPEC))
    for path, value in changes.items():
        node = spec
        *keys, last = path.split(".")
        for k in keys:
            node = node[k]
        node[last] = value
    return spec


ua = gpd.read_file("../data/raw/urban_atlas_2018_logrono.geojson").set_crs(CRS, allow_override=True)
continuous = shapely.union_all(ua[ua["code_2018"] == "11100"].geometry.make_valid().values)
shops = residents.representative_point().within(continuous)
hma_ua = hazards(residents.geometry, tiled(layer("streets_urban_atlas").geometry))["HMA"]

VARIANTS = {
    "WR_disability": (residents.assign(WR=residents["WR_disab"]), None, SPEC),
    "weights_text": (residents, None, variant_spec(**{"vulnerability.sensitivity.weights": [0.7, 0.3]})),
    "ground_floor_shops": (residents.assign(R_G=np.where(shops, 0.0, residents["R_G"])), None, SPEC),
    "streets_urban_atlas": (residents, hma_ua, SPEC),
}


def compare_to_base(name: str, out: pd.DataFrame) -> list[dict]:
    rows = []
    for r in SPEC["risks"]:
        hot_base, hot_var = residents[f"{r}_class"] >= 3, out[f"{r}_class"] >= 3
        rows.append({"variant": name, "risk": r,
                     "spearman": residents[r].rank().corr(out[r].rank()),
                     "hotspots_base": int(hot_base.sum()), "hotspots_variant": int(hot_var.sum()),
                     "hotspots_retained": (hot_base & hot_var).sum() / max(hot_base.sum(), 1)})
    return rows


robust = []
for name, (data, hma, spec) in VARIANTS.items():
    hz_v = {"HWB": data["HWB"], "HMA": data["HMA"] if hma is None else hma}
    robust += compare_to_base(name, bcr.assess(data, hz_v, spec))
robust = pd.DataFrame(robust)
robust.to_csv(RESULTS / "robustness.csv", index=False)
print(f"ground-floor-shops variant: {int(shops.sum()):,} buildings in continuous urban fabric")
print(robust.round(3).to_string(index=False))

# %% [markdown]
# ## 3. Do recorded impacts fall where the model floods?
#
# **Units.** Each reported place (one per distinct location; the same place reported in
# several storms counts once) and, as the baseline, every other street of the Cadastre
# register in the urban area, located by its address points.
#
# **Measure.** The flooded share (depth ≥ 30 cm, 100-year storm) of the **open ground**
# within 20 m of the unit — ground that is not a building or water. 20 m reaches the
# street from 90 % of address points (median distance 0 m). Two further measures: the
# mean hazard to mobility (HMA) of buildings within 50 m, and the highest mobility-risk
# class of residential buildings within 50 m (risk includes social vulnerability, which
# impacts cannot test — reported, not tested as such).
#
# **Test.** One-sided permutation test (10,000 label shuffles, fixed seed) of the mean
# percentile of the reported places within the baseline. Subsets and a stricter baseline
# (streets in continuous urban fabric, where press reports concentrate) follow, then the
# same test with the other return periods.

# %%
def open_ground_share(geoms: gpd.GeoSeries, flood: gpd.GeoSeries, radius: float = 20.0) -> np.ndarray:
    zones = gpd.GeoSeries(geoms.buffer(radius).values, crs=CRS)
    blocked = pd.concat([buildings.geometry, water], ignore_index=True)
    tree = shapely.STRtree(blocked.values)
    open_zones = []
    for z in zones.values:
        hits = tree.query(z, predicate="intersects")
        open_zones.append(z.difference(shapely.union_all(blocked.values[hits])) if len(hits) else z)
    return bcr.covered_fraction(gpd.GeoSeries(open_zones, crs=CRS), flood)


def nearby_buildings(geoms: gpd.GeoSeries, radius: float = 50.0) -> pd.DataFrame:
    zones = gpd.GeoDataFrame(geometry=geoms.buffer(radius).values, crs=CRS)
    j = gpd.sjoin(zones, buildings[["HMA", "geometry"]], predicate="intersects")
    jr = gpd.sjoin(zones, residents[["PFRMA_class", "geometry"]], predicate="intersects")
    return pd.DataFrame({"HMA_mean_50m": j.groupby(level=0)["HMA"].mean(),
                         "PFRMA_class_max_50m": jr.groupby(level=0)["PFRMA_class"].max()},
                        index=zones.index).fillna(0)

# %%
reports = layer("impact_places")  # one row per report (from 02)
places = (reports.assign(wkb=reports.geometry.to_wkb())
          .groupby("wkb", sort=False)
          .agg(place=("place", "first"), events=("event_date", lambda s: ";".join(sorted(set(s)))),
               precision=("precision", "first"), place_type=("place_type", "first"),
               press=("source_kind", lambda s: (s == "press").any())))
places = gpd.GeoDataFrame(places.reset_index(drop=True),
                          geometry=gpd.GeoSeries.from_wkb(places.index.values), crs=CRS)
print(f"{len(reports)} reports -> {len(places)} distinct places")

# %% [markdown]
# The baseline streets come from the Cadastre address register (official thoroughfare
# names, written by 02); the streets named in the reports are excluded from it.

# %%
REPORTED_STREETS = {"CL CLAVIJO", "CL EBRO", "AV COLON", "CL SAN GREGORIO", "PS ESPOLON", "AV BURGOS",
                    "AV CLUB DEPORTIVO", "CL CHILE", "PS LAS NORIAS"}
urban = layer("urban_area").geometry.iloc[0]
all_streets = layer("cadastre_streets")
all_streets["geometry"] = all_streets.geometry.intersection(urban)
baseline = all_streets[~all_streets.geometry.is_empty & ~all_streets["street"].isin(REPORTED_STREETS)]
baseline = baseline.reset_index(drop=True)
baseline["central"] = baseline.geometry.centroid.within(continuous)
print(f"baseline: {len(baseline)} streets ({int(baseline['central'].sum())} in continuous urban fabric)")

# %%
def measures(units: gpd.GeoDataFrame, flood: gpd.GeoSeries) -> pd.DataFrame:
    m = nearby_buildings(units.geometry)
    m.insert(0, "flooded_share_20m", open_ground_share(units.geometry, flood))
    return m


place_m = places.join(measures(places, floods[30]))
base_m = baseline.join(measures(baseline, floods[30]))

# %%
def percentile(values: pd.Series, reference: pd.Series) -> np.ndarray:
    ref = np.sort(reference.to_numpy())
    v = values.to_numpy()
    below = np.searchsorted(ref, v, side="left")
    ties = np.searchsorted(ref, v, side="right") - below
    return (below + 0.5 * ties) / len(ref)


def permutation_test(test_vals: np.ndarray, ref_vals: np.ndarray) -> dict:
    pooled = np.concatenate([test_vals, ref_vals])
    k = len(test_vals)
    observed = percentile(pd.Series(test_vals), pd.Series(ref_vals)).mean()
    null = np.empty(N_PERMUTATIONS)
    for i in range(N_PERMUTATIONS):
        perm = RNG.permutation(pooled)
        null[i] = percentile(pd.Series(perm[:k]), pd.Series(perm[k:])).mean()
    return {"n_places": k, "n_baseline": len(ref_vals), "mean_percentile": observed,
            "p_value": (1 + (null >= observed).sum()) / (1 + N_PERMUTATIONS)}


MEASURES = ["flooded_share_20m", "HMA_mean_50m", "PFRMA_class_max_50m"]
SUBSETS = {
    "all places": place_m.index == place_m.index,
    "press only": place_m["press"].to_numpy(),
    "without approximate": (place_m["precision"] != "approximate").to_numpy(),
    "streets only": (place_m["precision"] == "street").to_numpy(),
}
BASELINES = {"all streets": base_m["central"] | ~base_m["central"], "central streets": base_m["central"]}

rows = []
for measure in MEASURES:
    for sub, mask in SUBSETS.items():
        for bname, bmask in BASELINES.items():
            r = permutation_test(place_m.loc[mask, measure].to_numpy(), base_m.loc[bmask, measure].to_numpy())
            rows.append({"measure": measure, "places": sub, "baseline": bname, **r})
tests = pd.DataFrame(rows)
tests.to_csv(RESULTS / "impact_test.csv", index=False)
print(tests.round(3).to_string(index=False))

# %%
for measure in MEASURES:
    place_m[f"{measure}_pct"] = percentile(place_m[measure], base_m[measure])
place_m.drop(columns="geometry").to_csv(RESULTS / "impact_places.csv", index=False)
base_m.drop(columns="geometry").to_csv(RESULTS / "impact_baseline_streets.csv", index=False)
place_m[["place", "events", "precision", "flooded_share_20m", "flooded_share_20m_pct",
         "HMA_mean_50m", "PFRMA_class_max_50m"]].round(3)

# %% [markdown]
# ### Sensitivity to the design storm
#
# The same test on the flooded share at 30 cm for each REACHOUT return period.

# %%
rp_rows = []
for rp in ["rp2", "rp5", "rp10", "rp25", "rp50", "rp100", "rp200"]:
    flood = floods[30] if rp == "rp100" else layer(f"flood_{rp}_30").geometry
    pv = open_ground_share(places.geometry, flood)
    bv = open_ground_share(baseline.geometry, flood)
    for bname, bmask in BASELINES.items():
        rp_rows.append({"return_period": rp, "baseline": bname,
                        **permutation_test(pv, bv[bmask.to_numpy()])})
rp_tests = pd.DataFrame(rp_rows)
rp_tests.to_csv(RESULTS / "impact_test_return_periods.csv", index=False)
print(rp_tests.round(3).to_string(index=False))

# %% [markdown]
# ## Provenance

# %%
provenance = {"building-climate-risk": version("building-climate-risk"), "python": platform.python_version(),
              "geopandas": gpd.__version__, "shapely": shapely.__version__,
              "spec": SPEC, "permutations": N_PERMUTATIONS, "seed": 20261010}
(RESULTS / "run_provenance.json").write_text(json.dumps(provenance, indent=2))
provenance
