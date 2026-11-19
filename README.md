# Feux de forêt - Grand Est

Projet de groupe HETIC 2026/2027, EU01 « Modélisation et pipeline de données ».

**Région : Grand Est** (10 départements : Ardennes, Aube, Marne, Haute-Marne, Meurthe-et-Moselle, Meuse, Moselle, Bas-Rhin, Haut-Rhin, Vosges).

## La commande

La direction du SDIS 67 (Bas-Rhin) prépare la saison feux 2027 et doit arbitrer deux points :

1. **où concentrer ses moyens**, humains comme financiers, pour lutter contre les départs de feu ;
2. **à partir de quel niveau de la Météo des forêts** déclencher le dispositif renforcé (patrouilles, guet).

Elle veut savoir comment l'indice se comporte dans le Bas-Rhin, dans les autres départements du Grand Est et au niveau national.
Réponse attendue le **11 décembre**.

## Équipe et rôles

| Membre | GitHub | Rôle | Responsable de |
|---|---|---|---|
| Lawson Robert | [@lawsonboevirobert-boop](https://github.com/lawsonboevirobert-boop) | Chef de projet + responsable sources | Dépôt, tickets, checkpoints, journal des décisions ; inventaire, fiches d'identité, matrice questions × sources |
| Denis Wilson-Bahun | [@wilsonDenis](https://github.com/wilsonDenis) | Responsable qualité et conformité | Règles de qualité, tests, données personnelles |
| Franck Kevin Tambou | [@FranckTambou](https://github.com/FranckTambou) | Responsable pipeline et modèle | Chargement, consolidation, entrepôt |
| Firas (firas.ja) | [@firasjaouahdoups3-glitch](https://github.com/firasjaouahdoups3-glitch) | Renfort pipeline et modèle (depuis le 18/11) | Nettoyage et consolidation des données, avec Franck |

Le chef de projet garde aussi la responsabilité des sources, même depuis l'arrivée d'un quatrième membre (voir le journal des décisions).
Un rôle ne limite pas le travail de chacun : le responsable d'un domaine relit et valide les tickets qui en relèvent.
Tout changement de rôle est consigné dans le [journal des décisions](docs/decisions.md).

## Organisation

- Les tâches sont suivies dans les [issues](../../issues), réparties dans [docs/organisation/repartition-taches.md](docs/organisation/repartition-taches.md).
- Une issue = une branche (`type/numero-sujet`, par exemple `docs/7-inventaire-sources`) = une pull request relue par un autre membre.
- La branche `main` est protégée : on n'y pousse pas directement.

## Installation

Il faut Python 3.13. Avec Python 3.15, plusieurs bibliothèques ne s'installent pas encore ou sont bloquées par Windows.

```
py -3.13 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Sous PowerShell, l'activation se fait avec `.venv\Scripts\Activate.ps1`. Si PowerShell la refuse, lancer d'abord `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` (valable seulement pour la fenêtre ouverte). Sous Git Bash : `source .venv/Scripts/activate`.

Sur Mac ou Linux :

```
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Les versions sont figées dans `requirements.txt`. Sur un Windows 11 où le Contrôle intelligent des applications est actif, les versions plus récentes de numpy, scikit-learn et netCDF4 sont bloquées (« Une stratégie de contrôle d'application a bloqué ce fichier ») : avant de monter une version, vérifier que l'import passe.

Arborescence :

| Dossier | Contenu | Sur GitHub ? |
|---|---|---|
| `data/raw/` | fichiers téléchargés tels quels | non |
| `data/processed/` | données nettoyées | non |
| `src/` | code (récupération, nettoyage, analyse) | oui |
| `notebooks/` | explorations | oui |
| `outputs/figures/` | graphiques produits | non |
| `docs/` | analyses, fiches sources, décisions | oui |

## Récupérer les données

Les données brutes ne sont pas sur GitHub : chacun les télécharge avec le script, depuis la racine du projet et avec l'environnement activé.

```
python -m src.recuperation                         # toutes les sources
python -m src.recuperation mdf sis cog             # seulement certaines
python -m src.recuperation bdforet --departements 67
python -m src.recuperation --forcer                # retélécharger
```

| Code | Source | Fichiers dans `data/raw/` |
|---|---|---|
| `mdf` | Archives de la Météo des forêts (2024 à aujourd'hui) | `meteo_des_forets/mdf_AAAA.csv.gz` |
| `sis` | Interventions des services d'incendie et de secours (2008-2024) | `interventions_sis/interventionsAAAA.csv` |
| `cog` | Code officiel géographique 2026 (communes, mouvements, départements) | `cog/` |
| `bdiff` | BDIFF, 10 départements du Grand Est, 2006-2025 | `bdiff/bdiff_grand_est_2006_2025/` |
| `bdforet` | BD Forêt V2, un shapefile par département | `bd_foret/` |
| `copernicus` | FWI quotidien de Copernicus sur le Grand Est, 2006-2026, un fichier par année | `copernicus/fwi_grand_est_AAAA.nc` |

Pour Copernicus, il faut un compte sur l'EWDS, avoir accepté la licence CC-BY du jeu, et mettre sa clé dans un fichier `.env` : copier `.env.example` en `.env` puis compléter. Le fichier `.env` n'est jamais commité.

Un fichier déjà présent n'est pas retéléchargé. Si une source est en panne, le script le signale et passe à la suivante. Les pièges de chaque fichier (séparateurs, encodage, codes) sont décrits dans les fiches `docs/sources/fiche-*.md` et sont traités au nettoyage.

## Documents

| Document | Contenu |
|---|---|
| [Analyse globale](docs/analyse/analyse-globale.md) | Questions, hypothèses, besoins et données idéales du groupe |
| [Analyses individuelles](docs/analyse/) | Analyse de la commande de chaque membre (partie B) |
| [Glossaire](docs/glossaire.md) | Termes de la commande et des analyses |
| [Journal des décisions](docs/decisions.md) | Choix du groupe, avec date et justification |
| [Inventaire des sources](docs/sources/inventaire.md) | Sources de données envisagées |
