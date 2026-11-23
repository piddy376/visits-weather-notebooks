# Weather and climate notebooks from ECMWF open data

Interactive notebooks made for ECMWF liaison visits and partners. **Scan a QR** (or click a Colab badge), press
**Runtime → Run all**, and make a live map from ECMWF and Copernicus data, then change one line to make it for your own
place, day or variable. Everything runs in Google Colab: nothing to install, and a phone or a slow connection is fine.

Each folder has its own page with every notebook, its QR code and a preview.

| Folder | For | Notebooks | Data |
|---|---|---|---|
| [`greece/`](greece/) 🇬🇷 | ECMWF liaison visit to HNMS, Athens, November 2026 | 8 | IFS 9 km, wave model, HNMS stations, DWD ICON-EU, ERA5, ERA5-Land, CAMS |
| [`france/`](france/) 🇫🇷 | ECMWF liaison visit to Météo-France, Toulouse, 2026 | 3 | wave model, ERA5, ERA5-Land |
| [`sweden/`](sweden/) 🇸🇪 | ECMWF liaison visit to SMHI, Norrköping, 2026 | 3 | ERA5, ERA5-Land, CAMS |
| [`china/`](china/) 🇨🇳 | ECMWF–China bilateral meeting, 2026 | 2 | IFS, AIFS Single, ERA5-Land |
| [`germany/`](germany/) 🇩🇪 | ECMWF liaison visit to Germany, 2026 | 1 | IFS 9 km |
| [`poland/`](poland/) 🇵🇱 | ECMWF liaison visit to Poland, 2026 | 1 | CAMS European air quality, IFS 9 km |
| [`italy/`](italy/) 🇮🇹 | ECMWF liaison visit to Italy, 2026 | 1 | CAMS European air quality, IFS 9 km |
| [`canada/`](canada/) 🇨🇦 | ECMWF liaison visit to Canada, 2026 | 1 | IFS 9 km |
| [`senegal/`](senegal/) 🇸🇳 | Strengthening Early Warnings for Africa (SEWA), in English, French and Portuguese | 4 (× 3 languages) | IFS 9 km, AIFS, CAMS, ERA5 |
| [`unicef/`](unicef/) | UNICEF: the places UNICEF works | 6 | IFS 9 km, IFS ENS, AIFS ENS, SEAS5, ERA5, ERA5-Land, CAMS |
| [`hungary/`](hungary/) 🇭🇺 | ECMWF liaison visit to Hungary, 2026 | 1 | IFS 9 km |
| [`bulgaria/`](bulgaria/) 🇧🇬 | ECMWF liaison visit to Bulgaria, 2026 | 1 | IFS 9 km |

**Open data, no account:** ECMWF open data (IFS, AIFS, the wave model, the ensembles), HNMS stations on data.gov.gr,
DWD open data. **Copernicus, free key:** ERA5, ERA5-Land, SEAS5 (C3S) and CAMS; each of these notebooks explains how
to register and asks for the key in a hidden box that is kept only for the Colab session.

The four notebooks that used to sit at the top level (`bulgaria_forecast`, `hungary_forecast`, `greece_forecast`,
`greece_sea_heat`) now live in their country folders. The files left here only point to the new place, so QR codes
already printed still work.

## Repository layout

```
<country or partner>/   notebooks (.ipynb), their preview maps (.png), QR codes (*_qr.png), README.md
assets/                 logos used in the notebook headers
tools/                  scripts that build and run notebooks (make_qr.py makes a Colab QR for any notebook)
```

The Greece notebooks for HNMS stations and IFS × ICON-EU, and the Senegal notebooks, are built in the private
`ms-visit-pack` repository and copied here.

## Data & licence

- **ECMWF Open Data**, CC BY 4.0 ([Terms of Use](https://apps.ecmwf.int/datasets/licences/general/)):
  `© ECMWF · Source: www.ecmwf.int · CC-BY-4.0 and ECMWF Terms of Use`.
- **Copernicus** (C3S, CAMS), produced by ECMWF for the European Union, Copernicus licence:
  *Generated using Copernicus Climate Change Service / Atmosphere Monitoring Service information 2026.*
- **HNMS** station data (data.gov.gr) and **DWD** open data: CC BY 4.0, credited in each notebook.

The code in this repository is under the licence in [`LICENSE`](LICENSE). These are worked examples, not official
ECMWF products. Notebooks by Emma Pidduck · ECMWF User Services.
