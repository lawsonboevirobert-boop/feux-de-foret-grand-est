"""Tests des tables de travail (feux_travail.csv, jour_departement.csv), sur de petites tables.

    python -m unittest discover -s tests -t .
"""

import unittest

import pandas as pd

from src.nettoyage.tables import feux_travail, jour_departement, regles_feux_travail, regles_jour_departement
from src.qualite.regles import QualiteBloquante, barriere, executer


def calendrier(dates, departements=("67",)):
    return pd.DataFrame([
        {"date": d, "departement": dep, "jour_semaine": "lundi", "week_end": False, "ferie": False, "vacances": "non"}
        for d in dates for dep in departements
    ])


CAL = calendrier(["2015-07-01", "2025-08-12", "2025-08-13", "2026-08-12", "2026-08-13", "2026-12-01"])
FEUX = pd.DataFrame({
    "id_feu": ["2025-7287", "2025-11751"],
    "date": ["2025-08-13", "2025-08-13"],
    "departement": ["67", "67"],
    "surface_parcourue_ha": [1.5, 1.5],
    "surface_foret_ha": [1.5, 1.5],
    "doublon_probable": [False, True],
})
POPULATION = pd.DataFrame({
    "departement": ["67", "67"], "annee": [2015, 2025], "statut_bdiff": ["non renseigné", "renseigné"],
})
MDF = pd.DataFrame({"date": ["2025-08-12", "2025-08-13"], "departement": ["67", "67"], "niveau": ["1", "1"]})
FIRMS = pd.DataFrame({
    "code_commune_2026": ["67180", "67282"], "departement": ["67", "67"],
    "date": ["2026-08-12", "2026-08-12"], "nb_detections": [3, 2],
})


class TestJourDepartement(unittest.TestCase):
    def setUp(self):
        self.table = jour_departement(CAL, FEUX, POPULATION, MDF, FIRMS, "2026-11-20").set_index("date")

    def test_doublon_pas_compte(self):
        self.assertEqual(self.table.loc["2025-08-13", "nb_feux"], 1)

    def test_jour_sans_feu_annee_renseignee_vaut_zero(self):
        self.assertEqual(self.table.loc["2025-08-12", "nb_feux"], 0)

    def test_annee_non_renseignee_reste_vide(self):
        self.assertTrue(pd.isna(self.table.loc["2015-07-01", "nb_feux"]))
        self.assertEqual(self.table.loc["2015-07-01", "statut_bdiff"], "non renseigné")

    def test_2026_non_publiee(self):
        self.assertEqual(self.table.loc["2026-08-12", "statut_bdiff"], "non publié")
        self.assertTrue(pd.isna(self.table.loc["2026-08-12", "nb_feux"]))

    def test_niveau_entier_vide_hors_saison_publiee(self):
        self.assertTrue(pd.isna(self.table.loc["2015-07-01", "niveau"]))
        self.assertEqual(self.table.loc["2025-08-13", "niveau"], 1)
        self.assertEqual(str(self.table["niveau"].dtype), "Int64")  # 1 et pas 1.0

    def test_detections_seulement_2026(self):
        self.assertEqual(self.table.loc["2026-08-12", "nb_detections_satellite"], 5)
        self.assertEqual(self.table.loc["2026-08-12", "nb_communes_detection"], 2)
        self.assertEqual(self.table.loc["2026-08-13", "nb_detections_satellite"], 0)  # téléchargé, rien vu
        self.assertTrue(pd.isna(self.table.loc["2025-08-13", "nb_detections_satellite"]))  # pas téléchargé : vide

    def test_apres_le_telechargement_vide(self):
        self.assertTrue(pd.isna(self.table.loc["2026-12-01", "nb_detections_satellite"]))

    def test_sans_firms_tout_vide(self):
        table = jour_departement(CAL, FEUX, POPULATION, MDF, None).set_index("date")
        self.assertTrue(table["nb_detections_satellite"].isna().all())
        self.assertEqual(table.loc["2025-08-13", "nb_feux"], 1)  # le reste de la table est là
        self.assertEqual(barriere(executer(table.reset_index(), regles_jour_departement(FEUX, len(CAL)))), [])

    def test_barriere_passe(self):
        regles = regles_jour_departement(FEUX, len(CAL))
        self.assertEqual(barriere(executer(self.table.reset_index(), regles)), [])

    def test_feu_hors_calendrier_on_arrete(self):
        perdu = pd.concat([FEUX, FEUX.iloc[[0]].assign(id_feu="2025-1", date="2025-12-31")], ignore_index=True)
        table = jour_departement(CAL, perdu, POPULATION, MDF, FIRMS)
        with self.assertRaises(QualiteBloquante):  # T3 : un feu n'a pas trouvé son jour
            barriere(executer(table, regles_jour_departement(perdu, len(CAL))))


class TestFeuxTravail(unittest.TestCase):
    def test_type_de_jour_et_saison(self):
        table = feux_travail(FEUX, CAL)
        self.assertEqual(len(table), 1)  # le doublon est retiré
        self.assertEqual(table.loc[0, "jour_semaine"], "lundi")
        self.assertTrue(table.loc[0, "saison"])
        self.assertEqual(barriere(executer(table, regles_feux_travail(1))), [])


if __name__ == "__main__":
    unittest.main()
