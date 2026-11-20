# Analyse de la commande - Firas

SDIS 67 (Bas-Rhin), saison feux 2027, réponse pour le 11/12.

La direction doit décider deux choses avant l'été 2027 : où mettre ses moyens contre les départs de feu, et à quel niveau de la Météo des forêts lancer le dispositif renforcé (patrouilles, guet).
Elle n'a pas le budget pour renforcer partout tout l'été. Et les chefs de centre trouvent que le seuil actuel se trompe dans les deux sens : des alertes sans feu, et des feux des jours où l'indice est bas.

J'ai rejoint le groupe le 18/11 et je vais surtout travailler sur le pipeline. Du coup en lisant la commande je me suis aussi demandé ce qu'on va devoir croiser comme données, et si ça va être facile ou pas.

## 1. Questions

1. Où et quand partent les feux dans le Bas-Rhin ? Quelles communes ou massifs, quels mois, quels jours de la semaine. Est-ce que c'est concentré sur quelques secteurs ou un peu partout ?
2. C'est quoi le seuil actuel, et combien de jours par saison il a déclenché le renfort ces dernières années ? Si le 67 n'arrive presque jamais au niveau « élevé », le dispositif ne sert quasiment jamais.
3. Pour chaque niveau possible (faible, modéré, élevé, très élevé) : combien de jours de renfort par été, combien de feux couverts, combien de fausses alertes et de feux manqués ?
4. Les feux manqués, ils sont graves ou pas ? Un feu de 1 m² un jour d'indice faible, ce n'est pas pareil qu'un feu de 10 ha. Il faut compter en nombre de feux ou en hectares ?
5. Est-ce que d'autres choses que la météo aident à prévoir les jours à risque : week-end, jour férié, vacances, type de forêt, feux des années d'avant dans le secteur ?
6. Est-ce que le Bas-Rhin se compare au reste du Grand Est et à la France ? Est-ce qu'un même niveau d'indice donne autant de feux partout, à surface de forêt égale ?
7. Et 2026 ? C'est la saison la plus récente donc la plus parlante pour le SDIS, mais c'est sûrement celle où il manquera des données officielles.

## 2. Termes inconnus

| Terme | Ce que j'en comprends | Source ou statut |
|---|---|---|
| SDIS | Les pompiers du département, ici le Bas-Rhin (67). | Glossaire du groupe, vérifié |
| Météo des forêts | Carte de Météo-France publiée chaque jour en saison, avec un niveau de danger de feu par département pour le lendemain. | Glossaire, vérifié |
| IFM / FWI | L'indice calculé avec la météo (température, humidité, vent, pluie) qui donne le niveau de la Météo des forêts. Le FWI c'est la version canadienne de départ. | Glossaire, vérifié |
| dispositif renforcé | Les moyens en plus qu'on active quand le danger est élevé. Je ne sais pas ce qu'il y a dedans exactement dans le 67, ni combien ça coûte par jour. | À demander au SDIS 67 |
| guet | Surveiller depuis un point en hauteur pour voir les fumées tôt. Je ne sais pas s'il y a des tours de guet en Alsace. | À vérifier |
| départ de feu / feu manqué / fausse alerte | Un feu qui démarre ; un feu un jour où le renfort n'était pas lancé ; un jour de renfort sans feu. | Définitions du groupe (glossaire) |
| détection satellite (FIRMS) | Un point chaud repéré par un satellite de la NASA. Ça peut être un feu de forêt mais aussi un brûlage agricole ou une usine. | Nouveau pour moi, à préciser dans la fiche #36 |
| grain | Ce que représente une ligne dans une table (un feu, un jour, une commune). | Glossaire, vérifié |

## 3. Besoins

- Une carte des secteurs à risque du Bas-Rhin, avec les périodes où ça brûle, pour savoir où placer les moyens.
- Un tableau seuil par seuil avec jours de renfort, coût, feux couverts, fausses alertes et feux manqués. C'est avec ça que le SDIS pourra choisir.
- Une comparaison du Bas-Rhin avec les autres départements, faite avec les mêmes définitions partout, sinon ça ne veut rien dire.
- Un découpage plus fin que le département. La Météo des forêts est par département, mais le SDIS veut savoir où agir.
- Assez d'années pour que ce soit solide. 3 saisons de Météo des forêts c'est peu, surtout s'il y a peu de feux dans le 67.

Ce qui peut fausser les résultats, vu du pipeline :

- Les sources n'ont pas le même grain (un feu par ligne d'un côté, un jour par département de l'autre). Il faudra tout ramener à « un jour × une zone » avant de croiser.
- Il faut prendre le niveau prévu la veille et pas celui constaté, vu que c'est lui qui sert à déclencher.
- Les codes communes changent avec les fusions. Si on ne les met pas tous sur la même année du COG, on va perdre des feux dans les jointures.
- Si la BDIFF n'a pas encore 2026, il manquera la dernière saison. Les détections satellite peuvent aider un peu mais il y a beaucoup de bruit dedans.

## 4. Données idéales

| Donnée idéale | Pour quelle question | Détail souhaité | Difficulté à l'obtenir |
|---|---|---|---|
| Tous les départs de feu avec position GPS, date, heure, surface et cause | 1, 3, 4, 5 | 1 ligne par feu, 10 ans minimum, Grand Est et France | Moyenne. La BDIFF donne la commune et la date mais pas toujours l'heure ni la position exacte. Et les coordonnées et les causes posent un problème de données personnelles. |
| Niveau de la Météo des forêts prévu la veille, chaque jour | 2, 3, 6 | 1 jour × 1 département, toute l'année | Forte. Publié seulement depuis 2023 et de juin à septembre. Pour avant, il faudra reconstituer avec le FWI de Copernicus. |
| Indice FWI par jour et par petite maille | 3, 6 | 1 jour × 1 carreau, 10 ans | Moyenne. Copernicus l'a, mais il faut le convertir en niveaux et vérifier que ça colle aux niveaux officiels. |
| Seuil actuel, coût d'un jour de renfort, budget 2027 | 2, 3 | 1 valeur par secteur | Forte. Ce n'est pas public, il faut le demander au SDIS 67. |
| Interventions détaillées du SDIS 67 (heure d'alerte, d'arrivée, moyens) | 1, 4 | 1 ligne par intervention | Forte. Données internes. |
| Détections de feux par satellite (NASA FIRMS) | 1, 7 | 1 point par passage de satellite, 2026 compris | Facile à récupérer, mais dur à trier : il faut enlever les brûlages agricoles et les sites industriels. |
| Surface de forêt et essences (résineux / feuillus) | 5, 6 | 1 polygone de forêt | Facile, BD Forêt de l'IGN. |
| Jours fériés (Alsace-Moselle) et vacances scolaires | 5 | 1 jour | Facile, données publiques. |

Le plus dur à avoir, ce sont les données du SDIS 67 (seuil, coût, budget). Sans elles on pourra dire quel seuil couvre le plus de feux, mais pas combien il coûte.

## 5. Confrontation avec les sources

Sources de l'inventaire du groupe ([inventaire.md](../sources/inventaire.md)) : BDIFF, COG, Météo des forêts, interventions des SIS, comptes des SDIS par l'OFGL (fiche de Franck dans #31), Copernicus (FWI), BD Forêt.

Degrés : complet / partiel / absent / inconnu. Chaque raison cite la colonne du fichier ou la rubrique de la fiche.

| Question | BDIFF | COG | Météo des forêts | Interventions SIS | OFGL | Copernicus | BD Forêt |
|---|---|---|---|---|---|---|---|
| Q1 où et quand partent les feux dans le 67 (communes, mois, jours de la semaine) | partiel : `Code INSEE` donne la commune et `Date de première alerte` le jour (donc le mois et le jour de la semaine), remplis pour les 84 feux du 67. Mais aucun feu saisi dans le 67 en 2006, 2009, 2010, de 2012 à 2019 et en 2021 (rubrique « Contrôles qualité ») | partiel : pas de feux, sert seulement à rattacher `Code INSEE` à `COM` et `DEP`. Les codes de notre export sont déjà tous au COG 2026 (matrice, note 3) | absent : grain = 1 département par jour (`num_dep`), pas de feux | absent : grain = 1 département par an (`Numéro`), pas de commune ni de date | absent : « Une ligne représente un agrégat, pour un budget, pour un exercice », pas de feux | absent : que de la météo (`fwinx`), pas de feux | partiel : `tfv` et `essence` situent les massifs, mais pas de code commune (jointure spatiale) et photos de 2007 pour le 67 |
| Q2 le seuil actuel, et combien de jours il a déclenché le renfort | absent : liste de feux, rien sur le dispositif | absent | partiel : `niveau_j1` permet de compter les jours par niveau (67 en 2025 : 115 faible, 5 modéré, jamais élevé), mais on ne connaît pas le seuil utilisé par le SDIS, et rien ne dit si le renfort a vraiment été lancé | absent : totaux annuels d'interventions, pas de jours de renfort | absent : budget annuel, rien ne dit combien de jours le dispositif a tourné | partiel : `fwinx` permet de compter les jours au-dessus d'un seuil, mais ce n'est pas l'indice officiel | absent |
| Q3 pour chaque niveau : jours de renfort, feux couverts, fausses alertes, feux manqués | partiel : `Date de première alerte` au jour près, mais une fausse alerte = un jour sans feu, et les années vides rendent les « jours sans feu » douteux (règle P1) | partiel : sert à rattacher le feu au département (`DEP`) pour le croiser avec le niveau | partiel : `niveau_j1` par jour et par département, mais 3 saisons (2024 à 2026) et seulement de juin à septembre (rubrique « Période réellement couverte ») | absent : pas de date | absent | partiel : `fwinx` tous les jours depuis 1940 et toute l'année, mais c'est un proxy de l'indice officiel et son grain est une maille (`latitude`, `longitude`), pas un département | absent |
| Q4 les feux manqués sont-ils graves (nombre ou hectares) ? | partiel : `Surface parcourue (m2)` remplie pour les 84 feux du 67 (23 font 1 ha ou plus). Seules `Surface parcourue` et `Surface forêt` sont comparables avant et après 2023 (nouveau formulaire). Mêmes années vides qu'en Q1 | absent | partiel : donne le niveau du jour du feu (`niveau_j1`), donc dit si un feu est « manqué », mais seulement de juin à septembre 2024-2026 | absent : pas de surface | absent | partiel : même rôle que la Météo des forêts, toute l'année, mais en proxy | absent |
| Q5 week-end, férié, vacances, type de forêt, feux des années d'avant | partiel : `Date de première alerte` donne le jour de la semaine (week-end), et `Code INSEE` + `Année` donnent l'historique du secteur, avec les mêmes années vides | partiel : `COM` pour rattacher l'historique à la commune | absent : c'est l'indice qu'on cherche à compléter, pas une de ces variables | absent | absent | absent : météo seulement, c'est justement ce qu'on veut dépasser | partiel : `essence` donne la part de résineux, mais 924 polygones du 67 ont l'essence « NR », pas de code commune, photos de 2007 |
| Q6 le 67 comparé au Grand Est et à la France, à surface de forêt égale | partiel : `Département` couvre les 10 départements, mais la saisie est inégale (les Vosges font la moitié des feux), et notre export ne prend que le Grand Est (rubrique « Emprise ») | partiel : `DEP` et `REG` pour regrouper | partiel : `num_dep` couvre les 96 départements, mais 3 saisons | partiel : colonne « Feux de végétations » par `Numéro` et par an, absente de 2010 à 2013 ; compte toute la végétation, pas que la forêt | absent : des montants, pas de feux | partiel : téléchargé sur le Grand Est seulement (rubrique « Emprise »), à résumer par département | partiel : surface de forêt par département pour comparer à surface égale, mais un fichier par département et des millésimes différents |
| Q7 et la saison 2026 ? | absent : la BDIFF s'arrête au 14/11/2025, le site coupe à l'année d'avant (rubrique « Période réellement couverte ») | absent | partiel : `mdf_2026` couvre du 28 mai au 5 octobre 2026 (67 : 76 jours faible, 49 modéré, 6 élevé), mais il n'y a pas de feux à mettre en face | absent : le dernier fichier est 2024 | absent : comptes jusqu'en 2025 | partiel : jeu consolidé jusqu'au 31/08/2026 seulement, et mises à jour arrêtées depuis le 16/11/2026 | absent : pas de feux, et photos de 2007 |

Aucune question n'a de source « complet ». Aucune case « inconnu » : tout a été vu dans un fichier ou une fiche.

### Décisions

- **Q1 : approximer + collecter.** La commune (`Code INSEE`) remplace le massif. Les années vides comptent comme « non renseigné », jamais comme « 0 feu ». Collecter : les interventions 2020-2026 du SDIS 67 (date, commune, surface), demandées dans #41
- **Q2 : collecter.** Le seuil actuel et les jours où le renfort a vraiment été lancé ne sont que chez le SDIS 67 (#41). En attendant, on donne combien de jours chaque niveau aurait déclenché avec `niveau_j1`, en disant que c'est une simulation
- **Q3 : approximer.** Le FWI de Copernicus remplace le niveau officiel pour 2006-2025 et pour les mois hors juin-septembre. Les seuils de FWI sont calés sur la Météo des forêts 2024-2026. Ce que ça mesure mal : le niveau officiel ajoute l'avis des prévisionnistes et la sécheresse de la végétation. Les fausses alertes ne se comptent que sur les années renseignées de la BDIFF
- **Q4 : approximer.** On compte les feux manqués en nombre **et** en hectares (`Surface parcourue`), sur les années renseignées. Ce que ça mesure mal : un feu est rattaché au jour de sa première alerte, même s'il a duré plusieurs jours
- **Q5 : approximer + collecter.** Week-end et historique viennent de la BDIFF, la part de résineux de la BD Forêt. Les jours fériés et les vacances ne sont dans aucune des 7 sources de l'inventaire : le groupe les a collectés depuis (fiches [jours fériés](../sources/fiche-jours-feries.md) et [calendrier scolaire](../sources/fiche-calendrier-scolaire.md)). C'est devenu la Q3 du groupe
- **Q6 : approximer, et renoncer en partie.** Grand Est : FWI résumé par département et feux rapportés à la surface de forêt de la BD Forêt, sur les années où chaque département a des feux saisis. France : on renonce à comparer à surface de forêt égale (96 fichiers BD Forêt et 96 jointures spatiales), on se limite aux niveaux de la Météo des forêts et aux feux de végétation des SIS
- **Q7 : approximer + collecter.** Aucune source de l'inventaire n'a les feux de 2026. Approximer avec NASA FIRMS ([ma fiche](../sources/fiche-nasa-firms.md)) : 46 détections dans le 67 en 2026, sur 26 jours et 23 communes. Ce que ça mesure mal : ce sont des détections satellite, pas des départs de feu. Il y a des faux positifs (usines, brûlages agricoles), et des feux non vus : le feu de Haguenau du 12/08/2026 est détecté, celui du 13/08 non. Ça **surestime** les feux en plaine agricole et **sous-estime** les petits feux en forêt. Collecter : les interventions 2026 du SDIS 67 (#41), la seule source fiable pour cette saison

### Ce qui a changé par rapport à la section 4

- je pensais avoir une liste de feux complète sur 10 ans : dans le 67, la BDIFF a plus d'années vides (12) que d'années remplies (8)
- je voulais le niveau prévu la veille sur 10 ans : la Météo des forêts n'a que 3 étés, de juin à septembre. Copernicus rattrape l'historique, mais en proxy
- je comptais sur les détections satellite pour 2026 : elles existent, mais elles ne remplacent pas une liste de feux (faux positifs, feux manqués)
- le seuil actuel et le coût d'un jour de renfort ne sont dans aucune source ouverte. L'OFGL donne seulement le budget total du SDIS 67, avec un changement de nomenclature (M57) à partir de 2024
- pas besoin de convertir les codes communes : ceux de notre export BDIFF sont déjà tous au COG 2026
