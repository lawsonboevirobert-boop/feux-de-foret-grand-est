# Modèle de fiche d'identité d'une source

Une fiche par source, dans `docs/sources/fiche-nom-de-la-source.md` (exemple : `docs/sources/fiche-meteo-des-forets.md`), comme le demande la consigne de l'exercice 2. Chacun écrit ses fiches et fait un commit par fiche depuis son compte.

Avant de remplir, ouvrir la page de la source et au moins un de ses fichiers.

Règles :

- Une rubrique qu'on n'a pas pu vérifier dans le fichier ou sa documentation s'écrit « non vérifiée », avec la raison. Une valeur supposée compte comme une erreur.
- La date de mise à jour affichée sur la fiche n'est pas la période couverte par les données : ce sont deux rubriques différentes.
- Une source inaccessible, trop lourde pour le temps du projet ou sans rapport avec nos questions se documente aussi. La fiche dit pourquoi.

```markdown
# Fiche source : <nom de la source>

Explorée par : @pseudo, le AAAA-MM-JJ
Lien : <url de la page de la source>
Fichier ouvert : <nom du fichier téléchargé ou de l'appel API testé>

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | |
| Mode d'accès (export, API, téléchargement) et format | |
| Grain (une ligne = ?) | |
| Emprise géographique | |
| Période réellement couverte par les données | |
| Date de dernière mise à jour affichée sur la fiche | |
| Fréquence de mise à jour | |
| Volumétrie | |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | |
| Données personnelles | |
| Licence | |
| Questions de l'analyse auxquelles elle pourrait répondre | (Q1 à Q5 de l'analyse globale) |

## Contrôles qualité repérés

- Doublons : le même événement est-il saisi deux fois ?
- Dates : sont-elles toutes dans la période annoncée ?
- Codes géographiques : les codes commune ou département existent-ils dans le COG ? De quel millésime ?
- Valeurs manquantes : quels champs sont souvent vides ?

## Ce qu'on retient

(Deux ou trois lignes : la source est-elle utile pour nous, et qu'est-ce qui nous a surpris ?)
```
