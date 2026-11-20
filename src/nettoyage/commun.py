"""Outils partagés par le nettoyage : chemins et écriture des tables."""

from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
BRUT = RACINE / "data" / "raw"
PROPRE = RACINE / "data" / "processed"

# Les 10 départements du Grand Est (région 44 au COG)
REGION_GRAND_EST = "44"


class SourceManquante(Exception):
    """Levée quand un fichier brut n'est pas dans data/raw : on dit quelle récupération lancer."""


def verifier_fichiers(fichiers, source):
    """Lève SourceManquante si un des fichiers bruts n'existe pas."""
    manquants = [f.name for f in fichiers if not f.exists()]
    if manquants:
        raise SourceManquante(
            f"{', '.join(manquants)} introuvable dans data/raw : lancer d'abord `python -m src.recuperation {source}`"
        )


def ecrire_csv(df, nom, dossier=None):
    """Écrit une table propre en CSV UTF-8 (séparateur virgule, sans index), comme décidé dans #58."""
    dossier = Path(dossier) if dossier else PROPRE
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / nom
    df.to_csv(chemin, index=False, encoding="utf-8")
    return chemin
