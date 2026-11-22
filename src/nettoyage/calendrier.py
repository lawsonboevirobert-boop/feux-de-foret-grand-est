"""Calendrier : pour chaque jour et chaque département du Grand Est, le type de jour (calendrier.csv).

Sert à Q3 (le type de jour est une des 3 variables qu'on ajoute à l'indice). Voir
docs/pipeline/plan-nettoyage.md (étape 1, calendrier) et les fiches jours fériés et calendrier scolaire.

Une ligne = un jour × un département : jour de la semaine, week-end, férié, vacances scolaires.
- fériés : zone Alsace-Moselle pour le 57, le 67 et le 68 (Vendredi saint et 26 décembre en plus), métropole ailleurs
- vacances : dates en UTC dans le fichier, converties en heure de Paris (sinon tout est décalé d'un jour).
  Une période va du jour de début (inclus) au jour de reprise (exclu). Avant la rentrée 2017 le fichier
  n'a rien pour le Grand Est : vacances = « non renseigné », jamais « non »
"""

import json

import pandas as pd

from ..qualite.regles import Controle, Regle
from .commun import BRUT, verifier_fichiers

FUSEAU = "Europe/Paris"
DEPARTEMENTS_GRAND_EST = ["08", "10", "51", "52", "54", "55", "57", "67", "68", "88"]
ALSACE_MOSELLE = {"57", "67", "68"}
ACADEMIES = {
    "Reims": ["08", "10", "51", "52"],
    "Nancy-Metz": ["54", "55", "57", "88"],
    "Strasbourg": ["67", "68"],
}
POPULATIONS = {"-", "Élèves"}  # les lignes « Enseignants » ont une autre date de fin l'été
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def lire_feries(dossier=None):
    """{zone: {date: nom}} pour les deux zones."""
    dossier = dossier or BRUT / "jours_feries"
    fichiers = {zone: dossier / f"{zone}.json" for zone in ("alsace-moselle", "metropole")}
    verifier_fichiers(fichiers.values(), "feries")
    return {zone: json.loads(f.read_text(encoding="utf-8")) for zone, f in fichiers.items()}


def lire_scolaire(dossier=None):
    fichier = (dossier or BRUT / "calendrier_scolaire") / "fr-en-calendrier-scolaire.csv"
    verifier_fichiers([fichier], "scolaire")
    return pd.read_csv(fichier, sep=";", dtype=str, encoding="utf-8-sig", keep_default_na=False)


def jour_paris(valeurs):
    """Date-heure UTC du fichier -> jour en heure de Paris (2027-07-02T22:00:00+00:00 -> 2027-07-03)."""
    return pd.to_datetime(valeurs, utc=True).dt.tz_convert(FUSEAU).dt.tz_localize(None).dt.normalize()


def periodes_vacances(scolaire):
    """Les périodes de vacances des académies du Grand Est, en jours de Paris : début inclus, reprise exclue."""
    vac = scolaire[scolaire["location"].isin(ACADEMIES) & scolaire["population"].isin(POPULATIONS)].copy()
    vac["debut"] = jour_paris(vac["start_date"])
    vac["reprise"] = jour_paris(vac["end_date"])
    return vac[vac["reprise"] > vac["debut"]][["location", "description", "annee_scolaire", "debut", "reprise"]]


def table_calendrier(feries, scolaire, debut="2006-01-01", fin="2026-12-31"):
    jours = pd.date_range(debut, fin)
    periodes = periodes_vacances(scolaire)
    lignes = []
    for academie, departements in ACADEMIES.items():
        p = periodes[periodes["location"] == academie]
        couvert_du = pd.Timestamp(f"{p['annee_scolaire'].min()[:4]}-09-01")
        couvert_au = pd.Timestamp(f"{p['annee_scolaire'].max()[-4:]}-08-31")
        en_vacances = pd.Series(False, index=jours)
        for d, r in zip(p["debut"], p["reprise"]):
            en_vacances[(jours >= d) & (jours < r)] = True
        vacances = en_vacances.map({True: "oui", False: "non"})
        vacances[(jours < couvert_du) | (jours > couvert_au)] = "non renseigné"
        for dep in departements:
            zone = feries["alsace-moselle" if dep in ALSACE_MOSELLE else "metropole"]
            texte = jours.strftime("%Y-%m-%d")
            lignes.append(pd.DataFrame({
                "date": texte,
                "departement": dep,
                "jour_semaine": [JOURS[j] for j in jours.day_of_week],
                "week_end": jours.day_of_week >= 5,
                "ferie": [t in zone for t in texte],
                "nom_ferie": [zone.get(t, "") for t in texte],
                "vacances": vacances.values,
            }))
    return pd.concat(lignes, ignore_index=True).sort_values(["date", "departement"]).reset_index(drop=True)


def regles_calendrier():
    return [
        Regle(
            id="C1", dimension="unicité", portee="calendrier.csv, jour × département",
            controle=lambda t: Controle(int(t.duplicated(["date", "departement"], keep=False).sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un jour en double compterait ses feux deux fois",
        ),
        Regle(
            id="C2", dimension="complétude (temps)", portee="calendrier.csv, chaque jour pour les 10 départements",
            controle=lambda t: Controle(
                int(t["date"].nunique() * len(DEPARTEMENTS_GRAND_EST) - len(t)), len(t), "jours × départements manquants"
            ),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un jour sans ligne ferait disparaître ses feux à la jointure",
        ),
        Regle(
            id="C3", dimension="cohérence", portee="calendrier.csv, fériés de l'Alsace-Moselle (57, 67, 68)",
            controle=lambda t: Controle(
                int((t["departement"].isin(ALSACE_MOSELLE) & t["date"].str.endswith("-12-26") & ~t["ferie"]).sum()),
                len(t), "26 décembre non férié en Alsace-Moselle",
            ),
            seuil=0.0, severite="bloquer",
            decision="on arrête : le mauvais fichier de fériés a été pris pour l'Alsace-Moselle",
        ),
        Regle(
            id="C4", dimension="complétude (cellule)", portee="calendrier.csv, vacances",
            controle=lambda t: Controle(int((t["vacances"] == "non renseigné").sum()), len(t),
                                        "avant la rentrée 2017 : pas de données pour le Grand Est"),
            seuil=1.0, severite="tolerer",
            decision="les jours non couverts restent « non renseigné », jamais « non »",
        ),
    ]
