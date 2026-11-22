"""Étape 2 du nettoyage : les tables de travail, croisées à partir des tables propres de l'étape 1.

Voir docs/pipeline/plan-nettoyage.md (partie 4).

- feux_travail.csv : 1 feu (hors doublons probables) + le type de jour et la saison. La maille FWI viendra
  avec la table commune -> maille de Franck (étape 5)
- jour_departement.csv : 1 jour × 1 département du Grand Est, 2006-2026. Le FWI moyen viendra à l'étape 5

Le piège de toutes ces jointures : un vide n'est pas un zéro.
- feux : 0 seulement si l'année est renseignée dans la BDIFF (P1). Année vide, ou 2026 (pas encore publiée) : vide
- niveau de danger : vide hors des saisons publiées (P2), jamais « faible » par défaut
- détections satellite : téléchargées pour 2026 seulement. Avant : vide, pas 0
"""

import pandas as pd

from ..qualite.regles import Controle, Regle

MOIS_SAISON = range(3, 11)  # saison feux du groupe : mars à octobre (glossaire)
ANNEE_FIRMS = 2026


def feux_travail(feux, calendrier):
    """Les feux gardés (hors doublons probables), avec le type de jour de leur département."""
    gardes = feux[~feux["doublon_probable"]].drop(columns="doublon_probable")
    jour = calendrier[["date", "departement", "jour_semaine", "week_end", "ferie", "vacances"]]
    table = gardes.merge(jour, on=["date", "departement"], how="left", validate="many_to_one")
    table["saison"] = pd.to_datetime(table["date"]).dt.month.isin(MOIS_SAISON)
    return table


def jour_departement(calendrier, feux, population, mdf, firms, firms_jusqu_au=None, fwi=None):
    """firms : table commune × jour de FIRMS, ou None si FIRMS n'a pas été téléchargé (il faut une clé).
    firms_jusqu_au : dernier jour téléchargé. Après ce jour, pas de détection = inconnu (vide), pas 0.
    fwi : FWI moyen par jour et par département (copernicus.fwi_departement), ou None sans fichiers Copernicus.
    """
    table = calendrier[["date", "departement", "jour_semaine", "week_end", "ferie", "vacances"]].copy()
    table["annee"] = table["date"].str[:4].astype(int)
    table["saison"] = pd.to_datetime(table["date"]).dt.month.isin(MOIS_SAISON)

    # niveau de la Météo des forêts prévu la veille (déjà décalé à J+1 dans meteo_des_forets.csv)
    niveau = mdf[["date", "departement", "niveau"]]
    table = table.merge(niveau, on=["date", "departement"], how="left", validate="one_to_one")
    table["niveau"] = pd.to_numeric(table["niveau"]).astype("Int64")  # entier, vide hors saison (pas 1.0)

    # feux : 0 un jour sans feu d'une année renseignée, vide sinon
    gardes = feux[~feux["doublon_probable"]]
    par_jour = gardes.groupby(["date", "departement"]).agg(
        nb_feux=("id_feu", "size"),
        surface_parcourue_ha=("surface_parcourue_ha", "sum"),
        surface_foret_ha=("surface_foret_ha", "sum"),
    ).reset_index()
    table = table.merge(par_jour, on=["date", "departement"], how="left", validate="one_to_one")
    statut = population[["departement", "annee", "statut_bdiff"]].astype({"annee": int})
    table = table.merge(statut, on=["departement", "annee"], how="left", validate="many_to_one")
    table["statut_bdiff"] = table["statut_bdiff"].fillna("non publié")  # 2026 : la BDIFF s'arrête à l'année d'avant
    renseigne = table["statut_bdiff"] == "renseigné"
    for colonne in ("nb_feux", "surface_parcourue_ha", "surface_foret_ha"):
        table[colonne] = table[colonne].where(~renseigne | table[colonne].notna(), 0)
        table.loc[~renseigne, colonne] = pd.NA
    table["nb_feux"] = table["nb_feux"].astype("Int64")

    # détections satellite (2026 seulement) : jamais comptées comme des départs de feu (N5).
    # 0 seulement les jours téléchargés ; sans FIRMS, ou après le dernier jour téléchargé : vide
    if firms is None:
        firms = pd.DataFrame({"date": [], "departement": [], "nb_detections": [], "code_commune_2026": []}, dtype=str)
        fin = None
    else:
        fin = firms_jusqu_au or (firms["date"].max() if len(firms) else None)
    det = firms.groupby(["date", "departement"]).agg(
        nb_detections_satellite=("nb_detections", "sum"),
        nb_communes_detection=("code_commune_2026", "nunique"),
    ).reset_index()
    table = table.merge(det, on=["date", "departement"], how="left", validate="one_to_one")
    couvert = (table["annee"] == ANNEE_FIRMS) & (table["date"] <= fin) if fin else pd.Series(False, index=table.index)
    for colonne in ("nb_detections_satellite", "nb_communes_detection"):
        table[colonne] = table[colonne].where(~couvert | table[colonne].notna(), 0)
        table[colonne] = table[colonne].astype("Int64")

    # FWI de Copernicus (étape 5) : moyenne sur les communes, pondérée par la forêt, et moyenne simple à côté.
    # Vide sans fichiers Copernicus, et les jours hors des années téléchargées
    if fwi is None:
        fwi = pd.DataFrame({"date": [], "departement": [], "fwi_moyen": [], "fwi_moyen_simple": []})
    table = table.merge(fwi[["date", "departement", "fwi_moyen", "fwi_moyen_simple"]],
                        on=["date", "departement"], how="left", validate="one_to_one")
    return table.drop(columns="annee")


def regles_jour_departement(feux, nb_jours_calendrier, jours_fwi=()):
    """Règles de jointure : rien ne se perd, rien ne se double.

    jours_fwi : les dates couvertes par les fichiers FWI. Chacune doit avoir un FWI dans chaque département (T7).
    """
    feux_attendus = int((~feux["doublon_probable"]).sum())
    jours_fwi = set(jours_fwi)
    return [
        Regle(
            id="T1", dimension="unicité", portee="jour_departement.csv, jour × département",
            controle=lambda t: Controle(int(t.duplicated(["date", "departement"], keep=False).sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : une jointure a doublé des lignes",
        ),
        Regle(
            id="T2", dimension="complétude (population)", portee="jour_departement.csv, autant de lignes que le calendrier",
            controle=lambda t: Controle(abs(len(t) - nb_jours_calendrier), nb_jours_calendrier),
            seuil=0.0, severite="bloquer",
            decision="on arrête : des jours ont été perdus ou ajoutés à la jointure",
        ),
        Regle(
            id="T3", dimension="cohérence", portee="jour_departement.csv, total des feux = feux.csv hors doublons",
            controle=lambda t: Controle(abs(int(t["nb_feux"].sum()) - feux_attendus), feux_attendus,
                                        "feux perdus ou comptés 2 fois entre feux.csv et la table"),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un feu perdu à la jointure fausse tous les taux",
        ),
        Regle(
            id="T4", dimension="cohérence", portee="jour_departement.csv, 0 feu seulement les années renseignées (P1)",
            controle=lambda t: Controle(int(((t["statut_bdiff"] != "renseigné") & t["nb_feux"].notna()).sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : une année non renseignée ne doit jamais valoir 0 feu",
        ),
        Regle(
            id="T5", dimension="cohérence", portee="jour_departement.csv, niveau de danger seulement les jours publiés (P2)",
            controle=lambda t: Controle(int((t["niveau"].notna() & (t["date"] < "2024-06-01")).sum()), len(t)),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un niveau avant les archives de la Météo des forêts serait inventé",
        ),
        Regle(
            id="T7", dimension="complétude (cellule)", portee="jour_departement.csv, FWI moyen les jours couverts par Copernicus",
            controle=lambda t: Controle(int((t["date"].isin(jours_fwi) & t["fwi_moyen"].isna()).sum()),
                                        int(t["date"].isin(jours_fwi).sum()), "jours couverts sans FWI moyen"),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un département sans FWI un jour couvert veut dire une maille ou une forêt perdue à la jointure",
        ),
    ]


def regles_feux_travail(nb_feux_gardes):
    return [
        Regle(
            id="T6", dimension="complétude (population)", portee="feux_travail.csv, chaque feu a son type de jour",
            controle=lambda t: Controle(int(t["jour_semaine"].isna().sum()) + abs(len(t) - nb_feux_gardes), nb_feux_gardes),
            seuil=0.0, severite="bloquer",
            decision="on arrête : un feu sans jour du calendrier a une date hors de la période ou un département inconnu",
        ),
    ]
