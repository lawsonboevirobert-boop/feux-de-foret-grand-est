"""BDIFF : la liste des feux nettoyée, une ligne par feu (feux.csv).

Voir docs/pipeline/plan-nettoyage.md (étape 1, BDIFF) et docs/qualite/regles.md (B1 à B10, G2, G3, P1).
La lecture et les règles B1, B2, B4, P1 viennent de src/qualite/bdiff.py (#49).

Ce qu'on garde (minimisation) : identifiant, commune (code d'origine et code 2026), département,
date et heure de première alerte, surface parcourue et surface forêt en ha, cause, précision.
Ce qu'on jette : nom de la commune, décès, bâtiments détruits, surfaces non comparables avant et
après 2023 (B10), type de peuplement et surface maquis (toujours vides).
"""

import pandas as pd

from ..qualite.regles import Controle, Regle

M2_PAR_HA = 10_000
SURFACE_A_VERIFIER_HA = 500  # B8 : plus gros feu vu dans le Grand Est : 180 ha


def nettoyer_feux(brut, passage):
    """Table des feux propre à partir de l'export brut (tout en texte) et de la table de passage du COG."""
    vers_2026 = dict(zip(passage["code_origine"], passage["code_commune_2026"]))
    alerte = pd.to_datetime(brut["Date de première alerte"], errors="coerce")
    heure = alerte.dt.strftime("%H:%M").where(alerte.dt.strftime("%H:%M:%S") != "00:00:00", "")  # B5

    feux = pd.DataFrame({
        "id_feu": brut["Année"] + "-" + brut["Numéro"],
        "annee": brut["Année"].astype(int),
        "numero": brut["Numéro"].astype(int),
        "departement": brut["Département"],
        "code_commune_origine": brut["Code INSEE"],
        "code_commune_2026": brut["Code INSEE"].map(vers_2026).fillna(""),
        "date": alerte.dt.strftime("%Y-%m-%d"),
        "heure": heure,
        "surface_parcourue_ha": pd.to_numeric(brut["Surface parcourue (m2)"], errors="coerce") / M2_PAR_HA,
        "surface_foret_ha": pd.to_numeric(brut["Surface forêt (m2)"], errors="coerce") / M2_PAR_HA,
        "cause": brut["Nature"].fillna("").str.strip().replace("", "inconnue"),  # B9
        "precision": brut["Précision de la donnée"].fillna(""),
    })
    feux = feux.sort_values(["annee", "numero"]).reset_index(drop=True)
    feux["doublon_probable"] = feux.duplicated(  # B3 : on garde le premier, les suivants sont marqués
        ["code_commune_2026", "date", "heure", "surface_parcourue_ha"], keep="first"
    ) & (feux["heure"] != "")
    return feux


def population(feux, annees, departements):
    """P1 : une ligne par département et par année demandés dans l'export.

    Un couple sans aucun feu est « non renseigné », jamais « 0 feu » (sous-saisie probable).
    """
    comptes = feux[~feux["doublon_probable"]].groupby(["departement", "annee"]).size()
    lignes = []
    for dep in departements:
        for annee in annees:
            nb = int(comptes.get((dep, annee), 0))
            lignes.append({
                "departement": dep, "annee": annee,
                "nb_feux": nb if nb else "",
                "statut_bdiff": "renseigné" if nb else "non renseigné",
            })
    return pd.DataFrame(lignes)


def _compte(masque, total, detail=""):
    return Controle(int(masque.sum()), total, detail)


def regles_feux():
    """Règles sur feux.csv (les règles sur l'export brut sont dans src/qualite/bdiff.py)."""
    return [
        Regle(
            id="G2", dimension="cohérence", portee="feux.csv, code commune",
            controle=lambda t: _compte(t["code_commune_2026"] == "", len(t), "codes sans commune 2026 après passage"),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un feu sans commune 2026 ne peut être relié ni à une maille ni à un secteur",
        ),
        Regle(
            id="G3", dimension="cohérence", portee="feux.csv, code commune et département",
            controle=lambda t: _compte(t["code_commune_2026"].str[:2] != t["departement"], len(t)),
            seuil=0.0, severite="alerter",
            decision="on charge, les feux concernés sont listés dans le rapport",
        ),
        Regle(
            id="B3", dimension="unicité", portee="feux.csv, commune + date et heure + surface",
            controle=lambda t: _compte(t["doublon_probable"], len(t), "marqués doublon probable, le premier est gardé"),
            seuil=0.0, severite="alerter",
            decision="on garde le premier, les autres sont marqués et sortis des comptes",
        ),
        Regle(
            id="B5", dimension="exactitude", portee="feux.csv, heure",
            controle=lambda t: _compte(t["heure"] == "", len(t), "heure 00:00:00 = inconnue, mise à vide"),
            seuil=1.0, severite="tolerer",
            decision="on garde la date, l'heure est vide",
        ),
        Regle(
            id="B6", dimension="validité", portee="feux.csv, surfaces",
            controle=lambda t: _compte(
                t["surface_parcourue_ha"].isna() | (t["surface_parcourue_ha"] < 0) | (t["surface_foret_ha"] < 0), len(t)
            ),
            seuil=0.0, severite="bloquer",
            decision="on arrête : une surface manquante ou négative fausse la gravité des feux",
        ),
        Regle(
            id="B7", dimension="cohérence", portee="feux.csv, surface forêt et surface parcourue",
            controle=lambda t: _compte(t["surface_foret_ha"] > t["surface_parcourue_ha"], len(t)),
            seuil=0.0, severite="alerter",
            decision="on charge, les feux concernés sont listés",
        ),
        Regle(
            id="B8", dimension="exactitude", portee=f"feux.csv, surface parcourue > {SURFACE_A_VERIFIER_HA} ha",
            controle=lambda t: _compte(t["surface_parcourue_ha"] > SURFACE_A_VERIFIER_HA, len(t)),
            seuil=1.0, severite="tolerer",
            decision="on regarde à la main, on ne corrige pas sans preuve",
        ),
        Regle(
            id="B9", dimension="complétude (cellule)", portee="feux.csv, cause",
            controle=lambda t: _compte(t["cause"] == "inconnue", len(t), "cause vide = inconnue, jamais devinée"),
            seuil=1.0, severite="tolerer",
            decision="on garde « inconnue », la part des causes se donne sur les feux connus",
        ),
    ]
