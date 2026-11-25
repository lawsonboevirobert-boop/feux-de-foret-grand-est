"""Compare les quatre règles de Q4 sur les années de test du FWI seul.

    python -m src.q4      # écrit docs/analyse/q4/resultats.csv et docs/analyse/q4/jours-par-saison.csv

Il faut d'abord les tables du nettoyage (`python -m src.nettoyage`). Protocole : docs/analyse/budget-jours-q4.md.
"""

import pandas as pd

from ..h3.__main__ import lire
from ..h3.regle import evaluer, fwi_grand_est
from ..nettoyage.commun import RACINE
from . import regles

SORTIE = RACINE / "docs" / "analyse" / "q4"
CALAGE = range(2006, 2017)       # journal du 19/11, FWI seul
TEST = range(2017, 2026)
BUDGET = 20                      # supposé (#41)
SENSIBILITE = (10, 30)
ORDRE_SIMPLICITE = ["seuil fixe avec plafond", "seuil recalé avec plafond"]
ECART_EGALITE = 0.05             # moins de 5 % d'écart de départs couverts : à égalité


def recommander(resultats, budget):
    """Parmi les règles qui ne dépassent le budget dans aucune saison, celle qui couvre le plus de départs.
    À moins de 5 % d'écart, la plus simple. Fixé avant le calcul."""
    r = resultats[(resultats["budget"] == budget) & (resultats["zone"] == "Grand Est")]
    tenables = r[r["jours_max_saison"] <= budget]
    if tenables.empty:
        return None
    meilleur = tenables["couverts"].max()
    proches = tenables[tenables["couverts"] >= (1 - ECART_EGALITE) * meilleur]["regle"].tolist()
    for nom in ORDRE_SIMPLICITE:
        if nom in proches:
            return nom
    return proches[0]


def main():
    jd = lire("jour_departement.csv", parse_dates=["date"])
    foret = lire("foret_commune.csv")
    feux = lire("feux_travail.csv", parse_dates=["date"])
    feux = feux[feux["date"].dt.year.isin(TEST)]
    zones = {"Grand Est": feux, "67 (information)": feux[feux["departement"] == "67"]}
    fwi = fwi_grand_est(jd, foret)
    nb_jours_saison = regles.jours_de_saison(TEST)

    lignes, saisons = [], []
    for budget in (BUDGET, *SENSIBILITE):
        for nom, (jours, seuils) in regles.regles(fwi, CALAGE, TEST, budget).items():
            par_saison = regles.jours_par_saison(jours, TEST)
            for zone, f in zones.items():
                r = evaluer(jours, f)
                lignes.append({
                    "budget": budget, "regle": nom, "zone": zone, **r,
                    "gain_sur_le_hasard": r["taux"] / (r["jours"] / nb_jours_saison) if r["jours"] else float("nan"),
                    "jours_max_saison": max(par_saison.values()),
                    "saisons_au_dessus_du_budget": sum(j > budget for j in par_saison.values()),
                })
            for annee in TEST:
                f = feux[feux["date"].dt.year == annee]
                ja = pd.DatetimeIndex(jours)[pd.DatetimeIndex(jours).year == annee]
                saisons.append({"budget": budget, "regle": nom, "saison": annee, "seuil": round(seuils[annee], 2),
                                "jours": par_saison[annee], "departs": len(f), "couverts": int(f["date"].isin(ja).sum())})

    res = pd.DataFrame(lignes)
    SORTIE.mkdir(parents=True, exist_ok=True)
    res.to_csv(SORTIE / "resultats.csv", index=False, encoding="utf-8")
    pd.DataFrame(saisons).to_csv(SORTIE / "jours-par-saison.csv", index=False, encoding="utf-8")

    with pd.option_context("display.width", 220, "display.max_columns", 20):
        for budget in (BUDGET, *SENSIBILITE):
            ge = res[(res["budget"] == budget) & (res["zone"] == "Grand Est")].set_index("regle")
            print(f"\nbudget {budget} jours par saison, Grand Est {min(TEST)}-{max(TEST)}")
            print(ge[["couverts", "departs", "taux", "jours", "jours_max_saison", "saisons_au_dessus_du_budget",
                      "precision", "gain_sur_le_hasard", "feux_1ha_couverts"]].round(3))
            print(f"règle recommandée (critère fixé avant le calcul) : {recommander(res, budget)}")


if __name__ == "__main__":
    main()
