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
# # 04 — Figures
#
# 1. **Main result**: where the reported flood places rank among Logroño's streets by
#    modelled flooding, and how that holds across design storms.
# 2. **Risk maps**: building-level risk classes in the centre, with the reported places.
#
# Colours: categorical slots 1–3 (validated all-pairs, colour-vision-deficiency safe;
# marker shapes as secondary encoding); classes on a single-hue blue ordinal ramp.

# %%
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# %%
RESULTS = Path("../results")
FIGURES = Path("../figures")
FIGURES.mkdir(exist_ok=True)
GPKG = Path("../data/interim/logrono.gpkg")
plt.style.use("seaborn-v0_8-whitegrid")
DPI = 150

INK, INK_2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"
SLOTS = {"street": ("#2a78d6", "o", "street (Cadastre addresses)"),
         "exact": ("#eb6834", "D", "exact spot or road (OpenStreetMap)"),
         "approximate": ("#1baf7a", "s", "approximate location")}
CLASS_COLORS = ["#f0efec", "#86b6ef", "#3987e5", "#256abf", "#104281"]   # no risk … very high
CLASS_NAMES = ["no risk", "low", "medium", "high", "very high"]
PLACE_COLOR = "#eb6834"

places = pd.read_csv(RESULTS / "impact_places.csv")
rp = pd.read_csv(RESULTS / "impact_test_return_periods.csv")
tests = pd.read_csv(RESULTS / "impact_test.csv")


def kind(p: str) -> str:
    return "exact" if p in ("exact", "road") else p


def recessive(ax) -> None:
    ax.grid(color=GRID, linewidth=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=INK_2, labelsize=8)

# %% [markdown]
# ## 1. Main result

# %%
def short(name: str) -> str:
    return (name.replace(" (Centro de Tecnificación Deportiva Javier Adarraga, Las Norias)", "")
            .replace(", aparcamiento y salas de espera", "").replace("circunvalación ", ""))


p = places.assign(pct=100 * places["flooded_share_20m_pct"], kind=places["precision"].map(kind))
p = p.sort_values("pct").reset_index(drop=True)
main = tests[(tests["measure"] == "flooded_share_20m") & (tests["places"] == "all places")
             & (tests["baseline"] == "all streets")].iloc[0]

fig, (ax, bx) = plt.subplots(1, 2, figsize=(12, 5.6), gridspec_kw={"width_ratios": [1.5, 1]})
ax.axvline(50, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)))
ax.text(49, -0.6, "median street", color=INK_2, fontsize=8, ha="right", va="center")
for k, (color, marker, _) in SLOTS.items():
    s = p[p["kind"] == k]
    ax.scatter(s["pct"], s.index, s=64, color=color, marker=marker, edgecolor="white", linewidth=1.5, zorder=3)
ax.set_yticks(p.index, [f"{short(n)}  ({e.replace(';', ', ')})" for n, e in zip(p["place"], p["events"])],
              fontsize=8, color=INK)
ax.set_xlim(0, 100)
ax.set_xlabel("Percentile among 512 other streets (modelled flooding ≥ 30 cm, 100-year storm)", color=INK_2, fontsize=9)
ax.set_title(f"Reported flood places: mean {100 * main['mean_percentile']:.0f}th percentile\n"
             f"(one-sided permutation test p < 0.001, n = {int(main['n_places'])})", loc="left", fontsize=10, color=INK)
ax.legend(handles=[Line2D([], [], color=c, marker=m, linestyle="", markersize=7, markeredgecolor="white", label=l)
                   for c, m, l in SLOTS.values()], loc="upper left", fontsize=8, frameon=True, title="Located as",
          title_fontsize=8)
recessive(ax)

order = ["rp2", "rp5", "rp10", "rp25", "rp50", "rp100", "rp200"]
years = [int(r[2:]) for r in order]
for (bname, color, marker) in [("all streets", "#2a78d6", "o"), ("central streets", "#eb6834", "D")]:
    s = rp[rp["baseline"] == bname].set_index("return_period").loc[order]
    bx.plot(years, 100 * s["mean_percentile"], color=color, linewidth=2, marker=marker, markersize=8,
            markeredgecolor="white", markeredgewidth=1.5)
    bx.text(years[-1] * 1.12, 100 * s["mean_percentile"].iloc[-1], f"vs {bname}", color=INK_2, fontsize=8, va="center")
bx.axhline(50, color=MUTED, linewidth=1.2, linestyle=(0, (4, 3)))
bx.text(2, 51.5, "no better than chance", color=INK_2, fontsize=8)
bx.set_xscale("log")
bx.set_xticks(years, [str(y) for y in years])
bx.set_xlim(1.6, 600)
bx.set_ylim(0, 100)
bx.set_xlabel("Design storm return period (years)", color=INK_2, fontsize=9)
bx.set_ylabel("Mean percentile of the 13 places", color=INK_2, fontsize=9)
bx.set_title("Same for every design storm\n(all p < 0.001)", loc="left", fontsize=10, color=INK)
recessive(bx)
fig.tight_layout()
fig.savefig(FIGURES / "main_result.png", dpi=DPI, bbox_inches="tight")
fig.savefig(FIGURES / "main_result.pdf", bbox_inches="tight", metadata={"CreationDate": None})
plt.show()

# %% [markdown]
# ## 2. Risk maps — city centre

# %%
risk = gpd.read_file(RESULTS / "logrono_risk.gpkg", layer="buildings")
impact = gpd.read_file(GPKG, layer="impact_places")
streets = gpd.read_file(GPKG, layer="streets")
x0, y0, x1, y1 = 543300, 4699700, 547700, 4703300

fig, axes = plt.subplots(1, 2, figsize=(13, 6.2))
for ax, (col, title) in zip(axes, [("PFRWB_class", "Risk to well-being (ground-floor residents)"),
                                   ("PFRMA_class", "Risk to mobility and accessibility (all residents)")]):
    streets.plot(ax=ax, color="#f6f5f2")
    impact.plot(ax=ax, color=PLACE_COLOR, markersize=3, linewidth=1.6, alpha=0.9, zorder=2)
    for c in range(5):
        sel = risk[risk[col] == c].cx[x0:x1, y0:y1]
        if len(sel):
            hot = c >= 3
            sel.plot(ax=ax, color=CLASS_COLORS[c], edgecolor=INK if hot else "white",
                     linewidth=1.0 if hot else 0.3, zorder=4 if hot else 3)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_axis_off()
    ax.set_title(title, loc="left", fontsize=10, color=INK)
handles = ([Patch(facecolor=CLASS_COLORS[c], edgecolor=MUTED, linewidth=0.5, label=CLASS_NAMES[c]) for c in range(5)]
           + [Line2D([], [], color=PLACE_COLOR, linewidth=1.6, marker="o", markersize=3, label="reported flood places")])
fig.legend(handles=handles, loc="lower center", ncol=6, fontsize=8, frameon=False)
fig.suptitle("Logroño, 100-year design storm: building-level risk classes (authors' iterated-mean rule)",
             x=0.01, ha="left", fontsize=11, color=INK)
fig.tight_layout(rect=(0, 0.05, 1, 0.96))
fig.savefig(FIGURES / "risk_maps.png", dpi=DPI, bbox_inches="tight")
fig.savefig(FIGURES / "risk_maps.pdf", bbox_inches="tight", metadata={"CreationDate": None})
plt.show()
