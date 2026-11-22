# Fiches indicateurs (UE01.B, séance 2)

Une partie par membre, sur son objectif. Le jeu d'indicateurs v0 du groupe est à la fin.

## Firas : où concentrer les moyens (Q1)

### Objectif (rappel)

- **Question (Q1) :** où et quand partent les feux dans le Bas-Rhin ? Hypothèse H1 : ils se concentrent sur une minorité de communes ou de massifs
- **Décision du SDIS :** mettre des moyens fixes (guet, patrouilles prépositionnées) sur quelques secteurs, ou miser sur des moyens mobiles partout
- **Action :** désigner avant la saison des « secteurs prioritaires » où on renforce la prévention et la surveillance
- **Objectif :** que les secteurs prioritaires captent une grosse part des départs tout en restant une petite part du département
- **Objectif SMART :** Bas-Rhin, saisons 2026 et 2027 cumulées (1er mars au 31 octobre), et la suivante tant qu'on n'a pas 20 départs (plancher du jeu v0). Les 10 communes prioritaires, classées sur les 5 saisons renseignées de 2020 à 2025 (2020, 2022, 2023, 2024, 2025 ; 2021 est vide dans la BDIFF), reçoivent au moins 27 % des départs de feu de la BDIFF, en couvrant au plus 10 % de la surface du département
  - valeur de départ : **27 %** (3 départs sur 11 en 2024-2025, avec les 10 communes classées sur 2020-2023), pour 8,3 % de la surface
  - pourquoi 27 % : c'est la valeur de départ. Elle repose sur 11 feux, donc le but est de tenir ce niveau sur de nouvelles saisons, pas d'afficher un progrès. Une seule saison dans le 67 (5 à 10 départs) ne se lit pas : un feu de plus ou de moins bouge le taux de 15 à 20 points
  - au départ j'avais écrit 40 % sur une valeur de 42 %. Elle était fausse : pas de règle pour les égalités, et des feux hors saison comptés (voir la relecture de #60). Je garde la valeur obtenue avec la règle écrite avant le calcul, même si elle est plus basse
  - puis 33 % (4 sur 12) : le 2e feu de Haguenau du 13/08/2025 était compté. C'est un doublon probable (même commune, date, heure et surface, règle B3), repéré par le nettoyage dans `feux.csv` (#66). Sans lui : 3 sur 11 = 27 %. La liste des 10 communes ne change pas

### Indicateur principal : part des départs dans les secteurs prioritaires

| | |
|---|---|
| Numérateur | nb de départs de feu de la saison, dans le Bas-Rhin, dont la commune est dans la liste des K communes prioritaires |
| Dénominateur | nb de départs de feu de la saison dans le Bas-Rhin |
| Unité | % |
| Paramètres | K (nombre de communes prioritaires : 10) ; la période qui sert à classer (2020-2023 pour la valeur de départ, 2020-2025 pour 2027) ; l'unité de secteur (commune, ou plus tard maille FWI ou massif) ; ce qu'on appelle un départ (tous les feux de la BDIFF, ou seulement ceux de 1 ha ou plus) |
| Saison | seulement les départs du 1er mars au 31 octobre, pour classer comme pour mesurer. 5 des 83 feux du 67 sont hors saison (février 2008, janvier et février 2022, février 2023) : ils ne comptent pas |
| Règle de classement | écrite avant le calcul : 1) nb de départs sur la période de classement, du plus grand au plus petit ; 2) à égalité, la plus grande surface brûlée ; 3) s'il reste une égalité, le code commune (ordre croissant, choix arbitraire mais fixe) |
| Point important | la liste est fixée **avant** la saison mesurée. Si on classe et on mesure sur les mêmes années, le chiffre est toujours flatteur (voir les écartés) |
| Périmètre | Bas-Rhin (514 communes au COG 2026) |
| Période | saison (1er mars au 31 octobre), comme le KPI du seuil |
| Granularité | une commune |
| Fréquence | une fois par saison. La liste est revue avant chaque saison |

Pourquoi la règle des égalités compte : sur 2020-2023, 7 communes ont au moins 2 départs, puis 29 communes en ont 1 chacune. Les 3 dernières places du top 10 se jouent entre ces 29. Sans règle, on peut trouver n'importe quelle valeur entre deux extrêmes, selon les communes qu'on prend.

### Changer un paramètre : K = 10 → K = 20

| | K = 10 | K = 20 |
|---|---|---|
| Valeur sur 2024-2025 (classement 2020-2023) | 3/11 = 27 % | 3/11 = 27 % |
| Même calcul si on classe et mesure sur toute la période (78 départs en saison) | 34/78 = 44 % | 46/78 = 59 % |
| Surface du département couverte (classement 2020-2023) | 8,3 % | 11,8 % |

- **Ce qui change :** la surface à couvrir, donc le coût (+ 42 %), et la valeur « flatteuse » sur toute la période (44 → 59 %)
- **Ce qui ne change pas :** la valeur hors échantillon. Passer à 20 communes n'attrape aucun départ de plus en 2024-2025
- **Décision :** on garde K = 10. Doubler les secteurs coûte plus cher sans rien couvrir de plus. Il faudra le revérifier quand on aura plus de saisons

### Source et faisabilité

- **Source :** BDIFF, export Grand Est 2006-2025 (`python -m src.recuperation bdiff`), nettoyé dans `data/processed/feux.csv` (`python -m src.nettoyage`, #37). Voir la [fiche BDIFF](../docs/sources/fiche-bdiff.md)
- **Champs :** `Département`, `Code INSEE`, `Année`, `Date de première alerte`, `Surface parcourue (m2)` (pour les égalités et le KPI secondaire). Pour le garde-fou : la surface des communes (geo.api.gouv.fr, COG 2026)
- **Lignes utilisables :** 84 feux sur 84 dans le Bas-Rhin (code commune, date et surface remplis à 100 %). 1 doublon probable retiré (règle B3, Haguenau le 13/08/2025), donc 83 feux, dont 78 en saison. Les codes existent tous dans le COG 2026, il n'y a rien à convertir
- **Mais** seulement 8 années renseignées sur 20 (2007, 2008, 2011, 2020, 2022 à 2025, règle P1). Les autres sont « non renseigné », jamais « 0 feu ». Et peu de feux par saison : 22 en 2020, 26 en 2022, 1 en 2023, 1 en 2024, 10 en 2025
- **La liste classée sur 2020-2023** (49 départs en saison) : Haguenau 5, Strasbourg 4, Mertzwiller 3, Plaine 2, Kutzenhausen 2, Saulxures 2, Albé 2, puis à 1 départ : Weislingen et Wissembourg (1,5 ha chacune), Haegen (1 ha, à égalité avec Lohr, départagées par le code commune ; aucune des deux n'a de feu en 2024-2025, donc ce choix ne change pas le KPI)
- **Les 11 départs de 2024-2025 :** Haguenau 3 (dans la liste), et 8 hors liste : Saverne 2, Niederbronn-les-Bains, Rothbach, Wingen-sur-Moder, Wangenbourg-Engenthal, Mutzig, Obersteinbach
- **Calcul :** `pandas`, quelques lignes. Il tournera sur la table `feux.csv` du nettoyage (#37)

### Proxy et biais

| Terme voulu | Proxy | Biais | Sens |
|---|---|---|---|
| tous les départs de feu | les feux saisis dans la BDIFF | sous-saisie : 12 années vides dans le 67, alors que les SIS comptent des centaines d'interventions feux de végétation par an. Si la saisie est meilleure dans certaines forêts (domaniales, ONF), elles ressortent en tête | **surestime** la concentration |
| un secteur (massif, zone d'intervention) | la commune | une grande commune boisée (Haguenau, 18 000 ha de forêt autour) a plus de feux juste parce qu'elle est grande | **surestime** l'intérêt des grandes communes. D'où le garde-fou en surface |
| le lieu du départ | la commune de la fiche | un feu en lisière peut être noté dans la commune voisine (Haguenau / Mertzwiller) | flou, dans les deux sens |
| une commune à risque | une commune classée avec 1 seul départ, départagée par la surface | un seul gros feu suffit à faire entrer une commune (Weislingen, Wissembourg, Haegen : 1 feu chacune) | **surestime** le risque de ces communes |

### RACER

- **Relevant :** il dit directement si des moyens fixes sur quelques communes auraient été au bon endroit
- **Accepted :** « part des départs dans les communes prioritaires » est simple à comprendre, mais la liste de communes est à valider avec le SDIS 67, qui connaît ses massifs
- **Credible :** oui, maintenant que K, la période de classement, la saison et la règle des égalités sont écrits avant le calcul. Sans la règle des égalités, deux personnes pouvaient trouver deux valeurs différentes sur les mêmes données
- **Easy :** oui, une fois `feux.csv` prêt : un comptage. La surface des communes est publique
- **Robust :** fragile avec peu de feux. Avec la liste 2020-2023 : 2024 donne 0 sur 1 (le seul feu est à Niederbronn-les-Bains, hors liste), 2025 donne 3 sur 10. Une saison seule ne se lit pas (voir le seuil plancher)

### Garde-fou : part du département couverte par les secteurs prioritaires

- **Formule :** surface des K communes prioritaires ÷ surface du Bas-Rhin (479 427 ha)
- **Valeur de départ :** 8,3 % (classement 2020-2023), 9,1 % sur toute la période
- **Pourquoi lui :** il ne mesure pas les feux, il mesure le coût. Si on monte K pour faire monter le KPI, il monte aussi. Sa limite : au plus 10 %
- **Avec lui :**
  - **volume :** le nombre de départs de la saison est toujours affiché à côté du taux
  - **seuil plancher :** en dessous de 20 départs, on ne lit pas le taux d'une saison seule, on cumule les saisons
  - **règle fixée à l'avance :** K, la période de classement, la saison, la définition d'un départ et la règle des égalités sont dans cette fiche avant de calculer

### Détournement (K4)

- **Par qui :** celui qui présente les résultats au SDIS (nous, ou plus tard le service qui suit le chiffre), sans mauvaise foi
- **Comment :** classer les communes sur les mêmes années que celles où on mesure, et monter K à 20. Ou choisir les ex aequo après avoir vu les résultats
- **Effet :** le KPI passe de 27 % à 59 %. On croit les feux très concentrés et on fige des moyens sur 20 communes, sans couvrir un seul départ de plus
- **Garde-fou :** la surface couverte (de 8,3 % à 12,4 %, au-dessus de la limite de 10 %), la règle « classement avant la saison » et la règle des égalités écrite à l'avance
- **Risque résiduel :**
  - les feux qui ne sont pas dans la BDIFF : le garde-fou ne voit pas la sous-saisie
  - un secteur prioritaire où la prévention a marché a moins de feux, puis sort du classement l'année suivante. Le chiffre baisse alors que le dispositif a fonctionné
  - un classement de communes peut stigmatiser un territoire : on parle de « secteurs prioritaires », pas de « communes à problème »

### Pre-mortem

On est fin 2027, le SDIS a mal placé ses moyens à cause de cet indicateur. Pourquoi ?

| # | Raison | Probabilité | Gravité | Garde-fou |
|---|---|---|---|---|
| 1 | Le classement reflète où on saisit les feux, pas où ils partent (sous-saisie de la BDIFF) : des secteurs actifs ne sont jamais prioritaires | forte | forte | contrôle par échantillon : comparer le classement aux interventions du SDIS 67 (#41) et aux détections FIRMS 2026 (feu de Haguenau du 12/08 bien vu). Un secteur actif dans ces sources et absent du classement est relu à la main |
| 2 | Décision prise sur trop peu de feux : une saison à 1 ou 2 départs fait passer le taux de 0 à 100 % (2023 et 2024 : 1 départ chacune) | forte | moyenne | seuil plancher (20 départs minimum, sinon on cumule) et volume affiché à côté du taux |
| 3 | Les feux changent de place (nouvelle zone touristique, sécheresse sur un autre massif) et la liste a un an de retard. En 2025, 7 des 10 départs sont hors de la liste 2020-2023 | moyenne | moyenne | revoir la liste avant chaque saison, et suivre la part des départs hors secteurs prioritaires en cours de saison |

### Rôle de chaque indicateur

| Indicateur | Rôle | Pourquoi |
|---|---|---|
| Part des départs dans les K communes prioritaires (classées avant la saison) | KPI principal | répond à la décision « moyens fixes ou mobiles » |
| Part de la surface brûlée dans les communes prioritaires | KPI secondaire | 21 feux de 1 ha ou plus dans le 67 en saison : ce sont eux qui coûtent. Valeur de départ : 28 % (2,9 ha sur 10,1 ha en 2024-2025). Il dit si les secteurs prioritaires sont aussi ceux des gros feux |
| Part du département couverte par les communes prioritaires | garde-fou | mesure le coût, pas les feux. Monte si on gonfle K |
| Nombre de départs de la saison, années non renseignées | contexte | dit si le taux est lisible, ne guide pas l'action |
| Concentration calculée sur toute la période (top 10 = 44 %, top 20 = 59 %) | écarté | classe et mesure sur les mêmes feux, donc toujours flatteur. Si elle double, personne ne fait rien de différent : métrique de vanité |
| Nombre de communes touchées par an | écarté | dépend surtout du nombre de feux saisis. Aucune décision ne change avec sa valeur |

Lien avec le KPI du seuil (branche `docs/40-seuil-et-kpi`) : lui dit **quand** renforcer, celui-ci **où**. Les deux se lisent ensemble.

Chiffres recalculés le 20/11/2026 sur `feux.csv` (736 feux dont 1 doublon probable ; 83 dans le 67, 78 en saison). Règle des égalités ajoutée après la relecture de Denis (#60), doublon de Haguenau retiré après sa relecture de #66.

## Denis : sur quoi mettre la prévention (Q2)

### Objectif (rappel)

- **Question (Q2) :** quelle part des départs de feu a une cause humaine, et laquelle ?
- **Décision du SDIS :** quelle part du budget va à la prévention, et sur quel levier
- **Objectif SMART :** d'ici le rendu du 11/12/2026, montrer sur les départs du Grand Est 2006-2025 de cause connue que la cause involontaire reste au-dessus de 50 % dans chaque sous-ensemble fixé à l'avance, avec le taux de cause renseignée à côté. Détail dans [kpi/01](01_diagnostic_objectifs.md)
  - valeur de départ : **60 %** (58 sur 97 causes connues)
  - pourquoi 50 % : au-dessus, la cause involontaire est majoritaire et la prévention vise d'abord les travaux et les particuliers. En dessous, le levier n'est pas clair

### Indicateur principal : part des départs de cause involontaire parmi les causes connues

| | |
|---|---|
| Numérateur | nb de départs de la période, dans la zone, dont la cause est « Involontaire (travaux) » ou « Involontaire (particulier) » |
| Dénominateur | nb de départs de la période, dans la zone, dont la cause est connue (`cause` différente de « inconnue ») |
| Unité | %, toujours affiché avec le nombre de causes connues et le taux de cause renseignée |
| Leviers | involontaire (travaux + particulier) ; malveillance ; accidentelle (rupture de ligne électrique, échappement de véhicule, d'après `definitions.pdf` de la BDIFF) ; naturelle (foudre) |
| Paramètres | le regroupement en leviers ; la zone (Grand Est, le 67 pour information) ; la période (2006-2025) ; le plancher (20 causes connues) ; nombre de départs ou surface brûlée |
| Point important | une cause vide reste « inconnue », jamais devinée (règle B9). Le doublon de Haguenau est retiré (B3) |
| Périmètre | Grand Est, 10 départements |
| Période | 2006-2025, année entière (comme Lawson ; Firas compte la saison mars-octobre) |
| Granularité | par département ou par année, jamais la cause par commune (`regles.md`, partie 4) |
| Fréquence | une fois par an, quand la BDIFF de l'année d'avant est publiée |
| Propriétaire | au SDIS 67, le service prévention (supposé, à confirmer, #41) |

### Changer un paramètre : la zone, la taille et la période

| Sous-ensemble | Causes connues | Involontaire | Malveillance | Accidentelle | Naturelle |
|---|---|---|---|---|---|
| Grand Est 2006-2025 | 97 | 58 (60 %) | 19 (20 %) | 18 (19 %) | 2 (2 %) |
| sans les Ardennes | 67 | 38 (57 %) | 11 (16 %) | 17 (25 %) | 1 (1 %) |
| feux de 1 ha ou plus | 36 | 21 (58 %) | 6 (17 %) | 9 (25 %) | 0 |
| feux de moins de 1 ha | 61 | 37 (61 %) | 13 (21 %) | 9 (15 %) | 2 (3 %) |
| 2019-2025 | 80 | 50 (62 %) | 15 (19 %) | 13 (16 %) | 2 (2 %) |
| 2006-2018 | 17 | 8 (47 %) | 4 (24 %) | 5 (29 %) | 0 |
| 67 seul (information) | 13 | 5 (38 %) | 3 (23 %) | 5 (38 %) | 0 |

- **Ce qui change :** presque rien sur les sous-ensembles qui passent le plancher : entre 57 % et 62 %. Seul 2006-2018 descend à 47 %, mais avec 17 causes connues, sous le plancher
- **Ce qui ne change pas :** la cause involontaire est la première partout où on a assez de causes
- **Décision :** on garde le Grand Est 2006-2025 comme valeur de départ, et les sous-ensembles servent de test. Le 67 seul ne se lit pas : 13 causes

### Source et faisabilité

- **Source :** BDIFF, export Grand Est 2006-2025, nettoyé dans `data/processed/feux.csv` (#66). Voir la [fiche BDIFF](../docs/sources/fiche-bdiff.md)
- **Champs :** `cause` (la `Nature` de la BDIFF, « inconnue » si vide), `departement`, `annee`, `surface_parcourue_ha`, `doublon_probable`
- **Lignes utilisables :** 97 départs de cause connue sur 735 (13,2 %). C'est la vraie limite de Q2
- **Calcul :** un comptage en `pandas` sur `feux.csv`. Dans Power BI, c'est la mesure `Part involontaire (causes connues)` du tableau de bord de Lawson (#83), avec le même dénominateur

### Proxy et biais

| Terme voulu | Proxy | Biais | Sens |
|---|---|---|---|
| la cause de tous les départs | la cause des 13 % de départs où elle est saisie | les gros feux sont plus souvent renseignés : 17,6 % des feux de 1 ha ou plus ont une cause, contre 11,5 % des plus petits (surface moyenne 6,5 ha contre 1,5 ha) | flou : la répartition est celle des feux enquêtés. La cause vide n'est pas un manque au hasard (`regles.md`, partie 3), donc on ne l'étend pas aux 87 % |
| tous les départements pareil | les départements qui saisissent la cause | les Ardennes font 31 % des causes connues (30 sur 97) pour 9 % des feux ; les Vosges 3 % de causes renseignées (12 sur 368) | **surestime** le poids des Ardennes (plus de malveillance : 27 %) |
| la cause réelle | la cause écrite dans la fiche | la cause est souvent une présomption au moment de la saisie | flou |
| un levier de prévention | la catégorie de la BDIFF | « accidentelle » mélange lignes électriques et échappements de véhicules, qui ne se préviennent pas pareil | flou |

### RACER

- **Relevant :** il dit sur quel levier la prévention aurait le plus de prise. C'est la décision de Q2
- **Accepted :** les catégories sont celles de la BDIFF, que le SDIS connaît. Le regroupement en leviers est à valider avec eux (#41)
- **Credible :** faible tant que 87 % des causes manquent. Il devient crédible seulement parce que la part involontaire tient dans tous les sous-ensembles qui passent le plancher
- **Easy :** oui, un comptage sur `feux.csv`
- **Robust :** bon sur le Grand Est (entre 57 % et 62 %), mauvais sur le 67 seul (13 causes) et avant 2019 (17 causes)

### Garde-fous

- **Garde-fou 1, le taux de cause renseignée :** causes connues ÷ tous les départs, dans la même zone et la même période. Valeur de départ : 13,2 % sur le Grand Est (28 % sur 2023-2025 : 34 sur 123), 15,7 % dans le 67, 3,3 % dans les Vosges. Toujours affiché à côté du KPI. S'il baisse, le KPI devient moins fiable, même s'il ne bouge pas
- **Garde-fou 2, le plancher :** en dessous de 20 causes connues, on n'affiche pas de part, on écrit « à mesurer »
- **Garde-fou 3, sans le département le mieux saisi :** la même part sans les Ardennes (57 %). Si l'écart dépasse 10 points, c'est un département qui fait le chiffre

### Détournement (K4)

- **Par qui :** nous, en présentant Q2 au SDIS, sans mauvaise foi : on a envie d'une réponse nette
- **Comment :**
  - deviner les causes vides (par exemple tous les feux d'été en « involontaire ») pour avoir plus de lignes
  - choisir après coup le département ou la période qui donne le chiffre le plus net (Ardennes : 67 %)
  - compter « accidentelle » avec l'involontaire pour gonfler la part
- **Effet :** le SDIS met tout sur la sensibilisation alors que la répartition ne vaut que pour 13 % des feux
- **Garde-fou :** la règle B9 (jamais de cause devinée), les sous-ensembles et le regroupement fixés dans cette fiche avant le calcul, le taux de cause renseignée toujours affiché
- **Risque résiduel :**
  - les feux sans cause peuvent être d'un autre type (petits feux, écobuage non déclaré) : aucun garde-fou ne le voit avec la BDIFF seule
  - la surface brûlée par levier tient à 2 feux de la Meuse en 2019 (180 ha et 136 ha, involontaires) : on ne la donne qu'en secondaire

### Pre-mortem

On est fin 2027, le SDIS a mal ciblé sa prévention à cause de cet indicateur. Pourquoi ?

| # | Raison | Probabilité | Gravité | Garde-fou |
|---|---|---|---|---|
| 1 | Les causes connues ne ressemblent pas aux inconnues : la prévention vise les travaux, alors que les petits feux sans cause venaient d'ailleurs | forte | moyenne | taux de cause renseignée affiché, comparaison par taille de feu, et les causes demandées au SDIS 67 (#41) |
| 2 | Le chiffre reflète les Ardennes, pas le Grand Est | moyenne | moyenne | garde-fou 3 (sans les Ardennes) |
| 3 | Le SDIS lit « 98 % de causes humaines » et conclut « tout à la prévention » sans choisir de levier | moyenne | faible | on affiche la répartition par levier, pas la part humaine (écartée ci-dessous) |

### Rôle de chaque indicateur

| Indicateur | Rôle | Pourquoi |
|---|---|---|
| Part des départs de cause involontaire parmi les causes connues | KPI principal | dit sur quel levier mettre la prévention |
| Répartition des causes connues par levier (malveillance, accidentelle, naturelle) | KPI secondaire | dit le 2e levier : malveillance (20 %) ou lignes électriques et routes (19 %) |
| Part de la surface brûlée par levier (causes connues) | KPI secondaire, fragile | involontaire : 568 ha sur 629 (90 %), mais 2 feux de la Meuse en 2019 en font 316 |
| Taux de cause renseignée | garde-fou | sans lui, le KPI a l'air solide alors qu'il porte sur 13 % des feux |
| Nombre de causes connues, et plancher de 20 | garde-fou | dit si le taux est lisible |
| Part des causes connues venant des Ardennes (31 %) | contexte | dit si un département fait le chiffre |
| Part d'origine humaine (tout sauf naturelle) : 95 sur 97 = 98 % | écarté | toujours près de 100 %, il ne départage aucun levier. S'il passe de 98 à 96 %, personne ne fait rien de différent |
| Part humaine calculée sur tous les départs (95 sur 735 = 13 %) | écarté | mélange « cause pas saisie » et « cause pas humaine ». C'est la mesure d'exemple du guide Power BI (`Part Origine Humaine %`), et la valeur « Humaine » n'existe pas dans la BDIFF : telle quelle, elle donnerait 0 |

Lien avec les autres fiches : Firas dit **où** renforcer, Lawson **quand**, celle-ci **contre quoi** faire de la prévention.

Chiffres recalculés le 21/11/2026 sur `feux.csv` (735 feux, sans le doublon de Haguenau, qui n'a pas de cause).

## Lawson : à partir de quand renforcer (Q3, Q4)

Explication complète pour l'équipe : [le seuil et le KPI](../docs/analyse/seuil-et-kpi.md) (#56).

### Objectif (rappel)

- **Questions :** Q4 : pour chaque seuil, combien de jours de renfort, de départs couverts, de fausses alertes ? Q3 : une règle qui ajoute à l'indice le type de jour, l'historique du secteur et la part de résineux fait-elle mieux que l'indice seul ? Hypothèse H3 : la règle combinée couvre au moins 20 % de départs en plus que l'indice seul, à jours de renfort égaux
- **Décision du SDIS :** à partir de quand lancer le dispositif renforcé (patrouilles, guet), avec un budget qui limite le nombre de jours
- **Action :** choisir les jours de renfort avec une règle calée sur les données, au lieu d'un niveau fixe de la Météo des forêts
- **Objectif :** avec le même nombre de jours de renfort, couvrir plus de départs de feu
- **Objectif SMART :** d'ici le rendu du 11 décembre 2026, montrer sur les années de test 2023-2025, dans le Grand Est, qu'une règle de déclenchement calée sur 2017-2022 couvre au moins 25 % des départs de feu, sans utiliser plus de jours de renfort que le FWI seul (25 jours sur les 3 saisons)
  - valeur de départ : **21 %** (26 départs sur 123), avec le FWI seul calé sur 2017-2022 : 25 jours de renfort sur les 3 saisons de test, soit 8 par saison
  - pourquoi 25 % : 21 % + 20 %, le gain que teste H3. Concrètement, au moins 31 départs couverts sur 123 avec 25 jours au plus
  - si H3 est réfutée, on recommande le FWI seul avec un plafond de jours, qui fait déjà mieux qu'un seuil fixe de la Météo des forêts
  - pourquoi le Grand Est et pas le 67 seul : le 67 n'a que 13 départs saisis sur 2023-2025. Le résultat se jouerait à un ou deux feux. Le 67 est donné pour information
  - pourquoi pas un objectif sur la saison 2027 : la BDIFF 2027 ne sera publiée qu'en 2028. La saison 2027 sert au suivi, pas à la preuve

Ce que disent les données (diagnostic) :
- établi : dans le 67, de 2024 à 2026, la Météo des forêts a donné 285 jours « faible », 44 « modéré », 6 « élevé », jamais « très élevé ». Un seuil à « élevé » ne déclenche presque jamais
- établi : 43 % des feux du Grand Est partent hors de juin à septembre, quand la Météo des forêts n'est pas publiée. Le FWI de Copernicus, lui, existe tous les jours
- établi : un seuil fixe ne tient pas le budget. Calé pour 20 jours sur 2006-2016, il en donne 45 par saison sur 2017-2025
- supposé : un budget de 20 jours de renfort par saison, à remplacer par le chiffre du SDIS (#41)

### Indicateur principal : taux de départs couverts

| | |
|---|---|
| Numérateur | nb de départs de feu de la période, dans la zone, survenus un jour de renfort |
| Dénominateur | nb de départs de feu de la période, dans la zone |
| Unité | %, toujours affiché avec le nombre de jours de renfort réellement utilisés |
| Jour de renfort | un jour de mars à octobre où le FWI moyen de la zone dépasse le seuil. Le seuil est fixé **avant** la période mesurée : la valeur dépassée en moyenne 20 jours par saison sur les années de calage |
| Paramètres | la règle (FWI seul, ou règle combinée de H3) ; le budget visé (20 jours par saison, supposé) ; les années de calage et de test (2017-2022 et 2023-2025, fixées dans le journal le 19/11, avant le calcul) ; la zone (Grand Est, le 67 pour information) ; ce qu'on appelle un départ (tous les feux de la BDIFF, ou ceux de 1 ha ou plus) |
| Période | l'année entière. Les départs de novembre à février comptent au dénominateur : aucun renfort ne les couvre, et c'est une vraie limite du dispositif. Sur la seule saison (mars à octobre) : 26 sur 116 = 22 % |
| Périmètre | Grand Est (10 départements), le 67 pour information |
| Granularité | un jour × une zone |
| Fréquence | une fois par saison, à la fin de la saison. Le seuil est revu avant chaque saison |
| Gain sur le hasard | à afficher à côté : part des départs couverts ÷ part des jours de renfort dans la saison. FWI seul : × 6,2 |

Pourquoi il faut toujours lire le nombre de jours : le taux monte tout seul si la règle déclenche plus de jours. Avec le même FWI, passer de 8 à 15 jours par saison fait monter le taux de 21 % à 35 % sans que la règle soit meilleure (voir ci-dessous).

### Changer un paramètre : budget de 20 → 10 ou 30 jours par saison

FWI seul, calé sur 2017-2022, testé sur 2023-2025, Grand Est :

| | 10 jours | 20 jours | 30 jours |
|---|---|---|---|
| Seuil de FWI | 26,4 | 21,2 | 18,4 |
| Jours de renfort réels par saison | 2,7 | 8,3 | 14,7 |
| Départs couverts | 7 sur 123 = 6 % | 26 sur 123 = 21 % | 43 sur 123 = 35 % |
| Gain sur le hasard | × 5,2 | × 6,2 | × 5,8 |
| Précision | 75 % (6 jours sur 8) | 64 % (16 sur 25) | 59 % (26 sur 44) |
| Feux de 1 ha ou plus couverts | 2 sur 25 | 6 sur 25 | 13 sur 25 |

- **Ce qui change :** le taux, presque proportionnel au nombre de jours. La précision baisse quand on ajoute des jours, puisqu'on prend des jours de moins en moins risqués
- **Ce qui ne change presque pas :** le gain sur le hasard, entre × 5 et × 6. C'est la vraie qualité du FWI pour choisir les jours
- **Décision :** on garde 20 jours en attendant le budget du SDIS (#41), et on compare toujours les règles à jours égaux. Le budget est un choix du SDIS, pas un réglage pour faire monter le taux

### Source et faisabilité

- **Sources :**
  - BDIFF, export Grand Est 2006-2025, nettoyé dans `data/processed/feux.csv` (#66). Voir la [fiche BDIFF](../docs/sources/fiche-bdiff.md)
  - FWI de Copernicus, 2006-2025, grille d'origine 0,25° (13 × 22 mailles), `python -m src.recuperation copernicus`. Voir la [fiche Copernicus](../docs/sources/fiche-copernicus-indices-danger.md)
  - Météo des forêts 2024-2026, seulement pour traduire le seuil en niveaux
  - pour la règle de H3 : jours fériés, calendrier scolaire, part de résineux de la BD Forêt
- **Champs :**
  - BDIFF : `Date de première alerte`, `Département`, `Code INSEE`, `Surface parcourue (m2)`
  - Copernicus : `fwinx`, `valid_time`, `latitude`, `longitude`
  - Météo des forêts : `date` (+1 jour), `num_dep`, `niveau_j1`
- **Lignes utilisables :**
  - 735 feux sur 736 (1 doublon probable retiré, règle B3, Haguenau le 13/08/2025). Date et département remplis à 100 %
  - test 2023-2025 : 123 départs dans le Grand Est (55 en 2023, 10 en 2024, 58 en 2025), dont 13 dans le 67
  - le FWI est complet : un jour par maille, toute l'année
  - les années sans aucun feu saisi sont « non renseigné » (règle P1), jamais comptées à 0
- **Calcul :** quelques lignes de `pandas` et `xarray`. Aujourd'hui, le Grand Est est la moyenne de toutes les mailles, et le 67 un rectangle de mailles. Le calcul tournera sur `feux.csv` et la table commune → maille (#62) une fois prêts

### Proxy et biais

| Terme voulu | Proxy | Biais | Sens |
|---|---|---|---|
| tous les départs de feu | les feux saisis dans la BDIFF | années vides, petits feux éteints vite qui ne sont pas saisis | flou. Si les feux non saisis tombent plutôt les jours calmes, le taux est **surestimé** |
| le niveau de danger sur lequel le SDIS décide | le FWI de Copernicus | ce n'est pas l'indice officiel, et il est calculé avec la météo observée, alors que le SDIS décide la veille sur une prévision | **surestime** ce qu'une règle réelle ferait |
| le danger dans le secteur du feu | le FWI moyen de la zone (Grand Est ou rectangle du 67) | un jour peut être dangereux dans les Vosges et calme en Champagne | **sous-estime** ce que ferait une règle par secteur |
| des jours de renfort | des jours simulés au-dessus du seuil | personne n'a vraiment renforcé ces jours-là, et un renfort réel peut éviter des départs | flou |

### RACER

- **Relevant :** il dit directement combien de départs le dispositif renforcé aurait couverts, pour un nombre de jours donné. C'est la décision du seuil
- **Accepted :** l'unité, des jours de renfort, est celle du SDIS. Le budget et le seuil actuel sont à confirmer avec eux (#41)
- **Credible :** moyen. La BDIFF a des trous et le FWI n'est pas l'indice officiel. Le test sur des années qui n'ont pas servi au calage, fixées avant le calcul, le rend plus crédible
- **Easy :** oui, une fois `feux.csv` et la table commune → maille prêts : un comptage par jour
- **Robust :** bon sur le Grand Est sur 3 saisons, pas sur une saison seule ni sur le 67 seul. Avec le seuil calé sur 2017-2022 : 2023 a 15 jours de renfort et 15 départs couverts sur 55, 2024 n'a **aucun** jour de renfort (0 sur 10), 2025 a 10 jours et 11 départs couverts sur 58

### Garde-fous

- **Garde-fou 1, les jours de renfort utilisés :** jamais plus que le FWI seul sur le même test, soit 25 jours sur 2023-2025. Un taux qui monte parce que la règle a déclenché plus de jours ne compte pas
- **Garde-fou 2, la précision :** part des jours de renfort avec au moins un départ dans la zone. Valeur de départ : 64 % (16 jours sur 25), Grand Est, test 2023-2025, FWI seul. Elle ne doit pas baisser. Elle montre aussi les fausses alertes : 9 jours sur 25 sans aucun départ
- **Avec eux :**
  - **volume :** le nombre de départs de la période, toujours affiché à côté du taux
  - **seuil plancher :** en dessous de 20 départs, on ne lit pas le taux d'une saison seule, on cumule les saisons. Le 67 seul n'atteint jamais ce plancher sur le test
  - **règle fixée à l'avance :** les années de calage et de test, la saison, la définition d'un départ et le budget sont dans le journal (19/11) avant de calculer

### Détournement (K4)

- **Par qui :** nous, en présentant H3 au SDIS, sans mauvaise foi : on a envie que la règle combinée gagne
- **Comment :**
  - laisser la règle combinée déclencher plus de jours que le FWI seul (avec 15 jours par saison au lieu de 8, le FWI seul passe déjà de 21 % à 35 %)
  - ou recaler les années de calage après avoir vu le test
  - ou ne compter que la saison mars-octobre pour gagner un point (22 % au lieu de 21 %)
- **Effet :** on annonce que H3 est validée alors que la règle choisit les jours aussi mal ou plus mal. Le SDIS paie une règle plus compliquée pour rien
- **Garde-fou :** les jours utilisés (25 au plus), la précision (64 % au moins), les années et la période écrites dans le journal avant le calcul
- **Risque résiduel :**
  - un seuil fixe ne tient pas le budget d'une saison à l'autre : sur les années de calage, il aurait donné entre 0 jour (2021) et 37 jours (2020). Le plafond de jours dans la règle reste à tester
  - la météo observée fait mieux que la prévision de la veille : on surestime ce que ferait une règle réelle
  - les départs hors saison (novembre à février) ne seront jamais couverts, quelle que soit la règle

### Pre-mortem

On est fin 2027, le SDIS a mal réglé son dispositif renforcé à cause de cet indicateur. Pourquoi ?

| # | Raison | Probabilité | Gravité | Garde-fou |
|---|---|---|---|---|
| 1 | Une saison chaude : la règle déclenche bien plus de jours que prévu, le budget explose en août, et le taux monte sans que la règle soit meilleure | forte (le seuil calé sur 2006-2016 a donné 45 jours par saison au lieu de 20 sur 2017-2025) | forte | jours utilisés affichés à côté du taux, et un plafond de jours par saison dans la règle |
| 2 | On a lu le taux sur le 67 seul, ou sur une saison seule, et une saison à 1 feu (2024) l'a rendu absurde | forte | moyenne | lecture sur le Grand Est et sur plusieurs saisons, seuil plancher de 20 départs |
| 3 | La prévision de FWI de la veille est moins bonne que l'observé : la règle couvre moins que prévu | moyenne | moyenne | refaire le test avec des prévisions si on en trouve, et comparer en fin de saison 2027 les jours déclenchés aux jours où le FWI observé dépassait le seuil |

### Rôle de chaque indicateur

| Indicateur | Rôle | Pourquoi |
|---|---|---|
| Taux de départs couverts, avec les jours de renfort utilisés | KPI principal | répond à la décision « à partir de quand renforcer », pour un budget de jours donné |
| Taux de feux de 1 ha ou plus couverts | KPI secondaire | 10 % des feux font 85 % de la surface brûlée : ce sont eux qui coûtent. Valeur de départ : 6 sur 25 (FWI seul, Grand Est, test 2023-2025) |
| Jours de renfort utilisés par saison | garde-fou | mesure le coût. Monte si la règle déclenche trop |
| Précision (jours de renfort avec au moins un départ) | garde-fou | baisse si on ajoute des jours peu risqués. Dit aussi le nombre de fausses alertes |
| Nombre de départs de la période, années non renseignées, part des départs hors juin-septembre (43 %) | contexte | dit si le taux est lisible, ne guide pas l'action |
| Les N meilleurs jours de chaque saison (32 % sur le test avec 20 jours) | écarté | il faut connaître toute la saison pour les choisir. C'est un plafond théorique, pas une règle applicable |
| Nombre de jours en niveau « modéré » ou plus de la Météo des forêts | écarté | dépend surtout de la météo de l'année. S'il double, personne ne fait rien de différent : métrique de vanité |
| Taux de départs couverts dans le 67 seul | écarté comme KPI | 13 départs sur 3 saisons : il se joue à un feu. Donné pour information |

### Ce que ça donne pour le seuil

- Dans le 67, le FWI moyen vaut environ 30 les jours « modéré » de la Météo des forêts et 45 les jours « élevé »
- Un seuil calé pour 20 jours tombe vers FWI 21, donc en dessous du niveau « modéré »
- La règle proposée au SDIS aura deux parties : un seuil de FWI, et un plafond de jours par saison (ou un seuil revu chaque année sur les dernières saisons)

Lien avec le KPI de Firas : lui dit **où** renforcer, celui-ci **quand**. Les deux se lisent ensemble.

Chiffres calculés le 20/11/2026 sur l'export BDIFF sans le doublon de Haguenau (735 feux, 123 sur le test 2023-2025) et les fichiers FWI sur la grille d'origine (#45).

## Franck : un seuil commun ou un seuil propre au 67 (Q5)

### Objectif (rappel)

- **Question (Q5) :** l'indice se comporte-t-il dans le Bas-Rhin comme dans le reste du Grand Est ? Hypothèse H5 : le bon seuil n'est pas le même d'un département à l'autre
- **Décision du SDIS :** garder le seuil régional pour lancer le dispositif renforcé, ou prendre un seuil propre au Bas-Rhin
- **Action :** caler un seuil de déclenchement sur le Bas-Rhin seul et le comparer au seuil régional
- **Objectif :** dire au SDIS 67 si un seuil propre couvre nettement plus de départs que le seuil régional, pour le même nombre de jours de renfort
- **Objectif SMART :** d'ici le rendu du 11 décembre 2026, sur les années de test 2017-2025 (FWI seul, calage 2006-2016), dans le Bas-Rhin, année entière : le seuil propre est recommandé s'il couvre au moins 20 % de départs en plus que le seuil régional, sans utiliser plus de jours de renfort. Sinon, on garde le seuil régional
  - valeur de départ : **−10 %** (35 départs couverts sur 63 avec le seuil propre, 39 avec le seuil régional, pour 40 et 44 jours de renfort par saison). Le seuil propre ne passe pas la barre : on garde le seuil régional. Voir « Valeur de départ » plus bas
  - ce qui est déjà établi : un même niveau officiel ne donne pas le même nombre de jours selon le département (60 jours « modéré » ou plus dans le 67 en 2024-2026, 50 dans les Vosges, 110 dans la Marne)

**Pourquoi pas les années de Lawson (calage 2017-2022, test 2023-2025).** Le journal du 19/11 donne deux jeux d'années : FWI seul, calage 2006-2016 et test 2017-2025 ; règle de H3, calage 2017-2022 et test 2023-2025, parce qu'elle a besoin des vacances scolaires. Mes deux seuils sont du FWI seul, donc je prends le premier. Et sur 2023-2025 le 67 n'a que 13 départs (2, 1 et 10) : sous le plancher de 20, je ne pourrais rien recommander. Pour qu'on puisse lire mon KPI à côté de celui de Lawson, je donne aussi l'écart sur ses années, pour information : 2 départs couverts sur 13 avec les deux seuils.

### Indicateur principal : écart de départs couverts entre le seuil propre et le seuil régional

| | |
|---|---|
| Formule | (départs du 67 couverts par le seuil propre − départs du 67 couverts par le seuil régional) ÷ départs du 67 couverts par le seuil régional |
| Départ couvert | un départ de feu du 67 survenu un jour de renfort de la règle. Même définition que le KPI de Lawson |
| Jour de renfort, seuil régional | un jour où le FWI moyen du Grand Est dépasse la valeur dépassée en moyenne 20 jours par saison (mars à octobre) sur 2006-2016. C'est la règle de Lawson, avec le FWI moyen pondéré par la forêt (journal du 22/11) : 14,1 au lieu de 13,5 |
| Jour de renfort, seuil propre | un jour où le FWI moyen du 67 dépasse la valeur dépassée en moyenne 20 jours par saison sur 2006-2016, calculée sur le 67 seul |
| Unité | %, toujours affiché avec les deux taux de départs couverts et les jours de renfort utilisés par chaque règle dans le 67 |
| Paramètres | le budget (20 jours par saison, supposé, à remplacer par le chiffre du SDIS, #41) ; les années de calage et de test (2006-2016 et 2017-2025, journal du 19/11) ; la zone du 67 (les mailles de ses communes, #62, avec le FWI moyen pondéré par la forêt) ; ce qu'on appelle un départ (tous les feux de la BDIFF, ou ceux de 1 ha ou plus) |
| Seuil de décision | + 20 % ou plus, sans plus de jours de renfort : seuil propre. En dessous : seuil régional. Fixé ici, avant le calcul |
| Période | l'année entière, comme le KPI de Lawson. Les départs de novembre à février comptent au dénominateur |
| Périmètre | Bas-Rhin, comparé au Grand Est |
| Granularité | un jour × une zone |
| Fréquence | une fois, avant la saison 2027. À refaire si le SDIS donne son budget (#41) ou si la zone change (#62) |

Pourquoi un écart et pas deux taux séparés : la décision ne porte pas sur le niveau du taux (c'est le KPI de Lawson) mais sur la différence entre deux règles. Un écart de 0 veut dire « le seuil régional suffit ».

### Valeur de départ (calculée le 22/11)

Test 2017-2025, départs du 67 sur les années renseignées (63), sans le doublon de Haguenau. Pour chaque règle : le seuil, les départs couverts et les jours de renfort par saison.

| Calcul | Seuil régional | Seuil propre au 67 | Écart | Sans 2020 et 2022 (13 départs) |
|---|---|---|---|---|
| FWI moyen pondéré par la forêt (celui du journal, retenu) | 14,1 : 39 sur 63, 44 jours | 13,2 : 35 sur 63, 40 jours | **−10 %** | 6 contre 5 |
| Moyenne simple des communes (contrôle) | 14,8 : 36 sur 63, 44 jours | 13,9 : 34 sur 63, 39 jours | −6 % | 5 contre 5 |
| Méthode de Lawson (toutes les mailles, rectangle du 67) | 13,5 : 37 sur 63, 45 jours | 13,4 : 37 sur 63, 41 jours | 0 % | 6 contre 5 |
| Années de Lawson (calage 2017-2022, test 2023-2025), pour info | 23,0 : 2 sur 13, 6 jours | 20,9 : 2 sur 13, 9 jours | 0 % | - |

- **Lecture :** dans aucun calcul le seuil propre ne couvre plus de départs. Il est un peu plus bas que le seuil régional, mais le FWI du 67 est aussi plus bas que celui de la région : il déclenche un peu moins de jours (40 contre 44) et couvre un peu moins de départs. Rapportées aux jours utilisés, les deux règles font pareil, environ 3,4 fois mieux que le hasard
- **Décision, avec la règle fixée avant le calcul :** on est loin des +20 %. On garde le seuil régional pour le 67
- **Garde-fous :** le seuil propre n'utilise pas plus de jours (garde-fou 1 tenu). Sans 2020 et 2022, il ne reste que 13 départs, sous le plancher, et l'écart reste négatif ou nul : ça ne change pas la décision
- **Le problème vu par Lawson reste :** calé pour 20 jours sur 2006-2016, chaque seuil en donne 40 à 45 sur 2017-2025. Ça touche les deux règles de la même façon, ce n'est donc pas un argument pour le seuil propre
- **À refaire** avec le pipeline quand le FWI moyen sera dans `jour_departement.csv` (étape 5), et si le SDIS donne son budget de jours (#41). Les chiffres d'ici viennent d'un calcul à part, avec la même méthode
- **Retrouver les seuils de Lawson** (13,5 et 13,4, 45 et 41 jours) avec sa méthode montre que mon calcul suit bien le sien

### Changer un paramètre : le niveau officiel « modéré » → « élevé »

Avant d'avoir le FWI sur toutes les années, la Météo des forêts montre déjà l'effet d'un seuil commun. Niveau officiel du lendemain, 2024-2025, jours de juin à septembre :

| | 67, seuil « modéré » | Reste du Grand Est, seuil « modéré » | 67, seuil « élevé » | Reste du Grand Est, seuil « élevé » |
|---|---|---|---|---|
| Jours au-dessus du seuil, par département | 5 | 7,1 en moyenne | 0 | 0,2 en moyenne |
| Départs couverts | 3 sur 8 | 6 sur 38 | 0 sur 8 | 1 sur 38 |

- **Ce qui change :** à « élevé », le 67 ne déclenche plus jamais, alors que d'autres départements déclenchent encore quelques jours. Un même seuil officiel ne donne ni les mêmes jours ni les mêmes départs couverts selon le département
- **Ce qui ne se lit pas :** 8 départs dans le 67, sous le plancher de 20. Ces chiffres montrent l'effet d'un seuil commun, ils ne prouvent rien sur le bon seuil
- **Décision :** on ne compare pas sur la Météo des forêts (3 étés, juin à septembre). On compare sur le FWI, 2017-2025, année entière

### Source et faisabilité

- **Sources :**
  - BDIFF, export Grand Est 2006-2025, nettoyé dans `data/processed/feux.csv` (#66). Voir la [fiche BDIFF](../docs/sources/fiche-bdiff.md)
  - FWI de Copernicus, 2006-2025, grille d'origine 0,25° (13 × 22 mailles). Voir la [fiche Copernicus](../docs/sources/fiche-copernicus-indices-danger.md)
  - Météo des forêts 2024-2026, seulement pour la première lecture ci-dessus (`data/processed/meteo_des_forets.csv`)
  - la table commune → maille (#62) pour la zone du 67
- **Champs :**
  - BDIFF : `Date de première alerte`, `Département`, `Code INSEE`
  - Copernicus : `fwinx`, `valid_time`, `latitude`, `longitude`
  - Météo des forêts : `date` (+1 jour), `num_dep`, `niveau_j1`
- **Lignes utilisables :**
  - 735 feux sur 736 (doublon de Haguenau retiré, règle B3), dont 83 dans le 67
  - test 2017-2025 dans le 67 : 63 départs (22 en 2020, 28 en 2022, 2 en 2023, 1 en 2024, 10 en 2025). 2017, 2018, 2019 et 2021 sont « non renseigné » (règle P1) et sortent du dénominateur, jamais comptées à 0
  - le calage n'utilise que le FWI, complet tous les jours : les années vides de la BDIFF ne le gênent pas
- **Ce qui manquait :** le FWI de 2006-2015 et 2023-2025, envoyé par Lawson le 22/11 (même grille 13 × 22, années complètes, et identique au mien pour 2023-2025), et la table #62 pour la zone du 67, faite dans #89
- **Calcul :** quelques lignes de `pandas` et `xarray`, le même que celui de Lawson, lancé deux fois (zone Grand Est, zone 67)

### Proxy et biais

| Terme voulu | Proxy | Biais | Sens |
|---|---|---|---|
| tous les départs du 67 | les feux saisis dans la BDIFF | 4 années vides sur les 9 du test, et 50 des 63 départs en 2020 et 2022 | flou. Le résultat dépend surtout de deux étés |
| l'indice sur lequel le SDIS décide | le FWI de Copernicus | ce n'est pas l'indice officiel, et il est calculé avec la météo observée, pas la prévision de la veille | **surestime** ce que ferait une règle réelle, pour les deux seuils de la même façon |
| le danger dans le Bas-Rhin | le FWI moyen des mailles du 67 | une maille déborde sur l'Allemagne, la Moselle ou les Vosges ; les Vosges du Nord et la plaine d'Alsace n'ont pas le même climat | **sous-estime** l'écart entre secteurs du 67 |
| le danger régional | le FWI moyen du Grand Est | la moyenne de 10 départements écrase les extrêmes | **surestime** l'avantage d'un seuil propre |

### RACER

- **Relevant :** il répond directement à la décision « seuil commun ou seuil propre », sans redire ce que mesure le KPI de Lawson
- **Accepted :** « un seuil propre au 67 couvre X % de départs en plus pour le même nombre de jours » se dit en une phrase. Le seuil actuel du SDIS est à confirmer (#41)
- **Credible :** moyen. Les années de calage et de test, le budget et le seuil de décision sont écrits avant le calcul, mais le test du 67 repose sur deux étés
- **Easy :** oui, une fois le FWI 2006-2025 et la table #62 prêts : le calcul de Lawson, lancé sur deux zones
- **Robust :** fragile. Avec 63 départs, un écart de 20 % correspond à quelques départs couverts en plus. D'où l'affichage année par année

### Garde-fous

- **Garde-fou 1, les jours de renfort utilisés dans le 67 :** le seuil propre n'en utilise jamais plus que le seuil régional sur le même test. Un écart qui vient de jours en plus ne compte pas
- **Garde-fou 2, le résultat sans 2020 et 2022 :** l'écart est recalculé sans ces deux étés. S'il change de signe, on ne recommande pas de seuil propre
- **Avec eux :**
  - **volume :** le nombre de départs couverts par chaque règle, toujours affiché à côté de l'écart
  - **seuil plancher :** 20 départs au moins sur la période de test, sinon pas de recommandation (63 sur 2017-2025 : il passe)
  - **règle fixée à l'avance :** années, budget, zone et seuil de décision sont dans cette fiche avant le calcul

### Détournement (K4)

- **Par qui :** nous, sans mauvaise foi, si on a envie de montrer que le 67 « mérite » son propre seuil et plus de moyens (c'est l'un des enjeux de la commande)
- **Comment :**
  - caler le seuil propre pour un peu plus de 20 jours (un seuil plus bas couvre forcément plus)
  - choisir la zone du 67 après avoir vu le résultat (seulement les mailles boisées)
  - ne garder que les années où le seuil propre gagne
- **Effet :** on annonce un gain qui vient du nombre de jours ou du choix de la zone. Le SDIS complique son dispositif pour rien, et demande des moyens sur un argument faux
- **Garde-fou :** les jours utilisés (pas plus que le seuil régional), la zone fixée par #62, les années du journal du 19/11, le résultat sans 2020 et 2022
- **Risque résiduel :**
  - le FWI n'est pas l'indice officiel : un seuil propre en FWI est à traduire en niveaux de la Météo des forêts, avec le même chevauchement que dans la fiche Copernicus
  - le climat change : un seuil fixe calé sur des années anciennes peut déclencher beaucoup plus de jours sur les années récentes (Lawson : calé pour 20 jours sur 2006-2016, il en donne 45 par saison sur 2017-2025)

### Pre-mortem

On est fin 2027, le SDIS a pris le mauvais seuil à cause de cet indicateur. Pourquoi ?

| # | Raison | Probabilité | Gravité | Garde-fou |
|---|---|---|---|---|
| 1 | L'écart venait de 2020 et 2022 seulement. En 2027, le seuil propre ne fait pas mieux que le régional | forte | moyenne | le résultat sans 2020 et 2022, et l'affichage année par année |
| 2 | Le seuil propre a été calé sur plus de jours que le régional, sans qu'on le voie : il « gagne » parce qu'il déclenche plus | moyenne | forte | les jours utilisés comptés pour chaque règle, jamais plus pour le seuil propre |
| 3 | Le 67 prend son seuil, les autres départements aussi : le budget régional de jours n'est plus tenu | moyenne | moyenne | le nombre total de jours du Grand Est affiché à côté, et la décision prise avec la région, pas par le 67 seul |

### Rôle de chaque indicateur

| Indicateur | Rôle | Pourquoi |
|---|---|---|
| Écart de départs couverts entre le seuil propre et le seuil régional, à jours égaux | KPI principal | répond à la décision « seuil commun ou propre » |
| Jours de renfort utilisés dans le 67 par chaque règle | garde-fou | un écart qui vient de jours en plus ne compte pas |
| Écart recalculé sans 2020 et 2022 | garde-fou | dit si deux étés font tout le résultat |
| Jours au niveau « modéré » ou plus par département, Météo des forêts 2024-2026 (67 : 60, Vosges : 50, Marne : 110) | contexte | montre qu'un même seuil ne donne pas les mêmes jours partout. Ne tranche pas |
| Feux de végétation des SIS par département (67 : 214 sur 1 824 dans le Grand Est en 2024) | contexte | dit le poids du 67 dans la région, avec une source qui n'a pas les années vides de la BDIFF |
| Feux par an pour 10 000 ha de forêt, sur les années renseignées de chaque département (67 : 0,54, 3e sur 10, après les Vosges 0,80 et les Ardennes 0,66 ; Haut-Rhin 0,31, les autres entre 0,06 et 0,22) | contexte | la Q5 parle de « surface forestière comparable » : à forêt égale, le 67 a plus de feux que la plupart des départements. Limite : la saisie BDIFF reste inégale (8 années renseignées dans le 67, 15 dans les Vosges) |
| Taux de départs couverts du 67 au niveau « modéré », Météo des forêts 2024-2025 (3 sur 8) | écarté | 8 départs : il se joue à un feu. Donné pour information |
| Classement des départements par nombre de feux BDIFF | écarté | il mesure surtout la saisie (les Vosges font la moitié des feux de la région). Personne ne changerait de seuil à cause de lui |

Lien avec les autres fiches : Lawson dit **à partir de quand** renforcer dans le Grand Est, celle-ci dit si ce **quand** vaut aussi pour le 67.

Chiffres recalculés le 22/11/2026 sur `feux.csv` (735 feux, sans le doublon de Haguenau), `meteo_des_forets.csv`, `foret_commune.csv` (BD Forêt, 10 départements), `interventions_sis.csv` tel quel depuis #87 (1 824 feux de végétation dans le Grand Est en 2024, Ardennes comprises), et le FWI 2006-2025 avec `commune_maille.csv` (#89).

## Jeu d'indicateurs v0 (groupe)

Mise en commun des 3 fiches de ce fichier : Firas (**où** renforcer, Q1), Lawson (**quand** renforcer, Q3 et Q4), Denis (**contre quoi** faire de la prévention, Q2). Version 0, reprise en FOAD pour faire la v1.

### Les décisions du SDIS et le chiffre qui y répond

| Décision du SDIS 67 (commande) | Chiffre qui la guide | Fiche |
|---|---|---|
| à partir de quand lancer le dispositif renforcé | taux de départs couverts à budget fixé | Lawson |
| où placer des moyens fixes (guet, patrouilles) | part des départs dans les 10 communes prioritaires | Firas |
| sur quel levier mettre la prévention | part des départs de cause involontaire parmi les causes connues | Denis |

### Le jeu

| Rôle | Indicateur | Valeur de départ | Période | Pourquoi ce rôle |
|---|---|---|---|---|
| **KPI principal** | Taux de départs couverts à budget fixé, avec les jours de renfort utilisés | 21 % (26 sur 123, 25 jours de renfort), Grand Est, test 2023-2025. Se lit sur le Grand Est : le 67 seul (13 départs sur le test) est donné pour information | année entière | répond à la question centrale de la commande : le seuil de déclenchement. C'est aussi lui qui teste H3 |
| KPI secondaire | Part des départs dans les 10 communes prioritaires (classées avant la saison) | 27 % (3 sur 11), 67, 2024-2025, pour 8,3 % de la surface | saison mars-octobre | prépare le principal : une fois le jour décidé, où envoyer les moyens |
| KPI secondaire | Part des départs de cause involontaire parmi les causes connues | 60 % (58 sur 97), Grand Est 2006-2025 | année entière | dit sur quel levier mettre la prévention, toute l'année |
| KPI secondaire | Feux de 1 ha ou plus couverts (jours de renfort) | 6 sur 25, Grand Est, test 2023-2025 | année entière | 10 % des feux font 85 % de la surface brûlée : ce sont eux qui coûtent |
| Garde-fou | Jours de renfort utilisés par saison | 25 jours sur 2023-2025 (8 par saison) | année entière | mesure le coût du principal. Monte si la règle déclenche trop |
| Garde-fou | Précision : jours de renfort avec au moins un départ | 64 % (16 jours sur 25) | année entière | baisse si on ajoute des jours peu risqués. Donne aussi les fausses alertes (9 jours sur 25) |
| Garde-fou | Part du 67 couverte par les communes prioritaires | 8,3 %, limite 10 % | - | mesure le coût du secondaire « où ». Monte si on gonfle la liste |
| Garde-fou | Taux de cause renseignée | 13,2 % (97 sur 735) | année entière | sans lui, la part involontaire a l'air solide alors qu'elle porte sur 13 % des feux |
| Garde-fou commun | Nombre de départs (ou de causes connues) et plancher de 20 | - | celle du KPI | en dessous de 20, aucun taux n'est lu sur une saison seule : on cumule les saisons ou on écrit « à mesurer » |
| Contexte | Années non renseignées dans la BDIFF (12 sur 20 dans le 67) | - | - | dit si un taux est lisible, ne guide pas l'action |
| Contexte | Part des départs hors juin-septembre | 43,5 %, Grand Est | année entière | rappelle que la Météo des forêts ne couvre pas près de la moitié des feux |
| Contexte | Part des causes connues venant des Ardennes | 31 % (30 sur 97) | année entière | dit si un département fait le chiffre de la part involontaire |

12 indicateurs : 1 principal, 3 secondaires, 5 garde-fous, 3 de contexte. Au-delà, le jeu ne se lit plus en une fois.

### Écartés

| Indicateur | Venu de | Pourquoi écarté |
|---|---|---|
| Les N meilleurs jours de chaque saison (32 % avec 20 jours) | Lawson | il faut connaître toute la saison pour les choisir : un plafond théorique, pas une règle applicable |
| Nombre de jours en niveau « modéré » ou plus de la Météo des forêts | Lawson | dépend surtout de la météo de l'année. S'il double, personne ne fait rien de différent |
| Taux de départs couverts dans le 67 seul | Lawson | 13 départs sur 3 saisons : il se joue à un feu. Donné pour information |
| Concentration calculée sur toute la période (top 10 = 44 %) | Firas | classe et mesure sur les mêmes feux : toujours flatteur |
| Nombre de communes touchées par an | Firas | dépend surtout du nombre de feux saisis. Aucune décision ne change |
| Part d'origine humaine parmi les causes connues (98 %) | Denis | toujours près de 100 % : ne départage aucun levier |
| Part humaine calculée sur tous les départs (13 %) | Denis | mélange « cause pas saisie » et « cause pas humaine ». C'est la mesure d'exemple du guide Power BI, et la valeur « Humaine » n'existe pas dans la BDIFF |

### Règles communes, fixées avant les calculs

- **Chaque taux dit sa période.** Le principal et la part involontaire comptent l'année entière, la part des communes prioritaires compte la saison feux du glossaire, de mars à octobre (les moyens fixes ne sont placés qu'en saison). On ne compare jamais directement deux taux de périodes différentes
- **Même table de feux pour tous** : `feux.csv` (#66), doublon de Haguenau retiré (B3), années vides « non renseigné », jamais 0 (P1)
- **Plancher de 20** départs ou causes connues pour lire un taux, partout
- **Années de calage et de test** : celles du journal du 19/11, pour toute règle calée sur les données
- **Toujours un nombre à côté d'un taux** : jours de renfort, départs, causes connues

### À trancher en groupe pour la v1

- Le KPI principal : le seuil (proposé ici, c'est la question centrale de la commande), ou un principal par décision ?
- Le budget de jours de renfort : 20 par saison est supposé, le chiffre doit venir du SDIS 67 (#41)
- La fiche de Franck : à ajouter au jeu quand elle sera dans ce fichier
- La part de résineux (journal du 20/11, proposition) : elle entre dans la règle de H3, donc dans le principal, pas comme indicateur à part
