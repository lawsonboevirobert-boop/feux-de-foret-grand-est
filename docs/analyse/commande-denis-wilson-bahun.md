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
