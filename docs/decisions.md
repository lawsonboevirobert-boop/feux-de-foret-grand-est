# Journal des décisions

Chaque décision du groupe est consignée ici, la plus récente en haut.
Tout changement de rôle doit y figurer.

Modèle d'entrée :

```
## AAAA-MM-JJ - Titre court
- Décision :
- Raison :
- Alternatives écartées :
- Décidé par :
- Liens : (issues, PR, documents)
```

---
## 2026-11-19 - Choix du pipeline de nettoyage (réponses à Firas)

- **Décision :** les tables de travail sont en CSV, pas en Parquet (tables petites, pas de dépendance en plus). La table commune → maille est prise par Franck, avec le centre de la commune comme point de rattachement. Le FWI moyen d'un département est la moyenne sur ses communes, chaque commune comptée une fois, avec la valeur de sa maille. Les jours fériés, le calendrier scolaire et FIRMS sont ajoutés au script de récupération dans #37.
- **Raison :** tables petites, une seule maille par commune (règle F4 de regles.md), calcul simple et reproductible.
- **Alternatives écartées :** Parquet (ajoute pyarrow sans gain pour ce volume) ; maille couvrant le plus de surface (calcul géographique plus lourd) ; moyenne des mailles dont le centre est dans le département (ne suit pas la logique commune).
- **Décidé par :** Franck Kevin TAMBOU, en réponse au plan de Firas (#58).
- **Liens :** #37, #58, #59
- **Reste ouvert :** fuseau horaire de la date de première alerte BDIFF (à vérifier sur la documentation du site).

## 2026-11-18 - Arrivée d'un quatrième membre et nouvelle répartition

- **Décision :** Firas (firas.ja, @firasjaouahdoups3-glitch) rejoint le groupe en renfort sur le pipeline. Il prend le nettoyage et la consolidation (#37), fait son analyse individuelle de la commande (#35) et une fiche source, NASA FIRMS (#36). Lawson reste chef de projet et responsable sources, et reprend la matrice questions × sources (#8), qui relève des sources.
- **Changement de rôle :** l'environnement Python (#5) et les scripts de récupération (#38), prévus pour Franck, ont été faits par Lawson, qui avait déjà téléchargé et ouvert chaque source pour écrire les fiches. Franck n'a donc plus d'issue de pipeline en cours. Il garde la responsabilité pipeline et modèle (il relit #44, #45 et le nettoyage) et prend une nouvelle tâche, à choisir avec lui : la table commune → maille pour joindre le FWI de Copernicus aux feux, ou le modèle en étoile (rendu du 9/12).
- **Raison :** le pipeline est la partie la plus chargée pour la suite (récupérer, nettoyer, croiser cinq sources), alors que les sources sont déjà bien avancées. Les travaux individuels de Firas rendent sa contribution visible dans l'historique, comme pour les autres.
- **Alternatives écartées :** confier les sources à Firas pour séparer les rôles de chef de projet et de responsable sources. Il aurait dû reprendre un domaine presque terminé, pendant que le pipeline restait à une seule personne.
- **Décidé par :** le groupe.
- **Liens :** [README](../README.md), #5, #8, #35, #36, #37, #38, #44, #45

## 2026-11-18 - Q3 et H3 : chercher mieux que l'indice, pas prouver qu'il est mauvais

- **Décision :** Q3 ne mesure plus si l'indice est fiable. Elle cherche si trois variables hors météo aident à prévoir les départs de feu en plus de l'indice : le type de jour (week-end, férié, vacances scolaires), l'historique de départs du secteur et la part de résineux. H3 devient : la règle combinée couvre au moins 20 % de départs en plus que l'indice seul, à nombre de jours de renfort égal. Les fausses alertes, les feux manqués et leur gravité passent dans Q4.
- **Raison :** retour de la prof le 18/11 : l'ancienne H3 (« plus l'indice est élevé, plus il y a de feux, mais le lien est faible ») ne prouve rien, puisque le SDIS nous a déjà dit que l'indice déclenche mal. Il faut proposer mieux que l'indice, avec des variables qui ne sont pas dans son calcul (l'indice n'utilise que la température, l'humidité, le vent et la pluie). Les trois variables retenues expliquent des départs (les causes connues sont presque toutes humaines), le SDIS peut agir dessus (quand et où renforcer) et on a les données : BDIFF, BD Forêt, jours fériés, calendrier scolaire.
- **Comment on la teste :** règle calée sur 2017-2022 et vérifiée sur 2023-2025, sur les départements du Grand Est (le Bas-Rhin seul a trop d'années non renseignées dans la BDIFF, et le calendrier scolaire commence en 2017-2018). Le seuil de 20 % est fixé ici, avant tout calcul. On a déjà vu les chiffres de la saison 2025 dans le Bas-Rhin (6 feux sur 9 un jour « faible »), donc 2025 seule ne compte pas comme preuve.
- **Alternatives écartées :** garder l'ancienne H3 (ne prouve rien) ; ajouter le vent ou la sécheresse (déjà dans l'indice) ; l'interface habitat-forêt (demande les contours des communes et la population, plus long à construire, gardée en réserve).
- **Décidé par :** proposé par Denis après le retour de la prof, à valider par le groupe en relecture de la PR.
- **Liens :** [analyse globale](analyse/analyse-globale.md), [glossaire](glossaire.md), [fiche jours fériés](sources/fiche-jours-feries.md), [fiche calendrier scolaire](sources/fiche-calendrier-scolaire.md), #40

## 2026-11-17 - Réduire l'analyse globale à 5 questions

- **Décision :** l'analyse globale passe de 10 questions sur 3 axes à 5 questions (Q1 à Q5). Les questions sur l'éloignement des casernes et la charge par centre sont mises de côté.
- **Raison :** 10 questions, c'était trop pour le temps du projet, et plusieurs se recoupaient. Les 5 restantes couvrent les deux décisions demandées par le SDIS (où mettre les moyens, quel seuil) et la comparaison avec le Grand Est et la France. Les questions mises de côté demandent des données d'intervention détaillées que nous n'avons pas.
- **Décidé par :** le groupe.
- **Liens :** [analyse globale](analyse/analyse-globale.md)

## 2026-11-17 - Historique de l'indice : passer par l'IFM

- **Décision :** pour étudier le seuil sur une dizaine d'années, nous reconstituerons l'historique du danger à partir des valeurs de l'IFM, converties en niveaux, en plus des niveaux officiels de la Météo des forêts.
- **Raison :** la Météo des forêts n'est publiée que depuis juin 2023 et ses archives publiques ne commencent que le 3 juin 2024, soit 3 saisons seulement (2024 à 2026). C'est trop court pour juger un seuil de façon fiable. L'historique sera reconstitué avec l'indice canadien (FWI) recalculé par Copernicus.
- **Alternatives écartées :** se limiter aux 3 saisons officielles disponibles (trop peu de jours avec feu dans le Bas-Rhin pour conclure) ; attendre que Météo-France publie l'IFM historique (jeu annoncé, pas encore disponible).
- **Décidé par :** le groupe, lors de la fusion des analyses.
- **Liens :** [analyse globale, points d'attention](analyse/analyse-globale.md#points-dattention), #7

## 2026-11-17 - Une analyse globale à partir des trois analyses individuelles

- **Décision :** les trois analyses individuelles sont conservées telles quelles (partie B, travail individuel) et fusionnées dans une analyse globale qui sert de référence pour la suite du projet. Les questions sont regroupées en 3 axes : où concentrer les moyens (A), à quel niveau déclencher (B), comment le Bas-Rhin se situe (C).
- **Raison :** les trois analyses se recoupaient largement ; une seule liste de questions est nécessaire pour construire la matrice questions × sources et l'inventaire.
- **Décidé par :** le groupe.
- **Liens :** [analyse globale](analyse/analyse-globale.md), #11, #12, #13

## 2026-11-17 - Glossaire : trois statuts de définition

- **Décision :** chaque terme du glossaire porte un statut : « vérifié » (source officielle citée), « définition du groupe » (convention de calcul à faire valider par le SDIS) ou « à vérifier ».
- **Raison :** distinguer ce qui est établi de ce que nous fixons nous-mêmes, notamment fausse alerte, feu manqué et jour avec feu, qui conditionnent tous les calculs sur le seuil.
- **Décidé par :** le groupe.
- **Liens :** [glossaire](glossaire.md), #6

## 2026-11-16 - Environnement Python : version 3.13 et versions figées

- **Décision :** le projet utilise Python 3.13. numpy (2.3.5) et scikit-learn (1.7.2) sont figés dans `requirements.txt`.
- **Raison :** sur un poste Windows 11 avec le Contrôle intelligent des applications actif, les bibliothèques compilées pour Python 3.15 et les toutes dernières versions de numpy et scikit-learn sont bloquées. Les versions retenues fonctionnent.
- **Alternatives écartées :** désactiver le Contrôle intelligent des applications (irréversible sans réinstaller Windows).
- **Décidé par :** le groupe.
- **Liens :** #5

## 2026-11-16 - Organisation du travail

- **Décision :** une issue par tâche, une branche par issue (`type/numero-sujet`), une pull request relue par un autre membre avant fusion dans `main`. Les tâches de l'exercice 1 sont réparties dans les issues #1 à #13.
- **Raison :** rendre visible dans l'historique qui a fait quoi et quand, et garder `main` stable.
- **Décidé par :** le groupe.
- **Liens :** [répartition des tâches](organisation/repartition-taches.md)

## 2026-11-16 - Répartition des rôles

- **Décision :**

  | Membre | Rôle |
  |---|---|
  | Lawson Robert (@lawsonboevirobert-boop) | Chef de projet + responsable sources |
  | Denis Wilson-Bahun (@wilsonDenis) | Responsable qualité et conformité |
  | Franck Kevin Tambou (@FranckTambou) | Responsable pipeline et modèle |

- **Raison :** le groupe compte trois membres ; comme le prévoit la consigne, le chef de projet prend aussi la responsabilité des sources.
- **Décidé par :** le groupe.
- **Liens :** [README](../README.md), #2
