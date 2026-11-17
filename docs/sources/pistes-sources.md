# Pistes de sources

Liste de travail des sources qui peuvent répondre aux questions de l'[analyse globale](../analyse/analyse-globale.md). Elle sert à se répartir les sources pour l'exercice 2. L'inventaire demandé par la consigne (`docs/sources/inventaire.md`) sera fait en groupe après l'écriture des fiches.
Chaque source explorée aura sa fiche selon le [modèle](modele-fiche.md).

Point de départ fourni : le défi data.gouv.fr [« Prévenir et détecter les feux de forêt »](https://defis.data.gouv.fr/defis/prevenir-et-detecter-les-feux-de-foret) (porté par Pyronear et Latitudes), qui liste 39 sources. Seules celles qui servent nos questions sont reprises ici ; les autres sont listées en fin de document.

Priorité : **1** = indispensable pour répondre à la commande, **2** = utile, **3** = complément.
Accès : **ouvert** (open data), **sur demande**, **interne SDIS**, **à vérifier**.

## Vue d'ensemble

| # | Source | Producteur | Contenu | Grain | Période | Fraîcheur | Emprise | Accès | Questions | Priorité |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | BDIFF | Ministère de l'Agriculture, opérée par l'IGN | Liste des incendies de forêt : date, commune, surface brûlée, cause (selon les cas) | 1 feu | depuis 2006 | Annuelle | France | ouvert (export depuis le site) | Q1, Q2, Q3, Q5 | 1 |
| S2 | Archives de la Météo des forêts | Météo-France | Niveau de danger prévu pour J+1 (`niveau_j1`) et J+2 (`niveau_j2`), de 1 (faible) à 4 (très élevé). Un CSV par année. | 1 bulletin quotidien × 1 département (vérifié) | saisons 2024, 2025, 2026 ; publication de début juin à fin septembre | Quotidienne en saison | France métropolitaine (96 départements) | ouvert, Licence Ouverte 2.0 | Q3, Q4, Q5 | 1 |
| S3 | Indices de danger historiques CEMS (dont FWI) | Copernicus / ECMWF | Indice canadien (FWI, base de l'IFM) recalculé sur l'historique météo ERA5 | 1 jour × 1 maille (à vérifier) | plusieurs décennies (début exact à vérifier) | Mise à jour régulière | Monde | ouvert (compte Copernicus) | Q3, Q4, Q5 | 1 |
| S4 | IFM / FWI horaire | Météo-France | IFM officiel, horaire | 1 heure × 1 maille | à vérifier | à vérifier | France et voisinage | jeu annoncé sur data.gouv.fr, pas encore disponible | Q3, Q4 | 2 |
| S5 | Interventions du SDIS 67 | SDIS 67 | Interventions feux de végétation : centre engagé, heures d'alerte et d'arrivée, moyens | 1 intervention | à demander (idéalement 2020-2026) | non communiquée | Bas-Rhin | interne SDIS | Q1 (et questions mises de côté) | 1 |
| S6 | Coût du dispositif renforcé et budget 2027 | SDIS 67 | Coût d'un jour de renfort par secteur, enveloppe disponible, seuil actuel | 1 jour-secteur / 1 valeur | 2026-2027 | non communiquée | Bas-Rhin | interne SDIS | Q4 | 1 |
| S7 | Centres d'incendie et de secours | SDIS 67 (à défaut, données ouvertes à rechercher) | Localisation et effectifs des CIS | 1 centre | 2026 | Annuelle | Bas-Rhin | à vérifier | questions mises de côté | 2 |
| S8 | BD Forêt | IGN | Cartographie des formations végétales forestières | 1 polygone | dernier millésime | Pluriannuelle | France | ouvert | Q1, Q5 | 2 |
| S9 | CORINE Land Cover | Copernicus / Agence européenne pour l'environnement | Occupation du sol | 1 polygone | millésimes successifs (dernier : 2018) | Environ tous les 6 ans | Europe | ouvert | Q1, Q5 | 3 |
| S10 | EFFIS | Commission européenne (Copernicus) | Surfaces brûlées cartographiées par satellite, indices de danger | 1 feu cartographié / 1 maille | depuis les années 2000 (à vérifier) | Quotidienne | Europe | ouvert | Q5 | 3 |
| S11 | Code officiel géographique (COG) | INSEE | Codes et noms des communes, départements, régions, historique des fusions | 1 commune | 1 millésime par an | Annuelle | France | ouvert | toutes (jointures) | 1 |
| S12 | Données climatologiques | Météo-France (meteo.data.gouv.fr) | Vent, température, précipitations par station | 1 jour × 1 station | plusieurs décennies | Quotidienne | France | ouvert | Q3 (H2 : vent fort) | 3 |
| S13 | Jours fériés | État (data.gouv.fr) | Calendrier des jours fériés | 1 jour | plusieurs années | Annuelle | France | ouvert | Q1, Q3 (H2) | 3 |
| S14 | Interventions réalisées par les services d'incendie et de secours | Ministère de l'Intérieur (DGSCGC) | Nombre d'interventions par famille, dont « Feux de végétations » ; catégorie du SDIS | 1 année × 1 département (vérifié) | 2008 à 2024 | Annuelle | France (99 services) | ouvert, Licence Ouverte | Q5 | 2 |
| S15 | Météo des forêts (API) | Météo-France | Bulletin du jour, mêmes niveaux que S2 | 1 jour × 1 département | saison en cours | Quotidienne | France | ouvert (compte sur le portail API) | suivi 2027 | 3 |
| S16 | NASA FIRMS | NASA | Points chauds détectés par satellite (MODIS, VIIRS) | 1 détection | depuis 2000 (MODIS) | Quasi temps réel | Monde | ouvert | Q1, Q5 (contrôle de la BDIFF) | 3 |
| S17 | Carroyage DFCI 2 km | DFCI (data.gouv.fr) | Grille officielle de 2 km utilisée par les acteurs de la lutte | 1 carreau de 2 km | 2016 | Figée | France métropolitaine | ouvert, Licence Ouverte | Q1, Q4 (grain « secteur ») | 2 |
| S18 | Obligations légales de débroussaillement | Géorisques | Zones soumises à l'obligation de débroussaillement | 1 zone | en vigueur | à vérifier | France | ouvert | Q1, Q2 | 3 |
| S19 | GASPAR | Ministère de la Transition écologique | Procédures risques par commune (dont plans de prévention incendie de forêt) | 1 procédure × 1 commune | en vigueur | Régulière | France | ouvert | Q1 | 3 |
| S20 | Admin Express | IGN | Contours des communes, départements, régions | 1 commune | depuis 2017 | Annuelle | France | ouvert | toutes (cartes, jointures) | 1 |
| S21 | OCS-GE | IGN | Occupation du sol à grande échelle | 1 polygone | selon les départements | Pluriannuelle | France (déploiement progressif) | ouvert | Q1 (interface habitat-forêt) | 3 |
| S22 | Liste des festivals en France | Ministère de la Culture | Festivals avec lieu et période | 1 festival | en vigueur | Annuelle | France | ouvert | Q1, Q3 (H2 : activité humaine) | 3 |

## Points d'attention

- **Premier constat sur S2 (saison 2025).** Dans le Bas-Rhin, le niveau prévu pour J+1 a été « faible » 115 jours et « modéré » 5 jours sur les 120 jours publiés ; jamais « élevé » ni « très élevé ». Avec la Météo des forêts seule, un seuil à « élevé » n'aurait donc jamais déclenché le dispositif en 2025. C'est à confronter aux feux de la BDIFF et à vérifier sur 2024 et 2026.
- **Saison de publication.** La Météo des forêts n'est publiée que de début juin à fin septembre. Les feux de mars à mai et d'octobre n'ont pas de niveau officiel : il faudra l'IFM ou le FWI (S3) pour ces mois.
- **S14 n'est pas une liste d'interventions.** C'est un total annuel par département : utile pour comparer les départements (Q5), pas pour les questions au jour près. Les données détaillées restent à demander au SDIS 67 (S5).
- **Historique de la Météo des forêts plus court que prévu.** Les archives publiques commencent le 3 juin 2024, soit 3 saisons (2024 à 2026), et non 4. La saison 2023 est à demander à Météo-France. Cela renforce le choix de reconstituer l'historique à partir du FWI de Copernicus (S3) : voir le [journal des décisions](../decisions.md).
- **IFM et FWI.** L'IFM de Météo-France est adapté de l'indice canadien (FWI). Les valeurs Copernicus (S3) ne sont donc pas strictement identiques à l'IFM officiel : il faudra vérifier leur concordance sur les saisons où les deux existent (2024-2026).
- **Grain spatial.** La Météo des forêts est publiée par département ; le FWI Copernicus est sur une grille. Un seuil par secteur dans le Bas-Rhin suppose d'utiliser la grille.
- **Données internes SDIS (S5, S6, S7).** Elles conditionnent la question Q4 et les questions mises de côté. Une demande doit être envoyée au SDIS 67 au plus vite.
- **Prométhée** (base des feux de la zone méditerranéenne) ne couvre pas le Grand Est : écartée.

## À faire

- [x] Vérifier le découpage des archives de la Météo des forêts (1 jour × 1 département, niveaux 1 à 4).
- [ ] Ouvrir les autres sources de priorité 1 et vérifier les champs réellement disponibles (notamment la cause dans la BDIFF).
- [ ] Écrire les fiches de l'exercice 2 (une ou deux sources chacun, sans doublon entre nous).
- [ ] Faire l'inventaire de groupe `docs/sources/inventaire.md` au format de la consigne.
- [ ] Préparer la demande de données au SDIS 67 (S5, S6, S7).
- [ ] Alimenter la matrice questions × sources (#8).

## Liens

- BDIFF : <https://bdiff.agriculture.gouv.fr>
- Archives de la Météo des forêts : <https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets>
- IFM / FWI horaire : <https://www.data.gouv.fr/datasets/indice-ifm-fwi-horaire-pour-la-france-et-voisinage>
- Indices de danger historiques CEMS : <https://ewds.climate.copernicus.eu/datasets/cems-fire-historical-v1>
- Météo des forêts (présentation) : <https://www.feuxdeforet.fr/moyens-de-lutte/surveillance-et-prevention/meteo-des-forets/>
- Météo des forêts (API) : <https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesMeteoForets>
- Interventions des SIS : <https://www.data.gouv.fr/datasets/interventions-realisees-par-les-services-d-incendie-et-de-secours/>
- NASA FIRMS : <https://firms.modaps.eosdis.nasa.gov/>
- Carroyage DFCI : <https://www.data.gouv.fr/datasets/carroyage-dfci-2-km/>
- Obligations légales de débroussaillement : <https://www.georisques.gouv.fr/donnees/bases-de-donnees/obligations-legales-de-debroussaillement>

## Sources du défi non retenues pour l'instant

Images de départs de feux (Pyronear), modèles météo AROME et ARPEGE (prévisions brutes, trop lourdes pour notre besoin), données de changement climatique, statistiques nationales des SDIS, stratégie nationale et plans départementaux de protection (PDPFCI, PPRIF : à lire comme contexte), BD TOPO, BD ORTHO, MNS LiDAR HD, forêts publiques, parcelles agricoles, réserves biologiques, artificialisation des sols, données naturalistes de l'ONF, Geofla, OpenStreetMap, EuroGlobalMap, Sentinel 1A, trafic routier, ROUTE 500.
