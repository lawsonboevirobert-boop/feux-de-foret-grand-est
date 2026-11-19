"""COG 2026 : la liste des communes et le passage des anciens codes vers les codes 2026.

Deux tables, voir docs/pipeline/plan-nettoyage.md (étape 1, COG) :
- communes.csv : 1 commune au 01/01/2026 (code, département, région). Pas de nom (minimisation)
- passage_communes.csv : 1 code (actuel, délégué, associé ou disparu depuis 2006) -> son code commune 2026

Règles de docs/qualite/regles.md :
- G1 : code commune sur 5 caractères, code département avec son 0
- G2 : un code des autres tables doit exister au COG 2026 après passage (vérifié plus tard, sur chaque source)
- passage univoque : un ancien code mène à une seule commune 2026. Sinon il est marqué ambigu
"""

import re

import pandas as pd

from .commun import BRUT

DEPUIS = "2006-01-01"  # la BDIFF commence en 2006 : les codes plus anciens ne nous servent pas

MOTIF_COMMUNE = re.compile(r"^(\d{5}|2[AB]\d{3})$")
MOTIF_DEPARTEMENT = re.compile(r"^(\d{2}|2[AB]|97\d)$")


def lire_cog(dossier=None, millesime=2026):
    """Lit les deux fichiers du COG, tout en texte pour garder les 0 (01001, 08)."""
    dossier = dossier or BRUT / "cog"
    communes = pd.read_csv(dossier / f"v_commune_{millesime}.csv", dtype=str, keep_default_na=False)
    mouvements = pd.read_csv(dossier / f"v_mvt_commune_{millesime}.csv", dtype=str, keep_default_na=False)
    return communes, mouvements


def table_communes(communes):
    """Les communes au sens strict (TYPECOM = COM) : sans les communes déléguées, plus de code en double."""
    com = communes[communes["TYPECOM"] == "COM"]
    return (com[["COM", "DEP", "REG"]]
            .rename(columns={"COM": "code_commune", "DEP": "departement", "REG": "region"})
            .sort_values("code_commune")
            .reset_index(drop=True))


def table_passage(communes, mouvements, depuis=DEPUIS):
    """Pour chaque code connu, la commune 2026 où il se trouve aujourd'hui.

    1. une commune 2026 donne son propre code
    2. une commune déléguée ou associée donne sa commune de rattachement (COMPARENT)
    3. un code disparu depuis `depuis` suit les mouvements COM_AV -> COM_AP jusqu'à une commune 2026
    Si un code mène à plusieurs communes 2026 (commune scindée), il est marqué ambigu, pas deviné.
    """
    actuelles = set(communes.loc[communes["TYPECOM"] == "COM", "COM"])
    cible = {code: {code} for code in actuelles}
    origine = {code: "commune 2026" for code in actuelles}

    rattachees = communes[communes["TYPECOM"].isin(["COMD", "COMA"]) & ~communes["COM"].isin(actuelles)]
    for code, parent in zip(rattachees["COM"], rattachees["COMPARENT"]):
        cible.setdefault(code, set()).add(parent)
        origine.setdefault(code, "déléguée ou associée")

    # successeurs directs de chaque code dans les mouvements récents. On ignore les lignes sans code
    # avant (création, ex : Mayotte en 2011) ou sans code après (sortie du COG, ex : Saint-Barthélemy en 2007)
    recents = mouvements[
        (mouvements["DATE_EFF"] >= depuis)
        & (mouvements["COM_AV"] != "")
        & (mouvements["COM_AP"] != "")
        & (mouvements["COM_AV"] != mouvements["COM_AP"])
    ]
    suivants = {}
    for avant, apres in zip(recents["COM_AV"], recents["COM_AP"]):
        suivants.setdefault(avant, set()).add(apres)

    def resoudre(code, vus=()):
        if code in actuelles:
            return {code}
        if code in cible:
            return cible[code]
        if code in vus or code not in suivants:
            return set()
        trouve = set()
        for apres in suivants[code]:
            trouve |= resoudre(apres, vus + (code,))
        return trouve

    for code in suivants:
        if code not in cible:
            trouve = resoudre(code)
            if trouve:
                cible[code] = trouve
                origine[code] = "disparu depuis " + depuis[:4]

    lignes = []
    for code in sorted(cible):
        codes_2026 = sorted(cible[code] & actuelles)
        lignes.append({
            "code_origine": code,
            "code_commune_2026": codes_2026[0] if len(codes_2026) == 1 else "",
            "statut": origine[code] if len(codes_2026) == 1 else "ambigu : " + " ".join(codes_2026),
        })
    return pd.DataFrame(lignes)


def controle_format(table, colonne_commune, colonne_departement=None):
    """G1 : nb de lignes dont le code commune (ou département) n'a pas le bon format."""
    mauvais = ~table[colonne_commune].str.match(MOTIF_COMMUNE)
    if colonne_departement:
        mauvais |= ~table[colonne_departement].str.match(MOTIF_DEPARTEMENT)
    return int(mauvais.sum())


def controle_unicite(table, colonne):
    """Nb de lignes dont le code apparaît plusieurs fois."""
    return int(table[colonne].duplicated(keep=False).sum())


def controle_ambigus(passage):
    """Nb d'anciens codes qui mènent à plusieurs communes 2026."""
    return int(passage["statut"].str.startswith("ambigu").sum())
