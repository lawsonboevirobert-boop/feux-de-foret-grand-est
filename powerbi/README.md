# Tableau de bord Power BI (UE01.C)

Le tableau de bord du SDIS 67, en projet Power BI (`.pbip`) : le modèle, les requêtes, les mesures et les 4 pages sont en fichiers texte, lisibles et relus dans git comme le reste du dépôt.

| Fichier | Contenu |
|---|---|
| `projet/TableauDeBord-SDIS67.pbip` | **le projet à ouvrir dans Power BI Desktop** |
| `projet/TableauDeBord-SDIS67.SemanticModel/` | le modèle : tables, colonnes, mesures, relations, requêtes Power Query (format TMDL) |
| `projet/TableauDeBord-SDIS67.Report/` | le rapport : les 4 pages et leurs visuels (format PBIR) |
| `fiche-cadrage.md` | la fiche de cadrage du guide, remplie : décideur, décision, 3 questions, KPI, sources |
| `requetes/`, `mesures.dax` | les mêmes requêtes et mesures en copie lisible, pour les relire ou les refaire à la main (parties 1 à 3) |
| `theme_hetic.json` | le thème aux couleurs HETIC |

## 0. Ouvrir le projet (le plus simple)

1. Avoir les données sur sa machine : `python -m src.recuperation` (BDIFF, COG, Météo des forêts dans `data/raw/`).
2. Ouvrir `projet/TableauDeBord-SDIS67.pbip` dans Power BI Desktop (version de 2026).
3. Accueil > Transformer les données > Modifier les paramètres : mettre dans `DossierProjet` le chemin du dépôt sur sa machine, avec le `\` à la fin.
4. Accueil > Actualiser. Si Power BI demande un niveau de confidentialité : « Organisationnel » pour tous les fichiers.
5. Enregistrer (Ctrl+S) : Power BI réécrit les fichiers du projet, on les commite sur une branche comme le reste.

À ne jamais commiter : le dossier `.pbi/` (il contient les données en cache, exclu par le `.gitignore`) et les fichiers `.pbix` (même raison). Ne pas commiter non plus son propre chemin dans `DossierProjet` si on n'a rien changé d'autre.

Les parties 1 à 4 ci-dessous expliquent comment le même tableau de bord se monte à la main : utile pour comprendre chaque étape, ou si le projet ne s'ouvre pas.

Le modèle : deux tables de faits (Incendies, MeteoForets) et cinq dimensions (Calendrier, Departements, Communes, Causes, et Seuil, qui n'est reliée à rien).

```
              Communes      Causes
                  \           /
   Calendrier --- Incendies --- Departements
        \                          /
         `------ MeteoForets -----'
```

## 1. Power Query : importer et nettoyer

1. Accueil > Transformer les données (Power Query s'ouvre).
2. Pour chaque fichier de `requetes/`, dans l'ordre :
   - Accueil > Nouvelle source > Requête vide
   - Accueil > Éditeur avancé, tout effacer, coller le contenu du fichier
   - renommer la requête (volet de gauche) avec le nom du fichier sans le numéro : `DossierProjet`, `BDIFF_propre`, `MDF_propre`, `Incendies`, `MeteoForets`, `Communes`, `Departements`, `Causes`, `Seuil`
3. Dans `DossierProjet`, vérifier le chemin du dépôt (avec le `\` à la fin).
4. Clic droit sur `BDIFF_propre` puis sur `MDF_propre` > décocher « Activer le chargement » (ce sont des étapes intermédiaires).
5. Si Power BI demande un niveau de confidentialité : « Organisationnel » pour tous les fichiers.
6. Fermer et appliquer.

## 2. Vue Modèle : relier les tables

1. Modélisation > Nouvelle table : coller la table `Calendrier` de `mesures.dax`.
2. Calendrier : Outils de table > Marquer comme table de dates > colonne `Date`. Colonne `Mois` : Trier par colonne > `N° Mois`.
3. Vue Modèle (3e icône à gauche). Créer ces relations, toutes en « un à plusieurs » (1 côté dimension), filtrage dans un seul sens :

| Dimension (1) | Faits (*) |
|---|---|
| `Calendrier[Date]` | `Incendies[Date]` |
| `Calendrier[Date]` | `MeteoForets[Date]` |
| `Departements[Code département]` | `Incendies[Code département]` |
| `Departements[Code département]` | `MeteoForets[Code département]` |
| `Communes[Code commune]` | `Incendies[Code commune]` |
| `Causes[Cause]` | `Incendies[Cause]` |

Ne pas relier `Communes` à `Departements`, ni `Seuil` à quoi que ce soit. Power BI crée parfois des relations tout seul : supprimer celles qui ne sont pas dans le tableau.

4. `Departements[Lieu]` : Outils de colonne > Catégorie de données > Département (ou Lieu). `Seuil[Niveau de déclenchement]` : Trier par colonne > `Niveau`.

## 3. Mesures DAX

Clic droit sur la table `Incendies` > Nouvelle mesure, puis coller chaque mesure de `mesures.dax`, une à la fois. Régler le format indiqué en commentaire (Outils de mesure).

## 4. Thème et pages

Affichage > Thèmes > Parcourir les thèmes > `theme_hetic.json`.

Sur chaque page : le titre donne le message, les segments sont à gauche, les cartes KPI en haut, le détail en bas (lecture en Z). Orange pour un seul élément à signaler.

### Page 1 · Synthèse (Où en est-on ?)

Titre : **735 feux saisis dans le Grand Est depuis 2006, dont la moitié dans les Vosges**

- segments : `Calendrier[Année]`, `Departements[Département]`, `Causes[Cause]`
- 4 cartes : `Nb feux` (sous-titre : `Évolution vs N-1`), `Surface brûlée (ha)`, `Surface moyenne (ha)`, `Part hors juin-septembre`
- histogramme : `Nb feux` par `Calendrier[Année]`. Les trous sont des années non renseignées : l'écrire dans le sous-titre du visuel
- carte : `Departements[Lieu]`, taille = `Nb feux`
- barres horizontales triées : `Nb feux` par `Departements[Département]`, le Bas-Rhin en orange

### Page 2 · Analyse (Pourquoi ?)

Titre : **43 % des feux partent hors de juin à septembre, quand la Météo des forêts n'est pas publiée**

- segments : année, département
- histogramme : `Nb feux` par `Calendrier[Mois]` (mars-avril en orange)
- barres : `Nb feux` par `Incendies[Niveau Météo des forêts]` (juin 2024 à 2025 seulement, le dire dans le sous-titre)
- barres triées : `Nb feux` par `Causes[Cause]`, avec la carte `Part cause connue` à côté (13 %)
- ne jamais mettre la cause dans un visuel par commune

### Page 3 · Décision (Que fait-on ?)

Titre : **Au niveau « modéré », 9 jours de renfort sur 10 n'ont eu aucun feu**

- segment : `Seuil[Niveau de déclenchement]` en sélection unique, plus le département
- 4 cartes : `Jours de renfort`, `Taux de départs couverts`, `Précision`, `Jours de renfort sans feu`
- tableau par `Departements[Département]` : `Jours de renfort`, `Feux couverts`, `Feux pendant la publication`, `Précision`
- carte : `Part dans les secteurs prioritaires` + tableau `Communes[Commune]` / `Nb feux` filtré sur le Bas-Rhin, mise en forme conditionnelle sur `Nb feux`

### Page 4 · Détail

Titre : **Le détail par commune et par année, pour vérifier un cas**

- tableau : `Communes[Commune]`, `Departements[Département]`, `Calendrier[Année]`, `Nb feux`, `Surface brûlée (ha)`, `Nb feux de 1 ha ou plus`
- segments : année, département. Pas de segment de cause sur cette page (règle sur les données personnelles)

### Disposition mobile

Affichage > Disposition mobile, page Synthèse : les 4 cartes en haut, puis l'histogramme par année et les barres par département.

## 5. Vérifier ses chiffres

Sans aucun filtre, le rapport doit afficher :

| Mesure | Grand Est | Bas-Rhin (67) |
|---|---|---|
| Nb feux | 735 | 83 |
| Surface brûlée (ha) | 1 579,9 | 49,2 |
| Surface moyenne (ha) | 2,15 | 0,59 |
| Nb feux de 1 ha ou plus | 204 | 22 |
| Part cause connue | 13,2 % | 15,7 % |
| Part hors juin-septembre | 43,5 % | 51,8 % |
| Années renseignées | 19 | 8 |

Page Décision, seuil « 2 - modéré » :

| Mesure | Grand Est | Bas-Rhin (67) |
|---|---|---|
| Feux pendant la publication | 46 | 8 |
| Feux couverts | 9 | 3 |
| Taux de départs couverts | 19,6 % | 37,5 % |
| Jours de renfort | 69 | 5 |
| Jours de renfort avec feu | 7 | 2 |
| Précision | 10,1 % | 40,0 % |

Seuil « 3 - élevé », Grand Est : 1 feu couvert sur 46, 2 jours de renfort. Part dans les secteurs prioritaires, Bas-Rhin, années 2024 et 2025 : 27 % (3 feux sur 11), comme dans la fiche de Firas.

Si un chiffre ne colle pas : vérifier d'abord les relations (page 17 du guide), puis le type des colonnes de date et de code.

## 6. Limites

- les jours de renfort sont comptés en jours x département
- le 67 n'a que 8 feux pendant la publication de la Météo des forêts : ses taux se jouent à un feu près
- le FWI de Copernicus (seuil sur toute l'année) n'est pas encore dans le rapport : il arrivera avec la table commune → maille (#62) et le modèle en étoile du pipeline (#76)
- le fichier `.pbix` contient les données (commune, date, cause) : il ne va pas sur GitHub, comme `data/`
