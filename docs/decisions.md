# Journal des décisions

Chaque décision du groupe est consignée ici, la plus récente en haut.
Tout changement de rôle doit y figurer.

Modèle d'entrée :

```
## AAAA-MM-JJ - Titre court
- Décision :
- Raison :
- Alternatives écartées :
- Décidé par :
- Liens : (issues, PR, documents)
```

---

## 2026-11-25 - Test de H3 : valeur de départ recalée et règle figée avant le test (proposition)

- **Décision :**
  - la valeur de départ du FWI seul se lit avec le FWI du pipeline, pondéré par la forêt (#91) : seuil 23,0 calé sur 2017-2022, 23 départs couverts sur 123 sur 2023-2025, 19 jours de renfort, précision 74 %. L'objectif devient au moins 28 départs sur 123 avec 19 jours au plus
  - la règle combinée de H3 est une régression de Poisson par secteur (communes d'un département dans une maille) et par jour, sur le FWI, le type de jour, l'historique du secteur et la part de résineux. Le score d'un jour est le nombre de départs attendus dans le Grand Est ; on renforce au-dessus d'un seuil calé pour 20 jours par saison
  - calage de septembre 2017 à 2022 (le calendrier scolaire commence à la rentrée 2017), seuil sur les saisons 2018-2022. La règle calée est commitée dans `docs/analyse/h3/regle-calee.json` avant tout calcul sur 2023-2025
  - le critère est celui de l'objectif : H3 validée si la règle couvre au moins 28 départs sur 123 avec 19 jours au plus
- **Raison :** remarque de Firas sur #94 : comparer la règle combinée à l'ancien calcul du FWI seul reviendrait à comparer deux méthodes. Figer la règle et le critère avant le test, et le montrer par un commit, évite de choisir après coup la version qui arrange. Le secteur est le plus petit endroit où l'on a le FWI, le calendrier et le statut de la BDIFF ; l'historique et la part de résineux varient d'un secteur à l'autre, alors qu'ils ne varient presque pas entre 10 départements.
- **Alternatives écartées :** une règle par département (l'historique et les résineux sur 10 valeurs seulement) ; une règle par commune (5 115 communes, presque toutes sans aucun feu) ; une grille de points faite à la main (des poids choisis sans données) ; ajouter tout de suite un plafond de jours (une autre question, à tester ensuite) ; garder 21 % comme valeur de départ (ancienne méthode).
- **Décidé par :** proposé par Lawson le 25/11, à valider par le groupe en relecture de la PR.
- **Liens :** [test de H3](analyse/test-h3.md), [le seuil et le KPI](analyse/seuil-et-kpi.md), #94, #98

## 2026-11-20 - Part de résineux : la forêt mixte compte pour moitié (proposition)

- **Décision :** pour la 3ᵉ variable de H3, la part de résineux d'une commune est `(conifères + 0,5 × mixte) ÷ forêt avec couvert arboré` (colonne `part_resineux` de `foret_commune.csv`). La version sans la forêt mixte (`part_resineux_stricte`) est gardée en test de sensibilité : on refait le test de H3 avec elle, et on dit si le résultat change.
- **Raison :** la forêt mixte pèse lourd dans l'est du Grand Est : 22 % de la forêt avec couvert dans le 67, 25 % dans le 68, 21 % dans le 88. L'ignorer sous-estime les résineux : dans le 67, 27,8 % sans elle, 38,7 % en la comptant à moitié. Une forêt mixte contient des conifères. 0,5 est le milieu, faute de mieux.
- **Ce qui reste à vérifier :** la définition exacte du « mixte » dans le descriptif de contenu de la BD Forêt V2 (part de conifères dans une forêt mixte). Si elle donne une fourchette, on prend son milieu à la place de 0,5. Le lien de l'IGN vers le descriptif (`DC_BDForet_2-0.pdf`) redirige aujourd'hui vers une autre page.
- **Pourquoi l'écrire maintenant :** avant de caler la règle de H3 sur 2017-2022 (entrée du 19/11), sinon on risque de choisir la version qui arrange le résultat.
- **Alternatives écartées :** ignorer la forêt mixte (sous-estime les résineux) ; la compter en entier (surestime) ; une variable « mixte » à part dans la règle de H3 (une 4ᵉ variable, contre la décision du 18/11 de s'en tenir à 3).
- **Décidé par :** proposé par Denis et Firas sur #79, à valider par le groupe.
- **Liens :** [règles de qualité](qualite/regles.md) (BD Forêt), [fiche BD Forêt](sources/fiche-bd-foret.md), #37, #79

## 2026-11-19 - Années de calage et de test, fixées avant les calculs (proposition)

- **Décision :** on juge toute règle de déclenchement sur des années qui n'ont pas servi à la caler. FWI seul : calage 2006-2016, test 2017-2025. Règle combinée de H3 (elle a besoin des vacances scolaires, connues à partir de 2017-2018) : calage 2017-2022, test 2023-2025, sur tout le Grand Est. Le Bas-Rhin seul est donné pour information. Les « N meilleurs jours de la saison » ne servent que de maximum théorique, jamais de valeur de départ.
- **Raison :** relecture de Denis sur #56. Choisir les meilleurs jours d'une saison suppose de la connaître en entier. Et le 67 n'a que 14 départs saisis sur 2023-2025 : un résultat sur le 67 seul se jouerait à un ou deux feux. Fixer les années avant de calculer évite de choisir celles qui arrangent.
- **Ce qu'on a déjà vu :** la part des feux du week-end (29,3 %, pour 28,6 % des jours) a été calculée sur toutes les années, avant cette décision. On le signale ; le test de H3 se fera quand même sur 2023-2025.
- **Alternatives écartées :** caler et tester sur les mêmes années (résultat trop optimiste) ; tester sur le 67 seul (trop peu de feux) ; un objectif mesuré sur la saison 2027 (la BDIFF 2027 sort en 2028).
- **Décidé par :** proposé par Lawson et Denis le 19/11, à valider par le groupe en relecture de #56.
- **Liens :** [le seuil et le KPI](analyse/seuil-et-kpi.md), [analyse globale](analyse/analyse-globale.md) (H3), #40, #56

## 2026-11-18 - Arrivée d'un quatrième membre et nouvelle répartition

- **Décision :** Firas (firas.ja, @firasjaouahdoups3-glitch) rejoint le groupe en renfort sur le pipeline. Il prend le nettoyage et la consolidation (#37), fait son analyse individuelle de la commande (#35) et une fiche source, NASA FIRMS (#36). Lawson reste chef de projet et responsable sources, et reprend la matrice questions × sources (#8), qui relève des sources.
- **Changement de rôle :** l'environnement Python (#5) et les scripts de récupération (#38), prévus pour Franck, ont été faits par Lawson, qui avait déjà téléchargé et ouvert chaque source pour écrire les fiches. Franck n'a donc plus d'issue de pipeline en cours. Il garde la responsabilité pipeline et modèle (il relit #44, #45 et le nettoyage) et prend une nouvelle tâche, à choisir avec lui : la table commune → maille pour joindre le FWI de Copernicus aux feux, ou le modèle en étoile (rendu du 9/12).
- **Raison :** le pipeline est la partie la plus chargée pour la suite (récupérer, nettoyer, croiser cinq sources), alors que les sources sont déjà bien avancées. Les travaux individuels de Firas rendent sa contribution visible dans l'historique, comme pour les autres.
- **Alternatives écartées :** confier les sources à Firas pour séparer les rôles de chef de projet et de responsable sources. Il aurait dû reprendre un domaine presque terminé, pendant que le pipeline restait à une seule personne.
- **Décidé par :** le groupe.
- **Liens :** [README](../README.md), #5, #8, #35, #36, #37, #38, #44, #45

## 2026-11-18 - Décisions de la matrice questions × sources (exercice 3, partie B)

Une entrée numérotée par décision, comme le demande la consigne. Elles viennent de la [matrice](sources/matrice.md) (#47).

### D1 - Q2 : la cause des feux

- **Question :** Q2, quelle part des feux a une cause humaine ?
- **Manque :** la cause est vide pour 87 % des feux de la BDIFF (639 sur 736) ; aucune autre source ouverte ne la donne.
- **Décision :** approximer et collecter. On donne la répartition des causes sur les 13 % connus, en disant qu'elle n'est pas représentative, et on demande au SDIS 67 les causes par année et par type (#41).
- **Raison :** la cause est la seule façon de répondre à Q2 ; la demander feu par feu avec la commune poserait un problème de données personnelles (règles de qualité, partie 4).
- **Ce que ça coûte :** Q2 reste une réponse partielle, sans cause feu par feu.
- **Décidé par :** Lawson et Denis, le 18/11.

### D2 - Q4 : le coût du dispositif renforcé

- **Question :** Q4, combien coûte chaque seuil au regard du budget ?
- **Manque :** le coût d'une journée de renfort, le budget 2027 et le seuil actuel ne sont publiés nulle part.
- **Décision :** collecter auprès du SDIS 67 (#41, réponse visée le 28/11). Sans réponse, approximer avec les comptes OFGL (budget total du SDIS, frais de personnel 2025 : 71,9 M€), en ordre de grandeur.
- **Raison :** seul le SDIS a ces chiffres.
- **Ce que ça coûte :** sans réponse, le tableau seuil par seuil n'aura pas de montant en euros fiable.
- **Décidé par :** Lawson et Denis, le 18/11.

### D3 - Q5 : la surface forestière au niveau national

- **Question :** Q5, l'indice se comporte-t-il pareil dans le 67, le Grand Est et en France, à surface forestière comparable ?
- **Manque :** la BD Forêt se télécharge par département ; la France demande 96 fichiers et une jointure spatiale chacun.
- **Décision :** renoncer à la comparaison à surface égale au niveau national. Elle se fait sur les 10 départements du Grand Est. Au niveau national, on compare seulement le nombre de feux et les niveaux de danger.
- **Raison :** hors de portée dans le temps du projet.
- **Ce que ça coûte :** Q5 nationale moins fine.
- **Décidé par :** Lawson et Denis, le 18/11.

### D4 - Q3 et Q4 : l'historique de l'indice

- **Question :** Q3 et Q4, juger un seuil sur plusieurs années.
- **Manque :** la Météo des forêts n'a que 3 étés (2024 à 2026), de juin à septembre.
- **Décision :** approximer avec le FWI de Copernicus, tous les jours de 2006 à 2025, comme la BDIFF (déjà décidé le 17/11, ici rappelé pour la matrice). Les années de calage et de test sont celles de l'entrée du 19/11. On cale la correspondance FWI / niveaux officiels sur 2024-2026.
- **Raison :** c'est la seule source qui couvre toutes les années de la BDIFF, et toute l'année.
- **Correction du 22/11 :** l'entrée disait « de 2016 à 2025 » et « 10 ans ». Les fichiers téléchargés (#45) vont de 2006 à 2026, et l'entrée du 19/11 cale le FWI seul sur 2006-2016 : la période est donc 2006-2025. Repéré en relisant la partie A de Franck (#80), qui citait D4.
- **Ce que ça coûte :** le FWI n'est pas l'indice officiel de Météo-France.
- **Décidé par :** le groupe, le 17/11 ; rappel le 18/11.

### D5 - Q1, Q3, Q4 : les années vides de la BDIFF dans le Bas-Rhin

- **Question :** Q1, Q3 et Q4, qui comptent les départs de feu dans le 67.
- **Manque :** aucun feu dans le 67 en 2006, 2009, 2010, de 2012 à 2019 et en 2021, alors que les interventions des SIS montrent des centaines de feux de végétation par an.
- **Décision :** approximer. Les années non renseignées sont exclues des taux (règle P1 des règles de qualité), la règle de Q3 est testée sur tout le Grand Est, et on demande au SDIS 67 ses interventions feux de végétation 2020-2026 (date, commune, surface).
- **Raison :** compter ces années comme « 0 feu » fausserait tous les taux.
- **Ce que ça coûte :** les résultats sont moins propres au Bas-Rhin.
- **Décidé par :** Lawson et Denis, le 18/11.

### D6 - Noms des fichiers de l'exercice 3

- **Question :** où ranger la matrice et le journal.
- **Manque :** la consigne demande `docs/sources/matrice.md` et `docs/journal-des-decisions.md`.
- **Décision :** la matrice est renommée `docs/sources/matrice.md`. Le journal reste `docs/decisions.md`.
- **Raison :** le journal existe sous ce nom depuis le 16/11 et il est lié partout (README, glossaire, analyses).
- **Ce que ça coûte :** rien, à signaler à la prof au rendu.
- **Décidé par :** Denis, le 18/11, à valider par Lawson en relecture.

### D7 - Q1 et Q3 : le type de forêt et la part de résineux

- **Question :** Q1 (où partent les feux, par massif) et Q3 (la part de résineux du secteur, une des trois variables de H3).
- **Manque :** la BD Forêt du 67 vient de photos de 2007, 924 polygones (environ 10 000 ha) n'ont pas d'essence (« NR »), et il n'y a pas de code commune.
- **Décision :** approximer. On garde la BD Forêt de 2007 comme état des forêts du 67 ; la part de résineux d'un secteur se calcule sur les polygones dont l'essence est connue, et on affiche à côté la part de surface « NR ». Le rattachement aux communes se fait par jointure spatiale.
- **Raison :** c'est la seule source ouverte sur les essences ; une forêt change lentement, sauf coupes et tempêtes.
- **Ce que ça coûte :** les coupes et les replantations depuis 2007 ne sont pas vues ; un secteur avec beaucoup de « NR » aura une part de résineux peu fiable. Il faudra aussi les contours des communes (Admin Express) pour la jointure.
- **Décidé par :** Lawson, le 19/11, en tranchant les divergences de la matrice (à valider par le groupe en relecture de #47).

## 2026-11-18 - Q3 et H3 : chercher mieux que l'indice, pas prouver qu'il est mauvais

- **Décision :** Q3 ne mesure plus si l'indice est fiable. Elle cherche si trois variables hors météo aident à prévoir les départs de feu en plus de l'indice : le type de jour (week-end, férié, vacances scolaires), l'historique de départs du secteur et la part de résineux. H3 devient : la règle combinée couvre au moins 20 % de départs en plus que l'indice seul, à nombre de jours de renfort égal. Les fausses alertes, les feux manqués et leur gravité passent dans Q4.
- **Raison :** retour de la prof le 18/11 : l'ancienne H3 (« plus l'indice est élevé, plus il y a de feux, mais le lien est faible ») ne prouve rien, puisque le SDIS nous a déjà dit que l'indice déclenche mal. Il faut proposer mieux que l'indice, avec des variables qui ne sont pas dans son calcul (l'indice n'utilise que la température, l'humidité, le vent et la pluie). Les trois variables retenues expliquent des départs (les causes connues sont presque toutes humaines), le SDIS peut agir dessus (quand et où renforcer) et on a les données : BDIFF, BD Forêt, jours fériés, calendrier scolaire.
- **Comment on la teste :** règle calée sur 2017-2022 et vérifiée sur 2023-2025, sur les départements du Grand Est (le Bas-Rhin seul a trop d'années non renseignées dans la BDIFF, et le calendrier scolaire commence en 2017-2018). Le seuil de 20 % est fixé ici, avant tout calcul. On a déjà vu les chiffres de la saison 2025 dans le Bas-Rhin (6 feux sur 9 un jour « faible » ; 5 sur 8 sans le doublon de Haguenau du 13/08/2025, corrigé le 20/11 d'après la table jour × département de #74), donc 2025 seule ne compte pas comme preuve.
- **Alternatives écartées :** garder l'ancienne H3 (ne prouve rien) ; ajouter le vent ou la sécheresse (déjà dans l'indice) ; l'interface habitat-forêt (demande les contours des communes et la population, plus long à construire, gardée en réserve).
- **Décidé par :** proposé par Denis après le retour de la prof, à valider par le groupe en relecture de la PR.
- **Liens :** [analyse globale](analyse/analyse-globale.md), [glossaire](glossaire.md), [fiche jours fériés](sources/fiche-jours-feries.md), [fiche calendrier scolaire](sources/fiche-calendrier-scolaire.md), #40

## 2026-11-17 - Réduire l'analyse globale à 5 questions

- **Décision :** l'analyse globale passe de 10 questions sur 3 axes à 5 questions (Q1 à Q5). Les questions sur l'éloignement des casernes et la charge par centre sont mises de côté.
- **Raison :** 10 questions, c'était trop pour le temps du projet, et plusieurs se recoupaient. Les 5 restantes couvrent les deux décisions demandées par le SDIS (où mettre les moyens, quel seuil) et la comparaison avec le Grand Est et la France. Les questions mises de côté demandent des données d'intervention détaillées que nous n'avons pas.
- **Décidé par :** le groupe.
- **Liens :** [analyse globale](analyse/analyse-globale.md)

## 2026-11-17 - Historique de l'indice : passer par l'IFM

- **Décision :** pour étudier le seuil sur une dizaine d'années, nous reconstituerons l'historique du danger à partir des valeurs de l'IFM, converties en niveaux, en plus des niveaux officiels de la Météo des forêts.
- **Raison :** la Météo des forêts n'est publiée que depuis juin 2023 et ses archives publiques ne commencent que le 3 juin 2024, soit 3 saisons seulement (2024 à 2026). C'est trop court pour juger un seuil de façon fiable. L'historique sera reconstitué avec l'indice canadien (FWI) recalculé par Copernicus.
- **Alternatives écartées :** se limiter aux 3 saisons officielles disponibles (trop peu de jours avec feu dans le Bas-Rhin pour conclure) ; attendre que Météo-France publie l'IFM historique (jeu annoncé, pas encore disponible).
- **Décidé par :** le groupe, lors de la fusion des analyses.
- **Liens :** [analyse globale, points d'attention](analyse/analyse-globale.md#points-dattention), #7

## 2026-11-17 - Une analyse globale à partir des trois analyses individuelles

- **Décision :** les trois analyses individuelles sont conservées telles quelles (partie B, travail individuel) et fusionnées dans une analyse globale qui sert de référence pour la suite du projet. Les questions sont regroupées en 3 axes : où concentrer les moyens (A), à quel niveau déclencher (B), comment le Bas-Rhin se situe (C).
- **Raison :** les trois analyses se recoupaient largement ; une seule liste de questions est nécessaire pour construire la matrice questions × sources et l'inventaire.
- **Décidé par :** le groupe.
- **Liens :** [analyse globale](analyse/analyse-globale.md), #11, #12, #13

## 2026-11-17 - Glossaire : trois statuts de définition

- **Décision :** chaque terme du glossaire porte un statut : « vérifié » (source officielle citée), « définition du groupe » (convention de calcul à faire valider par le SDIS) ou « à vérifier ».
- **Raison :** distinguer ce qui est établi de ce que nous fixons nous-mêmes, notamment fausse alerte, feu manqué et jour avec feu, qui conditionnent tous les calculs sur le seuil.
- **Décidé par :** le groupe.
- **Liens :** [glossaire](glossaire.md), #6

## 2026-11-16 - Environnement Python : version 3.13 et versions figées

- **Décision :** le projet utilise Python 3.13. numpy (2.3.5) et scikit-learn (1.7.2) sont figés dans `requirements.txt`.
- **Raison :** sur un poste Windows 11 avec le Contrôle intelligent des applications actif, les bibliothèques compilées pour Python 3.15 et les toutes dernières versions de numpy et scikit-learn sont bloquées. Les versions retenues fonctionnent.
- **Alternatives écartées :** désactiver le Contrôle intelligent des applications (irréversible sans réinstaller Windows).
- **Décidé par :** le groupe.
- **Liens :** #5

## 2026-11-16 - Organisation du travail

- **Décision :** une issue par tâche, une branche par issue (`type/numero-sujet`), une pull request relue par un autre membre avant fusion dans `main`. Les tâches de l'exercice 1 sont réparties dans les issues #1 à #13.
- **Raison :** rendre visible dans l'historique qui a fait quoi et quand, et garder `main` stable.
- **Décidé par :** le groupe.
- **Liens :** [répartition des tâches](organisation/repartition-taches.md)

## 2026-11-16 - Répartition des rôles

- **Décision :**

  | Membre | Rôle |
  |---|---|
  | Lawson Robert (@lawsonboevirobert-boop) | Chef de projet + responsable sources |
  | Denis Wilson-Bahun (@wilsonDenis) | Responsable qualité et conformité |
  | Franck Kevin Tambou (@FranckTambou) | Responsable pipeline et modèle |

- **Raison :** le groupe compte trois membres ; comme le prévoit la consigne, le chef de projet prend aussi la responsabilité des sources.
- **Décidé par :** le groupe.
- **Liens :** [README](../README.md), #2
