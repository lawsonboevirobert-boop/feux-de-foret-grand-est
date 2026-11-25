"""Les briques du test de H3 : secteurs, historique, table secteur × jour, modèle, seuil, évaluation.

Un secteur = les communes d'un département dans une maille du FWI (0,25°). C'est le plus petit endroit
où l'on a à la fois le FWI (la maille), le calendrier et le statut de la BDIFF (le département).

La règle combinée prévoit, pour chaque secteur et chaque jour, un nombre de départs attendu (régression
de Poisson). Le score d'un jour est la somme sur les secteurs du Grand Est : le nombre de départs attendus
dans la région ce jour-là. Comme pour le FWI seul, on renforce les jours où le score dépasse un seuil
calé pour donner 20 jours par saison sur les années de calage.
"""

from collections import Counter

import numpy as np
import pandas as pd
from sklearn.linear_model import PoissonRegressor

MOIS_SAISON = range(3, 11)  # mars à octobre : les jours où le dispositif renforcé peut être lancé
JOURS_PAR_SAISON = 20       # budget supposé, à remplacer par le chiffre du SDIS (#41)
CLE_SECTEUR = ["departement", "latitude", "longitude"]
DECIMALES = 2               # les coordonnées des mailles sont des multiples de 0,25

# la règle combinée : le FWI et les trois variables de H3 (journal du 18/11)
VARIABLES = ["log_fwi", "week_end", "ferie", "vacances", "log_historique", "part_resineux"]


def en_saison(dates):
    return pd.DatetimeIndex(dates).month.isin(MOIS_SAISON)


# ---------- la base : le FWI seul ----------

def fwi_grand_est(jour_departement, foret_commune):
    """FWI moyen du Grand Est chaque jour : le FWI de chaque département (`fwi_moyen`, déjà pondéré par la
    forêt de ses communes), pondéré par la forêt du département. Revient à pondérer chaque commune par sa forêt."""
    foret = foret_commune.groupby("departement")["surface_foret_ha"].sum()
    fwi = jour_departement.pivot(index="date", columns="departement", values="fwi_moyen")
    poids = foret.reindex(fwi.columns)
    return (fwi * poids).sum(axis=1, min_count=1) / fwi.notna().mul(poids).sum(axis=1)


# ---------- le seuil et l'évaluation, communs aux deux règles ----------

def seuil_cale(score_par_jour, annees):
    """La valeur dépassée en moyenne JOURS_PAR_SAISON jours par saison (mars à octobre) sur les années de calage.
    Un jour de renfort est un jour où le score est strictement au-dessus."""
    s = score_par_jour[en_saison(score_par_jour.index) & score_par_jour.index.year.isin(annees)].dropna()
    rang = JOURS_PAR_SAISON * len(set(annees))
    return float(np.sort(s.to_numpy())[::-1][rang - 1])


def jours_de_renfort(score_par_jour, seuil, annees):
    s = score_par_jour[en_saison(score_par_jour.index) & score_par_jour.index.year.isin(annees)]
    return pd.DatetimeIndex(s[s > seuil].index)


def evaluer(jours, feux):
    """Le KPI et ses garde-fous pour un ensemble de jours de renfort.
    `feux` : les départs de la période (toute l'année : ceux de novembre à février comptent au dénominateur)."""
    jours = pd.DatetimeIndex(jours)
    couvert = feux["date"].isin(jours)
    surface = feux["surface_parcourue_ha"]
    jours_avec_feu = int(jours.isin(feux["date"]).sum())
    return {
        "departs": int(len(feux)),
        "couverts": int(couvert.sum()),
        "taux": float(couvert.mean()) if len(feux) else float("nan"),
        "jours": int(len(jours)),
        "jours_avec_feu": jours_avec_feu,
        "precision": jours_avec_feu / len(jours) if len(jours) else float("nan"),
        "surface_couverte_ha": float(surface[couvert].sum()),
        "surface_totale_ha": float(surface.sum()),
        "feux_1ha_couverts": int((couvert & (surface >= 1)).sum()),
        "feux_1ha": int((surface >= 1).sum()),
    }


# ---------- les secteurs et leurs variables ----------

def secteurs(commune_maille, foret_commune):
    """Une ligne par secteur : sa forêt et sa part de résineux, (conifères + 0,5 × mixte) ÷ forêt avec couvert
    (journal du 20/11), et la version stricte sans la forêt mixte, gardée pour le test de sensibilité."""
    surfaces = ["surface_foret_ha", "surface_coniferes_ha", "surface_feuillus_ha", "surface_mixte_ha"]
    c = commune_maille[["code_commune_2026"] + CLE_SECTEUR].merge(
        foret_commune[["code_commune_2026"] + surfaces], on="code_commune_2026", how="left",
    ).fillna({k: 0.0 for k in surfaces})
    c["latitude"], c["longitude"] = c["latitude"].round(DECIMALES), c["longitude"].round(DECIMALES)
    s = c.groupby(CLE_SECTEUR)[surfaces].sum().reset_index()
    couvert = s["surface_coniferes_ha"] + s["surface_feuillus_ha"] + s["surface_mixte_ha"]
    avec = couvert > 0
    s["part_resineux"] = 0.0
    s["part_resineux_stricte"] = 0.0
    s.loc[avec, "part_resineux"] = (s["surface_coniferes_ha"] + 0.5 * s["surface_mixte_ha"])[avec] / couvert[avec]
    s.loc[avec, "part_resineux_stricte"] = s["surface_coniferes_ha"][avec] / couvert[avec]
    return s[CLE_SECTEUR + ["surface_foret_ha", "part_resineux", "part_resineux_stricte"]]


def feux_par_secteur(feux_travail, commune_maille):
    """Chaque départ avec son secteur. Le département est celui de la BDIFF."""
    m = commune_maille[["code_commune_2026", "latitude", "longitude"]].copy()
    m["latitude"], m["longitude"] = m["latitude"].round(DECIMALES), m["longitude"].round(DECIMALES)
    f = feux_travail.merge(m, on="code_commune_2026", how="left")
    if f["latitude"].isna().any():
        raise ValueError(f"{int(f['latitude'].isna().sum())} départs sans maille : commune absente de commune_maille.csv")
    f["date"] = pd.to_datetime(f["date"])
    f["annee"] = f["date"].dt.year
    return f


def annees_renseignees(jour_departement):
    """Les couples (département, année) où la BDIFF a au moins un feu saisi (règle P1)."""
    jd = jour_departement[jour_departement["statut_bdiff"] == "renseigné"]
    return set(zip(jd["departement"], pd.to_datetime(jd["date"]).dt.year))


def historique(secteurs_, feux, renseignees, annee):
    """Départs par an du secteur, sur les années renseignées de son département avant `annee` : connu avant la
    saison. Un département sans aucune année renseignée avant : le taux moyen du Grand Est par hectare de forêt,
    multiplié par la forêt du secteur (on ne met jamais 0 pour « non renseigné », règle P1)."""
    avant = {(d, a) for d, a in renseignees if a < annee}
    nb_annees = Counter(d for d, _ in avant)
    gardes = feux[[(d, a) in avant for d, a in zip(feux["departement"], feux["annee"])]]
    nb_feux = gardes.groupby(CLE_SECTEUR).size()

    s = secteurs_.set_index(CLE_SECTEUR)
    annees = pd.Series([nb_annees.get(d, 0) for d in s.index.get_level_values("departement")], index=s.index)
    departs = nb_feux.reindex(s.index, fill_value=0).astype(float)
    connus = annees > 0
    taux_ha = departs[connus].sum() / (s["surface_foret_ha"][connus] * annees[connus]).sum()
    taux = (departs / annees.where(connus, 1)).where(connus, taux_ha * s["surface_foret_ha"])
    return taux.rename("historique").reset_index()


def table_secteur_jour(secteurs_, fwi_maille, calendrier, feux, renseignees, annees, resineux="part_resineux"):
    """Une ligne par secteur et par jour de mars à octobre des `annees` : les variables et le nombre de départs."""
    annees = sorted(set(annees))
    fwi = fwi_maille.copy()
    fwi["date"] = pd.to_datetime(fwi["date"])
    fwi = fwi[fwi["date"].dt.year.isin(annees) & en_saison(fwi["date"])]
    fwi["latitude"], fwi["longitude"] = fwi["latitude"].round(DECIMALES), fwi["longitude"].round(DECIMALES)
    t = secteurs_.merge(fwi, on=["latitude", "longitude"], how="inner")
    t["annee"] = t["date"].dt.year

    cal = calendrier[["date", "departement", "week_end", "ferie", "vacances"]].copy()
    cal["date"] = pd.to_datetime(cal["date"])
    t = t.merge(cal, on=["date", "departement"], how="left")

    hist = pd.concat([historique(secteurs_, feux, renseignees, a).assign(annee=a) for a in annees])
    t = t.merge(hist, on=CLE_SECTEUR + ["annee"], how="left")

    n = feux.groupby(CLE_SECTEUR + ["date"]).size().rename("nb_departs").reset_index()
    t = t.merge(n, on=CLE_SECTEUR + ["date"], how="left").fillna({"nb_departs": 0})

    t["log_fwi"] = np.log1p(t["fwi"].clip(lower=0))
    t["week_end"] = t["week_end"].astype(str).eq("True").astype(float)
    t["ferie"] = t["ferie"].astype(str).eq("True").astype(float)
    t["vacances"] = t["vacances"].map({"oui": 1.0, "non": 0.0})  # « non renseigné » reste vide
    t["log_historique"] = np.log1p(t["historique"])
    t["part_resineux"] = t[resineux]
    t["renseigne"] = [(d, a) in renseignees for d, a in zip(t["departement"], t["annee"])]
    return t


# ---------- le modèle ----------

def caler_modele(table, variables):
    """Régression de Poisson du nombre de départs d'un secteur un jour donné, sur les lignes renseignées."""
    lignes = table[table["renseigne"] & table[variables].notna().all(axis=1)]
    m = PoissonRegressor(alpha=0.0, max_iter=3000, tol=1e-10).fit(lignes[variables].to_numpy(), lignes["nb_departs"])
    return {"variables": list(variables), "constante": float(m.intercept_),
            "coefficients": {v: float(c) for v, c in zip(variables, m.coef_)},
            "lignes": int(len(lignes)), "departs": int(lignes["nb_departs"].sum())}


def score_par_jour(table, modele):
    """Départs attendus dans le Grand Est chaque jour : somme sur tous les secteurs (renseignés ou non :
    le jour de la décision, on ne sait pas si l'année sera saisie)."""
    x = table[modele["variables"]].to_numpy()
    b = np.array([modele["coefficients"][v] for v in modele["variables"]])
    attendu = pd.Series(np.exp(modele["constante"] + x @ b), index=table["date"])
    score = attendu.groupby(level=0).sum()
    incomplet = attendu.isna().groupby(level=0).any()  # une variable inconnue dans un secteur : pas de score ce jour-là
    return score.mask(incomplet).sort_index()
