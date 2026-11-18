# Fiche source : jours fériés (API calendrier.api.gouv.fr)

Explorée par : @wilsonDenis, le 2026-11-18
Lien : https://calendrier.api.gouv.fr/jours-feries/ (fiche data.gouv : https://www.data.gouv.fr/datasets/jours-feries-en-france)
Fichier ouvert : `alsace-moselle.json` et `metropole.json` (appel direct de l'API, sans compte)

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | Etalab (DINUM), API publique de l'État |
| Mode d'accès (export, API, téléchargement) et format | API sans compte : `https://calendrier.api.gouv.fr/jours-feries/<zone>.json`. JSON très simple : `{"2025-05-01": "1er mai", ...}`. Il y a une zone `alsace-moselle` a part |
| Grain (une ligne = ?) | 1 jour férié (date + nom) |
| Emprise géographique | France, par zone (métropole, Alsace-Moselle, outre-mer). Pour nous : zone `alsace-moselle` pour le 67, le 68 et le 57, zone `metropole` pour les 7 autres départements du Grand Est |
| Période réellement couverte par les données | de 2006 a 2031 dans le fichier (337 jours en Alsace-Moselle) |
| Date de dernière mise à jour affichée sur la fiche | non vérifiée : pas de date dans le JSON et je n'ai pas trouvé de date sur la page de l'API |
| Fréquence de mise à jour | pas besoin : les jours fériés sont calculés a l'avance (fichier jusqu'en 2031) |
| Volumétrie | 337 dates en Alsace-Moselle, 285 en métropole, 10 Ko. 130 jours fériés en Alsace-Moselle de 2016 a 2025 |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | la date -> se joint a la date d'un feu (BDIFF) ou a la date d'un bulletin. Choisir la zone selon le département |
| Données personnelles | aucune |
| Licence | Licence Ouverte 2.0 (data.gouv) |
| Questions de l'analyse auxquelles elle pourrait répondre | Q3 : le type de jour (férié ou pas) est une des 3 variables qu'on ajoute a l'indice |

## Contrôles qualité repérés

- Doublons : aucune date en double
- Dates : toutes au format AAAA-MM-JJ, de 2006 a 2031
- Codes géographiques : pas de code, juste la zone. A nous de dire quel département va dans quelle zone
- Valeurs manquantes : aucune

## Ce qu'on retient

- Petit, propre, rien a nettoyer
- Ce qui m'a surpris : l'Alsace-Moselle a 2 jours fériés de plus que le reste de la France (Vendredi saint et 26 décembre). Si on prend le fichier "métropole" pour le Bas-Rhin, on rate ces 2 jours chaque année. Le Vendredi saint tombe en mars-avril, en plein dans la période ou partent beaucoup de feux
