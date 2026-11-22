"""Interventions des SIS : les totaux par service et par année (interventions_sis.csv).

Voir docs/pipeline/plan-nettoyage.md (étape 1) et docs/qualite/regles.md (S1, S2).

Une ligne = un service d'incendie et de secours pour une année. On garde seulement ce qui sert à Q5
et au contrôle des années vides de la BDIFF (P1) : feux de végétation, incendies, total des interventions.
"""

import re

import pandas as pd

from ..qualite.regles import Controle, Regle
from .cog import MOTIF_DEPARTEMENT
from .commun import BRUT, verifier_fichiers

DEPARTEMENTS_GRAND_EST = ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"]

# colonne du fichier -> colonne propre. « Feux de végétations » n'existe pas de 2010 à 2013
COLONNES = {
    "Feux de végétations": "feux_vegetation",
    "Incendies": "incendies",
    "Total interventions": "total_interventions",
}
NON_COMMUNIQUE = "N.C."
SEPARATEURS_MILLIERS = re.compile(r"[\s?  ]")  # espace, ou « ? » dans le fichier 2024


def lire_sis(dossier=None):
    """Un fichier par année, en cp1252 (encodage Windows), séparateur `;`. Tout en texte."""
    dossier = dossier or BRUT / "interventions_sis"
    fichiers = sorted(dossier.glob("interventions*.csv"))
    if not fichiers:
        verifier_fichiers([dossier / "interventionsAAAA.csv"], "sis")
    return [pd.read_csv(f, sep=";", dtype=str, encoding="cp1252", keep_default_na=False) for f in fichiers]


def nombre(valeurs):
    """Texte -> nombre. Retire les séparateurs de milliers. « N.C. » et vide -> vide, jamais 0."""
    propre = valeurs.str.strip().replace(NON_COMMUNIQUE, "").str.replace(SEPARATEURS_MILLIERS, "", regex=True)
    return pd.to_numeric(propre.replace("", None), errors="coerce").astype("Int64")


def nettoyer_sis(bruts):
    lignes = []
    for brut in bruts:
        # 2a -> 2A, et 8 -> 08 : le fichier écrit les départements 1 à 9 sans le zéro (trouvé par Franck sur #37).
        # zfill ne touche pas aux codes de 2 caractères ou plus (67, 2A, 972, BSPP)
        code = brut["Numéro"].str.strip().str.upper().str.zfill(2)
        table = pd.DataFrame({
            "annee": brut["Année"].astype(int),
            "code_sis": code,
            "departement": code.where(code.str.match(MOTIF_DEPARTEMENT), ""),  # BSPP, BMPM : pas un département
        })
        for colonne, propre in COLONNES.items():
            if colonne in brut.columns:
                table[propre] = nombre(brut[colonne])
                # S1 : une cellule remplie (hors N.C.) qui n'a pas pu devenir un nombre
                remplie = (brut[colonne].str.strip() != "") & (brut[colonne].str.strip() != NON_COMMUNIQUE)
                table[propre + "_illisible"] = remplie & table[propre].isna()
            else:
                table[propre] = pd.array([pd.NA] * len(brut), dtype="Int64")
                table[propre + "_illisible"] = False
        lignes.append(table)
    table = pd.concat(lignes, ignore_index=True).sort_values(["annee", "code_sis"]).reset_index(drop=True)
    illisible = table[[c + "_illisible" for c in COLONNES.values()]].any(axis=1)
    return table.drop(columns=[c + "_illisible" for c in COLONNES.values()]).assign(illisible=illisible)


def departements_manquants(table):
    """S4 : nb de couples année × département du Grand Est absents de la table."""
    presents = set(zip(table["annee"], table["departement"]))
    return sum((a, d) not in presents for a in table["annee"].unique() for d in DEPARTEMENTS_GRAND_EST)


def regles_sis():
    return [
        Regle(
            id="S4", dimension="complétude (population)", portee="interventions_sis.csv, les 10 départements du Grand Est chaque année",
            controle=lambda t: Controle(departements_manquants(t), int(t["annee"].nunique()) * len(DEPARTEMENTS_GRAND_EST),
                                        "années × départements du Grand Est introuvables"),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un département perdu (code sans son 0) fausse les totaux du Grand Est",
        ),
        Regle(
            id="S1", dimension="validité", portee="interventions_sis.csv, nombres (cp1252, séparateurs de milliers)",
            controle=lambda t: Controle(int(t["illisible"].sum()), len(t), "lignes avec une cellule non convertie"),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un nombre lu comme du texte disparaît des totaux",
        ),
        Regle(
            id="S3", dimension="unicité", portee="interventions_sis.csv, année × service",
            controle=lambda t: Controle(int(t.duplicated(["annee", "code_sis"], keep=False).sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un service compté 2 fois la même année fausse la comparaison",
        ),
        Regle(
            id="S2", dimension="complétude (temps)", portee="interventions_sis.csv, feux de végétation",
            controle=lambda t: Controle(int(t["feux_vegetation"].isna().sum()), len(t),
                                        "vide : pas de détail de 2010 à 2013, ou non communiqué"),
            seuil=1.0, severite="tolerer",
            decision="les années absentes restent vides, pas 0",
        ),
    ]
