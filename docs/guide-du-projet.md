# Guide du projet

À lire en premier, ou à donner à quelqu'un qui arrive. État au 20/11/2026. Si une ligne n'est plus vraie, on la corrige dans une PR.

## 1. Le projet en bref

Le SDIS 67 (les pompiers du Bas-Rhin) prépare la saison des feux de forêt 2027. Il doit trancher deux points :

1. où concentrer ses moyens (humains et financiers) contre les départs de feu ;
2. à partir de quel niveau de la Météo des forêts lancer le dispositif renforcé (patrouilles, guet).

Le seuil actuel se trompe dans les deux sens : des alertes sans feu, et des feux les jours où l'indice est bas. Le budget ne permet pas de renforcer partout tout l'été. Le SDIS veut aussi comparer le Bas-Rhin au reste du Grand Est et à la France.

- Région : Grand Est, 10 départements (08, 10, 51, 52, 54, 55, 57, 67, 68, 88)
- Rendu au SDIS : vendredi 11 décembre
- Ce qu'on livre à la fin : un entrepôt de données (pipeline + modèle en étoile testé), des KPI, une réponse argumentée au SDIS

Le cours a deux UE avec la même prof (Marine Prost) :

| UE | Sujet | Où on écrit |
|---|---|---|
| UE01.A, Modélisation et pipeline | sources, qualité, entrepôt | `docs/`, `src/`, `tests/` |
| UE01.B, Définir des KPIs | diagnostic, objectifs SMART, indicateurs | `kpi/` |

## 2. Qui fait quoi

| Membre | GitHub | Rôle | Ce qu'il peut prendre maintenant |
|---|---|---|---|
| Lawson Robert | @lawsonboevirobert-boop | chef de projet + sources | demande au SDIS (#41) ; objectifs chiffrés (#40) ; relire les PR des sources (#34) |
| Denis Wilson-Bahun | @wilsonDenis | qualité et conformité (RGPD) | règles en tests pour chaque nouvelle source du nettoyage ; conventions et modèles d'issue et de PR (#4, PR #68) ; sa fiche indicateur |
| Franck Kevin Tambou | @FranckTambou | pipeline et modèle | la table commune → maille (#62), qui débloque le FWI par commune ; le modèle en étoile (pas encore d'issue) ; sa partie A de l'exo 3 et sa fiche indicateur manquent |
| Firas (firas.ja) | @firasjaouahdoups3-glitch | renfort pipeline, depuis le 18/11 | le nettoyage (#37) : COG et BDIFF faits (#65, #66), puis Météo des forêts, Copernicus, calendrier ; plan dans #58 |

Pour tout le monde, maintenant : son objectif et sa fiche indicateur dans `kpi/` (voir 7). C'est noté individuellement, donc chacun écrit et commite le sien.

Le responsable d'un domaine relit les PR de ce domaine. Un changement de rôle va dans le journal des décisions.

## 3. Comment on travaille

- 1 issue = 1 branche = 1 PR relue par quelqu'un d'autre. On ne pousse jamais sur `main`. Le détail est dans `CONTRIBUTING.md` (#68)
- nom de branche : `type/numéro-sujet`, par ex. `docs/50-guide-projet`, `feat/38-recuperation`, `test/48-tests-qualite-bdiff`
- commits petits, qui disent ce qu'ils font : `docs(sources): ajouter la fiche BDIFF (#24)`. La prof attend une centaine de commits au total, et une partie de la note RNCP vient de git (commits, branches, relectures)
- le tableau GitHub Projects suit les issues : à faire → en cours → en review → fait
- toute décision (choix d'une source, d'un seuil, d'une période) va dans `docs/decisions.md`, avec la raison et ce qu'on a écarté
- toute donnée de l'entrepôt a une fiche d'identité dans `docs/sources/`
- les données ne vont pas sur GitHub : `data/raw/` et `data/processed/` sont ignorés. La clé Copernicus va dans un `.env` (jamais commité)
- la prof préfère des rendus perso « moches », en listes, à des textes trop rédigés

Démarrer sur sa machine :

```
python3.13 -m venv .venv && source .venv/bin/activate      # Windows : voir le README
python -m pip install -r requirements.txt
python -m src.recuperation            # télécharge les données brutes dans data/raw/
python -m src.qualite                 # profil + règles de qualité sur la BDIFF (#49)
python -m src.nettoyage               # tables propres dans data/processed/ (#65, #66)
python -m src.etoile                  # modèle en étoile dans data/processed/etoile/ (#76)
python -m unittest discover -s tests -t .
```

## 4. Nos questions et hypothèses

Détail dans `docs/analyse/analyse-globale.md`.

| | Question | Hypothèse | Chiffrée ? |
|---|---|---|---|
| Q1 / H1 | Où et quand partent les feux dans le 67 ? | ils se concentrent sur une minorité de communes ou massifs | non |
| Q2 / H2 | Quelle part des feux a une cause humaine ? | une partie a une cause humaine | non |
| Q3 / H3 | Le type de jour, l'historique du secteur et la part de résineux aident-ils à prévoir les départs, en plus de l'indice ? | une règle qui les combine avec l'indice couvre au moins 20 % de départs en plus, à jours de renfort égaux | oui |
| Q4 / H4 | Pour chaque seuil : jours de renfort, départs couverts, fausses alertes, feux manqués, coût ? | le budget ne couvre qu'une partie des jours à risque | non, il faut les chiffres du SDIS |
| Q5 / H5 | L'indice se comporte-t-il dans le 67 comme ailleurs ? | le bon seuil n'est pas le même d'un département à l'autre | non |

H3 a été refaite le 18/11 après le retour de la prof : une hypothèse doit proposer mieux que l'indice, avec des variables qui ne sont pas dans son calcul (l'indice n'utilise que la météo).

## 5. Les sources

| Source | Ce qu'il y a | Sert à | Limite principale | Fiche |
|---|---|---|---|---|
| BDIFF | la liste des feux depuis 2006 : commune, date, surface, cause | Q1 à Q5 | années vides (2009 partout ; dans le 67, 12 années sur 20 sans feu), cause remplie à 13 % | `fiche-bdiff.md` |
| COG (INSEE) | les codes des communes 2026 et leurs changements | toutes les jointures | les codes changent avec les fusions de communes | `fiche-cog.md` |
| Météo des forêts | le niveau de danger du lendemain, par département | Q3, Q4, Q5 | 3 saisons seulement (2024 à 2026, de juin à septembre) | `fiche-meteo-des-forets.md` |
| Copernicus (FWI) | l'indice météo feu, par jour, sur une grille de 0,25° | refaire l'historique de l'indice (Q3, Q4) | grille et pas commune : il faut une table commune → maille ; mises à jour arrêtées depuis le 16/11 | `fiche-copernicus-indices-danger.md` |
| BD Forêt (IGN) | les forêts et leurs essences, par polygone | part de résineux (Q3), surface de forêt (Q1, Q5) | photos de 2007 pour le 67 | `fiche-bd-foret.md` |
| Interventions des SIS | nb d'interventions feux de végétation par département et par an | Q5, et vérifier les années vides de la BDIFF | totaux seulement, pas de détail feux de végétation de 2010 à 2013 | `fiche-interventions-sis.md` |
| Jours fériés | les fériés, zone Alsace-Moselle pour le 67 | type de jour (Q3) | rien de bloquant | `fiche-jours-feries.md` |
| Calendrier scolaire | les vacances par académie | type de jour (Q3) | commence en 2017-2018 | `fiche-calendrier-scolaire.md` |

Aussi : NASA FIRMS (feux vus par satellite en 2026, `fiche-nasa-firms.md`), les comptes des SDIS par l'OFGL (budget, `fiche-comptes-sdis.md`). À venir : les données demandées au SDIS 67 (#41 : coût d'un jour de renfort, budget, seuil actuel, interventions 2020-2026).

La matrice questions × sources est dans `docs/sources/matrice.md` (#47), l'inventaire dans `docs/sources/inventaire.md` (#30).

## 6. Ce qui manque

Données :
- le coût d'un jour de renfort, le budget et le seuil actuel du SDIS 67 : sans eux, H4 et la partie coût de Q4 ne se chiffrent pas. Réponse visée le 28/11
- la cause de 87 % des feux : on ne donne la part des causes que sur les feux connus, par département
- les années vides de la BDIFF : marquées « non renseigné », jamais « 0 feu »
- le calcul exact des niveaux de la Météo des forêts : un PDF de Météo-France, dans les fichiers du défi, à lire
- l'indice n'existe que de juin à septembre, alors que 43 % des feux tombent hors saison (221 en mars-avril). Chaque KPI doit dire s'il porte sur la saison ou sur l'année

Travail :
- `kpi/` : seule la fiche de Firas est faite (#60, #69). Le seuil et son KPI sont expliqués dans `docs/analyse/seuil-et-kpi.md` (#56), la fiche de H3 reste à écrire
- le nettoyage (#37) : COG et BDIFF faits, les autres sources à venir
- la table commune → maille (#62) bloque le FWI par commune
- le modèle en étoile n'est pas commencé et n'a pas d'issue
- l'exo 3 partie A manque pour Franck

À trancher en groupe :
- la date d'un feu : on prend la date de première alerte. 24 feux sur 736 sont signalés entre 23h et 1h, ils peuvent changer de type de jour (limite de H3)
- les années de calage et de test sont proposées dans le journal (#56) : FWI seul calé sur 2006-2016 et testé sur 2017-2025, H3 calée sur 2017-2022 et testée sur 2023-2025, sur tout le Grand Est. Attention : 2 départements sur 10 ont des feux en 2017 et 2018, et les Vosges font 323 des 615 feux de 2017-2025
- qui porte quel objectif en individuel dans `kpi/` (Firas a pris Q1)

À demander à la prof :
- les dates des rendus intermédiaires, et des séances S3 et S4 de l'UE01.B
- le PDF de l'UE01.B parle du SDIS 29 (Finistère) : on reste bien sur le 67 ?
- le nom du fichier `kpi/` de la séance 1, et la « spécification » citée en séance 2
- le « script fourni » pour le profil de la séance qualité (on a pris la BDIFF)

## 7. Calendrier et livrables

| Date | Séance | Livrable | État |
|---|---|---|---|
| lun 16/11 | lancement, la commande | analyse individuelle (exo 1), analyse globale | fait |
| mar 17/11 | les sources | fiches d'identité, inventaire (exo 2) ; matrice et journal (exo 3) | fait, sauf la partie A de l'exo 3 de Franck |
| mer 18/11 | qualité | profil, 3 règles en tests, rapport de qualité | fait (#49, #67) |
| jeu 19/11 | UE01.B séances 1 et 2 | diagnostic + objectifs SMART, puis `kpi/02_fiches_indicateurs.md` | en cours : fiche de Firas faite |
| fin de semaine | | premier squelette du pipeline + tests (V1) | récupération et qualité sur `main`, nettoyage en cours (#65, #66) |
| ? | UE01.B S3, FOAD, S4 | plan de mesure, jeu d'indicateurs v1, classement + ROI | dates inconnues |
| mar 8/12 | UE01.A S4 | | |
| mer 9/12 | UE01.A S5 + FOAD 2 | modèle en étoile historisé et testé | pas commencé |
| jeu 10/12 | UE01.A S6 | finalisation | |
| ven 11/12 | | réponse au SDIS | |

UE01.B, ce que chacun doit rendre dans `kpi/` :
1. en binôme, le diagnostic : stratégie, enjeu, objectif, action, chacun marqué établi ou supposé, plus une hypothèse stratégique et son verdict
2. seul, son objectif en 3 versions (une action, un objectif, un objectif SMART avec sa valeur de départ, « à mesurer » si on ne l'a pas). Un commit à son nom
3. en groupe, 3 à 5 objectifs retenus
4. seul, la fiche de son indicateur : formule, paramètres, source et champs, lignes utilisables, proxy et biais, décision éclairée, propriétaire, jugement RACER, garde-fou, risque résiduel, pre-mortem
5. en groupe, le jeu d'indicateurs v0 : KPI principal, secondaires, garde-fous, contexte, écartés

## 8. Où trouver quoi

| Fichier | Contenu |
|---|---|
| `README.md` | la commande, l'équipe, l'installation |
| `docs/analyse/` | les analyses individuelles et l'analyse globale (Q1-Q5, H1-H5) |
| `docs/sources/` | une fiche par source, l'inventaire, la matrice |
| `docs/qualite/regles.md` | les règles de qualité et le RGPD |
| `docs/qualite/rapport-qualite.md` | ce que nos chiffres peuvent affirmer ou pas (#49) |
| `docs/decisions.md` | le journal des décisions |
| `docs/glossaire.md` | les définitions complètes |
| `docs/organisation/repartition-taches.md` | la répartition des tickets |
| `src/recuperation/` | télécharger les données (#45) |
| `src/qualite/` | profil, règles, barrière de qualité (#49) |
| `src/nettoyage/` | tables propres dans `data/processed/` (#65, #66) |
| `src/etoile/` | faits et dimensions du modèle en étoile, règles E1 à E5 (#76) |
| `docs/pipeline/plan-nettoyage.md` | ce que produit le nettoyage, source par source (#58) |
| `docs/analyse/seuil-et-kpi.md` | le seuil et le KPI de H3 expliqués (#56) |
| `kpi/` | objectifs et indicateurs de l'UE01.B |
| `CONTRIBUTING.md` | comment on travaille sur le dépôt (#68) |

## 9. Sigles et mots

Les définitions complètes sont dans `docs/glossaire.md`.

| Sigle ou mot | Sens |
|---|---|
| SDIS | service départemental d'incendie et de secours (les pompiers d'un département) |
| SIS | service d'incendie et de secours, nom générique dans les stats nationales |
| CIS | centre d'incendie et de secours, une caserne |
| Dispositif renforcé | patrouilles et guet déclenchés quand le danger est jugé élevé |
| Météo des forêts | carte de danger feu de Météo-France, par département, pour le lendemain (J+1) |
| IFM / FWI | indice forêt météo, version française du Fire Weather Index canadien. Calculé avec température, humidité, vent, pluie |
| Seuil | le niveau d'indice à partir duquel on lance le renfort |
| Départ de feu | un feu enregistré dans la BDIFF, daté de sa première alerte |
| Départ couvert | un départ qui tombe un jour où le renfort était lancé |
| Fausse alerte | un jour de renfort sans aucun départ |
| BDIFF | base de données des incendies de forêt en France |
| COG | code officiel géographique (codes des communes, INSEE) |
| INSEE / IGN | institut des statistiques / institut de la géographie |
| Copernicus, CEMS, EWDS | programme européen d'observation ; son service d'urgence ; le site où on télécharge le FWI |
| EFFIS | système européen d'information sur les feux de forêt |
| NASA FIRMS | feux détectés par satellite, en quasi temps réel |
| OFGL | observatoire des finances locales (comptes des collectivités et des SDIS) |
| DFCI | défense des forêts contre l'incendie (pistes, points d'eau, grille de 2 km) |
| Maille | une case de la grille Copernicus (0,25°, environ 28 × 18 km ici) |
| Millésime / fraîcheur | l'année du référentiel / la date des données. Une fiche récente peut décrire des données anciennes |
| Grain | ce que représente une ligne (un feu, un jour × un département...) |
| RGPD | règlement sur les données personnelles. Chez nous : jamais plus fin que commune × jour, pas de cause par commune |
| Les 6 dimensions de qualité | complétude, exactitude, cohérence, validité, unicité, actualité |
| Barrière de qualité | un test bloquant en échec arrête le chargement |
| Couches brute / nettoyée / métier | `data/raw` tel quel, `data/processed` nettoyé, tables prêtes pour la décision |
| Modèle en étoile | une table de faits (les feux, les jours) entourée de tables de dimensions (date, commune, niveau...) |
| SMART | objectif spécifique, mesurable, atteignable, réaliste, temporel |
| KPI | indicateur clé suivi parce qu'il est lié à un objectif et peut changer une décision |
| RACER | critères d'un bon indicateur : relevant (lié à l'objectif), accepted, credible, easy, robust |
| Proxy | une donnée disponible qui remplace celle qu'on voudrait (avec son biais) |
| Garde-fou | un chiffre posé à côté d'un KPI pour voir s'il est détourné |
| Pre-mortem | imaginer que l'indicateur a échoué dans un an, et pourquoi |
| UE, FOAD, RNCP | unité d'enseignement ; séance à distance ; le titre visé (la note regarde aussi git) |
| PR | pull request : une demande de fusion relue avant d'entrer dans `main` |
