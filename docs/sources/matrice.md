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
| Q1 | Massifs et type de forêt autour des départs | absent | absent | absent | absent | complet (4) | absent | absent | absent | absent | absent |
| Q2 | Cause de chaque feu | partiel (5) | absent | absent | absent | absent | absent | absent | absent | absent | demandé (6) |
| Q3 | Départs de feu par jour (ce qu'on cherche à prévoir) | partiel (1) | absent | absent | absent | absent | complet (3) | absent | absent | absent | demandé |
| Q3 | Niveau de danger chaque jour | absent | partiel (7) | complet (8) | absent | absent | absent | absent | absent | absent | absent |
| Q3 | Type de jour (week-end, férié, vacances) | absent | absent | absent | absent | absent | absent | absent | complet (9) | partiel (10) | absent |
| Q3 | Historique de départs du secteur | partiel (1) | absent | absent | absent | absent | complet (3) | absent | absent | absent | demandé |
| Q3 | Part de résineux du secteur | absent | absent | absent | absent | complet (4) | absent | absent | absent | absent | absent |
| Q4 | Jours de renfort, départs couverts, fausses alertes et feux manqués pour chaque seuil | partiel (1) | partiel (7) | complet (8) | absent | absent | absent | absent | absent | absent | absent |
| Q4 | Gravité des feux manqués (surface brûlée) | partiel (1) | absent | absent | absent | absent | absent | absent | absent | absent | demandé |
| Q4 | Coût d'un jour de renfort, budget 2027, seuil actuel | absent | absent | absent | absent | absent | absent | partiel (11) | absent | absent | demandé |
| Q5 | Feux et niveau de danger dans les 9 autres départements du Grand Est | partiel (1) | partiel (7) | complet (8) | partiel (14) | absent | complet (3) | absent | absent | absent | absent |
| Q5 | Feux et niveau de danger au niveau national | partiel (12) | partiel (7) | partiel (13) | partiel (14) | absent | complet (3) | absent | absent | absent | absent |
| Q5 | Surface forestière de chaque département, pour comparer à surface égale | absent | absent | absent | absent | partiel (15) | absent | absent | absent | absent | absent |

## Questions fusionnées

Chaque question du groupe reprend des questions des analyses individuelles (détail dans l'[analyse globale](../analyse/analyse-globale.md)) :

| Question | Reprend |
|---|---|
| Q1 | Lawson Q1, Denis Q1 et Q2, Franck Q1 |
| Q2 | Lawson Q2, Denis Q4 |
| Q3 | Lawson Q3, Denis Q6 et Q8, Franck Q4 et Q5, puis reformulée le 18/11 après le retour de la prof |
| Q4 | Lawson Q4 et Q5, Denis Q7, Franck Q2 |
| Q5 | Lawson Q6 et Q7, Denis Q5 et Q9, Franck Q6 |

L'analyse de Firas (#35) est arrivée après : ses questions seront ajoutées ici une fois fusionnée.

## Notes

1. 736 feux dans le Grand Est de 2006 à 2025, à la commune. Le Bas-Rhin n'a aucun feu en 2006, 2009, 2010, de 2012 à 2019 et en 2021, et 2009 est vide partout : cela ressemble à de la sous-saisie, pas à des années sans feu (le SIS compte des centaines de feux de végétation par an dans le 67). Pour Q3, on teste donc la règle sur tout le Grand Est et pas sur le Bas-Rhin seul.
2. Totaux par département et par an seulement : pas de commune, pas de date.
3. Colonnes `COM_AV` -> `COM_AP` du fichier des mouvements, puis `COM`, `DEP` et `REG` du fichier des communes. Les codes communes de la BDIFF suivent leur année : 20 communes du 67 ont changé de code depuis 2006. On les convertit avant toute jointure.
4. Colonnes `tfv`, `tfv_g11` (type de formation) et `essence` (essence principale), une ligne par polygone. Pas de code commune : il faut une jointure spatiale. Le Bas-Rhin vient de photos de 2007, et 924 polygones (environ 10 000 ha) ont une essence « NR » dans le fichier du département (93 dans l'extrait autour de Haguenau).
5. La cause est vide pour 86 % des feux. Q2 n'a donc qu'une réponse partielle : on la présente comme telle, sans extrapoler aux 86 %.
6. Les causes sont demandées au SDIS 67, mais seulement par année et par type, sans commune : c'est ce que permettent nos règles de données personnelles ([règles de qualité](../qualite/regles.md)). Elles ne donnent donc pas la cause de chaque feu, juste une répartition.
7. Trois saisons seulement (2024 à 2026), de juin à septembre. Les feux de mars à mai et d'octobre n'ont pas de niveau officiel. Le code département change entre 2025 (`8`) et 2026 (`08`).
8. Colonne `fwinx`, par `valid_time`, `latitude` et `longitude`. FWI tous les jours depuis 1940, toute l'année, sur une grille d'environ 25 km. Il suit la Météo des forêts dans le 67 (corrélation de rang de 0,6) mais ce n'est pas l'indice officiel. Il faut une table commune → maille avant de le joindre aux feux.
9. Le JSON donne chaque férié sous la forme `"date": "nom"` (par exemple `"2025-05-01": "1er mai"`). Zone `alsace-moselle` pour le 57, le 67 et le 68 (deux jours fériés de plus), zone `metropole` pour les 7 autres départements.
10. Pour l'académie de Strasbourg, le fichier commence en 2017-2018. Les dates sont en UTC : il faut les convertir en heure de Paris sinon tout est décalé d'un jour.
11. Budget total du SDIS 67 par an (frais de personnel 2025 : 71,9 M€), mais rien sur le coût d'un jour de renfort. Rupture de série en 2023 (passage en M57).
12. La BDIFF couvre toute la France, mais notre export ne prend que les 10 départements du Grand Est. Un export national est possible avec le même script.
13. Téléchargé sur le Grand Est seulement. La même demande sur la France est possible, mais plus lourde.
14. Série coupée : pas de détail des feux de végétation de 2010 à 2013, et 2019 manque.
15. Faisable pour les 10 départements du Grand Est (un fichier par département). Pour la France il faudrait 96 fichiers et une jointure spatiale chacun : hors de portée dans le temps du projet. Les millésimes diffèrent d'un département à l'autre.

## Ce que montre la matrice

- **La BDIFF porte presque toutes les questions, et elle est incomplète.** Q1, Q3, Q4 et Q5 en dépendent. Les années vides du Bas-Rhin sont le premier risque du projet : la demande au SDIS 67 (#41) sert d'abord à les combler.
- **Deux besoins n'ont aucune source complète** : la cause des feux (Q2, 14 % renseignés) et le coût du dispositif renforcé (Q4, uniquement chez le SDIS 67). Sans réponse du SDIS, Q4 se fera avec des ordres de grandeur.
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
