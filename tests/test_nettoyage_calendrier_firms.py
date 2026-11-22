"""Tests du calendrier et de FIRMS, sur de petites tables faites à la main.

    python -m unittest discover -s tests -t .
"""

import tempfile
import unittest
from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import box

from src.nettoyage.calendrier import regles_calendrier, table_calendrier
from src.nettoyage.firms import (
    lire_couverture,
    marquer_sources_fixes,
    nettoyer_firms,
    par_commune_jour,
    preparer,
    regles_commune_jour,
    regles_points,
    versions_melangees,
)
from src.qualite.regles import QualiteBloquante, barriere, executer

FERIES = {
    "alsace-moselle": {"2024-12-25": "Noël", "2024-12-26": "2ème jour de Noël"},
    "metropole": {"2024-12-25": "Noël"},
}


def scolaire(lignes):
    colonnes = ["description", "population", "start_date", "end_date", "location", "zones", "annee_scolaire"]
    return pd.DataFrame(lignes, columns=colonnes, dtype=str)


# Toussaint 2024, zone B : du samedi 19/10 (inclus) au lundi 4/11 (reprise, exclu), écrit en UTC
SCOLAIRE = scolaire([
    ["Vacances de la Toussaint", "-", "2024-10-18T22:00:00+00:00", "2024-11-03T23:00:00+00:00", loc, "Zone B", "2024-2025"]
    for loc in ("Strasbourg", "Nancy-Metz", "Reims")
] + [
    ["Vacances d'Été", "Enseignants", "2025-07-04T22:00:00+00:00", "2025-08-28T22:00:00+00:00", "Strasbourg", "Zone B", "2024-2025"],
])


class TestCalendrier(unittest.TestCase):
    def setUp(self):
        self.table = table_calendrier(FERIES, SCOLAIRE, "2024-08-30", "2024-12-31").set_index(["date", "departement"])

    def test_vacances_en_heure_de_paris(self):
        self.assertEqual(self.table.loc[("2024-10-18", "67"), "vacances"], "non")  # vendredi : encore en classe
        self.assertEqual(self.table.loc[("2024-10-19", "67"), "vacances"], "oui")
        self.assertEqual(self.table.loc[("2024-11-03", "67"), "vacances"], "oui")
        self.assertEqual(self.table.loc[("2024-11-04", "67"), "vacances"], "non")  # jour de la reprise

    def test_avant_les_donnees_non_renseigne(self):
        self.assertEqual(self.table.loc[("2024-08-30", "67"), "vacances"], "non renseigné")

    def test_feries_alsace_moselle(self):
        self.assertTrue(self.table.loc[("2024-12-26", "67"), "ferie"])
        self.assertFalse(self.table.loc[("2024-12-26", "54"), "ferie"])
        self.assertTrue(self.table.loc[("2024-12-25", "54"), "ferie"])

    def test_week_end(self):
        self.assertTrue(self.table.loc[("2024-10-19", "08"), "week_end"])  # samedi
        self.assertEqual(self.table.loc[("2024-10-21", "08"), "jour_semaine"], "lundi")

    def test_barriere_passe(self):
        self.assertEqual(barriere(executer(self.table.reset_index(), regles_calendrier())), [])

    def test_mauvais_feries_on_arrete(self):
        mauvais = {"alsace-moselle": FERIES["metropole"], "metropole": FERIES["metropole"]}
        table = table_calendrier(mauvais, SCOLAIRE, "2024-12-20", "2024-12-31")
        with self.assertRaises(QualiteBloquante):
            barriere(executer(table, regles_calendrier()))


CONTOURS = gpd.GeoDataFrame(
    {"code": ["67180", "67482"], "codeDepartement": ["67", "67"]},
    geometry=[box(7.6, 48.7, 8.0, 49.0), box(7.6, 48.5, 8.0, 48.7)],
    crs="EPSG:4326",
)


def detections(lignes):
    colonnes = ["latitude", "longitude", "acq_date", "acq_time", "satellite", "instrument", "confidence",
                "frp", "traitement", "fichier", "type", "brightness", "bright_ti4"]
    return pd.DataFrame(lignes, columns=colonnes, dtype=str)


# Haguenau le 12/08/2026 : 3 satellites dans la nuit, plus un point en Allemagne
BRUT = detections([
    ["48.85", "7.80", "2026-08-12", "132", "N20", "VIIRS", "n", "0.55", "NRT", "firms_viirs_noaa20_2026", "", "", "300.1"],
    ["48.86", "7.81", "2026-08-12", "215", "N21", "VIIRS", "n", "1.9", "NRT", "firms_viirs_noaa21_2026", "", "", "310.2"],
    ["48.85", "7.79", "2026-08-12", "251", "N", "VIIRS", "n", "0.76", "NRT", "firms_viirs_snpp_2026", "", "", "305.0"],
    ["48.60", "7.70", "2026-07-28", "2230", "T", "MODIS", "76", "18.1", "SP", "firms_modis_2026", "0", "320.5", ""],
    ["49.50", "9.50", "2026-08-12", "132", "N20", "VIIRS", "n", "3.0", "NRT", "firms_viirs_noaa20_2026", "", "", "300.0"],
])


class TestCouverture(unittest.TestCase):
    def test_dernier_jour_telecharge(self):
        with tempfile.TemporaryDirectory() as dossier:
            dossier = Path(dossier)
            self.assertIsNone(lire_couverture(dossier))  # pas de fichier : inconnu
            pd.DataFrame({"satellite": ["MODIS"], "traitement": ["NRT"], "du": ["2026-09-01"], "au": ["2026-11-20"]}).to_csv(
                dossier / "couverture_firms_modis_2026.csv", index=False)
            pd.DataFrame({"satellite": ["VIIRS_SNPP"], "traitement": ["NRT"], "du": ["2026-08-01"], "au": ["2026-11-02"]}).to_csv(
                dossier / "couverture_firms_viirs_snpp_2026.csv", index=False)
            self.assertEqual(lire_couverture(dossier), "2026-11-20")


class TestFirms(unittest.TestCase):
    def setUp(self):
        self.points = nettoyer_firms(BRUT, CONTOURS)

    def test_heure_utc_vers_paris(self):
        # 22 h 30 UTC le 28/07 = 0 h 30 à Paris le 29/07
        self.assertEqual(preparer(BRUT).loc[3, "date"], "2026-07-29")

    def test_colonnes_modis_et_viirs_harmonisees(self):
        self.assertEqual(preparer(BRUT)["brillance"].isna().sum(), 0)

    def test_point_hors_grand_est_enleve(self):
        self.assertEqual(self.points["hors_grand_est"].tolist(), [False, False, False, False, True])

    def test_un_feu_une_ligne(self):
        table = par_commune_jour(self.points).set_index(["code_commune_2026", "date"])
        self.assertEqual(table.loc[("67180", "2026-08-12"), "nb_detections"], 3)
        self.assertEqual(table.loc[("67180", "2026-08-12"), "nb_satellites"], 3)
        self.assertEqual(len(table), 2)
        self.assertEqual(barriere(executer(table.reset_index(), regles_commune_jour())), [])

    def test_source_fixe(self):
        # la même case vue 3 jours différents, avec un seuil à 3 jours : usine
        usine = pd.DataFrame({"latitude": [48.851] * 3, "longitude": [7.801] * 3, "type": [""] * 3,
                              "date": ["2026-01-01", "2026-02-01", "2026-03-01"]})
        self.assertTrue(marquer_sources_fixes(usine, jours=3)["source_fixe"].all())
        self.assertFalse(marquer_sources_fixes(usine, jours=4)["source_fixe"].any())

    def test_sp_et_nrt_le_meme_jour_on_arrete(self):
        double = pd.concat([BRUT.iloc[[0]], BRUT.iloc[[0]].assign(traitement="SP")], ignore_index=True)
        points = nettoyer_firms(double, CONTOURS)
        self.assertEqual(versions_melangees(points), 1)
        with self.assertRaises(QualiteBloquante):
            barriere(executer(points, regles_points()))


if __name__ == "__main__":
    unittest.main()
