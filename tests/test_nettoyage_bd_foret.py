"""Tests de la BD Forêt par commune, sur de petits polygones faits à la main (en Lambert 93, en mètres).

    python -m unittest discover -s tests -t .
"""

import unittest

import geopandas as gpd
from shapely.geometry import Polygon, box

from src.nettoyage.bd_foret import LAMBERT_93, categorie, foret_par_commune, preparer, regles_communes, regles_polygones
from src.qualite.regles import barriere, executer

# 2 communes de 100 ha (1 000 m × 1 000 m), une dans le 67, une dans le 57, côte à côte
CONTOURS = gpd.GeoDataFrame(
    {"code": ["67001", "57001"], "codeDepartement": ["67", "57"]},
    geometry=[box(0, 0, 1000, 1000), box(1000, 0, 2000, 1000)],
    crs=LAMBERT_93,
)


def foret(lignes):
    """lignes : (département du fichier, ID, TFV_G11, géométrie)."""
    return gpd.GeoDataFrame(
        {
            "departement_fichier": [l[0] for l in lignes],
            "ID": [l[1] for l in lignes],
            "TFV_G11": [l[2] for l in lignes],
            "edition": "2014-04-01",
        },
        geometry=[l[3] for l in lignes],
        crs=LAMBERT_93,
    )


class TestCategorie(unittest.TestCase):
    def test_categories(self):
        self.assertEqual(categorie("Forêt fermée conifères"), "coniferes")
        self.assertEqual(categorie("Forêt ouverte feuillus"), "feuillus")
        self.assertEqual(categorie("Peupleraie"), "feuillus")
        self.assertEqual(categorie("Forêt fermée mixte"), "mixte")
        self.assertEqual(categorie("Forêt fermée sans couvert arboré"), "sans_couvert")
        self.assertEqual(categorie("Lande"), "")  # pas de la forêt


class TestForetParCommune(unittest.TestCase):
    def setUp(self):
        brut = foret([
            ("67", "A", "Forêt fermée conifères", box(0, 0, 500, 1000)),     # 50 ha de résineux dans 67001
            ("67", "B", "Forêt fermée feuillus", box(500, 0, 1000, 500)),     # 25 ha de feuillus
            ("67", "C", "Forêt fermée sans couvert arboré", box(500, 500, 1000, 750)),  # 12,5 ha sans couvert
            ("67", "D", "Lande", box(500, 750, 1000, 1000)),                  # pas de la forêt
            # le fichier du 67 déborde sur le 57, et le fichier du 57 a la même forêt : à ne compter qu'une fois
            ("67", "E", "Forêt fermée feuillus", box(1000, 0, 1500, 1000)),
            ("57", "A", "Forêt fermée feuillus", box(1000, 0, 1500, 1000)),
        ])
        self.foret = preparer(brut)
        self.table = foret_par_commune(self.foret, CONTOURS).set_index("code_commune_2026")

    def test_surfaces_et_parts(self):
        ligne = self.table.loc["67001"]
        self.assertAlmostEqual(ligne["surface_commune_ha"], 100)
        self.assertAlmostEqual(ligne["surface_foret_ha"], 87.5)  # sans la lande
        self.assertAlmostEqual(ligne["part_foret"], 0.875)
        self.assertAlmostEqual(ligne["part_resineux"], 50 / 75, places=4)  # sans couvert hors du calcul (arrondi à 4 décimales)

    def test_frontiere_comptee_une_fois(self):
        self.assertAlmostEqual(self.table.loc["57001", "surface_foret_ha"], 50)
        self.assertEqual(barriere(executer(self.table.reset_index(), regles_communes(2))), [])

    def test_commune_sans_foret(self):
        contours = CONTOURS.copy()
        contours.loc[1, "geometry"] = box(5000, 0, 6000, 1000)  # loin de toute forêt
        table = foret_par_commune(self.foret, contours).set_index("code_commune_2026")
        self.assertEqual(table.loc["57001", "surface_foret_ha"], 0)
        self.assertTrue(table["part_resineux"].isna()["57001"])  # vide, pas 0


class TestGeometries(unittest.TestCase):
    def test_contour_qui_se_croise_repare(self):
        noeud_papillon = Polygon([(0, 0), (1000, 1000), (1000, 0), (0, 1000)])  # invalide
        prepare = preparer(foret([("67", "Z", "Forêt fermée feuillus", noeud_papillon)]))
        self.assertTrue(prepare["repare"].all())
        self.assertTrue(prepare.is_valid.all())
        self.assertEqual(barriere(executer(prepare, regles_polygones())), [])


if __name__ == "__main__":
    unittest.main()
