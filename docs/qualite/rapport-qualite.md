# Rapport de qualité - BDIFF (v1)

Livrable de la séance qualité du 18/11 (#48). Source : l'export BDIFF Grand Est 2006-2025 (736 feux), c'est la base de Q1 a Q5.

- profil : [profil-bdiff.md](profil-bdiff.md)
- résultats des règles : [resultats-bdiff.md](resultats-bdiff.md)
- les règles et leurs seuils : [regles.md](regles.md)
- pour relancer : `python -m src.qualite` (le code de sortie vaut 1 si une règle bloquante échoue), tests : `python -m unittest discover -s tests -t .`

## Les règles codées

| Règle | Type de test | Sévérité | Résultat |
|---|---|---|---|
| B1 schéma (24 colonnes, entete ligne 4) | à la lecture | bloquer | ok |
| B2 Année + Numéro unique | ensemble | bloquer | réussite, 0 doublon |
| B4 Année = année de la date d'alerte | ligne | bloquer | réussite, 0 écart |
| P1 chaque département a au moins 1 feu par an | population (comparé au référentiel) | alerter | **échec : 114 départements-années sur 200 sans aucun feu** |

La barrière passe (pas d'échec bloquant), avec une alerte sur P1.

## Ce que nos indicateurs peuvent affirmer

- chaque feu est compté une seule fois (B2) et rattaché a une année cohérente avec sa date (B4) : les comptes de feux et de surfaces par jour ne sont pas gonflés par des doublons de clé
- les dates vont du 05/06/2006 au 14/11/2025, toutes lisibles : on peut relier chaque feu a un jour, donc a un niveau d'indice
- surface parcourue remplie a 100 %, donc les surfaces totales et par feu sont calculables sur les feux présents

## Ce qu'ils ne peuvent pas affirmer

- **un département-année sans feu n'est pas un "0 feu"** (P1). 2009 est vide partout. Pour le Bas-Rhin, seules 8 années sur 20 ont au moins un feu : 2007, 2008, 2011, 2020, 2022 a 2025. Ces années vides sont marquées "non renseigné" et sorties des taux
- **la calibration de H3 (2017-2022) tombe sur des années trouées** : 2 départements sur 10 ont des feux en 2017 et 2018, 4 en 2019. Seules 2020 a 2022 sont a peu pres complètes (7 a 9 départements). A rediscuter dans le groupe avant de calculer (journal des décisions)
- **un seul département pèse la moitié des feux** : les Vosges (88) font 323 des 615 feux de 2017-2025. Un taux "Grand Est" est surtout un taux des Vosges, il faut le donner aussi par département
- **la cause** (Nature) n'est remplie que pour 13,2 % des feux, et ça varie de 0 % (51) a 46 % (08), 3,3 % dans les Vosges. Le chiffre global cache donc un segment presque vide la ou il y a le plus de feux. Pour Q2 on donne la part "parmi les causes connues", par département, jamais extrapolée
- **la surface forêt vaut 0 pour 155 feux** (21 %) : feux de végétation hors forêt. Ce n'est pas une erreur, mais un indicateur sur "la surface de forêt brûlée" ne les voit pas
- deux colonnes sont vides a 100 % (type de peuplement, surface maquis) : on ne les garde pas (minimisation)

## Ce qui reste a coder

- G2 : les codes commune contre le COG 2026 (enregistrements orphelins), quand le COG sera récupéré par le script (#45)
- B3 (doublons probables : meme commune, date et surface), B5 (heure a 00:00 = inconnue), B6-B7 (surfaces)
- P1 croisé avec les interventions SIS : pour l'instant tout trou est marqué "non renseigné", meme si le département n'a peut-etre vraiment pas eu de feu
- les memes tests sur Météo des forêts et Copernicus (M1-M6, F1-F5)
- brancher la barrière sur le nettoyage (#37) pour qu'elle tourne a chaque chargement

La "source commune de la région avec le script fourni" de la consigne : on n'a pas eu de script, on a pris la BDIFF parce que c'est la source que toutes nos questions utilisent. A confirmer avec la prof.
