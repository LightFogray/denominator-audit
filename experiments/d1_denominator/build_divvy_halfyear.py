#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build grid-level Divvy activity for 2022/2023 half-years."""
from __future__ import annotations
import io, zipfile
from pathlib import Path
import geopandas as gpd
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw/divvy_2022_2023"
OUT = ROOT / "data/processed/d1_denominator"

def main():
    grid = gpd.read_file(ROOT / "data/processed/chicago_grid.geojson")[["grid_id", "geometry"]].to_crs(4326)
    rows = []
    for year in [2022, 2023]:
        for half, months in [("H1", range(1, 7)), ("H2", range(7, 13))]:
            counts = {}
            for m in months:
                f = RAW / f"{year}{m:02d}-divvy-tripdata.zip"
                if not f.exists() or not zipfile.is_zipfile(f):
                    raise FileNotFoundError(f"Missing or invalid monthly activity archive: {f}")
                z = zipfile.ZipFile(f)
                name = [n for n in z.namelist() if n.endswith(".csv") and not n.startswith("__MACOSX")][0]
                df = pd.read_csv(io.BytesIO(z.read(name)), usecols=["start_lat", "start_lng", "end_lat", "end_lng"])
                for lat, lng in [("start_lat", "start_lng"), ("end_lat", "end_lng")]:
                    d = df[[lat, lng]].dropna()
                    g = d.groupby([lat, lng]).size()
                    for (la, ln), n in g.items():
                        k = (round(float(la), 6), round(float(ln), 6))
                        counts[k] = counts.get(k, 0) + int(n)
                print(f.name, len(df), "cum", len(counts))
            pts = pd.DataFrame([(k[1], k[0], v) for k, v in counts.items()], columns=["lon", "lat", "trips"])
            g = gpd.GeoDataFrame(pts, geometry=gpd.points_from_xy(pts.lon, pts.lat), crs=4326)
            j = gpd.sjoin(g, grid, how="inner", predicate="within")
            act = j.groupby("grid_id")["trips"].sum().reindex(range(1246), fill_value=0)
            for gid, val in act.items():
                rows.append(dict(grid_id=gid, fold=f"{year}{half}", activity=float(val)))
            print(year, half, "total", int(act.sum()), "grids", int((act > 0).sum()))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "divvy_halfyear_activity.csv", index=False)
    print(out.groupby("fold")["activity"].sum())

if __name__ == "__main__":
    main()
