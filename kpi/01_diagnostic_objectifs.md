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
| Stratégie | Que veut faire l'organisation ? Quel est son objectif ? | Préparer la saison feux 2027 et lutter contre les départs de feu dans le Bas-Rhin, en choisissant où mettre ses moyens et quand lancer le dispositif renforcé | établi | la commande ([README](../README.md#la-commande), [analyse globale](../docs/analyse/analyse-globale.md#la-commande)) |
| Enjeu | Qu'est-ce qui bloque ? Qui s'oppose ? Qui contraint ? | **Ce qui contraint :** le budget ne permet pas de renforcer tout le département tout l'été (établi, commande). La Météo des forêts n'est publiée que de juin à septembre, alors que 43,5 % des feux du Grand Est partent hors de ces mois (établi, 320 sur 735). **Ce qui bloque :** les chefs de centre reprochent au seuil actuel des fausses alertes et des feux manqués (établi comme reproche, commande). Que ce reproche se vérifie dans les données : supposé, c'est l'hypothèse stratégique ci-dessous. **Qui s'oppose :** personne d'identifié. Les chefs de centre critiquent le seuil mais demandent un meilleur outil, ils ne s'opposent pas au renfort (supposé) | établi pour le budget, le calendrier de publication et le reproche ; supposé pour le reste | commande ; [jeu v0](02_fiches_indicateurs.md) (43,5 % hors juin-septembre) ; montant du budget et seuil actuel à demander au SDIS (#41) |
| Objectif | Quel résultat vise-t-on ? | Avec un nombre de jours de renfort fixé par le budget, couvrir plus de départs de feu, et mettre les moyens fixes là où ils partent | supposé : la commande demande d'arbitrer, elle ne donne pas de résultat chiffré. Les chiffres sont les nôtres | partie 2 et [jeu v0](02_fiches_indicateurs.md) : 21 % de départs couverts aujourd'hui avec le FWI seul (Lawson), 27 % dans les 10 communes prioritaires (Firas) |
| Action | Que décide-t-on ? Que fait-on ? | Choisir le niveau de déclenchement du dispositif renforcé (patrouilles, guet) et les secteurs où concentrer les moyens. Selon les causes, mettre une partie du budget dans la prévention | établi pour le seuil et les secteurs (commande) ; supposé pour la prévention (vient de notre Q2) ; supposé aussi pour le contenu exact du dispositif et le coût d'une journée | commande ; [analyse globale](../docs/analyse/analyse-globale.md#nos-questions) (Q2) ; demande au SDIS (#41) |

### Hypothèse stratégique

Sur un niveau supposé du tableau.

- **Niveau concerné :** Enjeu
- **Hypothèse :** le reproche des chefs de centre se vérifie. Avec le seuil actuel, qu'il soit à « modéré » ou à « élevé » (sa valeur n'est pas publique), la plupart des départs de feu partent un jour où le renfort n'est pas déclenché
- **La pièce qui la fonde :** la commande (les chefs de centre reprochent des jours à danger élevé sans feu et des feux les jours où l'indice est au plus bas), et l'[analyse globale](../docs/analyse/analyse-globale.md#points-dattention) : en 2025, le 67 a eu 115 jours « faible » et 5 « modéré », jamais « élevé »
- **Confirmée si :** plus de la moitié des départs partis pendant la publication de la Météo des forêts tombent un jour sous le seuil, avec un seuil à « modéré » comme à « élevé ». Lu sur au moins 20 départs (plancher du jeu v0), donc sur le Grand Est
- **Infirmée si :** la majorité de ces départs tombent un jour à « modéré » ou plus
- **Verdict :** confirmée sur le Grand Est.
  - 2024-2025, Grand Est : 46 départs pendant la publication, dont 37 un jour « faible » (80 %)
  - seuil à « modéré » : 9 départs couverts sur 46 (20 %), pour 69 jours × département de renfort, dont 62 sans aucun feu (précision 10 %)
  - seuil à « élevé » : 1 départ couvert sur 46, pour 2 jours de renfort
  - dans le 67 seul, pour information (8 départs, sous le plancher) : 5 sur 8 un jour « faible ». « Élevé » n'a été atteint aucun jour en 2024 et 2025, et 6 jours en 2026
  - les fausses alertes et les feux manqués sont donc vrais tous les deux, et en plus 43,5 % des feux partent hors de juin à septembre, sans bulletin du tout
- **Limites :**
  - 2 saisons seulement : la BDIFF 2026 n'est pas encore publiée, et 2026 est justement la saison avec le plus de jours « modéré » et « élevé » (49 et 6 dans le 67)
  - le seuil actuel du SDIS n'est pas connu : on teste les deux valeurs possibles, à confirmer avec eux (#41)
  - la BDIFF ne contient que les feux saisis : les petits feux éteints vite peuvent manquer
  - la Météo des forêts est donnée par département : un jour « faible » pour le département peut être plus dangereux dans un massif

Chiffres calculés le 22/11/2026 sur `feux.csv` (735 feux, sans le doublon de Haguenau) et `meteo_des_forets.csv` (2024-2026, niveau décalé au lendemain, règle M5).

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
