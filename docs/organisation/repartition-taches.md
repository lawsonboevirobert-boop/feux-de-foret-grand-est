# Répartition des tâches — Exercice 1

Groupe de 3. Rôles :

| Membre | Rôle | Responsable de |
|---|---|---|
| Membre 1 | Chef·fe de projet + sources | Dépôt, tickets, checkpoints, journal des décisions, inventaire, fiches d'identité, matrice questions × sources |
| Membre 2 | Qualité et conformité | Règles de qualité, tests, données personnelles |
| Membre 3 | Pipeline et modèle | Chargement, consolidation, entrepôt |

Le responsable d'un domaine relit et valide les tickets qui en relèvent, même s'il ne les a pas faits.
Chaque ticket = une branche (`type/numero-sujet`) + une pull request relue par une autre personne.

## Partie A — Dépôt (groupe)

| # | Ticket | Assigné | Relecteur | Livrable |
|---|---|---|---|---|
| 1 | Ajouter les membres comme collaborateurs et protéger `main` (PR obligatoire) | Membre 1 | — | Paramètres GitHub |
| 2 | Compléter le README : nom du projet, région Grand Est, tableau des rôles | Membre 1 | Membre 2 | `README.md` |
| 3 | Créer le journal des décisions et y consigner la répartition des rôles | Membre 1 | Membre 3 | `docs/decisions.md` |
| 4 | Ajouter les modèles d'issue et de PR, et les conventions de branches et de commits | Membre 2 | Membre 1 | `.github/`, `CONTRIBUTING.md` |
| 5 | Mettre en place l'environnement Python et la structure du dépôt (dossiers, `requirements.txt`, `.gitignore` des données, section « Installation » du README) | Membre 3 | Membre 2 | `requirements.txt`, `data/`, `src/`, `notebooks/` |
| 6 | Créer le glossaire du groupe (squelette, puis fusion des termes inconnus des 3 analyses) | Membre 2 | Membre 1 | `docs/glossaire.md` |
| 7 | Lancer l'inventaire des sources et le modèle de fiche d'identité (BDIFF, Météo des forêts, Prométhée, IGN BD Forêt, INSEE…) | Membre 1 | Membre 3 | `docs/sources/inventaire.md`, `docs/sources/modele-fiche.md` |
| 8 | Construire la matrice questions × sources à partir des questions des analyses individuelles | Membre 3 | Membre 1 | `docs/sources/matrice-questions-sources.md` |
| 9 | Rédiger les premières règles de qualité et le point données personnelles (localisation précise des feux, causes, RGPD) | Membre 2 | Membre 3 | `docs/qualite/regles.md` |
| 10 | Checkpoint 1 : relecture croisée des 3 analyses, mise à jour du glossaire et de la matrice | Membre 1 | Tous | Compte rendu dans `docs/decisions.md` |

## Partie B — Analyse de la commande (individuel)

Chacun écrit et committe **lui-même** son fichier, sur sa propre branche.

| # | Ticket | Assigné | Livrable |
|---|---|---|---|
| 11 | Analyse de la commande (questions, termes inconnus, besoins, données idéales) | Membre 1 | `docs/analyse/commande-prenom-nom.md` |
| 12 | Analyse de la commande (questions, termes inconnus, besoins, données idéales) | Membre 2 | `docs/analyse/commande-prenom-nom.md` |
| 13 | Analyse de la commande (questions, termes inconnus, besoins, données idéales) | Membre 3 | `docs/analyse/commande-prenom-nom.md` |

## Ordre conseillé

1. Ticket 1 (sans lui, personne ne peut pousser), puis 2 et 5 en parallèle.
2. Tickets 11, 12, 13 en parallèle : le commit individuel est obligatoire avant la fin de l'exercice.
3. Tickets 3, 4, 7, 9 en parallèle.
4. Tickets 6 et 8, qui dépendent des analyses individuelles, puis le checkpoint (10).

Charge : Membre 1 → 6 tickets (dont un de paramétrage rapide), Membre 2 → 4, Membre 3 → 4.
