"""BD Forêt V2 : surface de forêt et part de résineux par commune (foret_commune.csv).

Sert à Q1 (où sont les massifs), Q3 (la part de résineux, une des 3 variables de H3) et Q5 (comparer
les départements à surface de forêt égale). Voir docs/sources/fiche-bd-foret.md et regles.md (D1 à D3).

Catégories, d'après `TFV_G11` (11 grands types) :
- forêt : les types « Forêt … » et « Peupleraie ». Les landes et formations herbacées n'en sont pas
- conifères (résineux) : « Forêt fermée conifères », « Forêt ouverte conifères »
- feuillus : « Forêt … feuillus » et « Peupleraie »
- mixte : « Forêt … mixte ». Comptée à moitié dans la part de résineux (POIDS_MIXTE, proposition de Denis sur #79,
  journal du 20/11). La version stricte, sans la mixte, est gardée en test de sensibilité
- sans couvert arboré (coupe, jeune plantation) : de la forêt, mais essence « NR » : hors de la part de résineux

part_resineux = (conifères + POIDS_MIXTE × mixte) ÷ forêt avec couvert arboré (conifères + feuillus + mixte).
part_resineux_stricte = conifères ÷ forêt avec couvert arboré.
Calcul en Lambert 93 (EPSG:2154), en mètres : les contours des communes (WGS84) sont reprojetés.
"""

import re

import geopandas as gpd
import pandas as pd

from ..qualite.regles import Controle, Regle
from .commun import BRUT, verifier_fichiers

LAMBERT_93 = "EPSG:2154"
M2_PAR_HA = 10_000
POIDS_MIXTE = 0.5  # une forêt mixte compte pour moitié en résineux (à vérifier avec le descriptif IGN de la V2)


def categorie(tfv_g11):
    """Grand type BD Forêt -> catégorie du projet (ou "" si ce n'est pas de la forêt)."""
    if tfv_g11 == "Peupleraie":
        return "feuillus"
    if not tfv_g11.startswith("Forêt"):
        return ""  # lande, formation herbacée
    for mot, cat in (("conifères", "coniferes"), ("feuillus", "feuillus"), ("mixte", "mixte")):
        if mot in tfv_g11:
            return cat
    return "sans_couvert"


def lire_bd_foret(dossier=None):
    """Toutes les couches FORMATION_VEGETALE des départements téléchargés, avec leur édition."""
    dossier = dossier or BRUT / "bd_foret"
    fichiers = sorted(dossier.rglob("FORMATION_VEGETALE.shp"))
    if not fichiers:
        verifier_fichiers([dossier / "FORMATION_VEGETALE.shp"], "bdforet")
    couches = []
    for f in fichiers:
        trouve = re.search(r"_D0(\d{2}|2[AB])_(\d{4}-\d{2}-\d{2})", str(f))
        couche = gpd.read_file(f)
        couche["departement_fichier"] = trouve.group(1)
        couche["edition"] = trouve.group(2)  # date de l'édition IGN (pas l'année des photos, D3)
        couches.append(couche)
    return gpd.GeoDataFrame(pd.concat(couches, ignore_index=True), crs=couches[0].crs)


def preparer(foret):
    """Catégorie du projet, et réparation des géométries invalides (contours qui se croisent : 262 dans le 88).

    `repare` dit quels polygones ont été réparés avec make_valid, pour le compter dans le rapport (D1).
    """
    foret = foret.copy()
    foret["repare"] = ~foret.is_valid
    foret.loc[foret["repare"], "geometry"] = foret.loc[foret["repare"], "geometry"].make_valid()
    foret["categorie"] = foret["TFV_G11"].fillna("").map(categorie)
    return foret[foret["categorie"] != ""]


def foret_par_commune(foret, contours):
    """Découpe la forêt sur les communes et somme les surfaces par catégorie (en ha)."""
    communes = contours.to_crs(LAMBERT_93)[["code", "codeDepartement", "geometry"]]
    communes = communes.rename(columns={"code": "code_commune_2026", "codeDepartement": "departement"})
    # Chaque fichier départemental déborde un peu chez le voisin : sans ce filtre, la forêt d'une frontière
    # est comptée 2 fois (D4 l'a trouvé : 4 communes à plus de 100 % de forêt, entre 54 / 88 et 57 / 67).
    # On découpe donc chaque fichier seulement sur les communes de son département.
    morceaux = pd.concat([
        gpd.overlay(
            foret.loc[foret["departement_fichier"] == dep, ["categorie", "edition", "geometry"]],
            communes[communes["departement"] == dep], how="intersection", keep_geom_type=True,
        )
        for dep in sorted(foret["departement_fichier"].unique())
    ], ignore_index=True)
    morceaux["ha"] = morceaux.area / M2_PAR_HA
    surfaces = morceaux.pivot_table(index="code_commune_2026", columns="categorie", values="ha", aggfunc="sum", fill_value=0)
    for cat in ("coniferes", "feuillus", "mixte", "sans_couvert"):
        if cat not in surfaces:
            surfaces[cat] = 0.0
    edition = morceaux.groupby("code_commune_2026")["edition"].max()

    table = communes.assign(surface_commune_ha=communes.area / M2_PAR_HA).drop(columns="geometry")
    table = table.merge(surfaces, left_on="code_commune_2026", right_index=True, how="left").fillna(
        {c: 0.0 for c in ("coniferes", "feuillus", "mixte", "sans_couvert")})
    table = table.rename(columns={c: f"surface_{c}_ha" for c in ("coniferes", "feuillus", "mixte", "sans_couvert")})
    avec_couvert = table[["surface_coniferes_ha", "surface_feuillus_ha", "surface_mixte_ha"]].sum(axis=1)
    table["surface_foret_ha"] = avec_couvert + table["surface_sans_couvert_ha"]
    table["part_foret"] = table["surface_foret_ha"] / table["surface_commune_ha"]
    resineux = table["surface_coniferes_ha"] + POIDS_MIXTE * table["surface_mixte_ha"]
    table["part_resineux"] = (resineux / avec_couvert).where(avec_couvert > 0)  # vide sans forêt, pas 0
    table["part_resineux_stricte"] = (table["surface_coniferes_ha"] / avec_couvert).where(avec_couvert > 0)
    table["edition_bd_foret"] = table["code_commune_2026"].map(edition).fillna("")
    colonnes = ["code_commune_2026", "departement", "surface_commune_ha", "surface_foret_ha", "part_foret",
                "surface_coniferes_ha", "surface_feuillus_ha", "surface_mixte_ha", "surface_sans_couvert_ha",
                "part_resineux", "part_resineux_stricte", "edition_bd_foret"]
    return table[colonnes].round(4).sort_values("code_commune_2026").reset_index(drop=True)


def regles_polygones():
    return [
        Regle(
            id="D1", dimension="validité", portee="BD Forêt, géométries valides en Lambert 93 (après réparation)",
            controle=lambda t: Controle(int((~t.is_valid).sum()) + (0 if t.crs == LAMBERT_93 else len(t)), len(t),
                                        f"{int(t['repare'].sum())} polygones réparés avec make_valid"),
            seuil=0.0, severite="bloquer",
            decision="on arrête : une géométrie encore invalide après réparation fausserait les surfaces découpées",
        ),
        Regle(
            id="D2", dimension="unicité", portee="BD Forêt, identifiant `ID` par département",
            controle=lambda t: Controle(int(t.duplicated(["departement_fichier", "ID"], keep=False).sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un polygone en double compterait sa surface 2 fois",
        ),
    ]


def regles_communes(nb_communes):
    return [
        Regle(
            id="D4", dimension="cohérence", portee="foret_commune.csv, forêt ≤ surface de la commune",
            controle=lambda t: Controle(int((t["part_foret"] > 1.001).sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : plus de forêt que de commune = polygones superposés ou mauvaise projection",
        ),
        Regle(
            id="D5", dimension="complétude (population)", portee="foret_commune.csv, une ligne par commune du Grand Est",
            controle=lambda t: Controle(abs(len(t) - nb_communes) + int(t["code_commune_2026"].duplicated().sum()), nb_communes),
            seuil=0.0, severite="bloquer",
            decision="on arrête : une commune perdue n'aurait pas de part de résineux",
        ),
        Regle(
            id="D3", dimension="actualité", portee="foret_commune.csv, édition de la BD Forêt",
            controle=lambda t: Controle(int(((t["surface_foret_ha"] > 0) & (t["edition_bd_foret"] == "")).sum()), len(t),
                                        "commune avec forêt sans édition notée"),
            seuil=0.0, severite="alerter",
            decision="l'édition (et donc l'âge des photos) est donnée avec chaque résultat",
        ),
    ]
