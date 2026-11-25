"""Tests des règles de Q4 (#102), sur un FWI fait à la main.

    python -m unittest discover -s tests -t .
"""

import unittest

import pandas as pd

from src.q4 import regles
from src.q4.__main__ import recommander


def fwi_croissant(annees):
    """Un FWI qui monte chaque jour : les jours les plus hauts sont en fin de saison."""
    jours = pd.date_range(f"{min(annees)}-01-01", f"{max(annees)}-12-31")
    return pd.Series(range(len(jours)), index=jours, dtype=float)


class Plafond(unittest.TestCase):
    def test_garde_les_premiers_jours_de_chaque_saison(self):
        jours = pd.to_datetime(["2020-03-01", "2020-03-05", "2020-07-01", "2021-04-01"])
        garde = regles.plafonner(jours, 2)
        self.assertEqual(list(garde.strftime("%Y-%m-%d")), ["2020-03-01", "2020-03-05", "2021-04-01"])

    def test_sans_jour(self):
        self.assertEqual(len(regles.plafonner(pd.DatetimeIndex([]), 5)), 0)


class Seuils(unittest.TestCase):
    def test_un_fwi_qui_monte_fait_deborder_le_seuil_fixe(self):
        fwi = fwi_croissant(range(2010, 2014))
        fixe, _ = regles.seuil_fixe(fwi, range(2010, 2012), range(2012, 2014), 10)
        par_saison = regles.jours_par_saison(fixe, range(2012, 2014))
        self.assertTrue(all(j > 10 for j in par_saison.values()))  # toute la saison est au-dessus

    def test_le_seuil_recale_suit_le_fwi(self):
        fwi = fwi_croissant(range(2010, 2014))
        recale, seuils = regles.seuil_recale(fwi, range(2012, 2014), 2, 10)
        self.assertLess(seuils[2012], seuils[2013])  # recalé sur 2010-2011, puis sur 2011-2012
        self.assertTrue(all(j > 0 for j in regles.jours_par_saison(recale, range(2012, 2014)).values()))

    def test_quatre_regles_et_plafond_tenu(self):
        fwi = fwi_croissant(range(2010, 2014))
        r = regles.regles(fwi, range(2010, 2012), range(2012, 2014), 10)
        self.assertEqual(len(r), 4)
        for nom in ("seuil fixe avec plafond", "seuil recalé avec plafond"):
            self.assertTrue(all(j <= 10 for j in regles.jours_par_saison(r[nom][0], range(2012, 2014)).values()))

    def test_jours_de_saison(self):
        self.assertEqual(regles.jours_de_saison(range(2021, 2022)), 245)  # mars à octobre


class Recommandation(unittest.TestCase):
    def resultats(self, lignes):
        return pd.DataFrame([{"budget": 20, "zone": "Grand Est", "regle": r, "couverts": c, "jours_max_saison": m}
                             for r, c, m in lignes])

    def test_ecarte_les_regles_qui_depassent_le_budget(self):
        r = self.resultats([("seuil fixe", 300, 60), ("seuil fixe avec plafond", 100, 20),
                            ("seuil recalé avec plafond", 120, 20)])
        self.assertEqual(recommander(r, 20), "seuil recalé avec plafond")

    def test_a_egalite_la_plus_simple(self):
        r = self.resultats([("seuil fixe avec plafond", 98, 20), ("seuil recalé avec plafond", 100, 20)])
        self.assertEqual(recommander(r, 20), "seuil fixe avec plafond")


if __name__ == "__main__":
    unittest.main()
