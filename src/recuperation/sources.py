"""Un script par source : chacun télécharge les fichiers bruts dans data/raw/<source>/.

Les pièges de chaque fichier (séparateurs, encodage, codes) sont décrits dans
docs/sources/fiche-*.md : ils sont traités au nettoyage (#37), pas ici.
"""

import os
import re
import shutil
import zipfile

import py7zr
import requests
from dotenv import load_dotenv

from .commun import (
    DEPARTEMENTS_GRAND_EST,
    RACINE,
    dossier,
    ressources_data_gouv,
    telecharger,
)


def meteo_des_forets(forcer=False):
    """Archives de la Météo des forêts : un CSV compressé par année (depuis 2024)."""
    cible = dossier("meteo_des_forets")
    for titre, url in ressources_data_gouv("692f01d38fef6c5815d9262a"):
        annee = re.fullmatch(r"mdf\.(\d{4})", titre.strip())
        if annee:
            telecharger(url, cible / f"mdf_{annee.group(1)}.csv.gz", forcer=forcer)


def interventions_sis(forcer=False):
    """Interventions des services d'incendie et de secours : un CSV par année (2008-2024)."""
    cible = dossier("interventions_sis")
    for titre, url in ressources_data_gouv("53699736a3a729239d204c29"):
        annee = re.search(r"(\d{4})\s*$", titre)
        if annee:
            telecharger(url, cible / f"interventions{annee.group(1)}.csv", forcer=forcer)


def cog(millesime=2026, forcer=False):
    """Code officiel géographique de l'INSEE : communes, mouvements et départements."""
    cible = dossier("cog")
    voulus = {f"v_commune_{millesime}.csv", f"v_mvt_commune_{millesime}.csv", f"v_departement_{millesime}.csv"}
    trouves = set()
    for _, url in ressources_data_gouv("code-officiel-geographique-1"):
        nom = url.rsplit("/", 1)[-1]
        if nom in voulus:
            telecharger(url, cible / nom, forcer=forcer)
            trouves.add(nom)
    for manquant in sorted(voulus - trouves):
        print(f"  introuvable sur data.gouv.fr : {manquant}")


def bdiff(annee_debut=2006, annee_fin=2025, departements=DEPARTEMENTS_GRAND_EST, forcer=False):
    """BDIFF : on lance la recherche sur le site, puis on récupère l'export CSV (ZIP)."""
    cible = dossier("bdiff")
    zone = "grand_est" if sorted(departements) == DEPARTEMENTS_GRAND_EST else "-".join(departements)
    archive = cible / f"bdiff_{zone}_{annee_debut}_{annee_fin}.zip"
    if archive.exists() and not forcer:
        print(f"  déjà présent : {archive.relative_to(RACINE)}")
    else:
        site = "https://bdiff.agriculture.gouv.fr/incendies"
        with requests.Session() as session:
            recherche = session.get(site, timeout=120, params={
                "if[periodeAnnees][anneeDeb]": annee_debut,
                "if[periodeAnnees][anneeFin]": annee_fin,
                "if[deprts][value]": ",".join(departements),
                "if[submit]": "",
            })
            recherche.raise_for_status()
            nombre = re.search(r"([\d\s\u202f\u00a0]+)\s+incendies", recherche.text)
            if nombre:
                print(f"  recherche BDIFF : {re.sub(r'\D', '', nombre.group(1))} incendies")
            telecharger(site + "/zip", archive, session=session, forcer=True)
    with zipfile.ZipFile(archive) as contenu:
        contenu.extractall(archive.with_suffix(""))


def bd_foret(departements=DEPARTEMENTS_GRAND_EST, forcer=False):
    """BD Forêt V2 de l'IGN : une archive 7z (shapefile) par département, décompressée."""
    cible = dossier("bd_foret")
    flux = "https://data.geopf.fr/telechargement/resource/BDFORET"
    for code in departements:
        reponse = requests.get(flux, params={"zone": f"D0{code}"}, timeout=60)
        reponse.raise_for_status()  # site en panne : une erreur, pas « pas de BD Forêt »
        liste = reponse.text
        versions = re.findall(r"<title>(BDFORET_2-0__SHP_LAMB93_D0" + code + r"_[^<]+)</title>", liste)
        if not versions:
            print(f"  pas de BD Forêt V2 trouvée pour le {code}")
            continue
        nom = sorted(versions)[-1]
        reponse = requests.get(f"{flux}/{nom}", timeout=60)
        reponse.raise_for_status()
        page = reponse.text
        lien = re.search(r'href="([^"]+\.7z)"', page)
        if not lien:
            print(f"  pas d'archive pour {nom}")
            continue
        archive = telecharger(lien.group(1), cible / f"{nom}.7z", forcer=forcer)
        decompresser_7z(archive, cible / nom)


def decompresser_7z(archive, destination):
    """Décompresse un .7z avec py7zr : marche sous Windows 10 et 11, Mac et Linux.

    On décompresse d'abord dans un dossier .part : si ça plante, le dossier final
    n'existe pas et le lancement suivant recommence.
    """
    if destination.exists():
        if any(destination.iterdir()):
            return
        destination.rmdir()  # dossier vide laissé par une décompression ratée
    temporaire = destination.with_name(destination.name + ".part")
    shutil.rmtree(temporaire, ignore_errors=True)
    with py7zr.SevenZipFile(archive) as contenu:
        contenu.extractall(temporaire)
    temporaire.rename(destination)
    print(f"  décompressé : {destination.relative_to(RACINE)}")


def copernicus_fwi(annee_debut=2006, annee_fin=2026, forcer=False):
    """FWI quotidien de Copernicus sur le Grand Est, un fichier par année.

    Copernicus refuse les demandes trop grosses (« cost limits exceeded ») : on demande
    donc une année à la fois. La clé d'API est lue dans le fichier .env.
    """
    import cdsapi

    load_dotenv(RACINE / ".env")
    if not os.environ.get("CDSAPI_KEY"):
        print("  pas de clé CDSAPI_KEY dans .env : voir .env.example")
        return
    cible = dossier("copernicus")
    client = cdsapi.Client(quiet=True)
    en_erreur = []
    for annee in range(annee_debut, annee_fin + 1):
        fichier = cible / f"fwi_grand_est_{annee}.nc"
        if fichier.exists() and not forcer:
            print(f"  déjà présent : {fichier.relative_to(RACINE)}")
            continue
        demande = {
            "product_type": ["reanalysis"],
            "variable": ["fire_weather_index"],
            "dataset_type": "consolidated_dataset",
            "system_version": ["4_1"],
            "year": [str(annee)],
            "month": [f"{m:02d}" for m in range(1, 13)],
            "day": [f"{j:02d}" for j in range(1, 32)],
            "grid": "0.25/0.25",
            "data_format": "netcdf",
            # nord, ouest, sud, est : le Grand Est. Les bords tombent sur la grille d'origine
            # (multiples de 0,25°), sinon le serveur recalcule les valeurs sur une grille décalée.
            "area": [50.25, 3.25, 47.25, 8.5],
        }
        # On écrit d'abord dans un .part : un téléchargement coupé ne compte pas comme « déjà présent ».
        temporaire = fichier.with_suffix(fichier.suffix + ".part")
        try:
            client.retrieve("cems-fire-historical-v1", demande).download(str(temporaire))
        except Exception as erreur:  # une année en panne ne bloque pas les suivantes
            print(f"  ERREUR {annee} : {erreur}")
            en_erreur.append(annee)
            continue
        temporaire.replace(fichier)
        print(f"  téléchargé : {fichier.relative_to(RACINE)}")
    if en_erreur:
        raise RuntimeError(f"années non téléchargées : {', '.join(map(str, en_erreur))}")


def jours_feries(forcer=False):
    """Jours fériés (calendrier.api.gouv.fr) : zone Alsace-Moselle (57, 67, 68) et métropole (les 7 autres)."""
    cible = dossier("jours_feries")
    for zone in ("alsace-moselle", "metropole"):
        telecharger(f"https://calendrier.api.gouv.fr/jours-feries/{zone}.json", cible / f"{zone}.json", forcer=forcer)


def calendrier_scolaire(forcer=False):
    """Vacances scolaires (data.education.gouv.fr), toutes les académies, en un CSV (séparateur ;)."""
    cible = dossier("calendrier_scolaire")
    url = ("https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/"
           "fr-en-calendrier-scolaire/exports/csv?delimiter=%3B")
    telecharger(url, cible / "fr-en-calendrier-scolaire.csv", forcer=forcer)  # arrive en gzip, requests le décompresse


FIRMS_API = "https://firms.modaps.eosdis.nasa.gov/api"
FIRMS_RECTANGLE = "3.38,47.42,8.24,50.17"  # ouest, sud, est, nord : le Grand Est, qui déborde sur 4 pays (N8)
FIRMS_SATELLITES = ["MODIS", "VIIRS_SNPP", "VIIRS_NOAA20", "VIIRS_NOAA21"]
FIRMS_JOURS_PAR_APPEL = 5  # l'API refuse plus de 5 jours par appel


def firms(annee=2026, forcer=False):
    """Détections satellite NASA FIRMS sur le Grand Est, un CSV par satellite pour l'année.

    N9 : pour chaque satellite, la version SP (retraitée) tant qu'elle existe, puis la NRT (temps réel)
    après sa dernière date. Jamais les deux sur le même jour. La colonne `traitement` dit laquelle
    (la colonne `version` du fichier est celle de la NASA, ex : 6.1NRT, on n'y touche pas).
    La clé (gratuite, reçue par e-mail) est lue dans .env : FIRMS_MAP_KEY.
    """
    import datetime as dt
    import io

    import pandas as pd

    load_dotenv(RACINE / ".env")
    cle = os.environ.get("FIRMS_MAP_KEY", "").strip()
    if not cle:
        # comme Copernicus : sans clé on prévient et on continue. FIRMS est optionnel (le nettoyage s'en passe)
        print("  pas de clé FIRMS_MAP_KEY dans .env : FIRMS sauté (optionnel, voir .env.example)")
        return
    cible = dossier("firms")

    dispo = pd.read_csv(io.StringIO(requests.get(f"{FIRMS_API}/data_availability/csv/{cle}/all", timeout=60).text))
    dispo = {r.data_id: (dt.date.fromisoformat(r.min_date), dt.date.fromisoformat(r.max_date)) for r in dispo.itertuples()}
    debut, fin = dt.date(annee, 1, 1), min(dt.date(annee, 12, 31), dt.date.today())

    for satellite in FIRMS_SATELLITES:
        fichier = cible / f"firms_{satellite.lower()}_{annee}.csv"
        if fichier.exists() and not forcer:
            print(f"  déjà présent : {fichier.relative_to(RACINE)}")
            continue
        periodes = []
        fin_sp = debut - dt.timedelta(days=1)
        if f"{satellite}_SP" in dispo:
            fin_sp = min(fin, dispo[f"{satellite}_SP"][1])
            if fin_sp >= debut:
                periodes.append((f"{satellite}_SP", debut, fin_sp))
        if f"{satellite}_NRT" in dispo:
            nrt_min, nrt_max = dispo[f"{satellite}_NRT"]
            depart = max(fin_sp + dt.timedelta(days=1), nrt_min, debut)
            if min(fin, nrt_max) >= depart:
                periodes.append((f"{satellite}_NRT", depart, min(fin, nrt_max)))

        morceaux = []
        for version, du, au in periodes:
            jour = du
            while jour <= au:
                nb = min(FIRMS_JOURS_PAR_APPEL, (au - jour).days + 1)
                reponse = requests.get(f"{FIRMS_API}/area/csv/{cle}/{version}/{FIRMS_RECTANGLE}/{nb}/{jour}", timeout=120)
                reponse.raise_for_status()
                if not reponse.text.startswith("latitude"):
                    raise RuntimeError(f"réponse inattendue de FIRMS ({version} {jour}) : {reponse.text[:100]}")
                morceau = pd.read_csv(io.StringIO(reponse.text), dtype=str)
                morceaux.append(morceau.assign(traitement=version.rsplit("_", 1)[1]))
                jour += dt.timedelta(days=nb)

        table = pd.concat(morceaux, ignore_index=True) if morceaux else pd.DataFrame()
        temporaire = fichier.with_suffix(".csv.part")
        table.to_csv(temporaire, index=False)
        temporaire.replace(fichier)
        # La couverture dit jusqu'à quel jour on a regardé : après, « pas de détection » ne veut pas dire 0
        couverture = pd.DataFrame(
            [{"satellite": satellite, "traitement": v.rsplit("_", 1)[1], "du": d, "au": a} for v, d, a in periodes]
        )
        couverture.to_csv(cible / f"couverture_{fichier.name}", index=False)
        resume = ", ".join(f"{v.rsplit('_', 1)[1]} du {d} au {a}" for v, d, a in periodes)
        print(f"  téléchargé : {fichier.relative_to(RACINE)} ({len(table)} détections ; {resume})")


def contours_communes(departements=DEPARTEMENTS_GRAND_EST, forcer=False):
    """Contours des communes (geo.api.gouv.fr, COG de l'année), un GeoJSON par département, en WGS84.

    Sert à rattacher un point (détection FIRMS) à sa commune, et à la table commune -> maille.
    """
    cible = dossier("contours_communes")
    for code in departements:
        url = (f"https://geo.api.gouv.fr/departements/{code}/communes"
               "?format=geojson&geometry=contour&fields=code,codeDepartement")
        telecharger(url, cible / f"communes_{code}.geojson", forcer=forcer)
