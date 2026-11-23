"""Table commune -> maille Copernicus (commune_maille.csv), étape 5 du plan de nettoyage (#62).

Chaque commune du Grand Est va dans une seule maille de la grille FWI (règle F4), celle qui contient
son centre. Le centre est `representative_point()` calculé en Lambert 93 : il tombe toujours dans la
commune, alors que le centroïde d'une commune en croissant peut tomber dehors.

La grille est celle de `fwi_grand-est_AAAA.nc` (13 × 22, zone [50.25, 3.25, 47.25, 8.5], #45) : les
latitudes et longitudes du fichier sont les centres des mailles, tous les 0,25°. Une maille va donc de
0,125° de part et d'autre de son centre, et la maille qui contient un point est la plus proche.

Sert ensuite au FWI moyen d'un département (journal du 19/11, #61) et à la maille des feux.
"""

import numpy as np
import pandas as pd

from ..qualite.regles import Controle, Regle

LAMBERT_93 = "EPSG:2154"
WGS84 = "EPSG:4326"
PAS = 0.25
# centres des mailles, du nord au sud et d'ouest en est, comme dans les fichiers .nc
LATITUDES = np.round(np.arange(50.25, 47.25 - PAS / 2, -PAS), 2)
LONGITUDES = np.round(np.arange(3.25, 8.5 + PAS / 2, PAS), 2)


def centre_maille(valeurs, centres):
    """Centre de la maille la plus proche, pour chaque valeur. Vide si la valeur est hors de la grille."""
    valeurs = np.asarray(valeurs, dtype=float)
    plus_proche = centres[np.abs(valeurs[:, None] - centres[None, :]).argmin(axis=1)]
    dans_grille = np.abs(valeurs - plus_proche) <= PAS / 2
    return pd.Series(np.where(dans_grille, plus_proche, np.nan))


def commune_maille(contours):
    """Une ligne par commune : son point (WGS84) et le centre de sa maille."""
    communes = contours.to_crs(LAMBERT_93)
    points = communes.representative_point().to_crs(WGS84)
    table = pd.DataFrame({
        "code_commune_2026": communes["code"].to_numpy(),
        "departement": communes["codeDepartement"].to_numpy(),
        "latitude_point": points.y.round(5).to_numpy(),
        "longitude_point": points.x.round(5).to_numpy(),
    })
    table["latitude"] = centre_maille(table["latitude_point"], LATITUDES)
    table["longitude"] = centre_maille(table["longitude_point"], LONGITUDES)
    hors_grille = table[["latitude", "longitude"]].isna().any(axis=1)
    table.loc[hors_grille, ["latitude", "longitude"]] = np.nan  # une maille, c'est les deux ou rien
    return table.sort_values("code_commune_2026").reset_index(drop=True)


def regles_commune_maille(nb_communes):
    return [
        Regle(
            id="F4", dimension="cohérence", portee="commune_maille.csv, une seule maille par commune du Grand Est",
            controle=lambda t: Controle(
                abs(len(t) - nb_communes) + int(t["code_commune_2026"].duplicated().sum())
                + int(t[["latitude", "longitude"]].isna().any(axis=1).sum()),
                nb_communes, "communes manquantes, en double ou hors de la grille",
            ),
            seuil=0.0, severite="bloquer",
            decision="on arrête : une commune sans maille n'aurait pas de FWI, une commune en double le compterait 2 fois",
        ),
    ]
