# Analyse de la commande - SDIS 67 (Bas-Rhin), saison feux 2027

Projet : feux-de-foret-grand-est | Région : Grand Est | Auteur : Lawson Robert

**Problématique :** avec un budget limité, où et à partir de quel niveau de la Météo des forêts déclencher le dispositif renforcé dans le Bas-Rhin pour réduire au mieux les départs de feu en 2027 ?

## 1. Questions

| # | Question | Décision |
|---|---|---|
| Q1 | Où se concentrent les départs de feu dans le Bas-Rhin ? | Répartition des moyens par secteur |
| Q2 | Quelle part des feux est d'origine humaine ou liée à la météo ? | Prévention ciblée ou surveillance météo |
| Q3 | Quand l'indice est élevé (ou bas), quelle part des jours compte un feu ? | Évaluer le seuil actuel (fausses alertes, feux manqués) |
| Q4 | Pour chaque seuil possible, combien de jours activés et de feux couverts ? | Choix du nouveau seuil |
| Q5 | Combien coûte un jour de dispositif renforcé et combien le budget en permet-il ? | Plafond de jours activables |
| Q6 | Le Bas-Rhin se comporte-t-il comme le reste du Grand Est ? | Seuil local ou régional |
| Q7 | Le Grand Est se comporte-t-il comme les autres régions de France (Méditerranée, Nouvelle-Aquitaine, Bretagne, etc.) : fréquence des feux, part des jours à indice élevé avec feu, fausses alertes ? | Savoir si l'indice national est fiable ici ou s'il faut un seuil propre au Grand Est |

## 2. Termes inconnus

Météo des forêts, IFM (indice forêt météo), niveaux de danger, dispositif renforcé, BDIFF, interface habitat-forêt, fausse alerte, feu manqué, DFCI.

## 3. Besoins

- Localiser et qualifier les feux (lieu, cause, surface) : Q1, Q2
- Relier chaque jour à son indice et à ses feux : Q3, Q4
- Connaître le coût du dispositif et le budget : Q5
- Refaire les calculs pour les 10 départements du Grand Est : Q6
- Refaire les mêmes calculs pour les autres régions et comparer à la France entière, avec les mêmes définitions (feu de forêt, jour avec feu, indice) : Q7

## 4. Données

| Question | Donnée idéale | Grain | Période | Emprise |
|---|---|---|---|---|
| Q1, Q2 | Feux : lieu, date, cause, végétation, surface | Un feu | 10 ans minimum | Bas-Rhin |
| Q3, Q4 | Indice quotidien (prévu la veille) croisé avec le nombre de feux | Un jour par département | 10 ans, mars à octobre | Bas-Rhin |
| Q5 | Coût d'une journée de dispositif, budget | Une valeur | Saison 2026 | SDIS 67 |
| Q6 | Mêmes données que Q3 | Un jour par département | 10 ans | Grand Est |
| Q7 | Mêmes données que Q3, agrégées par région, avec taux de base (part des jours avec feu), taux de fausses alertes et taux de feux couverts | Un jour par département, regroupé par région | 10 ans | Toutes les régions de France |

**Sources :** SDIS 67 (interventions), BDIFF, Météo-France (indice), IGN et CORINE (occupation du sol), EFFIS. Accès à confirmer.
