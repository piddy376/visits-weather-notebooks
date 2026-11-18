#!/usr/bin/env python3
"""Build the UNICEF notebooks (open data, no account needed) into unicef/.

    python tools/build_unicef.py            # write the notebooks
    python tools/build_unicef.py --run DIR  # also execute them in DIR, keep outputs, copy the PNGs here
"""
import os, sys, shutil
import nbformat as nbf

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "unicef")
COLAB = "https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/unicef/"
PIP = ('# Install the open-source tools (Colab / fresh machine). Takes ~1 minute.\n'
       '!pip install -q "earthkit-data[ecmwf-opendata]" earthkit-plots')
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

PLACES = '''# Countries where UNICEF responded to, or prepared for, weather and climate hazards in 2025-26
PLACES = {
    "Somalia":     dict(domain=[36.5, 51.6, -2.5, 12.5],      # with the Ethiopian highlands that feed the rivers
                        cities=[("Mogadishu", 2.046, 45.318), ("Beledweyne", 4.736, 45.204), ("Baidoa", 3.114, 43.650),
                                ("Kismayo", -0.358, 42.545), ("Garowe", 8.406, 48.483), ("Hargeisa", 9.560, 44.065)]),
    "Mozambique":  dict(domain=[30.0, 41.0, -27.0, -10.3],
                        cities=[("Maputo", -25.966, 32.583), ("Xai-Xai", -25.052, 33.644), ("Beira", -19.844, 34.839),
                                ("Nampula", -15.116, 39.266)]),
    "Malawi":      dict(domain=[32.0, 36.5, -17.4, -9.2],
                        cities=[("Lilongwe", -13.963, 33.775), ("Blantyre", -15.786, 35.006), ("Nsanje", -16.920, 35.262)]),
    "Madagascar":  dict(domain=[42.8, 51.0, -26.0, -11.7],
                        cities=[("Antananarivo", -18.879, 47.508), ("Toamasina", -18.149, 49.402), ("Toliara", -23.354, 43.669)]),
    "Philippines": dict(domain=[116.5, 127.0, 4.5, 21.0],
                        cities=[("Manila", 14.600, 120.984), ("Virac", 13.580, 124.230), ("Tacloban", 11.244, 125.004),
                                ("Cebu", 10.316, 123.891), ("Davao", 7.190, 125.455)]),
    "Honduras":    dict(domain=[-89.5, -83.0, 12.8, 16.6],
                        cities=[("Tegucigalpa", 14.072, -87.192), ("San Pedro Sula", 15.506, -88.025), ("Choluteca", 13.300, -87.193)]),
    "Chad":        dict(domain=[13.4, 24.1, 7.4, 23.5],
                        cities=[("N'Djamena", 12.134, 15.055), ("Moussoro", 13.641, 16.490), ("Mao", 14.119, 15.313)]),
    "Pakistan":    dict(domain=[60.8, 77.9, 23.6, 37.1],
                        cities=[("Islamabad", 33.684, 73.048), ("Peshawar", 34.015, 71.524), ("Lahore", 31.520, 74.359),
                                ("Karachi", 24.861, 67.010)]),
}'''

LABELS = '''def label_cities(chart, cities, ink="#1d2230", halo="white"):
    for name, lat, lon in cities:
        chart.scatter(x=[lon], y=[lat], s=40, color="#ffd23f", edgecolors="#1a1a1a", linewidths=0.8, zorder=10)
        chart.ax.text(lon, lat, f"  {name}", ha="left", va="center", fontsize=10, fontweight="bold", color=ink, zorder=11,
                      transform=ccrs.PlateCarree(), path_effects=[pe.withStroke(linewidth=2.5, foreground=halo)])'''

LICENCE = '''### Data & licence
ECMWF Open Data is free under **Creative Commons CC-BY-4.0**:
`© ECMWF · Source: www.ecmwf.int · CC-BY-4.0 and ECMWF Terms of Use`. No account, no key.

[ECMWF open data](https://www.ecmwf.int/en/forecasts/datasets/open-data) ·
[earthkit](https://earthkit.ecmwf.int) · [earthkit-data](https://earthkit-data.readthedocs.io) ·
[earthkit-plots](https://earthkit-plots.readthedocs.io)'''


def rain():
    name = "rain_forecast.ipynb"
    return name, ["rain_map.png"], [
md(f"""# Where will the rain fall? The next 10 days at 9 km 🌧️
### ECMWF free & open data · no account needed

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name})

ECMWF's forecasts are **open data**: anyone can download them, with no login and no fee, under a CC-BY-4.0 licence.
This notebook pulls the latest **9 km** forecast of total rainfall for the next ten days and maps it for a country
where UNICEF works. It starts with the **Philippines**, where UNICEF responded to Super Typhoon Fung-wong (Uwan) in
November 2025. Switch to **Somalia** and the map takes in the Ethiopian highlands, where the Juba and Shabelle rivers
that flood Beledweyne begin.

*In Google Colab? Press **Runtime → Run all**. Nothing to install on your own computer.*"""),
code(PIP),
code("""import pyproj                     # import before earthkit.data (avoids a crash at exit)
import earthkit.data as ekd
import earthkit.plots as ekp
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patheffects as pe
import numpy as np"""),
md("""## 1 · Choose the place and the period

Pick any country from the list (or add your own with a `[west, east, south, north]` box), and how many days
of rain to add up (1 to 15)."""),
code(PLACES + """

PLACE = "Philippines"
DAYS  = 10"""),
md("""## 2 · Get the forecast (ECMWF open data, 9 km)

One request. `resol="0p1"` asks for the 0.1° grid (~9 km); `step` is hours from the start of the forecast.
Rainfall (`tp`) is accumulated from the start, so the field at `24 × DAYS` hours *is* the total."""),
code("""rain = ekd.from_source("ecmwf-open-data", time=0, step=24 * DAYS, stream="oper", type="fc",
                      param="tp", resol="0p1").to_fieldlist()
f = rain[0]
start, end = f.time.base_datetime(), f.time.valid_datetime()
print(f"Forecast from {start:%A %d %B %Y %H} UTC, total rain to {end:%A %d %B %H} UTC")"""),
md("## 3 · Map it"),
code(LABELS + """

P = PLACES[PLACE]
chart = ekp.Map(domain=P["domain"])
rain_style = ekp.styles.Style(levels=[1, 5, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500], extend="max", units="mm",
                              colors=["#e3f2fb", "#b9def3", "#86c5e9", "#52a6db", "#2f86c6", "#2867ad",
                                      "#3d4e9c", "#5b3c94", "#7d2d8a", "#a01f77", "#c31863"])
chart.contourf(rain, units="mm", style=rain_style)
chart.ax.add_feature(cfeature.RIVERS.with_scale("10m"), edgecolor="#1f5f99", linewidth=0.9, zorder=4)
chart.borders(linewidth=0.8, color="#555555")
chart.coastlines(linewidth=0.8)
label_cities(chart, P["cities"])
chart.legend(label="Total rainfall (mm)")
chart.title(f"Rain over the next {DAYS} days: {PLACE}\\n"
            f"ECMWF 9 km forecast from {start:%d %B %Y %H} UTC, to {end:%d %B}", fontsize=13)
chart.attribution("Data: © ECMWF, CC BY 4.0 · ECMWF open data")
chart.save("rain_map.png")
chart.show()"""),
md("""## 4 · How much at each place?"""),
code("""lat, lon = f.geography.latlons()
mm = f.to_numpy() * 1000                                                  # metres of water -> millimetres
for name, la, lo in P["cities"]:
    i = np.unravel_index(np.argmin((lat - la) ** 2 + ((lon - lo) * np.cos(np.radians(la))) ** 2), lat.shape)
    print(f"{name:14} {mm[i]:6.0f} mm in {DAYS} days")"""),
md("""## 5 · Your turn 🌍

- **Another country?** Set `PLACE = "Somalia"`, `"Mozambique"`, `"Madagascar"` … and Run all.
- **A shorter or longer window?** `DAYS = 3` for the next three days, up to `DAYS = 15`.
- **Another variable?** `param="2t"` with `units="celsius"` for temperature, `param="msl"` with `units="hPa"` for pressure.
- **How sure is the forecast?** That needs the ensemble: see `ensemble_probability.ipynb` in the same folder.

""" + LICENCE)]


def ensemble():
    name = "ensemble_probability.ipynb"
    return name, ["ensemble_probability.png"], [
md(f"""# How sure are we? Two open ensembles, side by side 🎲
### ECMWF free & open data · IFS ENS and AIFS ENS · no account needed

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name})

A single forecast says *what* is most likely. An **ensemble** of 50 forecasts, each started from slightly different
conditions, says *how likely*. That is the number anticipatory-action plans are built on: act when the chance of
heavy rain passes a threshold.

ECMWF runs two ensembles and both are open data: the physics-based **IFS ENS** and the machine-learning **AIFS ENS**.
This notebook maps, from each, the chance of more than 50 mm of rain in the next five days.

*In Google Colab? Press **Runtime → Run all**.*"""),
code(PIP),
code("""import pyproj                     # import before earthkit.data (avoids a crash at exit)
import earthkit.data as ekd
import earthkit.plots as ekp
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patheffects as pe
import numpy as np"""),
md("## 1 · Choose the place, the window and the threshold"),
code(PLACES + """

PLACE     = "Philippines"
DAYS      = 5        # rain added up over the next DAYS days (1 to 15)
THRESHOLD = 50       # mm"""),
md("""## 2 · Get both ensembles (ECMWF open data, 0.25°)

50 members from each model, rainfall accumulated to `24 × DAYS` hours. About 30 MB per model."""),
code("""def members(model):
    fl = ekd.from_source("ecmwf-open-data", model=model, stream="enfo", type="pf", param="tp",
                         step=24 * DAYS).to_fieldlist()
    da = fl.to_xarray()["tp"]                                               # dims: member, latitude, longitude
    scale = 1000 if fl[0].get("parameter.units") == "m" else 1              # metres -> mm when needed
    return fl, da * scale

ifs, ifs_mm = members("ifs")
aifs, aifs_mm = members("aifs-ens")
start, end = ifs[0].time.base_datetime(), ifs[0].time.valid_datetime()
print(f"{ifs_mm.sizes['member']} IFS and {aifs_mm.sizes['member']} AIFS members, run {start:%d %B %Y %H} UTC")"""),
md("""## 3 · Turn 50 forecasts into a probability

At every grid point, count the members with more than `THRESHOLD` mm. (Plain xarray: a probability of exceedance
is one line.)"""),
code("""prob = {"IFS ENS (physics)": (ifs_mm > THRESHOLD).mean("member") * 100,
        "AIFS ENS (machine learning)": (aifs_mm > THRESHOLD).mean("member") * 100}
for k, p in prob.items():
    p.attrs = {"units": "%", "long_name": f"Chance of more than {THRESHOLD} mm"}"""),
md("## 4 · Map both"),
code(LABELS + """

P = PLACES[PLACE]
style = ekp.styles.Style(levels=[5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                         colors=["#d6ecf5", "#a9d6ea", "#79bfdd", "#4ca5cf", "#2d86bd", "#2a66a6",
                                 "#3f4c96", "#5b3a8e", "#7a2a84", "#9b1c6f"], extend="neither")
fig = ekp.Figure(rows=1, columns=2, figsize=(10.5, 8))
for col, (label, p) in enumerate(prob.items()):
    m = fig.add_map(0, col, domain=P["domain"])
    m.contourf(p, style=style)
    m.ax.add_feature(cfeature.RIVERS.with_scale("10m"), edgecolor="#1f5f99", linewidth=0.8, zorder=4)
    m.borders(linewidth=0.7, color="#555555"); m.coastlines(linewidth=0.7)
    label_cities(m, P["cities"])
    m.title(label, fontsize=13)
fig.legend(label=f"Chance of more than {THRESHOLD} mm of rain in {DAYS} days (%)")
fig.title(f"{PLACE}: chance of heavy rain, {start:%d %b} to {end:%d %b %Y}\\n"
          f"ECMWF ensembles from {start:%d %B %Y %H} UTC, 50 members each", fontsize=14)
fig.attribution("Data: © ECMWF, CC BY 4.0 · ECMWF open data")
fig.save("ensemble_probability.png")
fig.show()"""),
md("## 5 · The numbers at each place"),
code("""lat, lon = ifs[0].geography.latlons()
print(f"Chance of more than {THRESHOLD} mm in {DAYS} days")
print(f"{'':14}{'IFS ENS':>9}{'AIFS ENS':>10}")
for name, la, lo in P["cities"]:
    v = [float(p.sel(latitude=la, longitude=lo % 360 if p.longitude.max() > 180 else lo, method="nearest"))
         for p in prob.values()]
    print(f"{name:14}{v[0]:8.0f}%{v[1]:9.0f}%")"""),
md("""## 6 · Your turn 🌍

- **A different trigger?** Change `THRESHOLD` (20, 100 mm …) and `DAYS`.
- **Another country?** `PLACE = "Somalia"`, `"Mozambique"`, `"Malawi"` …
- **Where do the two models agree?** Try `prob["IFS ENS (physics)"] - prob["AIFS ENS (machine learning)"]`.

""" + LICENCE)]


def write(name, cells, pngs, rundir=None):
    nb = nbf.v4.new_notebook(cells=cells, metadata={
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"}, "colab": {"provenance": []}})
    if rundir:
        from nbclient import NotebookClient
        os.makedirs(rundir, exist_ok=True)
        pip = nb.cells[1].source
        nb.cells[1].source = "# (install step skipped for the local run)"
        NotebookClient(nb, timeout=7200, kernel_name="python3", resources={"metadata": {"path": rundir}}).execute()
        nb.cells[1].source = pip; nb.cells[1].outputs = []; nb.cells[1].execution_count = None
        for c in nb.cells:
            if c.cell_type == "code":
                c.outputs = [o for o in c.outputs if not (o.get("output_type") == "stream" and o.get("name") == "stderr")]
        for p in pngs:
            shutil.copy(os.path.join(rundir, p), os.path.join(OUT, p))
    nbf.write(nb, os.path.join(OUT, name)); print("wrote", name, flush=True)


# ---- Copernicus notebooks (free account + key) --------------------------------------------------
PIP_CDS = ('# Install the open-source tools (Colab / fresh machine). Takes ~1 minute.\n'
           '!pip install -q "earthkit-data[cds]" earthkit-plots')
KEY_MD = """## Your free Copernicus key

Copernicus data is free and open too, but the data stores ask you to register once so they can manage the queue:
1. Create an account at [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu) (the same login works for the
   Atmosphere Data Store).
2. Open the dataset page and accept its licence (Download tab, bottom of the page). You only do this once.
3. Copy your API key from your [profile page](https://cds.climate.copernicus.eu/profile) and paste it below.
   It is kept only for this Colab session and is not saved in the notebook."""
KEY = '''import os
from getpass import getpass
if not os.path.exists(os.path.expanduser("~/.cdsapirc")):
    key = getpass("Copernicus API key: ")
    for url, rc in (("https://cds.climate.copernicus.eu/api", "~/.cdsapirc"),
                    ("https://ads.atmosphere.copernicus.eu/api", "~/.adsapirc")):
        with open(os.path.expanduser(rc), "w") as f:
            f.write(f"url: {url}\\nkey: {key}\\n")
print("Copernicus key ready")'''
IMPORTS = """import pyproj                     # import before earthkit.data (avoids a crash at exit)
import earthkit.data as ekd
import earthkit.plots as ekp
import cartopy.crs as ccrs
import matplotlib.patheffects as pe
import numpy as np"""
C_LICENCE = """### Data & licence
Copernicus data is free and open under the Copernicus licence (CC-BY 4.0 for these datasets). Credit:
*Generated using Copernicus Climate Change Service / Atmosphere Monitoring Service information [year].*
ECMWF runs both services for the European Union.

[Climate Data Store](https://cds.climate.copernicus.eu) · [Atmosphere Data Store](https://ads.atmosphere.copernicus.eu) ·
[earthkit](https://earthkit.ecmwf.int)"""

def seasonal():
    name = "seasonal_elnino.ipynb"
    return name, ["seasonal_elnino.png"], [
md(f"""# El Niño in ECMWF's seasonal forecast 🌊
### Copernicus Climate Change Service · SEAS5 · free account

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name})

UNICEF's October 2026 El Niño analysis combined **ECMWF's September seasonal forecast** with WorldPop child-population
data. ECMWF issues a new seasonal forecast on the 5th of every month, free through the Copernicus Climate Data Store.
This notebook fetches the latest one and maps what it expects for the coming season: sea-surface temperature, where
El Niño shows itself, and rainfall over land, where children feel it.

*In Google Colab? Press **Runtime → Run all**.*"""),
code(PIP_CDS), md(KEY_MD), code(KEY), code(IMPORTS),
md("""## 1 · Choose the forecast and the season

`START` is the month the forecast was issued. Lead month 1 is that month, so for a November start, lead months 2, 3
and 4 are December, January and February."""),
code('''START = "2026-11"
LEADS = [2, 3, 4]                 # December, January, February'''),
md("""## 2 · Get it from the Climate Data Store

The *post-processed* dataset already holds anomalies: the forecast minus ECMWF's own 1993–2016 hindcast climate."""),
code('''year, month = START.split("-")
seas = ekd.from_source("cds", "seasonal-postprocessed-single-levels", {
    "originating_centre": "ecmwf", "system": "51", "product_type": "ensemble_mean",
    "variable": ["sea_surface_temperature_anomaly", "total_precipitation_anomalous_rate_of_accumulation"],
    "year": year, "month": month, "leadtime_month": [str(m) for m in LEADS], "data_format": "grib"}).to_fieldlist()
ds = seas.to_xarray()
sst = ds["ssta"].mean([d for d in ds["ssta"].dims if d not in ("latitude", "longitude")])
rain = ds["tpara"].mean([d for d in ds["tpara"].dims if d not in ("latitude", "longitude")]) * 86400 * 1000   # m/s -> mm/day
nino34 = float(sst.sel(latitude=slice(5, -5), longitude=slice(190, 240)).mean())
print(f"Niño 3.4 sea-surface temperature anomaly, lead months {LEADS}: {nino34:+.1f} °C")'''),
md("## 3 · Map the season"),
code('''sst_style = ekp.styles.Style(levels=[-2.5, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5], colors="RdBu_r", extend="both")
rain_style = ekp.styles.Style(levels=[-3, -2, -1, -0.5, 0.5, 1, 2, 3], colors="BrBG", extend="both")
places = [("Somalia", 2.0, 45.3), ("Malawi", -14.0, 33.8), ("Mozambique", -26.0, 32.6),
          ("Philippines", 14.6, 121.0), ("Honduras", 14.1, -87.2), ("Chad", 12.1, 15.1)]

fig = ekp.Figure(rows=2, columns=1, figsize=(12, 11))
for row, (field, style, label) in enumerate(((sst, sst_style, "Sea-surface temperature anomaly (°C)"),
                                              (rain, rain_style, "Rainfall anomaly (mm/day)"))):
    m = fig.add_map(row, 0, crs=ccrs.Robinson(central_longitude=-160))
    m.contourf(field, style=style)
    m.coastlines(linewidth=0.5)
    for name, la, lo in places:
        m.scatter(x=[lo], y=[la], s=40, color="#ffd23f", edgecolors="#1a1a1a", zorder=10)
        m.ax.text(lo, la + 4, name, transform=ccrs.PlateCarree(), ha="center", fontsize=9, fontweight="bold", zorder=11,
                  path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
    m.legend(label=label)
fig.title(f"ECMWF SEAS5 from {START}: the season ahead (lead months {LEADS[0]}–{LEADS[-1]}), ensemble mean", fontsize=14)
fig.attribution("Generated using Copernicus Climate Change Service information 2026")
fig.save("seasonal_elnino.png")
fig.show()'''),
md("""## 4 · Your turn 🌍

- **Last month's forecast?** Set `START = "2026-09"` to see the run UNICEF used, and compare.
- **Later in the season?** `LEADS = [4, 5, 6]` for February to April.
- **Temperature over land?** Add `"2m_temperature_anomaly"` to the variables (variable `t2a`).
- **Other centres:** the same dataset has forecasts from the UK Met Office, Météo-France, DWD, CMCC and others.

""" + C_LICENCE)]

def cyclone():
    name = "cyclone_era5.ipynb"
    return name, ["cyclone_era5.png"], [
md(f"""# Look back at a cyclone with ERA5 🌀
### Copernicus Climate Change Service · ERA5 reanalysis · free account

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name})

**ERA5** is ECMWF's reconstruction of the weather everywhere on Earth, every hour since 1940. It is how you look back
at an event after it has happened: how much rain fell, where, and how strong the wind was.

This notebook maps **Cyclone Gezani** coming ashore near Toamasina, Madagascar, on 10 February 2026. UNICEF acted
before landfall with CERF early-action funding. Change the date and box to look at any storm since 1940.

*In Google Colab? Press **Runtime → Run all**.*"""),
code(PIP_CDS), md(KEY_MD), code(KEY), code(IMPORTS),
md("## 1 · Choose the event"),
code('''EVENT = "Cyclone Gezani"
DAY   = "2026-02-10"
HOURS = ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]   # UTC; rain is added up over these hours
AREA  = [-10, 42, -27, 56]                                         # north, west, south, east
CITIES = [("Toamasina", -18.149, 49.402), ("Antananarivo", -18.879, 47.508), ("Mahajanga", -15.717, 46.317)]'''),
md("## 2 · Get ERA5 from the Climate Data Store"),
code('''y, m, d = DAY.split("-")
era5 = ekd.from_source("cds", "reanalysis-era5-single-levels", {
    "product_type": "reanalysis", "variable": ["total_precipitation", "10m_u_component_of_wind", "10m_v_component_of_wind"],
    "year": y, "month": m, "day": d, "time": HOURS, "area": AREA, "data_format": "grib"}).to_fieldlist()
ds = era5.to_xarray(time_dims=["valid_time"])                     # one time axis
rain = ds["tp"].sum("valid_time") * 1000                            # metres -> mm over the period
u, v = ds["10u"].isel(valid_time=-1), ds["10v"].isel(valid_time=-1) # wind at the last hour
print(f"Most rain in {len(HOURS)} hours: {float(rain.max()):.0f} mm; strongest 10 m wind: {float(np.hypot(u, v).max()) * 3.6:.0f} km/h")'''),
md("## 3 · Map rain and wind"),
code('''style = ekp.styles.Style(levels=[2, 5, 10, 20, 30, 50, 75, 100], colors="Blues", extend="max")
chart = ekp.Map(domain=[AREA[1], AREA[3], AREA[2], AREA[0]])
chart.contourf(rain, style=style)
chart.ax.streamplot(u.longitude.values, u.latitude.values, u.values, v.values, color="#333333", density=1.6,
                    linewidth=0.7, arrowsize=0.8, transform=ccrs.PlateCarree(), zorder=5)
chart.coastlines(linewidth=0.8); chart.borders(linewidth=0.6)
for name, la, lo in CITIES:
    chart.scatter(x=[lo], y=[la], s=40, color="#ffd23f", edgecolors="#1a1a1a", zorder=10)
    chart.ax.text(lo, la, f"  {name}", transform=ccrs.PlateCarree(), fontsize=10, fontweight="bold", zorder=11,
                  path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
chart.legend(label=f"Rainfall, {HOURS[0]}–{HOURS[-1]} UTC (mm)")
chart.title(f"{EVENT}, {DAY}: ERA5 rainfall and 10 m wind", fontsize=14)
chart.attribution("Generated using Copernicus Climate Change Service information 2026")
chart.save("cyclone_era5.png")
chart.show()'''),
md("""## 4 · Your turn 🌍

- **Super Typhoon Fung-wong (Uwan), Philippines:** `DAY = "2025-11-09"`, `AREA = [20, 118, 10, 130]`.
- **Hurricane Melissa, Jamaica:** `DAY = "2025-10-28"`, `AREA = [22, -82, 14, -72]`.
- ERA5 runs at about 31 km, so it smooths the very core of a cyclone: peak winds come out lower than observed, but the
  rain and the storm's footprint are well captured. For the land at 9 km, try `reanalysis-era5-land`.

""" + C_LICENCE)]

def airq():
    name = "air_quality_cams.ipynb"
    return name, ["air_quality_cams.png"], [
md(f"""# The air children breathe, five days ahead 🌫️
### Copernicus Atmosphere Monitoring Service (CAMS) · free account

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name})

CAMS, run by ECMWF, forecasts air pollution worldwide twice a day, five days ahead: fine particles (PM2.5), dust, smoke,
ozone and more. This notebook maps the latest PM2.5 forecast over **South Asia**, where winter smog fills the
Indo-Gangetic Plain each November. Change the box for **Mongolia**, where UNICEF works on clean air for children in
Ulaanbaatar, or anywhere else.

*In Google Colab? Press **Runtime → Run all**.*"""),
code(PIP_CDS), md(KEY_MD), code(KEY), code(IMPORTS),
md("## 1 · Choose the place and the time"),
code('''import datetime as dt
REGION = "South Asia"
AREA   = [38, 60, 5, 100]                  # north, west, south, east; Mongolia: [53, 86, 40, 120]
DATE   = (dt.date.today() - dt.timedelta(days=1)).isoformat()   # yesterday's run is always complete
LEAD   = 48                                # hours ahead
CITIES = [("Lahore", 31.520, 74.359), ("Delhi", 28.614, 77.209), ("Patna", 25.594, 85.137), ("Dhaka", 23.811, 90.413)]'''),
md("## 2 · Get the CAMS forecast from the Atmosphere Data Store"),
code('''cams = ekd.from_source("ads", "cams-global-atmospheric-composition-forecasts", {
    "variable": "particulate_matter_2.5um", "date": f"{DATE}/{DATE}", "time": "00:00", "type": "forecast",
    "leadtime_hour": str(LEAD), "area": AREA, "data_format": "grib"}).to_fieldlist()
pm = cams.to_xarray()
pm25 = pm[list(pm.data_vars)[0]].squeeze() * 1e9               # kg/m3 -> µg/m3
valid = dt.datetime.fromisoformat(DATE) + dt.timedelta(hours=LEAD)
print(f"Highest PM2.5: {float(pm25.max()):.0f} µg/m³ (WHO 24-hour guideline: 15 µg/m³)")'''),
md("## 3 · Map it"),
code('''style = ekp.styles.Style(levels=[5, 15, 25, 37.5, 50, 75, 100, 150, 200, 300], colors="inferno_r", extend="max")
chart = ekp.Map(domain=[AREA[1], AREA[3], AREA[2], AREA[0]])
chart.contourf(pm25, style=style)
chart.coastlines(linewidth=0.7); chart.borders(linewidth=0.6)
for name, la, lo in CITIES:
    chart.scatter(x=[lo], y=[la], s=40, color="#ffd23f", edgecolors="#1a1a1a", zorder=10)
    chart.ax.text(lo, la, f"  {name}", transform=ccrs.PlateCarree(), fontsize=10, fontweight="bold", zorder=11,
                  path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
chart.legend(label="PM2.5 (µg/m³)")
chart.title(f"Fine particles (PM2.5) over {REGION}, {valid:%A %d %B %H:00} UTC\\nCAMS global forecast from {DATE} 00 UTC",
            fontsize=13)
chart.attribution("Generated using Copernicus Atmosphere Monitoring Service information 2026")
chart.save("air_quality_cams.png")
chart.show()'''),
md("""## 4 · Your turn 🌍

- **Mongolia:** `REGION = "Mongolia"`, `AREA = [53, 86, 40, 120]`, cities `[("Ulaanbaatar", 47.886, 106.906)]`.
- **Desert dust over the Sahel:** variable `"dust_aerosol_optical_depth_550nm"`, `AREA = [25, -20, 5, 40]`.
- **Another day ahead:** `LEAD` up to 120 hours.
- CAMS global runs at about 40 km, so it smooths out pollution trapped in narrow valleys such as Ulaanbaatar's.

""" + C_LICENCE)]

def heat():
    name = "hot_days_era5land.ipynb"
    return name, ["hot_days_era5land.png"], [
md(f"""# Counting hot days with ERA5-Land 🔥
### Copernicus Climate Change Service · ERA5-Land · free account

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name})

UNICEF's **Children's Climate Risk Report 2026** used **ERA5-Land**, at about 9 km, to count extremely hot days
above 35 °C for every place on Earth. This notebook does the same count for one country and one season, here
**Pakistan in May and June 2026**, and compares it with an earlier year.

*In Google Colab? Press **Runtime → Run all**. The Climate Data Store queues requests, so step 2 can take a few minutes.*"""),
code(PIP_CDS), md(KEY_MD), code(KEY), code(IMPORTS),
md("## 1 · Choose the place, the season and the years"),
code('''PLACE     = "Pakistan"
AREA      = [37.5, 60.5, 23.5, 78]           # north, west, south, east
MONTHS    = ["05", "06"]
YEARS     = ["1996", "2026"]                 # thirty years apart
THRESHOLD = 35                               # °C, as in the Children's Climate Risk Report
TIMEZONE  = "utc+05:00"                      # the local day
CITIES    = [("Jacobabad", 28.282, 68.438), ("Lahore", 31.520, 74.359), ("Karachi", 24.861, 67.010),
             ("Peshawar", 34.015, 71.524)]'''),
md("""## 2 · Get the daily maximum temperature

The *daily statistics* dataset computes each day's maximum from the hourly ERA5-Land data for you."""),
code('''hot = {}
for year in YEARS:
    tmax = ekd.from_source("cds", "derived-era5-land-daily-statistics", {
        "variable": "2m_temperature", "year": year, "month": MONTHS, "day": [f"{d:02d}" for d in range(1, 32)],
        "daily_statistic": "daily_maximum", "time_zone": TIMEZONE, "frequency": "1_hourly", "area": AREA}).to_xarray()
    t = tmax[list(tmax.data_vars)[0]] - 273.15
    tdim = [d for d in t.dims if d not in ("latitude", "longitude")][0]
    hot[year] = (t >= THRESHOLD).sum(tdim).where(np.isfinite(t.isel({tdim: 0})))
    print(f"{year}: {float(hot[year].mean()):.0f} days at or above {THRESHOLD} °C on average across the box")'''),
md("## 3 · Map both years"),
code('''style = ekp.styles.Style(levels=[1, 5, 10, 20, 30, 40, 50, 55, 61], colors="YlOrRd", extend="neither")
fig = ekp.Figure(rows=1, columns=len(YEARS), figsize=(13, 6))
for col, year in enumerate(YEARS):
    m = fig.add_map(0, col, domain=[AREA[1], AREA[3], AREA[2], AREA[0]])
    m.contourf(hot[year], style=style)
    m.coastlines(linewidth=0.7); m.borders(linewidth=0.6)
    for name, la, lo in CITIES:
        m.scatter(x=[lo], y=[la], s=30, color="#ffd23f", edgecolors="#1a1a1a", zorder=10)
        m.ax.text(lo, la, f"  {name}", transform=ccrs.PlateCarree(), fontsize=9, fontweight="bold", zorder=11,
                  path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
    m.title(year, fontsize=14)
fig.legend(label=f"Days at or above {THRESHOLD} °C, May–June")
fig.title(f"{PLACE}: extremely hot days from ERA5-Land", fontsize=15)
fig.attribution("Generated using Copernicus Climate Change Service information 2026")
fig.save("hot_days_era5land.png")
fig.show()'''),
md("""## 4 · Your turn 🌍

- **A thirty-year normal:** loop `YEARS` over 1991–2020 and average, the baseline ECMWF and WMO use.
- **Hot nights:** `daily_statistic = "daily_minimum"` and a threshold of 25 °C; children sleep badly in hot nights.
- **Another place:** the Sahel (`AREA = [24, 13, 7, 24]` for Chad), or anywhere on land.

""" + C_LICENCE)]


JOBS = {"rain": rain, "ensemble": ensemble, "seasonal": seasonal, "cyclone": cyclone, "airq": airq, "heat": heat}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    rundir = sys.argv[sys.argv.index("--run") + 1] if "--run" in sys.argv else None
    only = [a for a in sys.argv[1:] if a in JOBS] or list(JOBS)
    for job in only:
        name, pngs, cells = JOBS[job]()
        write(name, cells, pngs, rundir)
