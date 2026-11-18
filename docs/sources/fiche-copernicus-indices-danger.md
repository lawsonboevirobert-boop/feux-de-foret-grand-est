# Fiche source : Indices de danger feux historiques de Copernicus (CEMS)

Explorée par : @lawsonboevirobert-boop, le 2026-11-18
Lien : <https://ewds.climate.copernicus.eu/datasets/cems-fire-historical-v1>
Ce qui a été ouvert : la page du jeu de données, ses métadonnées dans le catalogue, le formulaire de téléchargement et le guide utilisateur de l'ECMWF. Aucun fichier de données : le téléchargement demande d'accepter des conditions d'utilisation dans un formulaire, et nous n'avons pas encore de compte.

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | Copernicus Emergency Management Service (programme de l'Union européenne). Les indices sont calculés par l'ECMWF à partir de la réanalyse météo ERA5, et diffusés sur l'Early Warning Data Store (EWDS). |
| Mode d'accès (export, API, téléchargement) et format | Formulaire de téléchargement sur l'EWDS, ou API Python (`cdsapi`) conseillée pour les gros volumes. On choisit le produit (réanalyse ou membres d'ensemble), les variables, les jours, la grille (d'origine, 0,5° ou 0,25°) et une zone. Formats : GRIB, ou NetCDF sur les grilles 0,5° et 0,25° uniquement. Le formulaire impose d'accepter des conditions d'utilisation. Besoin d'un compte : non vérifiée, nous n'avons pas tenté le téléchargement. |
| Grain (une ligne = ?) | Une valeur par jour et par maille de la grille, calculée pour midi heure locale. Le jeu contient le FWI (indice canadien, sans unité, à la base de l'IFM de Météo-France) et ses composantes (FFMC, DMC, DC, ISI, BUI), ainsi que des indices d'autres systèmes de danger (Keetch-Byram, Energy release component…). |
| Emprise géographique | Toutes les terres émergées du monde. Le formulaire permet de découper une zone, par exemple le Grand Est. À 0,25°, une maille mesure environ 28 km du nord au sud et 18 km d'est en ouest à la latitude du Bas-Rhin (calcul à partir de la taille de la grille). |
| Période réellement couverte par les données | Du 3 janvier 1940 au 14 novembre 2026 d'après les métadonnées du catalogue. Non vérifiée dans un fichier, pour la raison donnée plus haut. |
| Date de dernière mise à jour affichée sur la fiche | 16 novembre 2026. |
| Fréquence de mise à jour | Quotidienne en temps normal, avec un jeu « consolidé » et un jeu « intermédiaire » pour les jours les plus récents. Mais un avertissement du 12 novembre 2026 annonce que les mises à jour s'arrêtent à partir du 16 novembre 2026 « jusqu'à nouvel ordre », le temps d'un changement technique chez l'ECMWF. |
| Volumétrie | Non vérifiée : aucun fichier téléchargé, et le guide n'indique pas de taille. |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | La date et les coordonnées (latitude, longitude) de la maille. Il n'y a pas de code commune ni de code département : pour joindre avec les feux de la BDIFF, il faudra rattacher chaque commune à la maille qui la contient ; pour comparer avec la Météo des forêts, il faudra résumer les mailles par département. |
| Données personnelles | Aucune : des valeurs météorologiques sur une grille. |
| Licence | CC-BY 4.0, affichée sur la page et dans les métadonnées. |
| Questions de l'analyse auxquelles elle pourrait répondre | Q3 et Q4 : c'est la seule source qui donne un indice de danger chaque jour de l'année sur plus de dix ans, printemps compris, et pour 2026. Q5 : le même indice partout, ce qui permet de comparer le Bas-Rhin au Grand Est et à la France. |

## Contrôles qualité repérés

Les contrôles sur les valeurs (doublons, jours manquants, valeurs vides) restent à faire sur un premier fichier. Ce qu'on sait déjà :

- Le guide se contredit sur l'échelle du FWI : un tableau dit que l'indice n'a pas de borne haute, une autre section parle d'une plage de 0 à 100. À regarder sur les vraies valeurs.
- Le FWI de Copernicus n'est pas le niveau publié par la Météo des forêts. D'après la documentation de Météo-France, le niveau officiel part de l'IFM mais ajoute la sécheresse de la végétation, les zones sensibles et l'avis des prévisionnistes. Il faudra comparer les deux sur 2024-2026 avant de convertir le FWI en niveaux.
- L'arrêt des mises à jour depuis le 16 novembre 2026 ne gêne pas notre période d'étude, mais il faut le noter si on veut suivre la saison 2027.

## Ce qu'on retient

C'est la source qui comble le trou de la Météo des forêts : 86 ans d'indice, tous les mois de l'année, alors que 43 % des feux du Grand Est partent hors de la période juin-septembre. Il faut maintenant créer un compte sur l'EWDS, télécharger un premier fichier sur le Grand Est (par exemple 2024 à 2026 en NetCDF à 0,25°) et compléter les rubriques encore « non vérifiées ».
