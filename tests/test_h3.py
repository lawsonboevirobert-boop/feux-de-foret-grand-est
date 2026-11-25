"""Tests du test de H3 (#98), sur de petites tables faites à la main.

    python -m unittest discover -s tests -t .
"""

import math
import unittest

import pandas as pd

from src.h3 import regle


def foret(lignes):
    """lignes : (commune, département, forêt, conifères, feuillus, mixte)."""
    return pd.DataFrame(lignes, columns=["code_commune_2026", "departement", "surface_foret_ha",
                                         "surface_coniferes_ha", "surface_feuillus_ha", "surface_mixte_ha"])


MAILLE = pd.DataFrame({
    "code_commune_2026": ["67001", "67002", "57001"],
    "departement": ["67", "67", "57"],
    "latitude": [48.5, 48.5, 48.5],
    "longitude": [7.5, 7.5, 7.5],
})


class Secteurs(unittest.TestCase):
    def test_un_secteur_par_departement_et_par_maille(self):
        s = regle.secteurs(MAILLE, foret([
            ("67001", "67", 100, 20, 60, 20),
            ("67002", "67", 100, 40, 40, 20),
            ("57001", "57", 50, 0, 50, 0),
        ]))
        self.assertEqual(len(s), 2)  # même maille, deux départements
        s67 = s[s["departement"] == "67"].iloc[0]
        self.assertEqual(s67["surface_foret_ha"], 200)
        # (60 conifères + 0,5 × 40 mixte) ÷ 200 de forêt avec couvert (journal du 20/11)
        self.assertAlmostEqual(s67["part_resineux"], 0.4)
        self.assertAlmostEqual(s67["part_resineux_stricte"], 0.3)
        self.assertEqual(s[s["departement"] == "57"].iloc[0]["part_resineux"], 0.0)

    def test_secteur_sans_foret_avec_couvert(self):
        s = regle.secteurs(MAILLE.iloc[[2]], foret([("57001", "57", 0, 0, 0, 0)]))
        self.assertEqual(s.iloc[0]["part_resineux"], 0.0)


class Historique(unittest.TestCase):
    def setUp(self):
        self.secteurs = pd.DataFrame({"departement": ["67", "57"], "latitude": [48.5, 48.5],
                                      "longitude": [7.5, 7.5], "surface_foret_ha": [200.0, 100.0]})
        self.feux = pd.DataFrame({"departement": ["67", "67", "67", "57"], "latitude": 48.5, "longitude": 7.5,
                                  "annee": [2020, 2020, 2022, 2023]})

    def test_seulement_les_annees_renseignees_avant_la_saison(self):
        # 67 renseigné en 2020 et 2022 : 3 feux sur 2 ans. 2021 non renseigné ne compte pas pour 0 (P1)
        h = regle.historique(self.secteurs, self.feux, {("67", 2020), ("67", 2022), ("57", 2023)}, 2023)
        self.assertAlmostEqual(h.set_index("departement").loc["67", "historique"], 1.5)

    def test_departement_jamais_renseigne_avant_prend_le_taux_regional_par_hectare(self):
        # 57 n'a aucune année renseignée avant 2023 : 1,5 feu par an pour 200 ha dans le 67, donc 0,75 pour 100 ha
        h = regle.historique(self.secteurs, self.feux, {("67", 2020), ("67", 2022), ("57", 2023)}, 2023)
        self.assertAlmostEqual(h.set_index("departement").loc["57", "historique"], 0.75)

    def test_la_saison_elle_meme_ne_compte_pas(self):
        h = regle.historique(self.secteurs, self.feux, {("67", 2020), ("67", 2022)}, 2022)
        self.assertAlmostEqual(h.set_index("departement").loc["67", "historique"], 2.0)


class SeuilEtEvaluation(unittest.TestCase):
    def test_seuil_donne_le_budget_de_jours_par_saison(self):
        jours = pd.date_range("2018-01-01", "2019-12-31")
        score = pd.Series(range(len(jours)), index=jours, dtype=float)
        seuil = regle.seuil_cale(score, [2018, 2019])
        renfort = regle.jours_de_renfort(score, seuil, [2018, 2019])
        # strictement au-dessus de la 40e valeur : 39 jours, tous en mars-octobre
        self.assertEqual(len(renfort), 2 * regle.JOURS_PAR_SAISON - 1)
        self.assertTrue(renfort.month.isin(regle.MOIS_SAISON).all())

    def test_hors_saison_jamais_de_renfort(self):
        jours = pd.date_range("2018-01-01", "2018-12-31")
        score = pd.Series(1.0, index=jours)
        score[jours.month == 12] = 100.0
        renfort = regle.jours_de_renfort(score, 50.0, [2018])
        self.assertEqual(len(renfort), 0)

    def test_evaluer(self):
        feux = pd.DataFrame({"date": pd.to_datetime(["2023-07-01", "2023-07-01", "2023-07-02", "2023-12-01"]),
                             "surface_parcourue_ha": [2.0, 0.5, 1.0, 3.0]})
        r = regle.evaluer(pd.to_datetime(["2023-07-01", "2023-07-03"]), feux)
        self.assertEqual((r["couverts"], r["departs"], r["jours"], r["jours_avec_feu"]), (2, 4, 2, 1))
        self.assertAlmostEqual(r["precision"], 0.5)
        self.assertAlmostEqual(r["surface_couverte_ha"], 2.5)
        self.assertEqual((r["feux_1ha_couverts"], r["feux_1ha"]), (1, 3))


class Base(unittest.TestCase):
    def test_fwi_grand_est_pondere_par_la_foret_des_departements(self):
        jd = pd.DataFrame({"date": pd.to_datetime(["2023-07-01"] * 2), "departement": ["67", "88"],
                           "fwi_moyen": [10.0, 40.0]})
        f = foret([("67001", "67", 300, 0, 0, 0), ("88001", "88", 100, 0, 0, 0)])
        self.assertAlmostEqual(regle.fwi_grand_est(jd, f).iloc[0], 17.5)


class Modele(unittest.TestCase):
    def test_score_somme_les_secteurs_et_reste_vide_si_une_variable_manque(self):
        modele = {"variables": ["x"], "constante": 0.0, "coefficients": {"x": math.log(2)}}
        t = pd.DataFrame({"date": pd.to_datetime(["2023-07-01", "2023-07-01", "2023-07-02", "2023-07-02"]),
                          "x": [1.0, 0.0, 1.0, float("nan")]})
        s = regle.score_par_jour(t, modele)
        self.assertAlmostEqual(s.loc["2023-07-01"], 3.0)  # 2 + 1 départs attendus
        self.assertTrue(math.isnan(s.loc["2023-07-02"]))

    def test_caler_ne_prend_que_les_lignes_renseignees(self):
        t = pd.DataFrame({"x": [0.0, 1.0, 0.0, 1.0, 1.0], "nb_departs": [1, 2, 1, 2, 50],
                          "renseigne": [True, True, True, True, False]})
        m = regle.caler_modele(t, ["x"])
        self.assertEqual(m["lignes"], 4)
        self.assertAlmostEqual(math.exp(m["coefficients"]["x"]), 2.0, places=3)


if __name__ == "__main__":
    unittest.main()
