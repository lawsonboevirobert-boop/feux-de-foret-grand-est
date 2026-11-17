# Modèle de fiche d'identité d'une source

Copier ce modèle dans `docs/sources/fiches/<nom-court>.md` pour chaque source retenue dans l'[inventaire](inventaire.md).

```markdown
# Fiche source : <nom de la source>

## Identité
- **Nom complet :**
- **Producteur :** (organisme qui produit la donnée)
- **Diffuseur :** (où on la récupère, si différent)
- **Lien d'accès :**
- **Licence :** (Licence Ouverte, ODbL, interne SDIS, etc.)
- **Date de consultation :** AAAA-MM-JJ
- **Consultée par :** @pseudo

## Contenu
- **Description :** (en une ou deux phrases)
- **Grain :** (que représente une ligne : 1 feu, 1 jour × 1 département, 1 commune…)
- **Période couverte :** (du … au …)
- **Fraîcheur :** (fréquence de mise à jour, délai de publication)
- **Emprise :** (Bas-Rhin, Grand Est, France…)
- **Format :** (CSV, JSON, GeoPackage, NetCDF, API…)
- **Volume :** (nombre de lignes ou taille des fichiers)
- **Système de coordonnées :** (si données géographiques : Lambert 93, WGS84…)

## Champs utiles
| Champ | Description | Exemple | Questions concernées |
|---|---|---|---|
| | | | |

## Questions couvertes
(Renvoyer aux questions de l'[analyse globale](../analyse/analyse-globale.md) : Q1, Q3…)

## Qualité et limites
- **Valeurs manquantes :**
- **Changements de définition dans le temps :**
- **Jointure avec les autres sources :** (clé commune : date, code INSEE, département…)
- **Données personnelles :** (oui / non, lesquelles)

## Statut
- [ ] accès testé
- [ ] échantillon téléchargé dans `data/raw/`
- [ ] fiche relue par le responsable qualité
```
