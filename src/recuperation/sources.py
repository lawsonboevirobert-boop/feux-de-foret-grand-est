"""Un script par source : chacun télécharge les fichiers bruts dans data/raw/<source>/.

Les pièges de chaque fichier (séparateurs, encodage, codes) sont décrits dans
docs/sources/fiche-*.md : ils sont traités au nettoyage (#37), pas ici.
"""

import os
import re
import shutil
import subprocess
import zipfile

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
        liste = requests.get(flux, params={"zone": f"D0{code}"}, timeout=60).text
        versions = re.findall(r"<title>(BDFORET_2-0__SHP_LAMB93_D0" + code + r"_[^<]+)</title>", liste)
        if not versions:
            print(f"  pas de BD Forêt V2 trouvée pour le {code}")
            continue
        nom = sorted(versions)[-1]
        page = requests.get(f"{flux}/{nom}", timeout=60).text
        lien = re.search(r'href="([^"]+\.7z)"', page)
        if not lien:
            print(f"  pas d'archive pour {nom}")
            continue
        archive = telecharger(lien.group(1), cible / f"{nom}.7z", forcer=forcer)
        decompresser_7z(archive, cible / nom)


def decompresser_7z(archive, destination):
    """Décompresse un .7z avec l'outil tar de Windows (il lit le format 7z)."""
    if destination.exists():
        return
    tar_windows = shutil.which("tar", path=os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32"))
    if not tar_windows:
        print(f"  décompression impossible, à faire à la main : {archive.name}")
        return
    destination.mkdir(parents=True)
    subprocess.run([tar_windows, "-xf", str(archive), "-C", str(destination)], check=True)
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
            "area": [50.2, 3.3, 47.4, 8.3],  # nord, ouest, sud, est : le Grand Est
        }
        client.retrieve("cems-fire-historical-v1", demande).download(str(fichier))
        print(f"  téléchargé : {fichier.relative_to(RACINE)}")
