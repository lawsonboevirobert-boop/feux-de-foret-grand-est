# Q4 : tenir le budget de jours de renfort (#102)

Protocole figé le 25/11/2026, avant tout calcul des quatre règles sur les années de test. Les résultats sont dans la partie 4, ajoutés dans un commit suivant.

**Résultat :** le critère désigne le **seuil recalé avant chaque saison, avec un plafond de jours**. C'est la seule règle qui tient le budget chaque saison tout en suivant le réchauffement : 97 départs couverts sur 614 (16 %) avec 131 jours de renfort sur 9 saisons, jamais plus de 20 dans une saison. Le seuil fixe couvre plus, mais avec 396 jours (44 par saison, jusqu'à 90 en 2020).

## 1. La question

H3 n'est pas validée (#99) : on garde le FWI seul. Reste à savoir comment le transformer en jours de renfort sans sortir du budget.

- un seuil fixe calé pour 20 jours par saison sur 2006-2016 en donne 44 par saison sur 2017-2025 (fiche de Franck, #86, et #101). Les saisons récentes sont plus chaudes
- sur 2023-2025, le seuil calé sur 2017-2022 en donne 14, 0 et 5 : aucune saison ne dépasse le budget, un plafond ne s'y teste pas
- on prend donc les années du journal du 19/11 pour le FWI seul : **calage 2006-2016, test 2017-2025**, Grand Est. Le 67 est donné pour information

## 2. Les quatre règles

Toutes utilisent le FWI moyen du Grand Est, pondéré par la forêt (#91), et renforcent les jours de mars à octobre au-dessus d'un seuil. Le budget est de **20 jours par saison** (supposé, #41), avec 10 et 30 en sensibilité.

| Règle | Seuil | Plafond |
|---|---|---|
| seuil fixe | calé une fois sur 2006-2016 pour 20 jours par saison | aucun |
| seuil fixe avec plafond | le même | on arrête après 20 jours dans la saison |
| seuil recalé chaque saison | avant chaque saison, recalé pour 20 jours par saison sur les 11 saisons qui la précèdent (2017 sur 2006-2016, 2018 sur 2007-2017, etc.) | aucun |
| seuil recalé avec plafond | le même | on arrête après 20 jours dans la saison |

- le plafond prend les jours dans l'ordre du calendrier. Le jour de la décision, on ne sait pas si la fin de saison sera pire : une saison chaude au printemps peut épuiser le budget avant l'été, et c'est voulu
- le seuil recalé n'utilise que des saisons passées, comme le SDIS pourrait le faire chaque hiver

## 3. Le critère, fixé avant le calcul

- **règle recommandée :** parmi les règles qui ne dépassent le budget dans **aucune** saison, celle qui couvre le plus de départs sur 2017-2025
- à moins de 5 % d'écart de départs couverts, on prend la plus simple : d'abord le seuil fixe avec plafond, puis le seuil recalé avec plafond
- donnés à côté : les jours par saison, la saison la plus chargée, la précision, le gain sur le hasard, les feux de 1 ha ou plus couverts
- un départ couvert est un départ de feu de la BDIFF parti un jour de renfort. Les départs de toute l'année comptent au dénominateur (614 départs sur 2017-2025, sans le doublon de Haguenau)
- **déjà vu avant de figer :** le seuil fixe sur 2017-2025 (44 jours par saison, fiche de Franck) et les jours par saison de 2018-2025 avec le seuil calé sur 2017-2022 (#99). Rien sur les trois autres règles
- aucun réglage ne sera changé après le calcul

## 4. Résultats

Calculés le 25/11/2026 avec `python -m src.q4`, après le commit du protocole. Détail dans [`q4/resultats.csv`](q4/resultats.csv) et [`q4/jours-par-saison.csv`](q4/jours-par-saison.csv).

### Budget de 20 jours par saison, Grand Est 2017-2025 (614 départs)

| Règle | Départs couverts | Jours de renfort | Saison la plus chargée | Saisons au-dessus du budget | Précision | Gain sur le hasard | Feux de 1 ha ou plus couverts |
|---|---|---|---|---|---|---|---|
| seuil fixe | 312 (51 %) | 396 | 90 jours (2020) | 7 sur 9 | 39 % | × 2,8 | 91 sur 135 |
| seuil fixe avec plafond | 78 (13 %) | 147 | 20 | 0 | 33 % | × 1,9 | 15 sur 135 |
| seuil recalé chaque saison | 254 (41 %) | 286 | 75 jours (2018) | 6 sur 9 | 41 % | × 3,2 | 72 sur 135 |
| **seuil recalé avec plafond** | **97 (16 %)** | **131** | **20** | **0** | 38 % | × 2,7 | 21 sur 135 |

- **règle recommandée** (critère de la partie 3) : le seuil recalé avec plafond. Les deux règles avec plafond tiennent le budget ; celle-ci couvre 19 départs de plus (+ 24 %) avec 16 jours de moins
- même résultat avec un budget de 10 jours (56 départs couverts contre 50) et de 30 jours (137 contre 122)
- **le seuil fixe** couvre la moitié des départs, mais il déclenche 44 jours par saison en moyenne, plus du double du budget, et 90 jours en 2020. Il n'est pas tenable
- **le plafond seul** tient le budget, mais il le dépense trop tôt : avec un seuil de 14,1 calé sur des années plus fraîches, les 20 jours partent au printemps ou au début de l'été, avant les pires journées. Son gain sur le hasard tombe à × 1,9
- **le seuil recalé seul** suit le réchauffement (14,1 en 2017, 20,4 en 2025), mais il déborde encore 6 saisons sur 9 : le recalage a un temps de retard sur une saison exceptionnelle
- **les deux ensemble** : le seuil recalé garde les jours de renfort pour les journées vraiment chaudes, et le plafond coupe les saisons exceptionnelles

### Saison par saison, règle recommandée

| Saison | Seuil de FWI | Jours de renfort | Départs | Départs couverts |
|---|---|---|---|---|
| 2017 | 14,1 | 20 | 16 | 1 |
| 2018 | 14,2 | 20 | 8 | 1 |
| 2019 | 16,2 | 20 | 48 | 2 |
| 2020 | 17,8 | 20 | 175 | 22 |
| 2021 | 19,6 | 0 | 70 | 0 |
| 2022 | 19,4 | 20 | 174 | 43 |
| 2023 | 20,0 | 20 | 55 | 17 |
| 2024 | 20,6 | 0 | 10 | 0 |
| 2025 | 20,4 | 11 | 58 | 11 |

- en 2021 et 2024, saisons fraîches et humides, le FWI ne dépasse jamais le seuil : aucun jour de renfort, et le budget n'est pas dépensé. 2021 a pourtant 70 départs saisis, presque tous des jours où le FWI était bas
- 2020 et 2022 font plus de la moitié des départs de la période (349 sur 614) : le résultat dépend surtout de ces deux étés

### Le 67, pour information

63 départs sur 2017-2025 : la règle recommandée en couvre 19, le seuil fixe 39 (avec 396 jours), le seuil fixe avec plafond 15.

### Ce que ça veut dire pour le SDIS

- **la règle :** avant chaque saison, recaler le seuil de FWI sur les 11 saisons précédentes pour viser le budget de jours, puis déclencher le renfort les jours au-dessus du seuil, jusqu'à épuisement du budget de la saison. Pour 2026, le seuil serait recalé sur 2015-2025
- **ce qu'on peut en attendre :** avec 20 jours par saison, environ un départ sur six tombe un jour de renfort. La plupart des départs partent des jours où le FWI n'est pas exceptionnel (2021 en est l'exemple). Le renfort sert les journées les plus dangereuses ; la prévention et la surveillance du reste de l'année restent nécessaires
- **en niveaux de la Météo des forêts :** un FWI de 20 est un jour « modéré » plutôt bas dans le 67 (médiane des jours « modéré » : 27). Déclencher au niveau « modéré » s'en approche, mais sans plafond le niveau « modéré » ne tient pas le budget non plus : 54 jours « modéré » ou « élevé » dans le 67 en 2026, de juin à septembre
- **le chiffrage en euros** attend le coût d'un jour de renfort et le budget réel du SDIS (#41). Les jours sont donnés pour 10, 20 et 30 jours par saison, pour que le SDIS lise la ligne de son budget

## 5. Limites connues avant le calcul

- **le coût :** le coût d'un jour de renfort n'est pas connu (#41). Les résultats sont en jours ; le SDIS les multiplie par son coût
- **les années non renseignées :** certains départements n'ont aucun feu saisi certaines années (règle P1). Leurs feux manquent au numérateur comme au dénominateur, et la précision est sous-estimée ces années-là
- **la météo observée :** comme pour H3, le FWI de Copernicus est calculé avec la météo du jour, alors que le SDIS décide la veille
- **un seul seuil pour la région :** les jours de renfort sont décidés pour tout le Grand Est. Le seuil propre au 67 n'apporte rien (fiche de Franck, −10 %)

## Refaire le calcul

```
python -m src.nettoyage
python -m src.q4
python -m unittest tests.test_q4
```
