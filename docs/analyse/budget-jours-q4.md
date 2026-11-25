# Q4 : tenir le budget de jours de renfort (#102)

Protocole figé le 25/11/2026, avant tout calcul des quatre règles sur les années de test. Les résultats sont dans la partie 4, ajoutés dans un commit suivant.

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

À venir : `python -m src.q4`, après le commit de ce protocole.

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
