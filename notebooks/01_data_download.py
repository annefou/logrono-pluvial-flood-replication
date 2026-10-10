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
# | Social vulnerability | INE, Censo de Población y Viviendas 2021, indicators per sección censal + section boundaries (01/01/2021) | INE terms (reuse with attribution) |
#
# Only the `Baseline` scenario is extracted from the REACHOUT archive (seven
# return periods, ~44 MB of the 12.5 GB unzipped). The archive is checked against
# the MD5 Zenodo publishes. The Cadastre and INE publish no checksums and
# regenerate their files over time, so the source log (`data/raw/sources.json`)
# records each file's SHA-256 and the server's `Last-Modified` date — that is the
# exact version this run used.
#
# Recorded flood impacts are curated by hand from press reports and versioned in
# the repository (`data/impacts/`), not downloaded here.

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
    {"name": "ine_census2021_indicators", "license": "INE (reuse with attribution)",
     "url": "https://www.ine.es/censos2021/C2021_Indicadores.csv"},
    {"name": "ine_census2021_indicator_definitions", "license": "INE (reuse with attribution)",
     "url": "https://www.ine.es/censos2021/indicadores_seccen_c2021.xlsx"},
    {"name": "ine_census2021_sections", "license": "INE (reuse with attribution)",
     "url": "https://www.ine.es/censos2021/Cartografia_secc.zip",
     "extract": "Seccionado_2021/"},
]


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
# ## Source log

# %%
with open(RAW_DIR / "sources.json", "w") as f:
    json.dump({"accessed_on": datetime.date.today().isoformat(),
               "hazard": hazard_log, "web": web_log}, f, indent=2)

print(f"Logged 1 Zenodo record and {len(web_log)} web source(s) to {RAW_DIR / 'sources.json'}")
