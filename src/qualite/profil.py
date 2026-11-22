"""Profil d'une table : ce qu'elle contient vraiment, colonne par colonne.

Le profil ne dit pas si la donnée est bonne, il dit ou chercher (cours du 18/11).
On regarde : le remplissage, le nb de valeurs distinctes, les bornes et les
valeurs de remplissage (des "0", "-999", "N/A" qui veulent souvent dire "manquant").
"""

import pandas as pd

# valeurs qui ne sont pas vides mais qui cachent souvent un manque
VALEURS_REMPLISSAGE = {"-999", "N/A", "NA", "n/a", "Unknown", "inconnu", "Inconnu"}


def _vide(serie):
    """True la ou la cellule est NULL ou une chaine vide."""
    return serie.isna() | (serie.astype(str).str.strip() == "")


def _bornes(valeurs, nom_colonne):
    """Min et max si la colonne est un nombre ou une date, sinon rien.

    Pour une colonne texte on n'affiche pas de valeur (ex : noms de communes),
    le profil est versionné et doit rester sans donnée identifiante.
    """
    if valeurs.empty:
        return "-", "-", "vide"
    # un code (08, 08022) a l'air d'un nombre mais perd son 0 si on le convertit
    if valeurs.str.fullmatch(r"\d+").all() and valeurs.str.startswith("0").any():
        return valeurs.min(), valeurs.max(), "code"
    nombres = pd.to_numeric(valeurs, errors="coerce")
    if nombres.notna().all():
        return f"{nombres.min():g}", f"{nombres.max():g}", "nombre"
    if "date" in nom_colonne.lower():
        dates = pd.to_datetime(valeurs, errors="coerce")
        if dates.notna().all():
            return str(dates.min().date()), str(dates.max().date()), "date"
    return "-", "-", "texte"


def profil(df):
    """Une ligne par colonne : type, remplissage, distinct, bornes, zéros, valeurs de remplissage."""
    lignes = []
    total = len(df)
    for colonne in df.columns:
        serie = df[colonne]
        vide = _vide(serie)
        valeurs = serie[~vide].astype(str).str.strip()
        mini, maxi, genre = _bornes(valeurs, colonne)
        lignes.append({
            "colonne": colonne,
            "type": genre,
            "remplies": int((~vide).sum()),
            "remplissage": round(100 * (~vide).sum() / total, 1) if total else 0.0,
            "distinctes": int(valeurs.nunique()),
            "min": mini,
            "max": maxi,
            "zéros": int((valeurs == "0").sum()),
            "valeurs de remplissage": int(valeurs.isin(VALEURS_REMPLISSAGE).sum()),
        })
    return pd.DataFrame(lignes)


def remplissage_par_groupe(df, colonne, groupe):
    """Taux de remplissage d'une colonne par segment (ex : la cause par département).

    97 % au global peut cacher 3 % sur le segment qui compte : on regarde par segment.
    """
    rempli = ~_vide(df[colonne])
    resultat = rempli.groupby(df[groupe]).agg(["sum", "count"])
    resultat.columns = ["remplies", "lignes"]
    resultat["remplissage"] = (100 * resultat["remplies"] / resultat["lignes"]).round(1)
    return resultat.reset_index()
