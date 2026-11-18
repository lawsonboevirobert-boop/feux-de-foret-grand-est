# Fiche source : BD Forêt version 2 (IGN)

Explorée par : @wilsonDenis, le 2026-11-18
Lien : https://geoservices.ign.fr/bdforet (fiche data.gouv : https://www.data.gouv.fr/datasets/bd-foret-r)
Fichier ouvert : `BDFORET_2-0__SHP_LAMB93_D067_2014-04-01.7z` (Bas-Rhin), couche `FORMATION_VEGETALE.shp`. Rangé en local dans `data/raw/bdforet/`, pas sur le dépôt

Pour refaire le téléchargement : pas de compte. Liste des fichiers par département sur https://data.geopf.fr/telechargement/resource/BDFORET?zone=D067 (changer D067 pour un autre département), prendre la version `2-0`. Archive 7z de 19,6 Mo, 42 Mo une fois décompressée.

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | IGN (Institut national de l'information géographique et forestière). Faite par photo-interprétation des photos aériennes |
| Mode d'accès (export, API, téléchargement) et format | téléchargement direct, un fichier par département. Shapefile (ou GeoPackage) en Lambert 93 (EPSG:2154), dans une archive 7z. Il faut un outil SIG ou python (geopandas) pour l'ouvrir |
| Grain (une ligne = ?) | 1 polygone = 1 zone de végétation homogène (type de forêt + essence dominante), d'au moins 0,5 ha d'après la doc |
| Emprise géographique | France métropolitaine, découpée par département. Ouvert : Bas-Rhin seulement (pour le Grand Est il faut les 10 fichiers) |
| Période réellement couverte par les données | une photo a un instant, pas une série : les métadonnées du 67 citent les photos aériennes de 2007 (`PVA_2007`). Le nom du fichier dit 2014-04-01 (date d'édition). Donc l'état de la forêt vers 2007, pas en 2026 |
| Date de dernière mise à jour affichée sur la fiche | 17/11/2026 sur data.gouv (la fiche, pas les données). Métadonnées du fichier : traitement du 14/09/2022 |
| Fréquence de mise à jour | pas de rythme fixe, le département est refait quand l'IGN repasse. Pour le 67 la v2 date de 2014 et n'a pas bougé depuis. Rythme exact : non vérifié, pas trouvé dans la doc |
| Volumétrie | Bas-Rhin : 12 798 polygones, 5 colonnes (`ID`, `CODE_TFV`, `TFV`, `TFV_G11`, `ESSENCE`) + la géométrie. 196 774 ha au total |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | aucune clé commune ni date. Que de la géométrie -> jointure spatiale obligatoire (croiser avec les contours des communes pour avoir la surface de forêt par commune, ou avec les mailles Copernicus) |
| Données personnelles | aucune |
| Licence | Licence Ouverte 2.0 d'après data.gouv. Mais les métadonnées dans l'archive disent encore "conditions générales d'utilisation des fichiers IGN" (ancien texte d'avant l'ouverture des données IGN). On suit data.gouv, a confirmer avec la prof |
| Questions de l'analyse auxquelles elle pourrait répondre | Q1 oui : ou est la forêt dans le 67, et de quel type (résineux plus sensibles au feu que les feuillus). Q5 en partie : surface de forêt par département pour ramener le nb de feux a la surface boisée (il faut alors les 10 départements, voire toute la France). Q2, Q3, Q4 non (pas de date, pas de feux) |

## Contrôles qualité repérés

- Doublons : aucun `ID` en double, aucune géométrie en double
- Dates : pas de date dans les données. Le probleme c'est l'age : photos de 2007, donc les coupes, tempetes, scolytes depuis ne sont pas dedans
- Codes géographiques : pas de code commune ni département dans la couche. Le département se déduit du nom du fichier (D067). Toutes les géométries sont valides, aucune vide
- Valeurs manquantes : aucune case vide. Mais `ESSENCE` vaut "NR" sur 9 988 ha (les "forets fermées sans couvert arboré" : coupes, clairières) et "NC" sur 1 542 ha (landes, peupleraies...). 14 polygones font moins de 0,5 ha alors que la doc annonce 0,5 ha minimum (sans doute des morceaux coupés au bord du département)
- Libellés : un petit bug d'accent dans `TFV` : "Forêt fermée dun autre conifère..." (l'apostrophe a sauté), a corriger si on affiche les libellés

## Ce qu'on retient

- Bas-Rhin : environ 197 000 ha de forets et landes. Les feuillus dominent (91 000 ha), puis les conifères (51 000 ha) et le mixte (40 000 ha). Pin sylvestre pur 16 500 ha, sapin/épicéa 20 000 ha (les résineux, a priori plus inflammables, a vérifier avec le SDIS)
- Utile pour situer les feux (Q1) et pour comparer les départements a surface de foret égale (Q5). Pas utile pour les questions sur le seuil (Q3, Q4)
- Ce qui m'a surpris : les données ont presque 20 ans (photos 2007) et la licence n'est pas la meme dans l'archive et sur data.gouv
