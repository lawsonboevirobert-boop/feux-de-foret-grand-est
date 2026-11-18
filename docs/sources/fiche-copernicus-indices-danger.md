# Fiche source : Indices de danger feux historiques de Copernicus (CEMS)

Explorée par : @lawsonboevirobert-boop, le 2026-11-18
Lien : <https://ewds.climate.copernicus.eu/datasets/cems-fire-historical-v1>
Fichier ouvert : `fwi_grand_est_2024_2026.nc`, téléchargé par l'API (FWI, réanalyse, jeu consolidé, version 4_1, années 2024 à 2026, grille 0,25°, zone du Grand Est). Ouverts aussi : la page du jeu, ses métadonnées dans le catalogue et le guide utilisateur de l'ECMWF.

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | Copernicus Emergency Management Service (programme de l'Union européenne). Les indices sont calculés par l'ECMWF à partir de la réanalyse météo ERA5, et diffusés sur l'Early Warning Data Store (EWDS). |
| Mode d'accès (export, API, téléchargement) et format | Formulaire de téléchargement sur l'EWDS, ou API Python (`cdsapi`). Il faut un compte, une clé d'API et accepter deux licences sur le site : les conditions générales de Copernicus et la licence CC-BY du jeu. Sans la seconde, l'API répond « required licences not accepted ». On choisit le produit, les variables, les jours, la grille et une zone. Le fichier reçu est un NetCDF (format HDF5), converti depuis le GRIB par l'ECMWF. |
| Grain (une ligne = ?) | Une valeur par jour et par maille de 0,25° : la variable `fwinx`, le FWI au sens du service canadien des forêts, sans unité, calculé pour midi heure locale. Le formulaire propose aussi les composantes du FWI (FFMC, DMC, DC, ISI, BUI) et d'autres indices de danger. |
| Emprise géographique | Monde entier sur le site. Notre fichier couvre le rectangle du Grand Est : 12 latitudes (47,40° à 50,15°) sur 21 longitudes (3,30° à 8,30°), soit 252 mailles. Le Bas-Rhin en touche 24. À cette latitude, une maille fait environ 28 km du nord au sud et 18 km d'est en ouest. |
| Période réellement couverte par les données | Dans notre fichier : du 1er janvier 2024 au 31 août 2026, sans trou (974 jours). Le jeu « consolidé » s'arrête donc fin août 2026 ; le catalogue annonce des données jusqu'au 14 novembre 2026, qui doivent se trouver dans le jeu « intermédiaire » (non téléchargé). Sur le site, le jeu commence le 3 janvier 1940. |
| Date de dernière mise à jour affichée sur la fiche | 16 novembre 2026. |
| Fréquence de mise à jour | Quotidienne en temps normal. Un avertissement du 12 novembre 2026 annonce l'arrêt des mises à jour à partir du 16 novembre 2026 « jusqu'à nouvel ordre », le temps d'un changement technique chez l'ECMWF. |
| Volumétrie | 974 jours × 252 mailles, soit 245 448 valeurs, pour un fichier de 624 Ko. Dix ans sur la même zone feraient environ 2,3 Mo. |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | La date (`valid_time`) et les coordonnées de la maille (`latitude`, `longitude`). Il n'y a pas de code commune ni de code département : pour joindre avec les feux de la BDIFF, il faut rattacher chaque commune à sa maille ; pour comparer avec la Météo des forêts, il faut résumer les mailles par département. |
| Données personnelles | Aucune : des valeurs météorologiques sur une grille. |
| Licence | CC-BY 4.0 : on peut tout réutiliser en citant la source. |
| Questions de l'analyse auxquelles elle pourrait répondre | Q3 et Q4 : un indice chaque jour de l'année, sur plus de dix ans si on le souhaite, printemps compris. Q5 : le même indice partout, ce qui permet de comparer le Bas-Rhin au Grand Est et à la France. |

## Contrôles qualité repérés

- Doublons : aucun jour en double.
- Dates : aucun jour manquant entre le 1er janvier 2024 et le 31 août 2026.
- Valeurs manquantes : aucune sur les 245 448 valeurs, y compris sur les mailles du bord.
- Échelle : les valeurs vont de 0 à 83,2. Le guide se contredit sur la borne haute (pas de borne dans un tableau, 0 à 100 dans une autre section) ; dans nos données, on reste sous 100.
- Pour la Météo des forêts, il faut décaler d'un jour : le niveau `niveau_j1` du bulletin du jour J concerne le jour J+1, alors que le FWI est daté du jour qu'il décrit.

## Premier croisement avec la Météo des forêts (Bas-Rhin, 2024-2026)

Nous avons fait la moyenne des 24 mailles du Bas-Rhin et l'avons comparée, jour par jour, au niveau publié par Météo-France (335 jours en commun, de juin 2024 à août 2026).

| Niveau Météo des forêts | Jours | FWI moyen du Bas-Rhin (médiane) | Plage observée |
|---|---|---|---|
| 1 (faible) | 285 | 3,4 | 0 à 31,9 |
| 2 (modéré) | 44 | 26,7 | 14,3 à 51,5 |
| 3 (élevé) | 6 | 41,6 | 36,6 à 54,0 |

Les deux indices vont dans le même sens (corrélation de rang de 0,6), mais les plages se chevauchent : certains jours « faibles » ont un FWI plus haut que des jours « modérés ». Il faudra en tenir compte pour convertir le FWI en niveaux.

## Ce qu'on retient

Le fichier est propre, léger et facile à lire, et il couvre ce qui manque à la Météo des forêts : le printemps et les années avant 2024. Sur les 12 feux du Bas-Rhin enregistrés dans la BDIFF en 2024 et 2025, le FWI moyen du jour allait de 2,5 à 26,2, alors qu'il est à 0,6 un jour ordinaire (médiane). Trois de ces feux sont tombés hors de la saison de la Météo des forêts, et six autres des jours classés « faibles ». Le FWI semble donc mieux distinguer les jours à feu que le niveau publié : c'est à creuser pour Q3 et Q4.
