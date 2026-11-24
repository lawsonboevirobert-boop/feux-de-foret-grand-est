"""FWI de Copernicus : le FWI de chaque maille chaque jour, puis le FWI moyen de chaque département.

Étape 5 du plan de nettoyage (docs/pipeline/plan-nettoyage.md), règles F1 à F5 de docs/qualite/regles.md.

- fwi_maille.csv : 1 jour × 1 maille (date, latitude et longitude du centre, FWI)
- fwi_departement (dans jour_departement.csv) : 1 jour × 1 département, deux moyennes sur les communes,
  chaque commune avec le FWI de sa maille (commune_maille.csv, #62) :
  - fwi_moyen : pondérée par la surface de forêt de la commune (foret_commune.csv). C'est un indice de feux
    de forêt : une commune sans forêt ne compte pas (décision de #61)
  - fwi_moyen_simple : chaque commune compte pareil, gardée pour vérifier

Copernicus est optionnel, comme FIRMS : il faut une clé pour le télécharger. Sans fichiers, le nettoyage
prévient et continue, et les colonnes FWI restent vides (pas 0).
"""

import re

import pandas as pd

from ..qualite.regles import Controle, Regle
from .commun import BRUT, verifier_fichiers

VARIABLE = "fwinx"  # le FWI dans les fichiers de l'EWDS
FWI_MAX = 100  # F3 : borne haute vue dans le guide (max observé : 83,2)
DECIMALES = 2  # centres des mailles tous les 0,25° : arrondir évite les 48.749999
NOM_FICHIER = re.compile(r"^fwi_grand[-_]est_(\d{4})\.nc$")  # une année par fichier


def lire_fichiers(dossier=None):
    """Les fichiers annuels. Le script de récupération écrit fwi_grand_est_AAAA.nc, l'archive de Lawson
    fwi_grand-est_AAAA.nc : on accepte les deux. Une année présente sous les deux noms n'est lue qu'une fois.
    Un autre nom (l'ancien fwi_grand_est_2024_2026.nc de #45, sur une grille décalée) est ignoré, avec un message."""
    dossier = dossier or BRUT / "copernicus"
    fichiers = {}
    for f in sorted(dossier.glob("*.nc")):
        annee = NOM_FICHIER.match(f.name)
        if annee:
            fichiers.setdefault(int(annee.group(1)), f)
        else:
            print(f"  ALERTE fichier ignoré, nom attendu fwi_grand_est_AAAA.nc : {f.name}")
    if not fichiers:
        verifier_fichiers([dossier / "fwi_grand_est_AAAA.nc"], "copernicus")
    return [fichiers[a] for a in sorted(fichiers)]


def lire_fwi(fichiers):
    """Une ligne par jour et par maille, en mémoire (environ 1,1 million de lignes pour 2006-2026)."""
    import xarray as xr

    morceaux = []
    for f in fichiers:
        with xr.open_dataset(f) as ds:
            if VARIABLE not in ds:
                raise ValueError(f"F0 schéma inattendu dans {f.name} : pas de variable {VARIABLE}")
            temps = "valid_time" if "valid_time" in ds[VARIABLE].dims else "time"
            df = ds[VARIABLE].to_dataframe().reset_index()[[temps, "latitude", "longitude", VARIABLE]]
        df = df.rename(columns={temps: "date", VARIABLE: "fwi"})
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        df["latitude"] = df["latitude"].round(DECIMALES)
        df["longitude"] = df["longitude"].round(DECIMALES)
        morceaux.append(df)
    return pd.concat(morceaux, ignore_index=True).sort_values(["date", "latitude", "longitude"]).reset_index(drop=True)


def poids_departement_maille(commune_maille, foret_commune):
    """Pour chaque département et chaque maille : le nombre de communes et leur surface de forêt."""
    communes = commune_maille.merge(
        foret_commune[["code_commune_2026", "surface_foret_ha"]], on="code_commune_2026", how="left",
    ).fillna({"surface_foret_ha": 0.0})
    return communes.groupby(["departement", "latitude", "longitude"]).agg(
        nb_communes=("code_commune_2026", "size"), foret_ha=("surface_foret_ha", "sum"),
    ).reset_index()


def fwi_departement(fwi_maille, commune_maille, foret_commune):
    """FWI moyen de chaque département, chaque jour : pondéré par la forêt, et simple (chaque commune pareil).
    Une maille vide ne compte pas dans la moyenne du jour (F2) : ni sa valeur, ni son poids."""
    poids = poids_departement_maille(commune_maille, foret_commune)
    jours = fwi_maille.dropna(subset=["fwi"]).merge(poids, on=["latitude", "longitude"], how="inner")
    jours["fwi_x_foret"] = jours["fwi"] * jours["foret_ha"]
    jours["fwi_x_communes"] = jours["fwi"] * jours["nb_communes"]
    somme = jours.groupby(["date", "departement"])[["fwi_x_foret", "foret_ha", "fwi_x_communes", "nb_communes"]].sum()
    return pd.DataFrame({
        "fwi_moyen": (somme["fwi_x_foret"] / somme["foret_ha"]).round(2),
        "fwi_moyen_simple": (somme["fwi_x_communes"] / somme["nb_communes"]).round(2),
    }).reset_index()


def jours_manquants(fwi_maille):
    """F1 : nb de jours absents entre le 1er janvier et le dernier jour de chaque année téléchargée."""
    dates = pd.to_datetime(fwi_maille["date"].drop_duplicates())
    manquants = 0
    for annee, jours in dates.groupby(dates.dt.year):
        attendus = pd.date_range(f"{annee}-01-01", jours.max())
        manquants += len(attendus.difference(jours))
    return manquants


def mailles_sans_fwi(fwi_maille, commune_maille):
    """Nb de mailles de commune_maille.csv absentes de la grille des fichiers FWI."""
    grille = set(zip(fwi_maille["latitude"], fwi_maille["longitude"]))
    mailles = set(zip(commune_maille["latitude"].round(DECIMALES), commune_maille["longitude"].round(DECIMALES)))
    return len(mailles - grille)


def regles_fwi(commune_maille):
    return [
        Regle(
            id="F1", dimension="complétude (temps)", portee="fwi_maille.csv, chaque jour de chaque année téléchargée",
            controle=lambda t: Controle(jours_manquants(t), int(t["date"].nunique()), "jours manquants"),
            seuil=0.0, severite="bloquer",
            decision="on arrête et on retélécharge l'année : un jour sans FWI fausserait les seuils",
        ),
        Regle(
            id="F2", dimension="complétude (cellule)", portee="fwi_maille.csv, valeurs vides",
            controle=lambda t: Controle(int(t["fwi"].isna().sum()), len(t)),
            seuil=0.0, severite="alerter",
            decision="on charge, une maille vide ne compte pas dans la moyenne du jour",
        ),
        Regle(
            id="F3", dimension="exactitude", portee=f"fwi_maille.csv, FWI entre 0 et {FWI_MAX}",
            controle=lambda t: Controle(int(((t["fwi"] < 0) | (t["fwi"] > FWI_MAX)).sum()), len(t)),
            seuil=0.0, severite="alerter",
            decision="on charge et on regarde : une valeur hors bornes est signalée, pas corrigée",
        ),
        Regle(
            id="F4b", dimension="cohérence", portee="chaque maille de commune_maille.csv existe dans la grille FWI",
            controle=lambda t: Controle(mailles_sans_fwi(t, commune_maille), int(len(commune_maille[["latitude", "longitude"]].drop_duplicates()))),
            seuil=0.0, severite="bloquer",
            decision="on arrête : une maille sans FWI laisserait ses communes sans indice (mauvaise grille ou mauvaise zone)",
        ),
    ]
