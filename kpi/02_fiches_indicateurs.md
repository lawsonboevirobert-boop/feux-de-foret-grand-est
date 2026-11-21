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
