# Analyse de la commande - SDIS 67 (Bas-Rhin), saison feux 2027

Projet : feux-de-foret-grand-est | Région : Grand Est | Auteur : Lawson Robert

**Problématique :** avec un budget limité, où et à partir de quel niveau de la Météo des forêts déclencher le dispositif renforcé dans le Bas-Rhin pour réduire au mieux les départs de feu en 2027 ?

## 1. Questions

| # | Question | Décision |
|---|---|---|
| Q1 | Où se concentrent les départs de feu dans le Bas-Rhin ? | Répartition des moyens par secteur |
| Q2 | Quelle part des feux est d'origine humaine ou liée à la météo ? | Prévention ciblée ou surveillance météo |
| Q3 | Quand l'indice est élevé (ou bas), quelle part des jours compte un feu ? | Évaluer le seuil actuel (fausses alertes, feux manqués) |
| Q4 | Pour chaque seuil possible, combien de jours activés et de feux couverts ? | Choix du nouveau seuil |
| Q5 | Combien coûte un jour de dispositif renforcé et combien le budget en permet-il ? | Plafond de jours activables |
| Q6 | Le Bas-Rhin se comporte-t-il comme le reste du Grand Est ? | Seuil local ou régional |
| Q7 | Le Grand Est se comporte-t-il comme les autres régions de France (Méditerranée, Nouvelle-Aquitaine, Bretagne, etc.) : fréquence des feux, part des jours à indice élevé avec feu, fausses alertes ? | Savoir si l'indice national est fiable ici ou s'il faut un seuil propre au Grand Est |

## 2. Termes inconnus

Météo des forêts, IFM (indice forêt météo), niveaux de danger, dispositif renforcé, BDIFF, interface habitat-forêt, fausse alerte, feu manqué, DFCI.

## 3. Besoins

- Localiser et qualifier les feux (lieu, cause, surface) : Q1, Q2
- Relier chaque jour à son indice et à ses feux : Q3, Q4
- Connaître le coût du dispositif et le budget : Q5
- Refaire les calculs pour les 10 départements du Grand Est : Q6
- Refaire les mêmes calculs pour les autres régions et comparer à la France entière, avec les mêmes définitions (feu de forêt, jour avec feu, indice) : Q7

## 4. Données

| Question | Donnée idéale | Grain | Période | Emprise |
|---|---|---|---|---|
| Q1, Q2 | Feux : lieu, date, cause, végétation, surface | Un feu | 10 ans minimum | Bas-Rhin |
| Q3, Q4 | Indice quotidien (prévu la veille) croisé avec le nombre de feux | Un jour par département | 10 ans, mars à octobre | Bas-Rhin |
| Q5 | Coût d'une journée de dispositif, budget | Une valeur | Saison 2026 | SDIS 67 |
| Q6 | Mêmes données que Q3 | Un jour par département | 10 ans | Grand Est |
| Q7 | Mêmes données que Q3, agrégées par région, avec taux de base (part des jours avec feu), taux de fausses alertes et taux de feux couverts | Un jour par département, regroupé par région | 10 ans | Toutes les régions de France |

**Sources :** SDIS 67 (interventions), BDIFF, Météo-France (indice), IGN et CORINE (occupation du sol), EFFIS. Accès à confirmer.

## 5. Confrontation avec les sources

Sources de l'inventaire du groupe : BDIFF, COG (fiches de Denis), Météo des forêts, interventions des SIS, Copernicus, BD Forêt (mes fiches), comptes des SDIS par l'OFGL (fiche de Franck, #31).

Degrés : complet / partiel / absent / inconnu. Chaque raison cite la colonne du fichier ou la rubrique de la fiche.

| Question | BDIFF | COG | Météo des forêts | Interventions SIS | OFGL | Copernicus | BD Forêt |
|---|---|---|---|---|---|---|---|
| Q1 où se concentrent les départs dans le 67 | partiel : `Code INSEE` donne la commune, pas de coordonnées ; aucun feu saisi dans le 67 en 2006, 2009, 2010, 2012 à 2019 et 2021 | partiel : pas de feux, sert à convertir les anciens codes (`COM_AV` -> `COM_AP`), 20 communes du 67 concernées | absent : grain = 1 département par jour (`num_dep`), pas de feux | absent : grain = 1 département par an (`Numéro`), pas de commune | absent : comptes annuels, pas de feux | absent : que de la météo (`fwinx`), pas de feux | partiel : `tfv` et `essence` situent les massifs et leur type, mais pas de code commune (jointure spatiale) et photos de 2007 pour le 67 |
| Q2 part des feux d'origine humaine ou météo | partiel : `Nature` (la cause) est vide pour 86 % des feux du Grand Est | absent | absent : un niveau de danger, pas une cause | absent : pas de cause | absent | absent : la météo du jour ne dit pas pourquoi un feu est parti | absent |
| Q3 part des jours avec feu, par niveau d'indice | partiel : `Date de première alerte` au jour près, mais seules 2024 et 2025 se croisent avec la Météo des forêts | partiel : sert à rattacher `Code INSEE` à `DEP` | partiel : `niveau_j1` par jour et par département, mais 3 saisons (2024 à 2026) et seulement de juin à septembre | absent : totaux annuels | absent | partiel : `fwinx` tous les jours depuis 1940, toute l'année, mais ce n'est pas le niveau officiel (corrélation de rang 0,6 avec `niveau_j1`) et c'est une grille (`latitude`, `longitude`) | absent |
| Q4 jours activés et feux couverts pour chaque seuil | partiel : même limite qu'en Q3 ; dans le 67, 9 feux de juin à septembre en 2025 | partiel : jointure, comme en Q3 | partiel : on compte les jours par niveau avec `niveau_j1` (67 en 2025 : 115 faible, 5 modéré, jamais élevé) | absent | absent | partiel : on compte les jours au-dessus d'un seuil `fwinx` sur 20 ans, mais le seuil est à caler sur les niveaux officiels | absent |
| Q5 coût d'un jour de renfort et budget | absent | absent | absent | absent | partiel : budget total du SDIS 67 par an (rubrique « Grain » de la fiche), rien sur le dispositif renforcé ; rupture de série en 2023 (passage en M57) | absent | absent |
| Q6 le 67 comparé au reste du Grand Est | partiel : `Département` couvre les 10 départements, mais la saisie est inégale (les Vosges font environ la moitié des feux) | partiel : `DEP` et `REG` pour regrouper | partiel : `num_dep` couvre les 10 départements, mais 3 saisons | partiel : colonne « Feux de végétations » par `Numéro` et par an, absente de 2010 à 2013 et 2019 manque ; compte toute la végétation, pas que la forêt | absent | partiel : même grille sur tout le Grand Est, à résumer par département | partiel : surface de forêt par département pour comparer à surface égale, millésimes différents selon les départements |
| Q7 le Grand Est comparé aux autres régions | partiel : notre export ne prend que le Grand Est (rubrique « Emprise » de la fiche), un export France est possible mais pas fait | partiel : `REG` pour regrouper par région | partiel : `num_dep` couvre les 96 départements, mais 3 saisons | partiel : tous les départements, mais les colonnes `Zone` et `Région` suivent les anciennes régions jusqu'en 2015 : joindre sur `Numéro` | absent | partiel : téléchargé sur le Grand Est seulement (emprise de la demande), la France est possible mais plus lourde | partiel : un fichier par département, 96 jointures spatiales : hors de portée dans le temps du projet |

Aucune question n'a de source « complet ». Aucune case « inconnu » : tout a été vu dans un fichier ou une fiche.

### Décisions

- Q1 : approximer. La commune (`Code INSEE`) remplace le massif, et la BD Forêt sert à classer les communes par type de forêt. Les années vides comptent comme « non renseigné », jamais comme « 0 feu ». Collecter en plus : les interventions 2020-2026 du SDIS 67 (date, commune, surface), demandées dans #41
- Q2 : approximer. La part des causes se calcule sur les 14 % de feux où `Nature` est rempli, par année et par type (règle RGPD de #43), en disant que ce n'est pas représentatif de tous les feux
- Q3 : approximer. Le FWI de Copernicus remplace le niveau officiel pour 2006-2025 et pour les mois hors saison. On cale des seuils de FWI sur les niveaux de la Météo des forêts 2024-2026. Ce que ça mesure mal : le niveau officiel inclut l'avis des prévisionnistes, pas le FWI. La question a été reprise en groupe (#46) : on teste aussi le type de jour, l'historique du secteur et la part de résineux
- Q4 : approximer + collecter. Les jours et les feux couverts par seuil se calculent avec le FWI. Le seuil actuel est à demander au SDIS 67 (#41)
- Q5 : collecter. Le coût d'un jour de renfort et le budget 2027 ne sont que chez le SDIS 67 (#41). En attendant, ordre de grandeur à partir du budget OFGL, en le disant
- Q6 : approximer. FWI résumé par département sur tout le Grand Est, feux rapportés à la surface de forêt de la BD Forêt, et uniquement sur les années où chaque département a des feux saisis
- Q7 : renoncer en partie. On ne calcule pas les fausses alertes et les feux couverts région par région. La comparaison avec la France se limite aux niveaux de la Météo des forêts (3 saisons, 96 départements) et aux feux de végétation des SIS par département

### Ce qui a changé par rapport à la section 4

- je voulais 10 ans d'indice prévu la veille : la Météo des forêts n'en a que 3 étés, et seulement de juin à septembre. Copernicus rattrape l'historique, mais ce n'est pas l'indice officiel
- je voulais une liste de feux complète sur 10 ans : dans le 67, la BDIFF a plus d'années vides que d'années remplies
- je comptais sur la cause pour Q2 : elle est vide pour 86 % des feux
- le coût du dispositif (Q5) n'existe dans aucune source ouverte, comme je le craignais
- je n'ai pas exploré CORINE ni EFFIS : le site d'EFFIS avait un certificat expiré, et la BD Forêt suffit pour le type de forêt
