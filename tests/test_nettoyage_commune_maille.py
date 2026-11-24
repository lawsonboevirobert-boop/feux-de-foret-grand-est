"""Tests de la table commune -> maille, sur de petites communes faites à la main (en WGS84, en degrés).

    python -m unittest discover -s tests -t .
"""

import unittest

import geopandas as gpd
from shapely.geometry import Polygon, box

from src.nettoyage.commune_maille import commune_maille, regles_commune_maille
from src.qualite.regles import QualiteBloquante, barriere, executer


def contours(communes):
    """communes : (code, département, géométrie en WGS84)."""
    return gpd.GeoDataFrame(
        {"code": [c[0] for c in communes], "codeDepartement": [c[1] for c in communes]},
        geometry=[c[2] for c in communes],
        crs="EPSG:4326",
    )


# une commune en croissant (un U ouvert vers le nord) : son centroïde tombe dans le creux, hors de la commune
CROISSANT = Polygon([(7.60, 48.40), (7.90, 48.40), (7.90, 48.70), (7.85, 48.70), (7.85, 48.45),
                     (7.65, 48.45), (7.65, 48.70), (7.60, 48.70)])


class TestCommuneMaille(unittest.TestCase):
    def test_maille_qui_contient_le_point(self):
        # petite commune autour de Strasbourg (48,58 ; 7,75) : maille centrée sur 48,50 ; 7,75
        table = commune_maille(contours([("67482", "67", box(7.74, 48.57, 7.76, 48.59))]))
        self.assertEqual(table.loc[0, "latitude"], 48.5)
        self.assertEqual(table.loc[0, "longitude"], 7.75)

    def test_point_dans_la_commune_meme_en_croissant(self):
        table = commune_maille(contours([("67001", "67", CROISSANT)]))
        self.assertTrue(CROISSANT.contains(gpd.points_from_xy(table["longitude_point"], table["latitude_point"])[0]))
        self.assertFalse(CROISSANT.contains(CROISSANT.centroid))  # le piège que representative_point évite

    def test_hors_grille_vide(self):
        # une commune au sud de la zone téléchargée (47,25 - 0,125) n'a pas de maille : vide, pas la plus proche
        table = commune_maille(contours([("68999", "68", box(7.30, 46.90, 7.32, 46.92))]))
        self.assertTrue(table[["latitude", "longitude"]].isna().all(axis=None))

    def test_f4_passe(self):
        table = commune_maille(contours([("67482", "67", box(7.74, 48.57, 7.76, 48.59)),
                                         ("88160", "88", box(6.48, 48.15, 6.50, 48.17))]))
        self.assertEqual(barriere(executer(table, regles_commune_maille(2))), [])

    def test_f4_commune_perdue_on_arrete(self):
        table = commune_maille(contours([("67482", "67", box(7.74, 48.57, 7.76, 48.59))]))
        with self.assertRaises(QualiteBloquante):
            barriere(executer(table, regles_commune_maille(2)))

    def test_f4_hors_grille_on_arrete(self):
        table = commune_maille(contours([("68999", "68", box(7.30, 46.90, 7.32, 46.92))]))
        with self.assertRaises(QualiteBloquante):
            barriere(executer(table, regles_commune_maille(1)))


if __name__ == "__main__":
    unittest.main()
