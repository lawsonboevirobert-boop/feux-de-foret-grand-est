"""Tests de l'étoile (#76), sur de petites tables faites à la main.

    python -m unittest discover -s tests -t .
"""

import unittest

import pandas as pd

from src.etoile import tables
from src.qualite.regles import QualiteBloquante, barriere, executer


def feux(lignes):
    """lignes : (id_feu, date, département, commune 2026, cause, surface, doublon probable)."""
    return pd.DataFrame({
        "id_feu": [l[0] for l in lignes],
        "date": [l[1] for l in lignes],
        "heure": "14:00",
        "departement": [l[2] for l in lignes],
        "code_commune_2026": [l[3] for l in lignes],
        "code_commune_origine": [l[3] for l in lignes],
        "cause": [l[4] for l in lignes],
        "surface_parcourue_ha": [l[5] for l in lignes],
        "surface_foret_ha": 0.0,
        "precision": None,
        "doublon_probable": [l[6] for l in lignes],
    })


FEUX = feux([
    ("2025-1", "2025-08-13", "67", "67180", "inconnue", 2.0, False),
    ("2025-2", "2025-08-13", "67", "67180", "inconnue", 2.0, True),  # doublon de Haguenau (B3)
    ("2025-3", "2025-04-02", "88", "88160", "Malveillance", 0.5, False),
])

CALENDRIER = pd.DataFrame({
    "date": ["2025-04-02", "2025-04-02", "2025-08-13", "2025-08-13", "2025-12-01", "2025-12-01"],
    "departement": ["67", "88"] * 3,
    "jour_semaine": ["mercredi", "mercredi", "mercredi", "mercredi", "lundi", "lundi"],
    "week_end": False,
})

COMMUNE_MAILLE = pd.DataFrame({
    "code_commune_2026": ["67180", "88160"],
    "departement": ["67", "88"],
    "latitude": [48.75, 48.25],
    "longitude": [7.75, 6.5],
})

FORET = pd.DataFrame({
    "code_commune_2026": ["67180", "88160"],
    "surface_commune_ha": [18000.0, 4500.0],
    "surface_foret_ha": [13000.0, 2600.0],
    "part_foret": [0.72, 0.58],
    "part_resineux": [0.4, 0.6],
    "part_resineux_stricte": [0.3, 0.5],
    "edition_bd_foret": ["2014-04-01", "2015-04-01"],
})

DEPARTEMENTS_COG = pd.DataFrame({"DEP": ["67", "88", "75"], "LIBELLE": ["Bas-Rhin", "Vosges", "Paris"],
                                 "REG": ["44", "44", "11"]})


def jours(statut="renseigné", nb_feux=1.0, niveau=2.0):
    return pd.DataFrame({
        "date": ["2025-08-13", "2025-08-13"], "departement": ["67", "88"], "niveau": [niveau, None],
        "ferie": False, "vacances": "oui", "statut_bdiff": statut, "nb_feux": [nb_feux, None if statut else 0.0],
        "surface_parcourue_ha": None, "surface_foret_ha": None, "nb_detections_satellite": None,
        "nb_communes_detection": None, "fwi_moyen": None,
    })


def etoile(jour=None, f=FEUX):
    t = {
        "dim_date": tables.dim_date(CALENDRIER),
        "dim_departement": tables.dim_departement(DEPARTEMENTS_COG),
        "dim_maille": tables.dim_maille(COMMUNE_MAILLE),
        "dim_commune": tables.dim_commune(COMMUNE_MAILLE, FORET),
        "dim_niveau": tables.dim_niveau(),
        "dim_cause": tables.dim_cause(f),
        "fait_feu": tables.fait_feu(f, "2026-11-22"),
        "fait_jour_departement": tables.fait_jour_departement(jour if jour is not None else jours()),
        "dim_commune_historique": pd.DataFrame({"code_origine": ["67180"], "code_commune_2026": ["67180"],
                                                "statut": ["commune 2026"], "commune_jusqu_au": [""]}),
    }
    return {**t, "feux": f}


class TestDimensions(unittest.TestCase):
    def test_dim_date(self):
        d = tables.dim_date(CALENDRIER).set_index("date")
        self.assertEqual(len(d), 3)  # une ligne par jour, pas par département
        self.assertEqual(d.loc["2025-08-13", "nom_mois"], "août")
        self.assertTrue(d.loc["2025-04-02", "saison"])
        self.assertFalse(d.loc["2025-12-01", "saison"])  # décembre : hors saison feux

    def test_dim_departement_grand_est_seulement(self):
        d = tables.dim_departement(DEPARTEMENTS_COG).set_index("departement")
        self.assertEqual(list(d.index), ["67", "88"])
        self.assertEqual(d.loc["67", "zone_feries"], "Alsace-Moselle")
        self.assertEqual(d.loc["88", "academie"], "Nancy-Metz")

    def test_dim_commune_a_sa_maille(self):
        d = tables.dim_commune(COMMUNE_MAILLE, FORET).set_index("code_commune_2026")
        self.assertEqual(d.loc["67180", "id_maille"], "48.75_7.75")
        self.assertEqual(d.loc["88160", "id_maille"], "48.25_6.50")

    def test_historique_date_de_fin(self):
        passage = pd.DataFrame({"code_origine": ["88001", "88160"], "code_commune_2026": ["88160", "88160"],
                                "statut": ["déléguée ou associée", "commune 2026"]})
        mouvements = pd.DataFrame({"COM_AV": ["88001"], "COM_AP": ["88160"], "DATE_EFF": ["2016-01-01"]})
        h = tables.dim_commune_historique(passage, mouvements, pd.Series(["88160"])).set_index("code_origine")
        self.assertEqual(h.loc["88001", "commune_jusqu_au"], "2016-01-01")
        self.assertEqual(h.loc["88160", "commune_jusqu_au"], "")  # toujours une commune


class TestFaits(unittest.TestCase):
    def test_fait_feu_sans_doublon(self):
        self.assertEqual(list(tables.fait_feu(FEUX, "2026-11-22")["id_feu"]), ["2025-3", "2025-1"])

    def test_fait_feu_pas_reecrit(self):
        precedent = pd.DataFrame({"id_feu": ["2025-1"], "date_chargement": ["2026-11-01"]})
        f = tables.fait_feu(FEUX, "2026-11-22", precedent).set_index("id_feu")
        self.assertEqual(f.loc["2025-1", "date_chargement"], "2026-11-01")  # déjà chargé : on garde sa date
        self.assertEqual(f.loc["2025-3", "date_chargement"], "2026-11-22")  # nouveau

    def test_niveau_entier_et_vide_hors_saison(self):
        j = tables.fait_jour_departement(jours())
        self.assertEqual(str(j["niveau"].dtype), "Int64")
        self.assertTrue(pd.isna(j.loc[1, "niveau"]))  # vide, pas « faible »


class TestRegles(unittest.TestCase):
    def test_etoile_propre_on_passe(self):
        self.assertEqual(barriere(executer(etoile(), tables.regles_etoile())), ["E5"])  # FWI pas encore là

    def test_e1_cle_en_double_on_arrete(self):
        t = etoile()
        t["dim_departement"] = pd.concat([t["dim_departement"], t["dim_departement"].head(1)])
        with self.assertRaises(QualiteBloquante):
            barriere(executer(t, tables.regles_etoile()))

    def test_e2_commune_sans_dimension_on_arrete(self):
        t = etoile()
        t["fait_feu"].loc[0, "code_commune_2026"] = "67999"
        with self.assertRaises(QualiteBloquante):
            barriere(executer(t, tables.regles_etoile()))

    def test_e3_feu_perdu_on_arrete(self):
        t = etoile()
        t["fait_feu"] = t["fait_feu"].head(1)
        with self.assertRaises(QualiteBloquante):
            barriere(executer(t, tables.regles_etoile()))

    def test_e4_zero_invente_on_arrete(self):
        with self.assertRaises(QualiteBloquante):
            barriere(executer(etoile(jours(statut="non renseigné", nb_feux=0.0)), tables.regles_etoile()))


if __name__ == "__main__":
    unittest.main()
