#!/usr/bin/env python3
"""Build four Senegal notebooks into senegal/, one per animation in the SEWA set, plus their QR codes.

    heat_forecast.ipynb    ECMWF open data, IFS 9 km 2 m temperature, the next six afternoons (no account)
    aifs_vs_ifs.ipynb      ECMWF open data, AIFS Single and IFS side by side, same run (no account)
    dust_cams.ipynb        CAMS global forecast, dust (free Copernicus key)
    rain_era5.ipynb        ERA5 monthly means, the 2024 rainy season against 1991-2020 (free Copernicus key)

    uv run --with "earthkit-data[cds,ecmwf-opendata]" --with earthkit-plots --with ecmwf-opendata --with nbformat \
           --with nbclient --with ipykernel --with "qrcode[pil]" python tools/build_senegal_stories.py [--run DIR] [--only NAME]
"""
import os, sys, shutil
import nbformat as nbf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_greece_stories import PIP_OD, PIP_CDS, key_md, KEY, OD_LICENCE, c_licence

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "senegal")
COLAB = "https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/senegal/"
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell


def head(title, sub, name, body, wait=False):
    tail = ("*In Google Colab? Press **Runtime → Run all**. The data store queues requests, so step 2 can take a few minutes.*"
            if wait else "*In Google Colab? Press **Runtime → Run all**. Nothing to install, no account needed.*")
    return md(f"""# {title}
### {sub}

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{name})

{body}

{tail}""")


IMPORTS = """import pyproj                     # import before earthkit.data (avoids a crash at exit)
import datetime as dt
import earthkit.data as ekd
import earthkit.plots as ekp
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np"""

CITIES = '''CITIES = [("Dakar", 14.716, -17.467), ("Saint-Louis", 16.018, -16.489), ("Touba", 14.850, -15.883),
          ("Tambacounda", 13.771, -13.667), ("Ziguinchor", 12.583, -16.272), ("Kédougou", 12.557, -12.174)]

def label_cities(ax):
    for name, la, lo in CITIES:
        ax.scatter([lo], [la], s=36, color="#ffd23f", edgecolors="#1a1a1a", linewidths=0.8, zorder=10,
                   transform=ccrs.PlateCarree())
        ax.text(lo, la, f"  {name}", transform=ccrs.PlateCarree(), fontsize=10, fontweight="bold", zorder=11,
                color="#1d2230", path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])'''

HEAT_COLOURS = '["#fff3c4", "#fdd27a", "#f99a3c", "#e0543e", "#a3307e", "#4a1f6a"]'


# ---------------------------------------------------------------------------------------------------------------
def heat():
    name, png = "heat_forecast.ipynb", "heat_forecast.png"
    return name, png, [
head("Senegal's next six afternoons at 9 km 🌡️", "ECMWF free & open data · IFS 9 km · no account needed", name,
     """ECMWF's 9 km forecast (IFS) is **open data**: no login, no fee. This notebook downloads 2 m temperature for
15:00 UTC (15:00 in Dakar) on each of the next six days, prints how hot each afternoon gets in six Senegalese towns,
and maps the hottest one."""),
code(PIP_OD.replace('earthkit-plots', 'earthkit-plots ecmwf-opendata')), code(IMPORTS + "\nfrom ecmwf.opendata import Client"),
md("## 1 · Choose the area"),
code('''AREA  = [17.5, -18.5, 11.5, -10.5]          # north, west, south, east: Senegal and The Gambia
STEPS = [15 + 24 * d for d in range(6)]     # 15 UTC today and the next five days (Dakar is on UTC)
''' + CITIES),
md("## 2 · Get the 9 km forecast (ECMWF open data)"),
code('''result = Client("ecmwf").retrieve(time=0, step=STEPS, stream="oper", type="fc", levtype="sfc",
                                  param="2t", resol="0p1", target="t2m.grib2")      # resol="0p1" = 9 km
run = result.datetime
x = ekd.from_source("file", "t2m.grib2").to_xarray()
x = x.assign_coords(longitude=((x.longitude + 180) % 360) - 180).sortby("longitude")
x = x.sel(latitude=slice(AREA[0] + 0.5, AREA[2] - 0.5), longitude=slice(AREA[1] - 0.5, AREA[3] + 0.5))  # small margin
t2m = x[list(x.data_vars)[0]] - 273.15                                            # kelvin -> °C
sdim = [d for d in t2m.dims if d not in ("latitude", "longitude")][0]
print(f"Forecast run {run:%A %d %B %Y} 00 UTC")
for k, s in enumerate(STEPS):
    v = run + dt.timedelta(hours=s)
    towns = "  ".join(f"{n} {float(t2m.isel({sdim: k}).sel(latitude=la, longitude=lo, method='nearest')):.0f}°"
                      for n, la, lo in CITIES)
    print(f"  {v:%a %d %b} 15 UTC   {towns}")
hot = int(t2m.mean(["latitude", "longitude"]).argmax())                            # the hottest afternoon
day = run + dt.timedelta(hours=STEPS[hot])'''),
md("## 3 · Map the hottest afternoon"),
code('''style = ekp.styles.Style(levels=[24, 26, 28, 30, 32, 34, 36, 38, 40, 42], colors=''' + HEAT_COLOURS + ''', extend="both")
chart = ekp.Map(domain=[AREA[1], AREA[3], AREA[2], AREA[0]], figsize=(11, 8))
chart.contourf(t2m.isel({sdim: hot}), style=style)
chart.coastlines(linewidth=0.7); chart.borders(linewidth=0.6)
label_cities(chart.ax)
chart.legend(label="2 m temperature (°C)")
chart.title(f"Senegal at 15:00 UTC on {day:%A %d %B}, the hottest of the next six afternoons\\n"
            f"ECMWF IFS 9 km forecast from {run:%d %B %Y} 00 UTC", fontsize=13)
chart.attribution("© ECMWF · CC-BY-4.0 · Source: www.ecmwf.int")
chart.save("heat_forecast.png")
chart.show()'''),
md("""## 4 · Your turn 🌍

- **Night-time:** change `15` to `3` in `STEPS` for 03 UTC, the coolest part of the night.
- **The wind:** add `"10u", "10v"` to `param` and draw arrows with `chart.ax.quiver`.
- **Anywhere else:** change `AREA`, for example `[16, -6, 9, 3]` for Burkina Faso.

""" + OD_LICENCE)]


def aifs():
    name, png = "aifs_vs_ifs.ipynb", "aifs_vs_ifs.png"
    return name, png, [
head("AIFS and IFS, side by side over Senegal 🤖", "ECMWF free & open data · machine-learned and physics-based · no account",
     name,
     """ECMWF runs two global forecasts and both are **open data**: the physics-based **IFS** and **AIFS**, the
machine-learned model, which produces a ten-day forecast in minutes. This notebook takes the same run of each, maps
2 m temperature three days ahead side by side, then maps the difference between them."""),
code(PIP_OD), code(IMPORTS),
md("## 1 · Choose the area and the lead time"),
code('''AREA = [22.0, -22.0, 8.0, -6.0]             # north, west, south, east
STEP = 60                                   # hours after the run starts (about two and a half days)
''' + CITIES),
md("## 2 · Get both forecasts (ECMWF open data, 0.25°)"),
code('''def get(model):
    fl = ekd.from_source("ecmwf-open-data", model=model, param="2t", step=STEP).to_fieldlist()
    x = fl.to_xarray()
    x = x.assign_coords(longitude=((x.longitude + 180) % 360) - 180).sortby("longitude")
    x = x.sel(latitude=slice(AREA[0], AREA[2]), longitude=slice(AREA[1], AREA[3]))
    return fl, x[list(x.data_vars)[0]].squeeze() - 273.15

ifs_fl, ifs = get("ifs")
aifs_fl, aifs = get("aifs-single")
run, valid = ifs_fl[0].time.base_datetime(), ifs_fl[0].time.valid_datetime()
assert aifs_fl[0].time.base_datetime() == run, "the two models came from different runs: run the cell again"
diff = aifs - ifs
print(f"Run {run:%d %B %Y %H} UTC, valid {valid:%A %d %B %H}:00 UTC")
print(f"IFS {float(ifs.min()):.0f} to {float(ifs.max()):.0f} °C · AIFS {float(aifs.min()):.0f} to {float(aifs.max()):.0f} °C")
print(f"AIFS minus IFS: mean {float(diff.mean()):+.1f} °C, typical size {float(np.sqrt((diff ** 2).mean())):.1f} °C")'''),
md("## 3 · Map them"),
code('''from matplotlib.colors import BoundaryNorm, ListedColormap
levels = [20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
cmap = ListedColormap(plt.get_cmap("inferno")(np.linspace(0.15, 0.95, len(levels) - 1)))
fig, axs = plt.subplots(1, 3, figsize=(17, 6.2), subplot_kw=dict(projection=ccrs.PlateCarree()))
for ax, da, title in ((axs[0], ifs, "IFS · physics-based"), (axs[1], aifs, "AIFS · machine-learned")):
    m = ax.pcolormesh(da.longitude, da.latitude, da, cmap=cmap, norm=BoundaryNorm(levels, cmap.N))
    ax.set_title(title, fontsize=13, fontweight="bold", loc="left")
fig.colorbar(m, ax=axs[:2], orientation="horizontal", shrink=0.6, pad=0.06, label="2 m temperature (°C)")
d = axs[2].pcolormesh(diff.longitude, diff.latitude, diff, cmap="RdBu_r", vmin=-4, vmax=4)
axs[2].set_title("AIFS minus IFS", fontsize=13, fontweight="bold", loc="left")
fig.colorbar(d, ax=axs[2], orientation="horizontal", pad=0.06, label="Difference (°C)")
for ax in axs:
    ax.set_extent([AREA[1], AREA[3], AREA[2], AREA[0]]); ax.coastlines(lw=0.7); ax.add_feature(__import__("cartopy").feature.BORDERS, lw=0.5)
    ax.plot(-17.467, 14.716, "*", ms=12, color="#ffd23f", mec="#1a1a1a", transform=ccrs.PlateCarree())
fig.suptitle(f"2 m temperature, {valid:%A %d %B %H}:00 UTC, both models run {run:%d %B %Y %H} UTC", fontsize=14)
fig.text(0.5, 0.01, "© ECMWF · CC-BY-4.0 · Source: www.ecmwf.int", ha="center", fontsize=9, color="#555")
fig.savefig("aifs_vs_ifs.png", dpi=110, bbox_inches="tight")
plt.show()'''),
md("""## 4 · Your turn 🌍

- **Further ahead:** `STEP = 144` (six days). The two models usually drift further apart with lead time.
- **Another variable:** `param="10u"` or `"msl"` (mean sea level pressure; divide by 100 for hPa).
- **The ensembles:** both have open ensembles too: `model="aifs-ens"` or `"ifs"` with `stream="enfo"`.

""" + OD_LICENCE)]


def dust():
    name, png = "dust_cams.ipynb", "dust_cams.png"
    page = "https://ads.atmosphere.copernicus.eu/datasets/cams-global-atmospheric-composition-forecasts?tab=download"
    return name, png, [
head("Harmattan dust over West Africa with CAMS 🏜️", "Copernicus Atmosphere Monitoring Service · free account", name,
     """From November to March the dry north-easterly **Harmattan** carries Saharan dust across the Sahel towards the
Atlantic. This notebook maps the dust forecast from the **CAMS global forecast**, run by ECMWF for the European Union,
from yesterday's run up to five days ahead.""", wait=True),
code(PIP_CDS), md(key_md("Atmosphere Data Store", page)), code(KEY), code(IMPORTS),
md("## 1 · Choose the run, the lead time and the area"),
code('''AREA = [27.0, -26.0, 4.0, 10.0]                                   # north, west, south, east
DATE = (dt.date.today() - dt.timedelta(days=1)).isoformat()      # yesterday's run is always complete
LEAD = 72                                                         # hours after 00 UTC, up to 120
''' + CITIES),
md("## 2 · Get the dust forecast"),
code('''cams = ekd.from_source("ads", "cams-global-atmospheric-composition-forecasts", {
    "variable": "dust_aerosol_optical_depth_550nm", "date": f"{DATE}/{DATE}", "time": "00:00",
    "type": "forecast", "leadtime_hour": str(LEAD), "area": AREA, "data_format": "grib"}).to_xarray()
duaod = cams[list(cams.data_vars)[0]].squeeze()
valid = dt.datetime.fromisoformat(DATE) + dt.timedelta(hours=LEAD)
print(f"Dust optical depth up to {float(duaod.max()):.2f} at {valid:%A %d %B %H}:00 UTC")'''),
md("## 3 · Map it"),
code('''colors = ["#f6ecd9", "#efd3a8", "#e6b77d", "#d9955a", "#c27046", "#a34f3c", "#7d3533", "#562126"]
style = ekp.styles.Style(levels=[0.05, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.5], colors=colors, extend="max")
chart = ekp.Map(domain=[AREA[1], AREA[3], AREA[2], AREA[0]], figsize=(12, 8))
chart.contourf(duaod, style=style)
chart.coastlines(linewidth=0.7); chart.borders(linewidth=0.5)
label_cities(chart.ax)
chart.legend(label="Dust aerosol optical depth at 550 nm")
chart.title(f"Desert dust over West Africa, {valid:%A %d %B %H}:00 UTC\\nCAMS global forecast from {DATE} 00 UTC", fontsize=13)
chart.attribution("Generated using Copernicus Atmosphere Monitoring Service information 2026")
chart.save("dust_cams.png")
chart.show()'''),
md("""## 4 · Your turn 🌍

- **Step through the week:** change `LEAD` from 0 to 120 in steps of 3.
- **Dust near the ground:** variable `"dust_aerosol_0.9-20um_mixing_ratio"` is the coarse dust; or try
  `"particulate_matter_10um"` (multiply by 1e9 for µg/m³), which is mostly dust in the Sahel dry season.
- CAMS global runs at about 40 km: it shows where the dust goes, not individual towns.

""" + c_licence("Atmosphere Monitoring Service"))]


def rain():
    name, png = "rain_era5.ipynb", "rain_era5.png"
    page = "https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means?tab=download"
    return name, png, [
head("Senegal's 2024 rainy season in ERA5 🌧️", "Copernicus Climate Change Service · ERA5 · free account", name,
     """How wet was the 2024 rainy season (June to October) compared with a normal year? This notebook uses the
**ERA5 monthly means**, the Copernicus reanalysis that ECMWF produces for the European Union, to compare 2024 with
the 1991–2020 average, as a percentage of normal. The Senegal River rises in the highlands of Guinea and Mali, so the
map covers its whole basin.""", wait=True),
code(PIP_CDS), md(key_md("Climate Data Store", page)), code(KEY), code(IMPORTS),
md("## 1 · Choose the season, the year and the area"),
code('''AREA   = [18.0, -18.5, 9.0, -6.0]                     # north, west, south, east
YEAR   = 2024
MONTHS = ["06", "07", "08", "09", "10"]               # June to October
DAYS   = {"06": 30, "07": 31, "08": 31, "09": 30, "10": 31}
''' + CITIES),
md("## 2 · Get ERA5 monthly rainfall, 1991–2020 and the chosen year"),
code('''era = ekd.from_source("cds", "reanalysis-era5-single-levels-monthly-means", {
    "product_type": "monthly_averaged_reanalysis", "variable": "total_precipitation",
    "year": [str(y) for y in range(1991, 2021)] + [str(YEAR)], "month": MONTHS, "time": "00:00",
    "area": AREA, "data_format": "grib"}).to_xarray()
tp = era[list(era.data_vars)[0]]                                   # metres per day, monthly mean
tdim = [d for d in tp.dims if d not in ("latitude", "longitude")][0]
t = tp[tdim].dt
mm = tp * 1000 * tp[tdim].dt.days_in_month                       # -> mm in each month
season = mm.groupby(t.year).sum(tdim)                             # mm over June-October, each year
normal = season.sel(year=slice(1991, 2020)).mean("year")
this = season.sel(year=YEAR)
pct = 100 * this / normal
print(f"{YEAR}: {float(this.mean()):.0f} mm across the box, normal {float(normal.mean()):.0f} mm "
      f"({float(100 * this.mean() / normal.mean()):.0f}% of normal)")
for n, la, lo in CITIES:
    print(f"  {n:12s} {float(this.sel(latitude=la, longitude=lo, method='nearest')):5.0f} mm, "
          f"{float(pct.sel(latitude=la, longitude=lo, method='nearest')):4.0f}% of normal")'''),
md("## 3 · Map it"),
code('''colors = ["#8c510a", "#bf812d", "#dfc27d", "#f6e8c3", "#f5f5f5", "#c7eae5", "#80cdc1", "#35978f", "#01665e"]
style = ekp.styles.Style(levels=[50, 70, 80, 90, 95, 105, 110, 120, 130, 150], colors=colors, extend="both")
chart = ekp.Map(domain=[AREA[1], AREA[3], AREA[2], AREA[0]], figsize=(12, 7.5))
chart.pcolormesh(pct, style=style)
chart.coastlines(linewidth=0.7); chart.borders(linewidth=0.6)
chart.ax.add_feature(__import__("cartopy").feature.RIVERS, edgecolor="#2b6cb0", linewidth=1.0)
label_cities(chart.ax)
chart.legend(label=f"Rain June–October {YEAR}, % of the 1991–2020 average")
chart.title(f"Senegal's {YEAR} rainy season compared with normal\\nERA5 monthly means", fontsize=13)
chart.attribution("Generated using Copernicus Climate Change Service information 2026")
chart.save("rain_era5.png")
chart.show()'''),
md("""## 4 · Your turn 🌍

- **Another year:** `YEAR = 2020` or any year from 1940.
- **Just the peak months:** `MONTHS = ["08", "09"]`.
- **Hotter or cooler than normal:** `"2m_temperature"` (kelvin) and `this - normal` instead of a percentage.

""" + c_licence("Climate Change Service"))]


JOBS = {"heat": heat, "aifs": aifs, "dust": dust, "rain": rain}
LABELS = {"heat": "heat_qr.png", "aifs": "aifs_qr.png", "dust": "dust_qr.png", "rain": "rain_qr.png"}


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
