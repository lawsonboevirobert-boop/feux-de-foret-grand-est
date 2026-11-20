# Fiche source : NASA FIRMS (feux détectés par satellite)

Explorée par : @firasjaouahdoups3-glitch, le 2026-11-19
Lien : https://firms.modaps.eosdis.nasa.gov/ (API : https://firms.modaps.eosdis.nasa.gov/api/area/)
Fichier ouvert : appels de l'API `area/csv` sur un rectangle autour du Grand Est (`3.38,47.42,8.24,50.17`), du 01/01/2026 au 18/11/2026, pour les 4 satellites (MODIS, VIIRS S-NPP, NOAA-20, NOAA-21), soit 258 fichiers CSV. Plus le fichier public `MODIS_C6_1_Europe_7d.csv` (sans clé) pour voir le format.

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | NASA (système LANCE / Earthdata). Les points viennent de deux capteurs : MODIS (satellites Terra et Aqua) et VIIRS (satellites S-NPP, NOAA-20, NOAA-21) |
| Mode d'accès (export, API, téléchargement) et format | API avec une clé gratuite (MAP_KEY, reçue par e-mail) : `api/area/csv/<clé>/<source>/<rectangle>/<nb jours>/<date début>`. 5 jours maximum par appel, 5 000 appels par 10 minutes. CSV. Sans clé : seulement les fichiers des dernières 24 h, 48 h et 7 jours. La clé va dans `.env` (`FIRMS_MAP_KEY`), jamais dans le dépôt |
| Grain (une ligne = ?) | 1 pixel « chaud » vu par 1 satellite à 1 passage : position, date, heure (UTC), puissance du feu (`frp`), confiance. Pixel de 375 m en VIIRS, 1 km en MODIS. **Un feu donne plusieurs lignes** (plusieurs pixels, plusieurs satellites, plusieurs passages) |
| Emprise géographique | Monde. Le rectangle demandé déborde sur la Belgique, le Luxembourg, l'Allemagne et la Suisse : 8 783 lignes en tout, dont 3 041 dans une commune du Grand Est |
| Période réellement couverte par les données | MODIS depuis novembre 2000, VIIRS S-NPP depuis janvier 2012. Mon fichier : du 2026-01-01 au 2026-11-18. Deux versions : « SP », données retraitées, jusqu'au 31/07/2026 (VIIRS) et au 31/08/2026 (MODIS) ; « NRT », temps réel, après ces dates |
| Date de dernière mise à jour affichée sur la fiche | Le 19/11/2026, l'appel `data_availability` donne des données NRT jusqu'au 2026-11-19 (MODIS, NOAA-21) et au 2026-11-18 (NOAA-20). S-NPP s'arrête au 2026-11-02 : le fichier public VIIRS S-NPP des 7 derniers jours est vide |
| Fréquence de mise à jour | Quasi temps réel, plusieurs passages par jour. Les données NRT sont remplacées plus tard par la version SP (environ 3 à 4 mois de retard d'après les dates ci-dessus) |
| Volumétrie | 8 783 détections sur le rectangle en 2026, environ 0,7 Mo de CSV. 3 041 dans le Grand Est, 46 dans le Bas-Rhin |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | Pas de code commune. Latitude / longitude (WGS84) → commune en testant le point dans les contours des communes (j'ai pris geo.api.gouv.fr) ; → maille Copernicus par arrondi. Date : `acq_date` + `acq_time` sont en **UTC**. Un passage à 22 h 30 UTC tombe le lendemain en heure française l'été : il faut convertir avant de joindre à la BDIFF ou au niveau du jour |
| Données personnelles | Indirectes : la position est précise à 375 m et peut tomber sur une propriété privée (brûlage dans un jardin, une ferme). Règle déjà prévue dans [regles.md](../qualite/regles.md) : on rattache les points à la commune ou à la maille, pas de carte en points |
| Licence | Données de la NASA, sans restriction d'usage (politique Earthdata). La NASA demande de citer la source, avec le DOI du produit (par ex. `10.5067/FIRMS/MODIS/MCD14DL.NRT.0061` pour MODIS NRT) et la date de téléchargement |
| Questions de l'analyse auxquelles elle pourrait répondre | Q1 : où et quand partent les feux en 2026, la seule saison que la BDIFF n'a pas encore. Q3 : ajouter 2026 aux jours avec départ, avec prudence (voir plus bas). Contrôle de la BDIFF : un feu vu par satellite et absent de la BDIFF |

## Contrôles qualité repérés

- Doublons : 0 ligne exactement en double. Par contre, le même feu revient plusieurs fois. Haguenau, nuit du 12/08/2026 : 3 satellites entre 01 h 32 et 02 h 51 UTC, plus 2 pixels voisins dans la commune de Mertzwiller, soit 5 lignes pour un seul feu d'environ 1 ha. Il faut regrouper en « commune × jour » avant de compter des départs
- Dates : toutes en 2026, du 01/01 au 18/11. Heures en UTC (voir les clés)
- Codes géographiques : aucun dans le fichier. Rattachement par les contours 2026 (5 115 communes du Grand Est). Grand Est : 08 → 116, 10 → 131, 51 → 451, 52 → 37, 54 → 854, 55 → 290, 57 → 776, 67 → 46, 68 → 274, 88 → 66
- Valeurs manquantes : aucune sur les colonnes communes. Mais les colonnes changent selon le capteur :
  - MODIS : `brightness`, `bright_t31`, `confidence` de 0 à 100
  - VIIRS : `bright_ti4`, `bright_ti5`, `confidence` en `l` / `n` / `h`
  - la colonne `type` (0 = végétation présumée, 2 = autre source fixe) n'existe que dans les fichiers SP

  Il faut harmoniser avant de fusionner
- Faux positifs : beaucoup.
  - Dans les fichiers SP, 3 754 lignes sur le rectangle sont marquées `type = 2` (source fixe, pas un feu), contre 1 718 en `type = 0`
  - Dans le Grand Est, 22 cases d'environ 1 km sont vues 10 jours ou plus dans l'année : ce sont des usines, pas des feux. Par exemple Héming (129 jours, cimenterie), Neuves-Maisons (122 jours, aciérie), Couvrot (117 jours, cimenterie), Serémange-Erzange (59 jours, site ArcelorMittal)
  - Aucune case de ce genre dans le Bas-Rhin
- Feux manqués : le satellite ne voit pas tout. À Haguenau, le feu du 13/08/2026 (le 3ᵉ en deux jours, une trentaine de pompiers d'après France 3) et celui du 25/06/2026 n'ont aucune détection. Causes possibles : nuages, feu trop petit, ou pas de passage de satellite au bon moment

## Ce qu'on retient

- Utile pour 2026, à condition de le présenter comme un **indicateur et pas comme une liste de feux**. Dans le Bas-Rhin : 46 détections, 26 jours différents, 23 communes, d'avril à octobre, avec un pic en juillet (12). Le feu de Haguenau du 12/08 est bien vu, celui du 13/08 non
- Ce qui m'a surpris : la majorité des points du Grand Est ne sont pas des feux de forêt. Ce sont des usines qui reviennent toute l'année, et sûrement des brûlages agricoles en plaine (Nordhouse, Uhrwiller...). FIRMS ne dit pas si un point est en forêt : il faudra le croiser avec la BD Forêt pour ne garder que les points en forêt ou en lisière
- Pour le pipeline (#37) : regrouper en commune × jour en heure française, enlever `type = 2` et les cases vues 10 jours ou plus, et marquer ces jours « détection satellite », jamais « départ de feu » comme dans la BDIFF. Les règles FIRMS restent à ajouter dans [regles.md](../qualite/regles.md)
