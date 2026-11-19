# Fiche source : Comptes des SDIS 2012-2025 (OFGL)

Auteur : Franck Kevin TAMBOU
Exercice : 2 - Fiche d'identité des sources
Statut : fichier `ofgl-base-sdis.csv` ouvert et contrôlé ; page officielle relevée par recherche web.

Légende : **Vérifié (fichier)** = relevé dans le CSV ; **Vérifié (page)** = relevé sur la page data.gouv.fr ; **Non vérifiée** = à contrôler, raison indiquée.

## 1. Identification

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Nom | Comptes des SDIS 2012-2025 | Vérifié (page) |
| Description | Principaux agrégats financiers des services départementaux d'incendie et de secours | Vérifié (page) |
| URL de la source | https://www.data.gouv.fr/datasets/comptes-des-sdis-2012-2025 | Vérifié (page) |
| Fichier exploré | `ofgl-base-sdis.csv` (84 420 lignes, 15,2 Mo) | Vérifié (fichier) |

## 2. Provenance et propriété

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Producteur | OFGL (Observatoire des finances et de la gestion publique locale), créateur et éditeur | Vérifié (page) |
| Source des comptes | Balances comptables des SDIS publiées par la DGFiP | Vérifié (page) |
| Système source | Balances comptables de la DGFiP, agrégées par l'OFGL | Vérifié (page) |
| Date de mise à jour affichée | 20 juillet 2026 | Vérifié (page) |

## 3. Accès et format

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Mode d'accès | Téléchargement direct du fichier. Un JSON existe aussi (`ofgl-base-sdis.json`, 45,6 Mo reçu) ; son contenu identique n'a pas été comparé ligne à ligne. | Vérifié (page et fichiers) |
| Format | CSV, séparateur point-virgule, encodage UTF-8 avec marque BOM | Vérifié (fichier) |
| Colonnes | 21 : exercice, catégorie, code et nom de région, code et nom de département, SIREN et SIRET du budget, libellé du budget, CBUDG, nomenclature, agrégat, montant, montant par habitant, DOM, population, rural, nombre d'interventions 2025, strate, population équivalent habitant 2025, catégorie | Vérifié (fichier) |

## 4. Type de données

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Nature | Agrégats comptables annuels (fonctionnement, investissement, personnel, dette) | Vérifié (fichier) |
| Caractère | Quantitatif (montants en euros, montants par habitant) | Vérifié (fichier) |
| Statique ou série | Série annuelle | Vérifié (fichier) |

## 5. Granularité

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Une ligne représente | Un agrégat, pour un budget, pour un exercice | Vérifié (fichier) |
| Niveau géographique le plus fin | Département (code et nom du département) | Vérifié (fichier) |
| Budgets par département | Un budget principal, plus des budgets annexes (œuvres sociales, production d'énergie, cantines selon les départements) | Vérifié (fichier) |
| Pas de temps | Annuel | Vérifié (fichier) |

## 6. Couverture

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Emprise géographique | France, avec les départements du Grand Est (10 départements, 8 509 lignes). Nombre total de SDIS non compté. | Vérifié (fichier) |
| Période réellement couverte | Exercices 2012 à 2025 (14 ans) | Vérifié (fichier) |
| Volumétrie | 84 420 lignes ; 8 509 pour le Grand Est | Vérifié (fichier) |
| Nomenclatures | M61 (6 913 lignes GE), M57 (1 434), M4 (162) | Vérifié (fichier) |

Point d'attention : la page indiquait une couverture 2012-2023 dans une version antérieure, alors que le fichier couvre 2012-2025. La fiche retient le fichier.

## 7. Clés et jointures

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Clé département | `Code Département` (sur deux caractères) : à joindre au `num_dep` des archives Météo des forêts et au `code` du GeoJSON | Vérifié (fichier) |
| Clé temporelle | `Exercice` (année) | Vérifié (fichier) |
| Clé budget | `Siren SDIS`, `SIRET Budget`, `Libellé Budget` | Vérifié (fichier) |
| Changement de libellé | Le budget principal du Bas-Rhin et du Haut-Rhin s'appelle « SDIS » jusqu'en 2023, puis « SIS » en 2024-2025. Un filtre sur le libellé seul perd donc deux ans. | Vérifié (fichier) |
| Jointure possible | Avec les interventions par département (colonne `Nombre d'interventions 2025`, seulement pour 2025) et avec la Météo des forêts | Vérifié (fichier) |

## 8. Qualité

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Budgets à filtrer | Les annexes (œuvres sociales, production d'énergie) doivent être exclues des totaux départementaux | Vérifié (fichier) |
| Ruptures de série | Changement de nomenclature (M61 → M57) : les totaux ne sont pas forcément comparables d'une année à l'autre. Exemple Bas-Rhin : dépenses totales de 83,4 M€ en 2022 contre 95,7 M€ en 2023, à expliquer avant comparaison. | Vérifié (fichier) ; cause non vérifiée |
| Interventions | Disponibles pour 2025 seulement, dans le fichier | Vérifié (fichier) |
| Doublons | Non contrôlés sur la clé complète | Non vérifiée |

## 9. Juridique et données personnelles

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Licence | Licence Ouverte 2.0 selon la relecture de Denis (page data.gouv.fr) ; non reconfirmée à la date de cette fiche | Non vérifiée (à relever sur la page) |
| Données personnelles | Aucune : agrégats par établissement public, sans personne physique | Vérifié (fichier) |

## 10. Lien avec nos questions

| Rubrique | Valeur |
|:---------|:-------|
| Questions couvertes | Q1 (moyens par secteur), Q2 (budget par jour et par secteur, à croiser avec les volumes), Q6 (comparaison départementale) |
| Résultats utiles pour le Grand Est | Frais de personnel 2025 : Bas-Rhin 71,9 M€ (61 € par habitant SDIS), Moselle 68,0 M€, Haut-Rhin 46,6 M€, Meurthe-et-Moselle 44,8 M€. Ratio par habitant : Haute-Marne 81,5 €, Meuse 61,1 €, Bas-Rhin 61,4 € (chiffres issus du fichier, population SDIS 2025). |
| Limites | Pas de ventilation par centre ni par type de feu. Interventions 2025 seulement. Ruptures de nomenclature. |
| Décision | **Retenue**. Seule source de moyens financiers vérifiée pour Q2 et Q6. À compléter par les interventions SDIS pour Q3. |
