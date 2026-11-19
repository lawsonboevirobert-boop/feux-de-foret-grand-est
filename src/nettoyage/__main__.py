"""Nettoie les données brutes dans data/processed/.

    python -m src.nettoyage            # toutes les étapes déjà codées

Pour l'instant : le COG (communes et passage des anciens codes). Les autres sources
suivront dans l'ordre de docs/pipeline/plan-nettoyage.md. S'arrête avec le code 1
si un contrôle bloquant échoue.
"""

import sys

from . import cog
from .commun import REGION_GRAND_EST, ecrire_csv


def nettoyer_cog():
    print("[cog] communes et passage des anciens codes")
    communes, mouvements = cog.lire_cog()
    table = cog.table_communes(communes)
    passage = cog.table_passage(communes, mouvements)

    bloquants = {
        "G1 format des codes (communes)": cog.controle_format(table, "code_commune", "departement"),
        "unicité du code commune": cog.controle_unicite(table, "code_commune"),
        "G1 format des codes (passage)": cog.controle_format(passage, "code_origine"),
        "unicité du code d'origine": cog.controle_unicite(passage, "code_origine"),
    }
    alertes = {"anciens codes ambigus (communes scindées)": cog.controle_ambigus(passage)}

    for nom, fautifs in {**bloquants, **alertes}.items():
        print(f"  {nom} : {fautifs} fautif(s)")
    if any(bloquants.values()):
        return False

    ecrire_csv(table, "communes.csv")
    ecrire_csv(passage, "passage_communes.csv")
    grand_est = table[table["region"] == REGION_GRAND_EST]
    print(f"  communes.csv : {len(table)} communes, dont {len(grand_est)} dans le Grand Est")
    print(f"  passage_communes.csv : {len(passage)} codes, statuts {passage['statut'].str.split(' :').str[0].value_counts().to_dict()}")
    return True


def main():
    if not nettoyer_cog():
        print("ARRET : contrôle bloquant en échec")
        sys.exit(1)


if __name__ == "__main__":
    main()
