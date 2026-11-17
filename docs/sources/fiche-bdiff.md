# Fiche source : BDIFF (Base de données sur les incendies de forêt en France)

Explorée par : @lawsonboevirobert-boop, le 2026-11-17
Liens : <https://bdiff.agriculture.gouv.fr/incendies> et la fiche <https://www.data.gouv.fr/datasets/base-de-donnees-sur-les-incendies-de-forets-en-france-bdiff>
Fichier ouvert : export CSV du Bas-Rhin, années 2006 à 2025 (`Incendies.csv`), et le PDF `Définitions.pdf` livré dans le même ZIP

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | Application web du ministère de l'Agriculture (`bdiff.agriculture.gouv.fr`). La fiche data.gouv.fr est publiée par l'IGN. Qui saisit les fiches incendie : non vérifiée, ce n'est écrit ni dans l'export ni dans le PDF de définitions. |
| Mode d'accès (export, API, téléchargement) et format | Formulaire de recherche sur le site (années, département, commune, surfaces…), puis bouton « Télécharger CSV ». On reçoit un ZIP avec `Incendies.csv`, `Définitions.pdf` et `Mention légales.pdf`. CSV en UTF-8, séparateur point-virgule, nombres au format français, et 3 lignes de résumé de la recherche avant la ligne d'en-tête. La ressource data.gouv.fr est étiquetée « api » mais renvoie vers la page d'accueil du site ; nous n'avons pas trouvé d'API documentée. |
| Grain (une ligne = ?) | Un incendie : année, numéro, département, code INSEE et nom de la commune, date et heure de première alerte, surfaces parcourues par type de végétation (en m²), précision des surfaces, nature de la cause, décès et bâtiments touchés. La localisation s'arrête à la commune : pas de coordonnées. L'export appliquait le filtre « Type de feu : F » proposé par défaut. |
| Emprise géographique | France entière d'après la fiche. Comptages faits sur le site pour 2006-2025 : 52 811 incendies en France, 736 dans les 10 départements du Grand Est, 84 dans le Bas-Rhin, 77 dans le Haut-Rhin, 368 dans les Vosges. |
| Période réellement couverte par les données | Le site couvre 2006 jusqu'à l'année précédente (2025 aujourd'hui). Pour le Bas-Rhin, l'export va du 16 avril 2007 au 31 août 2025, et seules 8 années ont des feux : 2007 (7), 2008 (8), 2011 (5), 2020 (22), 2022 (28), 2023 (2), 2024 (1) et 2025 (11). Aucun feu n'est enregistré en 2006, 2009, 2010, de 2012 à 2019 ni en 2021. |
| Date de dernière mise à jour affichée sur la fiche | 13 décembre 2025 sur data.gouv.fr. La même fiche annonce une couverture 2006-2022, alors que le site fournit déjà les feux de 2025 : la fiche est en retard sur le site. |
| Fréquence de mise à jour | Annuelle d'après la fiche data.gouv.fr, qui précise que le site donne les feux « jusqu'à l'année antérieure ». Les feux de 2026 ne sont donc pas encore disponibles. |
| Volumétrie | Export du Bas-Rhin : 84 lignes, 24 colonnes, environ 10 Ko. France entière sur 2006-2025 : 52 811 incendies (comptage du site, export complet non téléchargé). |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | Le code INSEE de la commune (avec le COG et les contours de communes), le département et la date de première alerte (avec la Météo des forêts). Le couple année + numéro identifie un incendie : aucun doublon dans l'export. Le millésime du COG utilisé pour les codes commune : non vérifié, il n'est indiqué nulle part. |
| Données personnelles | Pas de nom, pas d'adresse, pas de coordonnées : la localisation s'arrête à la commune. Deux champs restent sensibles : la nature de la cause (dont « Malveillance ») et le nombre de décès, à manipuler avec le responsable qualité et conformité. |
| Licence | Licence Ouverte 2.0 d'après la fiche data.gouv.fr. Le PDF `Mention légales.pdf` livré dans l'export : non vérifié, nous ne l'avons pas ouvert. |
| Questions de l'analyse auxquelles elle pourrait répondre | Q1 (communes et mois des feux), Q2 (cause, mais rarement renseignée), Q3 et Q4 (dates des feux à croiser avec les niveaux de l'indice), Q5 (nombre de feux par département). |

## Contrôles qualité repérés

- Doublons : aucun sur le couple année + numéro.
- Dates : toutes entre 2007 et 2025, avec une heure renseignée pour chaque feu.
- Années vides : 12 années sans aucun feu dans le Bas-Rhin. Il faudra savoir s'il n'y a vraiment pas eu de feu ou si les fiches n'ont pas été saisies, avant de calculer une moyenne annuelle.
- Valeurs manquantes : la cause (« Nature ») n'est renseignée que pour 13 feux sur 84 (5 accidentels, 3 malveillances, 3 involontaires de particuliers, 2 involontaires liés à des travaux). Le type de peuplement est toujours vide, ce qui est normal : d'après les définitions, il ne concerne que les départements méditerranéens.
- Changement de formulaire en 2023 : les colonnes de surface ne sont pas les mêmes avant et après la campagne 2023 (le PDF de définitions le détaille). Il faudra regrouper les deux jeux de colonnes.
- Précision : 67 surfaces estimées, 2 mesurées, 15 non précisées ; 13 feux sont marqués « données partielles ou non valides ».

## Ce qu'on retient

C'est la seule source qui liste les feux un par un, donc nous en avons besoin pour toutes les questions. Mais dans le Bas-Rhin, elle est petite : 84 feux en vingt ans, souvent de quelques centaines de m² (médiane 400 m², le plus grand fait 7 ha), dont 13 à Haguenau. Ce qui nous a le plus surpris : 43 de ces 84 feux sont partis entre janvier et mai, surtout en avril (20 feux), donc en dehors de la période où la Météo des forêts est publiée. Pour juger le seuil, il faudra un indice qui couvre aussi le printemps. Le PDF de définitions répond aussi à une question de notre glossaire : un incendie de forêt est un feu qui démarre ou se propage en forêt ou dans des terres boisées. Le PDF ne fixe pas de surface minimale pour l'incendie ; le seuil de 0,5 ha sert seulement à dire ce qui compte comme forêt.
