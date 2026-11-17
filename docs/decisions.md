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

## 2026-11-17 - Historique de l'indice : passer par l'IFM

- **Décision :** pour étudier le seuil sur une dizaine d'années, nous reconstituerons l'historique du danger à partir des valeurs de l'IFM, converties en niveaux, en plus des niveaux officiels de la Météo des forêts.
- **Raison :** la Météo des forêts n'est publiée que depuis juin 2023 et ses archives publiques ne commencent que le 3 juin 2024, soit 3 saisons seulement (2024 à 2026). C'est trop court pour juger un seuil de façon fiable. L'historique sera reconstitué avec l'indice canadien (FWI) recalculé par Copernicus.
- **Alternatives écartées :** se limiter aux 3 saisons officielles disponibles (trop peu de jours avec feu dans le Bas-Rhin pour conclure) ; attendre que Météo-France publie l'IFM historique (jeu annoncé, pas encore disponible).
- **Décidé par :** le groupe, lors de la fusion des analyses.
- **Liens :** [analyse globale, section 6](analyse/analyse-globale.md#6-points-dattention), #7

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
