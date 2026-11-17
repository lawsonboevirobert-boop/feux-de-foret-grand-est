# Fiche source : Interventions réalisées par les services d'incendie et de secours (2008-2024)

Auteur : Franck Kevin TAMBOU
Exercice : 2 - Fiche d'identité des sources
Statut : fichiers annuels 2008 à 2024 ouverts et contrôlés (2012 présent en double, contenu identique). **2019 et 2025 non reçus.**

Légende : **Vérifié (fichier)** = relevé dans les CSV ; **Vérifié (page)** = relevé sur la page data.gouv.fr ou interieur.gouv.fr ; **Non vérifiée** = à contrôler, raison indiquée.

## 1. Identification

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Nom | Interventions réalisées par les services d'incendie et de secours (statistiques annuelles par département) | Vérifié (page) |
| Description | Nombre d'interventions des sapeurs-pompiers par département et par catégorie, pour les SDIS, la BSPP et le BMPM | Vérifié (page et fichier) |
| URL de la source | https://www.data.gouv.fr/datasets/interventions-realisees-par-les-services-d-incendie-et-de-secours (page de référence) | Vérifié (page) |
| Fichiers explorés | 16 CSV : `interventions2008` à `2018` (2012 présent deux fois), `2020` à `2024`. 2019 non reçu. | Vérifié (fichier) |

## 2. Provenance et propriété

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Producteur | Direction générale de la sécurité civile et de la gestion des crises (DGSCGC), ministère de l'Intérieur | Vérifié (page) |
| Système source | Enquête annuelle déclarative auprès des services d'incendie et de secours, via le site InfoSDIS | Vérifié (page) |
| Propriétaire des données | Ministère de l'Intérieur (DGSCGC). Licence et mention de source non relevées sur la page. | Non vérifiée |

## 3. Accès et format

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Mode d'accès | Téléchargement de fichiers annuels | Vérifié (fichier) |
| Format | CSV, séparateur point-virgule, encodage cp1252 (caractères accentués mal lus si ouvert en UTF-8) | Vérifié (fichier) |
| Nombres | Séparateur de milliers : espace (2013-2018, 2020-2024), absent en 2010-2012. « N.C. » = donnée non communiquée (quelques cellules, dont Paris et Martinique 2018). En 2024, le séparateur est mal encodé dans le fichier, mais les chiffres sont récupérables. | Vérifié (fichier) |
| Schéma | Deux schémas. 2008-2009 : détail par catégorie, total en colonne 70. 2010-2013 : 16 colonnes agrégées (« Incendies » en colonne 7, total en colonne 16). 2014-2024 : environ 70 colonnes détaillées (dont « Feux de végétations » en colonne 16, « Incendies » en colonne 18). Les noms de colonnes changent (« Catégorie » devient « Catégorie A », « Secours à victime » devient « Secours à victimes », etc.). | Vérifié (fichier) |

## 4. Type de données

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Nature | Comptages annuels d'interventions (événements déclarés par les SDIS) | Vérifié (fichier) |
| Caractère | Quantitatif, entier | Vérifié (fichier) |
| Statique ou série | Série annuelle | Vérifié (fichier) |

## 5. Granularité

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Une ligne représente | Un service (SDIS, BSPP, BMPM) pour une année | Vérifié (fichier) |
| Niveau géographique le plus fin | Département (numéro et nom), avec zone et région | Vérifié (fichier) |
| Pas de temps | Annuel | Vérifié (fichier) |
| Lignes par fichier | Une ligne par département, plus BSPP et BMPM. 10 lignes Grand Est par fichier, vérifiées. | Vérifié (fichier) |

## 6. Couverture

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Emprise géographique | France entière, dont le Grand Est (10 départements) | Vérifié (fichier) |
| Période couverte | 2008 à 2024, sauf 2019 (non reçu) et 2025 (non reçu) : 16 années disponibles | Vérifié (fichier) |
| Volumétrie | Environ 9 Ko par fichier en 2008-2013, environ 30 Ko en 2014-2024 | Vérifié (fichier) |
| Interventions Grand Est (total) | 279 670 (2008) ; 394 520 (2018) ; 352 192 (2024) | Vérifié (fichier) |

Point d'attention : 2019 et 2025 manquent. La page ne renseigne pas la couverture temporelle ; la série est donc présentée avec ce trou.

## 7. Clés et jointures

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Clé département | Numéro de département (colonne « Numéro », codes sur deux caractères, 2A et 2B pour la Corse). À joindre au `num_dep` de la Météo des forêts et au `Code Département` des comptes des SDIS. | Vérifié (fichier) |
| Clé temporelle | Année | Vérifié (fichier) |
| Jointure | Avec les comptes des SDIS (années communes 2012-2018 et 2020-2024 ; 2025 seulement côté comptes) | Déduit, non vérifié (jointure non faite) |

## 8. Série Grand Est et Bas-Rhin (contrôlée)

Totaux calculés depuis les CSV (somme des 10 départements Grand Est, et ligne Bas-Rhin). « Incendies » = colonne « Incendies » du fichier, qui regroupe tous les feux déclarés.

| Année | GE total | BR total | GE incendies | GE végétations |
|:------|--------:|--------:|-----------:|--------------:|
| 2008 | 279 670 | 44 961 | 30 160 | 2 972 |
| 2009 | 304 023 | 62 500 | 30 304 | 3 760 |
| 2010 | 319 701 | 60 841 | 30 224 | n.d. |
| 2011 | 346 218 | 68 019 | 29 179 | n.d. |
| 2012 | 344 867 | 69 755 | 28 306 | n.d. |
| 2013 | 366 700 | 96 802 | 24 771 | n.d. |
| 2014 | 344 542 | 67 418 | 24 430 | 4 017 |
| 2015 | 355 431 | 73 683 | 27 959 | 6 512 |
| 2016 | 343 891 | 62 028 | 22 540 | 2 709 |
| 2017 | 351 439 | 75 829 | 24 308 | 3 448 |
| 2018 | 394 520 | 87 358 | 28 831 | 5 041 |
| 2019 | non reçu | non reçu | non reçu | non reçu |
| 2020 | 333 664 | 66 720 | 27 340 | 5 548 |
| 2021 | 334 211 | 61 777 | 22 302 | 2 489 |
| 2022 | 356 923 | 64 704 | 26 755 | 5 442 |
| 2023 | 343 093 | 57 130 | 25 435 | 4 040 |
| 2024 | 352 192 | 59 450 | 21 043 | 1 824 |

n.d. : colonne absente dans le schéma 2010-2013. Les végétations existent en 2008-2009 et 2014-2024.

## 9. Qualité

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Valeurs manquantes | « N.C. » en quelques cellules (Paris et Martinique 2018, entre autres). Aucune valeur manquante pour les 10 départements du Grand Est dans les fichiers lus. | Vérifié (fichier) |
| Ruptures de série | Bas-Rhin : 60 841 (2010) à 69 755 (2012) puis 96 802 (2013) : +39 % en un an, porté par « Secours à victime ». Bas-Rhin 2008 à 2009 : 44 961 à 62 500 (+39 %), même ordre de grandeur. Cause (changement de méthode ou de déclaration) non vérifiée. | Vérifié (fichier) ; cause non vérifiée |
| Ruptures de nomenclature | Changement de schéma en 2014 (détail des feux), et entre 2009 et 2010 (16 colonnes agrégées). Les catégories ne sont pas comparables entre schémas. | Vérifié (fichier) |
| Doublons | Fichier 2012 présent deux fois : mêmes totaux (344 867 pour le Grand Est). | Vérifié (fichier) |
| Définition de « Incendies » | Regroupe tous les feux déclarés (habitations, ERP, véhicules, végétations, autres). Ce n'est pas un indicateur de feux de forêt. | Vérifié (fichier) |
| Cohérence avec d'autres sources | Le Bas-Rhin compte 59 450 interventions en 2024 dans cette série, alors que le fichier OFGL des comptes affiche 66 976 pour 2025 ; ce dernier chiffre n'est pas une valeur de même année. Les deux sources ne comptent probablement pas la même chose. À vérifier avant toute jointure. | Vérifié (fichier) ; définition non vérifiée |

## 10. Juridique et données personnelles

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Licence | Non relevée dans les fichiers ni dans l'extrait de page consulté | Non vérifiée |
| Données personnelles | Aucune : comptages agrégés par département | Vérifié (fichier) |

## 11. Lien avec nos questions

| Rubrique | Valeur |
|:---------|:-------|
| Questions couvertes | Q3 (charge par centre, ici par département), Q1 et Q2 (moyens rapportés à l'activité), Q5 (comparaison des départs et des niveaux de danger) |
| Résultats utiles | Végétations (disponibles 2008-2009 et 2014-2024) : Grand Est de 1 824 (2024) à 6 512 (2015). Bas-Rhin : 164 (2017) à 1 433 (2015). Les totaux et les végétations varient fortement d'une année à l'autre. |
| Limites | Pas de ventilation par centre. Pas de distinction entre forêt et autres végétations. Pas de date ni d'heure. Ruptures de série en 2010 et 2013-2014. 2019 et 2025 non reçus. |
| Décision | **Retenue**. Seule source de nombre d'interventions par département et par année disponible dans le lot. Série utilisable 2008-2024 sauf 2019, à relier aux comptes des SDIS pour Q2. |
