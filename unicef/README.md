# UNICEF — ECMWF open data for the places UNICEF works

Six notebooks: two from ECMWF open data with no account, four from Copernicus with a free key. The open-data ones have a `PLACES` list of countries
where UNICEF responded to, or prepared for, weather and climate hazards in 2025–26 (Philippines, Somalia,
Mozambique, Malawi, Madagascar, Honduras, Chad, Pakistan).

**Where will the rain fall?** The next 10 days at 9 km.
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/unicef/rain_forecast.ipynb)

<img src="rain_qr.png" width="200" align="left" hspace="20"/>
<img src="rain_map.png" width="300"/>

<br clear="all"/>

**How sure are we?** The chance of heavy rain from two open ensembles, IFS ENS (physics) and AIFS ENS (machine learning).
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/unicef/ensemble_probability.ipynb)

<img src="ensemble_qr.png" width="200" align="left" hspace="20"/>
<img src="ensemble_probability.png" width="420"/>

<br clear="all"/>

### Copernicus data (free account and key)

Copernicus data, run by ECMWF for the EU, is free and open too; the data stores ask you to register once. Each
notebook asks for your key with a hidden prompt and keeps it only for the Colab session.

**El Niño in ECMWF's seasonal forecast** (C3S, SEAS5). UNICEF's October 2026 El Niño analysis used the September run.
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/unicef/seasonal_elnino.ipynb)

<img src="seasonal_qr.png" width="200" align="left" hspace="20"/>
<img src="seasonal_elnino.png" width="360"/>

<br clear="all"/>

**Look back at a cyclone with ERA5** (C3S reanalysis, 1940 to now). Cyclone Gezani, Madagascar, February 2026.
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/unicef/cyclone_era5.ipynb)

<img src="cyclone_qr.png" width="200" align="left" hspace="20"/>
<img src="cyclone_era5.png" width="300"/>

<br clear="all"/>

**The air children breathe, five days ahead** (CAMS). PM2.5 over South Asia; switch to Mongolia in one line.
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/unicef/air_quality_cams.ipynb)

<img src="air_qr.png" width="200" align="left" hspace="20"/>
<img src="air_quality_cams.png" width="360"/>

<br clear="all"/>

**Counting hot days with ERA5-Land** (C3S). Days at or above 35 °C, the measure in UNICEF's Children's Climate Risk Report 2026.
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/piddy376/visits-weather-notebooks/blob/main/unicef/hot_days_era5land.ipynb)

<img src="hot_qr.png" width="200" align="left" hspace="20"/>
<img src="hot_days_era5land.png" width="420"/>

<br clear="all"/>

---

## Data & licence

ECMWF Open Data is free under **Creative Commons CC-BY-4.0**
([Terms of Use](https://apps.ecmwf.int/datasets/licences/general/)):
`© ECMWF · Source: www.ecmwf.int · CC-BY-4.0 and ECMWF Terms of Use`.

Copernicus data (C3S, CAMS), produced by ECMWF for the European Union, is free and open under the Copernicus licence:
*Generated using Copernicus Climate Change Service / Atmosphere Monitoring Service information 2026.*

Notebooks by Emma Pidduck · ECMWF User Services.
