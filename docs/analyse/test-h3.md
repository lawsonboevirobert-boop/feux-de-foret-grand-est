# Test de H3 (#98)

Le protocole et la règle ont été figés le 25/11/2026, avant tout calcul sur les années de test (2023-2025). Ils sont dans ce fichier et dans [`h3/regle-calee.json`](h3/regle-calee.json), commités avant les résultats : l'historique git le montre. Les résultats sont dans la partie 5.

## 1. La question

- **Q3 :** le type de jour, l'historique du secteur et la part de résineux aident-ils à choisir les jours de renfort, en plus du FWI ?
- **H3** (journal du 18/11) : une règle qui combine ces trois variables avec le FWI couvre au moins 20 % de départs en plus que le FWI seul, à jours de renfort égaux
- **Années** (journal du 19/11) : calage 2017-2022, test 2023-2025, sur tout le Grand Est. Le 67 est donné pour information
- **Décision du SDIS :** à partir de quand lancer le dispositif renforcé, avec un nombre de jours limité par le budget

## 2. La valeur de départ, recalée sur le pipeline

Le FWI seul se lit maintenant avec le FWI du pipeline (#91), et non plus avec la moyenne de toutes les mailles du rectangle :

- **FWI du Grand Est :** chaque jour, le `fwi_moyen` de chaque département (déjà pondéré par la forêt de ses communes, `jour_departement.csv`), pondéré par la forêt du département. Ça revient à pondérer chaque commune par sa forêt
- **Seuil :** la valeur dépassée en moyenne 20 jours par saison (mars à octobre) sur 2017-2022 : **23,0**
- **Sur le test 2023-2025 :** **23 départs couverts sur 123 (18,7 %)**, **19 jours de renfort**, précision **74 %** (14 jours sur 19 avec au moins un départ)
- on retrouve les chiffres de la relecture de Firas sur #94, et le seuil de 23,0 de la fiche de Franck (#86) pour ces années
- l'ancien calcul (toutes les mailles du rectangle, #56) donnait 26 sur 123 et 25 jours

Ce que devient l'objectif SMART : au moins **28 départs couverts sur 123** (23 × 1,2 = 27,6, arrondi au-dessus), soit 23 %, avec **19 jours de renfort au plus**. La mise à jour de `kpi/` (kpi/01, kpi/02, jeu v0, objectifs retenus) se fait dans une PR à part.

## 3. La règle combinée

**Le secteur.** Les communes d'un département dans une maille du FWI (table commune → maille, #89) : 203 secteurs dans 139 mailles, dont 19 dans le 67. C'est le plus petit endroit où l'on a à la fois le FWI (la maille), le calendrier et le statut de la BDIFF (le département).

**Ce que prévoit la règle.** Pour chaque secteur et chaque jour de mars à octobre, un nombre de départs attendu, par une régression de Poisson sur :

| Variable | Ce que c'est | Source |
|---|---|---|
| FWI | `log(1 + FWI)` de la maille du secteur, ce jour-là | `fwi_maille.csv` (#91) |
| week-end | samedi ou dimanche | `calendrier.csv` |
| férié | jour férié, calendrier d'Alsace-Moselle pour le 57, le 67 et le 68 | `calendrier.csv` |
| vacances | vacances scolaires de l'académie du département | `calendrier.csv` |
| historique du secteur | `log(1 + départs par an)` : les départs du secteur sur les années renseignées de son département **avant** la saison (règle P1). Un département sans aucune année renseignée avant : le taux moyen du Grand Est par hectare de forêt, multiplié par la forêt du secteur | `feux_travail.csv`, `jour_departement.csv` |
| part de résineux | (conifères + 0,5 × mixte) ÷ forêt avec couvert, sur les communes du secteur (journal du 20/11) | `foret_commune.csv` |

**Le calage.** Sur les secteurs × jours de mars à octobre, de septembre 2017 à octobre 2022, seulement les années où la BDIFF du département est renseignée (P1) : 150 054 lignes, 451 départs. On commence en septembre 2017 parce que le calendrier scolaire commence à la rentrée 2017.

**Le score d'un jour.** La somme des départs attendus sur les 203 secteurs : le nombre de départs attendus dans le Grand Est ce jour-là. On fait la somme sur tous les secteurs, renseignés ou non : le jour de la décision, on ne sait pas si l'année sera saisie.

**Le seuil.** Comme pour le FWI seul : la valeur dépassée en moyenne 20 jours par saison, sur les saisons complètes du calage avec le calendrier scolaire (2018-2022) : **1,28 départ attendu**. On renforce les jours de mars à octobre où le score est au-dessus.

**Ce que la règle a appris sur 2017-2022** (multiplicateur du nombre de départs attendus) :

| Variable | Effet |
|---|---|
| FWI | × 3,7 quand le FWI passe de 5 à 25 ; × 2,5 de 10 à 30 |
| week-end | × 1,06 |
| férié | × 0,99 |
| vacances scolaires | × 1,50 |
| historique du secteur | × 2,6 entre un secteur à 1 départ par an et un secteur à 2 |
| part de résineux | × 1,16 pour 10 points de résineux en plus |

- le week-end et les fériés ne changent presque rien, comme la part des feux du week-end vue le 19/11
- l'historique pèse le plus, mais il mesure aussi la saisie : un département qui saisit beaucoup de feux a un historique élevé (voir les limites)
- la règle reste une règle à seuil fixe, comme le FWI seul. Le plafond de jours par saison est une autre question, à tester ensuite

## 4. Le critère, fixé avant le calcul

- **H3 est validée** si, sur 2023-2025, la règle combinée couvre **au moins 28 départs sur 123** avec **19 jours de renfort au plus**
- sinon, H3 n'est pas validée et on recommande le FWI seul, comme prévu dans l'objectif
- si la règle combinée déclenche plus de 19 jours, H3 n'est pas validée, même si elle couvre plus de départs. Pour information seulement, on donne ses 19 meilleurs jours du test : c'est un diagnostic, il suppose de connaître la saison
- **garde-fous, donnés à côté :** la précision (74 % au départ), la surface brûlée des départs couverts, les feux de 1 ha ou plus couverts
- **variantes calées en même temps, sans entrer dans le verdict :**
  - la part de résineux stricte, sans la forêt mixte (journal du 20/11)
  - le même modèle avec le FWI seul : dit si un écart vient des trois variables ou de la forme du modèle (FWI par maille, régression)
  - la règle sans le type de jour, sans l'historique, sans les résineux : la part de chaque variable
- **le 67 pour information :** 13 départs sur le test, sous le plancher de 20 du jeu v0
- **ce qu'on a déjà vu de 2023-2025 avant de figer la règle :** le FWI seul (la valeur de départ), la saison 2025 du 67 (journal du 18/11) et le nombre de départs par année. Rien sur la règle combinée
- aucun réglage ne sera changé après avoir vu le test. Si une erreur de code est trouvée après, on la corrige, on le dit, et on donne les deux résultats

## 5. Résultats

À venir : `python -m src.h3 tester`, après le commit de ce protocole.

## 6. Limites connues avant le test

- **L'historique mesure aussi la saisie.** La BDIFF est inégale selon les départements (les Vosges font la moitié des feux de la région). Une règle qui suit l'historique suit aussi les départements qui saisissent beaucoup. Pour le SDIS, c'est un vrai problème si sa propre saisie change
- **La météo observée.** Le FWI de Copernicus est calculé avec la météo du jour. Le SDIS décide la veille avec une prévision : une règle réelle ferait un peu moins bien, les deux règles de la même façon
- **3 saisons de test, 123 départs**, dont 10 en 2024 : un résultat qui se joue à 2 ou 3 départs reste fragile
- **Le seuil fixe ne tient pas le budget** d'une saison à l'autre (journal du 19/11) : les jours réellement utilisés sont toujours donnés à côté du taux

## Refaire le calcul

```
python -m src.nettoyage      # les tables de data/processed
python -m src.h3 caler       # recalcule regle-calee.json (même résultat si les données n'ont pas changé)
python -m src.h3 tester      # applique la règle figée à 2023-2025
python -m unittest tests.test_h3
```

Sous Windows, si la console refuse un caractère, lancer d'abord `set PYTHONIOENCODING=utf-8`.
