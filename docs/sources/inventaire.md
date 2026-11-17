# Inventaire des sources

Premier inventaire des sources envisagées pour répondre aux questions de l'[analyse globale](../analyse/analyse-globale.md).
Chaque source retenue fera l'objet d'une fiche d'identité selon le [modèle](modele-fiche.md).

Priorité : **1** = indispensable pour répondre à la commande, **2** = utile, **3** = complément.
Accès : **ouvert** (open data), **sur demande**, **interne SDIS**, **à vérifier**.

## Vue d'ensemble

| # | Source | Producteur | Contenu | Grain | Période | Fraîcheur | Emprise | Accès | Questions | Priorité |
|---|---|---|---|---|---|---|---|---|---|---|
| S1 | BDIFF | Ministère de l'Agriculture, opérée par l'IGN | Liste des incendies de forêt : date, commune, surface brûlée, cause (selon les cas) | 1 feu | depuis 2006 | Annuelle | France | ouvert (export depuis le site) | A1, A2, A3, B1-B3, C1, C2 | 1 |
| S2 | Archives de la Météo des forêts | Météo-France | Niveaux de danger publiés chaque jour | 1 jour × 1 zone (à vérifier) | depuis le 3 juin 2024 | Quotidienne | France métropolitaine | ouvert (data.gouv.fr) | B1-B3, C1, C2 | 1 |
| S3 | Indices de danger historiques CEMS (dont FWI) | Copernicus / ECMWF | Indice canadien (FWI, base de l'IFM) recalculé sur l'historique météo ERA5 | 1 jour × 1 maille (à vérifier) | plusieurs décennies (début exact à vérifier) | Mise à jour régulière | Monde | ouvert (compte Copernicus) | B1-B3, C1, C2 | 1 |
| S4 | IFM / FWI horaire | Météo-France | IFM officiel, horaire | 1 heure × 1 maille | à vérifier | à vérifier | France et voisinage | jeu annoncé sur data.gouv.fr, pas encore disponible | B1-B3 | 2 |
| S5 | Interventions du SDIS 67 | SDIS 67 | Interventions feux de végétation : centre engagé, heures d'alerte et d'arrivée, moyens | 1 intervention | à demander (idéalement 2020-2026) | — | Bas-Rhin | interne SDIS | A1, A4, B2 | 1 |
| S6 | Coût du dispositif renforcé et budget 2027 | SDIS 67 | Coût d'un jour de renfort par secteur, enveloppe disponible, seuil actuel | 1 jour-secteur / 1 valeur | 2026-2027 | — | Bas-Rhin | interne SDIS | A5, B3 | 1 |
| S7 | Centres d'incendie et de secours | SDIS 67 (à défaut, données ouvertes à rechercher) | Localisation et effectifs des CIS | 1 centre | 2026 | Annuelle | Bas-Rhin | à vérifier | A4 | 2 |
| S8 | BD Forêt | IGN | Cartographie des formations végétales forestières | 1 polygone | dernier millésime | Pluriannuelle | France | ouvert | A1, C2 | 2 |
| S9 | CORINE Land Cover | Copernicus / Agence européenne pour l'environnement | Occupation du sol | 1 polygone | millésimes successifs (dernier : 2018) | Environ tous les 6 ans | Europe | ouvert | A1, C2 | 3 |
| S10 | EFFIS | Commission européenne (Copernicus) | Surfaces brûlées cartographiées par satellite, indices de danger | 1 feu cartographié / 1 maille | depuis les années 2000 (à vérifier) | Quotidienne | Europe | ouvert | C2 | 3 |
| S11 | Code officiel géographique (COG) | INSEE | Codes et noms des communes, départements, régions, historique des fusions | 1 commune | 1 millésime par an | Annuelle | France | ouvert | toutes (jointures) | 1 |
| S12 | Données climatologiques | Météo-France (meteo.data.gouv.fr) | Vent, température, précipitations par station | 1 jour × 1 station | plusieurs décennies | Quotidienne | France | ouvert | B2 (H3 : vent fort) | 3 |
| S13 | Jours fériés | État (data.gouv.fr) | Calendrier des jours fériés | 1 jour | plusieurs années | Annuelle | France | ouvert | A2, B2 (H3) | 3 |

## Points d'attention

- **Historique de la Météo des forêts plus court que prévu.** Les archives publiques commencent le 3 juin 2024, soit 3 saisons (2024 à 2026), et non 4. La saison 2023 est à demander à Météo-France. Cela renforce le choix de reconstituer l'historique à partir du FWI de Copernicus (S3) : voir le [journal des décisions](../decisions.md).
- **IFM et FWI.** L'IFM de Météo-France est adapté de l'indice canadien (FWI). Les valeurs Copernicus (S3) ne sont donc pas strictement identiques à l'IFM officiel : il faudra vérifier leur concordance sur les saisons où les deux existent (2024-2026).
- **Grain spatial.** La Météo des forêts est publiée par département ; le FWI Copernicus est sur une grille. Un seuil par secteur dans le Bas-Rhin suppose d'utiliser la grille.
- **Données internes SDIS (S5, S6, S7).** Elles conditionnent les questions A4, A5 et B3. Une demande doit être envoyée au SDIS 67 au plus vite.
- **Prométhée** (base des feux de la zone méditerranéenne) ne couvre pas le Grand Est : écartée.

## À faire

- [ ] Ouvrir chaque source de priorité 1 et vérifier les champs réellement disponibles (notamment la cause dans la BDIFF et le découpage des archives de la Météo des forêts).
- [ ] Rédiger les fiches d'identité de S1, S2, S3 et S11.
- [ ] Préparer la demande de données au SDIS 67 (S5, S6, S7).
- [ ] Alimenter la matrice questions × sources (#8).

## Liens

- BDIFF : <https://bdiff.agriculture.gouv.fr>
- Archives de la Météo des forêts : <https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets>
- IFM / FWI horaire : <https://www.data.gouv.fr/datasets/indice-ifm-fwi-horaire-pour-la-france-et-voisinage>
- Indices de danger historiques CEMS : <https://ewds.climate.copernicus.eu/datasets/cems-fire-historical-v1>
- Météo des forêts (présentation) : <https://www.feuxdeforet.fr/moyens-de-lutte/surveillance-et-prevention/meteo-des-forets/>
