# Résultats des règles de qualité, BDIFF

Généré par `python -m src.qualite` sur l'export BDIFF (10 départements, 2006-2025). Ne pas modifier à la main, relancer le script.

Règles : voir [regles.md](regles.md). Lecture : [rapport-qualite.md](rapport-qualite.md).

| règle | dimension | portée | seuil | contrôlés | fautifs | résultat | sévérité | décision | détail |
|---|---|---|---|---|---|---|---|---|---|
| B2 | unicité | toutes les lignes, clé Année + Numéro | 0% | 736 | 0 | réussite | bloquer | on arrete le chargement et on regarde l'export (un feu compté 2 fois fausse les surfaces) | 0 lignes en double sur la clé |
| B4 | cohérence | toutes les lignes, colonnes Année et Date de première alerte | 0% | 736 | 0 | réussite | bloquer | on arrete le chargement : sans date sure, le feu ne peut pas etre relié au niveau du jour | 0 dates illisibles, 0 années différentes |
| P1 | complétude (population) | 10 départements x 20 années demandées dans l'export | 0% | 200 | 114 | échec | alerter | on charge, mais ces départements-années sont marqués non renseignés et exclus des taux | 08 : 2006-2019 ; 10 : 2006, 2008-2014, 2016-2018 ; 51 : 2006-2007, 2009-2023 ; 52 : 2006-2018, 2021, 2024 ; 54 : 2006-2009, 2011, 2013, 2016-2019, 2024 ; 55 : 2006-2011, 2013-2018, 2023-2024 ; 57 : 2006-2009, 2011, 2014, 2016-2019, 2024 ; 67 : 2006, 2009-2010, 2012-2019, 2021 ; 68 : 2008-2009, 2019, 2024 ; 88 : 2006-2009, 2011 |
