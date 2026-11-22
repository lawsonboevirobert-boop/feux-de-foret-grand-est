# Fiches indicateurs (UE01.B, séance 2)

Une partie par membre, sur son objectif. Le jeu d'indicateurs v0 du groupe est à la fin.

## Firas : où concentrer les moyens (Q1)

### Objectif (rappel)

- **Question (Q1) :** où et quand partent les feux dans le Bas-Rhin ? Hypothèse H1 : ils se concentrent sur une minorité de communes ou de massifs
- **Décision du SDIS :** mettre des moyens fixes (guet, patrouilles prépositionnées) sur quelques secteurs, ou miser sur des moyens mobiles partout
- **Action :** désigner avant la saison des « secteurs prioritaires » où on renforce la prévention et la surveillance
- **Objectif :** que les secteurs prioritaires captent une grosse part des départs tout en restant une petite part du département
- **Objectif SMART :** saison 2027 (1er mars au 31 octobre), Bas-Rhin. Les 10 communes prioritaires, classées avant la saison sur les 5 saisons renseignées de 2020 à 2025 (2020, 2022, 2023, 2024, 2025 ; 2021 est vide dans la BDIFF), reçoivent au moins 27 % des départs de feu de la BDIFF, en couvrant au plus 10 % de la surface du département
  - valeur de départ : **27 %** (3 départs sur 11 en 2024-2025, avec les 10 communes classées sur 2020-2023), pour 8,3 % de la surface
  - pourquoi 27 % : c'est la valeur de départ. Elle repose sur 11 feux, donc le but est de tenir ce niveau sur une vraie saison, pas d'afficher un progrès
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

## Franck : un seuil commun ou un seuil propre au 67 (Q5)

### Objectif (rappel)

- **Question (Q5) :** l'indice se comporte-t-il dans le Bas-Rhin comme dans le reste du Grand Est ? Hypothèse H5 : le bon seuil n'est pas le même d'un département à l'autre
- **Décision du SDIS :** garder le seuil régional pour lancer le dispositif renforcé, ou prendre un seuil propre au Bas-Rhin
- **Action :** caler un seuil de déclenchement sur le Bas-Rhin seul et le comparer au seuil régional
- **Objectif :** dire au SDIS 67 si un seuil propre couvre nettement plus de départs que le seuil régional, pour le même nombre de jours de renfort
- **Objectif SMART :** d'ici le rendu du 11 décembre 2026, sur les années de test 2017-2025 (FWI seul, calage 2006-2016), dans le Bas-Rhin, année entière : le seuil propre est recommandé s'il couvre au moins 20 % de départs en plus que le seuil régional, sans utiliser plus de jours de renfort. Sinon, on garde le seuil régional
  - valeur de départ : **à mesurer** (FWI 2006-2025 et zone du 67, voir « Source et faisabilité »)
  - ce qui est déjà établi : un même niveau officiel ne donne pas le même nombre de jours selon le département (60 jours « modéré » ou plus dans le 67 en 2024-2026, 50 dans les Vosges, 110 dans la Marne)

**Pourquoi pas les années de Lawson (calage 2017-2022, test 2023-2025).** Le journal du 19/11 donne deux jeux d'années : FWI seul, calage 2006-2016 et test 2017-2025 ; règle de H3, calage 2017-2022 et test 2023-2025, parce qu'elle a besoin des vacances scolaires. Mes deux seuils sont du FWI seul, donc je prends le premier. Et sur 2023-2025 le 67 n'a que 13 départs (2, 1 et 10) : sous le plancher de 20, je ne pourrais rien recommander. Pour qu'on puisse lire mon KPI à côté de celui de Lawson, je donne aussi l'écart sur ses années, pour information (à mesurer avec le même FWI).

### Indicateur principal : écart de départs couverts entre le seuil propre et le seuil régional

| | |
|---|---|
| Formule | (départs du 67 couverts par le seuil propre − départs du 67 couverts par le seuil régional) ÷ départs du 67 couverts par le seuil régional |
| Départ couvert | un départ de feu du 67 survenu un jour de renfort de la règle. Même définition que le KPI de Lawson |
| Jour de renfort, seuil régional | un jour où le FWI moyen du Grand Est dépasse la valeur dépassée en moyenne 20 jours par saison (mars à octobre) sur 2006-2016. C'est le seuil de Lawson, pas un nouveau calcul |
| Jour de renfort, seuil propre | un jour où le FWI moyen du 67 dépasse la valeur dépassée en moyenne 20 jours par saison sur 2006-2016, calculée sur le 67 seul |
| Unité | %, toujours affiché avec les deux taux de départs couverts et les jours de renfort utilisés par chaque règle dans le 67 |
| Paramètres | le budget (20 jours par saison, supposé, à remplacer par le chiffre du SDIS, #41) ; les années de calage et de test (2006-2016 et 2017-2025, journal du 19/11) ; la zone du 67 (rectangle de mailles aujourd'hui, mailles des communes avec #62) ; ce qu'on appelle un départ (tous les feux de la BDIFF, ou ceux de 1 ha ou plus) |
| Seuil de décision | + 20 % ou plus, sans plus de jours de renfort : seuil propre. En dessous : seuil régional. Fixé ici, avant le calcul |
| Période | l'année entière, comme le KPI de Lawson. Les départs de novembre à février comptent au dénominateur |
| Périmètre | Bas-Rhin, comparé au Grand Est |
| Granularité | un jour × une zone |
| Fréquence | une fois, avant la saison 2027. À refaire si le SDIS donne son budget (#41) ou si la zone change (#62) |

Pourquoi un écart et pas deux taux séparés : la décision ne porte pas sur le niveau du taux (c'est le KPI de Lawson) mais sur la différence entre deux règles. Un écart de 0 veut dire « le seuil régional suffit ».

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
- **Ce qui manque :** en local, le FWI de 2016 à 2022 seulement. Il faut 2006-2015 et 2023-2025 (`python -m src.recuperation copernicus`, avec une clé), et la table #62 pour la zone du 67
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

Chiffres recalculés le 22/11/2026 sur `feux.csv` (735 feux, sans le doublon de Haguenau), `meteo_des_forets.csv` et `foret_commune.csv` (BD Forêt, 10 départements). Pour les feux de végétation des SIS, les Ardennes sont remises à la main en attendant #87, qui corrige les codes 01 à 09 dans `interventions_sis.csv`.

## Jeu d'indicateurs v0 (groupe)

À remplir ensemble à partir des fiches de chacun : KPI principal, secondaires, garde-fous, contexte, écartés.
