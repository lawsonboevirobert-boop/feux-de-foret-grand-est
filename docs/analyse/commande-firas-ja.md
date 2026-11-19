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
