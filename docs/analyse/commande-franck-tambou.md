# Analyse de la commande : saison feux 2027 (SDIS 67)

Auteur : Franck Kevin TAMBOU
Exercice 1:  De la commande aux données partie B
Région : Grand Est

## 1. Décision attendue

La direction du SDIS 67 (Bas-Rhin) doit arbitrer deux points avant l'été 2027 :

1. où concentrer les moyens humains et financiers contre les départs de feu ;

2. à partir de quel niveau de l'indice Météo-Forêt déclencher le dispositif renforcé (patrouilles, guet).

Elle veut aussi comparer le Bas-Rhin aux autres départements de la région et au niveau national. Réponse attendue le 11 décembre.

## 2. Questions analytiques

Domaine 1 : ressources humaines et financières

- **Question 1.** Dans quels secteurs du Bas-Rhin les départs de feu sont-ils les plus fréquents, et les moyens actuels (centres, effectifs, patrouilles) y sont-ils proportionnés ?
  *Décision : où répartir les moyens humains.*
- **Question 2.** Combien de jours-secteurs de dispositif renforcé le budget permet-il de financer cet été, et quels secteurs couvrir en priorité ?
  *Décision : où et combien de temps activer le renfort.*
- **Question 3.** Quelle est la charge d'intervention par centre en période à risque, et quelle part des départs est maîtrisée avant de devenir des feux déclarés ?
  *Décision : dimensionner les effectifs d'été.*

Domaine 2 : prévisions de feux de forêt

- **Question 4.** Quelle est la fréquence des départs de feu selon la classe de l'indice Météo-Forêt, dans le Bas-Rhin ?
  *Décision : à partir de quelle classe déclencher le dispositif renforcé.*
- **Question 5.** Quelle part des jours à indice élevé n'a donné lieu à aucun départ (faux positifs), et quelle part des départs a eu lieu à indice bas (faux négatifs) ?
  *Décision : arbitrer le seuil entre coût du renfort et risque manqué.*
- **Question 6.** Comment l'indice se comporte-t-il dans le Bas-Rhin par rapport aux autres départements de la région et à la moyenne nationale ?
  *Décision : garder un seuil commun ou un seuil propre au département.*

## 3. Termes inconnus (à mettre dans le glossaire)

- **Indice Météo-Forêt** : indicateur quotidien de danger de feu de forêt, par zone. Son mode de calcul et ses classes restent à vérifier auprès de Météo-France.
- **Départ de feu** : début d'un feu, à distinguer du feu déclaré (qui mobilise les secours).
- **Dispositif renforcé** : moyens supplémentaires activés en cas de danger élevé (patrouilles, guet).
- **Faux positif / faux négatif** : indice élevé sans départ / départ à indice bas.
- **Grain** : niveau de détail d'une donnée (commune, jour, centre).
- **Emprise** : périmètre géographique couvert par la donnée.
- **Fraîcheur** : délai entre l'événement et la disponibilité de la donnée.

## 4. Besoins et hypothèses de travail

- **Hypothèse 1.** Les départs de feu se concentrent sur une minorité de communes ou de massifs (pinèdes, landes, massifs boisés).
- **Hypothèse 2.** La fréquence des départs augmente avec la classe de l'indice, mais la relation est faible : beaucoup de jours à indice élevé restent sans départ.
- **Hypothèse 3.** L'indice ne capte pas tout. Une part des départs survient les jours de vent fort ou d'activité humaine (week-ends, jours fériés), même à indice modéré.
- **Hypothèse 4.** Le seuil optimal diffère selon le département, à cause du climat et de la végétation. Un seuil régional unique serait donc un compromis.
- **Hypothèse 5.** Le budget ne couvre qu'une fraction des jours-secteurs à risque, ce qui impose de prioriser.

Besoins déduits : un historique de départs de feu géolocalisé, un historique quotidien de l'indice par zone, les effectifs et les coûts par centre, et des données comparables pour les autres départements.

## 5. Données idéales

| Questions | Donnée à obtenir | Grain | Période | Fraîcheur | Emprise |
|:----------|:-----------------|:------|:--------|:---------:|:--------|
| **Q1, Q3** | Départs de feu et interventions | Commune · date · cause | 10 dernières années, saison estivale | Annuelle | Bas-Rhin, puis Grand Est |
| **Q2** | Coût journalier du dispositif renforcé, budget 2027 | Centre ou secteur | Saison 2026 | Mensuelle | Bas-Rhin |
| **Q4, Q5** | Indice Météo-Forêt quotidien, apparié aux départs | Zone météo ou commune · jour | 10 dernières années, avril à octobre | Quotidienne | Bas-Rhin |
| **Q6** | Mêmes données pour les autres départements | Département · jour | Identique à Q4 et Q5 | Quotidienne | Grand Est, France |
