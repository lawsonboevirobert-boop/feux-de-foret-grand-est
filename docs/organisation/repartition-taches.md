# Répartition des tâches — Exercice 1

Groupe de 3. Rôles :

| Membre | Rôle | Responsable de |
|---|---|---|
| @lawsonboevirobert-boop | Chef·fe de projet + sources | Dépôt, tickets, checkpoints, journal des décisions, inventaire, fiches d'identité, matrice questions × sources |
| @wilsonDenis | Qualité et conformité | Règles de qualité, tests, données personnelles |
| @FranckTambou | Pipeline et modèle | Chargement, consolidation, entrepôt |

Les tickets correspondent aux issues GitHub du même numéro.

Le responsable d'un domaine relit et valide les tickets qui en relèvent, même s'il ne les a pas faits.
Chaque ticket = une branche (`type/numero-sujet`) + une pull request relue par une autre personne.

## Partie A — Dépôt (groupe)

| # | Ticket | Assigné | Relecteur | Livrable |
|---|---|---|---|---|
| #1 | Ajouter les membres comme collaborateurs et protéger `main` (PR obligatoire) | @lawsonboevirobert-boop | @wilsonDenis | Paramètres GitHub |
| #2 | Compléter le README : nom du projet, région Grand Est, tableau des rôles | @lawsonboevirobert-boop | @wilsonDenis | `README.md` |
| #3 | Créer le journal des décisions et y consigner la répartition des rôles | @lawsonboevirobert-boop | @FranckTambou | `docs/decisions.md` |
| #4 | Ajouter les modèles d'issue et de PR, et les conventions de branches et de commits | @wilsonDenis | @lawsonboevirobert-boop | `.github/`, `CONTRIBUTING.md` |
| #5 | Mettre en place l'environnement Python et la structure du dépôt (dossiers, `requirements.txt`, `.gitignore` des données, section « Installation » du README) | @FranckTambou | @wilsonDenis | `requirements.txt`, `data/`, `src/`, `notebooks/` |
| #6 | Créer le glossaire du groupe (squelette, puis fusion des termes inconnus des 3 analyses) | @wilsonDenis | @lawsonboevirobert-boop | `docs/glossaire.md` |
| #7 | Lancer l'inventaire des sources et le modèle de fiche d'identité (BDIFF, Météo des forêts, Prométhée, IGN BD Forêt, INSEE…) | @lawsonboevirobert-boop | @FranckTambou | `docs/sources/inventaire.md`, `docs/sources/modele-fiche.md` |
| #8 | Construire la matrice questions × sources à partir des questions des analyses individuelles | @FranckTambou | @lawsonboevirobert-boop | `docs/sources/matrice-questions-sources.md` |
| #9 | Rédiger les premières règles de qualité et le point données personnelles (localisation précise des feux, causes, RGPD) | @wilsonDenis | @FranckTambou | `docs/qualite/regles.md` |
| #10 | Checkpoint 1 : relecture croisée des 3 analyses, mise à jour du glossaire et de la matrice | @lawsonboevirobert-boop | Tous | Compte rendu dans `docs/decisions.md` |

## Partie B — Analyse de la commande (individuel)

Chacun écrit et committe **lui-même** son fichier, sur sa propre branche.

| # | Ticket | Assigné | Livrable |
|---|---|---|---|
| #11 | Analyse de la commande (questions, termes inconnus, besoins, données idéales) | @lawsonboevirobert-boop | `docs/analyse/commande-prenom-nom.md` |
| #12 | Analyse de la commande (questions, termes inconnus, besoins, données idéales) | @wilsonDenis | `docs/analyse/commande-prenom-nom.md` |
| #13 | Analyse de la commande (questions, termes inconnus, besoins, données idéales) | @FranckTambou | `docs/analyse/commande-prenom-nom.md` |

# Exercice 2 : fiches d'identité des sources

Chacun prend deux sources, choisies d'après les 5 questions de l'[analyse globale](../analyse/analyse-globale.md), sans doublon entre nous. Les fiches suivent le [modèle](../sources/modele-fiche.md) : une fiche par commit, depuis son propre compte.

| # | Membre | Sources | Fichiers | Pourquoi ces sources |
|---|---|---|---|---|
| #23 | @lawsonboevirobert-boop | Archives de la Météo des forêts, BDIFF | `fiche-meteo-des-forets.md`, `fiche-bdiff.md` | Les niveaux de l'indice et la liste des feux : c'est la base de Q1 à Q5. |
| #24 | @wilsonDenis | Interventions des SIS, carroyage DFCI | `fiche-interventions-sis.md`, `fiche-carroyage-dfci.md` | Comparer les départements (Q5) et découper le Bas-Rhin en secteurs (Q1, Q4). |
| #25 | @FranckTambou | Indices de danger Copernicus, BD Forêt | `fiche-copernicus-indices-danger.md`, `fiche-bd-foret.md` | Reconstituer l'indice sur 10 ans (Q3, Q4) et connaître la surface forestière (Q1, Q5). |

Mise en commun (#26) : @wilsonDenis crée `docs/sources/inventaire.md` au format de la consigne une fois les six fiches fusionnées. La PR est relue par @lawsonboevirobert-boop, responsable sources.
