# Fiche source : BDIFF (Base de Données sur les Incendies de Forêts en France)

Auteur : Franck Kevin TAMBOU
Exercice : 2 - Fiche d'identité des sources
Sources de vérification :
- description officielle du site bdiff.agriculture.gouv.fr (texte transmis par l'auteur) ;
- mentions légales du site, PDF « BDIFF_IGNv1 » (transmis par l'auteur) ;
- définitions des champs, PDF « Définition des termes renseignés dans les fiches incendies » (transmis par l'auteur) ;
- **extrait de données** : fichier `Incendies.csv`, 736 lignes, Grand Est, feux de forêt (type F), 2006-01-01 à 2025-12-31 (transmis par l'auteur, ouvert et contrôlé).

Légende : **Vérifié** = constaté dans l'extrait ou dans un document officiel transmis ; **Non vérifiée** = à contrôler, raison indiquée.

## 1. Identification

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Nom | BDIFF : Base de Données sur les Incendies de Forêts en France | Officiel |
| Description | Application internet qui centralise les données sur les incendies de forêt sur le territoire français depuis 2006 et les met à disposition du public et des services de l'État | Officiel |
| URL | https://bdiff.agriculture.gouv.fr/ | Officiel |
| URL du fichier explorée | Non renseignée : extrait transmis par fichier (`Incendies.csv`) | Vérifié (fichier ouvert) |

## 2. Provenance et propriété

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Producteur et éditeur | Ministère de l'Agriculture et de la Souveraineté Alimentaire (MASA), direction générale de la performance économique et environnementale des entreprises (DGPE) | Officiel (mentions légales) |
| Conception et hébergement | Conception technique et développement par l'IGN ; hébergement par OVH | Officiel (mentions légales) |
| Système source | Collecte annuelle par un réseau de contributeurs (opérateurs de saisie), qui alimentent la base avec les incendies de l'année en cours. Les opérateurs agissent dans une mission d'intérêt public | Officiel (description et mentions légales) |
| Propriétaire des données | Non vérifiée : les mentions légales désignent le MASA comme éditeur et responsable de traitement, mais ne parlent pas de « propriété » des données | Non vérifiée |
| Date de dernière mise à jour | Non vérifiée : aucune date de mise à jour dans l'extrait | Non vérifiée |

## 3. Accès et format

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Mode d'accès | Consultation publique par l'application web, avec critères de sélection (date, région, type de feu) et export | Vérifié (critères et export présents dans l'extrait) |
| Format | **CSV**, séparateur `;`, valeurs entre guillemets, encodage UTF-8 avec BOM | Vérifié |
| Structure du fichier | 3 lignes de métadonnées (message d'ancienne version du formulaire, nombre d'incendies, critères de sélection), puis une ligne d'en-tête et les données | Vérifié |
| Schéma | 24 colonnes, décrites dans le PDF des définitions (voir glossaire BDIFF) | Vérifié |

Remarque : la première ligne du fichier indique que <q>certaines données sont associées à l'ancienne version du formulaire incendie</q>. Les colonnes de surface changent entre 2006-2022 et 2023 et après.

## 4. Type de données

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Nature | Registre d'événements : un enregistrement par incendie | Vérifié |
| Caractère | Quantitatif (surfaces en m², nombre de décès, bâtiments), qualitatif (nature, précision, type de peuplement) | Vérifié |
| Statique ou série | Série événementielle, de 2006 à 2025 | Vérifié |

## 5. Granularité

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Une ligne représente | **Un incendie**, identifié par l'année et un numéro. Aucun doublon d'identifiant constaté (0 cas sur 736 lignes) | Vérifié |
| Niveau géographique | **Commune** (code INSEE et nom) | Vérifié |
| Pas de temps | **Date et heure de première alerte** (au format `AAAA-MM-JJ hh:mm:ss`). Selon le PDF des définitions, il s'agit du moment où l'information d'un départ de feu parvient au CODIS | Vérifié |

**Correction par rapport à la version précédente de cette fiche** : j'avais écrit que la base ne permettait pas de descendre au jour. L'extrait contient la date et l'heure de chaque incendie. Le passage à la date est donc possible dans cet export. La mention « agrégée à la commune » concerne la consultation publique de l'application, pas l'extrait par critères.

## 6. Couverture

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Emprise géographique | Région Grand Est (critère de sélection), avec 10 départements : 08, 10, 51, 52, 54, 55, 57, 67, 68, 88 | Vérifié |
| Période couverte par les données | **Du 5 juin 2006 au 14 novembre 2025** (critères : du 1er janvier 2006 au 31 décembre 2025) | Vérifié |
| Années absentes dans l'extrait | Toute la région : 2009. Pour le Bas-Rhin : 2006, 2009, 2010 et de 2012 à 2019 (voir section 8) | Vérifié |
| Volumétrie | 736 incendies ; 24 colonnes ; fichier de 79,3 Ko | Vérifié |
| Surface totale parcourue | 15 814 226 m², soit environ 1 581 ha ; médiane 300 m² ; maximum 1 800 000 m² (2019, Meuse) | Vérifié |

Périmètre dans l'extrait : **Type de feu = F** (feu de forêt). Les feux de végétation hors forêt ne sont pas présents. Définition officielle : un incendie qui <q>démarre en forêt ou qui se propage en forêt ou au sein de terres boisées</q> ; dans l'aire méditerranéenne, les maquis et garrigues sont inclus.

## 7. Clés et jointures

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Clés disponibles | Code INSEE (commune), code département, date et heure de première alerte, année et numéro | Vérifié |
| Jointure possible avec Admin Express (communes) | Par le code INSEE | Déduit du champ présent ; jointure non testée |
| Jointure possible avec Météo des forêts | Par département et par date : seulement pour 2024 à 2025 (la Météo des forêts n'est archivée que depuis le 3 juin 2024) | Déduit des dates ; **12 incendies du Bas-Rhin** tombent dans cette fenêtre |

## 8. Qualité

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Cause (Nature) renseignée | **97 incendies sur 736** (13 %). Pour le Bas-Rhin : 13 sur 84 (15 %). Les 639 autres sont vides | Vérifié |
| Précision des surfaces | **Estimées** : 652 (89 %) ; **Mesurées** : 33 (4 %) ; vides : 51 (7 %) | Vérifié |
| Cohérence des surfaces | Aucune ligne où la surface en forêt dépasse la surface parcourue. Aucune surface parcourue égale à 0 | Vérifié |
| Doublon probable | Commune 67180 (Haguenau), 13 août 2025 à 17 h 54 : deux lignes (numéros 7287 et 11751), même surface (15 000 m²). **À traiter avant tout comptage** | Vérifié |
| Lignes marquées « données partielles » | Champ « Précision de la donnée » rempli par <q>Données partielles ou non valides</q> surtout de 2008 à 2012, et quelques lignes de 2023 à 2025 | Vérifié |
| Trou de série pour le Bas-Rhin | Aucun incendie du Bas-Rhin en 2006, 2009, 2010 et de 2012 à 2019 dans l'extrait. Cela peut être une absence réelle d'incendies ou un défaut de saisie. Non tranché | Non vérifiée (cause à déterminer) |
| Déséquilibre entre départements | Les Vosges (88) représentent 368 des 736 incendies (50 %). En 2020, 105 des 175 incendies sont dans les Vosges | Vérifié ; interprétation (effort de saisie ou réel) non vérifiée |
| Changement de définitions | Les définitions des surfaces diffèrent entre les fiches d'avant 2023 et celles de 2023 et après (surfaces autres terres boisées, non boisées). Les comparaisons de surfaces sur toute la période doivent en tenir compte | Vérifié (PDF des définitions) |

## 9. Juridique et données personnelles

| Rubrique | Valeur | Vérifié |
|:---------|:-------|:--------|
| Licence | **Pas de licence ouverte standard.** Réutilisation autorisée à des fins personnelles, associatives ou professionnelles, sans vente ni location, avec citation explicite du site et respect de l'intégrité des données. **Toute utilisation commerciale ou publicitaire est exclue.** | Vérifié (mentions légales, article 7) |
| Équivalence avec la Licence Ouverte 2.0 | Non équivalente : la clause d'exclusion commerciale n'existe pas dans la Licence Ouverte 2.0 | Analyse ; à valider par l'enseignante |
| Données personnelles dans l'extrait | **Aucune.** Les colonnes ne contiennent que des données sur les incendies et les communes | Vérifié (colonnes) |
| Données personnelles sur le site | Les comptes utilisateurs collectent nom, prénom, adresse électronique, organisme, téléphone. Ces données ne sont pas dans l'extrait, mais elles existent dans la plateforme | Vérifié (mentions légales) |
| Cause et données sensibles | Les champs de décès et de bâtiments sont des totaux par incendie, sans identité. Les 5 lignes où le champ est rempli indiquent 0 décès | Vérifié |

## 10. Lien avec nos questions

| Question | Possible avec la BDIFF ? | Condition |
|:---------|:-------------------------|:----------|
| **Q1** Secteurs les plus exposés (Bas-Rhin) | **Oui** | Commune et date ; attention au trou de série 2012 à 2019 |
| **Q2** Jours-secteurs financés | Non, la BDIFF ne contient pas de budget | Croiser avec les comptes des SDIS |
| **Q3** Charge d'intervention | Partiellement | La BDIFF compte les feux, pas les interventions. Compléter avec les interventions SDIS |
| **Q4** Fréquence des départs selon l'indice | **Limitée** | Seuls 12 incendies du Bas-Rhin (11 après suppression du doublon) tombent dans la fenêtre Météo des forêts 2024-2025. Il faut un indice historique (IFM) |
| **Q5** Faux positifs et faux négatifs | **Limitée** | Même limite que Q4 |
| **Q6** Comparaison départementale | **Oui** | Pour les années où les départements sont bien saisis ; le déséquilibre entre départements doit être pris en compte |

**Décision** : **retenue** comme historique principal des départs de feu. Limites : cause renseignée à 13 %, surfaces estimées à 89 %, trou de série pour le Bas-Rhin, doublon à traiter, fenêtre de recouvrement avec l'indice trop courte pour Q4 et Q5.
