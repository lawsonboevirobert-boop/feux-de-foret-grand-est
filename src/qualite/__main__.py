"""Profil + règles de qualité de la BDIFF, et barrière.

    python -m src.qualite                     # cherche le CSV dans data/raw/bdiff/
    python -m src.qualite chemin/vers/export.csv

Écrit docs/qualite/profil-bdiff.md et docs/qualite/resultats-bdiff.md, puis
s'arrete avec le code 1 si une règle bloquante échoue (barrière de qualité).
"""

import argparse
import sys
from pathlib import Path

from .bdiff import lire_bdiff, regles_bdiff
from .profil import profil, remplissage_par_groupe
from .regles import QualiteBloquante, barriere, executer

RACINE = Path(__file__).resolve().parents[2]


def tableau_md(df):
    """DataFrame -> tableau markdown (sans dépendance en plus)."""
    entete = "| " + " | ".join(str(c) for c in df.columns) + " |"
    separateur = "|" + "---|" * len(df.columns)
    lignes = ["| " + " | ".join(str(v).replace("|", "/") for v in ligne) + " |" for ligne in df.itertuples(index=False)]
    return "\n".join([entete, separateur, *lignes])


def trouver_csv(dossier=RACINE / "data" / "raw" / "bdiff"):
    """Le CSV de la BDIFF sous data/raw/bdiff/ (son nom change selon qu'on l'a pris à la main ou par le script).

    S'il y en a plusieurs (par ex. un export Grand Est et un export du 67 seul), on s'arrete :
    prendre le mauvais sans rien dire réécrirait les pages versionnées avec de faux chiffres.
    """
    candidats = sorted(Path(dossier).rglob("*.csv"))
    if not candidats:
        sys.exit("pas de CSV BDIFF dans data/raw/bdiff/ : lancer d'abord la récupération (#38)")
    if len(candidats) > 1:
        liste = "\n".join(f"  {c}" for c in candidats)
        sys.exit(f"plusieurs exports BDIFF, donner le chemin de celui à contrôler :\n{liste}")
    return candidats[0]


def main():
    parser = argparse.ArgumentParser(description="Profil et règles de qualité de la BDIFF.")
    parser.add_argument("chemin", nargs="?", help="export CSV de la BDIFF")
    parser.add_argument("--sortie", default=str(RACINE / "docs" / "qualite"), help="dossier des pages générées")
    args = parser.parse_args()

    chemin = Path(args.chemin) if args.chemin else trouver_csv()
    sortie = Path(args.sortie)
    df, annees, departements = lire_bdiff(chemin)  # B1 : schéma et critères vérifiés ici, sinon ValueError
    perimetre = f"{len(departements)} départements, {annees[0]}-{annees[-1]}"
    print(f"BDIFF : {len(df)} feux, {perimetre}")
    entete = f"Généré par `python -m src.qualite` sur l'export BDIFF ({perimetre}). Ne pas modifier à la main, relancer le script."

    cause = remplissage_par_groupe(df, "Nature", "Département")
    (sortie / "profil-bdiff.md").write_text(
        "# Profil de la BDIFF\n\n" + entete + "\n\n"
        + f"{len(df)} lignes, {len(df.columns)} colonnes. Schéma vérifié (règle B1).\n\n"
        + "Le profil dit ou chercher, pas si la donnée est bonne. Les colonnes texte n'affichent pas de valeur.\n\n"
        + "## Colonne par colonne\n\n" + tableau_md(profil(df)) + "\n\n"
        + "## La cause (Nature) par département\n\n"
        + "Le remplissage global cache des écarts entre départements (complétude par segment).\n\n"
        + tableau_md(cause) + "\n",
        encoding="utf-8",
    )

    rapport = executer(df, regles_bdiff(annees, departements))
    (sortie / "resultats-bdiff.md").write_text(
        "# Résultats des règles de qualité, BDIFF\n\n" + entete + "\n\n"
        + "Règles : voir [regles.md](regles.md). Lecture : [rapport-qualite.md](rapport-qualite.md).\n\n"
        + tableau_md(rapport) + "\n",
        encoding="utf-8",
    )
    for ligne in rapport.itertuples(index=False):
        print(f"  {ligne[0]} {ligne[6]} ({ligne[5]}/{ligne[4]} fautifs, {ligne[7]})")

    try:
        alertes = barriere(rapport)
    except QualiteBloquante as erreur:
        print(f"ARRET : {erreur}")
        sys.exit(1)
    print(f"barrière passée, alertes : {', '.join(alertes) or 'aucune'}")


if __name__ == "__main__":
    main()
