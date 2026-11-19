"""Tests du nettoyage de la BDIFF (feux.csv) sur de petites tables faites à la main.

    python -m unittest discover -s tests -t .
"""

import unittest

import pandas as pd

from src.nettoyage.bdiff import nettoyer_feux, population, regles_feux
from src.qualite.regles import QualiteBloquante, barriere, executer

COLONNES = [
    "Année", "Numéro", "Département", "Code INSEE", "Date de première alerte",
    "Surface parcourue (m2)", "Surface forêt (m2)", "Nature", "Précision de la donnée",
]


def brut(lignes):
    return pd.DataFrame(lignes, columns=COLONNES, dtype=str)


PASSAGE = pd.DataFrame({
    "code_origine": ["67180", "67402", "08105"],
    "code_commune_2026": ["67180", "67372", "08105"],
    "statut": ["commune 2026", "disparu depuis 2006", "commune 2026"],
})

BRUT = brut([
    ["2025", "7287", "67", "67180", "2025-08-13 17:54:00", "15000", "15000", None, None],
    ["2025", "11751", "67", "67180", "2025-08-13 17:54:00", "15000", "15000", None, None],  # doublon probable
    ["2012", "40", "67", "67402", "2012-04-02 00:00:00", "300", "0", "Malveillance", None],   # ancien code, heure inconnue
    ["2024", "5", "08", "08105", "2024-03-10 14:00:00", "1", "", "  ", None],
])


class TestNettoyerFeux(unittest.TestCase):
    def setUp(self):
        self.feux = nettoyer_feux(BRUT, PASSAGE).set_index("id_feu")

    def test_ancien_code_converti(self):
        self.assertEqual(self.feux.loc["2012-40", "code_commune_2026"], "67372")
        self.assertEqual(self.feux.loc["2012-40", "code_commune_origine"], "67402")

    def test_surfaces_en_hectares(self):
        self.assertEqual(self.feux.loc["2025-7287", "surface_parcourue_ha"], 1.5)
        self.assertEqual(self.feux.loc["2024-5", "surface_parcourue_ha"], 0.0001)

    def test_heure_minuit_devient_inconnue(self):
        self.assertEqual(self.feux.loc["2012-40", "heure"], "")
        self.assertEqual(self.feux.loc["2012-40", "date"], "2012-04-02")

    def test_cause_vide_devient_inconnue(self):
        self.assertEqual(self.feux.loc["2025-7287", "cause"], "inconnue")
        self.assertEqual(self.feux.loc["2024-5", "cause"], "inconnue")  # que des espaces
        self.assertEqual(self.feux.loc["2012-40", "cause"], "Malveillance")

    def test_doublon_probable_garde_le_premier(self):
        self.assertFalse(self.feux.loc["2025-7287", "doublon_probable"])
        self.assertTrue(self.feux.loc["2025-11751", "doublon_probable"])

    def test_colonnes_jetees(self):
        self.assertNotIn("Nom de la commune", self.feux.columns)
        self.assertNotIn("Nombre de décès", self.feux.columns)


class TestPopulation(unittest.TestCase):
    def test_annee_sans_feu_non_renseignee(self):
        feux = nettoyer_feux(BRUT, PASSAGE)
        pop = population(feux, [2024, 2025], ["67", "08"]).set_index(["departement", "annee"])
        self.assertEqual(pop.loc[("67", 2025), "nb_feux"], 1)  # le doublon n'est pas compté
        self.assertEqual(pop.loc[("67", 2024), "statut_bdiff"], "non renseigné")
        self.assertEqual(pop.loc[("67", 2024), "nb_feux"], "")  # vide, pas 0


class TestBarriere(unittest.TestCase):
    def test_table_propre_alerte_doublon_seulement(self):
        rapport = executer(nettoyer_feux(BRUT, PASSAGE), regles_feux())
        self.assertEqual(barriere(rapport), ["B3"])

    def test_code_sans_commune_2026_on_arrete(self):
        inconnu = brut([["2024", "9", "67", "67999", "2024-05-01 10:00:00", "100", "100", None, None]])
        rapport = executer(nettoyer_feux(inconnu, PASSAGE), regles_feux())
        with self.assertRaises(QualiteBloquante):
            barriere(rapport)

    def test_surface_negative_on_arrete(self):
        negatif = brut([["2024", "9", "67", "67180", "2024-05-01 10:00:00", "-5", "0", None, None]])
        with self.assertRaises(QualiteBloquante):
            barriere(executer(nettoyer_feux(negatif, PASSAGE), regles_feux()))


if __name__ == "__main__":
    unittest.main()
