"""French versions of the Senegal notebooks: (English, French) replacements applied to the built English cells.

Every pair must match somewhere in its notebook, so a change to the English text that is not mirrored here fails
the build instead of leaving English behind.
"""

DATES = '''
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
        "novembre", "décembre"]
def jour(d): return f"{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]}"     # dates en français
def date(d): return f"{d.day} {MOIS[d.month - 1]} {d.year}"'''

COMMON = [
    ("Made for SEWA, Strengthening Early Warnings for Africa",
     "Réalisé pour SEWA (Strengthening Early Warnings for Africa), le renforcement des alertes précoces en Afrique"),
    ("**What you need:** ", "**Ce qu'il vous faut :** "),
    ("a Google account (to use Colab). No other account, no fee, nothing to install.",
     "un compte Google (pour utiliser Colab). Aucun autre compte, aucun frais, rien à installer."),
    ("a Google account (to use Colab) and a free Copernicus account (step below).",
     "un compte Google (pour utiliser Colab) et un compte Copernicus gratuit (étape ci-dessous)."),
    ("Everything runs on Google's computers: the data is downloaded there, not to your phone\nor laptop, so a slow or mobile connection is fine.",
     "Tout tourne sur les ordinateurs de Google : les données y sont téléchargées, pas sur votre\ntéléphone ou votre ordinateur, donc une connexion lente ou mobile suffit."),
    ("| Data | What this notebook uses | Licence |", "| Données | Ce que ce notebook utilise | Licence |"),
    ("**Tools:** [earthkit](https://earthkit.ecmwf.int), ECMWF's free, open-source Python tools for weather and climate data.",
     "**Outils :** [earthkit](https://earthkit.ecmwf.int), les outils Python libres et gratuits de l'ECMWF pour les données météo et climat."),
    ("*Press **Runtime → Run all**. The first run takes a few minutes, mostly installing the tools.*",
     "*Cliquez sur **Exécution → Tout exécuter** (Runtime → Run all). La première exécution prend quelques minutes, surtout pour installer les outils.*"),
    ("*Press **Runtime → Run all**. The data store queues requests, so step 2 can take a few minutes.*",
     "*Cliquez sur **Exécution → Tout exécuter** (Runtime → Run all). Le data store met les demandes en file d'attente : l'étape 2 peut prendre quelques minutes.*"),
    ("# Install the open-source tools (Colab / fresh machine). Takes ~1 minute.",
     "# Installer les outils libres (Colab / nouvelle machine). Environ 1 minute."),
    ("# import before earthkit.data (avoids a crash at exit)", "# à importer avant earthkit.data (évite un plantage à la fermeture)"),
    ("## 4 · Your turn 🌍", "## 4 · À vous de jouer 🌍"),
    (" on the Atmosphere Data Store ", " sur l'Atmosphere Data Store "),
    (" on the Climate Data Store ", " sur le Climate Data Store "),
    ("# north, west, south, east", "# nord, ouest, sud, est"),
    ("did not answer ({type(err).__name__}), trying the next mirror", "ne répond pas ({type(err).__name__}), essai du miroir suivant"),
    ("# ECMWF first, then the cloud mirrors if it is busy", "# l'ECMWF d'abord, puis les miroirs cloud s'il est occupé"),
]

OD = [
    ("CC BY 4.0, open data", "CC BY 4.0, données ouvertes"),
    ("""### Data & licence
ECMWF Open Data is free under **Creative Commons CC-BY-4.0**:
`© ECMWF · Source: www.ecmwf.int · CC-BY-4.0 and ECMWF Terms of Use`. No account, no key.

[ECMWF open data](https://www.ecmwf.int/en/forecasts/datasets/open-data)""",
     """### Données et licence
Les données ouvertes de l'ECMWF sont gratuites sous licence **Creative Commons CC-BY-4.0** :
`© ECMWF · Source: www.ecmwf.int · CC-BY-4.0 and ECMWF Terms of Use`. Sans compte, sans clé.

[Données ouvertes de l'ECMWF](https://www.ecmwf.int/en/forecasts/datasets/open-data)"""),
]

COP = [
    ("Copernicus licence, free", "licence Copernicus, gratuit"),
    ("## Your free Copernicus key", "## Votre clé Copernicus gratuite"),
    ("Copernicus data is free and open, but the data stores ask you to register once so they can manage the queue:",
     "Les données Copernicus sont libres et gratuites, mais les data stores demandent de s'inscrire une fois pour gérer la file d'attente :"),
    ("1. Create an account at", "1. Créez un compte sur"),
    ("(the same login works for the\n   Atmosphere Data Store).", "(le même identifiant sert pour\n   l'Atmosphere Data Store)."),
    ("2. Open the [dataset page]", "2. Ouvrez la [page du jeu de données]"),
    ("and accept its licence (bottom of the Download tab). You only do this once.",
     "et acceptez sa licence (en bas de l'onglet Download). Une seule fois suffit."),
    ("3. Copy your API key from your [profile page](https://cds.climate.copernicus.eu/profile) and paste it below.",
     "3. Copiez votre clé API depuis votre [page de profil](https://cds.climate.copernicus.eu/profile) et collez-la ci-dessous."),
    ("""**Use your own key.** Everyone who runs this notebook needs their own free Copernicus account and key. The next cell asks
for it in a hidden box and saves it on the machine running the notebook (in Colab that is a temporary machine, wiped when
you close the tab). The key is never stored in the notebook, so don't paste it into a code cell, and don't share a notebook
or screenshot that shows it. On your own computer with `~/.cdsapirc` / `~/.adsapirc` already in place, the cell asks nothing.""",
     """**Utilisez votre propre clé.** Chaque personne qui exécute ce notebook a besoin de son propre compte et de sa clé
Copernicus gratuits. La cellule suivante demande la clé dans un champ masqué et l'enregistre sur la machine qui exécute
le notebook (dans Colab, une machine temporaire effacée à la fermeture de l'onglet). La clé n'est jamais enregistrée dans
le notebook : ne la collez pas dans une cellule de code et ne partagez pas de notebook ou de capture d'écran qui la montre.
Sur votre ordinateur, si `~/.cdsapirc` / `~/.adsapirc` existent déjà, la cellule ne demande rien."""),
    ('getpass("Copernicus API key: ")', 'getpass("Clé API Copernicus : ")'),
    ('print("Copernicus key ready")', 'print("Clé Copernicus prête")'),
    ("### Data & licence\nCopernicus data is free and open under the Copernicus licence (CC-BY 4.0). Credit:",
     "### Données et licence\nLes données Copernicus sont libres et gratuites sous licence Copernicus (CC-BY 4.0). Mention :"),
    ("ECMWF runs the Copernicus Atmosphere Monitoring Service and the\nCopernicus Climate Change Service for the European Union.",
     "L'ECMWF opère le service Copernicus de surveillance de l'atmosphère (CAMS) et le\nservice Copernicus concernant le changement climatique (C3S) pour l'Union européenne."),
]

HEAT = OD + [
    ("# Senegal's next six afternoons at 9 km 🌡️", "# Les six prochains après-midi au Sénégal, à 9 km 🌡️"),
    ("### ECMWF free & open data · IFS 9 km · no account needed",
     "### Données ouvertes et gratuites de l'ECMWF · IFS 9 km · sans compte"),
    ("""ECMWF's 9 km forecast (IFS) is **open data**: no login, no fee. This notebook downloads 2 m temperature for
15:00 UTC (15:00 in Dakar) on each of the next six days, prints how hot each afternoon gets in six Senegalese towns,
and maps the hottest one.""",
     """La prévision à 9 km de l'ECMWF (IFS) est en **données ouvertes** : sans identifiant, sans frais. Ce notebook
télécharge la température à 2 m pour 15 h UTC (15 h à Dakar) sur chacun des six prochains jours, affiche la chaleur
de chaque après-midi dans six villes du Sénégal et cartographie le plus chaud."""),
    ("ECMWF IFS forecast, 9 km (0.1°)", "Prévision IFS de l'ECMWF, 9 km (0,1°)"),
    ("2 m temperature at 15 UTC, six days, latest run", "Température à 2 m à 15 h UTC, six jours, dernier run"),
    ("## 1 · Choose the area", "## 1 · Choisir la zone"),
    (": Senegal and The Gambia", " : le Sénégal et la Gambie"),
    ("# 15 UTC today and the next five days (Dakar is on UTC)", "# 15 h UTC aujourd'hui et les cinq jours suivants (Dakar est à l'heure UTC)"),
    ("## 2 · Get the 9 km forecast (ECMWF open data)", "## 2 · Télécharger la prévision à 9 km (données ouvertes de l'ECMWF)"),
    ("# small margin", "# petite marge"),
    ("# kelvin -> °C", "# kelvins -> °C"),
    ('print(f"Forecast run {run:%A %d %B %Y} 00 UTC")', 'print(f"Prévision du {jour(run)} {run.year}, run de 00 h UTC")'),
    ('print(f"  {v:%a %d %b} 15 UTC   {towns}")', 'print(f"  {jour(v):21s} 15 h UTC   {towns}")'),
    ("# the hottest afternoon", "# l'après-midi le plus chaud"),
    ("## 3 · Map the hottest afternoon", "## 3 · Cartographier l'après-midi le plus chaud"),
    ('label="2 m temperature (°C)"', 'label="Température à 2 m (°C)"'),
    ('chart.title(f"Senegal at 15:00 UTC on {day:%A %d %B}, the hottest of the next six afternoons\\n"\n            f"ECMWF IFS 9 km forecast from {run:%d %B %Y} 00 UTC", fontsize=13)',
     'chart.title(f"Le Sénégal le {jour(day)} à 15 h UTC, le plus chaud des six prochains après-midi\\n"\n            f"Prévision IFS 9 km de l\'ECMWF du {date(run)}, 00 h UTC", fontsize=13)'),
    ("""- **Night-time:** change `15` to `3` in `STEPS` for 03 UTC, the coolest part of the night.
- **The wind:** add `"10u", "10v"` to `param` and draw arrows with `chart.ax.quiver`.
- **Anywhere else:** change `AREA`, for example `[16, -6, 9, 3]` for Burkina Faso.""",
     """- **La nuit :** remplacez `15` par `3` dans `STEPS` pour 03 h UTC, le moment le plus frais de la nuit.
- **Le vent :** ajoutez `"10u", "10v"` à `param` et tracez des flèches avec `chart.ax.quiver`.
- **Ailleurs :** changez `AREA`, par exemple `[16, -6, 9, 3]` pour le Burkina Faso."""),
]

AIFS = OD + [
    ("# AIFS and IFS, side by side over Senegal 🤖", "# AIFS et IFS côte à côte sur le Sénégal 🤖"),
    ("### ECMWF free & open data · machine-learned and physics-based · no account",
     "### Données ouvertes et gratuites de l'ECMWF · apprentissage automatique et physique · sans compte"),
    ("""ECMWF runs two global forecasts and both are **open data**: the physics-based **IFS** and **AIFS**, the
machine-learned model, which produces a ten-day forecast in minutes. This notebook takes the same run of each, maps
2 m temperature about two and a half days ahead side by side, then maps the difference between them.""",
     """L'ECMWF produit deux prévisions mondiales, toutes deux en **données ouvertes** : l'**IFS**, fondé sur la physique,
et l'**AIFS**, le modèle par apprentissage automatique, qui calcule une prévision à dix jours en quelques minutes. Ce
notebook prend le même run des deux, cartographie côte à côte la température à 2 m à environ deux jours et demi
d'échéance, puis la différence entre les deux."""),
    ("ECMWF IFS forecast, 0.25°", "Prévision IFS de l'ECMWF, 0,25°"),
    ("ECMWF AIFS Single forecast, 0.25°", "Prévision AIFS Single de l'ECMWF, 0,25°"),
    ("2 m temperature, latest run", "Température à 2 m, dernier run"),
    ("2 m temperature, the same run", "Température à 2 m, le même run"),
    ("## 1 · Choose the area and the lead time", "## 1 · Choisir la zone et l'échéance"),
    ("# hours after the run starts (about two and a half days)", "# heures après le début du run (environ deux jours et demi)"),
    ("## 2 · Get both forecasts (ECMWF open data, 0.25°)", "## 2 · Télécharger les deux prévisions (données ouvertes de l'ECMWF, 0,25°)"),
    ('"the two models came from different runs: run the cell again"', '"les deux modèles viennent de runs différents : relancez la cellule"'),
    ('print(f"Run {run:%d %B %Y %H} UTC, valid {valid:%A %d %B %H}:00 UTC")',
     'print(f"Run du {date(run)} à {run:%H} h UTC, valable le {jour(valid)} à {valid:%H} h UTC")'),
    ('print(f"AIFS minus IFS: mean {float(diff.mean()):+.1f} °C, typical size {float(np.sqrt((diff ** 2).mean())):.1f} °C")',
     'print(f"AIFS moins IFS : moyenne {float(diff.mean()):+.1f} °C, écart typique {float(np.sqrt((diff ** 2).mean())):.1f} °C")'),
    ('print(f"IFS {float(ifs.min()):.0f} to {float(ifs.max()):.0f} °C · AIFS {float(aifs.min()):.0f} to {float(aifs.max()):.0f} °C")',
     'print(f"IFS de {float(ifs.min()):.0f} à {float(ifs.max()):.0f} °C · AIFS de {float(aifs.min()):.0f} à {float(aifs.max()):.0f} °C")'),
    ("## 3 · Map them", "## 3 · Les cartographier"),
    ('"IFS · physics-based"', '"IFS · physique"'),
    ('"AIFS · machine-learned"', '"AIFS · apprentissage automatique"'),
    ('label="2 m temperature (°C)"', 'label="Température à 2 m (°C)"'),
    ('"AIFS minus IFS", fontsize', '"AIFS moins IFS", fontsize'),
    ('label="Difference (°C)"', 'label="Différence (°C)"'),
    ('fig.suptitle(f"2 m temperature, {valid:%A %d %B %H}:00 UTC, both models run {run:%d %B %Y %H} UTC", fontsize=14)',
     'fig.suptitle(f"Température à 2 m, {jour(valid)} à {valid:%H} h UTC, les deux modèles lancés le {date(run)} à {run:%H} h UTC", fontsize=14)'),
    ("""- **Further ahead:** `STEP = 144` (six days). The two models usually drift further apart with lead time.
- **Another variable:** `param="10u"` or `"msl"` (mean sea level pressure; divide by 100 for hPa).
- **The ensembles:** both have open ensembles too: `model="aifs-ens"` or `"ifs"` with `stream="enfo"`.""",
     """- **Plus loin :** `STEP = 144` (six jours). Les deux modèles s'écartent en général avec l'échéance.
- **Une autre variable :** `param="10u"` ou `"msl"` (pression au niveau de la mer ; divisez par 100 pour des hPa).
- **Les ensembles :** les deux ont aussi des ensembles ouverts : `model="aifs-ens"` ou `"ifs"` avec `stream="enfo"`."""),
]

DUST = COP + [
    ("# Desert dust over West Africa with CAMS 🏜️", "# Les poussières désertiques sur l'Afrique de l'Ouest avec CAMS 🏜️"),
    ("### Copernicus Atmosphere Monitoring Service · free account",
     "### Service Copernicus de surveillance de l'atmosphère · compte gratuit"),
    ("""In the dry season, roughly November to March, the north-easterly **Harmattan** carries Saharan dust across the
Sahel towards the Atlantic. This notebook maps the dust forecast from the **CAMS global forecast**, run by ECMWF for
the European Union, from yesterday's run up to five days ahead.""",
     """En saison sèche, à peu près de novembre à mars, l'**harmattan**, vent de nord-est, transporte les poussières du
Sahara à travers le Sahel vers l'Atlantique. Ce notebook cartographie la prévision de poussières de la **prévision
mondiale CAMS**, produite par l'ECMWF pour l'Union européenne, à partir du run d'hier et jusqu'à cinq jours."""),
    ("CAMS global atmospheric composition forecast, about 40 km", "Prévision mondiale CAMS de la composition atmosphérique, environ 40 km"),
    ("Dust aerosol optical depth at 550 nm", "Épaisseur optique des aérosols désertiques à 550 nm"),
    ("## 1 · Choose the run, the lead time and the area", "## 1 · Choisir le run, l'échéance et la zone"),
    ("# yesterday's run is always complete", "# le run d'hier est toujours complet"),
    ("# hours after 00 UTC, up to 120", "# heures après 00 h UTC, jusqu'à 120"),
    ("## 2 · Get the dust forecast", "## 2 · Télécharger la prévision de poussières"),
    ('print(f"Dust optical depth up to {float(duaod.max()):.2f} at {valid:%A %d %B %H}:00 UTC")',
     'print(f"Épaisseur optique des poussières jusqu\'à {float(duaod.max()):.2f} le {jour(valid)} à {valid:%H} h UTC")'),
    ("## 3 · Map it", "## 3 · La cartographier"),
    ('chart.title(f"Desert dust over West Africa, {valid:%A %d %B %H}:00 UTC\\nCAMS global forecast from {DATE} 00 UTC", fontsize=13)',
     'chart.title(f"Poussières désertiques sur l\'Afrique de l\'Ouest, {jour(valid)} à {valid:%H} h UTC\\nPrévision mondiale CAMS du {DATE}, 00 h UTC", fontsize=13)'),
    ("""- **Step through the week:** change `LEAD` from 0 to 120 in steps of 3.
- **Dust near the ground:** variable `"dust_aerosol_0.9-20um_mixing_ratio"` is the coarse dust; or try
  `"particulate_matter_10um"` (multiply by 1e9 for µg/m³), which is mostly dust in the Sahel dry season.
- CAMS global runs at about 40 km: it shows where the dust goes, not individual towns.""",
     """- **Parcourir la semaine :** changez `LEAD` de 0 à 120 par pas de 3.
- **Les poussières près du sol :** la variable `"dust_aerosol_0.9-20um_mixing_ratio"` donne les grosses poussières ; ou
  essayez `"particulate_matter_10um"` (multipliez par 1e9 pour des µg/m³), surtout des poussières en saison sèche au Sahel.
- CAMS mondial a une résolution d'environ 40 km : il montre où vont les poussières, pas le détail ville par ville."""),
]

RAIN = COP + [
    ("# Senegal's 2024 rainy season in ERA5 🌧️", "# La saison des pluies 2024 au Sénégal dans ERA5 🌧️"),
    ("### Copernicus Climate Change Service · ERA5 · free account",
     "### Service Copernicus concernant le changement climatique · ERA5 · compte gratuit"),
    ("""How wet was the 2024 rainy season (June to October) compared with a normal year? This notebook uses the
**ERA5 monthly means**, the Copernicus reanalysis that ECMWF produces for the European Union, to compare 2024 with
the 1991–2020 average, as a percentage of normal. The Senegal River rises in the highlands of Guinea and Mali, so the
map covers its whole basin.""",
     """La saison des pluies 2024 (juin à octobre) a-t-elle été plus humide qu'une année normale ? Ce notebook utilise les
**moyennes mensuelles d'ERA5**, la réanalyse Copernicus que l'ECMWF produit pour l'Union européenne, pour comparer
2024 à la moyenne 1991–2020, en pourcentage de la normale. Le fleuve Sénégal prend sa source dans les hauts plateaux
de Guinée et du Mali : la carte couvre donc tout son bassin."""),
    ("ERA5 monthly means, about 31 km", "Moyennes mensuelles ERA5, environ 31 km"),
    ("Total precipitation, June–October, 1991–2024", "Précipitations totales, juin–octobre, 1991–2024"),
    ("## 1 · Choose the season, the year and the area", "## 1 · Choisir la saison, l'année et la zone"),
    ("# June to October", "# juin à octobre"),
    ("## 2 · Get ERA5 monthly rainfall, 1991–2020 and the chosen year",
     "## 2 · Télécharger les pluies mensuelles ERA5, 1991–2020 et l'année choisie"),
    ("# metres per day, monthly mean", "# mètres par jour, moyenne mensuelle"),
    ("# -> mm in each month", "# -> mm par mois"),
    ("# mm over June-October, each year", "# mm de juin à octobre, chaque année"),
    ('print(f"{YEAR}: {float(this.mean()):.0f} mm across the box, normal {float(normal.mean()):.0f} mm "\n      f"({float(100 * this.mean() / normal.mean()):.0f}% of normal)")',
     'print(f"{YEAR} : {float(this.mean()):.0f} mm sur la zone, normale {float(normal.mean()):.0f} mm "\n      f"({float(100 * this.mean() / normal.mean()):.0f} % de la normale)")'),
    ('f"{float(pct.sel(latitude=la, longitude=lo, method=\'nearest\')):4.0f}% of normal")',
     'f"{float(pct.sel(latitude=la, longitude=lo, method=\'nearest\')):4.0f} % de la normale")'),
    ("## 3 · Map it", "## 3 · La cartographier"),
    ('label=f"Rain June–October {YEAR}, % of the 1991–2020 average"', 'label=f"Pluie juin–octobre {YEAR}, % de la moyenne 1991–2020"'),
    ('chart.title(f"Senegal\'s {YEAR} rainy season compared with normal\\nERA5 monthly means", fontsize=13)',
     'chart.title(f"La saison des pluies {YEAR} au Sénégal comparée à la normale\\nMoyennes mensuelles ERA5", fontsize=13)'),
    ("""- **Another year:** `YEAR = 2020` or any year from 1940.
- **Just the peak months:** `MONTHS = ["08", "09"]`.
- **Hotter or cooler than normal:** `"2m_temperature"` (kelvin) and `this - normal` instead of a percentage.""",
     """- **Une autre année :** `YEAR = 2020` ou toute année depuis 1940.
- **Seulement les mois les plus pluvieux :** `MONTHS = ["08", "09"]`.
- **Plus chaud ou plus frais que la normale :** `"2m_temperature"` (kelvins) et `this - normal` au lieu d'un pourcentage."""),
]

TABLE = {"heat": HEAT, "aifs": AIFS, "dust": DUST, "rain": RAIN}


def translate(key, cells, name_en, name_fr, png_en, png_fr):
    pairs = COMMON + TABLE[key] + [(name_en, name_fr), (f'"{png_en}"', f'"{png_fr}"')]
    used = [False] * len(pairs)
    for c in cells:
        src = c.source
        for i, (en, fr) in enumerate(pairs):
            if en in src:
                src = src.replace(en, fr); used[i] = True
        if c.cell_type == "code" and "import numpy as np" in src and "JOURS" not in src:
            src += "\n" + DATES
        c.source = src
    required = range(len(COMMON), len(pairs) - 1)          # notebook-specific pairs must all match
    missing = [pairs[i][0][:70] for i in required if not used[i]]
    assert not missing, f"{key}: untranslated {missing}"
    return cells
