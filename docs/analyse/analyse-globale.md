# Analyse globale de la commande - SDIS 67, saison feux 2027

Projet : feux-de-foret-grand-est | Région : Grand Est | Réponse attendue le 11 décembre

Cette analyse reprend nos quatre analyses individuelles :
[Lawson Robert](commande-lawson-robert.md),
[Denis Wilson-Bahun](commande-denis-wilson-bahun.md),
[Franck Kevin Tambou](commande-franck-tambou.md) et
[Firas](commande-firas-ja.md), arrivé le 18/11.
Les termes techniques sont définis dans le [glossaire](../glossaire.md).

## La commande

Le SDIS du Bas-Rhin n'a pas le budget pour renforcer son dispositif sur tout le département pendant tout l'été. La direction doit donc choisir où concentrer ses moyens, et à partir de quel niveau de la Météo des forêts lancer le dispositif renforcé (patrouilles, guet). Elle veut aussi savoir comment l'indice se comporte dans le Bas-Rhin, dans le reste du Grand Est et en France.

Les chefs de centre reprochent deux choses au seuil actuel : des jours annoncés à danger élevé où aucun feu ne part (fausses alertes), et des feux qui partent des jours où l'indice est au plus bas (feux manqués).

## Nos questions

À trois, nous avions 22 questions, dont beaucoup se recoupaient. Nous en gardons 5, chacune liée à une décision que la direction devra prendre.

| # | Question | Ce que la réponse change pour le SDIS | Reprend |
|---|---|---|---|
| Q1 | Où et quand partent les feux dans le Bas-Rhin (communes ou massifs, mois, jours de la semaine) ? | Si les feux sont concentrés, on prépositionne des moyens sur ces secteurs et ces périodes. S'ils sont dispersés, on mise sur des moyens mobiles. | Lawson Q1, Denis Q1 et Q2, Franck Q1, Firas Q1 |
| Q2 | Quelle part des feux a une cause humaine (agriculture, imprudence, malveillance) ? | Si elle est forte, une partie du budget va à la prévention plutôt qu'à la lutte. | Lawson Q2, Denis Q4 |
| Q3 | En plus du niveau de danger, est-ce que le type de jour (week-end, jour férié, vacances scolaires), l'historique de départs du secteur et le type de forêt (part de résineux) aident à prévoir les jours de départ de feu ? | Si oui, le SDIS déclenche le renfort avec une règle qui combine l'indice et ces variables, au lieu de l'indice seul. | Lawson Q3, Denis Q6 et Q8, Franck Q4 et Q5, Firas Q5 |
| Q4 | Pour chaque seuil possible, combien de jours de renfort par été, combien de départs couverts, de fausses alertes et de feux manqués (et les feux manqués sont-ils graves ?), et combien cela coûte au regard du budget ? | C'est le choix du nouveau seuil, éventuellement différent selon les secteurs. | Lawson Q4 et Q5, Denis Q7, Franck Q2, Firas Q2, Q3 et Q4 |
| Q5 | L'indice se comporte-t-il dans le Bas-Rhin comme dans le reste du Grand Est et en France, à surface forestière comparable ? | Oui : un seuil régional commun. Non : un seuil propre au Bas-Rhin, et des arguments pour demander plus de moyens. | Lawson Q6 et Q7, Denis Q5 et Q9, Franck Q6, Firas Q6 |

### Questions mises de côté

Denis demandait si les feux les plus étendus sont ceux éloignés d'une caserne ou détectés tard, et Franck posait la question de la charge d'intervention par centre. Ces questions sont utiles pour placer le guet, mais elles demandent les données détaillées d'intervention du SDIS 67 (heures d'alerte et d'arrivée), que nous n'avons pas. Nous les reprendrons si le SDIS nous les fournit.

Firas demandait aussi ce que donne la saison 2026, la plus récente. La BDIFF s'arrête à 2025 : aucune de nos sources ne donne encore les feux de 2026. Sa fiche NASA FIRMS (#36) dira si les détections satellite peuvent combler ce trou.

## Hypothèses à vérifier

Chaque hypothèse a maintenant un seuil chiffré et ce qui la réfuterait, fixés avant les calculs dans les fiches indicateurs ([kpi/02](../../kpi/02_fiches_indicateurs.md)) et dans le [journal](../decisions.md) (#40).

| # | Hypothèse | Question |
|---|---|---|
| H1 | Les feux se concentrent sur une minorité de communes ou de massifs. Chiffrée par Firas : dans le Bas-Rhin, les 10 communes prioritaires, classées avant la saison, reçoivent au moins 27 % des départs en couvrant au plus 10 % du département. Réfutée si elles en reçoivent moins sur les saisons 2026 et 2027 cumulées (au moins 20 départs). **Où on en est :** 27 % en 2024-2025 (3 départs sur 11) pour 8,3 % de la surface ; à mesurer sur 2026-2027, la BDIFF 2026 n'est pas encore publiée. | Q1 |
| H2 | Une partie des feux a une cause humaine (agriculture, imprudence, malveillance). Chiffrée par Denis : la cause involontaire (travaux, particuliers) fait plus de la moitié des causes connues dans chaque sous-ensemble fixé à l'avance (sans les Ardennes, feux de 1 ha ou plus, 2019-2025), toujours lue avec le taux de cause renseignée. Réfutée si un sous-ensemble d'au moins 20 causes connues passe sous 50 %. **Où on en est :** elle tient, 60 % sur le Grand Est (58 sur 97) et entre 57 % et 62 % dans les sous-ensembles, mais 13,2 % seulement des départs ont une cause. Le 67 seul ne se lit pas (13 causes connues). | Q2 |
| H3 | Le SDIS sait déjà que l'indice seul déclenche mal. Une règle qui combine le niveau de l'indice avec le type de jour, l'historique de départs du secteur et la part de résineux couvre au moins 20 % de départs de feu en plus que l'indice seul, pour le même nombre de jours de renfort. Réfutée si le gain est inférieur à 20 %, ou si retirer l'une des trois variables ne change pas le résultat. Ces trois variables ne font pas partie du calcul de l'indice, qui n'utilise que la météo. **Où on en est :** non validée le 25/11 ([test de H3](test-h3.md), #99). La règle combinée couvre 66 départs sur 123, mais avec 105 jours de renfort au lieu de 19 ; à jours égaux, 24 départs contre 23 pour l'indice seul. | Q3 |
| H4 | Le budget ne couvre qu'une partie des jours à risque, donc il faut choisir. Elle reste une limite, pas une hypothèse testée, tant que le SDIS 67 n'a pas donné son budget et le coût d'un jour de renfort (#41). **Ce qu'on sait déjà :** un seuil fixe calé pour 20 jours par saison en donne 44 sur 2017-2025 ; la règle qui tient le budget chaque saison (seuil recalé avant la saison, avec plafond) couvre 16 % des départs (97 sur 614) avec 20 jours au plus ([Q4](budget-jours-q4.md), #103). | Q4 |
| H5 | Le bon seuil n'est pas le même d'un département à l'autre (climat, végétation). Chiffrée par Franck : un seuil propre au Bas-Rhin couvre au moins 20 % de départs en plus que le seuil régional, sans plus de jours de renfort (test 2017-2025). **Où on en est :** réfutée, − 10 % (35 départs couverts sur 63 contre 39 avec le seuil régional, pour 40 et 44 jours par saison). On garde le seuil régional. | Q5 |

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
