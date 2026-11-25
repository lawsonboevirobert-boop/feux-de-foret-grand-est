"""Test de H3 en deux temps, pour que la règle soit figée avant de regarder les années de test.

    python -m src.h3 caler     # calage sur 2017-2022 : écrit docs/analyse/h3/regle-calee.json
    python -m src.h3 tester    # applique la règle figée à 2023-2025 : écrit docs/analyse/h3/resultats-test.csv

Il faut d'abord les tables du nettoyage (`python -m src.nettoyage`). Le protocole est dans docs/analyse/test-h3.md.
"""

import json
import math
import sys
from datetime import date

import pandas as pd

from ..nettoyage.commun import PROPRE, RACINE
from . import regle

SORTIE = RACINE / "docs" / "analyse" / "h3"
REGLE = SORTIE / "regle-calee.json"
RESULTATS = SORTIE / "resultats-test.csv"

CALAGE = range(2017, 2023)          # journal du 19/11
SEUIL_REGLE = range(2018, 2023)     # saisons complètes avec le calendrier scolaire (il commence en septembre 2017)
TEST = range(2023, 2026)
GAIN_H3 = 0.20                      # journal du 18/11, fixé avant tout calcul

# la règle combinée, puis les variantes calées en même temps : sensibilité et part de chaque variable
VARIANTES = {
    "combinee": (regle.VARIABLES, "part_resineux"),
    "combinee_resineux_stricte": (regle.VARIABLES, "part_resineux_stricte"),
    "modele_fwi_seul": (["log_fwi"], "part_resineux"),
    "sans_type_de_jour": (["log_fwi", "log_historique", "part_resineux"], "part_resineux"),
    "sans_historique": (["log_fwi", "week_end", "ferie", "vacances", "part_resineux"], "part_resineux"),
    "sans_resineux": (["log_fwi", "week_end", "ferie", "vacances", "log_historique"], "part_resineux"),
}


def lire(nom, **kwargs):
    chemin = PROPRE / nom
    if not chemin.exists():
        sys.exit(f"{nom} introuvable dans data/processed : lancer d'abord `python -m src.nettoyage`")
    return pd.read_csv(chemin, dtype={"departement": str, "code_commune_2026": str}, **kwargs)


def charger():
    jd = lire("jour_departement.csv", parse_dates=["date"])
    foret = lire("foret_commune.csv")
    maille = lire("commune_maille.csv")
    feux = regle.feux_par_secteur(lire("feux_travail.csv"), maille)
    return {
        "jour_departement": jd, "foret": foret, "feux": feux,
        "secteurs": regle.secteurs(maille, foret), "renseignees": regle.annees_renseignees(jd),
        "fwi_maille": lire("fwi_maille.csv"), "calendrier": lire("calendrier.csv"),
    }


def table(d, annees, resineux):
    return regle.table_secteur_jour(d["secteurs"], d["fwi_maille"], d["calendrier"], d["feux"],
                                    d["renseignees"], annees, resineux)


def caler():
    d = charger()
    base = regle.fwi_grand_est(d["jour_departement"], d["foret"])
    sortie = {
        "date_de_calage": date.today().isoformat(),
        "protocole": {"calage": [CALAGE.start, CALAGE.stop - 1], "seuil_regles": [SEUIL_REGLE.start, SEUIL_REGLE.stop - 1],
                      "test": [TEST.start, TEST.stop - 1], "jours_par_saison": regle.JOURS_PAR_SAISON,
                      "mois": [min(regle.MOIS_SAISON), max(regle.MOIS_SAISON)], "gain_h3": GAIN_H3},
        "fwi_seul": {"seuil": regle.seuil_cale(base, CALAGE),
                     "seuil_sur_2018_2022": regle.seuil_cale(base, SEUIL_REGLE)},
        "regles": {},
    }
    print(f"FWI seul : seuil {sortie['fwi_seul']['seuil']:.2f} (2017-2022), "
          f"{sortie['fwi_seul']['seuil_sur_2018_2022']:.2f} (2018-2022)")
    tables = {}
    for nom, (variables, resineux) in VARIANTES.items():
        if resineux not in tables:
            t = table(d, CALAGE, resineux)
            tables[resineux] = t[t["vacances"].notna()]  # toutes les variantes sur les mêmes lignes
        t = tables[resineux]
        modele = regle.caler_modele(t, variables)
        modele["part_resineux"] = resineux
        modele["seuil"] = regle.seuil_cale(regle.score_par_jour(t, modele), SEUIL_REGLE)
        sortie["regles"][nom] = modele
        effets = ", ".join(f"{v} x{math.exp(c):.2f}" for v, c in modele["coefficients"].items())
        print(f"{nom} : seuil {modele['seuil']:.3f} départs attendus ; {modele['lignes']} lignes, "
              f"{modele['departs']} départs ; {effets}")
    SORTIE.mkdir(parents=True, exist_ok=True)
    REGLE.write_text(json.dumps(sortie, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"règle figée dans {REGLE.relative_to(RACINE)}")


def tester():
    if not REGLE.exists():
        sys.exit("pas de règle calée : lancer d'abord `python -m src.h3 caler`")
    figee = json.loads(REGLE.read_text(encoding="utf-8"))
    d = charger()
    feux = d["feux"][d["feux"]["annee"].isin(TEST)]
    zones = {"Grand Est": feux, "67 (information)": feux[feux["departement"] == "67"]}
    lignes = []

    base = regle.fwi_grand_est(d["jour_departement"], d["foret"])
    jours_base = regle.jours_de_renfort(base, figee["fwi_seul"]["seuil"], TEST)
    for zone, f in zones.items():
        lignes.append({"regle": "fwi_seul (valeur de départ)", "zone": zone, **regle.evaluer(jours_base, f)})

    tables = {}
    for nom, modele in figee["regles"].items():
        resineux = modele["part_resineux"]
        if resineux not in tables:
            tables[resineux] = table(d, TEST, resineux)
        score = regle.score_par_jour(tables[resineux], modele)
        jours = regle.jours_de_renfort(score, modele["seuil"], TEST)
        for zone, f in zones.items():
            lignes.append({"regle": nom, "zone": zone, **regle.evaluer(jours, f)})
        if nom == "combinee":
            # diagnostic seulement : les N meilleurs jours du test, N = jours du FWI seul. Suppose de connaître la saison
            s = score[regle.en_saison(score.index) & score.index.year.isin(TEST)]
            meilleurs = s.sort_values(ascending=False).index[:len(jours_base)]
            lignes.append({"regle": "combinee, à jours égaux (diagnostic)", "zone": "Grand Est",
                           **regle.evaluer(meilleurs, zones["Grand Est"])})

    res = pd.DataFrame(lignes)
    res.to_csv(RESULTATS, index=False, encoding="utf-8")
    ge = res[res["zone"] == "Grand Est"].set_index("regle")
    with pd.option_context("display.width", 200, "display.max_columns", 20):
        print(ge[["couverts", "departs", "taux", "jours", "jours_avec_feu", "precision",
                  "surface_couverte_ha", "feux_1ha_couverts"]].round(3))

    b, c = ge.loc["fwi_seul (valeur de départ)"], ge.loc["combinee"]
    cible = math.ceil((1 + GAIN_H3) * b["couverts"])
    valide = c["couverts"] >= cible and c["jours"] <= b["jours"]
    print(f"\nH3 : la règle combinée couvre {c['couverts']} départs avec {c['jours']} jours ; il en fallait au moins "
          f"{cible} avec {b['jours']} jours au plus. H3 {'VALIDÉE' if valide else 'NON VALIDÉE'}.")
    print(f"résultats dans {RESULTATS.relative_to(RACINE)}")


def main():
    etapes = {"caler": caler, "tester": tester}
    if len(sys.argv) != 2 or sys.argv[1] not in etapes:
        sys.exit(__doc__)
    etapes[sys.argv[1]]()


if __name__ == "__main__":
    main()
