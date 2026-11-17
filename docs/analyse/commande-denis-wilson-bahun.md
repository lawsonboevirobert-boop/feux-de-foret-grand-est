# Analyse de la commande - Denis Wilson-Bahun

SDIS 67, saison feux 2027, réponse le 11/12.
Ils doivent décider 2 trucs : ou mettre les moyens, et a quel niveau de la Météo des forêts lancer le dispositif renforcé.
Probleme : pas le budget pour renforcer partout tout l'été, et le seuil actuel se trompe dans les 2 sens (alerte sans feu / feu avec indice bas).

## 1. Questions

Ou mettre les moyens :
- Q1 : les départs de feu sont concentrés sur qq communes / massifs ou un peu partout dans le 67 ? concentrés = on prépositionne des moyens la bas, sinon moyens mobiles
- Q2 : ils arrivent quand (mois, jour, heure) ? si c'est sur qq semaines on renforce juste a ce moment la
- Q3 : les plus gros feux c'est ceux loin d'une caserne / détectés tard ? si oui faut du guet ou des moyens dans ces zones
- Q4 : combien de feux ont une cause humaine (agriculture, imprudence...) ? si beaucoup -> mettre de l'argent dans la prévention plutot que la lutte
- Q5 : le 67 a plus ou moins de feux (par rapport a sa surface de foret) que le reste du Grand Est et la France ? ca sert a demander plus de moyens ou une mutualisation

Le seuil :
- Q6 : pour chaque niveau de l'indice, % de jours avec au moins 1 départ de feu ? si deja beaucoup de feux en "modéré" on baisse le seuil, si quasi rien en "élevé" on le monte
- Q7 : combien de jours par été a chaque niveau ? = le cout du renfort selon le seuil. si trop cher on monte le seuil ou on renforce que les zones a risque (montagne vs plaine ?)
- Q8 : les feux des jours "faible" ils sont gros ? si oui l'indice suffit pas tout seul pour déclencher
- Q9 : l'indice marche pareil dans les autres départements du Grand Est ? oui = seuil régional, non = seuil propre au 67

## 2. Termes inconnus

- SDIS : service départemental d'incendie et de secours
- Météo des forêts : indice de danger feu de foret de Météo-France, par niveaux (faible -> très élevé, combien de niveaux à vérifier)
- IFM : indice forêt météo, le calcul derriere (temp, vent, humidité, pluie ?) à vérifier
- dispositif renforcé : patrouilles, guet... ce que ca contient exactement dans le 67 je sais pas
- guet : surveillance pour repérer les départs (tours de guet)
- départ de feu / feu de foret : a partir de quelle surface ca compte ? à vérifier
- surface brulée : hectares touchés
- BDIFF : base de données des incendies de foret en France, à vérifier ce qu'il y a dedans
- CIS / chef de centre : la caserne et son chef
- saison feux : surtout l'été, dates exactes à vérifier
- COG : codes communes INSEE, changent chaque année

## 3. Besoins

- carte des zones avec le plus de départs / les plus gros feux
- les périodes a risque
- pour chaque seuil : nb de jours de renfort (cout), feux couverts, fausses alertes -> un seuil recommandé, peut etre par zone
- le 67 comparé au Grand Est et a la France
- la part des feux qu'on pourrait éviter avec de la prévention

## 4. Données idéales

| Questions | Donnée | 1 ligne = | Période | Fraicheur | Emprise |
|---|---|---|---|---|---|
| Q1 Q2 Q4 Q8 | liste des feux (date heure, commune, coordonnées, surface, cause) | 1 feu | max d'années (2006-2026 ?) | annuelle | 67, Grand Est, France |
| Q3 | casernes + heure d'alerte et d'arrivée | 1 intervention | 2020-2026 | annuelle | 67 |
| Q5 | surface de foret | 1 commune | dernier millésime | qq années | France |
| Q6 Q7 Q9 | niveau Météo des forêts | 1 jour x 1 zone | depuis que l'indice existe (à vérifier) | quotidienne | Grand Est (+ France) |
| Q7 | cout d'une journée de renfort | 1 jour | 2026 | annuelle | 67 |

- cout du renfort et heures d'intervention = données internes SDIS, surement pas en open data
- pour croiser feux et indice faut la meme date et la meme zone des 2 cotés, a voir si c'est possible

## 5. Confrontation avec les sources (exo 3)

Sources de l'inventaire du groupe : BDIFF (ma fiche), COG (ma fiche), Météo des forêts et interventions des SIS (fiches de Lawson), indices Copernicus et BD Forêt (fiches de Franck, pas encore faites -> inconnu partout).

Degrés : complet / partiel / absent / inconnu. La raison renvoie a la colonne du fichier ou a la rubrique de la fiche.

| Question | BDIFF | COG | Météo des forêts | Interventions SIS | Copernicus | BD Forêt |
|---|---|---|---|---|---|---|
| Q1 ou partent les feux | partiel : `Code INSEE` donne la commune mais pas de coordonnées ni de massif, et des années sans aucun feu dans le 67 (2012 a 2019) | absent : pas de feux, sert juste a rattacher `COM` -> `DEP` | absent : 1 ligne = 1 département, pas de feux | absent : 1 ligne = 1 département x 1 année, rien plus fin | inconnu | inconnu (pourrait donner les massifs) |
| Q2 quand | partiel : `Date de première alerte` au jour et a l'heure, mais trous dans les années (rien en 2009 dans tout le Grand Est) et 7 heures a 00:00:00 | absent | absent | absent : grain année | inconnu | absent : pas de date |
| Q3 gros feux loin d'une caserne | partiel : `Surface parcourue` oui, mais ni casernes ni heure d'arrivée | absent | absent | absent : totaux annuels, pas d'intervention une par une | absent | absent |
| Q4 cause humaine | partiel : `Nature` vide pour 86% des feux (71 sur 84 dans le 67) | absent | absent | absent : pas de cause | absent | absent |
| Q5 67 vs Grand Est vs France, par surface de foret | partiel : notre export c'est que le Grand Est, et les Vosges font la moitié des feux (saisie inégale entre départements) | absent : sert a la jointure `DEP` / `REG` | absent | partiel : colonne feux de végétations par département et par an, mais végétation c'est pas que la foret, et pas de détail 2010-2013 | inconnu | inconnu (surface de foret) |
| Q6 % de jours avec feu par niveau | partiel : seuls 2024-2025 se croisent avec l'indice, et dans le 67 ca fait 9 feux de juin a septembre (tous en 2025) | absent | partiel : `niveau_j1` par jour et par département, mais 3 saisons seulement, juin a septembre | absent | inconnu | absent |
| Q7 jours par été a chaque niveau = cout | absent | absent | partiel : on peut compter les jours par niveau avec `niveau_j1` (67 en 2025 : 115 faible, 5 modéré) mais aucun cout | absent : pas de cout | inconnu | absent |
| Q8 les feux des jours "faible" sont gros ? | partiel : `Surface parcourue` ok mais meme probleme de recouvrement qu'en Q6 | absent | partiel : `niveau_j1`, période courte | absent | inconnu | absent |
| Q9 l'indice pareil dans le Grand Est ? | partiel : feux des 10 départements mais saisie inégale | absent | partiel : `num_dep` couvre les 96 départements, mais 3 saisons | absent | inconnu | absent |

Aucune question a une source "complet".

### Décisions

- Q1 : approximer. On garde la commune (`Code INSEE`) a la place du massif, et on regroupe les communes avec la BD Forêt une fois la fiche faite. Ca mesure mal les années ou rien n'a été saisi
- Q2 : approximer. On calcule sur les années remplies seulement et on le dit, les années vides comptent pas comme "0 feu"
- Q3 : collecter. Demander au SDIS 67 les interventions une par une (heure d'alerte, heure d'arrivée, caserne). Sans ca on renonce, comme dans l'analyse globale
- Q4 : collecter + approximer. Demander les causes au SDIS 67. En attendant on regarde les 14% de feux ou la cause est connue, en disant que c'est pas représentatif
- Q5 : vérifier d'abord la BD Forêt (inconnu). Refaire l'export BDIFF en "France entière". Les interventions SIS servent de proxy pour comparer les départements, mais ca compte toute la végétation, pas que la foret
- Q6 et Q8 : vérifier d'abord la fiche Copernicus (inconnu). Si ca marche on approxime avec le FWI sur 10 ans, en disant qu'il mesure mal la sécheresse de la végétation et l'avis des prévisionnistes qui sont dans le niveau officiel. Sinon on renonce au 67 seul et on fait le calcul a l'échelle du Grand Est (47 feux en juin-septembre 2024-2025 au lieu de 9)
- Q7 : collecter. Les jours par niveau on les a, le cout d'une journée de renfort et le seuil actuel faut les demander au SDIS 67
- Q9 : approximer, comme Q6 (Copernicus si ca marche), et en attendant comparer les 3 saisons officielles en disant que c'est trop court pour conclure

Ce qui a changé par rapport a ce que j'imaginais en section 4 : je pensais avoir l'indice "depuis qu'il existe" et une liste de feux propre. En vrai l'indice c'est 3 étés seulement, et la liste des feux a des trous, donc presque tout passe par approximer ou collecter.
