"""Les quatre règles de déclenchement comparées pour Q4, toutes sur le FWI moyen du Grand Est.

- seuil fixe : calé une fois sur les années de calage, puis appliqué tel quel
- seuil fixe avec plafond : pareil, mais on s'arrête quand le budget de la saison est épuisé
- seuil recalé : avant chaque saison, on recale le seuil sur les saisons précédentes (même nombre d'années que le calage)
- seuil recalé avec plafond : les deux

Le plafond prend les jours dans l'ordre du calendrier : le jour de la décision, on ne connaît pas la suite de la saison.
"""

import pandas as pd

from ..h3.regle import en_saison, jours_de_renfort, seuil_cale


def plafonner(jours, plafond):
    """Garde, dans chaque saison, les `plafond` premiers jours de renfort dans l'ordre du calendrier."""
    jours = pd.DatetimeIndex(sorted(jours))
    if len(jours) == 0:
        return jours
    rang = pd.Series(1, index=jours).groupby(jours.year).cumsum()
    return pd.DatetimeIndex(rang[rang <= plafond].index)


def seuil_fixe(fwi, calage, test, budget):
    seuil = seuil_cale(fwi, calage, budget)
    return jours_de_renfort(fwi, seuil, test), {a: seuil for a in test}


def seuil_recale(fwi, test, fenetre, budget):
    """Avant chaque saison, le seuil est recalé sur les `fenetre` saisons qui la précèdent."""
    seuils, jours = {}, []
    for annee in test:
        seuils[annee] = seuil_cale(fwi, range(annee - fenetre, annee), budget)
        jours.extend(jours_de_renfort(fwi, seuils[annee], [annee]))
    return pd.DatetimeIndex(sorted(jours)), seuils


def regles(fwi, calage, test, budget):
    """Les jours de renfort des quatre règles, et les seuils utilisés chaque saison."""
    fixe, seuils_fixes = seuil_fixe(fwi, calage, test, budget)
    recale, seuils_recales = seuil_recale(fwi, test, len(calage), budget)
    return {
        "seuil fixe": (fixe, seuils_fixes),
        "seuil fixe avec plafond": (plafonner(fixe, budget), seuils_fixes),
        "seuil recalé chaque saison": (recale, seuils_recales),
        "seuil recalé avec plafond": (plafonner(recale, budget), seuils_recales),
    }


def jours_par_saison(jours, test):
    jours = pd.DatetimeIndex(jours)
    return {a: int((jours.year == a).sum()) for a in test}


def jours_de_saison(test):
    """Nombre de jours de mars à octobre sur les saisons de test : la base du « gain sur le hasard »."""
    dates = pd.date_range(f"{min(test)}-01-01", f"{max(test)}-12-31")
    return int(en_saison(dates).sum())
