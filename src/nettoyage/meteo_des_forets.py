"""Météo des forêts : le niveau de danger de chaque jour, par département (meteo_des_forets.csv).

Voir docs/pipeline/plan-nettoyage.md (étape 1) et docs/qualite/regles.md (M1 à M6).

Une ligne = le jour concerné × un département. Le niveau est `niveau_j1` du bulletin publié
la veille (M5) : c'est lui qui sert à déclencher le renfort. `niveau_j2` n'est pas gardé.
"""

import gzip

import pandas as pd

from ..qualite.regles import Controle, Regle
from .cog import MOTIF_DEPARTEMENT
from .commun import BRUT, verifier_fichiers

COLONNES = ["date", "num_dep", "niveau_j1"]
NIVEAUX = {"1", "2", "3", "4"}  # faible, modéré, élevé, très élevé
FUSEAU = "Europe/Paris"


def lire_fichier(chemin):
    """M1 : séparateur `,` (2024-2025) ou `;` (2026), lu sur la première ligne. Tout en texte."""
    with gzip.open(chemin, "rt", encoding="utf-8") as fichier:
        entete = fichier.readline()
    brut = pd.read_csv(chemin, sep=";" if ";" in entete else ",", dtype=str, keep_default_na=False)
    manquantes = [c for c in COLONNES if c not in brut.columns]
    if manquantes:
        raise ValueError(f"M1 schéma inattendu dans {chemin.name} : colonnes manquantes {manquantes}")
    return brut[COLONNES]  # le nom du département (`nom_dep` ou `dep_nom`) ne sert pas


def lire_mdf(dossier=None):
    dossier = dossier or BRUT / "meteo_des_forets"
    fichiers = sorted(dossier.glob("mdf_*.csv.gz"))
    if not fichiers:
        verifier_fichiers([dossier / "mdf_AAAA.csv.gz"], "mdf")
    return pd.concat([lire_fichier(f) for f in fichiers], ignore_index=True)


def nettoyer_mdf(brut):
    """Une ligne par bulletin, avec le jour concerné en heure de Paris.

    - M2 : code département remis sur 2 caractères (`8` -> `08`)
    - M5 : la date de diffusion est en UTC. On la passe en heure de Paris, puis + 1 jour (niveau_j1)
    - M4 : s'il y a plusieurs bulletins pour le même jour et le même département, le dernier publié
      est gardé, les autres sont marqués `remplace`
    """
    diffusion = pd.to_datetime(brut["date"], utc=True, errors="coerce").dt.tz_convert(FUSEAU)
    table = pd.DataFrame({
        "date": (diffusion.dt.normalize() + pd.Timedelta(days=1)).dt.strftime("%Y-%m-%d"),
        "departement": brut["num_dep"].str.strip().str.upper().str.zfill(2),
        "niveau": brut["niveau_j1"].str.strip(),
        "date_diffusion": diffusion.dt.strftime("%Y-%m-%d %H:%M"),
    })
    table = table.sort_values(["date", "departement", "date_diffusion"]).reset_index(drop=True)
    table["remplace"] = table.duplicated(["date", "departement"], keep="last")
    return table


def jours_manquants(table):
    """M6 : couples jour × département absents, dans chaque saison publiée (du 1er au dernier jour de l'année)."""
    gardes = table[~table["remplace"]]
    departements = sorted(gardes["departement"].unique())
    manquants = 0
    for _, saison in gardes.groupby(gardes["date"].str[:4]):
        jours = pd.date_range(saison["date"].min(), saison["date"].max()).strftime("%Y-%m-%d")
        attendus = {(j, d) for j in jours for d in departements}
        manquants += len(attendus - set(zip(saison["date"], saison["departement"])))
    return manquants


def regles_mdf():
    return [
        Regle(
            id="M2", dimension="validité", portee="meteo_des_forets.csv, code département",
            controle=lambda t: Controle(int((~t["departement"].str.match(MOTIF_DEPARTEMENT)).sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : sans le 0 devant, les Ardennes (08) se perdent à la jointure",
        ),
        Regle(
            id="M3", dimension="validité", portee="meteo_des_forets.csv, niveau (1 à 4)",
            controle=lambda t: Controle(int((~t["niveau"].isin(NIVEAUX)).sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un niveau hors de 1 à 4 n'a pas de sens pour le seuil",
        ),
        Regle(
            id="M5", dimension="cohérence", portee="meteo_des_forets.csv, date de diffusion lisible",
            controle=lambda t: Controle(int(t["date"].isna().sum()), len(t), "date illisible = jour concerné inconnu"),
            seuil=0.0, severite="bloquer",
            decision="on arrête : sans date, le niveau ne peut pas être relié au jour d'un feu",
        ),
        Regle(
            id="M4", dimension="unicité", portee="meteo_des_forets.csv, jour × département",
            controle=lambda t: Controle(int(t["remplace"].sum()), len(t), "bulletins remplacés par un plus récent"),
            seuil=0.0, severite="alerter",
            decision="on garde le dernier bulletin publié",
        ),
        Regle(
            id="M6", dimension="complétude (temps)", portee="meteo_des_forets.csv, chaque jour de chaque saison publiée",
            controle=lambda t: Controle(jours_manquants(t), len(t), "couples jour × département manquants"),
            seuil=0.0, severite="alerter",
            decision="on charge, les jours manquants restent sans niveau (jamais « faible » par défaut)",
        ),
    ]
