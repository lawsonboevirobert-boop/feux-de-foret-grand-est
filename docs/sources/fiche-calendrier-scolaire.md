# Fiche source : calendrier scolaire (Éducation nationale)

Explorée par : @wilsonDenis, le 2026-11-18
Lien : https://data.education.gouv.fr/explore/dataset/fr-en-calendrier-scolaire/
Fichier ouvert : export CSV complet du jeu (`fr-en-calendrier-scolaire`, séparateur `;`), via l'API du portail, sans compte

| Rubrique | Valeur |
|---|---|
| Propriétaire et système | Ministère de l'Éducation nationale (DNE), portail data.education.gouv.fr |
| Mode d'accès (export, API, téléchargement) et format | export CSV ou JSON depuis le portail (API Opendatasoft), pas de compte. Attention : le fichier arrive compressé (gzip) si on le télécharge en ligne de commande |
| Grain (une ligne = ?) | 1 période de vacances x 1 académie x 1 population (élèves, enseignants ou "-") : description, date de début, date de fin, académie, zone, année scolaire |
| Emprise géographique | toutes les académies, outre-mer compris. Pour nous : académie de Strasbourg (67, 68) en zone B. Les autres académies du Grand Est (Nancy-Metz, Reims) sont aussi dans le fichier |
| Période réellement couverte par les données | pour Strasbourg : de l'année 2017-2018 a 2027-2028. Avant 2017-2018 il n'y a que la Corse dans le fichier, alors que le jeu commence en 2009-2010 |
| Date de dernière mise à jour affichée sur la fiche | 01/10/2026 |
| Fréquence de mise à jour | non vérifiée : pas indiquée sur la fiche. Les nouvelles années sont ajoutées quand le ministère publie le calendrier |
| Volumétrie | 2 587 lignes, 7 colonnes, 274 Ko. Strasbourg : 75 lignes |
| Clés disponibles (sur quoi pourra-t-on joindre ?) | dates de début et de fin -> on fabrique une table "jour x académie : en vacances oui / non", qui se joint a la date d'un feu. Académie <-> département a faire nous-memes (67 et 68 = Strasbourg) |
| Données personnelles | aucune |
| Licence | Licence Ouverte 2.0 (Etalab), affichée sur le portail |
| Questions de l'analyse auxquelles elle pourrait répondre | Q3 : le type de jour (vacances scolaires ou pas) est une des 3 variables qu'on ajoute a l'indice |

## Contrôles qualité repérés

- Doublons : 10 périodes en double pour Strasbourg, mais c'est voulu : les grandes vacances ont une ligne "Élèves" et une ligne "Enseignants" avec des dates de fin différentes. On garde "Élèves" (ou "-")
- Dates : aucune date de fin avant la date de début. **Piège** : les dates sont en UTC, par ex. le début des vacances d'été 2027 est écrit `2027-07-02T22:00:00+00:00`, c'est le 3 juillet a minuit heure de Paris. Si on coupe juste la date sans convertir, on décale tout d'un jour
- Codes géographiques : pas de code académie ni département, juste le nom ("Strasbourg") et la zone ("Zone B")
- Valeurs manquantes : aucune case vide. Mais population incomplète : rien pour Strasbourg avant 2017-2018

## Ce qu'on retient

- Utile pour Q3, a condition de bien convertir les dates en heure de Paris
- Ce qui m'a surpris : il manque toute la période 2016 - aout 2017 pour la métropole. Pour tester notre règle "indice + type de jour" sur 10 ans, il faudra soit commencer a la rentrée 2017, soit retrouver les vacances 2016-2017 ailleurs (zone B, arreté du ministère). Pas fait, a décider en groupe
