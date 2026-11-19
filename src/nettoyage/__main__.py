"""Nettoie les données brutes dans data/processed/.

    python -m src.nettoyage            # toutes les étapes déjà codées

Pour l'instant : le COG (communes et passage des anciens codes). Les autres sources
suivront dans l'ordre de docs/pipeline/plan-nettoyage.md. Les contrôles passent par la
barrière de src/qualite : s'arrête avec le code 1 si une règle bloquante échoue.
"""

import sys

import pandas as pd

from ..qualite.regles import QualiteBloquante, barriere, executer
from . import cog
from .commun import REGION_GRAND_EST, ecrire_csv


def afficher(rapport):
    for ligne in rapport.itertuples(index=False):
        print(f"  {ligne[0]} {ligne[6]} ({ligne[5]}/{ligne[4]} fautifs, {ligne[7]}) : {ligne[2]}")


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


def main():
    try:
        nettoyer_cog()
    except QualiteBloquante as erreur:
        print(f"ARRET : {erreur}")
        sys.exit(1)


if __name__ == "__main__":
    main()
