"""Tests du nettoyage du COG sur de petites tables faites à la main.

    python -m unittest discover -s tests -t .
"""

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.nettoyage.commun import SourceManquante
from src.nettoyage.cog import (
    controle_ambigus,
    controle_format,
    controle_unicite,
    lire_cog,
    regles_communes,
    regles_passage,
    table_communes,
    table_passage,
)
from src.qualite.regles import QualiteBloquante, barriere, executer

COLONNES_COMMUNES = ["TYPECOM", "COM", "DEP", "REG", "COMPARENT"]
COLONNES_MOUVEMENTS = ["MOD", "DATE_EFF", "COM_AV", "COM_AP"]


def communes(lignes):
    return pd.DataFrame(lignes, columns=COLONNES_COMMUNES)


def mouvements(lignes):
    return pd.DataFrame(lignes, columns=COLONNES_MOUVEMENTS)


# 67372 est une commune nouvelle, 67402 une ancienne commune fusionnée dedans,
# 67100 une commune déléguée de 67372, 08001 une commune simple
COMMUNES = communes([
    ["COM", "67372", "67", "44", ""],
    ["COM", "08001", "08", "44", ""],
    ["COMD", "67100", "67", "44", "67372"],
    ["COMD", "67372", "67", "44", "67372"],  # la déléguée qui garde le code de la commune nouvelle
])
MOUVEMENTS = mouvements([
    ["32", "2016-01-01", "67402", "67372"],
])


class TestTableCommunes(unittest.TestCase):
    def test_garde_seulement_les_communes(self):
        table = table_communes(COMMUNES)
        self.assertEqual(table["code_commune"].tolist(), ["08001", "67372"])

    def test_pas_de_doublon(self):
        self.assertEqual(controle_unicite(table_communes(COMMUNES), "code_commune"), 0)

    def test_garde_le_zero_du_departement(self):
        table = table_communes(COMMUNES)
        self.assertIn("08", table["departement"].tolist())


class TestPassage(unittest.TestCase):
    def passage(self, mvts=MOUVEMENTS, depuis="2006-01-01"):
        return table_passage(COMMUNES, mvts, depuis).set_index("code_origine")["code_commune_2026"].to_dict()

    def test_commune_actuelle_donne_son_code(self):
        self.assertEqual(self.passage()["08001"], "08001")

    def test_deleguee_donne_sa_commune(self):
        self.assertEqual(self.passage()["67100"], "67372")

    def test_ancien_code_fusionne(self):
        self.assertEqual(self.passage()["67402"], "67372")

    def test_chaine_de_fusions(self):
        # 67500 devient 67402 en 2010, qui devient 67372 en 2016
        mvts = pd.concat([MOUVEMENTS, mouvements([["32", "2010-01-01", "67500", "67402"]])])
        self.assertEqual(self.passage(mvts)["67500"], "67372")

    def test_mouvement_trop_ancien_ignore(self):
        mvts = mouvements([["32", "1971-01-01", "67999", "67372"]])
        self.assertNotIn("67999", self.passage(mvts))

    def test_ligne_sans_code_ignoree(self):
        # sortie du COG (code après vide) et création (code avant vide) : pas de lien entre les deux
        mvts = mouvements([["30", "2007-02-23", "97123", ""], ["20", "2011-03-31", "", "08001"]])
        passage = self.passage(mvts)
        self.assertNotIn("97123", passage)
        self.assertNotIn("", passage)

    def test_commune_scindee_marquee_ambigue(self):
        mvts = mouvements([["21", "2015-01-01", "67777", "67372"], ["21", "2015-01-01", "67777", "08001"]])
        table = table_passage(COMMUNES, mvts)
        ligne = table[table["code_origine"] == "67777"].iloc[0]
        self.assertEqual(ligne["code_commune_2026"], "")
        self.assertTrue(ligne["statut"].startswith("ambigu"))
        self.assertEqual(controle_ambigus(table), 1)


class TestBarriere(unittest.TestCase):
    def test_tables_propres_on_passe(self):
        rapport = pd.concat([
            executer(table_communes(COMMUNES), regles_communes()),
            executer(table_passage(COMMUNES, MOUVEMENTS), regles_passage()),
        ])
        self.assertEqual(barriere(rapport), [])

    def test_code_mal_forme_on_arrete(self):
        table = pd.DataFrame({"code_commune": ["8105"], "departement": ["8"], "region": ["44"]})
        with self.assertRaises(QualiteBloquante):
            barriere(executer(table, regles_communes()))

    def test_code_ambigu_seulement_alerte(self):
        mvts = mouvements([["21", "2015-01-01", "67777", "67372"], ["21", "2015-01-01", "67777", "08001"]])
        rapport = executer(table_passage(COMMUNES, mvts), regles_passage())
        self.assertEqual(barriere(rapport), ["G5"])


class TestSourceManquante(unittest.TestCase):
    def test_cog_absent_message_clair(self):
        with tempfile.TemporaryDirectory() as vide:
            with self.assertRaises(SourceManquante) as erreur:
                lire_cog(Path(vide))
        self.assertIn("python -m src.recuperation cog", str(erreur.exception))


class TestFormat(unittest.TestCase):
    def test_codes_valides(self):
        table = pd.DataFrame({"c": ["67482", "2A004", "97101"], "d": ["67", "2A", "971"]})
        self.assertEqual(controle_format(table, "c", "d"), 0)

    def test_code_sans_zero_trouve(self):
        table = pd.DataFrame({"c": ["8105", "67482"], "d": ["8", "67"]})
        self.assertEqual(controle_format(table, "c", "d"), 1)


if __name__ == "__main__":
    unittest.main()
