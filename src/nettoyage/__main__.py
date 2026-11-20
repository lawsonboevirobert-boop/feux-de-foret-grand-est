"""Nettoie les données brutes dans data/processed/.

    python -m src.nettoyage            # toutes les étapes déjà codées

Pour l'instant : le COG (communes et passage des anciens codes), puis la BDIFF (feux.csv). Les autres sources
suivront dans l'ordre de docs/pipeline/plan-nettoyage.md. Les contrôles passent par la
barrière de src/qualite : s'arrête avec le code 1 si une règle bloquante échoue.
"""

import sys

import pandas as pd

from ..qualite.__main__ import trouver_csv
from ..qualite.bdiff import lire_bdiff, regles_bdiff
from ..qualite.regles import QualiteBloquante, barriere, executer
from . import bdiff, cog
from .commun import REGION_GRAND_EST, SourceManquante, ecrire_csv


def afficher(rapport):
    """Une ligne par règle. Les colonnes sont lues par leur nom : ajouter une colonne au rapport ne casse rien."""
    for ligne in rapport.to_dict("records"):
        print(f"  {ligne['règle']} {ligne['résultat']} ({ligne['fautifs']}/{ligne['contrôlés']} fautifs, "
              f"{ligne['sévérité']}) : {ligne['portée']}")


def nettoyer_cog():
    print("[cog] communes et passage des anciens codes")
    communes, mouvements = cog.lire_cog()
    table = cog.table_communes(communes)
    passage = cog.table_passage(communes, mouvements)

    rapport = pd.concat([executer(table, cog.regles_communes()), executer(passage, cog.regles_passage())])
    afficher(rapport)
    alertes = barriere(rapport)  # lève QualiteBloquante avant d'écrire quoi que ce soit

    ecrire_csv(table, "communes.csv")
    ecrire_csv(passage, "passage_communes.csv")
    ecrire_csv(rapport, "rapport_qualite_cog.csv")
    grand_est = table[table["region"] == REGION_GRAND_EST]
    print(f"  communes.csv : {len(table)} communes, dont {len(grand_est)} dans le Grand Est")
    print(f"  passage_communes.csv : {len(passage)} codes, statuts {passage['statut'].str.split(' :').str[0].value_counts().to_dict()}")
    print(f"  barrière passée, alertes : {', '.join(alertes) or 'aucune'}")
    return passage


def nettoyer_bdiff(passage, chemin=None):
    print("[bdiff] feux")
    brut, annees, departements = lire_bdiff(chemin or trouver_csv())  # B1 : schéma vérifié ici
    feux = bdiff.nettoyer_feux(brut, passage)

    rapport = pd.concat([executer(brut, regles_bdiff(annees, departements)), executer(feux, bdiff.regles_feux())])
    afficher(rapport)
    alertes = barriere(rapport)

    ecrire_csv(feux, "feux.csv")
    ecrire_csv(bdiff.population(feux, annees, departements), "bdiff_population.csv")
    ecrire_csv(rapport, "rapport_qualite_bdiff.csv")
    gardes = feux[~feux["doublon_probable"]]
    print(f"  feux.csv : {len(feux)} feux ({len(gardes)} hors doublons probables), "
          f"{len(departements)} départements, {annees[0]}-{annees[-1]}")
    print(f"  barrière passée, alertes : {', '.join(alertes) or 'aucune'}")


def main():
    try:
        passage = nettoyer_cog()
        nettoyer_bdiff(passage)
    except (QualiteBloquante, SourceManquante) as erreur:
        print(f"ARRET : {erreur}")
        sys.exit(1)


if __name__ == "__main__":
    main()
