# Plan du nettoyage et de la consolidation (#37)

Par : Firas (@firasjaouahdoups3-glitch), le 2026-11-19. À relire par Franck (responsable pipeline et modèle) avant de coder.

Ce document dit ce que fait le nettoyage, source par source, et quelles tables il produit. Les pièges viennent des [fiches sources](../sources/), les règles de [regles.md](../qualite/regles.md). Les points marqués **à valider** sont des propositions : on les tranche ensemble, puis ils vont dans le [journal des décisions](../decisions.md).

## 1. Le principe

```
data/raw/            data/processed/                  data/processed/
(brut, jamais        1 table propre par source        tables de travail
 modifié)       -->  (même grain que la source)  -->  (croisées, prêtes pour Q1 à Q5)
   #45                        étape 1                         étape 2
```

- **Étape 1, nettoyer :** chaque source est lue, corrigée (formats, codes, dates) et contrôlée avec ses règles. Une ligne reste une ligne de la source : un feu reste un feu, un bulletin reste un bulletin.
- **Étape 2, consolider :** on croise les tables propres pour fabriquer les tables de travail demandées dans #37.
- Le brut ne se touche jamais. On peut tout refaire depuis `data/raw/` avec une seule commande : `python -m src.nettoyage`.
- Relancer deux fois donne le même résultat (pas de ligne en double).
- Chaque étape passe par la **barrière de qualité** de `src/qualite` (#49) : une règle bloquante en échec arrête tout, une alerte est comptée dans le rapport.
- À chaque lancement, un rapport : lignes lues, gardées, marquées, par règle et par source.

## 2. Les choix communs à toutes les tables

| Sujet | Choix | Pourquoi |
|---|---|---|
| Codes commune | millésime COG 2026, 5 caractères (`67482`) | règles G1 et G2 : un ancien code est converti, jamais jeté |
| Codes département | 2 caractères avec le 0 (`08`) | règle G1, piège de la Météo des forêts (`8` en 2024-2025) |
| Dates | date du jour en **heure de Paris** | les sources mélangent UTC (Météo des forêts, calendrier scolaire, FIRMS) et heure locale |
| Surfaces | en hectares | règle B6 (la BDIFF est en m²) |
| Vide ≠ 0 | une année sans données est « non renseigné », jamais 0 | règles P1, P2, S2 |
| Données personnelles | jamais plus fin que commune × jour, pas de nom de commune dans les tables, pas de cause par commune | [regles.md, partie 4](../qualite/regles.md) |
| Format des fichiers | CSV en UTF-8, séparateur `,` | **à valider** : pas besoin de bibliothèque en plus. Le Parquet serait plus léger et garde les types, mais il faut ajouter `pyarrow` à `requirements.txt` |
| Période | 2006 à 2026 | la BDIFF commence en 2006. Chaque table garde ce que sa source couvre réellement |

## 3. Étape 1 : nettoyer chaque source

### COG (codes des communes)

- **Entrée :** `v_commune_2026.csv`, `v_mvt_commune_2026.csv`, `v_departement_2026.csv`
- **Ce qu'on fait :**
  - on garde seulement `TYPECOM = COM` (sinon 584 codes en double, à cause des communes déléguées)
  - table de passage « ancien code → code 2026 » à partir des mouvements. Il faut suivre les chaînes (A devient B en 2016, puis B devient C en 2019 → A donne C)
- **Sorties :**
  - `communes.csv` : 1 commune (code, département, région)
  - `passage_communes.csv` : 1 ancien code → son code 2026
- **Règles :** G1, et une nouvelle règle : chaque ancien code mène à un seul code 2026

### BDIFF (les feux)

- **Entrée :** l'export du script de #45, lu avec `lire_bdiff()` de #49 (en-tête, période, départements, règle B1)
- **Ce qu'on fait :**
  - identifiant du feu = `Année` + `Numéro`
  - code commune converti au COG 2026 avec `passage_communes.csv`. On garde aussi le code d'origine
  - date et heure de la première alerte. Une heure à `00:00:00` devient vide (B5)
  - surfaces en ha. On ne garde que `Surface parcourue` et `Surface forêt`, les seules comparables avant et après 2023 (B10)
  - cause : `Nature` gardée telle quelle, vide → « inconnue » (B9)
  - doublon probable (même commune, date, heure et surface, par ex. Haguenau 13/08/2025) : on garde le premier, l'autre est marqué (B3)
  - colonnes jetées (minimisation) : nom de la commune, décès, bâtiments détruits, colonnes de surface non comparables, colonnes toujours vides
- **Sortie :** `feux.csv`, 1 feu
- **Règles :** B1 à B10, G2, G3

### Météo des forêts (niveaux de danger)

- **Entrée :** `mdf_2024.csv.gz` à `mdf_2026.csv.gz`
- **Ce qu'on fait :**
  - séparateur `,` en 2024-2025 et `;` en 2026, colonne `nom_dep` ou `dep_nom` (M1)
  - `num_dep` sur 2 caractères (M2)
  - la date de diffusion est en UTC : conversion en heure de Paris, **puis + 1 jour** pour `niveau_j1`, qui vaut pour le lendemain (M5). On garde seulement `niveau_j1`, celui qui sert à déclencher la veille
  - un seul bulletin par jour et par département ; s'il y en a plusieurs, le dernier publié (M4)
  - on garde les 96 départements (utile pour comparer à la France, Q5)
- **Sortie :** `meteo_des_forets.csv`, 1 jour concerné × 1 département : date, département, niveau (1 à 4), date de diffusion
- **Règles :** M1 à M6

### Copernicus (FWI)

- **Entrée :** `fwi_grand_est_AAAA.nc`, un fichier par année, sur la grille d'origine (zone corrigée dans #45 : 13 × 22 mailles)
- **Ce qu'on fait :**
  - lecture avec `xarray`, une ligne par jour et par maille
  - identifiant de maille = latitude et longitude de son centre
  - 2026 s'arrête au 31/08 (jeu consolidé) : les jours manquants restent absents, pas à 0
- **Sorties :**
  - `fwi_maille.csv` : 1 jour × 1 maille (date, latitude, longitude, FWI)
  - `commune_maille.csv` : 1 commune → 1 maille (règle F4). **À valider :**
    - qui la fait : c'est une des deux pistes proposées à Franck dans le journal du 18/11
    - comment rattacher une commune : maille qui contient le centre de la commune (simple), ou maille qui couvre la plus grande partie de la commune (plus juste pour les grandes communes)
    - quels contours : Admin Express (IGN) ou geo.api.gouv.fr. Les deux sont au COG de l'année
- **Règles :** F1 à F5

### Interventions des SIS

- **Entrée :** `interventions2008.csv` à `interventions2024.csv`
- **Ce qu'on fait :**
  - lecture en cp1252, `?` des milliers retiré en 2024 (S1)
  - colonnes renommées pareil pour toutes les années (`Catégorie` / `Catégorie A`)
  - code département en majuscules (`2a` → `2A`)
  - feux de végétation vides pour 2010-2013 (pas de détail ces années-là) : « non renseigné », pas 0 (S2)
- **Sortie :** `interventions_sis.csv`, 1 année × 1 département
- **Règles :** S1, S2

### Calendrier : week-ends, jours fériés, vacances scolaires (Q3)

- **Entrées :** jours fériés (`alsace-moselle.json` pour le 57, le 67 et le 68 ; `metropole.json` pour les autres) et calendrier scolaire
- **Ce qu'on fait :**
  - une ligne par jour et par département
  - vacances : dates converties d'UTC en heure de Paris (sinon tout est décalé d'un jour), ligne « Élèves » gardée, département rattaché à son académie
  - avant 2017-2018, pas de données de vacances : « non renseigné »
- **Sortie :** `calendrier.csv`, 1 jour × 1 département : jour de la semaine, week-end, férié, vacances
- **À faire avant :** ces deux sources ne sont pas encore dans le script de récupération (#45). Il faut les y ajouter

### BD Forêt (surface et part de résineux)

- **Entrée :** les shapefiles par département (décompressés par #45)
- **Ce qu'on fait :** croiser les polygones avec les contours des communes, puis calculer par commune la surface de forêt et la part de résineux. On garde le millésime des photos (D3)
- **Sortie :** `foret_commune.csv`, 1 commune
- **Règles :** D1 à D3
- **À valider :** c'est le traitement le plus lourd (calcul géographique). On peut le faire en dernier, il ne sert qu'à Q1, Q3 et Q5

### NASA FIRMS (2026 seulement)

- **Entrée :** détections 2026 par l'API (voir la [fiche](../sources/fiche-nasa-firms.md)). À ajouter au script de récupération, la clé va dans `.env`
- **Ce qu'on fait :**
  - heures UTC → heure de Paris
  - on enlève `type = 2` (sources fixes) et les cases vues 10 jours ou plus dans l'année (usines)
  - rattachement à la commune, puis regroupement par commune et par jour
- **Sortie :** `firms_commune_jour.csv`, 1 commune × 1 jour avec au moins une détection. Ce sont des « détections satellite », jamais des « départs de feu »

## 4. Étape 2 : les tables de travail

### Table 1 : les feux (demandée dans #37)

`feux.csv` de l'étape 1, plus la maille de la commune et le calendrier du jour. C'est la base de Q1 et Q2.

### Table 2 : jour × département (demandée dans #37)

Une ligne par jour et par département du Grand Est, de 2006 à 2026.

| Colonne | D'où | Vide quand |
|---|---|---|
| date, département | calendrier | jamais |
| niveau Météo des forêts | `meteo_des_forets.csv` | hors saison publiée et avant juin 2024 |
| FWI moyen du département | `fwi_maille.csv` + `commune_maille.csv` | après le 31/08/2026 |
| nombre de feux, surface brûlée | `feux.csv` | **non renseigné** si le département-année est vide dans la BDIFF (P1) |
| statut BDIFF | règle P1 | jamais : « renseigné » ou « non renseigné » |
| week-end, férié, vacances | `calendrier.csv` | vacances avant 2017-2018 |

**À valider :** comment calculer le FWI moyen d'un département :
- moyenne des mailles dont le centre est dans le département ;
- ou moyenne sur ses communes, pondérée par la surface.

La fiche Copernicus a utilisé la première méthode (24 mailles pour le Bas-Rhin).

### Pour plus tard, à décider avec Franck

- **Q3 et Q4 par secteur :** une table jour × maille (FWI, feux, part de résineux, historique de départs), parce que le niveau de la Météo des forêts n'existe que par département
- **le modèle en étoile du 9/12 :** les tables ci-dessus deviennent les faits (feux, jours) et les dimensions (date, commune, maille, département, niveau). Ce plan essaie déjà d'avoir les clés qu'il faudra

## 5. Le code

```
src/nettoyage/
  __main__.py            python -m src.nettoyage : lance tout, dans l'ordre
  commun.py              chemins, lecture/écriture, conversion UTC -> Paris
  cog.py                 communes + passage des anciens codes
  bdiff.py               feux (réutilise src/qualite/bdiff.py)
  meteo_des_forets.py
  copernicus.py
  interventions_sis.py
  calendrier.py
  bd_foret.py
  firms.py
  tables.py              étape 2 : tables de travail
tests/test_nettoyage.py  petites tables faites à la main, comme dans #49
```

Ordre : COG d'abord (tout le monde en a besoin), puis les sources une par une, puis les tables de travail.

## 6. L'ordre de travail proposé

| # | Quoi | Dépend de | Visé pour |
|---|---|---|---|
| 1 | ce plan, relu par Franck | rien | 21/11 |
| 2 | COG + BDIFF → `feux.csv` | #45, #49 | 24/11 |
| 3 | Météo des forêts, interventions SIS | #45 | 26/11 |
| 4 | calendrier (avec l'ajout dans la récupération) | rien | 27/11 |
| 5 | Copernicus + `commune_maille.csv` | #45, choix de la méthode | 1/12 |
| 6 | table jour × département | 2 à 5 | 3/12 |
| 7 | BD Forêt, FIRMS | 5 | 5/12 |
| 8 | prêt pour le modèle en étoile | 6 | 8/12 |

Une PR par étape, pour que chaque relecture reste courte.

## 7. Questions ouvertes

- **Pour Franck :**
  - format CSV ou Parquet ?
  - prends-tu la table commune → maille ? Avec quelle méthode ?
  - comment calculer le FWI moyen d'un département ?
- **Pour le groupe :**
  - l'heure de la BDIFF est-elle en heure de Paris ? Probable, mais pas écrit dans la fiche
  - calage de H3 sur des années trouées (voir le [rapport de qualité](../qualite/rapport-qualite.md)) : la période retenue change les années à nettoyer en priorité
- **Pour la récupération :** ajouter les jours fériés, le calendrier scolaire et FIRMS au script de #45 (dans #37 ou dans une issue à part ?)
