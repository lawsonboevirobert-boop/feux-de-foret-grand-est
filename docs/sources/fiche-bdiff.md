# Fiche source : BDIFF (base de données sur les incendies de forêt en France)

Explorée par : @wilsonDenis, le 2026-11-17
Lien : https://bdiff.agriculture.gouv.fr/incendies (fiche data.gouv : https://www.data.gouv.fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff)
Fichier ouvert : export CSV du portail, rangé en local dans `data/raw/bdiff/incendies_grand-est_2006-2025.csv` (+ `definitions.pdf` et `mentions-legales.pdf` fournis avec)

Pour refaire l'export : date de première alerte du 01/01/2006 au 17/11/2026, surface vide (pas de mini ni de maxi), région administrative Grand Est, aucun département coché. Le site ajoute tout seul le filtre "Type de feu : F" et coupe au 31/12/2025.

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | Ministère de l'Agriculture (éditeur), l'IGN fait le site et la base. Les fiches sont saisies par les services sur le terrain |
| Mode d'accès (export, API, téléchargement) et format | formulaire de recherche sur le site puis export. CSV séparateur `;`, UTF-8. Attention les 3 premières lignes c'est du texte (avertissement, nb d'incendies, critères), l'entete est a la ligne 4 |
| Grain (une ligne = ?) | 1 incendie, localisé a la commune (pas de coordonnées) |
| Emprise géographique | France entière dans la base. Notre export : les 10 départements du Grand Est |
| Période réellement couverte par les données | notre export : premier feu le 05/06/2006, dernier le 14/11/2025. Le site s'arrete a l'année d'avant (pas de 2026) |
| Date de dernière mise à jour affichée sur la fiche | 13/12/2025 sur data.gouv. Pas de date sur le portail ni dans l'export |
| Fréquence de mise à jour | annuelle d'après data.gouv |
| Volumétrie | 736 feux, 24 colonnes, 81 Ko pour le Grand Est |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | `Code INSEE` (commune) -> COG. `Département`. `Date de première alerte` (jour + heure) -> Météo des forêts. Identifiant d'un feu = `Année` + `Numéro` (le numéro tout seul se répète d'une année a l'autre) |
| Données personnelles | pas de nom, pas d'adresse, pas de coordonnées. Mais commune + date + heure + nature "Malveillance" peut renvoyer a une affaire connue localement -> a garder au niveau commune / jour, pas plus fin |
| Licence | pas clair. data.gouv dit Licence Ouverte 2.0, mais les mentions légales du site disent : pas d'usage commercial, pas de modification des données reproduites, citer le site, droits de reproduction réservés. A trancher avec le groupe / la prof |
| Questions de l'analyse auxquelles elle pourrait répondre | Q1 oui (commune, date, heure). Q2 en partie seulement (cause vide 87% du temps). Q3 et Q4 oui une fois croisée avec la Météo des forêts (jours avec feu, surface des feux manqués). Q5 oui pour le Grand Est, pour la France il faut refaire un export "France entière" |

## Contrôles qualité repérés

- Doublons : pas de doublon sur `Année` + `Numéro`. Mais un doublon probable : 2 fiches a Haguenau le 13/08/2025 a 17:54 avec la meme surface (15 000 m2), numéros 7287 et 11751. A enlever ou a signaler
- Dates : toutes dans la période, l'année colle toujours avec la date. 7 feux a 00:00:00 pile, surement une heure pas connue
- Codes géographiques : tous les codes INSEE commencent bien par le bon département. Reste a vérifier qu'ils existent tous dans le COG 2026 (fusions de communes, voir [fiche COG](fiche-cog.md))
- Valeurs manquantes :
  - `Nature` (la cause) vide pour 639 feux sur 736 (87%). Dans le 67 : 71 sur 84 (85%)
  - `Précision de la donnée` = "Données partielles ou non valides" pour 54 feux
  - surfaces maquis/garrigues et type de peuplement toujours vides (normal hors zone méditerranéenne)
  - les colonnes de surface par végétation changent en 2023 (nouveau formulaire). Les 124 feux de 2023 a 2025 n'ont pas les anciennes colonnes, et les anciennes années n'ont pas les nouvelles. Seules `Surface parcourue` et `Surface forêt` sont comparables sur toute la période
- Population incomplète (le plus génant) :
  - aucun feu en 2009 dans tout le Grand Est
  - le Bas-Rhin n'a aucun feu en 2006, 2009, 2010, de 2012 a 2019 et en 2021, puis 22 en 2020 et 28 en 2022
  - les Vosges font la moitié des feux de la région (368 sur 736)
  - ca ressemble plus a des différences de saisie entre départements et entre années qu'a une vraie absence de feux. Comparer des départements ou des années avec ca sans précaution c'est risqué

## Ce qu'on retient

- C'est la source principale pour les feux, on peut pas faire sans. Surfaces en m2 (et pas en ha), du plus petit 1 m2 au plus gros 180 ha, médiane 300 m2 : 531 feux font moins d'1 ha, donc les petits feux sont bien dedans
- Ce qui m'a surpris :
  - 43% des feux partent hors juin-septembre (surtout mars-avril : 221 feux), donc en dehors des mois ou la Météo des forêts est publiée. Pour Q3 et Q4 il faudra le FWI de Copernicus pour ces mois la
  - les trous dans les années, surtout pour le Bas-Rhin
  - la licence qui dit pas la meme chose sur data.gouv et sur le site
- Le fichier brut reste en local, on le met pas sur le dépôt (données brutes pas versionnées, cf #5). Chacun peut le refaire avec les critères en haut de la fiche
