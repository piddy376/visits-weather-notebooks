# 🇵🇱 Poland: a weather notebook from ECMWF open data

Made for the ECMWF liaison visit to Poland, 2026.
The notebook runs in Google Colab: **scan the QR** (or click the badge) and press **Runtime → Run all**. Nothing to
install; everything runs on Google's computers, so a phone or a slow connection is fine. It ends with a *Your turn*
section, where one change makes it your own place, day or variable.

| | Notebook | Data | Account |
|---|---|---|---|
| 1 | [Poland's air, the next four days](#1-polands-air-the-next-four-days) | CAMS European air quality × ECMWF IFS 9 km wind | free Copernicus key |

---

### 1. Poland's air, the next four days

The latest CAMS European air quality forecast (PM2.5, or NO₂ with a one-line switch), the most polluted hour
of the next four days, with the ECMWF 9 km 10 m wind at that hour drawn as streamlines: where the wind is light the
pollution stays; where it blows, it moves on. Copernicus data is free and open; the Atmosphere Data Store asks you to
register once. The notebook explains how, and asks for your key in a hidden box that is kept only for the Colab session.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/poland/poland_air_quality.ipynb)

<img src="poland_air_quality_qr.png" width="160" align="left" hspace="20"/>
<img src="poland_air_quality.png" width="420"/>

<br clear="all"/>

---

## Data & licence

- **Copernicus** (CAMS), Copernicus licence: *Generated using Copernicus Atmosphere Monitoring Service information 2026.*
- **ECMWF open data**, CC BY 4.0: `© ECMWF · Source: www.ecmwf.int · CC-BY-4.0 and ECMWF Terms of Use`.

This is a worked example, not an official ECMWF product. Notebooks by Emma Pidduck · ECMWF User Services.
