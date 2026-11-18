# Matrice questions × sources

Les lignes reprennent les 5 questions de l'[analyse globale](../analyse/analyse-globale.md), découpées selon les données dont chaque question a besoin. Q3 est la version reformulée après le retour de la prof (journal des décisions, 18/11). Les colonnes sont les sources de l'[inventaire](inventaire.md), plus les deux sources ajoutées pour Q3 et la demande faite au SDIS 67.

Valeurs d'une case :

- **oui** : la source donne ce qu'il faut, au bon grain et sur la bonne période ;
- **partiel** : elle répond en partie (période courte, trous, grain trop large), voir la note ;
- **non** : elle ne répond pas à ce besoin ;
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
| Q1 | Commune et date de chaque départ de feu dans le 67 | partiel (1) | non | non | non (2) | non | oui (3) | non | non | non | demandé |
| Q1 | Massifs et type de forêt autour des départs | non | non | non | non | oui (4) | non | non | non | non | non |
| Q2 | Cause de chaque feu | partiel (5) | non | non | non | non | non | non | non | non | non (6) |
| Q3 | Départs de feu par jour (ce qu'on cherche à prévoir) | partiel (1) | non | non | non | non | oui (3) | non | non | non | demandé |
| Q3 | Niveau de danger chaque jour | non | partiel (7) | oui (8) | non | non | non | non | non | non | non |
| Q3 | Type de jour (week-end, férié, vacances) | non | non | non | non | non | non | non | oui (9) | partiel (10) | non |
| Q3 | Historique de départs du secteur | partiel (1) | non | non | non | non | oui (3) | non | non | non | demandé |
| Q3 | Part de résineux du secteur | non | non | non | non | oui (4) | non | non | non | non | non |
| Q4 | Jours de renfort, départs couverts, fausses alertes et feux manqués pour chaque seuil | partiel (1) | partiel (7) | oui (8) | non | non | non | non | non | non | non |
| Q4 | Gravité des feux manqués (surface brûlée) | oui | non | non | non | non | non | non | non | non | demandé |
| Q4 | Coût d'un jour de renfort, budget 2027, seuil actuel | non | non | non | non | non | non | partiel (11) | non | non | demandé |
| Q5 | Feux et niveau de danger dans les 9 autres départements du Grand Est | partiel (1) | partiel (7) | oui (8) | non | non | oui (3) | non | non | non | non |
| Q5 | Feux et niveau de danger au niveau national | partiel (12) | oui | partiel (13) | partiel (14) | non | oui | non | non | non | non |
| Q5 | Surface forestière de chaque département, pour comparer à surface égale | non | non | non | non | partiel (15) | non | non | non | non | non |

## Notes

1. 736 feux dans le Grand Est de 2006 à 2025, à la commune. Le Bas-Rhin n'a aucun feu de 2012 à 2019, et 2009 est vide partout : cela ressemble à de la sous-saisie, pas à des années sans feu (le SIS compte des centaines de feux de végétation par an dans le 67). Pour Q3, on teste donc la règle sur tout le Grand Est et pas sur le Bas-Rhin seul.
2. Totaux par département et par an seulement : pas de commune, pas de date.
3. Les codes communes de la BDIFF suivent leur année : 20 communes du 67 ont changé de code depuis 2006. On les convertit avec le fichier des mouvements du COG avant toute jointure.
4. Type de formation et essence principale pour chaque polygone. Pas de code commune : il faut une jointure spatiale. Le Bas-Rhin vient de photos de 2007, et 93 polygones ont une essence « NR ».
5. La cause est vide pour 86 % des feux. Q2 n'a donc qu'une réponse partielle : on la présente comme telle, sans extrapoler aux 86 %.
6. Les règles de données personnelles limitent la demande au SDIS à la date, la commune et la surface : les causes n'y sont pas, on ne les utilise que par année et par type ([règles de qualité](../qualite/regles.md)).
7. Trois saisons seulement (2024 à 2026), de juin à septembre. Les feux de mars à mai et d'octobre n'ont pas de niveau officiel. Le code département change entre 2025 (`8`) et 2026 (`08`).
8. FWI tous les jours depuis 1940, toute l'année, sur une grille d'environ 25 km. Il suit la Météo des forêts dans le 67 (corrélation de rang de 0,6) mais ce n'est pas l'indice officiel. Il faut une table commune → maille avant de le joindre aux feux.
9. Zone `alsace-moselle` pour le 57, le 67 et le 68 (deux jours fériés de plus), zone `metropole` pour les 7 autres départements.
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

## Sources utiles pas encore explorées

| Source | Pour quoi | Question |
|---|---|---|
| Grille DFCI de 2 km | découper le Bas-Rhin en secteurs plus fins que la commune | Q1, Q4 |
| Admin Express (IGN) | contours des communes, pour la jointure spatiale avec la BD Forêt et la grille du FWI | Q1, Q3, Q5 |
