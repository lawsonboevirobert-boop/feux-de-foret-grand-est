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

## 6. Confrontation avec les sources

Section 6 : la section 5 existe déjà (données idéales, exercice 1). Cette section est celle de l'exercice 3, partie A.

Sources de l'inventaire du groupe ([inventaire.md](../sources/inventaire.md)) : BDIFF, COG, Météo des forêts, interventions des SIS, comptes des SDIS par l'OFGL (ma fiche, #31), Copernicus (FWI), BD Forêt.

Degrés : complet / partiel / absent / inconnu. Chaque raison cite la colonne du fichier ou la rubrique de la fiche.

| Question | BDIFF | COG | Météo des forêts | Interventions SIS | OFGL | Copernicus | BD Forêt |
|---|---|---|---|---|---|---|---|
| Q1 où partent les feux dans le 67, et les moyens y sont-ils proportionnés ? | partiel : `Code INSEE` donne la commune et `Date de première alerte` le jour, mais pas de coordonnées ni de massif. Aucun feu saisi dans le 67 en 2006, 2009, 2010, de 2012 à 2019 et en 2021 (rubrique « Contrôles qualité »). Rien sur les centres ni les effectifs | partiel : pas de feux, sert seulement à rattacher `Code INSEE` à `COM` et `DEP`. Les codes de notre export sont déjà tous au COG 2026 (matrice, note 3) | absent : grain = 1 département par jour (`num_dep`), pas de feux ni de moyens | absent : grain = 1 département par an (`Numéro`), pas de commune ni de centre | absent : « une ligne = un agrégat, pour un budget, pour un exercice » (rubrique « Grain »), pas de feux ni de détail par centre | absent : que de la météo (`fwinx`), pas de feux | partiel : `tfv` et `essence` situent les massifs et leur type, mais pas de code commune (jointure spatiale) et photos de 2007 pour le 67 |
| Q2 combien de jours-secteurs de renfort le budget finance, et quels secteurs d'abord ? | partiel : `Code INSEE` + `Date de première alerte` montrent les communes qui brûlent le plus, donc les secteurs à couvrir d'abord. Rien sur le budget, et mêmes années vides qu'en Q1 | absent | partiel : `niveau_j1` permet de compter les jours par niveau (67 en 2025 : 115 faible, 5 modéré, jamais élevé), mais par département et pas par secteur, 3 saisons (2024 à 2026) de juin à septembre | absent : totaux annuels d'interventions, pas de jours ni de coût | partiel : budget total du SDIS 67 par an (rubrique « Grain »), rien sur le coût d'un jour de renfort ; rupture de série en 2024 dans le 67 (passage en M57, rubrique « Contrôles qualité ») | partiel : `fwinx` permet de compter les jours au-dessus d'un seuil, par maille (`latitude`, `longitude`), donc plus fin que le département, mais ce n'est pas l'indice officiel | absent : pas de feux ni de budget |
| Q3 charge d'intervention par centre en période à risque, et part des départs maîtrisés ? | partiel : `Date de première alerte` et `Code INSEE` donnent les feux de la période à risque, mais pas de centre ni d'effectifs. Aucune colonne ne distingue un départ maîtrisé d'un feu déclaré : `Surface parcourue` peut servir de proxy (531 feux de moins d'1 ha, rubrique « Ce qu'on retient ») | absent | partiel : `niveau_j1` situe la période à risque, mais 3 saisons de juin à septembre, et rien sur les centres ni les effectifs | absent : grain = 1 département par an (`Numéro`), pas de centre ni de période | absent : budget de tout le SDIS, pas d'effectifs par centre | partiel : `fwinx` situe la période à risque toute l'année, mais rien sur les centres ni les effectifs | absent |
| Q4 fréquence des départs selon la classe de l'indice, dans le 67 | partiel : `Date de première alerte` au jour près, mais seules 2024 et 2025 se croisent avec la Météo des forêts (12 feux dans le 67), et les années vides rendent les « jours sans feu » douteux (règle P1) | partiel : sert à rattacher `Code INSEE` à `DEP` pour croiser le feu avec le niveau | partiel : `niveau_j1` par jour et par département, mais 3 saisons (2024 à 2026) et seulement de juin à septembre (rubrique « Période réellement couverte ») ; dans le 67, jamais « très élevé » | absent : totaux annuels, pas de date | absent : des montants, pas de feux | partiel : `fwinx` tous les jours, toute l'année et sur plus de dix ans, mais c'est un proxy du niveau officiel (corrélation de rang 0,6 avec `niveau_j1`) et une grille (`latitude`, `longitude`) : il faut la table commune -> maille | absent |
| Q5 part des faux positifs et des faux négatifs | partiel : un faux positif = un jour sans feu, et les années vides du 67 rendent ces jours douteux (règle P1). `Date de première alerte` donne le jour de chaque départ, donc les faux négatifs | partiel : sert à rattacher le feu au département (`DEP`) | partiel : `niveau_j1`, 3 saisons de juin à septembre. Les 6 jours « élevé » du 67 sont tous en 2026, année que la BDIFF n'a pas encore : aucun faux positif calculable avec le niveau officiel (rubrique « Ce qu'on retient ») | absent : pas de date | absent | partiel : `fwinx` toute l'année ; sur les 12 feux du 67 en 2024-2025, 6 tombent des jours « faibles » et 3 hors saison (rubrique « Ce qu'on retient »), mais le seuil de FWI est à caler sur les niveaux officiels | absent |
| Q6 le 67 comparé au Grand Est et à la France | partiel : `Département` couvre les 10 départements, mais la saisie est inégale (les Vosges font la moitié des feux), et notre export ne prend que le Grand Est (rubrique « Emprise ») | partiel : `DEP` et `REG` pour regrouper | partiel : `num_dep` couvre les 96 départements, mais 3 saisons | partiel : colonne « Feux de végétations » par `Numéro` et par an, absente de 2010 à 2013 ; compte toute la végétation, pas que la forêt | absent : des montants, pas de feux | partiel : téléchargé sur le Grand Est seulement (rubrique « Emprise »), à résumer par département ; la France est possible mais plus lourde | partiel : surface de forêt par département pour comparer à surface égale, mais un fichier par département et des millésimes différents |

Aucune question n'a de source « complet ». Aucune case « inconnu » : tout a été vu dans un fichier ou une fiche.

### Décisions

- Q1 : approximer + collecter. La commune (`Code INSEE`) remplace le massif, et la BD Forêt sert à classer les communes par type de forêt (jointure spatiale, D7). Les années vides comptent comme « non renseigné », jamais comme « 0 feu » (règle P1). Les centres et leurs effectifs ne sont dans aucune source ouverte : à ajouter à la demande au SDIS 67 (#41). Ce que ça mesure mal : un massif coupé entre plusieurs communes, et la forêt telle qu'elle était en 2007
- Q2 : collecter + approximer. Le coût d'un jour de renfort et le budget 2027 ne sont que chez le SDIS 67 (#41, D2). En attendant, on compte les jours à risque par maille avec le FWI, et on donne un ordre de grandeur à partir du budget OFGL, en disant que c'est le budget de tout le SDIS. Ce que ça mesure mal : une maille de Copernicus n'est pas un secteur du SDIS, et la série OFGL du 67 a une rupture en 2024 (M57)
- Q3 : collecter, sinon renoncer en partie. La charge par centre demande les interventions une par une avec le centre (#41). Sans réponse, on renonce à la charge par centre et on donne seulement le nombre de feux en période à risque. La part des départs maîtrisés s'approxime avec `Surface parcourue` (un feu de moins d'1 ha compté comme départ maîtrisé), seuil à valider avec le groupe. Ce que ça mesure mal : un petit feu n'est pas forcément un feu maîtrisé tôt
- Q4 : approximer. Le FWI de Copernicus remplace le niveau officiel de 2016 à 2025 et pour les mois hors juin-septembre (D4). Les classes de FWI sont calées sur les niveaux de la Météo des forêts 2024-2026. Les taux se calculent sur les années renseignées seulement (D5). À faire avant : la table commune -> maille. Ce que ça mesure mal : le niveau officiel ajoute la sécheresse de la végétation et l'avis des prévisionnistes
- Q5 : approximer. Même base que Q4 : avec le niveau officiel seul, aucun faux positif « élevé » n'est calculable, puisque les 6 jours « élevé » du 67 sont en 2026. Les faux positifs se comptent sur les années renseignées de la BDIFF. Pour arbitrer le seuil, il faut le coût d'un jour de renfort (Q2, #41). Ce que ça mesure mal : même une année renseignée, un jour « sans départ » peut cacher un feu non saisi, donc les faux positifs sont plutôt surestimés
- Q6 : approximer, et renoncer en partie. Grand Est : FWI résumé par département et feux rapportés à la surface de forêt de la BD Forêt, sur les années où chaque département a des feux saisis. France : on renonce à comparer à surface de forêt égale (D3), on se limite aux niveaux de la Météo des forêts (96 départements, 3 saisons) et aux feux de végétation des SIS. Ce que ça mesure mal : la saisie de la BDIFF n'est pas la même d'un département à l'autre

### Ce qui a changé par rapport à la section 5

- je voulais 10 ans d'indice apparié aux départs, d'avril à octobre : la Météo des forêts n'a que 3 étés, de juin à septembre, et seules 2024 et 2025 se croisent avec la BDIFF. Copernicus rattrape l'historique, mais en proxy
- je voulais les départs avec leur cause, par commune, sur 10 ans : dans le 67, la BDIFF a 12 années vides sur 20, et la cause est vide pour 71 feux sur 84
- je pensais trouver les effectifs et les coûts par centre (Q1 à Q3) : aucune source ouverte ne descend au centre. L'OFGL donne le budget de tout le SDIS, les SIS des totaux annuels par département
- je n'avais pas prévu de jointure par maille : Copernicus est une grille, il faut une table commune -> maille avant tout calcul sur l'indice
- pour Q6, je voulais les mêmes données pour la France que pour le 67 : au niveau national on se limite aux niveaux officiels et aux feux de végétation des SIS
