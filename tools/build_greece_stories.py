#!/usr/bin/env python3
"""Build four Greece notebooks into greece/, one per animation in the HNMS visit deck, plus their QR codes.

    waves_forecast.ipynb   ECMWF open data, wave model (no account)
    smoke_cams.ipynb       CAMS global forecast + GFAS fires (free Copernicus key)
    dust_cams.ipynb        CAMS global forecast, dust (free Copernicus key)
    heat_era5land.ipynb    ERA5-Land hourly temperature (free Copernicus key)

    uv run --with "earthkit-data[cds,ecmwf-opendata]" --with earthkit-plots --with nbformat --with nbclient \
           --with ipykernel --with "qrcode[pil]" python tools/build_greece_stories.py [--run DIR] [--only NAME]
"""
import os, sys, shutil
import nbformat as nbf

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "greece")
COLAB = "https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/greece/"
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

PIP_OD = ('# Install the open-source tools (Colab / fresh machine). Takes ~1 minute.\n'
          '!pip install -q "earthkit-data[ecmwf-opendata]" earthkit-plots')
PIP_CDS = ('# Install the open-source tools (Colab / fresh machine). Takes ~1 minute.\n'
           '!pip install -q "earthkit-data[cds]" earthkit-plots')


def key_md(store, page):
    return f"""## Your free Copernicus key

Copernicus data is free and open, but the data stores ask you to register once so they can manage the queue:
1. Create an account at [cds.climate.copernicus.eu](https://cds.climate.copernicus.eu) (the same login works for the
   Atmosphere Data Store).
2. Open the [dataset page]({page}) on the {store} and accept its licence (bottom of the Download tab). You only do this once.
3. Copy your API key from your [profile page](https://cds.climate.copernicus.eu/profile) and paste it below.

**Use your own key.** Everyone who runs this notebook needs their own free Copernicus account and key. The next cell asks
for it in a hidden box and saves it on the machine running the notebook (in Colab that is a temporary machine, wiped when
you close the tab). The key is never stored in the notebook, so don't paste it into a code cell, and don't share a notebook
or screenshot that shows it. On your own computer with `~/.cdsapirc` / `~/.adsapirc` already in place, the cell asks nothing."""


KEY = '''import os
from getpass import getpass
rc = {"~/.cdsapirc": "https://cds.climate.copernicus.eu/api", "~/.adsapirc": "https://ads.atmosphere.copernicus.eu/api"}
missing = [p for p in rc if not os.path.exists(os.path.expanduser(p))]
if missing:
    key = getpass("Copernicus API key: ")
    for p in missing:
        with open(os.path.expanduser(p), "w") as f:
            f.write(f"url: {rc[p]}\\nkey: {key}\\n")
print("Copernicus key ready")'''

IMPORTS = """import pyproj                     # import before earthkit.data (avoids a crash at exit)
import datetime as dt
import earthkit.data as ekd
import earthkit.plots as ekp
import cartopy.crs as ccrs
import matplotlib.patheffects as pe
import numpy as np"""

CITIES = '''CITIES = [("Athens", 37.984, 23.728), ("Thessaloniki", 40.640, 22.944), ("Patras", 38.246, 21.735),
          ("Heraklion", 35.339, 25.144), ("Rhodes", 36.434, 28.217)]

def label_cities(chart):
    for name, la, lo in CITIES:
        chart.scatter(x=[lo], y=[la], s=36, color="#ffd23f", edgecolors="#1a1a1a", linewidths=0.8, zorder=10)
        chart.ax.text(lo, la, f"  {name}", transform=ccrs.PlateCarree(), fontsize=10, fontweight="bold", zorder=11,
                      color="#1d2230", path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])'''

OD_LICENCE = """### Data & licence
ECMWF Open Data is free under **Creative Commons CC-BY-4.0**:
`© ECMWF · Source: www.ecmwf.int · CC-BY-4.0 and ECMWF Terms of Use`. No account, no key.

[ECMWF open data](https://www.ecmwf.int/en/forecasts/datasets/open-data) · [earthkit](https://earthkit.ecmwf.int)"""


def c_licence(service):
    return f"""### Data & licence
Copernicus data is free and open under the Copernicus licence (CC-BY 4.0). Credit:
*Generated using Copernicus {service} information 2026.* ECMWF runs the Copernicus Atmosphere Monitoring Service and the
Copernicus Climate Change Service for the European Union.

[Climate Data Store](https://cds.climate.copernicus.eu) · [Atmosphere Data Store](https://ads.atmosphere.copernicus.eu) ·
[earthkit](https://earthkit.ecmwf.int)"""


def head(title, sub, name, body, wait=False):
    tail = ("*In Google Colab? Press **Runtime → Run all**. The data store queues requests, so step 2 can take a few minutes.*"
            if wait else "*In Google Colab? Press **Runtime → Run all**. Nothing to install, no account needed.*")
    return md(f"""# {title}
### {sub}

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name})

{body}

{tail}""")


# ---------------------------------------------------------------------------------------------------------------
def waves():
    name, png = "waves_forecast.ipynb", "waves_forecast.png"
    return name, png, [
head("Waves around Greece, the next six days 🌊", "ECMWF free & open data · wave model · no account needed", name,
     """ECMWF's wave model forecasts the sea state worldwide, and it is **open data**: no login, no fee.
This notebook pulls the latest six-day forecast of **significant wave height** (roughly the height of the biggest third of
the waves), finds the stormiest moment around Greece, and maps it with arrows showing where the waves are heading."""),
code(PIP_OD), code(IMPORTS),
md("## 1 · Choose the area"),
code('''AREA  = [42.0, 18.5, 33.5, 30.5]           # north, west, south, east: Ionian, Aegean, Cretan and Libyan Seas
STEPS = list(range(0, 145, 6))             # every 6 hours, six days ahead
''' + CITIES),
md("## 2 · Get the wave forecast (ECMWF open data)"),
code('''fc = ekd.from_source("ecmwf-open-data", stream="wave", type="fc", param=["swh", "mwd"], step=STEPS)
ds = fc.to_xarray()
ds = ds.assign_coords(longitude=((ds.longitude + 180) % 360) - 180).sortby("longitude")
ds = ds.sel(latitude=slice(AREA[0], AREA[2]), longitude=slice(AREA[1], AREA[3]))
sdim = "step" if "step" in ds.swh.dims else [d for d in ds.swh.dims if d not in ("latitude", "longitude")][0]
storm = int(ds.swh.mean(["latitude", "longitude"]).argmax())     # the stormiest moment over the whole sea
swh, mwd = ds.swh.isel({sdim: storm}), ds.mwd.isel({sdim: storm})
md0 = fc.to_fieldlist()[0].metadata
run = dt.datetime.strptime(f"{md0('dataDate')}{int(md0('dataTime')):04d}", "%Y%m%d%H%M")     # run time from the GRIB header
valid = run + dt.timedelta(hours=STEPS[storm])
print(f"Forecast from {run:%d %B %Y %H} UTC. Stormiest: {valid:%A %d %B %H}:00 UTC, highest waves {float(swh.max()):.1f} m")'''),
md("## 3 · Map it"),
code('''style = ekp.styles.Style(levels=[0, 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6], colors="Blues", extend="max")
chart = ekp.Map(domain=[AREA[1], AREA[3], AREA[2], AREA[0]], figsize=(11, 8))
chart.contourf(swh, style=style)
chart.land(color="#e9ecf1"); chart.coastlines(linewidth=0.7)
# arrows point where the waves are going (mwd is the direction they come from)
th = np.radians(mwd.values[::4, ::4]); lo, la = np.meshgrid(mwd.longitude.values[::4], mwd.latitude.values[::4])
chart.ax.quiver(lo, la, -np.sin(th), -np.cos(th), transform=ccrs.PlateCarree(), color="#1d2230", scale=40, width=0.0022)
label_cities(chart)
chart.legend(label="Significant wave height (m)")
chart.title(f"Waves around Greece, {valid:%A %d %B %H}:00 UTC (the stormiest moment)\\n"
            f"ECMWF wave model forecast from {run:%d %B %Y %H} UTC", fontsize=13)
chart.attribution("© ECMWF · CC-BY-4.0 · Source: www.ecmwf.int")
chart.save("waves_forecast.png")
chart.show()'''),
md("""## 4 · Your turn 🌍

- **A different moment:** set `storm = 0` (now) or any index into `STEPS`, then re-run step 3.
- **Wave period:** add `"mwp"` to `param` and map how long the waves are.
- **Anywhere else:** change `AREA`, for example `[62, -12, 48, 5]` for the North Sea and the British Isles.

""" + OD_LICENCE)]


def smoke():
    name, png = "smoke_cams.ipynb", "smoke_cams.png"
    page = "https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts?tab=download"
    return name, png, [
head("Wildfire smoke over Greece with CAMS 🔥", "Copernicus Atmosphere Monitoring Service · free account", name,
     """On **2 August 2026** fires in West Attica and on Kefalonia sent smoke across Greece. This notebook maps that day
from the **CAMS global forecast** (organic-matter aerosol, which in summer is mostly smoke) and adds the fires detected
by satellite (**CAMS GFAS**). Both are run by ECMWF for the European Union.

GFAS fire data are on the [GFAS dataset page](https://ads.atmosphere.copernicus.eu/datasets/cams-global-fire-emissions-gfas?tab=download):
accept that licence too.""", wait=True),
code(PIP_CDS), md(key_md("Atmosphere Data Store", page)), code(KEY), code(IMPORTS),
md("## 1 · Choose the day and the area"),
code('''AREA = [42.5, 18.0, 34.0, 30.0]            # north, west, south, east
DATE = "2026-08-02"
LEAD = 12                                  # hours after 00 UTC: 12 UTC = 15:00 in Athens
''' + CITIES),
md("## 2 · Get the smoke forecast and the fires"),
code('''cams = ekd.from_source("ads", "cams-global-atmospheric-composition-forecasts", {
    "variable": "organic_matter_aerosol_optical_depth_550nm", "date": f"{DATE}/{DATE}", "time": "00:00",
    "type": "forecast", "leadtime_hour": str(LEAD), "area": AREA, "data_format": "grib"}).to_xarray()
omaod = cams[list(cams.data_vars)[0]].squeeze()

day_before = (dt.date.fromisoformat(DATE) - dt.timedelta(days=1)).isoformat()
gfas = ekd.from_source("ads", "cams-global-fire-emissions-gfas", {
    "variable": "wildfire_radiative_power", "date": f"{day_before}/{DATE}", "area": AREA,
    "data_format": "grib"}).to_xarray()
frp = gfas[list(gfas.data_vars)[0]]
frp = frp.max([d for d in frp.dims if d not in ("latitude", "longitude")])      # strongest over the two days
fl, fo = np.where(frp.values > 0.02)
print(f"Smoke optical depth up to {float(omaod.max()):.2f}; {len(fl)} grid cells with active fires")'''),
md("## 3 · Map it"),
code('''style = ekp.styles.Style(levels=[0.05, 0.1, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2], colors="YlOrBr", extend="max")
chart = ekp.Map(domain=[AREA[1], AREA[3], AREA[2], AREA[0]], figsize=(11, 8))
chart.contourf(omaod, style=style)
chart.coastlines(linewidth=0.7); chart.borders(linewidth=0.5)
chart.scatter(x=frp.longitude.values[fo], y=frp.latitude.values[fl], s=40 + 400 * np.sqrt(frp.values[fl, fo]),
              color="#ff3b1f", edgecolors="#ffe08a", linewidths=0.8, zorder=9)
label_cities(chart)
chart.legend(label="Organic-matter aerosol optical depth at 550 nm (mostly smoke)")
chart.title(f"Wildfire smoke over Greece, {DATE} {LEAD:02d}:00 UTC\\nCAMS global forecast · red: fires detected by satellite (GFAS)",
            fontsize=13)
chart.attribution("Generated using Copernicus Atmosphere Monitoring Service information 2026")
chart.save("smoke_cams.png")
chart.show()'''),
md("""## 4 · Your turn 🌍

- **The Crete fire:** `DATE = "2026-07-31"`. The smoke shows a day after the fire, because the CAMS forecast uses the
  previous day's fire detections.
- **Today:** set `DATE` to yesterday's date for the latest forecast, and `LEAD` up to 120 hours ahead.
- **Fine particles near the ground:** variable `"particulate_matter_2.5um"` (multiply by 1e9 for µg/m³).
- CAMS global runs at about 40 km: it shows where the smoke goes, not individual valleys.

""" + c_licence("Atmosphere Monitoring Service"))]


def dust():
    name, png = "dust_cams.ipynb", "dust_cams.png"
    page = "https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts?tab=download"
    return name, png, [
head("Saharan dust reaches Greece with CAMS 🏜️", "Copernicus Atmosphere Monitoring Service · free account", name,
     """From 11 to 15 November 2026 strong southerly winds carried dust from Libya across the Ionian Sea to Greece. This
notebook maps **Friday 13 November at 12:00 UTC**, when the dust peaked over the Peloponnese and Athens, from the
**CAMS global forecast** run by ECMWF for the European Union. The animation on the slide uses the CAMS European
air-quality forecast (about 10 km); the global forecast here (about 40 km) is kept for longer and shows the whole plume
from the Sahara.""", wait=True),
code(PIP_CDS), md(key_md("Atmosphere Data Store", page)), code(KEY), code(IMPORTS),
md("## 1 · Choose the day and the area"),
code('''AREA = [43.0, 8.0, 26.0, 32.0]             # north, west, south, east: from the Libyan desert to the Balkans
DATE = "2026-11-13"
LEAD = 12                                  # hours after 00 UTC
''' + CITIES),
md("## 2 · Get the dust forecast"),
code('''cams = ekd.from_source("ads", "cams-global-atmospheric-composition-forecasts", {
    "variable": "dust_aerosol_optical_depth_550nm", "date": f"{DATE}/{DATE}", "time": "00:00",
    "type": "forecast", "leadtime_hour": str(LEAD), "area": AREA, "data_format": "grib"}).to_xarray()
duaod = cams[list(cams.data_vars)[0]].squeeze()
print(f"Dust optical depth up to {float(duaod.max()):.2f}")'''),
md("## 3 · Map it"),
code('''colors = ["#f6ecd9", "#efd3a8", "#e6b77d", "#d9955a", "#c27046", "#a34f3c", "#7d3533", "#562126"]
style = ekp.styles.Style(levels=[0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0], colors=colors, extend="max")
chart = ekp.Map(domain=[AREA[1], AREA[3], AREA[2], AREA[0]], figsize=(11, 8))
chart.contourf(duaod, style=style)
chart.coastlines(linewidth=0.7); chart.borders(linewidth=0.5)
label_cities(chart)
chart.legend(label="Dust aerosol optical depth at 550 nm")
chart.title(f"Saharan dust towards Greece, {DATE} {LEAD:02d}:00 UTC\\nCAMS global forecast", fontsize=13)
chart.attribution("Generated using Copernicus Atmosphere Monitoring Service information 2026")
chart.save("dust_cams.png")
chart.show()'''),
md("""## 4 · Your turn 🌍

- **The days before and after:** `DATE = "2026-11-11"` to `"2026-11-15"`.
- **Today and the next five days:** set `DATE` to yesterday and `LEAD` from 0 to 120.
- **Dust near the ground at 10 km:** the CAMS European air-quality forecast (`cams-europe-air-quality-forecasts`,
  variable `"dust"`, `model` `"ensemble"`, `level` `"0"`) for recent dates.

""" + c_licence("Atmosphere Monitoring Service"))]


def heat():
    name, png = "heat_era5land.ipynb", "heat_era5land.png"
    page = "https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=download"
    return name, png, [
head("The hottest week of summer 2026 in Greece 🌡️", "Copernicus Climate Change Service · ERA5-Land · free account", name,
     """The hottest week of summer 2026 in Greece was **22 to 28 August**. This notebook maps its hottest hour,
**Sunday 23 August at 15:00 in Athens**, from **ERA5-Land**, the Copernicus land reanalysis at about 9 km that ECMWF
produces for the European Union. ERA5-Land covers land only, so every island shows and the sea stays blank.""", wait=True),
code(PIP_CDS), md(key_md("Climate Data Store", page)), code(KEY), code(IMPORTS),
md("## 1 · Choose the hour and the area"),
code('''AREA = [42.0, 19.0, 34.5, 30.0]            # north, west, south, east
YEAR, MONTH, DAY, HOUR = "2026", "08", "23", "12:00"   # UTC: 12 UTC = 15:00 in Athens in summer
''' + CITIES),
md("## 2 · Get ERA5-Land"),
code('''era = ekd.from_source("cds", "reanalysis-era5-land", {
    "variable": "2m_temperature", "year": YEAR, "month": MONTH, "day": DAY, "time": HOUR,
    "area": AREA, "data_format": "grib"}).to_xarray()
t2m = era[list(era.data_vars)[0]].squeeze() - 273.15
print(f"{float(t2m.min()):.0f} to {float(t2m.max()):.0f} °C across the land")'''),
md("## 3 · Map it"),
code('''colors = ["#fff3b0", "#ffd27a", "#ffb562", "#f6904a", "#e8623a", "#c93a2e", "#9e1f2a", "#6b0f24"]
style = ekp.styles.Style(levels=[24, 26, 28, 30, 32, 34, 36, 38, 40], colors=colors, extend="both")
chart = ekp.Map(domain=[AREA[1], AREA[3], AREA[2], AREA[0]], figsize=(11, 8))
chart.pcolormesh(t2m, style=style)          # grid cells, so even the smallest islands show
chart.coastlines(linewidth=0.6); chart.borders(linewidth=0.5)
label_cities(chart)
chart.legend(label="2 m temperature (°C)")
chart.title(f"Greece at {HOUR} UTC on {DAY}/{MONTH}/{YEAR}, the hottest hour of summer 2026\\nERA5-Land", fontsize=13)
chart.attribution("Generated using Copernicus Climate Change Service information 2026")
chart.save("heat_era5land.png")
chart.show()'''),
md("""## 4 · Your turn 🌍

- **The night after:** `DAY, HOUR = "23", "23:00"`: the mainland cools fast, the islands stay warm.
- **Another summer:** change `YEAR`. ERA5-Land goes back to 1950.
- **Feels-like heat:** add `"2m_dewpoint_temperature"` and compute the heat index with earthkit-meteo.

""" + c_licence("Climate Change Service"))]


JOBS = {"waves": waves, "smoke": smoke, "dust": dust, "heat": heat}
LABELS = {"waves": "waves_qr.png", "smoke": "smoke_qr.png", "dust": "dust_qr.png", "heat": "heat_qr.png"}


def qr(name, out):
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
    from qrcode.image.styles.colormasks import RadialGradiantColorMask
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=16, border=3)
    q.add_data(COLAB + name); q.make(fit=True)
    q.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(),
                 color_mask=RadialGradiantColorMask(back_color=(255, 255, 255), center_color=(0, 61, 107),
                                                    edge_color=(42, 134, 193))).save(out)
    print(out, "->", COLAB + name)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    rundir = sys.argv[sys.argv.index("--run") + 1] if "--run" in sys.argv else None
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else list(JOBS)
    for key in only:
        name, png, cells = JOBS[key]()
        nb = nbf.v4.new_notebook(cells=cells, metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"}, "colab": {"provenance": []}})
        if rundir:
            from nbclient import NotebookClient
            os.makedirs(rundir, exist_ok=True)
            pip = nb.cells[1].source; nb.cells[1].source = "# (install step skipped for the local run)"
            NotebookClient(nb, timeout=10800, kernel_name="python3", resources={"metadata": {"path": rundir}}).execute()
            nb.cells[1].source = pip; nb.cells[1].outputs = []; nb.cells[1].execution_count = None
            for c in nb.cells:
                if c.cell_type == "code":
                    c.outputs = [o for o in c.outputs if not (o.get("output_type") == "stream" and o.get("name") == "stderr")]
            shutil.copy(os.path.join(rundir, png), os.path.join(OUT, png))
        nbf.write(nb, os.path.join(OUT, name)); print("wrote", name, flush=True)
        qr(name, os.path.join(OUT, LABELS[key]))
