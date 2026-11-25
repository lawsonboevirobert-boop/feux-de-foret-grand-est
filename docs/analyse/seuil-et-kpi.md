# Le seuil et le KPI : comment tout se tient

Pour l'équipe, état au 19/11/2026, revu après la relecture de Denis. But : avoir la même explication du seuil et du KPI, de la question de l'analyse globale jusqu'à l'objectif SMART, et savoir la défendre à l'oral.

Tous les chiffres viennent des données publiques déjà téléchargées (BDIFF, archives de la Météo des forêts, FWI de Copernicus sur la grille d'origine). Un seul chiffre est supposé : le budget de 20 jours de renfort par saison. La méthode de calcul est à la fin.

## 1. En une phrase

On ne cherche pas « le bon niveau de l'indice ». On cherche la règle qui couvre le plus de départs de feu pour un budget de jours de renfort donné, et on la juge sur des années qui n'ont pas servi à la caler.

## 2. Pourquoi un seuil fixe sur la Météo des forêts ne marche pas

- Dans le 67, de juin 2024 à août 2026 (les 335 jours où le FWI existe aussi), la Météo des forêts a donné 285 jours « faible », 44 « modéré », 6 « élevé » et aucun « très élevé ». Un seuil à « élevé » ne déclenche presque jamais.
- Dans le Grand Est en 2024-2025, un seuil à « modéré » aurait lancé 69 jours de renfort (tous départements confondus). Ces jours couvrent 19 % des feux de la saison de publication, et 90 % d'entre eux n'ont eu aucun feu.
- 22 des 69 feux du Grand Est en 2024-2025 sont partis hors de la saison de publication (juin à septembre). Sur 2006-2025, c'est 43 % des feux. Aucun seuil sur cet indice ne peut les couvrir, puisqu'il n'est pas publié ces jours-là.
- L'indice a quand même de la valeur : un jour « modéré » a environ 6 fois plus de chances d'avoir un feu qu'un jour moyen (environ 10 % contre 1,7 %). Le problème vient du seuil fixe et de la saison courte, pas de la météo.

## 3. Ce que vaut le FWI pour choisir les jours

Le FWI de Copernicus existe tous les jours depuis 1940, toute l'année. On l'utilise de deux façons.

### Le maximum théorique : les N meilleurs jours de chaque saison

Si on renforce chaque saison (mars à octobre) les N jours où le FWI a été le plus haut, sur 2006-2025 :

| N jours par saison | Feux couverts, Grand Est | Feux couverts, 67 | Au hasard |
|---|---|---|---|
| 10 | 16 % (117 sur 736) | 17 % (14 sur 84) | 4 % |
| 20 | 28 % (208 sur 736) | 33 % (28 sur 84) | 8 % |
| 30 | 37 % (274 sur 736) | 44 % (37 sur 84) | 12 % |

**Ce n'est pas applicable tel quel** : pour savoir quels sont les 20 meilleurs jours, il faut connaître le FWI de toute la saison. Ces chiffres sont un plafond, ce qu'on ferait de mieux en connaissant l'avenir. Ils montrent seulement que le FWI fait 3 à 4 fois mieux que le hasard.

### La version réaliste : un seuil fixe calé sur des années passées

On cherche sur des années de calage la valeur de FWI qui aurait donné 20 jours de renfort par saison, puis on applique ce seuil tel quel à d'autres années, les années de test :

| Zone | Calage | Test | Seuil FWI | Jours de renfort réels par saison | Départs couverts | Gain sur le hasard | Précision |
|---|---|---|---|---|---|---|---|
| Grand Est | 2006-2016 | 2017-2025 | 13,5 | 45 | 52 % (317 sur 615) | × 2,8 | 39 % |
| Grand Est | 2017-2022 | 2023-2025 | 21,2 | 8 | 21 % (26 sur 124) | × 6,2 | 64 % |
| 67 | 2006-2016 | 2017-2025 | 13,4 | 41 | 59 % (38 sur 64) | × 3,6 | 9 % |
| 67 | 2017-2022 | 2023-2025 | 21,0 | 10 | 14 % (2 sur 14) | × 3,6 | 3 % |

Gain sur le hasard : part des départs couverts ÷ part des jours de renfort dans la saison. Précision : part des jours de renfort avec au moins un départ dans la zone.

**Ce que ça apprend : un seuil fixe ne tient pas le budget.** Calé pour 20 jours sur 2006-2016, il en donne 45 sur 2017-2025, parce que les saisons récentes sont plus chaudes. Calé sur 2017-2022, il n'en donne que 8 sur 2023-2025. Le taux de départs couverts ne veut donc rien dire seul : il faut toujours le lire avec le nombre de jours réellement utilisés, ou avec le gain sur le hasard.

## 4. Le fil, de la commande au KPI

| Étape | Contenu |
|---|---|
| Décision du SDIS | à partir de quand lancer le dispositif renforcé, avec un budget qui limite le nombre de jours |
| Questions | Q4 : pour chaque seuil, jours de renfort, départs couverts, fausses alertes, feux manqués. Q3 : une règle qui ajoute le type de jour, l'historique du secteur et la part de résineux fait-elle mieux que l'indice seul ? |
| Hypothèse | H3 : la règle combinée couvre au moins 20 % de départs en plus que l'indice seul, à jours de renfort égaux |
| Valeur de départ | FWI seul, calé sur 2017-2022, testé sur 2023-2025, Grand Est : 21 % des départs couverts avec 8 jours de renfort par saison |
| Objectif SMART | voir ci-dessous |
| KPI | taux de départs couverts, toujours affiché avec les jours de renfort réellement utilisés |
| Garde-fous | les jours utilisés ne dépassent pas le budget ; la précision ne baisse pas |
| Décision éclairée | la règle 2027 : un seuil de FWI (et sa correspondance en niveaux de la Météo des forêts), avec un plafond de jours |

**Objectif SMART.** D'ici le rendu du 11 décembre 2026, montrer sur les années de test 2023-2025, dans le Grand Est, qu'une règle de déclenchement calée sur 2017-2022 couvre au moins 25 % des départs de feu (21 % + 20 %), sans utiliser plus de jours de renfort que le FWI seul.

- Spécifique : une seule mesure, la part des départs couverts, à jours de renfort égaux.
- Mesurable : sur le passé, avec les données publiques, sans attendre la BDIFF 2027.
- Atteignable : c'est le gain que teste H3. Si H3 est réfutée, on recommande le FWI seul.
- Réaliste : même nombre de jours, donc même coût ; seul le choix des jours change.
- Temporel : résultat au rendu du 11/12.

Pourquoi pas un objectif « 2027 dans le Bas-Rhin » : le 67 a eu 2 feux saisis en 2023, 1 en 2024 et 11 en 2025. Un objectif sur une seule saison du 67 se joue à un ou deux feux près, et la BDIFF 2027 ne sera publiée qu'en 2028. La saison 2027 sert au suivi, pas à la preuve.

## 5. Le KPI

- **Nom :** taux de départs couverts, à lire avec les jours de renfort utilisés.
- **Formule :** départs survenus un jour de renfort ÷ départs de la période, pour une zone. Les jours de renfort sont donnés par une règle fixée avant la période (seuil calé sur les années de calage).
- **Toujours affiché à côté :** le nombre de jours de renfort réellement utilisés par saison, et le gain sur le hasard (part des départs couverts ÷ part des jours de renfort).
- **Indicateur secondaire :** le même taux pour les feux de 1 ha ou plus (10 % des feux font 85 % de la surface brûlée). FWI seul, Grand Est, test 2023-2025 : 6 sur 26.
- **Garde-fou 1 :** les jours de renfort utilisés ne dépassent pas le budget. Un taux qui monte parce que la règle a déclenché plus de jours ne compte pas.
- **Garde-fou 2 :** la précision, la part des jours de renfort avec au moins un départ. FWI seul, Grand Est, test 2023-2025 : 64 %. Elle ne doit pas baisser.
- **Contexte :** le nombre de départs de la période, les années non renseignées, la part des départs hors juin-septembre.

## 6. Ce que ça donne pour le seuil

- Dans le 67, le FWI moyen vaut environ 30 les jours « modéré » et 45 les jours « élevé » de la Météo des forêts.
- Un seuil de FWI calé pour 20 jours tombe entre 13 et 21 selon les années de calage, donc en dessous du niveau « modéré » dans tous les cas.
- Comme un seuil fixe ne tient pas le budget d'une saison à l'autre, la règle proposée au SDIS devra avoir deux parties : un seuil de FWI, et un plafond de jours par saison (ou un seuil revu chaque année sur les dernières saisons). C'est à tester sur les années de test, comme le reste.

## 7. Limites

- **Les « N meilleurs jours » sont un maximum théorique** : ils supposent de connaître toute la saison. Ils servent de plafond, pas de valeur de départ.
- **Le FWI de Copernicus est calculé avec la météo observée**, alors que le SDIS décide la veille avec une prévision. Une règle réelle ferait un peu moins bien que nos calculs.
- Le 67 est approché par un rectangle de mailles du FWI (latitudes 48,1 à 49,1, longitudes 7,0 à 8,3), tant que la table commune -> maille n'existe pas. Pour le Grand Est, c'est la moyenne de toutes les mailles.
- Le 67 n'a que 84 départs sur ses années renseignées, dont 14 sur 2023-2025. Les tests se font sur le Grand Est ; le 67 est donné pour information.
- Les jours de renfort sont simulés, pas relevés.
- Les chiffres ont été recalculés le 19/11 avec les fichiers FWI sur la grille d'origine (#45).
- Ils comptent encore le doublon probable de Haguenau (13/08/2025, règle B3, retiré dans `feux.csv` par #66). Sans lui, le test 2023-2025 du Grand Est donne 26 départs couverts sur 123, toujours 21 %, et 6 feux de 1 ha ou plus sur 25. Le 67 passe à 83 départs, dont 13 sur 2023-2025. Les chiffres de la fiche indicateur (`kpi/02_fiches_indicateurs.md`) sont ceux sans doublon.

## 8. À décider en groupe

1. **Les années de calage et de test, à fixer avant tout autre calcul** (proposition consignée dans le journal) : FWI seul, calage 2006-2016 et test 2017-2025 ; H3, qui a besoin des vacances scolaires, calage 2017-2022 et test 2023-2025 sur tout le Grand Est.
2. **Le budget de jours.** 20 par saison est un ordre de grandeur (le 67 a eu 50 jours « modéré » ou plus sur 2024-2026, dont 45 en 2026). Le chiffre réel viendra du SDIS (#41).
3. **Le plafond de jours dans la règle**, puisque le seuil seul ne tient pas le budget.
4. **Le week-end dans H3.** Les feux du week-end (29,3 %) sont dans la même proportion que les jours de week-end (28,6 %). Le week-end seul ne semble pas aider à prévoir ; les fériés et les vacances restent à tester. Ce chiffre a été regardé sur toutes les années, pas seulement sur la période de calage : c'est noté dans le journal.
5. **Qui porte quel KPI dans `kpi/`.** Proposition : le taux de départs couverts pour Lawson (Q3, Q4), la précision ou la gravité pour Denis, la concentration des départs pour Firas (Q1, #60).

## 9. Comment les chiffres ont été calculés

- **Feux :** export BDIFF du Grand Est, 2006-2025 (736 feux). Un départ = un feu, daté du jour de sa `Date de première alerte`. Surface : `Surface parcourue (m2)`.
- **Météo des forêts :** archives 2024 à 2026. Le niveau d'un jour est le `niveau_j1` publié la veille (date de diffusion + 1 jour), par `num_dep` (codes remis sur 2 chiffres).
- **FWI :** fichiers Copernicus 2006-2025 sur la grille d'origine (13 × 22 mailles), variable `fwinx`. Grand Est : moyenne de toutes les mailles. 67 : moyenne des mailles du rectangle de la partie 7.
- **Maximum théorique :** pour chaque année, les N jours de mars à octobre où le FWI est le plus haut ; on compte les feux tombés ces jours-là. Pour le 67, seulement les années où des feux sont saisis.
- **Seuil fixe :** la valeur de FWI dépassée en moyenne 20 jours sur les 245 jours de mars à octobre des années de calage. On l'applique tel quel aux années de test, et on compte les jours où il est dépassé et les feux tombés ces jours-là.
- **Week-end :** part des feux un samedi ou un dimanche, comparée à 2 jours sur 7.

Tout sera refait dans le pipeline une fois le nettoyage (#37) et la table commune -> maille prêts. Ces chiffres servent à cadrer le KPI, pas de résultat final.
