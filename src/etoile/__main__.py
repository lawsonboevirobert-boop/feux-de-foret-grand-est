"""Construit le modèle en étoile dans data/processed/etoile/, à partir des tables du nettoyage.

    python -m src.nettoyage     # d'abord
    python -m src.etoile

Les contrôles E1 à E5 passent par la barrière de src/qualite : s'arrête avec le code 1 si une règle
bloquante échoue, ou si une table du nettoyage manque.
"""

import datetime as dt
import sys

import pandas as pd

from ..nettoyage.commun import BRUT, PROPRE, SourceManquante, ecrire_csv
from ..qualite.regles import QualiteBloquante, barriere, executer
from . import tables

DOSSIER = PROPRE / "etoile"
TEXTE = {"departement": str, "code_commune_2026": str, "code_commune_origine": str, "code_origine": str}


def lire(nom, dossier=PROPRE):
    chemin = dossier / nom
    if not chemin.exists():
        raise SourceManquante(f"{nom} introuvable dans data/processed : lancer d'abord `python -m src.nettoyage`")
    return pd.read_csv(chemin, dtype=TEXTE, keep_default_na=True)


def jours_fwi():
    """Les dates couvertes par les fichiers FWI (celles de fwi_maille.csv, comme T7), ou None sans l'étape 5."""
    chemin = PROPRE / "fwi_maille.csv"
    if not chemin.exists():
        return None
    return pd.read_csv(chemin, usecols=["date"], dtype=str)["date"].unique()


def construire(aujourd_hui=None):
    aujourd_hui = aujourd_hui or dt.date.today().isoformat()
    feux = lire("feux.csv")
    cm = lire("commune_maille.csv")
    precedent = lire("fait_feu.csv", DOSSIER) if (DOSSIER / "fait_feu.csv").exists() else None
    cog = BRUT / "cog"
    departements = pd.read_csv(cog / "v_departement_2026.csv", dtype=str, keep_default_na=False)
    mouvements = pd.read_csv(cog / "v_mvt_commune_2026.csv", dtype=str, keep_default_na=False)

    t = {
        "dim_date": tables.dim_date(lire("calendrier.csv")),
        "dim_departement": tables.dim_departement(departements),
        "dim_maille": tables.dim_maille(cm),
        "dim_commune": tables.dim_commune(cm, lire("foret_commune.csv")),
        "dim_niveau": tables.dim_niveau(),
        "dim_cause": tables.dim_cause(feux),
        "fait_feu": tables.fait_feu(feux, aujourd_hui, precedent),
        "fait_jour_departement": tables.fait_jour_departement(lire("jour_departement.csv")),
    }
    t["dim_commune_historique"] = tables.dim_commune_historique(
        lire("passage_communes.csv"), mouvements, t["dim_commune"]["code_commune_2026"])
    return t, feux


def main():
    print("[etoile] faits et dimensions")
    try:
        t, feux = construire()
        rapport = executer({**t, "feux": feux, "jours_fwi": jours_fwi()}, tables.regles_etoile())
        for _, r in rapport.iterrows():
            print(f"  {r['règle']} {r['résultat']} ({r['fautifs']}/{r['contrôlés']} fautifs, {r['sévérité']}) : {r['portée']}")
        alertes = barriere(rapport)
    except (QualiteBloquante, SourceManquante, ValueError) as erreur:
        print(f"ARRET : {erreur}")
        sys.exit(1)

    for nom, table in t.items():
        ecrire_csv(table, f"{nom}.csv", DOSSIER)
        print(f"  {nom}.csv : {len(table)} lignes")
    ecrire_csv(rapport, "rapport_qualite_etoile.csv", DOSSIER)
    print(f"  barrière passée, alertes : {', '.join(alertes) or 'aucune'}")


if __name__ == "__main__":
    main()
