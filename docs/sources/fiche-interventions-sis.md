# Fiche source : Interventions réalisées par les services d'incendie et de secours

Explorée par : @lawsonboevirobert-boop, le 2026-11-17
Lien : <https://www.data.gouv.fr/datasets/interventions-realisees-par-les-services-d-incendie-et-de-secours>
Fichiers ouverts : les 17 fichiers annuels, de `interventions2008.csv` à `interventions2024.csv`

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | Ministère de l'Intérieur. D'après la fiche, la Direction générale de la sécurité civile et de la gestion des crises (DGSCGC) collecte ces chiffres chaque année auprès des SDIS, de la brigade de sapeurs-pompiers de Paris et du bataillon de marins-pompiers de Marseille. |
| Mode d'accès (export, API, téléchargement) et format | Téléchargement direct sur data.gouv.fr, sans compte : un CSV par année. Séparateur point-virgule, encodage Windows (cp1252), pas UTF-8 : les accents s'affichent mal si on ouvre le fichier en UTF-8. |
| Grain (une ligne = ?) | Un service d'incendie et de secours pour une année : le nombre d'interventions par type (feux d'habitation, feux de végétations, secours à personne, accidents…), plus la catégorie du service (A, B ou C). Ce sont des totaux annuels, pas des interventions une par une : pas de date, pas de commune. |
| Emprise géographique | France, outre-mer compris : 98 lignes par an jusqu'en 2013, 99 ensuite. Paris et la petite couronne sont regroupés dans une seule ligne (BSPP), et Marseille a sa propre ligne (BMPM) à côté de celle du SDIS des Bouches-du-Rhône. |
| Période réellement couverte par les données | De 2008 à 2024, une année par fichier. Le détail « Feux de végétations » n'existe que pour 2008, 2009 et de 2014 à 2024 : les fichiers 2010 à 2013 n'ont que 16 colonnes, avec le total des incendies sans le détail par type. |
| Date de dernière mise à jour affichée sur la fiche | 2 juillet 2026 (ajout du fichier 2024). |
| Fréquence de mise à jour | Annuelle d'après la fiche. Le fichier d'une année arrive environ un an et demi après : celui de 2024 a été mis en ligne en juillet 2026. |
| Volumétrie | 1 677 lignes sur les 17 fichiers, 16 à 71 colonnes selon l'année, environ 30 Ko par fichier. |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | Le numéro de département (`Numéro`) et l'année. Attention : dans le fichier 2024, la Corse est écrite `2a` et `2b` en minuscules (non vérifié pour les autres années), et les colonnes `Zone` et `Région` suivent les anciennes régions jusqu'en 2015 (Alsace, Lorraine, Champagne-Ardenne), puis « Grand Est » à partir de 2016. Il vaut mieux joindre sur le numéro que sur le nom de région. |
| Données personnelles | Aucune : uniquement des totaux par département et par année. |
| Licence | Licence Ouverte (code `fr-lo` sur data.gouv.fr). |
| Questions de l'analyse auxquelles elle pourrait répondre | Q5 surtout : comparer le nombre de feux de végétation du Bas-Rhin avec les autres départements du Grand Est et la France, d'une année à l'autre. Elle ne peut pas servir pour Q1, Q3 ou Q4, faute de date et de commune. |

## Contrôles qualité repérés

- Doublons : aucun numéro de département en double dans une même année.
- Dates : chaque fichier ne contient que son année.
- Codes géographiques : les 10 départements du Grand Est sont présents chaque année. Les noms de région changent en 2016 (voir les clés).
- Format des nombres : dans le fichier 2024, les milliers sont séparés par un point d'interrogation (`1?265` pour 1 265) dans 1 563 cellules. Si on ne nettoie pas ce caractère, ces nombres sont lus comme du texte et disparaissent des totaux. Les autres années n'ont pas ce problème.
- Structure : 70 colonnes en 2008-2009, 16 de 2010 à 2013, 71 à partir de 2014. La colonne de catégorie s'appelle `Catégorie` jusqu'en 2016, puis `Catégorie A`.
- Valeurs manquantes : 2 à 5 cases vides par an en général, mais 57 en 2019 et en 2022, et 66 en 2008.

## Ce qu'on retient

Cette source ne remplace pas la BDIFF, mais elle aide à la lire. Le Bas-Rhin compte des centaines d'interventions pour feux de végétations chaque année (631 en 2008, 1 433 en 2015, 214 en 2024), alors que la BDIFF n'y enregistre que quelques feux de forêt par an, et aucun certaines années. Les deux sources ne comptent pas la même chose (toute la végétation d'un côté, la forêt de l'autre), mais l'écart montre que l'absence de feu dans la BDIFF ne veut pas dire absence d'intervention. Pour Q5, elle permet une comparaison simple entre départements : en 2024, le Bas-Rhin pèse 214 des 1 824 feux de végétations du Grand Est, et la France en compte 29 270.
