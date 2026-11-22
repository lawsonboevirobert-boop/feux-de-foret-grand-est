"""Les tables de l'étoile et leurs règles (E1 à E5).

Faits :
- fait_feu : 1 feu de la BDIFF, sans les doublons probables (règle B3)
- fait_jour_departement : 1 jour × 1 département du Grand Est, 2006-2026

Dimensions : dim_date, dim_departement, dim_commune, dim_maille, dim_niveau, dim_cause.
Historisation :
- dim_commune_historique garde les anciens codes des communes (fusions depuis 2006) et la date où ils
  ont cessé d'être une commune. fait_feu garde le code du jour du feu (`code_commune_origine`) et le code 2026
- fait_feu n'est jamais réécrit : un feu déjà chargé garde sa date de chargement, un nouveau feu
  (BDIFF 2026, saison 2027) arrive avec la date du jour

Pas de nom de commune (minimisation, plan de nettoyage) : Power BI le prend dans le COG s'il en a besoin.
Les vides restent vides : une année « non renseigné » n'a pas de nb_feux (règle P1), un jour hors
saison n'a pas de niveau (P2).
"""

import pandas as pd

from ..nettoyage.calendrier import ACADEMIES, ALSACE_MOSELLE
from ..nettoyage.tables import MOIS_SAISON
from ..qualite.regles import Controle, Regle

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
        "novembre", "décembre"]
NIVEAUX = {1: "faible", 2: "modéré", 3: "élevé", 4: "très élevé"}
ORIGINE = {
    "Malveillance": "humaine",
    "Involontaire (travaux)": "humaine",
    "Involontaire (particulier)": "humaine",
    "Accidentelle": "humaine",
    "Naturelle": "naturelle",
    "inconnue": "inconnue",
}


def id_maille(latitude, longitude):
    """Une seule colonne pour la clé de maille (Power BI ne relie que sur une colonne) : 48.50_7.75."""
    return latitude.map("{:.2f}".format) + "_" + longitude.map("{:.2f}".format)


def dim_date(calendrier):
    jours = calendrier[["date", "jour_semaine", "week_end"]].drop_duplicates("date").copy()
    d = pd.to_datetime(jours["date"])
    jours["annee"] = d.dt.year
    jours["mois"] = d.dt.month
    jours["nom_mois"] = d.dt.month.map(lambda m: MOIS[m - 1])
    jours["saison"] = d.dt.month.isin(MOIS_SAISON)
    colonnes = ["date", "annee", "mois", "nom_mois", "jour_semaine", "week_end", "saison"]
    return jours[colonnes].sort_values("date").reset_index(drop=True)


def dim_departement(departements_cog, region="44"):
    dep = departements_cog[departements_cog["REG"] == region]
    table = pd.DataFrame({"departement": dep["DEP"], "nom": dep["LIBELLE"], "region": dep["REG"]})
    academie = {d: a for a, deps in ACADEMIES.items() for d in deps}
    table["academie"] = table["departement"].map(academie)
    table["zone_feries"] = table["departement"].map(lambda d: "Alsace-Moselle" if d in ALSACE_MOSELLE else "métropole")
    return table.sort_values("departement").reset_index(drop=True)


def dim_maille(commune_maille):
    m = commune_maille.groupby(["latitude", "longitude"]).size().rename("nb_communes").reset_index()
    m.insert(0, "id_maille", id_maille(m["latitude"], m["longitude"]))
    return m.sort_values("id_maille").reset_index(drop=True)


def dim_commune(commune_maille, foret):
    table = commune_maille[["code_commune_2026", "departement", "latitude", "longitude"]].copy()
    table["id_maille"] = id_maille(table["latitude"], table["longitude"])
    colonnes_foret = ["surface_commune_ha", "surface_foret_ha", "part_foret", "part_resineux",
                      "part_resineux_stricte", "edition_bd_foret"]
    table = table.drop(columns=["latitude", "longitude"]).merge(
        foret[["code_commune_2026"] + colonnes_foret], on="code_commune_2026", how="left", validate="one_to_one")
    return table.sort_values("code_commune_2026").reset_index(drop=True)


def dim_commune_historique(passage, mouvements, communes_etoile):
    """Chaque code connu d'une commune du Grand Est -> son code 2026, et jusqu'à quand il a été une commune."""
    table = passage[passage["code_commune_2026"].isin(communes_etoile)].copy()
    sortie = mouvements[(mouvements["COM_AV"] != mouvements["COM_AP"]) & (mouvements["COM_AP"] != "")]
    fin = sortie.groupby("COM_AV")["DATE_EFF"].max()
    table["commune_jusqu_au"] = table["code_origine"].map(fin).where(table["statut"] != "commune 2026", "")
    table["commune_jusqu_au"] = table["commune_jusqu_au"].fillna("")
    return table.sort_values("code_origine").reset_index(drop=True)


def dim_niveau():
    return pd.DataFrame({"niveau": list(NIVEAUX), "libelle": list(NIVEAUX.values())})


def dim_cause(feux):
    causes = sorted(set(feux["cause"]) | set(ORIGINE))
    return pd.DataFrame({"cause": causes, "origine": [ORIGINE.get(c, "inconnue") for c in causes]})


def fait_feu(feux, aujourd_hui, precedent=None):
    """Les feux gardés. Un feu déjà chargé garde sa date de chargement (les faits ne sont pas réécrits)."""
    gardes = feux[~feux["doublon_probable"]]
    colonnes = ["id_feu", "date", "heure", "departement", "code_commune_2026", "code_commune_origine", "cause",
                "surface_parcourue_ha", "surface_foret_ha", "precision"]
    table = gardes[colonnes].copy()
    deja = {} if precedent is None else dict(zip(precedent["id_feu"], precedent["date_chargement"]))
    table["date_chargement"] = [deja.get(i, aujourd_hui) for i in table["id_feu"]]
    return table.sort_values(["date", "id_feu"]).reset_index(drop=True)


def fait_jour_departement(jour):
    colonnes = ["date", "departement", "niveau", "ferie", "vacances", "statut_bdiff", "nb_feux",
                "surface_parcourue_ha", "surface_foret_ha", "nb_detections_satellite", "nb_communes_detection",
                "fwi_moyen"]
    table = jour[colonnes].copy()
    table["niveau"] = table["niveau"].astype("Int64")  # sort en décimal du nettoyage (remarque de Denis, #76)
    return table.sort_values(["date", "departement"]).reset_index(drop=True)


# --- règles : `t` est le dictionnaire des tables de l'étoile (plus `feux`, la table du nettoyage) ---

CLES = {
    "dim_date": ["date"],
    "dim_departement": ["departement"],
    "dim_commune": ["code_commune_2026"],
    "dim_maille": ["id_maille"],
    "dim_niveau": ["niveau"],
    "dim_cause": ["cause"],
    "dim_commune_historique": ["code_origine"],
    "fait_feu": ["id_feu"],
    "fait_jour_departement": ["date", "departement"],
}

# (table, colonne) -> (dimension, clé). Une valeur vide n'est pas contrôlée : niveau hors saison (P2)
LIENS = {
    ("fait_feu", "date"): ("dim_date", "date"),
    ("fait_feu", "departement"): ("dim_departement", "departement"),
    ("fait_feu", "code_commune_2026"): ("dim_commune", "code_commune_2026"),
    ("fait_feu", "cause"): ("dim_cause", "cause"),
    ("fait_jour_departement", "date"): ("dim_date", "date"),
    ("fait_jour_departement", "departement"): ("dim_departement", "departement"),
    ("fait_jour_departement", "niveau"): ("dim_niveau", "niveau"),
    ("dim_commune", "departement"): ("dim_departement", "departement"),
    ("dim_commune", "id_maille"): ("dim_maille", "id_maille"),
    ("dim_commune_historique", "code_commune_2026"): ("dim_commune", "code_commune_2026"),
}


def cles_en_double(t):
    return sum(int(t[nom].duplicated(cle).sum()) for nom, cle in CLES.items())


def cles_orphelines(t):
    """Nombre de valeurs d'une clé étrangère qui n'existent pas dans leur dimension."""
    total = 0
    for (table, colonne), (dim, cle) in LIENS.items():
        valeurs = t[table][colonne].dropna()
        total += int((~valeurs.isin(set(t[dim][cle]))).sum())
    return total


def ecart_feux(t):
    """E3 : même nombre de feux et même surface que feux.csv hors doublons."""
    gardes = t["feux"][~t["feux"]["doublon_probable"]]
    surface = abs(t["fait_feu"]["surface_parcourue_ha"].sum() - gardes["surface_parcourue_ha"].sum()) > 0.01
    return abs(len(t["fait_feu"]) - len(gardes)) + int(surface)


def zeros_inventes(t):
    """E4 : un jour d'une année « non renseigné » n'a jamais de nb_feux (pas de 0 inventé, règle P1)."""
    j = t["fait_jour_departement"]
    return int((j["statut_bdiff"].eq("non renseigné") & j["nb_feux"].notna()).sum())


def regles_etoile():
    return [
        Regle(
            id="E1", dimension="unicité", portee="étoile, la clé de chaque dimension et de chaque fait",
            controle=lambda t: Controle(cles_en_double(t), sum(len(t[n]) for n in CLES), "clés en double"),
            seuil=0.0, severite="bloquer",
            decision="on arrête : une clé en double compte 2 fois les faits qui la regardent",
        ),
        Regle(
            id="E2", dimension="intégrité", portee="étoile, chaque clé étrangère existe dans sa dimension",
            controle=lambda t: Controle(cles_orphelines(t), sum(len(t[tb]) for tb, _ in LIENS), "clés sans dimension"),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un fait sans dimension disparaît des filtres de Power BI",
        ),
        Regle(
            id="E3", dimension="exactitude", portee="fait_feu, même nombre de feux et même surface que feux.csv",
            controle=lambda t: Controle(ecart_feux(t), len(t["fait_feu"])),
            seuil=0.0, severite="bloquer",
            decision="on arrête : l'étoile ne doit ni perdre ni ajouter de feu",
        ),
        Regle(
            id="E4", dimension="validité", portee="fait_jour_departement, pas de 0 inventé (règle P1)",
            controle=lambda t: Controle(zeros_inventes(t), len(t["fait_jour_departement"]),
                                        "jours d'une année non renseignée avec un nb_feux"),
            seuil=0.0, severite="bloquer",
            decision="on arrête : une année vide lue comme 0 feu fausse toutes les moyennes",
        ),
        Regle(
            id="E5", dimension="complétude", portee="fait_jour_departement, FWI moyen rempli",
            controle=lambda t: Controle(int(t["fait_jour_departement"]["fwi_moyen"].isna().sum()),
                                        len(t["fait_jour_departement"]), "jours sans FWI moyen"),
            seuil=0.0, severite="alerter",
            decision="on continue : le FWI moyen arrive avec l'étape 5 du nettoyage, il suffira de relancer",
        ),
    ]
