# Fiche source : Archives de la Météo des forêts

Auteur : Franck Kevin TAMBOU
Exercice : 2 - Fiche d'identité des sources
Statut : métadonnées vérifiées sur la page officielle ; fichiers annuels 2024, 2025 et 2026 ouverts et contrôlés

Légende : **Vérifié (page)** = relevé sur la page Météo-France / data.gouv.fr ; **Vérifié (fichier)** = relevé dans les fichiers annuels ouverts ; **Non vérifiée** = à contrôler, raison indiquée.

## 1. Identification

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Nom | Archives de la Météo des forêts | Vérifié (page) |
| Description | Niveau de danger de feu de forêt par département, établi à partir des prévisions météorologiques et de l'état de sécheresse de la végétation. Délivré pour J+1 et J+2. | Vérifié (page) |
| URL de la source | https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets (page de référence) | Vérifié (page) |
| Fichiers explorés | `mdf_2024.csv.gz`, `mdf_2025.csv.gz`, `mdf_2026.csv.gz` | Vérifié (fichier) |

## 2. Provenance et propriété

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Producteur | Météo-France | Vérifié (page) |
| Système source | Non vérifiée : la page indique qu'elle combine prévisions météo et état de sécheresse, sans détailler le modèle de calcul | Non vérifiée (documentation technique non consultée) |
| Propriétaire des données | Non vérifiée : la page demande de citer Météo-France comme source, sans préciser le propriétaire juridique | Non vérifiée |
| Date de mise à jour | Année en cours mise à jour chaque jour de juin à septembre ; l'archive 2026 contient des données jusqu'au 05/10/2026 | Vérifié (fichier) |

## 3. Accès et format

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Mode d'accès | Téléchargement direct d'un fichier annuel, sans authentification. L'API temps réel (avec authentification) est un autre flux et n'est pas nécessaire ici. | Vérifié (page) |
| Format | CSV compressé en gzip (`.csv.gz`) | Vérifié (fichier) |
| Séparateur | Virgule en 2024 et 2025, point-virgule en 2026 | Vérifié (fichier) |
| Schéma | 5 colonnes : date de production, code département, niveau J+1, niveau J+2, nom du département. Les noms changent selon l'année (voir section 7). | Vérifié (fichier) |

## 4. Type de données

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Nature | Série temporelle quotidienne de niveaux de danger (prévision, pas une mesure) | Vérifié (page) |
| Caractère | Qualitatif ordinal à 4 niveaux : 1 vert (faible), 2 jaune (modéré), 3 orange (élevé), 4 rouge (très élevé) | Vérifié (page) |
| Statique ou série | Série temporelle | Vérifié (fichier) |

## 5. Granularité

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Une ligne représente | Un département, pour une date de production | Vérifié (fichier) |
| Niveau géographique le plus fin | Département (96 départements métropolitains, codes 01 à 95 avec 2A et 2B) | Vérifié (fichier) |
| Pas de temps | Une production par jour, à heure fixe (vers 16 h 50 ou 18 h locales selon l'année) | Vérifié (fichier, heures relevées sur les horodatages) |
| Lignes par date | 96, soit une ligne par département | Vérifié (fichier) |

## 6. Couverture

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Emprise géographique | France métropolitaine, 96 départements | Vérifié (fichier) |
| Période couverte | 3 juin 2024 au 5 octobre 2026 (trois saisons) | Vérifié (fichier) |
| Dates distinctes | 2024 : 120 ; 2025 : 120 ; 2026 : 131 | Vérifié (fichier) |
| Volumétrie | 2024 : 11 520 lignes ; 2025 : 11 520 lignes ; 2026 : 12 576 lignes | Vérifié (fichier) |
| Lignes Grand Est | 1 080 (2024), 1 080 (2025), 1 310 (2026) | Vérifié (fichier) |

Point d'attention : la période couverte est de trois saisons. C'est insuffisant pour calibrer seul un seuil, mais suffisant pour une première comparaison entre saisons.

## 7. Clés et jointures

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Clé département | `num_dep` (dans les trois fichiers) : code sur deux caractères, à joindre au champ `code` du GeoJSON des départements | Vérifié (fichier et GeoJSON) |
| Clé temporelle | Colonne `date` (dans les trois fichiers) | Vérifié (fichier) |
| Noms de colonnes | Le nom du département change : `nom_dep` (2024, 2026) ou `dep_nom` (2025). La page officielle parle de `Reference_time` et `dep_code` : ces noms ne figurent pas dans les archives ouvertes, mais se retrouvent dans l'échantillon de flux. À harmoniser avant jointure. | Vérifié (fichier et page) |
| Jointure possible | Avec les départs de feu par département et par jour (BDIFF ou SDIS) | Déduit, non vérifié (pas encore fait) |

## 8. Qualité

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Complétude | Nombre de lignes égal à 96 × nombre de dates dans les trois fichiers. Champs vides non contrôlés. | Vérifié (fichier, comptage) |
| Doublons | Non contrôlés (pas de test de clé unique) | Non vérifiée |
| Anomalie à signaler | En 2024, tous les jours et tous les départements du Grand Est sont au niveau 1. Ce résultat est à vérifier avant tout usage comme référence. | Vérifié (fichier) |
| Incohérence de documentation | La page annonce 4 niveaux et les colonnes décrites ; l'échantillon du 22/05/2024 ne montre que les niveaux 1 à 3 | Vérifié (page et fichier) |

## 9. Juridique et données personnelles

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Licence | Licence Ouverte d'Etalab, sans redevance | Vérifié (page) |
| Mention de source | « Source : Météo-France » ou « Informations créées à partir de données de Météo-France » | Vérifié (page) |
| Données personnelles | Aucune : données géographiques (département) et de danger, sans identification de personnes | Vérifié (fichier, 5 colonnes) |

## 10. Lien avec nos questions

| Rubrique | Valeur |
|:---------|:-------|
| Questions couvertes | Q4 (fréquence des départs selon le niveau de danger) et Q5 (faux positifs et faux négatifs), à condition de disposer des départs de feu. Q6 (comparaison départementale) est possible sur les trois saisons. |
| Limites | Trois saisons seulement. Niveau départemental, alors que l'indice de l'exercice 1 est calculé par zone. Aucune donnée de départs de feu dans cette source. Année 2024 à vérifier (tous niveaux à 1 en Grand Est). |
| Décision | **Retenue**. C'est la source la plus directe pour le niveau de danger. Elle doit être croisée avec la BDIFF ou les interventions SDIS pour répondre à Q4 et Q5. |
