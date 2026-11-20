# Fiche source : Comptes des SDIS 2012-2025 (OFGL)

Explorée par : FranckTambou, le 2026-11-19
Lien : https://www.data.gouv.fr/datasets/comptes-des-sdis-2012-2025
Fichier ouvert : `ofgl-base-sdis.csv` (84 420 lignes)

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | Créateur et éditeur : OFGL. Calcul à partir des balances comptables des SDIS publiées par la DGFiP |
| Mode d'accès (export, API, téléchargement) et format | Téléchargement direct. CSV, séparateur point-virgule, UTF-8 avec BOM. Un JSON existe aussi, non comparé ligne à ligne |
| Grain (une ligne = ?) | Un agrégat financier, pour un budget, pour un exercice |
| Emprise géographique | France. Grand Est : 10 départements, 8 509 lignes |
| Période réellement couverte par les données | Exercices 2012 à 2025 dans le fichier (la page indiquait 2012-2023 dans une version antérieure) |
| Date de dernière mise à jour affichée sur la fiche | À vérifier : 20 juillet 2026 relevé sur la page ; 13/08/2026 donné par l'API (relevé de Denis) |
| Fréquence de mise à jour | Non vérifiée : pas indiquée sur la page data.gouv.fr |
| Volumétrie | 84 420 lignes, 21 colonnes ; 8 509 lignes pour le Grand Est |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | `Code Département` (sur deux caractères), `Exercice`, `Siren SDIS`, `SIRET Budget`, `Libellé Budget`, `CBUDG` (type de budget) |
| Données personnelles | Aucune : agrégats par établissement public, sans personne physique |
| Licence | Licence Ouverte 2.0 (vérifiée sur data.gouv.fr, API `lov2`) |
| Questions de l'analyse auxquelles elle pourrait répondre | Q4 (coût du SDIS), en partie seulement : budget de tout le SDIS, pas le coût d'un jour de renfort. Q5 pour comparer les départements. Pas de feux ni de forêt dans cette source |

## Contrôles qualité repérés

- Doublons : aucun sur la clé exercice + SIRET budget + agrégat (contrôlé par Denis).
- Dates : tous les exercices sont dans la période 2012-2025.
- Codes géographiques : 98 SIREN pour 97 départements, à expliquer avant jointure.
- Budgets annexes : `CBUDG = 3` (œuvres sociales, production d'énergie, cantines selon les départements) à exclure des totaux départementaux. Pour le budget principal, filtrer sur `CBUDG = 1` plutôt que sur le libellé.
- Libellé : le budget principal du Bas-Rhin et du Haut-Rhin s'appelle « SDIS » jusqu'en 2023, puis « SIS » en 2024-2025.
- Rupture de nomenclature : M61 → M57. Pour le Bas-Rhin, le passage se fait en 2024 ; pour les autres départements du Grand Est, il se fait entre 2022 et 2024 selon le département (Meuse 2022, Aube et Marne 2023, les autres 2024). Le saut de 83,4 M€ (2022) à 95,7 M€ (2023) n'est pas dû au M57 : cause non vérifiée.
- Valeurs manquantes : non vérifiée.

## Ce qu'on retient

Source utile pour Q4 et Q5 : elle donne le budget de l'ensemble de chaque SDIS et permet de comparer les départements. Elle ne donne ni le détail par centre ni le coût d'un jour de renfort. Surprise : les ruptures de nomenclature entre 2022 et 2024 changent les totaux d'une année à l'autre.