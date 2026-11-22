"""Nettoie les données brutes dans data/processed/.

    python -m src.nettoyage            # toutes les étapes déjà codées

Pour l'instant : le COG (communes et passage des anciens codes), la BDIFF (feux.csv), la Météo
des forêts, les interventions des SIS, le calendrier (fériés, vacances) et les détections FIRMS 2026.
Puis les tables de travail (feux_travail.csv, jour_departement.csv) et la BD Forêt (foret_commune.csv).
Copernicus suivra (étape 5), dans l'ordre de
docs/pipeline/plan-nettoyage.md. Les contrôles passent par la barrière de src/qualite :
s'arrête avec le code 1 si une règle bloquante échoue (ou si un fichier brut manque, ou si
son schéma n'est pas celui attendu).
"""

import sys

import pandas as pd

from ..qualite.__main__ import trouver_csv
from ..qualite.bdiff import lire_bdiff, regles_bdiff
from ..qualite.regles import QualiteBloquante, barriere, executer
from . import bd_foret, bdiff, calendrier, cog, firms, interventions_sis, meteo_des_forets, tables
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

    population = bdiff.population(feux, annees, departements)
    ecrire_csv(feux, "feux.csv")
    ecrire_csv(population, "bdiff_population.csv")
    ecrire_csv(rapport, "rapport_qualite_bdiff.csv")
    gardes = feux[~feux["doublon_probable"]]
    print(f"  feux.csv : {len(feux)} feux ({len(gardes)} hors doublons probables), "
          f"{len(departements)} départements, {annees[0]}-{annees[-1]}")
    print(f"  barrière passée, alertes : {', '.join(alertes) or 'aucune'}")
    return feux, population


def nettoyer_meteo_des_forets():
    print("[mdf] niveaux de la Météo des forêts")
    table = meteo_des_forets.nettoyer_mdf(meteo_des_forets.lire_mdf())  # M1 : lecture selon l'année
    rapport = executer(table, meteo_des_forets.regles_mdf())
    afficher(rapport)
    alertes = barriere(rapport)

    gardes = table[~table["remplace"]].drop(columns="remplace")
    ecrire_csv(gardes, "meteo_des_forets.csv")
    ecrire_csv(rapport, "rapport_qualite_mdf.csv")
    print(f"  meteo_des_forets.csv : {len(gardes)} jours × départements, "
          f"du {gardes['date'].min()} au {gardes['date'].max()}, {gardes['departement'].nunique()} départements")
    print(f"  barrière passée, alertes : {', '.join(alertes) or 'aucune'}")
    return gardes


def nettoyer_interventions_sis():
    print("[sis] interventions des SIS")
    table = interventions_sis.nettoyer_sis(interventions_sis.lire_sis())
    rapport = executer(table, interventions_sis.regles_sis())
    afficher(rapport)
    alertes = barriere(rapport)

    ecrire_csv(table.drop(columns="illisible"), "interventions_sis.csv")
    ecrire_csv(rapport, "rapport_qualite_sis.csv")
    print(f"  interventions_sis.csv : {len(table)} lignes, {table['annee'].min()}-{table['annee'].max()}")
    print(f"  barrière passée, alertes : {', '.join(alertes) or 'aucune'}")


def nettoyer_calendrier():
    print("[calendrier] week-ends, jours fériés, vacances scolaires")
    table = calendrier.table_calendrier(calendrier.lire_feries(), calendrier.lire_scolaire())
    rapport = executer(table, calendrier.regles_calendrier())
    afficher(rapport)
    alertes = barriere(rapport)

    ecrire_csv(table, "calendrier.csv")
    ecrire_csv(rapport, "rapport_qualite_calendrier.csv")
    print(f"  calendrier.csv : {len(table)} jours × départements, du {table['date'].min()} au {table['date'].max()}")
    print(f"  barrière passée, alertes : {', '.join(alertes) or 'aucune'}")
    return table


def nettoyer_firms():
    """FIRMS est optionnel : il faut une clé personnelle pour le télécharger, et il ne sert qu'en indicateur 2026 (N5).

    Sans fichiers, on prévient et on continue : les colonnes satellite des tables de travail restent vides (pas 0).
    Renvoie la table commune × jour et le dernier jour téléchargé, ou (None, None).
    """
    print("[firms] détections satellite 2026")
    try:
        brut = firms.lire_firms()
    except SourceManquante as erreur:
        print(f"  ALERTE : {erreur}. Étape sautée, les colonnes satellite resteront vides (FIRMS demande une clé, voir .env.example)")
        return None, None
    points = firms.nettoyer_firms(brut, firms.lire_contours())
    table = firms.par_commune_jour(points)
    rapport = pd.concat([executer(points, firms.regles_points()), executer(table, firms.regles_commune_jour())])
    afficher(rapport)
    alertes = barriere(rapport)

    ecrire_csv(table, "firms_commune_jour.csv")
    ecrire_csv(rapport, "rapport_qualite_firms.csv")
    print(f"  firms_commune_jour.csv : {len(table)} communes × jours, {int(points['garde'].sum())} détections gardées "
          f"sur {len(points)} ({int(points['hors_grand_est'].sum())} hors Grand Est, {int(points['source_fixe'].sum())} sources fixes)")
    jusqu_au = firms.lire_couverture()
    print(f"  téléchargé jusqu'au : {jusqu_au or 'inconnu (relancer la récupération firms)'}")
    print(f"  barrière passée, alertes : {', '.join(alertes) or 'aucune'}")
    return table, jusqu_au


def nettoyer_bd_foret():
    print("[bdforet] surface de forêt et part de résineux par commune (1 à 2 minutes)")
    foret = bd_foret.preparer(bd_foret.lire_bd_foret())  # répare les géométries invalides (D1)
    contours = firms.lire_contours()
    table = bd_foret.foret_par_commune(foret, contours)
    rapport = pd.concat([executer(foret, bd_foret.regles_polygones()), executer(table, bd_foret.regles_communes(len(contours)))])
    afficher(rapport)
    alertes = barriere(rapport)

    ecrire_csv(table, "foret_commune.csv")
    ecrire_csv(rapport, "rapport_qualite_bd_foret.csv")
    print(f"  foret_commune.csv : {len(table)} communes, {table['surface_foret_ha'].sum():.0f} ha de forêt")
    print(f"  barrière passée, alertes : {', '.join(alertes) or 'aucune'}")
    return table


def construire_tables(feux, population, mdf, cal, firms_jour, firms_jusqu_au):
    print("[tables] tables de travail")
    travail = tables.feux_travail(feux, cal)
    jours = tables.jour_departement(cal, feux, population, mdf, firms_jour, firms_jusqu_au)
    rapport = pd.concat([
        executer(travail, tables.regles_feux_travail(int((~feux["doublon_probable"]).sum()))),
        executer(jours, tables.regles_jour_departement(feux, len(cal))),
    ])
    afficher(rapport)
    alertes = barriere(rapport)

    ecrire_csv(travail, "feux_travail.csv")
    ecrire_csv(jours, "jour_departement.csv")
    ecrire_csv(rapport, "rapport_qualite_tables.csv")
    print(f"  feux_travail.csv : {len(travail)} feux ; jour_departement.csv : {len(jours)} jours × départements")
    print(f"  barrière passée, alertes : {', '.join(alertes) or 'aucune'}")


def main():
    try:
        passage = nettoyer_cog()
        feux, population = nettoyer_bdiff(passage)
        mdf = nettoyer_meteo_des_forets()
        nettoyer_interventions_sis()
        cal = nettoyer_calendrier()
        firms_jour, firms_jusqu_au = nettoyer_firms()
        construire_tables(feux, population, mdf, cal, firms_jour, firms_jusqu_au)
        nettoyer_bd_foret()
    except (QualiteBloquante, SourceManquante, ValueError) as erreur:
        print(f"ARRET : {erreur}")
        sys.exit(1)


if __name__ == "__main__":
    main()
