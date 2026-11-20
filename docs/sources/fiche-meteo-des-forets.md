# Fiche source : Archives de la Météo des forêts

Explorée par : @lawsonboevirobert-boop, le 2026-11-17
Lien : <https://www.data.gouv.fr/datasets/archives-de-la-meteo-des-forets>
Fichiers ouverts : `mdf_2024.csv.gz`, `mdf_2025.csv.gz`, `mdf_2026.csv.gz` (en entier), et le PDF de présentation de Météo-France

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | Météo-France. Les archives sont publiées sur data.gouv.fr par le compte Météo-France ; les fichiers CSV sont hébergés sur l'espace de stockage de Météo-France (`meteofrance.s3.sbg.io.cloud.ovh.net`). Le niveau publié vient de l'« indice de danger intégré » de Météo-France (IFM, état de sécheresse de la végétation, zones sensibles), revu par les prévisionnistes. |
| Mode d'accès (export, API, téléchargement) et format | Téléchargement direct, sans compte : un CSV compressé (`.csv.gz`) par année, encodé en UTF-8. La fiche propose aussi un GeoJSON des départements, un ZIP d'échantillons et un PDF de présentation. Une API existe pour le bulletin du jour (portail API de Météo-France) : non vérifiée, nous ne l'avons pas testée. |
| Grain (une ligne = ?) | Un bulletin pour un département : la date et l'heure de diffusion (`date`, en UTC), le numéro et le nom du département, et deux niveaux de danger notés de 1 à 4 : `niveau_j1` pour le lendemain, `niveau_j2` pour le surlendemain. La documentation décrit une échelle à 4 niveaux (faible, modéré, élevé, très élevé) ; la correspondance exacte entre chiffre et libellé n'y est pas écrite, mais l'ordre 1 à 4 est le seul cohérent. |
| Emprise géographique | France métropolitaine : 96 départements, Corse comprise (2A et 2B). Pas d'outre-mer. |
| Période réellement couverte par les données | 2024 : du 3 juin au 30 septembre (120 jours). 2025 : du 3 juin au 30 septembre (120 jours). 2026 : du 28 mai au 5 octobre (131 jours). Rien avant 2024, alors que le dispositif existe depuis 2023. Rien d'octobre à mai. |
| Date de dernière mise à jour affichée sur la fiche | 5 octobre 2026 (fichier `mdf.2026`). Les fichiers 2024 et 2025 ont été mis à jour les 24 et 25 juin 2026. |
| Fréquence de mise à jour | Quotidienne pendant la saison, d'après la fiche. Le fichier de l'année en cours grandit d'une ligne par département et par jour de diffusion. |
| Volumétrie | 11 520 lignes en 2024, 11 520 en 2025, 12 576 en 2026, soit 35 616 lignes. Moins de 50 Ko par fichier compressé. |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | Le numéro de département (`num_dep`) et la date. Pour joindre avec les feux, il faut prendre la date de diffusion plus un jour pour `niveau_j1`. Attention, le code département n'a pas le même format selon l'année : `1`, `2`… en 2024 et 2025, `01`, `02`… en 2026. |
| Données personnelles | Aucune : uniquement des niveaux de danger par département. |
| Licence | Licence Ouverte 2.0 (Etalab), affichée sur la fiche. |
| Questions de l'analyse auxquelles elle pourrait répondre | Q3 (fiabilité de l'indice dans le Bas-Rhin), Q4 (jours de renfort selon le seuil) et Q5 (comparaison avec le Grand Est et la France), une fois croisée avec la liste des feux de la BDIFF. |

## Contrôles qualité repérés

- Doublons : aucun couple jour × département en double sur les trois années.
- Dates : aucun jour manquant dans les périodes indiquées, et chaque jour a bien ses 96 départements.
- Codes géographiques : format différent entre 2024-2025 et 2026 (voir les clés). Les noms de colonne changent aussi : `nom_dep` en 2024 et 2026, `dep_nom` en 2025.
- Format : séparateur virgule en 2024 et 2025, point-virgule en 2026. Un chargement automatique doit gérer les deux.
- Valeurs manquantes : aucune.
- Heure de diffusion : 16:00 UTC en 2024, vers 14:50 UTC en 2025 et 2026, alors que la documentation annonce une diffusion à 17 h (heure de Paris).

## Ce qu'on retient

La source est propre et facile à charger, mais courte : trois saisons, et seulement de juin à septembre. Dans le Bas-Rhin, le niveau prévu pour le lendemain a été faible tous les jours en 2024, faible 115 jours et modéré 5 jours en 2025, puis faible 76 jours, modéré 49 jours et élevé 6 jours en 2026. Il n'a jamais été très élevé. Pour couvrir dix ans et les mois de printemps, il faudra un autre indice ; comme le niveau publié intègre la sécheresse de la végétation et l'avis des prévisionnistes, un IFM brut converti en niveaux ne donnera pas exactement les mêmes valeurs.
