"""Outils partagés par les scripts de récupération : chemins et téléchargement."""

from pathlib import Path

import requests
import truststore

# Le site de la BDIFF envoie une chaîne de certificats incomplète : Windows sait la
# compléter, pas la liste de certificats de Python. On fait donc vérifier les
# certificats par le système (la vérification reste active).
truststore.inject_into_ssl()

RACINE = Path(__file__).resolve().parents[2]
DONNEES_BRUTES = RACINE / "data" / "raw"

# Les 10 départements du Grand Est
DEPARTEMENTS_GRAND_EST = ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"]

API_DATA_GOUV = "https://www.data.gouv.fr/api/1/datasets/"


def dossier(nom):
    """Renvoie le dossier data/raw/<nom>, créé s'il n'existe pas."""
    chemin = DONNEES_BRUTES / nom
    chemin.mkdir(parents=True, exist_ok=True)
    return chemin


def telecharger(url, destination, session=None, forcer=False):
    """Télécharge url dans destination. Ne refait rien si le fichier existe déjà, sauf si forcer."""
    destination = Path(destination)
    if destination.exists() and not forcer:
        print(f"  déjà présent : {destination.relative_to(RACINE)}")
        return destination
    client = session or requests
    with client.get(url, stream=True, timeout=120) as reponse:
        reponse.raise_for_status()
        temporaire = destination.with_suffix(destination.suffix + ".part")
        with open(temporaire, "wb") as fichier:
            for bloc in reponse.iter_content(chunk_size=1 << 16):
                fichier.write(bloc)
        temporaire.replace(destination)
    print(f"  téléchargé : {destination.relative_to(RACINE)} ({destination.stat().st_size // 1024} Ko)")
    return destination


def ressources_data_gouv(identifiant):
    """Liste les ressources (titre, url) d'un jeu de données data.gouv.fr."""
    reponse = requests.get(API_DATA_GOUV + identifiant + "/", timeout=60)
    reponse.raise_for_status()
    return [(r["title"], r["url"]) for r in reponse.json()["resources"]]
