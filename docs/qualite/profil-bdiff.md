# Profil de la BDIFF

Généré par `python -m src.qualite` sur l'export BDIFF (10 départements, 2006-2025). Ne pas modifier à la main, relancer le script.

736 lignes, 24 colonnes. Schéma vérifié (règle B1).

Le profil dit ou chercher, pas si la donnée est bonne. Les colonnes texte n'affichent pas de valeur.

## Colonne par colonne

| colonne | type | remplies | remplissage | distinctes | min | max | zéros | valeurs de remplissage |
|---|---|---|---|---|---|---|---|---|
| Année | nombre | 736 | 100.0 | 19 | 2006 | 2025 | 0 | 0 |
| Numéro | nombre | 736 | 100.0 | 688 | 30 | 27686 | 0 | 0 |
| Département | code | 736 | 100.0 | 10 | 08 | 88 | 0 | 0 |
| Code INSEE | code | 736 | 100.0 | 431 | 08022 | 88531 | 0 | 0 |
| Nom de la commune | texte | 736 | 100.0 | 432 | - | - | 0 | 0 |
| Date de première alerte | date | 736 | 100.0 | 733 | 2006-06-05 | 2025-11-14 | 0 | 0 |
| Surface parcourue (m2) | nombre | 736 | 100.0 | 105 | 1 | 1.8e+06 | 0 | 0 |
| Surface forêt (m2) | code | 736 | 100.0 | 79 | 0 | 96700 | 155 | 0 |
| Surface maquis garrigues (m2) | vide | 0 | 0.0 | 0 | - | - | 0 | 0 |
| Autres surfaces naturelles hors forêt (m2) | code | 736 | 100.0 | 47 | 0 | 900 | 573 | 0 |
| Surfaces agricoles (m2) | code | 124 | 16.8 | 7 | 0 | 850200 | 116 | 0 |
| Autres surfaces (m2) | code | 120 | 16.3 | 1 | 0 | 0 | 120 | 0 |
| Surface autres terres boisées (m2) | code | 612 | 83.2 | 47 | 0 | 900 | 451 | 0 |
| Surfaces non boisées naturelles (m2) | code | 612 | 83.2 | 16 | 0 | 9200 | 596 | 0 |
| Surfaces non boisées artificialisées (m2) | code | 612 | 83.2 | 14 | 0 | 80000 | 596 | 0 |
| Surfaces non boisées (m2) | code | 612 | 83.2 | 27 | 0 | 9200 | 580 | 0 |
| Précision des surfaces | texte | 685 | 93.1 | 2 | - | - | 0 | 0 |
| Type de peuplement | vide | 0 | 0.0 | 0 | - | - | 0 | 0 |
| Nature | texte | 97 | 13.2 | 5 | - | - | 0 | 0 |
| Décès ou bâtiments touchés | texte | 113 | 15.4 | 2 | - | - | 0 | 0 |
| Nombre de décès | code | 5 | 0.7 | 1 | 0 | 0 | 5 | 0 |
| Nombre de bâtiments totalement détruits | code | 5 | 0.7 | 2 | 0 | 1 | 4 | 0 |
| Nombre de bâtiments partiellement détruits | code | 5 | 0.7 | 1 | 0 | 0 | 5 | 0 |
| Précision de la donnée | texte | 54 | 7.3 | 1 | - | - | 0 | 0 |

## La cause (Nature) par département

Le remplissage global cache des écarts entre départements (complétude par segment).

| Département | remplies | lignes | remplissage |
|---|---|---|---|
| 08 | 30 | 65 | 46.2 |
| 10 | 1 | 24 | 4.2 |
| 51 | 0 | 3 | 0.0 |
| 52 | 6 | 24 | 25.0 |
| 54 | 9 | 26 | 34.6 |
| 55 | 10 | 24 | 41.7 |
| 57 | 7 | 41 | 17.1 |
| 67 | 13 | 84 | 15.5 |
| 68 | 9 | 77 | 11.7 |
| 88 | 12 | 368 | 3.3 |
