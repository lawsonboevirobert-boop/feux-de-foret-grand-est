# Règles de qualité et données personnelles

Premier jet (#9). A compléter au fur et a mesure du pipeline (#37, #38). Tout changement de règle ou de seuil -> une entrée dans le [journal des décisions](../decisions.md).

Basé sur ce qu'on a trouvé dans les [fiches sources](../sources/) et sur les cours du 17/11 (RGPD) et du 18/11 (qualité).

## 1. Comment on s'en sert

- les règles sont des **tests** : chacune doit pouvoir s'écrire en quelques lignes de python ou de SQL, et tourner a chaque chargement
- elles tournent au passage `data/raw/` (brut, pas touché) -> `data/processed/` (nettoyé). Le brut ne se modifie jamais, on peut tout refaire depuis lui
- chaque règle a un niveau :
  - **bloquant** : on arrete le chargement, faut corriger avant
  - **alerte** : on charge quand meme mais on marque les lignes et on le compte dans le rapport
  - **info** : juste compté dans le rapport
- a chaque chargement on sort un petit rapport de qualité (nb de lignes lues / gardées / marquées par règle, date du chargement, fichier source). Relancer le chargement 2 fois doit donner le meme résultat (pas de lignes en double)
- les seuils ci-dessous sont des choix du groupe pour démarrer, a ajuster quand on aura les vrais chiffres

Les 6 dimensions du cours (ISO/IEC 25012) : complétude, exactitude, cohérence, validité, unicité, actualité. Chaque règle dit laquelle elle teste.

## 2. Règles par source

### Codes géographiques (COG)

| Id | Dimension | Règle | Seuil | Si ca casse |
|---|---|---|---|---|
| G1 | validité | code commune = 5 caractères (`67482`, `2A004`), code département = 2 caractères avec le 0 devant (`08` et pas `8`) | 100% | bloquant (on corrige le format avant, cf piège Météo des forêts) |
| G2 | cohérence | tout code commune des autres tables existe dans le COG 2026, apres conversion avec le fichier des mouvements | 100% apres conversion | bloquant |
| G3 | cohérence | les 2 premiers caractères du code commune = le département annoncé dans la ligne | 100% | alerte |
| G4 | unicité | un code commune 2026 n'apparaît qu'une fois dans `communes.csv` (on garde `TYPECOM = COM`), et un code d'origine qu'une fois dans `passage_communes.csv` | 0 doublon | bloquant |
| G5 | cohérence | un ancien code (depuis 2006) mène à une seule commune 2026. S'il en donne plusieurs (commune scindée), il est marqué « ambigu », jamais deviné | 0 | alerte : les feux concernés restent sans commune 2026 et sont listés |

G1, G4 et G5 sont codées dans `src/nettoyage/cog.py` (#37). DOM compris dans le format : département sur 3 caractères (`971`).

On travaille tout au millésime COG 2026. Les anciens codes (fusions de communes, 20 changements dans le 67 depuis 2006) sont convertis, jamais jetés.

### BDIFF (liste des feux)

| Id | Dimension | Règle | Seuil | Si ca casse |
|---|---|---|---|---|
| B1 | validité | on saute les 3 lignes de texte, l'entete est a la ligne 4, 24 colonnes | exact | bloquant |
| B2 | unicité | `Année` + `Numéro` unique | 0 doublon | bloquant |
| B3 | unicité | pas 2 feux avec meme commune + meme date et heure + meme surface (ex : Haguenau 13/08/2025 17:54, numéros 7287 et 11751) | 0 | alerte : on garde le premier, l'autre est marqué "doublon probable" |
| B4 | cohérence | `Année` = année de `Date de première alerte` | 100% | bloquant |
| B5 | exactitude | heure a 00:00:00 pile = heure inconnue (7 feux) | info | on met l'heure a vide, on garde la date |
| B6 | validité | surfaces >= 0, en m2 a l'entrée, converties en ha dans `data/processed` | 100% | bloquant |
| B7 | cohérence | `Surface forêt` <= `Surface parcourue` | 100% | alerte |
| B8 | exactitude | surface parcourue > 500 ha dans le Grand Est = a vérifier a la main (max vu : 180 ha) | info | on regarde, on ne corrige pas sans preuve |
| B9 | complétude (cellule) | `Nature` (la cause) vide | info, 87% aujourd'hui (639 sur 736) | on garde "inconnue", jamais remplacé par une cause devinée |
| B10 | cohérence | seules `Surface parcourue` et `Surface forêt` sont comparables avant/apres 2023 (nouveau formulaire) | - | les autres colonnes de surface ne sont pas utilisées pour comparer des années |

### Météo des forêts

| Id | Dimension | Règle | Seuil | Si ca casse |
|---|---|---|---|---|
| M1 | validité | lecture selon l'année : séparateur `,` (2024-2025) ou `;` (2026), colonne `nom_dep` ou `dep_nom` | exact | bloquant |
| M2 | validité | `num_dep` remis sur 2 caractères (`8` -> `08`), sinon on perd les Ardennes a la jointure | 100% | bloquant |
| M3 | validité | `niveau_j1` dans {1, 2, 3, 4} | 100% | bloquant |
| M4 | unicité | un seul bulletin par jour et par département (si plusieurs : on garde le dernier publié) | 0 doublon apres | alerte |
| M5 | cohérence | le `niveau_j1` du bulletin du jour J vaut pour le jour J+1 : la date est décalée avant toute jointure avec les feux | - | règle de transformation |
| M6 | complétude (temps) | chaque jour de la saison publiée a un bulletin pour chaque département | 100% | alerte, les jours manquants sont listés dans le rapport |

### Copernicus (FWI)

| Id | Dimension | Règle | Seuil | Si ca casse |
|---|---|---|---|---|
| F1 | complétude (temps) | 365 ou 366 jours par année téléchargée, pas de trou | 100% | bloquant (on retélécharge) |
| F2 | complétude (cellule) | aucune valeur vide sur la grille du Grand Est | 0 | alerte |
| F3 | exactitude | FWI entre 0 et 100 (max vu : 83,2) | 100% | alerte |
| F4 | cohérence | chaque commune du Grand Est est rattachée a une seule maille (table commune -> maille) | 100% | bloquant |
| F5 | actualité | on note la version (`consolidated`, `4_1`) et la date de téléchargement. Les mises a jour sont arretées depuis le 16/11/2026 | - | info |

### Interventions des SIS

| Id | Dimension | Règle | Seuil | Si ca casse |
|---|---|---|---|---|
| S1 | validité | encodage Windows a l'ouverture, `?` comme séparateur des milliers en 2024 a nettoyer avant de convertir en nombre | 100% des cellules converties | bloquant |
| S2 | complétude (temps) | une valeur par département et par année, de 2008 a 2024. Pas de détail feux de végétation de 2010 a 2013 (2019 est bien la : 751 feux de végétation dans le 67). « N.C. » (non communiqué, Martinique 2018) = vide | - | info : années absentes = vides, pas 0 |
| S3 | unicité | une seule ligne par année et par service (`Numéro`). BSPP et BMPM sont des services, pas des départements : leur colonne `departement` reste vide | 0 doublon | bloquant |

M2 à M6, S1 à S3 sont codées dans `src/nettoyage/meteo_des_forets.py` et `src/nettoyage/interventions_sis.py` (#37). M1 est vérifiée à la lecture (schéma inattendu = arrêt).

### Calendrier : jours fériés et vacances scolaires (Q3)

| Id | Dimension | Règle | Seuil | Si ca casse |
|---|---|---|---|---|
| C1 | unicité | une ligne par jour et par département dans `calendrier.csv` | 0 doublon | bloquant |
| C2 | complétude (temps) | chaque jour de la période a une ligne pour les 10 départements du Grand Est | 100% | bloquant |
| C3 | cohérence | le 26 décembre (et le Vendredi saint) est férié dans le 57, le 67 et le 68 : sinon on a pris le fichier `metropole` pour l'Alsace-Moselle | 100% | bloquant |
| C4 | complétude (cellule) | vacances inconnues avant la rentrée 2017 (le fichier ne commence qu'en 2017-2018 pour Strasbourg, Nancy-Metz et Reims) | info | « non renseigné », jamais « non » |

Les dates du calendrier scolaire sont en UTC : converties en heure de Paris, une période va du jour de début (inclus) au jour de reprise (exclu). On garde les lignes « Élèves » ou « - ». Codées dans `src/nettoyage/calendrier.py`. N1 à N4, N8 et N9 sont codées dans `src/nettoyage/firms.py` (#37). FIRMS est **optionnel** : il faut une clé personnelle pour le télécharger. Sans les fichiers, le nettoyage prévient et continue, et les colonnes satellite restent vides (pas 0). La récupération note jusqu'à quel jour elle a téléchargé (`couverture_firms_*.csv`) : après ce jour, pas de détection = inconnu, pas 0.

### BD Forêt

| Id | Dimension | Règle | Seuil | Si ca casse |
|---|---|---|---|---|
| D1 | validité | géométries valides, en Lambert 93 (EPSG:2154). Les contours qui se croisent eux-mêmes sont réparés (`make_valid`) et comptés : 264 dans le Grand Est, dont 262 dans le 88 | 100% après réparation | bloquant |
| D2 | unicité | `ID` unique dans chaque département | 0 doublon | bloquant |
| D3 | actualité | on garde le millésime des photos par département (2007 pour le 67) a coté de chaque surface. `foret_commune.csv` garde l'édition IGN du fichier (2014 à 2022 selon le département) | - | info : on le dit dans chaque résultat |
| D4 | cohérence | la forêt d'une commune ne dépasse pas sa surface. Chaque fichier départemental déborde chez le voisin : il n'est découpé que sur les communes de son département, sinon la forêt des frontières compte 2 fois | 100% | bloquant |
| D5 | complétude (population) | une ligne par commune du Grand Est (5 115), même sans forêt (surface 0, part de résineux vide) | exact | bloquant |

Forêt = les types « Forêt … » et les peupleraies (pas les landes ni les formations herbacées). Part de résineux = (conifères + 0,5 × mixte) ÷ forêt avec couvert arboré (`part_resineux`). La version sans la forêt mixte (`part_resineux_stricte`) est gardée en test de sensibilité. Dans le 67 : 38,7 % avec la mixte à moitié, 27,8 % sans (voir le journal du 20/11, proposition à valider avant le calage de H3). Codées dans `src/nettoyage/bd_foret.py` (#37).

### NASA FIRMS (détections satellite, #36)

Une ligne FIRMS = un pixel chaud vu par un satellite a un passage, pas un départ de feu. Détail dans la [fiche](../sources/fiche-nasa-firms.md).

| Id | Dimension | Règle | Seuil | Si ca casse |
|---|---|---|---|---|
| N1 | validité | `acq_date` + `acq_time` sont en UTC : conversion en heure de Paris avant toute jointure (un passage a 22 h 30 UTC l'été tombe le lendemain) | 100% | bloquant |
| N2 | validité | colonnes harmonisées entre MODIS et VIIRS avant de fusionner (`confidence` de 0 a 100 d'un coté, `l` / `n` / `h` de l'autre ; `brightness` / `bright_ti4`) | 100% | bloquant |
| N3 | exactitude | on enlève les sources fixes : `type = 2` dans les fichiers SP, et les cases d'environ 1 km vues 10 jours ou plus dans l'année (usines : Héming, Neuves-Maisons, Couvrot...). Les 10 jours sont un choix du groupe, pris dans la fiche, comme le seuil des 3 feux | 0 restante | alerte : on compte ce qui a été enlevé dans le rapport |
| N4 | unicité | un feu donne plusieurs lignes (pixels voisins, plusieurs satellites, plusieurs passages) : on regroupe en commune x jour avant de compter | 1 ligne par commune x jour | bloquant |
| N5 | cohérence | une détection n'est jamais comptée comme un départ de feu de la BDIFF. Elle sert d'indicateur pour 2026 et de contrôle des années vides, pas au calage de H3 | - | règle de transformation (colonne a part, `detection_satellite`) |
| N6 | actualité | on note la version (NRT ou SP) et la date de téléchargement : les données NRT sont remplacées par la version SP 3 a 4 mois plus tard | - | info : un fichier NRT est retéléchargé quand la version SP sort |
| N7 | complétude (population) | le satellite ne voit pas tout (nuages, petit feu, pas de passage) : pas de détection ne veut pas dire pas de feu (ex : Haguenau le 13/08/2026) | - | info : jamais « 0 feu » a partir de FIRMS seul |
| N8 | cohérence | l'API se demande sur un rectangle qui déborde sur la Belgique, le Luxembourg, l'Allemagne et la Suisse : chaque point est rattaché a une commune du Grand Est (COG 2026), sinon il est enlevé. En 2026 : 3 041 points gardés sur 8 783 | 100% des points gardés dans une commune du Grand Est | alerte : on compte les points enlevés dans le rapport |
| N9 | unicité | une seule version par jour et par satellite : la SP si elle existe, sinon la NRT. Sans ca, garder les 2 fichiers pour la même période compte la même détection 2 fois (va avec N6) | 0 doublon jour x satellite x version | bloquant |

### Tables de travail (jointures)

Quand on croise les tables propres, rien ne doit se perdre ni se doubler. Codées dans `src/nettoyage/tables.py` (#37).

| Id | Dimension | Règle | Seuil | Si ca casse |
|---|---|---|---|---|
| T1 | unicité | une ligne par jour et par département dans `jour_departement.csv` | 0 doublon | bloquant |
| T2 | complétude (population) | autant de lignes que dans `calendrier.csv` | exact | bloquant |
| T3 | cohérence | total des feux de la table = feux de `feux.csv` hors doublons probables | exact | bloquant |
| T4 | cohérence | « 0 feu » seulement les années renseignées dans la BDIFF (P1). Année vide ou 2026 (pas encore publiée) : vide | 0 | bloquant |
| T5 | cohérence | pas de niveau de danger avant les archives de la Météo des forêts (juin 2024), ni hors saison publiée (P2) | 0 | bloquant |
| T6 | complétude (population) | chaque feu de `feux_travail.csv` a son type de jour (date et département connus du calendrier) | 100% | bloquant |

## 3. Le piège : un feu absent n'est pas un zéro

Compter les cases vides ne suffit pas : une ligne qui manque ne se voit pas (complétude de la population). Chez nous :

- la BDIFF a des années entieres sans aucun feu (2009 partout ; dans le 67, 12 années sur 20 : 2006, 2009, 2010, 2012 a 2019, 2021, cf règle P1 et [rapport-qualite.md](rapport-qualite.md)), alors que les interventions des SIS comptent des centaines de feux de végétation par an dans le 67. On pense que c'est de la sous-saisie, pas une absence de feux
- règle P1 : une année ou un département sans aucun feu dans la BDIFF est marqué **"non renseigné"**, et pas "0 feu", si les interventions SIS ou une autre source montrent de l'activité cette année-la. Ces années sont exclues des taux (feux par niveau, feux par an)
- la cause vide (B9) n'est sans doute pas un manque au hasard : elle dépend du département et de l'année (saisie inégale). Donc on ne peut pas calculer "la part de feux de malveillance" sur les 13% connus et l'appliquer au reste. On donne le chiffre sur les feux connus, en le disant
- règle P2 : les feux hors saison Météo des forêts (43% des feux) ne comptent ni comme "faible" ni comme "jour sans danger" : ils n'ont pas de niveau, point

## 4. Données personnelles (RGPD)

### Ce qu'on a, source par source

| Source | Données personnelles ? | Pourquoi |
|---|---|---|
| BDIFF | indirectes | pas de nom ni d'adresse, mais commune + date + heure + cause "Malveillance" peut renvoyer a une affaire connue dans une petite commune. 19 feux de malveillance dans le Grand Est, répartis sur 16 communes : le plus souvent c'est le seul de la commune dans l'année, donc facile a relier a un fait divers. Une colonne "bâtiments détruits" (1 cas) permet aussi de retrouver un propriétaire |
| Météo des forêts, Copernicus, BD Forêt, COG, comptes OFGL | non | météo, territoires, budgets |
| Interventions SIS (open data) | non | totaux par département et par an |
| Interventions du SDIS 67 (a demander, #41) | oui si on prend tout | une intervention une par une peut contenir adresse, victimes (= données de santé, catégorie particulière, art. 9) |
| NASA FIRMS (#36) | indirectes | coordonnées précises d'un point chaud : peut tomber sur une propriété privée |

La cause "Malveillance" c'est une infraction présumée. Tant qu'elle n'est liée a personne c'est pas une donnée personnelle, mais si on la croise avec une commune et une date précises on s'en rapproche (art. 10 : données sur les infractions). D'ou les règles ci-dessous.

### Ce qu'on fait

- **finalité** : les données servent uniquement a évaluer le seuil du dispositif renforcé pour le SDIS 67. Rien d'autre
- **minimisation** : on ne garde que les colonnes qui répondent a une question de l'[analyse globale](../analyse/analyse-globale.md). Pour la BDIFF on jette `Nom de la commune` (on a le code), les colonnes décès / bâtiments détruits, et les colonnes de surface pas comparables. Pas de champ gardé "au cas ou"
- **grain** : on descend jamais plus bas que commune x jour. L'heure sert seulement a vérifier l'ordre des événements, elle ne sort pas du pipeline
- **restitution** (tableaux, graphes, rendu au SDIS) :
  - les causes sont données par département ou par an, jamais "commune + date + malveillance"
  - pas de case avec moins de 3 feux quand on croise cause et commune (choix du groupe, a valider avec la prof)
  - les points FIRMS sont rattachés a la commune ou a la maille, pas affichés en points sur une carte
- **pseudonymiser c'est pas anonymiser** : remplacer un code commune par un numéro ne suffit pas si on garde la date et la cause a coté. On agrège plutot que de masquer
- **demande au SDIS 67 (#41)** : on demande seulement les interventions feux de végétation 2020-2026 avec date, commune et surface. Pas de centre engagé ni d'heures d'alerte / d'arrivée : ca servait aux questions mises de côté (casernes, délais), aucune de Q1 a Q5 n'en a besoin. Les causes seulement par année et par type, sans commune (suffit pour Q2). Pas d'adresse, pas de nom, rien sur les victimes. On écrit dans la demande qu'on supprime les fichiers apres la soutenance du 11/12
- **stockage** : `data/raw/` et `data/processed/` ne sont pas versionnés (pas sur GitHub). Les fichiers du SDIS restent sur nos postes, pas dans un drive partagé

### Secrets

- les clés d'API (Copernicus, FIRMS) vont dans `.env`, ignoré par git. Le dépôt contient seulement un `.env.example` sans valeur (#38)
- avant chaque PR : vérifier qu'aucune clé ni fichier de données ne part dans le commit (`git status`, jamais de `git add .`)

### Licences

Pas du RGPD mais c'est de la conformité aussi :

- Licence Ouverte 2.0 (Météo des forêts, interventions SIS, COG, BD Forêt, OFGL) : citer la source et la date
- CC-BY 4.0 (Copernicus) : citer avec le DOI `10.24381/cds.0e89c522`
- NASA FIRMS : données sans restriction d'usage (politique Earthdata), mais la NASA demande de citer la source avec le DOI du produit (par ex. `10.5067/FIRMS/MODIS/MCD14DL.NRT.0061` pour MODIS NRT) et la date de téléchargement
- BDIFF : data.gouv dit Licence Ouverte mais les mentions légales du site interdisent l'usage commercial et la modification. Pour un projet école c'est ok, mais on cite le site et on demande a la prof. Si le SDIS veut réutiliser notre travail, il faudra trancher

## 5. A faire

- [ ] écrire les règles en tests dans le pipeline : fait pour la BDIFF (#49), en cours pour le COG et le nettoyage des feux (#65, #66). Reste la Météo des forêts, Copernicus et FIRMS
- [x] premier rapport de qualité sur la BDIFF ([rapport](rapport-qualite.md), #49)
- [ ] rapport de qualité sur la Météo des forêts
- [ ] valider avec la prof : seuil des 3 feux, licence BDIFF
- [x] ajouter les règles FIRMS (N1 a N7 dans #49, N8 et N9 ensuite)
- [ ] relire la demande au SDIS (#41) avec la partie 4 avant envoi
