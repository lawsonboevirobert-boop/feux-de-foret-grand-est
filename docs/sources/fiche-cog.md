# Fiche source : Code officiel géographique (COG)

Explorée par : @wilsonDenis, le 2026-11-17
Lien : https://www.data.gouv.fr/datasets/code-officiel-geographique-1 (fichiers hébergés sur insee.fr)
Fichiers ouverts : `v_commune_2026.csv`, `v_mvt_commune_2026.csv`, `v_departement_2026.csv` (millésime 2026)

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | INSEE. data.gouv.fr ne fait que renvoyer vers les fichiers sur insee.fr |
| Mode d'accès (export, API, téléchargement) et format | téléchargement direct, un CSV par table (séparateur virgule, valeurs entre guillemets, UTF-8) |
| Grain (une ligne = ?) | `v_commune` : 1 commune (ou commune déléguée / associée / arrondissement de Paris Lyon Marseille). `v_mvt_commune` : 1 événement sur une commune (fusion, changement de nom...) |
| Emprise géographique | France (métropole + DOM). Les collectivités d'outre-mer sont dans des fichiers à part |
| Période réellement couverte par les données | `v_commune` : situation au 01/01/2026. `v_mvt_commune` : événements du 19/02/1943 au 01/01/2026 |
| Date de dernière mise à jour affichée sur la fiche | 07/11/2026 sur data.gouv.fr |
| Fréquence de mise à jour | annuelle (un millésime par an) |
| Volumétrie | `v_commune` : 37 496 lignes, 4,3 Mo. `v_mvt_commune` : 13 734 lignes, 2,3 Mo. `v_departement` : 101 lignes |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | `COM` (code commune INSEE, ex 67482 = Strasbourg), `DEP` (département), `REG` (région, 44 = Grand Est). Dans les mouvements : `COM_AV` (ancien code) -> `COM_AP` (nouveau code) |
| Données personnelles | non, que des codes et noms de territoires |
| Licence | Licence Ouverte (code fr-lo sur data.gouv.fr) |
| Questions de l'analyse auxquelles elle pourrait répondre | aucune directement. Elle sert a relier les sources pour toutes les questions (Q1 a Q5) : rattacher un feu de la BDIFF a son département et sa région, et comparer le 67 au Grand Est et a la France (Q5) |

## Contrôles qualité repérés

- Doublons : 584 codes apparaissent plusieurs fois dans `v_commune`, parce qu'une commune déléguée garde le meme code que sa commune nouvelle. En gardant seulement `TYPECOM = COM` il n'y a plus de doublon (34 875 communes, 34 875 codes)
- Dates : `v_mvt_commune` va de 1943 a 2026, rien en dehors
- Codes géographiques : depuis 2006 il y a environ 150 mouvements avec changement de code dans le Grand Est, dont 20 dans le Bas-Rhin (ex Ringeldorf, Uberach et La Walck -> Val-de-Moder). Un feu de la BDIFF enregistré avec un ancien code ne trouvera pas sa commune dans le COG 2026 -> il faudra passer par `v_mvt_commune` pour convertir les anciens codes
- Valeurs manquantes : `ARR` vide 17 fois, `CAN` 56 fois, `COMPARENT` toujours vide pour les communes (normal, il sert que pour les communes déléguées). Rien de vide sur `COM`, `DEP`, `REG`

## Ce qu'on retient

- Indispensable pour les jointures, pas pour répondre aux questions. Grand Est = 5 115 communes au 01/01/2026, dont 514 dans le Bas-Rhin
- Ce qui m'a surpris : les doublons de codes a cause des communes déléguées, et le nombre de changements de codes depuis 2006. Faut choisir un millésime pour tout le projet (je propose 2026) et convertir les codes de la BDIFF avant de joindre
