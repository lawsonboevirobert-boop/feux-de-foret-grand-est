"""Lecture de l'export BDIFF et ses règles de qualité.

Voir docs/sources/fiche-bdiff.md pour le format du fichier et docs/qualite/regles.md
pour la liste complète des règles. Ici on code les 3 premières en tests :
- B2 (unicité) : Année + Numéro identifie un feu
- B4 (cohérence dans la ligne) : l'Année = l'année de la date de première alerte
- P1 (complétude de la population) : chaque département a au moins un feu chaque année
"""

import re

import pandas as pd

from .regles import Controle, Regle

DEPARTEMENTS_GRAND_EST = ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"]

# B1 : le schéma attendu, vérifié juste apres la lecture (avant toute règle)
COLONNES_ATTENDUES = [
    "Année", "Numéro", "Département", "Code INSEE", "Nom de la commune",
    "Date de première alerte", "Surface parcourue (m2)", "Surface forêt (m2)", "Nature",
]
NB_COLONNES = 24
LIGNES_AVANT_ENTETE = 3


def lire_criteres(ligne):
    """Années et départements demandés, lus dans la ligne des critères de l'export.

    Il y a 2 formats :
    - export fait à la main sur le site : « de : 2006-01-01 » / « jusqu'à : 2025-12-31 » et « Région administrative : GRAND-EST »
    - export du script de récupération (#45) : « Période de répétition de la sélection : 2006,2025 » et « Département(s) : 08, 10, ... »
    Si on ne trouve pas la période ou les départements : ValueError (B1, bloquant), on ne devine pas.
    """
    annees = re.findall(r"(\d{4})-\d{2}-\d{2}", ligne)
    if len(annees) < 2:
        repetition = re.search(r"(\d{4})\s*,\s*(\d{4})", ligne)
        annees = list(repetition.groups()) if repetition else []
    if len(annees) < 2:
        raise ValueError(f"B1 période introuvable dans les critères : {ligne[:150]!r}")
    periode = list(range(int(annees[0]), int(annees[1]) + 1))

    liste = re.search(r"Département\(s\)\s*:\s*([^\"]+)", ligne)
    if liste:
        departements = re.findall(r"\b(\d{2}|2A|2B)\b", liste.group(1))
    elif "GRAND-EST" in ligne.upper():
        departements = list(DEPARTEMENTS_GRAND_EST)
    else:
        raise ValueError(f"B1 départements introuvables dans les critères : {ligne[:150]!r}")
    return periode, departements


def lire_bdiff(chemin):
    """Lit l'export CSV de la BDIFF. Tout en texte pour ne pas perdre le 0 des codes (08, 08105).

    Renvoie la table, les années et les départements demandés dans l'export (ligne des critères).
    Lève ValueError si le schéma ou les critères ne sont pas ceux attendus (règle B1, bloquante).
    """
    with open(chemin, encoding="utf-8") as fichier:
        entete = [next(fichier) for _ in range(LIGNES_AVANT_ENTETE)]
    df = pd.read_csv(chemin, sep=";", skiprows=LIGNES_AVANT_ENTETE, dtype=str, encoding="utf-8")

    manquantes = [c for c in COLONNES_ATTENDUES if c not in df.columns]
    if manquantes or len(df.columns) != NB_COLONNES:
        raise ValueError(f"B1 schéma BDIFF inattendu : {len(df.columns)} colonnes, manquantes {manquantes}")

    periode, departements = lire_criteres(entete[2])
    return df, periode, departements


def _resumer_annees(annees):
    """[2012, 2013, 2014, 2016] -> '2012-2014, 2016'."""
    morceaux, debut, prec = [], None, None
    for annee in sorted(annees):
        if debut is None:
            debut = prec = annee
        elif annee == prec + 1:
            prec = annee
        else:
            morceaux.append(f"{debut}-{prec}" if prec > debut else str(debut))
            debut = prec = annee
    if debut is not None:
        morceaux.append(f"{debut}-{prec}" if prec > debut else str(debut))
    return ", ".join(morceaux)


def controle_cle_unique(df):
    """B2 : Année + Numéro ne doit jamais apparaitre 2 fois."""
    doublons = df.duplicated(["Année", "Numéro"], keep=False)
    return Controle(int(doublons.sum()), len(df), f"{int(doublons.sum())} lignes en double sur la clé")


def controle_annee_date(df):
    """B4 : l'Année de la ligne = l'année de la date de première alerte (date illisible = fautive)."""
    dates = pd.to_datetime(df["Date de première alerte"], errors="coerce")
    illisibles = dates.isna()
    differentes = ~illisibles & (dates.dt.year.astype("Int64").astype(str) != df["Année"])
    fautifs = int((illisibles | differentes).sum())
    return Controle(fautifs, len(df), f"{int(illisibles.sum())} dates illisibles, {int(differentes.sum())} années différentes")


def controle_population(departements, annees):
    """P1 : on compare au référentiel (départements x années) ce qui est arrivé.

    Un couple sans aucun feu n'est pas un 0 : c'est "non renseigné" tant qu'on n'a pas
    vérifié avec une autre source (interventions SIS).
    """
    def controle(df):
        attendus = {(d, a) for d in departements for a in annees}
        observes = set(zip(df["Département"], df["Année"].astype(int)))
        manquants = attendus - observes
        par_dep = {}
        for dep, annee in manquants:
            par_dep.setdefault(dep, []).append(annee)
        detail = " ; ".join(f"{d} : {_resumer_annees(a)}" for d, a in sorted(par_dep.items()))
        return Controle(len(manquants), len(attendus), detail)
    return controle


def regles_bdiff(annees, departements=DEPARTEMENTS_GRAND_EST):
    """Les 3 règles de la BDIFF codées pour l'instant."""
    return [
        Regle(
            id="B2", dimension="unicité",
            portee="toutes les lignes, clé Année + Numéro",
            controle=controle_cle_unique, seuil=0.0, severite="bloquer",
            decision="on arrete le chargement et on regarde l'export (un feu compté 2 fois fausse les surfaces)",
        ),
        Regle(
            id="B4", dimension="cohérence",
            portee="toutes les lignes, colonnes Année et Date de première alerte",
            controle=controle_annee_date, seuil=0.0, severite="bloquer",
            decision="on arrete le chargement : sans date sure, le feu ne peut pas etre relié au niveau du jour",
        ),
        Regle(
            id="P1", dimension="complétude (population)",
            portee=f"{len(departements)} départements x {len(annees)} années demandées dans l'export",
            controle=controle_population(departements, annees), seuil=0.0, severite="alerter",
            decision="on charge, mais ces départements-années sont marqués non renseignés et exclus des taux",
        ),
    ]
