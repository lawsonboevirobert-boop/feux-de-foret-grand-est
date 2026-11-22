# Diagnostic et objectifs (UE01.B, séance 1)

Le livrable de la séance 1 : le diagnostic du groupe, l'objectif de chacun, puis les objectifs retenus. Le PDF ne donne pas de nom de fichier (« dans kpi/ ») : on suit la numérotation de `02_fiches_indicateurs.md`.

Qui commite quoi :
- partie 1 (diagnostic) et partie 3 (objectifs retenus) : commits de groupe
- partie 2 : chacun écrit sa section et la commite depuis son compte. Un commit par objectif

Un niveau est **établi** s'il s'appuie sur une citation de la commande ou un résultat de nos analyses (avec le lien), sinon il est **supposé**. Une valeur de départ qu'on n'a pas s'écrit « à mesurer », jamais inventée.

## 1. Diagnostic (groupe)

### Les quatre niveaux

| Niveau | Question | Pour le SDIS 67 | Établi ou supposé | Sur quoi ça s'appuie |
|---|---|---|---|---|
| Stratégie | Que veut faire l'organisation ? Quel est son objectif ? | | | |
| Enjeu | Qu'est-ce qui bloque ? Qui s'oppose ? Qui contraint ? | | | |
| Objectif | Quel résultat vise-t-on ? | | | |
| Action | Que décide-t-on ? Que fait-on ? | | | |

### Hypothèse stratégique

Sur un niveau supposé du tableau.

- **Niveau concerné :**
- **Hypothèse :**
- **La pièce qui la fonde :**
- **Confirmée si :**
- **Infirmée si :**
- **Verdict** (confirmée, infirmée, ou les données ne permettent pas de trancher) :
- **Limites :**

## 2. Objectifs individuels

Pour chacun, dans cet ordre :

1. **Question analytique** (Q1 à Q5 de l'[analyse globale](../docs/analyse/analyse-globale.md)) et **décision** que la réponse permet de prendre
2. **Trois formulations**, chacune complète la précédente :
   - une action (ce n'est pas un objectif)
   - un objectif, pas encore SMART
   - un objectif SMART : un résultat, une échéance, une condition
3. **Le SMART critère par critère** : spécifique, mesurable, atteignable, réaliste, temporel
4. **Situation de référence** : la valeur de départ, avec son calcul, ou « à mesurer »
5. **Test de cohérence** : comment pourrait-on atteindre l'objectif sans faire avancer la stratégie ?

### Firas

### Lawson

### Denis

- **Question (Q2) :** quelle part des départs de feu a une cause humaine, et laquelle (travaux, particuliers, malveillance, accident) ?
- **Décision du SDIS :** quelle part du budget va à la prévention plutôt qu'à la lutte, et sur quel levier de prévention : sensibilisation et règles pour les travaux et les particuliers, surveillance contre la malveillance, entretien le long des lignes électriques et des routes

Les trois formulations :

1. **Action :** donner au SDIS la répartition des causes des départs de feu
2. **Objectif :** dire au SDIS sur quel levier de prévention mettre l'argent, à partir des causes connues
3. **Objectif SMART :** d'ici le rendu du 11 décembre 2026, montrer au SDIS 67, sur les départs du Grand Est 2006-2025 dont la cause est connue, que la cause involontaire (travaux ou particulier) reste au-dessus de 50 % dans chaque sous-ensemble fixé à l'avance (sans les Ardennes, feux de 1 ha ou plus, 2019-2025), toujours affichée avec le taux de cause renseignée

Le SMART critère par critère :

- **Spécifique :** les départs de cause connue du Grand Est, regroupés en 4 leviers (involontaire, malveillance, accidentelle, naturelle)
- **Mesurable :** la part involontaire, et le taux de cause renseignée à côté
- **Atteignable :** sur les données BDIFF, les sous-ensembles donnent déjà entre 57 % et 62 % (kpi/02). Le vrai test, ce sont les causes du SDIS 67 si on les reçoit (#41) : elles seront jugées avec la même règle, sans la changer
- **Réaliste :** tout se calcule avec `feux.csv`. Le 67 seul n'a que 13 causes connues : il est donné pour information, pas comme preuve
- **Temporel :** le rendu du 11/12/2026. La BDIFF 2026 ne sort qu'en 2027

**Situation de référence :**

- Grand Est 2006-2025 : 58 départs de cause involontaire sur 97 de cause connue = **60 %**
- taux de cause renseignée : 97 sur 735 = **13,2 %**
- dans le 67 : 13 causes connues sur 83 départs (15,7 %), dont 5 involontaires. Sous le plancher de 20 causes connues : **à mesurer** avec les données du SDIS 67 (#41)

**Test de cohérence** (comment atteindre l'objectif sans faire avancer la stratégie) :

- choisir après coup le sous-ensemble qui arrange : les Ardennes seules donnent 67 % d'involontaire
- compter les causes « accidentelle » avec les involontaires pour passer au-dessus de 50 %
- atteindre 60 % sur 13 % des feux sans rien dire des 87 % autres : si les feux sans cause sont différents (petits feux, écobuage non déclaré), la prévention vise à côté

Les sous-ensembles et le regroupement en leviers sont donc fixés ici, et le taux de cause renseignée est toujours affiché à côté.

### Franck

**1. Question et décision**

- **Question (Q5) :** l'indice se comporte-t-il dans le Bas-Rhin comme dans le reste du Grand Est ? Hypothèse H5 : le bon seuil n'est pas le même d'un département à l'autre (climat, végétation)
- **Décision du SDIS :** garder le seuil régional pour lancer le dispositif renforcé, ou prendre un seuil propre au Bas-Rhin. Lawson dit à partir de quel niveau renforcer dans le Grand Est (Q3, Q4) ; mon objectif dit si ce niveau vaut aussi pour le 67

**2. Trois formulations**

| | Formulation |
|---|---|
| Action | Caler un seuil de déclenchement sur le Bas-Rhin seul et le comparer au seuil régional |
| Objectif | Dire au SDIS 67 si un seuil propre couvre nettement plus de départs que le seuil régional, pour le même nombre de jours de renfort |
| Objectif SMART | D'ici le rendu du 11 décembre 2026, sur les années de test 2017-2025 (FWI seul, calage 2006-2016, journal du 19/11), dans le Bas-Rhin, année entière : mesurer le taux de départs couverts avec le seuil de FWI régional et avec un seuil calé sur le 67 seul, les deux calés pour 20 jours de renfort par saison. Le seuil propre est recommandé s'il couvre au moins 20 % de départs en plus que le seuil régional, sans utiliser plus de jours de renfort. Sinon, on garde le seuil régional |

**3. Le SMART critère par critère**

| Critère | Pourquoi |
|---|---|
| Spécifique | une zone (le 67), deux règles (seuil régional, seuil propre), un budget (20 jours par saison, le même que Lawson), des années fixées avant le calcul |
| Mesurable | deux taux de départs couverts calculés comme le KPI de Lawson (`feux.csv` et FWI de Copernicus), et l'écart entre les deux. Les jours de renfort réellement utilisés sont comptés pour chaque règle |
| Atteignable | le calage n'utilise que le FWI (on compte des jours au-dessus d'un seuil), pas les feux. Les années vides de la BDIFF dans le 67 ne gênent donc pas le calage. Le test a 63 départs dans le 67, au-dessus du plancher de 20 |
| Réaliste | tout se calcule avec `feux.csv`, le FWI et la table commune → maille (#62, ma tâche). En attendant #62, le 67 est le rectangle de mailles déjà utilisé par Lawson |
| Temporel | le rendu du 11/12/2026. Le seuil retenu vaudrait pour la saison 2027, mais la BDIFF 2027 ne sortira qu'en 2028 : le suivi de la saison passera par les interventions du SDIS 67 (#41) |

Pourquoi 20 % de plus : c'est le gain que H3 demande à la règle combinée. Un seuil propre complique le dispositif (deux règles à suivre au lieu d'une) : il faut un gain net pour le justifier, pas un point de plus.

**4. Situation de référence**

- taux de départs couverts du 67 avec le seuil régional, et avec le seuil propre : **à mesurer**. Il faut le FWI de 2006 à 2025 (je n'ai en local que 2016 à 2022 ; le reste se récupère avec `python -m src.recuperation copernicus`, qui demande une clé) et la zone du 67 (#62)
- départs du 67 sur le test 2017-2025 : **63** (22 en 2020, 28 en 2022, 2 en 2023, 1 en 2024, 10 en 2025). 2017, 2018, 2019 et 2021 sont « non renseigné » (règle P1)
- établi avec la Météo des forêts, qui a la même échelle partout (2024-2026) : le niveau « modéré » ou plus a été atteint 60 jours dans le 67, contre 50 dans les Vosges et 110 dans la Marne. Un même seuil ne donne donc pas le même nombre de jours de renfort selon le département
- au niveau « modéré », en 2024-2025 : 3 départs couverts sur 8 dans le 67, 6 sur 38 dans le reste du Grand Est. Le 67 est sous le plancher de 20 : donné pour information, pas comme preuve

**5. Test de cohérence : atteindre l'objectif sans faire avancer la stratégie**

- **comparer à jours inégaux** : un seuil propre plus bas déclenche plus de jours et couvre forcément plus de départs. D'où la condition « sans utiliser plus de jours de renfort », avec les jours réellement utilisés comptés pour chaque règle
- **choisir la zone du 67 après avoir vu le résultat** (rectangle de mailles, mailles des communes, seulement les communes boisées) : la zone est fixée ici, c'est celle de la table commune → maille (#62, règle F4)
- **deux étés font le résultat** : 50 des 63 départs du test sont en 2020 et 2022. Un seuil propre peut gagner grâce à ces deux saisons seulement. Le résultat est donc toujours affiché année par année à côté du total
- **gagner dans le 67 en perdant ailleurs** : un seuil propre ne dit rien des 9 autres départements. Si chacun prend le sien, le budget régional de jours n'est plus tenu. L'objectif porte sur le 67, mais le nombre total de jours du Grand Est est affiché à côté

## 3. Objectifs retenus (groupe)

Mise en commun des objectifs de la partie 2, doublons fusionnés : 3 à 5 objectifs, repris en séance 2 (fiches indicateurs) puis classés en séance 4.

| # | Objectif retenu | Question | Porté par | Fiche indicateur |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
