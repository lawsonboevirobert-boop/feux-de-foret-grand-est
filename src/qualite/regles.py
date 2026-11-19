"""Une règle de qualité = un test qui renvoie réussite ou échec (cours du 18/11).

Chaque règle a :
- une portée (le sélecteur) : sur quelles lignes / colonnes elle porte
- un controle (le prédicat) : une fonction qui compte les cas fautifs
- un seuil : la part de cas fautifs tolérée (0 = aucun)
- une sévérité : bloquer, alerter ou tolérer
- une décision : ce qu'on fait si elle échoue

Les ids reprennent ceux de docs/qualite/regles.md.
"""

from dataclasses import dataclass
from typing import Callable

import pandas as pd

SEVERITES = ("bloquer", "alerter", "tolerer")


@dataclass
class Controle:
    """Ce que renvoie le controle d'une règle."""
    fautifs: int     # nb de cas qui ne respectent pas la règle
    controles: int   # nb de cas regardés
    detail: str = ""  # résumé lisible, sans donnée identifiante


@dataclass
class Regle:
    id: str
    dimension: str
    portee: str
    controle: Callable[[pd.DataFrame], Controle]
    seuil: float      # part de fautifs tolérée, entre 0 et 1
    severite: str
    decision: str

    def __post_init__(self):
        if self.severite not in SEVERITES:
            raise ValueError(f"{self.id} : sévérité inconnue {self.severite!r}")


class QualiteBloquante(Exception):
    """Levée quand au moins une règle bloquante échoue : le chargement s'arrete."""


def executer(df, regles):
    """Fait tourner toutes les règles et renvoie le rapport (une ligne par règle)."""
    lignes = []
    for regle in regles:
        resultat = regle.controle(df)
        taux = resultat.fautifs / resultat.controles if resultat.controles else 0.0
        lignes.append({
            "règle": regle.id,
            "dimension": regle.dimension,
            "portée": regle.portee,
            "seuil": f"{regle.seuil:.0%}",
            "contrôlés": resultat.controles,
            "fautifs": resultat.fautifs,
            "résultat": "réussite" if taux <= regle.seuil else "échec",
            "sévérité": regle.severite,
            "décision": regle.decision,
            "détail": resultat.detail,
        })
    return pd.DataFrame(lignes)


def barriere(rapport):
    """Barrière de qualité : un échec bloquant -> exception, des alertes seules -> on passe.

    Renvoie la liste des règles en alerte pour les afficher.
    """
    echecs = rapport[rapport["résultat"] == "échec"]
    bloquants = echecs[echecs["sévérité"] == "bloquer"]
    if not bloquants.empty:
        raise QualiteBloquante(f"règles bloquantes en échec : {', '.join(bloquants['règle'])}")
    return echecs[echecs["sévérité"] == "alerter"]["règle"].tolist()
