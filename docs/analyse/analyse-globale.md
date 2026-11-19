# Analyse globale de la commande - SDIS 67, saison feux 2027

Projet : feux-de-foret-grand-est | Région : Grand Est | Réponse attendue le 11 décembre

Cette analyse reprend nos trois analyses individuelles :
[Lawson Robert](commande-lawson-robert.md),
[Denis Wilson-Bahun](commande-denis-wilson-bahun.md) et
[Franck Kevin Tambou](commande-franck-tambou.md).
Les termes techniques sont définis dans le [glossaire](../glossaire.md).

## La commande

Le SDIS du Bas-Rhin n'a pas le budget pour renforcer son dispositif sur tout le département pendant tout l'été. La direction doit donc choisir où concentrer ses moyens, et à partir de quel niveau de la Météo des forêts lancer le dispositif renforcé (patrouilles, guet). Elle veut aussi savoir comment l'indice se comporte dans le Bas-Rhin, dans le reste du Grand Est et en France.

Les chefs de centre reprochent deux choses au seuil actuel : des jours annoncés à danger élevé où aucun feu ne part (fausses alertes), et des feux qui partent des jours où l'indice est au plus bas (feux manqués).

## Nos questions

À trois, nous avions 22 questions, dont beaucoup se recoupaient. Nous en gardons 5, chacune liée à une décision que la direction devra prendre.

| # | Question | Ce que la réponse change pour le SDIS | Reprend |
|---|---|---|---|
| Q1 | Où et quand partent les feux dans le Bas-Rhin (communes ou massifs, mois, jours de la semaine) ? | Si les feux sont concentrés, on prépositionne des moyens sur ces secteurs et ces périodes. S'ils sont dispersés, on mise sur des moyens mobiles. | Lawson Q1, Denis Q1 et Q2, Franck Q1 |
| Q2 | Quelle part des feux a une cause humaine (agriculture, imprudence, malveillance) ? | Si elle est forte, une partie du budget va à la prévention plutôt qu'à la lutte. | Lawson Q2, Denis Q4 |
| Q3 | En plus du niveau de danger, est-ce que le type de jour (week-end, jour férié, vacances scolaires), l'historique de départs du secteur et le type de forêt (part de résineux) aident à prévoir les jours de départ de feu ? | Si oui, le SDIS déclenche le renfort avec une règle qui combine l'indice et ces variables, au lieu de l'indice seul. | Lawson Q3, Denis Q6 et Q8, Franck Q4 et Q5 |
| Q4 | Pour chaque seuil possible, combien de jours de renfort par été, combien de départs couverts, de fausses alertes et de feux manqués (et les feux manqués sont-ils graves ?), et combien cela coûte au regard du budget ? | C'est le choix du nouveau seuil, éventuellement différent selon les secteurs. | Lawson Q4 et Q5, Denis Q7, Franck Q2 |
| Q5 | L'indice se comporte-t-il dans le Bas-Rhin comme dans le reste du Grand Est et en France, à surface forestière comparable ? | Oui : un seuil régional commun. Non : un seuil propre au Bas-Rhin, et des arguments pour demander plus de moyens. | Lawson Q6 et Q7, Denis Q5 et Q9, Franck Q6 |

### Questions mises de côté

Denis demandait si les feux les plus étendus sont ceux éloignés d'une caserne ou détectés tard, et Franck posait la question de la charge d'intervention par centre. Ces questions sont utiles pour placer le guet, mais elles demandent les données détaillées d'intervention du SDIS 67 (heures d'alerte et d'arrivée), que nous n'avons pas. Nous les reprendrons si le SDIS nous les fournit.

## Hypothèses à vérifier

| # | Hypothèse | Question |
|---|---|---|
| H1 | Les feux se concentrent sur une minorité de communes ou de massifs. | Q1 |
| H2 | Une partie des feux a une cause humaine (agriculture, imprudence, malveillance). | Q2 |
| H3 | Le SDIS sait déjà que l'indice seul déclenche mal. Une règle qui combine le niveau de l'indice avec le type de jour, l'historique de départs du secteur et la part de résineux couvre au moins 20 % de départs de feu en plus que l'indice seul, pour le même nombre de jours de renfort. Réfutée si le gain est inférieur à 20 %, ou si retirer l'une des trois variables ne change pas le résultat. Ces trois variables ne font pas partie du calcul de l'indice, qui n'utilise que la météo. | Q3 |
| H4 | Le budget ne couvre qu'une partie des jours à risque, donc il faut choisir. | Q4 |
| H5 | Le bon seuil n'est pas le même d'un département à l'autre (climat, végétation). | Q5 |

## Ce que nous devons rendre le 11 décembre

1. Une carte des secteurs du Bas-Rhin où partent le plus de feux, avec les périodes à risque (Q1).
2. La part des causes humaines, pour trancher entre prévention et lutte (Q2).
3. Un tableau seuil par seuil : jours de renfort, coût, départs couverts, fausses alertes, feux manqués, avec un seuil recommandé (Q4). Le même tableau pour la règle « indice seul » et pour la règle combinée « indice + type de jour, historique du secteur, part de résineux », à nombre de jours de renfort égal (Q3).
4. Une comparaison du Bas-Rhin avec les autres départements du Grand Est et avec la France, calculée avec les mêmes définitions partout (Q5).

## Données dont nous avons besoin

| Questions | Donnée | Une ligne = | Période | Fraîcheur | Emprise | Source |
|---|---|---|---|---|---|---|
| Q1, Q2, Q3, Q5 | Liste des feux : date, commune, surface, cause | 1 feu | depuis 2006 | Annuelle | Bas-Rhin, Grand Est, France | BDIFF |
| Q3, Q4, Q5 | Niveau de la Météo des forêts prévu pour le lendemain | 1 jour × 1 département | saisons 2024 à 2026, de juin à septembre | Quotidienne | France | Météo-France (archives sur data.gouv.fr) |
| Q3, Q4, Q5 | Indice canadien (FWI, base de l'IFM) recalculé sur le passé | 1 jour × 1 maille | 10 ans | Quotidienne | Grand Est | Copernicus (CEMS) |
| Q4 | Coût d'une journée de renfort, budget 2027, seuil actuel | 1 valeur par secteur | 2026-2027 | Annuelle | Bas-Rhin | SDIS 67 (à demander) |
| Q3 | Jours fériés (zone Alsace-Moselle pour le 67) | 1 jour | 2006 à 2031 | Calculée à l'avance | France, par zone | calendrier.api.gouv.fr |
| Q3 | Vacances scolaires | 1 période × 1 académie | depuis 2017-2018 | Annuelle | France, par académie | Éducation nationale |
| Q1, Q4 | Grille DFCI de 2 km, pour découper le département en secteurs | 1 carreau | fixe | - | France | data.gouv.fr |
| Q1, Q3, Q5 | Surface forestière et essences | 1 polygone ou 1 commune | dernier millésime | Pluriannuelle | France | IGN (BD Forêt), CORINE Land Cover |
| Q5 | Nombre d'interventions pour feux de végétation | 1 année × 1 département | 2008 à 2024 | Annuelle | France | Ministère de l'Intérieur |
| toutes | Codes et contours des communes | 1 commune | 1 millésime par an | Annuelle | France | INSEE (COG), IGN (Admin Express) |

## Points d'attention

- La Météo des forêts n'existe que depuis juin 2023, ses archives publiques commencent en juin 2024 et elle n'est publiée que de juin à septembre. Pour couvrir dix ans et les mois de mars à mai, nous passerons par le FWI de Copernicus, converti en niveaux. Il faudra vérifier qu'il colle aux niveaux officiels sur 2024-2026.
- En 2025, la Météo des forêts a classé le Bas-Rhin en danger faible 115 jours et modéré 5 jours sur 120 ; jamais élevé. Si le seuil actuel est « élevé », le dispositif ne s'est jamais déclenché cette année-là. À confronter aux feux de la BDIFF.
- La Météo des forêts est publiée par département. Pour recommander un seuil par secteur, il faudra le FWI par maille.
- Pour croiser feux et indice, il faut la même date et la même zone des deux côtés, et le niveau prévu la veille, puisque c'est lui qui sert à déclencher.
- « Feu de forêt » et « jour avec feu » doivent avoir la même définition pour toutes les sources. La définition exacte de la BDIFF reste à vérifier.
- Le coût du renfort, le budget et le seuil actuel ne sont pas publics : la demande au SDIS 67 doit partir vite, sinon Q4 restera sans montant en euros.
- Les coordonnées précises des feux et leurs causes peuvent permettre d'identifier des personnes. Le responsable qualité et conformité décide de ce qu'on garde.
