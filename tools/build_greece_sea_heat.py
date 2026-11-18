#!/usr/bin/env python3
"""Build the Greece "hot summer sea" notebook (ERA5 sea surface temperature vs normal; free Copernicus account).

    python tools/build_greece_sea_heat.py            # write greece_sea_heat.ipynb + greece_sea_qr.png
    python tools/build_greece_sea_heat.py --run DIR  # also execute it in DIR, keep outputs, copy the PNG here
"""
import os, sys, shutil
import nbformat as nbf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_unicef import PIP_CDS, KEY_MD, KEY, IMPORTS, C_LICENCE
OWN_KEY_MD = ("\n\n**Use your own key.** Everyone who runs this notebook needs their own free Copernicus account and key. "
              "The next cell asks for it in a hidden box and saves it to `~/.cdsapirc` on the machine running the notebook "
              "(in Colab that is a temporary machine, wiped when you close the tab). The key is never stored in the notebook, "
              "so don't paste it into a code cell, and don't share a notebook or screenshot that shows it. "
              "On your own computer with a `~/.cdsapirc` already in place, the cell uses that and asks nothing.")
KEY_MD = KEY_MD.rstrip() + OWN_KEY_MD

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME, PNG, QR = "greece_sea_heat.ipynb", "greece_sea_heat.png", "greece_sea_qr.png"
COLAB = "https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/"
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

CELLS = [
md(f"""# How warm was the sea around Greece? 🌊
### Copernicus Climate Change Service · ERA5 · free account

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB}{NAME})

In summer 2026 the seas around Greece were warmer than the 1991–2020 average on every day from June to September.
This notebook maps one day, **21 July 2026**, when the seas around Greece were on average about 2 °C warmer than normal,
using **ERA5**, the Copernicus reanalysis produced by ECMWF.

*In Google Colab? Press **Runtime → Run all**. The Climate Data Store queues requests, so step 2 can take a few minutes.*"""),
code(PIP_CDS), md(KEY_MD), code(KEY), code(IMPORTS),
md("## 1 · Choose the day and the area"),
code('''AREA  = [43.5, 13.0, 30.5, 36.5]          # north, west, south, east: Ionian, Aegean, Cretan and Libyan Seas
YEAR, MONTH, DAY = "2026", "07", "21"
NORMAL = [str(y) for y in range(1991, 2021)]  # the WMO 30-year baseline
CITIES = [("Athens", 37.984, 23.728), ("Heraklion", 35.339, 25.144), ("Rhodes", 36.434, 28.217), ("Patras", 38.246, 21.735)]'''),
md("""## 2 · Get the sea surface temperature

One field for the day, and the July average of each year from 1991 to 2020 from the *monthly means* dataset."""),
code('''day = ekd.from_source("cds", "reanalysis-era5-single-levels", {
    "product_type": "reanalysis", "variable": "sea_surface_temperature",
    "year": YEAR, "month": MONTH, "day": DAY, "time": "12:00", "area": AREA}).to_xarray()
normal = ekd.from_source("cds", "reanalysis-era5-single-levels-monthly-means", {
    "product_type": "monthly_averaged_reanalysis", "variable": "sea_surface_temperature",
    "year": NORMAL, "month": MONTH, "time": "00:00", "area": AREA}).to_xarray()

sst_day = day["sst"].squeeze()
tdim = [d for d in normal["sst"].dims if d not in ("latitude", "longitude")]
sst_normal = normal["sst"].mean(tdim)
anomaly = (sst_day - sst_normal.values).squeeze()
print(f"Average sea temperature in the box: {float(sst_day.mean()) - 273.15:.1f} °C, "
      f"{float(anomaly.mean()):+.1f} °C compared with July 1991–2020")'''),
md("## 3 · Map it"),
code('''# blue below normal, white-to-red above it (white sits at 0)
colors = ["#4393c3", "#92c5de", "#fde0d2", "#fbbfa3", "#f4a582", "#e7785c", "#d6604d", "#b2182b", "#8c0d25", "#5c0016"]
style = ekp.styles.Style(levels=[-1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4], colors=colors, extend="both")
chart = ekp.Map(domain=[AREA[1], AREA[3], AREA[2], AREA[0]], figsize=(12, 7))
chart.contourf(anomaly, style=style)
chart.land(color="#e9ecf1"); chart.coastlines(linewidth=0.7); chart.borders(linewidth=0.5)
for name, la, lo in CITIES:
    chart.scatter(x=[lo], y=[la], s=30, color="#ffd23f", edgecolors="#1a1a1a", zorder=10)
    chart.ax.text(lo, la, f"  {name}", transform=ccrs.PlateCarree(), fontsize=10, fontweight="bold", zorder=11,
                  path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
chart.legend(label="Sea surface temperature compared with July 1991–2020 (°C)")
chart.title(f"The sea around Greece on {DAY}/{MONTH}/{YEAR}, compared with normal", fontsize=14)
chart.attribution("Generated using Copernicus Climate Change Service information 2026")
chart.save("greece_sea_heat.png")
chart.show()'''),
md("""## 4 · Your turn 🌍

- **Another day:** change `MONTH` and `DAY`, for example `"08"`, `"16"` (the coolest spell of the summer).
- **The Meltemi signature:** look at the eastern Aegean near the Turkish coast. Strong northerly winds pull cooler water up
  from below, so it often stays close to normal while the rest of the sea is warm.
- **Absolute temperature:** plot `sst_day - 273.15` instead of `anomaly` to see the sea in °C.

""" + C_LICENCE),
]


def write(rundir=None):
    nb = nbf.v4.new_notebook(cells=CELLS, metadata={
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
        shutil.copy(os.path.join(rundir, PNG), os.path.join(HERE, PNG))
    nbf.write(nb, os.path.join(HERE, NAME)); print("wrote", NAME, flush=True)


def qr():
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
    from qrcode.image.styles.colormasks import RadialGradiantColorMask
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=16, border=3)
    q.add_data(COLAB + NAME); q.make(fit=True)
    q.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(),
                 color_mask=RadialGradiantColorMask(back_color=(255, 255, 255), center_color=(0, 61, 107),
                                                    edge_color=(42, 134, 193))).save(os.path.join(HERE, QR))
    print("wrote", QR, "->", COLAB + NAME)


if __name__ == "__main__":
    write(sys.argv[sys.argv.index("--run") + 1] if "--run" in sys.argv else None)
    qr()
