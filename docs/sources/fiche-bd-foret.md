# Fiche source : BD Forêt V2 (IGN)

Explorée par : @lawsonboevirobert-boop, le 2026-11-18
Lien : <https://www.data.gouv.fr/datasets/bd-foret-r>
Fichier ouvert : extrait du service WFS de la Géoplateforme (couche `LANDCOVER.FORESTINVENTORY.V2:formation_vegetale`) sur un rectangle autour de Haguenau, enregistré en GeoJSON (581 polygones)

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | IGN. D'après la fiche, la V2 a été réalisée entre 2007 et 2018 par photo-interprétation des images infrarouges de la BD ORTHO, département par département. Elle est diffusée sur geoservices.ign.fr et par les services web de la Géoplateforme (`data.geopf.fr`). |
| Mode d'accès (export, API, téléchargement) et format | Trois accès : téléchargement par département sur geoservices.ign.fr (format annoncé : shapefile, non testé), service WFS (testé, sortie GeoJSON) et services d'affichage WMS et WMTS. |
| Grain (une ligne = ?) | Un polygone de formation végétale : identifiant (`id`), code et libellé du type de formation (`code_tfv`, `tfv`), regroupement en 11 grands types (`tfv_g11`) et essence principale (`essence`). La fiche annonce un polygone minimum de 5 000 m² ; le plus petit de l'extrait fait 5 006 m². |
| Emprise géographique | France métropolitaine. Le WFS compte 2 035 951 polygones en tout, et 25 980 dans le rectangle qui englobe le Bas-Rhin (ce rectangle déborde sur les départements voisins). |
| Période réellement couverte par les données | Photographies prises entre 2007 et 2018 selon les départements. Le millésime exact du Bas-Rhin : non vérifié, l'IGN le donne sur une carte des millésimes que nous n'avons pas ouverte. La fiche data.gouv.fr indique une couverture de 2006 à 2022. |
| Date de dernière mise à jour affichée sur la fiche | 17 novembre 2026 sur data.gouv.fr. |
| Fréquence de mise à jour | Irrégulière d'après la fiche. |
| Volumétrie | 2 035 951 polygones pour la France. L'extrait autour de Haguenau fait 581 polygones et 3,8 Mo en GeoJSON. |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | Uniquement la géométrie, en Lambert 93 (EPSG:2154). Il n'y a ni code commune ni code département : il faudra croiser les polygones avec les contours des communes (Admin Express) ou avec les mailles de Copernicus. |
| Données personnelles | Aucune : des types de forêt et d'essences. |
| Licence | Licence Ouverte 2.0, affichée sur la fiche. |
| Questions de l'analyse auxquelles elle pourrait répondre | Q1 : localiser les massifs et leurs essences là où partent les feux. Q5 : calculer la surface forestière de chaque département pour comparer le nombre de feux à surface boisée égale. |

## Contrôles qualité repérés

- Doublons : aucun identifiant en double dans l'extrait.
- Valeurs manquantes : aucune case vide dans l'extrait, mais 93 polygones ont l'essence « NR » et le type « Forêt fermée sans couvert arboré ».
- Surface minimale : respectée dans l'extrait (5 006 m² au plus petit).
- Millésimes différents selon les départements : comparer deux départements, c'est parfois comparer des photos de 2008 et de 2017.
- Le WFS renvoie les polygones entiers qui touchent le rectangle demandé, donc un peu de forêt hors de la zone. Pour calculer une surface par département, il faudra découper sur les contours officiels.

## Ce qu'on retient

La BD Forêt ne dit rien sur les feux, mais elle donne le dénominateur qui manque pour Q5 : la surface boisée de chaque département. Autour de Haguenau, la commune qui a le plus de feux dans la BDIFF, l'extrait montre 18 245 ha de forêt, dont 92 polygones de pin sylvestre pur. Le lien entre le type de forêt et les départs de feu reste à vérifier, mais c'est une piste pour Q1. Le téléchargement par département n'a pas été testé : c'est le prochain fichier à ouvrir pour avoir tout le Bas-Rhin.
