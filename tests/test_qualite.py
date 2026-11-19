"""Tests des règles de qualité sur de petites tables faites à la main.

    python -m unittest discover -s tests -t .

On vérifie que chaque règle trouve bien le défaut qu'elle doit trouver, et que la
barrière arrete le chargement seulement sur une règle bloquante.
"""

import unittest

import pandas as pd

from src.qualite.bdiff import controle_annee_date, controle_cle_unique, controle_population, regles_bdiff
from src.qualite.profil import profil, remplissage_par_groupe
from src.qualite.regles import QualiteBloquante, barriere, executer


def feux(lignes):
    colonnes = ["Année", "Numéro", "Département", "Date de première alerte", "Nature"]
    return pd.DataFrame(lignes, columns=colonnes)


PROPRE = feux([
    ["2024", "1", "67", "2024-07-01 14:00:00", "Malveillance"],
    ["2024", "2", "68", "2024-08-02 15:30:00", None],
    ["2025", "1", "67", "2025-07-10 12:00:00", ""],
    ["2025", "2", "68", "2025-06-20 16:45:00", None],
])


class TestB2CleUnique(unittest.TestCase):
    def test_table_propre(self):
        self.assertEqual(controle_cle_unique(PROPRE).fautifs, 0)

    def test_doublon_trouve(self):
        df = pd.concat([PROPRE, PROPRE.iloc[[0]]])
        self.assertEqual(controle_cle_unique(df).fautifs, 2)  # les 2 lignes en double


class TestB4AnneeDate(unittest.TestCase):
    def test_table_propre(self):
        self.assertEqual(controle_annee_date(PROPRE).fautifs, 0)

    def test_annee_differente_et_date_illisible(self):
        df = PROPRE.copy()
        df.loc[0, "Année"] = "2023"
        df.loc[1, "Date de première alerte"] = "pas une date"
        self.assertEqual(controle_annee_date(df).fautifs, 2)


class TestP1Population(unittest.TestCase):
    def test_rien_ne_manque(self):
        resultat = controle_population(["67", "68"], [2024, 2025])(PROPRE)
        self.assertEqual((resultat.fautifs, resultat.controles), (0, 4))

    def test_departement_annee_absents(self):
        resultat = controle_population(["67", "68", "57"], [2023, 2024, 2025])(PROPRE)
        # 57 n'a rien sur 3 ans, 67 et 68 rien en 2023
        self.assertEqual(resultat.fautifs, 5)
        self.assertIn("57 : 2023-2025", resultat.detail)


class TestBarriere(unittest.TestCase):
    def test_alerte_seule_on_passe(self):
        rapport = executer(PROPRE, regles_bdiff([2023, 2024, 2025], ["67", "68"]))
        self.assertEqual(barriere(rapport), ["P1"])

    def test_bloquant_on_arrete(self):
        df = pd.concat([PROPRE, PROPRE.iloc[[0]]])
        rapport = executer(df, regles_bdiff([2024, 2025], ["67", "68"]))
        with self.assertRaises(QualiteBloquante):
            barriere(rapport)


class TestProfil(unittest.TestCase):
    def test_vide_et_chaine_vide_comptent_comme_manquants(self):
        ligne = profil(PROPRE).set_index("colonne").loc["Nature"]
        self.assertEqual(ligne["remplies"], 1)

    def test_code_garde_son_zero(self):
        df = pd.DataFrame({"Département": ["08", "67"]})
        ligne = profil(df).iloc[0]
        self.assertEqual((ligne["type"], ligne["min"]), ("code", "08"))

    def test_remplissage_par_segment(self):
        par_dep = remplissage_par_groupe(PROPRE, "Nature", "Département").set_index("Département")
        self.assertEqual(par_dep.loc["67", "remplissage"], 50.0)
        self.assertEqual(par_dep.loc["68", "remplissage"], 0.0)


if __name__ == "__main__":
    unittest.main()
