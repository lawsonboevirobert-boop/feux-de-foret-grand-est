"""NASA FIRMS 2026 : les détections satellite, regroupées par commune et par jour (firms_commune_jour.csv).

Voir docs/sources/fiche-nasa-firms.md, docs/pipeline/plan-nettoyage.md et docs/qualite/regles.md (N1 à N9).

Une ligne FIRMS = un pixel chaud vu par un satellite à un passage, pas un départ de feu (N5).
Sortie : une ligne par commune du Grand Est et par jour (heure de Paris) avec au moins une détection gardée.
Pas de coordonnées dans la sortie (RGPD : un point peut tomber sur une propriété privée).
"""

import geopandas as gpd
import pandas as pd

from ..qualite.regles import Controle, Regle
from .commun import BRUT, verifier_fichiers

FUSEAU = "Europe/Paris"
JOURS_SOURCE_FIXE = 10  # N3 : une case d'environ 1 km vue 10 jours ou plus dans l'année = usine (choix du groupe)
DECIMALES_CASE = 2  # 0,01° ≈ 1 km


def lire_firms(dossier=None):
    dossier = dossier or BRUT / "firms"
    fichiers = sorted(dossier.glob("firms_*.csv"))
    if not fichiers:
        verifier_fichiers([dossier / "firms_SATELLITE_AAAA.csv"], "firms")
    return pd.concat(
        [pd.read_csv(f, dtype=str, keep_default_na=False).assign(fichier=f.stem) for f in fichiers],
        ignore_index=True,
    )


def lire_couverture(dossier=None):
    """Dernier jour téléchargé (texte AAAA-MM-JJ), tous satellites confondus, ou None si inconnu.

    Écrit par la récupération (couverture_firms_*.csv). Après ce jour, on n'a pas regardé :
    l'absence de détection ne vaut pas 0.
    """
    dossier = dossier or BRUT / "firms"
    fichiers = sorted(dossier.glob("couverture_firms_*.csv"))
    if not fichiers:
        return None
    return max(pd.read_csv(f, dtype=str)["au"].max() for f in fichiers)


def lire_contours(dossier=None):
    dossier = dossier or BRUT / "contours_communes"
    fichiers = sorted(dossier.glob("communes_*.geojson"))
    if not fichiers:
        verifier_fichiers([dossier / "communes_DEP.geojson"], "contours")
    contours = pd.concat([gpd.read_file(f) for f in fichiers], ignore_index=True)
    return gpd.GeoDataFrame(contours[["code", "codeDepartement", "geometry"]], crs="EPSG:4326")


def preparer(brut):
    """N1 : date et heure UTC -> heure de Paris. N2 : mêmes colonnes pour MODIS et VIIRS."""
    # en fusionnant MODIS et VIIRS, la colonne absente d'un satellite devient NaN : on la remet à ""
    brut = brut.fillna("")
    heure = brut["acq_time"].str.zfill(4)
    utc = pd.to_datetime(brut["acq_date"] + " " + heure.str[:2] + ":" + heure.str[2:], utc=True, errors="coerce")
    paris = utc.dt.tz_convert(FUSEAU)
    brillance = brut["brightness"] if "brightness" in brut else pd.Series("", index=brut.index)
    if "bright_ti4" in brut:
        brillance = brillance.where(brillance != "", brut["bright_ti4"])
    return pd.DataFrame({
        "fichier": brut["fichier"],
        "satellite": brut["satellite"],
        "instrument": brut["instrument"],
        "traitement": brut["traitement"],  # SP ou NRT
        "acq_date": brut["acq_date"],
        "date": paris.dt.strftime("%Y-%m-%d"),
        "latitude": pd.to_numeric(brut["latitude"], errors="coerce"),
        "longitude": pd.to_numeric(brut["longitude"], errors="coerce"),
        "brillance": pd.to_numeric(brillance, errors="coerce"),  # brightness (MODIS) ou bright_ti4 (VIIRS)
        "confiance": brut["confidence"],  # 0 à 100 (MODIS) ou l / n / h (VIIRS) : gardée en texte
        "frp": pd.to_numeric(brut["frp"], errors="coerce"),
        "type": brut["type"] if "type" in brut else "",  # seulement dans les fichiers SP
    })


def rattacher(points, contours):
    """N8 : chaque point est rattaché à la commune du Grand Est qui le contient, sinon commune vide."""
    geo = gpd.GeoDataFrame(points, geometry=gpd.points_from_xy(points["longitude"], points["latitude"]), crs="EPSG:4326")
    joint = gpd.sjoin(geo, contours, how="left", predicate="within")
    joint = joint[~joint.index.duplicated(keep="first")]  # un point sur une frontière : une seule commune
    points = points.copy()
    points["code_commune_2026"] = joint["code"].fillna("").values
    points["departement"] = joint["codeDepartement"].fillna("").values
    return points


def marquer_sources_fixes(points, jours=JOURS_SOURCE_FIXE):
    """N3 : `type = 2` (SP), ou une case d'environ 1 km vue `jours` jours différents ou plus dans l'année."""
    case = points["latitude"].round(DECIMALES_CASE).astype(str) + "," + points["longitude"].round(DECIMALES_CASE).astype(str)
    jours_vus = points.groupby(case)["date"].transform("nunique")
    points = points.copy()
    points["source_fixe"] = (points["type"] == "2") | (jours_vus >= jours)
    return points


def nettoyer_firms(brut, contours):
    points = rattacher(preparer(brut), contours)
    points["hors_grand_est"] = points["code_commune_2026"] == ""
    dedans = marquer_sources_fixes(points[~points["hors_grand_est"]])
    points["source_fixe"] = False
    points.loc[dedans.index, "source_fixe"] = dedans["source_fixe"]
    points["garde"] = ~points["hors_grand_est"] & ~points["source_fixe"]
    return points


def par_commune_jour(points):
    """N4 et N5 : une ligne par commune et par jour. Des détections, jamais des départs de feu."""
    gardes = points[points["garde"]]
    table = gardes.groupby(["code_commune_2026", "departement", "date"]).agg(
        nb_detections=("frp", "size"),
        nb_satellites=("satellite", "nunique"),
        frp_max=("frp", "max"),
        traitements=("traitement", lambda t: "/".join(sorted(set(t)))),
    ).reset_index()
    return table.assign(detection_satellite=True)


def versions_melangees(points):
    """N9 : nb de couples fichier (satellite) × jour UTC présents à la fois en SP et en NRT."""
    return int((points.groupby(["fichier", "acq_date"])["traitement"].nunique() > 1).sum())


def regles_points():
    return [
        Regle(
            id="N1", dimension="validité", portee="détections FIRMS, date et heure UTC lisibles",
            controle=lambda t: Controle(int(t["date"].isna().sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : sans heure lisible, on ne sait pas à quel jour de Paris rattacher le point",
        ),
        Regle(
            id="N2", dimension="validité", portee="détections FIRMS, colonnes harmonisées MODIS / VIIRS",
            controle=lambda t: Controle(int((t["brillance"].isna() | (t["confiance"] == "") | t["frp"].isna()).sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : une colonne mal harmonisée fausse la comparaison entre satellites",
        ),
        Regle(
            id="N9", dimension="unicité", portee="détections FIRMS, une seule version (SP ou NRT) par satellite et par jour",
            controle=lambda t: Controle(versions_melangees(t), len(t), "couples satellite × jour en SP et en NRT"),
            seuil=0.0, severite="bloquer",
            decision="on arrête : la même détection serait comptée 2 fois",
        ),
        Regle(
            id="N8", dimension="cohérence", portee="détections FIRMS, dans une commune du Grand Est",
            controle=lambda t: Controle(int(t["hors_grand_est"].sum()), len(t), "points hors Grand Est, enlevés"),
            seuil=1.0, severite="tolerer",
            decision="on les enlève et on les compte : le rectangle demandé déborde sur 4 pays",
        ),
        Regle(
            id="N3", dimension="exactitude", portee="détections FIRMS dans le Grand Est, sources fixes",
            controle=lambda t: Controle(int(t["source_fixe"].sum()), int((~t["hors_grand_est"]).sum()),
                                        f"type = 2, ou case vue {JOURS_SOURCE_FIXE} jours ou plus : enlevés"),
            seuil=1.0, severite="tolerer",
            decision="on les enlève et on les compte : ce sont des usines, pas des feux",
        ),
    ]


def regles_commune_jour():
    return [
        Regle(
            id="N4", dimension="unicité", portee="firms_commune_jour.csv, commune × jour",
            controle=lambda t: Controle(int(t.duplicated(["code_commune_2026", "date"], keep=False).sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un feu vu par plusieurs satellites doit rester une seule ligne",
        ),
    ]
