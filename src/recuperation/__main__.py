"""Récupère les données brutes du projet.

Exemples :
    python -m src.recuperation                      # toutes les sources
    python -m src.recuperation mdf sis cog          # seulement certaines
    python -m src.recuperation bdforet --departements 67
    python -m src.recuperation --forcer             # retélécharge tout
"""

import argparse
import sys

from . import sources
from .commun import DEPARTEMENTS_GRAND_EST

SOURCES = {
    "mdf": ("Archives de la Météo des forêts", sources.meteo_des_forets),
    "sis": ("Interventions des services d'incendie et de secours", sources.interventions_sis),
    "cog": ("Code officiel géographique 2026", sources.cog),
    "bdiff": ("BDIFF, Grand Est 2006-2025", sources.bdiff),
    "bdforet": ("BD Forêt V2", sources.bd_foret),
    "copernicus": ("FWI Copernicus, Grand Est", sources.copernicus_fwi),
    "feries": ("Jours fériés (Alsace-Moselle et métropole)", sources.jours_feries),
    "scolaire": ("Calendrier scolaire", sources.calendrier_scolaire),
    "firms": ("Détections satellite NASA FIRMS 2026, Grand Est", sources.firms),
}


def main():
    parser = argparse.ArgumentParser(description="Télécharge les données brutes dans data/raw/.")
    parser.add_argument("sources", nargs="*",
                        help=f"sources à récupérer parmi {', '.join(SOURCES)} (par défaut : toutes)")
    parser.add_argument("--departements", nargs="+", default=DEPARTEMENTS_GRAND_EST,
                        help="départements pour la BDIFF et la BD Forêt (par défaut : Grand Est)")
    parser.add_argument("--forcer", action="store_true", help="retélécharger même si le fichier existe")
    args = parser.parse_args()
    inconnues = [s for s in args.sources if s not in SOURCES]
    if inconnues:
        parser.error(f"source inconnue : {', '.join(inconnues)} (choix : {', '.join(SOURCES)})")

    en_erreur = []
    for cle in args.sources or SOURCES:
        titre, fonction = SOURCES[cle]
        print(f"[{cle}] {titre}")
        options = {"forcer": args.forcer}
        if cle in ("bdiff", "bdforet"):
            options["departements"] = args.departements
        try:
            fonction(**options)
        except Exception as erreur:  # une source en panne ne doit pas bloquer les autres
            print(f"  ERREUR : {erreur}")
            en_erreur.append(cle)

    # Code de sortie 1 si une source a échoué : la suite (nettoyage) ne doit pas partir sur des données incomplètes.
    if en_erreur:
        sys.exit(f"sources en erreur : {', '.join(en_erreur)}")


if __name__ == "__main__":
    main()
