# Inventaire des sources

Mise en commun de l'exo 2. Questions = les 5 questions de l'[analyse globale](../analyse/analyse-globale.md). Le détail de chaque source est dans sa fiche.

| Source | Explorée par | Pertinente pour nos questions ? | Ce que nous avons découvert |
|---|---|---|---|
| [BDIFF](fiche-bdiff.md) | @wilsonDenis | oui, Q1 a Q5. C'est la seule liste de feux qu'on a | 736 feux dans le Grand Est de 2006 a 2025, a la commune. Cause vide pour 86% des feux. Années sans aucun feu (2009 partout, 2012-2019 dans le 67) qui ressemblent a de la sous-saisie. 43% des feux partent hors juin-septembre. Licence pas claire (data.gouv vs mentions légales du site) |
| [COG](fiche-cog.md) | @wilsonDenis | oui mais indirect : sert aux jointures pour toutes les questions | 20 codes communes ont changé depuis 2006 dans le 67, il faut convertir les codes de la BDIFF avec le fichier des mouvements. Faux doublons a cause des communes déléguées |
| [Météo des forêts](fiche-meteo-des-forets.md) | @lawsonboevirobert-boop (+ @FranckTambou dans #31) | oui, Q3 Q4 Q5 | Propre, mais 3 saisons seulement (2024-2026) et juin a septembre. Dans le 67 : jamais "très élevé", et "élevé" seulement 6 jours en 2026. En 2024 tout le Grand Est est au niveau faible tous les jours. Format du CSV différent en 2026, et le code département aussi (`8` en 2024-2025, `08` en 2026) : une jointure faite sans corriger ca perd les Ardennes |
| [Interventions des SIS](fiche-interventions-sis.md) | @lawsonboevirobert-boop (+ @FranckTambou dans #31) | oui pour Q5 seulement (totaux par département et par an) | Des centaines d'interventions pour feux de végétation par an dans le 67, alors que la BDIFF a 0 feu certaines années. Pas de détail par type de 2010 a 2013. 2019 pas récupéré. Bas-Rhin : +39% d'interventions d'un coup en 2013 (secours a victime), cause inconnue. Le fichier 2024 a des "?" a la place des séparateurs de milliers |
| Comptes des SDIS 2012-2025 (OFGL) | @FranckTambou (fiche dans #31) | en partie pour Q4 : budget annuel du SDIS, pas le cout d'un jour de renfort | Budget par département et par an (Licence Ouverte 2.0). Frais de personnel 2025 du SDIS 67 : 71,9 M€. Rupture de série avec le passage en M57 en 2023, et le budget du 67 s'appelle "SIS" et plus "SDIS" a partir de 2024 |
| Indices de danger Copernicus | @FranckTambou | a compléter | fiche pas encore faite (#25) |
| BD Forêt | @FranckTambou | a compléter | fiche pas encore faite (#25) |

## Quelles questions n'ont encore aucune source ?

- Q4 : le cout d'une journée de renfort, le budget 2027 et le seuil actuel. Les comptes OFGL donnent le budget global du SDIS 67 mais pas ce qui va au dispositif renforcé. Le reste est a demander au SDIS 67
- la question mise de côté sur les casernes et les délais d'intervention : il faudrait les interventions une par une du SDIS 67
- Q2 a une source mais presque vide : la cause est connue pour 14% des feux seulement

## Quelle source nous a surpris, et pourquoi ?

La BDIFF. On pensait avoir une liste de feux complète, et en fait il y a des années entières sans rien dans le Bas-Rhin. En la mettant a coté des interventions des SIS (des centaines de feux de végétation par an dans le 67), ca ressemble plus a des feux pas saisis qu'a des années sans feu. Et la Météo des forêts qui est publiée que de juin a septembre alors que plein de feux partent en mars-avril.

## Quelle source semble utile mais inexploitable dans le temps du projet ?

- les interventions des SIS pour Q5 : il faudrait les feux de végétation sur une série continue, mais la colonne n'existe pas de 2010 a 2013 et 2019 manque
- les comptes OFGL pour Q4 : on a le budget total, mais rien ne dit combien coute un jour de renfort. Sans le SDIS 67 on peut juste donner un ordre de grandeur
- Copernicus et BD Forêt : toujours pas de fiche (#25), donc on sait pas encore. Copernicus c'est notre seule piste pour avoir l'indice sur 10 ans et au printemps
