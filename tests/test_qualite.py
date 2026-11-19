"""Tests des règles de qualité sur de petites tables faites à la main.

    python -m unittest discover -s tests -t .

On vérifie que chaque règle trouve bien le défaut qu'elle doit trouver, et que la
barrière arrete le chargement seulement sur une règle bloquante.
"""

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.qualite.__main__ import trouver_csv
from src.qualite.bdiff import (
    COLONNES_ATTENDUES, DEPARTEMENTS_GRAND_EST, NB_COLONNES,
    controle_annee_date, controle_cle_unique, controle_population, lire_bdiff, lire_criteres, regles_bdiff,
)
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


# Les 2 lignes de critères qu'on a vues pour de vrai
CRITERES_A_LA_MAIN = ('"Critères de sélection =>";"Date de première alerte, de : 2006-01-01 00:00:00";'
                      '"Date de première alerte, jusqu\'à : 2025-12-31 23:59:00";"Région administrative : GRAND-EST";"Type de feu : F"')
CRITERES_SCRIPT = ('"Critères de sélection =>";"Date de première alerte, jusqu\'à : 2025-12-31 23:59:00";'
                   '"Période de répétition de la sélection : 2006,2025";"Département(s) : 08, 10, 51, 52, 54, 55, 57, 67, 68, 88";"Type de feu : F"')
CRITERES_SCRIPT_67 = CRITERES_SCRIPT.replace("08, 10, 51, 52, 54, 55, 57, 67, 68, 88", "67")


class TestCriteres(unittest.TestCase):
    def test_export_a_la_main(self):
        periode, deps = lire_criteres(CRITERES_A_LA_MAIN)
        self.assertEqual((periode[0], periode[-1], deps), (2006, 2025, DEPARTEMENTS_GRAND_EST))

    def test_export_du_script(self):
        periode, deps = lire_criteres(CRITERES_SCRIPT)
        self.assertEqual((periode[0], periode[-1], deps), (2006, 2025, DEPARTEMENTS_GRAND_EST))

    def test_export_du_script_un_departement(self):
        self.assertEqual(lire_criteres(CRITERES_SCRIPT_67)[1], ["67"])

    def test_criteres_illisibles(self):
        with self.assertRaises(ValueError):
            lire_criteres('"Critères de sélection =>";"Type de feu : F"')


class TestLecture(unittest.TestCase):
    def ecrire_export(self, dossier, nom, criteres):
        colonnes = COLONNES_ATTENDUES + [f"autre {i}" for i in range(NB_COLONNES - len(COLONNES_ATTENDUES))]
        ligne = ["2024", "1", "67", "67482", "Strasbourg", "2024-07-01 14:00:00", "100", "0", ""] + [""] * (NB_COLONNES - 9)
        chemin = Path(dossier) / nom
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text("\n".join(['"texte"', '"Nombre : 1"', criteres, ";".join(colonnes), ";".join(ligne)]) + "\n", encoding="utf-8")
        return chemin

    def test_les_2_formats_donnent_la_meme_chose(self):
        with tempfile.TemporaryDirectory() as dossier:
            a = lire_bdiff(self.ecrire_export(dossier, "main.csv", CRITERES_A_LA_MAIN))
            b = lire_bdiff(self.ecrire_export(dossier, "script.csv", CRITERES_SCRIPT))
            self.assertEqual((a[1], a[2]), (b[1], b[2]))

    def test_plusieurs_exports_on_s_arrete(self):
        with tempfile.TemporaryDirectory() as dossier:
            self.ecrire_export(dossier, "bdiff_67_2006_2025/Incendies.csv", CRITERES_SCRIPT_67)
            self.ecrire_export(dossier, "bdiff_grand_est_2006_2025/Incendies.csv", CRITERES_SCRIPT)
            with self.assertRaises(SystemExit):
                trouver_csv(dossier)

    def test_un_seul_export(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = self.ecrire_export(dossier, "Incendies.csv", CRITERES_SCRIPT)
            self.assertEqual(trouver_csv(dossier), chemin)


if __name__ == "__main__":
    unittest.main()
