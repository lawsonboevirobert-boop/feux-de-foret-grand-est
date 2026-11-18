# Fiche source : indices de danger feu historiques Copernicus (CEMS, dont le FWI)

Explorée par : @wilsonDenis, le 2026-11-18
Lien : https://ewds.climate.copernicus.eu/datasets/cems-fire-historical-v1
Fichier ouvert : `fwi_grand-est_2025.nc` et `fwi_grand-est_2016.nc` (téléchargés via l'API, rangés en local dans `data/raw/copernicus/`, pas sur le dépôt)

Pour refaire le téléchargement : compte gratuit sur le site EWDS + accepter la licence en bas de l'onglet Download, puis requête avec :
product_type `reanalysis`, variable `fire_weather_index`, dataset_type `consolidated_dataset`, system_version `4_1`, grille `0.25/0.25`, format `netcdf`, zone nord 50.25 / ouest 3.25 / sud 47.25 / est 8.5 (boite autour du Grand Est), une année entière par requête.
La clé API va dans le `.env` (ignoré par git), jamais dans un fichier du dépôt.

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | Copernicus Emergency Management Service (CEMS), géré par le JRC (Commission européenne). Calcul fait par l'ECMWF pour EFFIS, a partir de la réanalyse météo ERA5. Site de diffusion : EWDS (CEMS Early Warning Data Store) |
| Mode d'accès (export, API, téléchargement) et format | formulaire sur le site ou API (client python `ecmwf-datastores-client`), compte gratuit obligatoire. GRIB ou NetCDF (NetCDF marqué "experimental" mais il s'ouvre sans souci avec xarray). Une requête = une liste de jours x une zone |
| Grain (une ligne = ?) | 1 jour x 1 maille de 0,25° (environ 28 km nord-sud sur 18 km est-ouest chez nous). Pas une ligne mais une grille : 13 latitudes x 22 longitudes pour notre boite = 286 mailles. Heure de référence de la valeur (midi ?) : non vérifiée, pas trouvée dans le fichier (les dates sont a 00:00) |
| Emprise géographique | monde entier. Notre boite déborde un peu sur la Belgique, le Luxembourg et l'Allemagne |
| Période réellement couverte par les données | catalogue : du 03/01/1940 au 14/11/2026. Nos fichiers : 01/01 au 31/12 pour 2016 (366 jours) et 2025 (365 jours), aucun jour manquant |
| Date de dernière mise à jour affichée sur la fiche | 16/11/2026. Avec un bandeau : les mises a jour sont arretées depuis le 16/11/2026 "jusqu'a nouvel ordre" (changement technique chez l'ECMWF) |
| Fréquence de mise à jour | quotidienne d'après le catalogue (avant l'arret). 2 versions : "consolidated" (définitive) et "intermediate" (provisoire, sur les mois récents). On prend la consolidée |
| Volumétrie | 1 an sur le Grand Est = 104 390 valeurs (365 x 286), 275 Ko en NetCDF. 10 ans ≈ 3 Mo, rien de lourd. Limite du site : 3 720 champs par requete, donc 1 an par requete ca passe |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | date (`valid_time`) + latitude / longitude du centre de la maille. Pas de code commune ni de département -> pour joindre avec la BDIFF ou la Météo des forêts il faut une table commune -> maille (centre de chaque commune, puis maille la plus proche). Pas encore faite : l'API geo.api.gouv.fr ne répondait pas le 18/11 |
| Données personnelles | aucune, que de la météo sur une grille |
| Licence | CC-BY 4.0 : usage libre, meme commercial, en citant la source (DOI 10.24381/cds.0e89c522). Pas le meme probleme que la BDIFF |
| Questions de l'analyse auxquelles elle pourrait répondre | Q3 oui : historique du danger sur 10 ans et plus, toute l'année (y compris mars-avril, hors saison Météo des forêts). Q4 oui : compter par an les jours au-dessus d'un seuil FWI = nb d'activations du dispositif. Q5 en partie : meme indice partout, on peut comparer les départements. Q1 et Q2 non (pas de feux dedans) |

## Contrôles qualité repérés

- Doublons : pas de doublon de date (365 dates uniques sur 365 en 2025, 366 sur 366 en 2016)
- Dates : toutes dans l'année demandée, aucun trou
- Codes géographiques : pas de code commune ni département, que des coordonnées. Le rattachement au COG est a construire (voir clés)
- Valeurs manquantes : 0 valeur vide sur 104 390 en 2025, aucune maille toujours vide. FWI de 0 a 49 en 2025, médiane 0,9 (l'hiver tire tout vers 0)
- Cohérence avec la Météo des forêts (Bas-Rhin, saison 2025, boite approximative autour du 67, 24 mailles) : 120 jours comparés du 04/06 au 01/10.
  - 115 jours "faible" : FWI moyen de la boite 6,3
  - 5 jours "modéré" : FWI moyen 21,9
  - ca va dans le bon sens, mais des jours "faible" montent quand meme a 33,6 -> les niveaux Météo-France ne se déduisent pas directement du FWI
- Cohérence avec la BDIFF (tout le Grand Est, moyenne de la boite par jour) :
  - 2025 : FWI moyen 12,3 les 42 jours avec feu contre 3,5 les autres jours
  - 2016 : 11,1 les 5 jours avec feu contre 3,1
  - 2025 : 10 jours avec feu en avril, la ou la Météo des forêts n'existe pas. Le FWI les couvre

## Ce qu'on retient

- C'est la seule source qui donne le danger sur 10 ans et toute l'année : sans elle on a 3 étés de Météo des forêts et une poignée de feux. Petite, propre, licence ouverte
- Ce qui m'a surpris :
  - le FWI n'est pas l'IFM de Météo-France (meme formule canadienne, mais pas les memes données météo). Il faudra caler un seuil FWI sur les niveaux Météo des forêts avec les saisons 2024-2025
  - les mises a jour sont arretées depuis le 16/11/2026. Pas génant pour 2016-2025, mais rien ne garantit la saison 2027 par cette source
  - la note du site sur 2025 : un probleme dans ERA5 a obligé a recalculer, a garder en tete si 2025 parait bizarre
- A faire : la table commune -> maille pour les jointures (pour le pipeline)
