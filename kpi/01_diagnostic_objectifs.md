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

**1. Question et décision**

- **Question (Q1) :** où et quand partent les feux dans le Bas-Rhin ? Hypothèse H1 : ils se concentrent sur une minorité de communes ou de massifs. Mon objectif porte sur le **où** ; le **quand** est porté par Lawson (Q3, Q4)
- **Décision que la réponse permet de prendre :** mettre des moyens fixes (guet, patrouilles prépositionnées) sur quelques secteurs, ou miser sur des moyens mobiles partout. Le budget ne permet pas de renforcer tout le département (commande)

**2. Trois formulations**

| | Formulation |
|---|---|
| Action | Désigner avant chaque saison des « secteurs prioritaires » où le SDIS renforce la prévention et la surveillance |
| Objectif | Que les secteurs prioritaires reçoivent une grosse part des départs de feu tout en restant une petite part du département |
| Objectif SMART | Bas-Rhin, saisons 2026 et 2027 cumulées (1er mars au 31 octobre), et la suivante tant qu'on n'a pas 20 départs : les 10 communes prioritaires, classées sur les 5 saisons renseignées de 2020 à 2025 (avant les saisons mesurées), reçoivent au moins 27 % des départs de feu de la BDIFF, en couvrant au plus 10 % de la surface du département |

**3. Le SMART critère par critère**

| Critère | Pourquoi |
|---|---|
| Spécifique | un territoire (le 67), une liste fixée (10 communes), un type d'événement (les départs de feu de la BDIFF), des saisons (mars à octobre, 2026 et 2027 cumulées) |
| Mesurable | un rapport de deux comptages : départs dans les communes prioritaires ÷ départs du 67. Les deux viennent de `feux.csv` (#66). La surface vient des contours des communes |
| Atteignable | c'est la valeur déjà observée en 2024-2025 avec la même règle (27 %). On ne demande pas de progrès, on demande que la liste tienne sur de nouvelles saisons |
| Réaliste | 10 % du 67, c'est environ 48 000 ha : un périmètre que des patrouilles et un guet peuvent couvrir. La liste actuelle en fait 8,3 % |
| Temporel | les saisons 2026 et 2027, lues ensemble : environ 5 à 10 départs par saison dans le 67, donc une seule saison passe rarement le plancher de 20 du jeu v0 (#85). On ajoute une saison tant qu'on n'a pas 20 départs. On ne mesure pas 2024-2025, qui servent au classement. Limite : la BDIFF 2027 ne sera publiée qu'en 2028 ; pour suivre la saison en cours, il faudra les interventions du SDIS 67 (#41) |

**4. Situation de référence**

- **27 %** : 3 départs sur 11 en 2024-2025 tombent dans les 10 communes classées sur 2020-2023 (saison mars-octobre, doublon de Haguenau retiré, règle B3)
- la liste couvre 8,3 % de la surface du Bas-Rhin
- règle de classement, écrite avant le calcul : nombre de départs, puis surface brûlée, puis code commune
- détail et historique de la valeur (42 %, puis 33 %, puis 27 %) dans [la fiche indicateur](02_fiches_indicateurs.md)

**5. Test de cohérence : atteindre l'objectif sans faire avancer la stratégie**

- **la sous-saisie** : si les feux sont mieux saisis dans certaines forêts (domaniales, ONF), ces communes restent en tête. Le taux est atteint, mais les vrais départs sont ailleurs et les moyens fixes sont au mauvais endroit
- **les grandes communes** : une commune très boisée (Haguenau, 84 % de forêt d'après `foret_commune.csv`, #79) a plus de feux juste parce qu'elle est grande. En ajoutant des grandes communes, on monte le taux sans mieux cibler. D'où la limite de 10 % de la surface
- **choisir la liste après avoir vu la saison** : on atteint n'importe quel taux. D'où la règle « classement avant la saison », écrite dans la fiche
- **l'effet inverse** : si la prévention marche dans un secteur prioritaire, il y a moins de feux, et le taux baisse alors que la stratégie avance. Le taux seul ne suffit pas à juger, il se lit avec le nombre de départs

### Lawson

**1. Question et décision**

- **Questions (Q4, Q3) :** pour chaque seuil, combien de jours de renfort, de départs couverts, de fausses alertes (Q4) ? Une règle qui ajoute à l'indice le type de jour, l'historique du secteur et la part de résineux fait-elle mieux que l'indice seul (Q3) ? Hypothèse H3 : la règle combinée couvre au moins 20 % de départs en plus que l'indice seul, à jours de renfort égaux. Mon objectif porte sur le **quand** ; le **où** est porté par Firas (Q1)
- **Décision que la réponse permet de prendre :** à partir de quand lancer le dispositif renforcé (patrouilles, guet), avec un nombre de jours limité par le budget (commande)

**2. Trois formulations**

| | Formulation |
|---|---|
| Action | Choisir les jours de renfort avec une règle calée sur les données, au lieu d'un niveau fixe de la Météo des forêts |
| Objectif | Avec le même nombre de jours de renfort, couvrir plus de départs de feu |
| Objectif SMART | D'ici le rendu du 11 décembre 2026, montrer sur les années de test 2023-2025, dans le Grand Est, qu'une règle de déclenchement calée sur 2017-2022 couvre au moins 25 % des départs de feu, sans utiliser plus de jours de renfort que le FWI seul (25 jours sur les 3 saisons) |

**3. Le SMART critère par critère**

| Critère | Pourquoi |
|---|---|
| Spécifique | une zone (le Grand Est), une mesure (la part des départs de feu couverts par un jour de renfort), des années fixées avant le calcul (calage 2017-2022, test 2023-2025), un budget de jours (25 sur les 3 saisons de test) |
| Mesurable | un rapport de deux comptages : départs partis un jour de renfort ÷ départs de 2023-2025. Les départs viennent de `feux.csv` (#66), le FWI de Copernicus (#37). Tout se calcule sur le passé, sans attendre la BDIFF 2027 |
| Atteignable | la valeur de départ est 21 % avec le FWI seul. 25 %, c'est 21 % plus le gain de 20 % que teste H3 : au moins 31 départs couverts sur 123 |
| Réaliste | même nombre de jours, donc même coût pour le SDIS : seul le choix des jours change. Les variables ajoutées sont publiques (calendrier, historique des feux, part de résineux) |
| Temporel | le résultat est donné au rendu du 11/12/2026. La saison 2027 sert au suivi, pas à la preuve : la BDIFF 2027 ne sera publiée qu'en 2028 |

**4. Situation de référence**

- **21 %** : 26 départs sur 123, Grand Est, 2023-2025, avec le FWI seul calé sur 2017-2022 (doublon de Haguenau retiré, règle B3)
- 25 jours de renfort sur les 3 saisons de test, soit 8 par saison, et 64 % de ces jours ont eu au moins un départ (précision)
- le 67 seul n'a que 13 départs saisis sur 2023-2025 : le résultat s'y jouerait à un ou deux feux, il est donné pour information
- le budget réel de jours du SDIS est **à mesurer** (#41). En attendant, on suppose 20 jours par saison
- détail du calcul dans [la fiche indicateur](02_fiches_indicateurs.md) et dans [le seuil et le KPI](../docs/analyse/seuil-et-kpi.md)

**5. Test de cohérence : atteindre l'objectif sans faire avancer la stratégie**

- **plus de jours** : avec 15 jours par saison au lieu de 8, le FWI seul passe déjà de 21 % à 35 %. Si la règle combinée dépasse le budget, elle gagne par le nombre de jours et pas par leur choix. D'où le plafond de 25 jours, écrit dans l'objectif
- **recaler après coup** : changer les années de calage après avoir vu le test donne le taux qu'on veut. Les années, la période et la définition d'un départ couvert sont dans le journal (19/11) avant le calcul
- **réduire la période** : ne compter que mars à octobre fait gagner un point (22 % au lieu de 21 %). On garde l'année entière
- **le Grand Est au lieu du 67** : la règle peut gagner sur le Grand Est sans gagner dans le Bas-Rhin, qui est celui qui décide. Le seuil propre au 67 est testé à part (objectif de Franck, Q5)
- **couvrir n'est pas protéger** : un départ couvert veut dire que le renfort était là ce jour-là, pas que le feu a été éteint plus tôt ni que la surface brûlée baisse. Le taux peut monter sans que les dégâts diminuent : on le lit avec la surface brûlée des départs couverts
- **la météo observée** : la règle est testée avec le FWI calculé sur la météo du jour, alors qu'en vrai le SDIS décide la veille avec une prévision. Le taux est un maximum, une règle réelle fera un peu moins

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
| Réaliste | tout se calcule avec `feux.csv`, le FWI et la table commune → maille (#62, ma tâche, faite dans #89) |
| Temporel | le rendu du 11/12/2026. Le seuil retenu vaudrait pour la saison 2027, mais la BDIFF 2027 ne sortira qu'en 2028 : le suivi de la saison passera par les interventions du SDIS 67 (#41) |

Pourquoi 20 % de plus : c'est le gain que H3 demande à la règle combinée. Un seuil propre complique le dispositif (deux règles à suivre au lieu d'une) : il faut un gain net pour le justifier, pas un point de plus.

**4. Situation de référence**

- taux de départs couverts du 67 sur le test 2017-2025, calculé le 22/11 (FWI moyen pondéré par la forêt, journal du 22/11) : seuil régional (14,1) **39 sur 63 (62 %)**, avec 44 jours de renfort par saison ; seuil propre (13,2) **35 sur 63 (56 %)**, avec 40 jours. Écart : **−10 %**, soit 4 départs de moins pour 4 jours de moins par saison. Rapportées aux jours utilisés, les deux règles font pareil (environ 3,4 fois mieux que le hasard). On est loin des +20 % : on garde le seuil régional. Détail et contrôles dans la fiche (`kpi/02`)
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
| 1 | D'ici le 11/12/2026, montrer sur les années de test 2023-2025, dans le Grand Est, qu'une règle de déclenchement calée sur 2017-2022 couvre au moins 25 % des départs de feu, sans plus de jours de renfort que le FWI seul (25 jours sur les 3 saisons). Départ : **21 %** | Q3, Q4 (H3) | Lawson | taux de départs couverts |
| 2 | D'ici le 11/12/2026, dire au SDIS 67 si un seuil propre au Bas-Rhin couvre au moins 20 % de départs en plus que le seuil régional, sans plus de jours de renfort (test 2017-2025). Départ : **−10 %**, on garde pour l'instant le seuil régional | Q5 (H5) | Franck | écart entre le seuil propre et le seuil régional (#86) |
| 3 | Bas-Rhin, saisons 2026 et 2027 cumulées : les 10 communes prioritaires, classées avant la saison, reçoivent au moins 27 % des départs de feu, en couvrant au plus 10 % du département. Départ : **27 %** (3 sur 11) | Q1 (H1) | Firas | part des départs dans les secteurs prioritaires |
| 4 | D'ici le 11/12/2026, montrer que la cause involontaire reste au-dessus de 50 % des causes connues dans chaque sous-ensemble fixé à l'avance, toujours affichée avec le taux de cause renseignée. Départ : **60 %** (58 sur 97), avec 13,2 % de causes renseignées | Q2 | Denis | part des départs de cause involontaire |

Les fiches sont dans [02_fiches_indicateurs.md](02_fiches_indicateurs.md).

**Comment on a fusionné**

- Chaque objectif répond à une décision différente du SDIS : **quand** renforcer (1), **avec quel seuil dans le 67** (2), **où** placer les moyens fixes (3) et **contre quoi** faire de la prévention (4). Il n'y a pas de doublon
- Les objectifs 1 et 2 portent sur le même dispositif. On les garde séparés, parce que le 2 ne mesure pas le niveau de couverture : il dit si le seuil du 1 vaut aussi pour le 67. Il se lit avec le 1, avec la même définition d'un départ couvert et le même budget de jours
- Le 3 vient après le 1 : une fois le jour décidé, il dit où envoyer les moyens

**Ce qui vaut pour les 4** : les [règles communes du jeu v0](02_fiches_indicateurs.md) s'appliquent toutes :

- même table de feux (`feux.csv`)
- plancher de 20 départs ou causes connues
- années de calage et de test fixées avant les calculs
- toujours un nombre à côté d'un taux
