# Feux de forêt - Grand Est

Projet de groupe HETIC 2026/2027, EU01 « Modélisation et pipeline de données ».

**Région : Grand Est** (10 départements : Ardennes, Aube, Marne, Haute-Marne, Meurthe-et-Moselle, Meuse, Moselle, Bas-Rhin, Haut-Rhin, Vosges).

## La commande

La direction du SDIS 67 (Bas-Rhin) prépare la saison feux 2027 et doit arbitrer deux points :

1. **où concentrer ses moyens**, humains comme financiers, pour lutter contre les départs de feu ;
2. **à partir de quel niveau de la Météo des forêts** déclencher le dispositif renforcé (patrouilles, guet).

Elle veut savoir comment l'indice se comporte dans le Bas-Rhin, dans les autres départements du Grand Est et au niveau national.
Réponse attendue le **11 décembre**.

## Équipe et rôles

| Membre | GitHub | Rôle | Responsable de |
|---|---|---|---|
| Lawson Robert | [@lawsonboevirobert-boop](https://github.com/lawsonboevirobert-boop) | Chef de projet + responsable sources | Dépôt, tickets, checkpoints, journal des décisions ; inventaire, fiches d'identité, matrice questions × sources |
| Denis Wilson-Bahun | [@wilsonDenis](https://github.com/wilsonDenis) | Responsable qualité et conformité | Règles de qualité, tests, données personnelles |
| Franck Kevin Tambou | [@FranckTambou](https://github.com/FranckTambou) | Responsable pipeline et modèle | Chargement, consolidation, entrepôt |

Groupe de trois : le chef de projet prend aussi la responsabilité des sources.
Un rôle ne limite pas le travail de chacun : le responsable d'un domaine relit et valide les tickets qui en relèvent.
Tout changement de rôle est consigné dans le [journal des décisions](docs/decisions.md).

## Organisation

- Les tâches sont suivies dans les [issues](../../issues), réparties dans [docs/organisation/repartition-taches.md](docs/organisation/repartition-taches.md).
- Une issue = une branche (`type/numero-sujet`, par exemple `docs/7-inventaire-sources`) = une pull request relue par un autre membre.
- La branche `main` est protégée : on n'y pousse pas directement.

## Documents

| Document | Contenu |
|---|---|
| [Analyse globale](docs/analyse/analyse-globale.md) | Questions, hypothèses, besoins et données idéales du groupe |
| [Analyses individuelles](docs/analyse/) | Analyse de la commande de chaque membre (partie B) |
| [Glossaire](docs/glossaire.md) | Termes de la commande et des analyses |
| [Journal des décisions](docs/decisions.md) | Choix du groupe, avec date et justification |
| [Inventaire des sources](docs/sources/inventaire.md) | Sources de données envisagées |
