# Matrice questions × sources

Les lignes reprennent les 5 questions de l'[analyse globale](../analyse/analyse-globale.md), découpées selon les données dont chaque question a besoin. Q3 est la version reformulée après le retour de la prof (journal des décisions, 18/11). Les colonnes sont les sources de l'[inventaire](inventaire.md), plus les deux sources ajoutées pour Q3 et la demande faite au SDIS 67.

Valeurs d'une case (les degrés de la partie A, plus « demandé »). Comme le veut la consigne, chaque case « complet » renvoie à une note qui cite les colonnes du fichier :

- **complet** : la source donne ce qu'il faut, au bon grain et sur la bonne période ;
- **partiel** : elle répond en partie (période courte, trous, grain trop large), voir la note ;
- **absent** : elle ne répond pas à ce besoin ;
- **demandé** : la donnée est demandée au SDIS 67 (#41), pas encore reçue.

Colonnes :

| Code | Source | Fiche |
|---|---|---|
| BDIFF | Base de données sur les incendies de forêt | [fiche](fiche-bdiff.md) |
| MDF | Archives de la Météo des forêts | [fiche](fiche-meteo-des-forets.md) |
| FWI | Indices de danger Copernicus (FWI quotidien) | [fiche](fiche-copernicus-indices-danger.md) |
| SIS | Interventions des services d'incendie et de secours | [fiche](fiche-interventions-sis.md) |
| BDF | BD Forêt V2 | [fiche](fiche-bd-foret.md) |
| COG | Code officiel géographique | [fiche](fiche-cog.md) |
| OFGL | Comptes des SDIS | fiche dans #31 |
| FER | Jours fériés | [fiche](fiche-jours-feries.md) |
| SCO | Calendrier scolaire | [fiche](fiche-calendrier-scolaire.md) |
| SDIS | Demande au SDIS 67 | #41 |

## Matrice

| Question | Besoin | BDIFF | MDF | FWI | SIS | BDF | COG | OFGL | FER | SCO | SDIS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Commune et date de chaque départ de feu dans le 67 | partiel (1) | absent | absent | absent (2) | absent | complet (3) | absent | absent | absent | demandé |
| Q1 | Massifs et type de forêt autour des départs | absent | absent | absent | absent | partiel (4) | absent | absent | absent | absent | absent |
| Q2 | Cause de chaque feu | partiel (5) | absent | absent | absent | absent | absent | absent | absent | absent | demandé (6) |
| Q3 | Départs de feu par jour (ce qu'on cherche à prévoir) | partiel (1) | absent | absent | absent | absent | complet (3) | absent | absent | absent | demandé |
| Q3 | Niveau de danger chaque jour | absent | partiel (7) | partiel (8) | absent | absent | absent | absent | absent | absent | absent |
| Q3 | Type de jour (week-end, férié, vacances) | absent | absent | absent | absent | absent | absent | absent | complet (9) | partiel (10) | absent |
| Q3 | Historique de départs du secteur | partiel (1) | absent | absent | absent | absent | complet (3) | absent | absent | absent | demandé |
| Q3 | Part de résineux du secteur | absent | absent | absent | absent | partiel (4) | absent | absent | absent | absent | absent |
| Q4 | Jours de renfort, départs couverts, fausses alertes et feux manqués pour chaque seuil | partiel (1) | partiel (7) | partiel (8) | absent | absent | absent | absent | absent | absent | absent |
| Q4 | Gravité des feux manqués (surface brûlée) | partiel (1) | absent | absent | absent | absent | absent | absent | absent | absent | demandé |
| Q4 | Coût d'un jour de renfort, budget 2027, seuil actuel | absent | absent | absent | absent | absent | absent | partiel (11) | absent | absent | demandé |
| Q5 | Feux et niveau de danger dans les 9 autres départements du Grand Est | partiel (1) | partiel (7) | partiel (8) | partiel (14) | absent | complet (3) | absent | absent | absent | absent |
| Q5 | Feux et niveau de danger au niveau national | partiel (12) | partiel (7) | partiel (13) | partiel (14) | absent | complet (3) | absent | absent | absent | absent |
| Q5 | Surface forestière de chaque département, pour comparer à surface égale | absent | absent | absent | absent | partiel (15) | absent | absent | absent | absent | absent |

## Questions fusionnées

Chaque question du groupe reprend des questions des analyses individuelles (détail dans l'[analyse globale](../analyse/analyse-globale.md)) :

| Question | Reprend |
|---|---|
| Q1 | Lawson Q1, Denis Q1 et Q2, Franck Q1, Firas Q1 |
| Q2 | Lawson Q2, Denis Q4 |
| Q3 | Lawson Q3, Denis Q6 et Q8, Franck Q4 et Q5, Firas Q5, puis reformulée le 18/11 après le retour de la prof |
| Q4 | Lawson Q4 et Q5, Denis Q7, Franck Q2, Firas Q2, Q3 et Q4 |
| Q5 | Lawson Q6 et Q7, Denis Q5 et Q9, Franck Q6, Firas Q6 |

L'analyse de Firas (#52) est arrivée après la matrice, ses questions ont été rangées ensuite :

- sa Q5 (week-end, férié, vacances, type de forêt, feux des années d'avant) correspond aux trois variables de la nouvelle Q3 ;
- sa Q4 (compter les feux manqués en nombre ou en hectares) rejoint la ligne « gravité des feux manqués » de Q4 ;
- sa Q7, sur la saison 2026, n'entre dans aucune question du groupe. La BDIFF s'arrête à 2025, donc aucune source de l'inventaire ne couvre 2026 pour les feux. Sa fiche NASA FIRMS (#36) dira si les détections satellite peuvent combler ce trou. En attendant, la question reste de côté.

## Divergences tranchées

Les parties A de Lawson (#53) et de Denis (#29) ne donnaient pas toujours le même degré que la première version de la matrice. On est retournés aux fichiers pour trancher :

| Source et besoin | Lawson | Denis | Matrice v1 | Tranché | Pourquoi |
|---|---|---|---|---|---|
| FWI de Copernicus, niveau de danger chaque jour (Q3, Q4, Q5) | partiel | partiel | complet | **partiel** | ce n'est pas l'indice officiel, et le grain est une maille de 0,25°, pas une commune ni un département. C'est un proxy : décision D4 |
| BD Forêt, type de forêt et part de résineux (Q1, Q3) | partiel | partiel | complet | **partiel** | photos de 2007 pour le 67, 924 polygones sans essence (« NR »), pas de code commune. Décision D7 |
| COG, codes communes pour les jointures | partiel | absent | complet | **complet** pour les codes, absent pour le reste | vérifié dans les fichiers : les 431 codes de l'export BDIFF sont tous des communes 2026 (`COM` de `v_commune_2026`). Il ne répond à aucune question seul, mais sa part est complète |
| Interventions SIS, année 2019 | « 2019 manque » | « 2019 manque » | « 2019 manque » | **présente** | le fichier `interventions2019.csv` a la colonne « Feux de végétations » (751 dans le 67). La série n'est coupée que de 2010 à 2013 |

Un écart de méthode aussi : la partie A de Denis n'a pas de colonne OFGL, alors que les comptes des SDIS sont dans l'inventaire. Sans conséquence ici (l'OFGL ne sert qu'à Q4, en ordre de grandeur), mais à ajouter dans #29.

## Notes

1. 736 feux dans le Grand Est de 2006 à 2025, à la commune. Le Bas-Rhin n'a aucun feu en 2006, 2009, 2010, de 2012 à 2019 et en 2021, et 2009 est vide partout : cela ressemble à de la sous-saisie, pas à des années sans feu (le SIS compte des centaines de feux de végétation par an dans le 67). Pour Q3, on teste donc la règle sur tout le Grand Est et pas sur le Bas-Rhin seul.
2. Totaux par département et par an seulement : pas de commune, pas de date.
3. Colonnes `COM_AV` -> `COM_AP` du fichier des mouvements, puis `COM`, `DEP` et `REG` du fichier des communes. Vérifié dans les fichiers le 19/11 : les 431 codes communes de notre export BDIFF (736 feux) sont tous des communes du COG 2026, aucune conversion n'est nécessaire. Le fichier des mouvements reste utile si on ajoute d'autres sources ou un export France.
4. Colonnes `tfv`, `tfv_g11` (type de formation) et `essence` (essence principale), une ligne par polygone. Partiel : pas de code commune (il faut une jointure spatiale), et le Bas-Rhin vient de photos de 2007, et 924 polygones (environ 10 000 ha) ont une essence « NR » dans le fichier du département (93 dans l'extrait autour de Haguenau).
5. La cause est vide pour 86 % des feux. Q2 n'a donc qu'une réponse partielle : on la présente comme telle, sans extrapoler aux 86 %.
6. Les causes sont demandées au SDIS 67, mais seulement par année et par type, sans commune : c'est ce que permettent nos règles de données personnelles ([règles de qualité](../qualite/regles.md)). Elles ne donnent donc pas la cause de chaque feu, juste une répartition.
7. Trois saisons seulement (2024 à 2026), de juin à septembre. Les feux de mars à mai et d'octobre n'ont pas de niveau officiel. Le code département change entre 2025 (`8`) et 2026 (`08`).
8. Colonne `fwinx`, par `valid_time`, `latitude` et `longitude`. FWI tous les jours depuis 1940, toute l'année, sur une grille d'environ 25 km. Partiel : il suit la Météo des forêts dans le 67 (corrélation de rang de 0,6) mais ce n'est pas l'indice officiel, et son grain est une maille, pas une commune ni un département. Il faut une table commune → maille avant de le joindre aux feux.
9. Le JSON donne chaque férié sous la forme `"date": "nom"` (par exemple `"2025-05-01": "1er mai"`). Zone `alsace-moselle` pour le 57, le 67 et le 68 (deux jours fériés de plus), zone `metropole` pour les 7 autres départements.
10. Pour l'académie de Strasbourg, le fichier commence en 2017-2018. Les dates sont en UTC : il faut les convertir en heure de Paris sinon tout est décalé d'un jour.
11. Budget total du SDIS 67 par an (frais de personnel 2025 : 71,9 M€), mais rien sur le coût d'un jour de renfort. Rupture de série en 2024 dans le 67 (passage en M57, entre 2022 et 2024 selon le département).
12. La BDIFF couvre toute la France, mais notre export ne prend que les 10 départements du Grand Est. Un export national est possible avec le même script.
13. Téléchargé sur le Grand Est seulement. La même demande sur la France est possible, mais plus lourde.
14. Série coupée : pas de détail des feux de végétation de 2010 à 2013 (le fichier 2019 est bien là, avec 751 feux de végétation dans le 67).
15. Faisable pour les 10 départements du Grand Est (un fichier par département). Pour la France il faudrait 96 fichiers et une jointure spatiale chacun : hors de portée dans le temps du projet. Les millésimes diffèrent d'un département à l'autre.

## Ce que montre la matrice

- **La BDIFF porte presque toutes les questions, et elle est incomplète.** Q1, Q3, Q4 et Q5 en dépendent. Les années vides du Bas-Rhin sont le premier risque du projet : la demande au SDIS 67 (#41) sert d'abord à les combler.
- **Une fois les divergences tranchées, presque aucun besoin n'a de source complète.** Seuls les jours fériés couvrent un besoin en entier (le type de jour) ; le COG est complet pour sa part, les codes communes, pas pour les feux. Tout le reste passe par approximer ou collecter (décisions D1 à D7 du journal).
- **Deux besoins n'ont aucune source, même partielle, qui suffise** : la cause des feux (Q2, 14 % renseignés) et le coût du dispositif renforcé (Q4, uniquement chez le SDIS 67). Sans réponse du SDIS, Q4 se fera avec des ordres de grandeur.
- **Le FWI remplace la Météo des forêts pour l'historique.** La Météo des forêts n'a que 3 étés ; le FWI couvre toute l'année depuis 1940. On garde la Météo des forêts pour caler la correspondance entre FWI et niveaux officiels sur 2024-2026.
- **Q3 a une source pour chacune de ses trois variables.** La contrainte vient du calendrier scolaire (2017-2018 pour Strasbourg), qui fixe le début de la période de test.
- **Q5 au niveau national** se limite au nombre de feux et aux niveaux de danger. La comparaison à surface forestière égale reste à l'échelle du Grand Est.

### Lecture dans l'autre sens : les sources

- **COG** : ne répond à aucune question seule, mais toutes les jointures passent par lui (codes communes au millésime 2026). À garder comme référentiel.
- **Interventions des SIS** : ne sert qu'à Q5, en totaux par an. À interroger : elle sert aussi à repérer les années sous-saisies de la BDIFF (règle P1 des [règles de qualité](../qualite/regles.md)), même si elle compte toute la végétation et pas que la forêt.
- **Comptes OFGL** : ne sert qu'à Q4, et seulement en ordre de grandeur (budget total du SDIS). À garder tant que le SDIS 67 n'a pas répondu, à écarter si on reçoit le coût d'une journée de renfort.
- **Jours fériés et calendrier scolaire** : servent uniquement à Q3. Ils ont été ajoutés pour elle.

## Sources utiles pas encore explorées

| Source | Pour quoi | Question |
|---|---|---|
| Grille DFCI de 2 km | découper le Bas-Rhin en secteurs plus fins que la commune | Q1, Q4 |
| Admin Express (IGN) | contours des communes, pour la jointure spatiale avec la BD Forêt et la grille du FWI | Q1, Q3, Q5 |
