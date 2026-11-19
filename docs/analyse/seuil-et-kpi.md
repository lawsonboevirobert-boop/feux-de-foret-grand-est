# Le seuil et le KPI : comment tout se tient

Pour l'équipe, état au 19/11/2026. But : avoir la même explication du seuil et du KPI, de la question de l'analyse globale jusqu'à l'objectif SMART, et savoir la défendre à l'oral.

Tous les chiffres viennent des données publiques déjà téléchargées (BDIFF, archives de la Météo des forêts, FWI de Copernicus). Un seul chiffre est supposé : le nombre de jours de renfort par saison. La méthode de calcul est à la fin.

## 1. En une phrase

On ne cherche pas « le bon niveau de l'indice ». On cherche les meilleurs jours pour un budget donné : si le SDIS ne peut renforcer que N jours dans la saison, quelle règle choisit les jours qui couvrent le plus de départs de feu ?

## 2. Pourquoi un seuil fixe sur la Météo des forêts ne marche pas

- Dans le 67, de 2024 à 2026, la Météo des forêts a donné 285 jours « faible », 44 « modéré », 6 « élevé » et aucun « très élevé ». Un seuil à « élevé » ne déclenche presque jamais.
- Dans le Grand Est en 2024-2025, un seuil à « modéré » aurait lancé 69 jours de renfort (tous départements confondus). Ces jours couvrent 19 % des feux de la saison de publication, et 90 % d'entre eux n'ont eu aucun feu.
- 22 des 69 feux du Grand Est en 2024-2025 sont partis hors de la saison de publication (juin à septembre). Sur 2006-2025, c'est 43 % des feux. Aucun seuil sur cet indice ne peut les couvrir, puisqu'il n'est pas publié ces jours-là.
- L'indice a quand même de la valeur : un jour « modéré » a environ 6 fois plus de chances d'avoir un feu qu'un jour moyen (environ 10 % contre 1,7 %). Le problème vient du seuil fixe, pas de la météo.

## 3. L'idée : comparer les règles à nombre de jours égal

Le SDIS ne peut pas renforcer tous les jours. Une règle se juge donc sur ce qu'elle couvre pour le même nombre de jours, donc pour le même coût.

Avec le FWI de Copernicus (tous les jours depuis 1940, toute l'année), sur 2006-2025, si on renforce chaque saison (mars à octobre) les N jours où le FWI est le plus haut :

| N jours par saison | Feux couverts, Grand Est | Feux couverts, 67 | Au hasard |
|---|---|---|---|
| 10 | 16 % (117 sur 736) | 14 % (12 sur 84) | 4 % |
| 20 | 28 % (209 sur 736) | 32 % (27 sur 84) | 8 % |
| 30 | 37 % (273 sur 736) | 45 % (38 sur 84) | 12 % |

Le FWI seul fait 3 à 4 fois mieux que le hasard. C'est la valeur de départ que la règle combinée de H3 doit battre.

## 4. Le fil, de la commande au KPI

| Étape | Contenu |
|---|---|
| Décision du SDIS | à partir de quand lancer le dispositif renforcé, avec un budget qui limite le nombre de jours |
| Questions | Q4 : pour chaque seuil, jours de renfort, départs couverts, fausses alertes, feux manqués. Q3 : une règle qui ajoute le type de jour, l'historique du secteur et la part de résineux fait-elle mieux que l'indice seul ? |
| Hypothèse | H3 : la règle combinée couvre au moins 20 % de départs en plus que l'indice seul, à jours de renfort égaux |
| Valeur de départ | 32 % des départs du 67 couverts avec 20 jours et le FWI seul |
| Objectif SMART | saison 2027 (1er mars au 31 octobre), Bas-Rhin, 20 jours de renfort au plus : au moins 38 % des départs tombent un jour de renfort (32 % + 20 %) |
| KPI | taux de départs couverts à budget fixé |
| Garde-fous | le nombre de jours reste à N ; la part des jours de renfort avec au moins un départ ne baisse pas |
| Décision éclairée | le seuil 2027, exprimé en valeur de FWI et traduit en niveaux de la Météo des forêts pour le SDIS |

Si H3 est réfutée (gain inférieur à 20 %), l'objectif redescend à 32 % et on recommande le FWI seul, qui fait déjà mieux qu'un seuil fixe.

## 5. Le KPI

- **Nom :** taux de départs couverts à budget fixé.
- **Formule :** départs survenus un jour de renfort ÷ départs de la saison, pour un département, avec exactement N jours de renfort entre le 1er mars et le 31 octobre.
- **Paramètres :** N (20 supposé), la règle qui choisit les jours (niveau de la Météo des forêts, seuil de FWI, règle combinée), la zone, la saison.
- **Indicateur secondaire :** le même taux pour les feux de 1 ha ou plus. 10 % des feux font 85 % de la surface brûlée, c'est là que le renfort compte le plus. Valeur de départ avec 20 jours : 33 % dans le Grand Est (68 sur 205), 6 sur 23 dans le 67.
- **Garde-fou 1 :** le nombre de jours reste égal à N. Sinon il suffirait d'ajouter des jours pour monter le taux.
- **Garde-fou 2 :** la précision, c'est-à-dire la part des jours de renfort avec au moins un départ. Elle vaut 15 % dans le 67 avec le FWI seul et 20 jours (24 jours sur 160), contre 10 % pour le seuil « modéré » dans le Grand Est en 2024-2025. Elle ne doit pas baisser.
- **Contexte à afficher à côté :** le nombre de départs de la saison, les années non renseignées, la part des départs hors juin-septembre.

## 6. Ce que ça donne pour le seuil

- Dans le 67, le FWI moyen vaut environ 28 les jours « modéré » et 43 les jours « élevé ».
- Pour avoir 20 jours de renfort par saison, il faut déclencher vers FWI 15 (vers 21 pour 10 jours, vers 12 pour 30 jours). C'est en dessous du niveau « modéré ».
- Lecture provisoire : déclencher à « modéré » ne suffit pas à utiliser 20 jours, et « élevé » ne déclenche presque jamais. Le seuil recommandé se donnera en FWI, avec sa correspondance en niveaux pour le SDIS.

## 7. Limites

- Le 67 est approché par un rectangle de mailles du FWI (latitudes 48,1 à 49,1, longitudes 7,0 à 8,3), tant que la table commune -> maille n'existe pas.
- Les fichiers FWI utilisés sont encore sur l'ancienne grille, décalée (voir #45) : tout est à recalculer une fois le retéléchargement fini. Les ordres de grandeur ne devraient pas changer.
- Le 67 n'a que 84 départs sur ses années renseignées (2007, 2008, 2011, 2020, 2022 à 2025). Une saison seule pèse peu : il faut lire le KPI sur plusieurs saisons, ou sur le Grand Est.
- Les jours de renfort sont simulés, pas relevés. La BDIFF 2027 ne sera publiée qu'en 2028 : pour suivre 2027, il faudra les interventions du SDIS 67.

## 8. À décider en groupe

1. **N, le nombre de jours de renfort.** 20 est un ordre de grandeur : le 67 a eu 50 jours « modéré » ou plus sur 2024-2026, dont 45 en 2026. Le chiffre réel viendra du SDIS (#41).
2. **Le week-end dans H3.** Les feux du week-end (29,3 %) sont dans la même proportion que les jours de week-end (28,6 %). Le week-end seul ne semble pas aider à prévoir ; les fériés et les vacances restent à tester. On a regardé ce chiffre sur toutes les années, pas seulement sur la période de calage 2017-2022 : il faut le noter dans le journal des décisions.
3. **Qui porte quel KPI dans `kpi/`.** Celui-ci couvre Q3 et Q4 (le seuil). Q1 (où mettre les moyens) peut avoir le sien, par exemple la part des départs dans les communes les plus touchées (H1).

## 9. Comment les chiffres ont été calculés

- **Feux :** export BDIFF du Grand Est, 2006-2025 (736 feux). Un départ = un feu, daté du jour de sa `Date de première alerte`. Surface : `Surface parcourue (m2)`.
- **Météo des forêts :** archives 2024 à 2026. Le niveau d'un jour est le `niveau_j1` publié la veille (date de diffusion + 1 jour), par `num_dep` (codes remis sur 2 chiffres).
- **FWI :** fichiers Copernicus 2006-2025, variable `fwinx`. Grand Est : moyenne de toutes les mailles. 67 : moyenne des mailles du rectangle de la partie 7.
- **Règle « N meilleurs jours » :** pour chaque année, on garde les N jours de mars à octobre où le FWI est le plus haut, et on compte les feux tombés ces jours-là. Pour le 67, seulement les années où des feux sont saisis.
- **Seuils de FWI :** la valeur dépassée en moyenne N jours sur les 245 jours de mars à octobre, sur 2006-2025.
- **Week-end :** part des feux un samedi ou un dimanche, comparée à 2 jours sur 7.

Tout sera refait dans le pipeline une fois le nettoyage (#37) et la table commune -> maille prêts. Ces chiffres servent à cadrer le KPI, pas de résultat final.
