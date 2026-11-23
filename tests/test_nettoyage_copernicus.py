"""Tests de l'étape FWI (Copernicus), sur de petits fichiers NetCDF faits à la main.

    python -m unittest discover -s tests -t .
"""

import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

from src.nettoyage.commun import SourceManquante
from src.nettoyage.copernicus import (
    fwi_departement,
    jours_manquants,
    lire_fichiers,
    lire_fwi,
    mailles_sans_fwi,
    regles_fwi,
)
from src.nettoyage.tables import jour_departement, regles_jour_departement
from src.qualite.regles import QualiteBloquante, barriere, executer


def ecrire_nc(chemin, dates, valeurs, latitudes=(48.75, 48.5), longitudes=(7.75, 8.0)):
    """Un petit fichier comme ceux de l'EWDS : variable fwinx sur (valid_time, latitude, longitude)."""
    ds = xr.Dataset(
        {"fwinx": (("valid_time", "latitude", "longitude"), np.asarray(valeurs, dtype="float32"))},
        coords={"valid_time": pd.to_datetime(dates), "latitude": list(latitudes), "longitude": list(longitudes)},
    )
    ds.to_netcdf(chemin)


# 2 mailles utilisées : (48.75, 7.75) et (48.5, 7.75). Le 67 a 2 communes, le 68 une seule
COMMUNE_MAILLE = pd.DataFrame({
    "code_commune_2026": ["67180", "67482", "68066"],
    "departement": ["67", "67", "68"],
    "latitude": [48.75, 48.5, 48.5],
    "longitude": [7.75, 7.75, 7.75],
})
FORET = pd.DataFrame({
    "code_commune_2026": ["67180", "67482", "68066"],
    "surface_foret_ha": [300.0, 100.0, 50.0],  # Haguenau très boisée, Strasbourg peu
})


class TestLecture(unittest.TestCase):
    def test_deux_noms_de_fichier_une_seule_fois_par_annee(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            valeurs = np.zeros((1, 2, 2))
            ecrire_nc(d / "fwi_grand_est_2024.nc", ["2024-07-01"], valeurs)     # nom du script de récupération
            ecrire_nc(d / "fwi_grand-est_2024.nc", ["2024-07-01"], valeurs)     # nom de l'archive de Lawson
            ecrire_nc(d / "fwi_grand-est_2025.nc", ["2025-07-01"], valeurs)
            self.assertEqual([f.name[-7:-3] for f in lire_fichiers(d)], ["2024", "2025"])

    def test_pas_de_fichier_message_clair(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(SourceManquante) as erreur:
                lire_fichiers(Path(d))
        self.assertIn("python -m src.recuperation copernicus", str(erreur.exception))

    def test_une_ligne_par_jour_et_par_maille(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "fwi_grand_est_2024.nc"
            ecrire_nc(f, ["2024-07-01", "2024-07-02"], np.arange(8).reshape(2, 2, 2))
            fwi = lire_fwi([f])
        self.assertEqual(len(fwi), 8)
        self.assertEqual(list(fwi.columns), ["date", "latitude", "longitude", "fwi"])
        self.assertEqual(fwi["date"].min(), "2024-07-01")


class TestFwiDepartement(unittest.TestCase):
    def setUp(self):
        # un jour : 40 sur la maille de Haguenau, 10 sur celle de Strasbourg
        self.fwi_maille = pd.DataFrame({
            "date": ["2024-07-01"] * 2, "latitude": [48.75, 48.5], "longitude": [7.75, 7.75], "fwi": [40.0, 10.0],
        })
        self.dep = fwi_departement(self.fwi_maille, COMMUNE_MAILLE, FORET).set_index("departement")

    def test_pondere_par_la_foret(self):
        self.assertAlmostEqual(self.dep.loc["67", "fwi_moyen"], (40 * 300 + 10 * 100) / 400)  # 32,5

    def test_moyenne_simple_sur_les_communes(self):
        self.assertAlmostEqual(self.dep.loc["67", "fwi_moyen_simple"], (40 + 10) / 2)  # 25

    def test_departement_a_une_maille(self):
        self.assertAlmostEqual(self.dep.loc["68", "fwi_moyen"], 10)


class TestRegles(unittest.TestCase):
    def test_jour_manquant_on_arrete(self):
        fwi = pd.DataFrame({
            "date": ["2024-01-01", "2024-01-03"], "latitude": [48.75] * 2, "longitude": [7.75] * 2, "fwi": [1.0, 2.0],
        })
        self.assertEqual(jours_manquants(fwi), 1)  # le 2 janvier
        with self.assertRaises(QualiteBloquante):
            barriere(executer(fwi, regles_fwi(COMMUNE_MAILLE)))

    def test_maille_absente_de_la_grille(self):
        fwi = pd.DataFrame({"date": ["2024-01-01"], "latitude": [48.75], "longitude": [7.75], "fwi": [1.0]})
        self.assertEqual(mailles_sans_fwi(fwi, COMMUNE_MAILLE), 1)  # (48.5, 7.75) manque

    def test_valeur_hors_bornes_seulement_alerte(self):
        dates = pd.date_range("2024-01-01", "2024-01-02").strftime("%Y-%m-%d")
        fwi = pd.DataFrame({
            "date": list(dates) * 2, "latitude": [48.75] * 2 + [48.5] * 2,
            "longitude": [7.75] * 4, "fwi": [1.0, 150.0, 2.0, 3.0],
        })
        self.assertEqual(barriere(executer(fwi, regles_fwi(COMMUNE_MAILLE))), ["F3"])


def calendrier(dates):
    return pd.DataFrame([
        {"date": d, "departement": "67", "jour_semaine": "lundi", "week_end": False, "ferie": False, "vacances": "non"}
        for d in dates
    ])


class TestJourDepartement(unittest.TestCase):
    CAL = calendrier(["2024-07-01", "2026-12-01"])
    FEUX = pd.DataFrame({"id_feu": [], "date": [], "departement": [], "surface_parcourue_ha": [],
                         "surface_foret_ha": [], "doublon_probable": []}).astype({"doublon_probable": bool})
    POPULATION = pd.DataFrame({"departement": ["67", "67"], "annee": [2024, 2026], "statut_bdiff": ["renseigné"] * 2})
    MDF = pd.DataFrame({"date": [], "departement": [], "niveau": []})
    FWI = pd.DataFrame({"date": ["2024-07-01"], "departement": ["67"], "fwi_moyen": [32.5], "fwi_moyen_simple": [25.0]})

    def test_fwi_branche_et_vide_hors_couverture(self):
        table = jour_departement(self.CAL, self.FEUX, self.POPULATION, self.MDF, None, None, self.FWI).set_index("date")
        self.assertEqual(table.loc["2024-07-01", "fwi_moyen"], 32.5)
        self.assertTrue(pd.isna(table.loc["2026-12-01", "fwi_moyen"]))  # pas téléchargé : vide, pas 0

    def test_sans_copernicus_tout_vide(self):
        table = jour_departement(self.CAL, self.FEUX, self.POPULATION, self.MDF, None)
        self.assertTrue(table["fwi_moyen"].isna().all())

    def test_jour_couvert_sans_fwi_on_arrete(self):
        table = jour_departement(self.CAL, self.FEUX, self.POPULATION, self.MDF, None)  # FWI perdu
        regles = regles_jour_departement(self.FEUX, len(self.CAL), jours_fwi=["2024-07-01"])
        with self.assertRaises(QualiteBloquante):
            barriere(executer(table, regles))


if __name__ == "__main__":
    unittest.main()
