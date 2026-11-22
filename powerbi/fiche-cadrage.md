# Fiche de cadrage du tableau de bord (UE01.C)

Binôme : Lawson Robert et ..................  Date : 20/11/2026

| | |
|---|---|
| **Le décideur** | la direction du SDIS 67 (pompiers du Bas-Rhin) |
| **La décision** | avant la saison 2027 (mars) : où concentrer les moyens contre les départs de feu, et à partir de quel niveau de la Météo des forêts lancer le dispositif renforcé (patrouilles, guet), avec un budget qui limite le nombre de jours |
| **Question 1 · Où en est-on ?** | combien de feux, quelle surface, où et quelles années, dans le Bas-Rhin comparé au reste du Grand Est |
| **Question 2 · Pourquoi ?** | quand partent les feux (mois, saison, niveau de danger du jour), et pour quelles causes, quand elles sont connues |
| **Question 3 · Que fait-on ?** | quel niveau de déclenchement couvre le plus de feux pour le moins de jours sans feu ; quelles communes du 67 surveiller en priorité |

## Les indicateurs (KPI)

| KPI | Formule DAX (mesure) | Question | Visuel |
|---|---|---|---|
| Nombre de feux, comparé à N-1 | `Nb feux = COUNTROWS(Incendies)` ; `Évolution vs N-1 = DIVIDE([Nb feux] - [Nb feux N-1], [Nb feux N-1])` | 1 | carte KPI + histogramme par année |
| Surface brûlée (ha) | `Surface brûlée (ha) = SUM(Incendies[Surface (ha)])` | 1 | carte KPI + barres par département |
| Part des feux hors juin-septembre | `DIVIDE(CALCULATE([Nb feux], Calendrier[Période Météo des forêts] = "Hors publication"), [Nb feux])` | 2 | carte KPI + histogramme par mois |
| Taux couverts (Météo des forêts), avec les jours de renfort | `DIVIDE([Feux couverts], [Feux pendant la publication])` ; `Jours de renfort` | 3 | cartes KPI pilotées par le segment du seuil + tableau par département |
| Précision (garde-fou) | `DIVIDE([Jours de renfort avec feu], [Jours de renfort])` | 3 | carte KPI |
| Part des feux dans les secteurs prioritaires du 67 | `DIVIDE(CALCULATE([Nb feux], Communes[Secteur prioritaire 67] = TRUE()), [Nb feux])` | 3 | carte KPI + tableau des communes |

Toutes les formules sont dans `mesures.dax`.

## Les sources de données

| Source | Ce qu'elle apporte | Colonne de liaison |
|---|---|---|
| BDIFF (Grand Est, 2006-2025) | les feux : date, commune, surface, cause | Code commune, Date, Code département, Cause |
| COG 2026 de l'INSEE | les communes et les départements, avec leurs noms | Code commune, Code département |
| Météo des forêts (2024-2026) | le niveau de danger de chaque jour, par département | Date + Code département |

## Ce que les données ne disent pas (à dire à l'oral)

- 2009 est vide partout, et le Bas-Rhin n'a que 8 années renseignées sur 20 : une année sans feu saisi est « non renseignée », pas « 0 feu »
- la cause n'est connue que pour 13 % des feux
- la Météo des forêts n'existe que depuis juin 2024, de juin à septembre : le seuil se juge sur 46 feux dans le Grand Est, dont 8 dans le 67
- les causes ne sont jamais croisées avec une commune (données personnelles, `docs/qualite/regles.md`)
