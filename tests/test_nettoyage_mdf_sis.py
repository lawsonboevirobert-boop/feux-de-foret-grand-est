"""Tests du nettoyage de la Météo des forêts et des interventions des SIS, sur de petites tables.

    python -m unittest discover -s tests -t .
"""

import gzip
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.nettoyage.interventions_sis import nettoyer_sis, nombre, regles_sis
from src.nettoyage.meteo_des_forets import jours_manquants, lire_mdf, nettoyer_mdf, regles_mdf
from src.qualite.regles import QualiteBloquante, barriere, executer


def bulletins(lignes):
    return pd.DataFrame(lignes, columns=["date", "num_dep", "niveau_j1"], dtype=str)


class TestLectureMdf(unittest.TestCase):
    def test_deux_formats_de_fichier(self):
        # M1 : virgule et `dep_nom` en 2025, point-virgule et `nom_dep` en 2026
        with tempfile.TemporaryDirectory() as dossier:
            dossier = Path(dossier)
            with gzip.open(dossier / "mdf_2025.csv.gz", "wt", encoding="utf-8") as f:
                f.write("date,num_dep,niveau_j1,niveau_j2,dep_nom\n2025-06-03T14:50:06Z,8,2,1,Ardennes\n")
            with gzip.open(dossier / "mdf_2026.csv.gz", "wt", encoding="utf-8") as f:
                f.write("date;num_dep;niveau_j1;niveau_j2;nom_dep\n2026-05-28T14:50:07Z;08;1;1;Ardennes\n")
            brut = lire_mdf(dossier)
        self.assertEqual(len(brut), 2)
        self.assertEqual(sorted(nettoyer_mdf(brut)["departement"].unique()), ["08"])  # M2


class TestNettoyerMdf(unittest.TestCase):
    def test_niveau_vaut_pour_le_lendemain_en_heure_de_paris(self):
        table = nettoyer_mdf(bulletins([
            ["2025-06-03T14:50:06Z", "67", "2"],  # 16 h 50 à Paris le 03/06 -> vaut pour le 04/06
            ["2024-06-04T22:30:00Z", "67", "1"],  # 00 h 30 à Paris le 05/06 -> vaut pour le 06/06
        ])).set_index("niveau")
        self.assertEqual(table.loc["2", "date"], "2025-06-04")
        self.assertEqual(table.loc["1", "date"], "2024-06-06")

    def test_dernier_bulletin_garde(self):
        table = nettoyer_mdf(bulletins([
            ["2025-06-03T14:50:00Z", "67", "1"],
            ["2025-06-03T15:30:00Z", "67", "2"],  # rectificatif publié plus tard
        ]))
        self.assertEqual(table[~table["remplace"]]["niveau"].tolist(), ["2"])
        self.assertEqual(barriere(executer(table, regles_mdf())), ["M4"])

    def test_jour_manquant_compte(self):
        table = nettoyer_mdf(bulletins([
            ["2025-06-01T14:50:00Z", "67", "1"], ["2025-06-01T14:50:00Z", "68", "1"],
            ["2025-06-02T14:50:00Z", "67", "1"],  # le 68 manque le 03/06
            ["2025-06-03T14:50:00Z", "67", "1"], ["2025-06-03T14:50:00Z", "68", "1"],
        ]))
        self.assertEqual(jours_manquants(table), 1)

    def test_niveau_hors_echelle_on_arrete(self):
        table = nettoyer_mdf(bulletins([["2025-06-03T14:50:00Z", "67", "5"]]))
        with self.assertRaises(QualiteBloquante):
            barriere(executer(table, regles_mdf()))


def fichier_sis(lignes, avec_vegetation=True):
    colonnes = ["Année", "Numéro", "Incendies", "Total interventions"]
    if avec_vegetation:
        colonnes.insert(2, "Feux de végétations")
    return pd.DataFrame(lignes, columns=colonnes, dtype=str)


class TestInterventionsSis(unittest.TestCase):
    def test_nombres(self):
        valeurs = pd.Series(["1 265", "1?265", "214", "N.C.", ""])
        self.assertEqual(nombre(valeurs).tolist(), [1265, 1265, 214, pd.NA, pd.NA])

    def test_annee_sans_detail_reste_vide(self):
        table = nettoyer_sis([
            fichier_sis([["2012", "67", "5565", "69755"]], avec_vegetation=False),
            fichier_sis([["2024", "67", "214", "3?595", "59?450"]]),
        ]).set_index("annee")
        self.assertTrue(pd.isna(table.loc[2012, "feux_vegetation"]))  # pas 0
        self.assertEqual(table.loc[2024, "feux_vegetation"], 214)
        self.assertEqual(table.loc[2024, "total_interventions"], 59450)

    def test_codes_des_services(self):
        table = nettoyer_sis([fichier_sis([
            ["2024", "2a", "10", "1", "2"], ["2024", "BSPP", "10", "1", "2"],
        ])]).set_index("code_sis")
        self.assertEqual(table.loc["2A", "departement"], "2A")
        self.assertEqual(table.loc["BSPP", "departement"], "")  # pas un département

    def test_table_propre_on_passe(self):
        table = nettoyer_sis([fichier_sis([["2024", "67", "214", "3?595", "59?450"]])])
        self.assertEqual(barriere(executer(table, regles_sis())), [])

    def test_nombre_illisible_on_arrete(self):
        table = nettoyer_sis([fichier_sis([["2024", "67", "deux cents", "3595", "59450"]])])
        with self.assertRaises(QualiteBloquante):
            barriere(executer(table, regles_sis()))


if __name__ == "__main__":
    unittest.main()
