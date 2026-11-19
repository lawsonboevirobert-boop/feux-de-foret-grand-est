# Comment on travaille sur le dépôt

Les règles qu'on suit depuis le début, écrites pour que tout le monde (et la prof) les retrouve au même endroit.

## Une tâche = une issue = une branche = une PR

1. La tâche a une issue, avec un responsable et un relecteur
2. On crée une branche depuis `main` à jour
3. On ouvre une PR qui renvoie à l'issue (`Refs #12`, ou `Closes #12` si la PR la termine)
4. Un autre membre relit et approuve
5. **L'auteur fusionne sa PR lui-même**, une fois approuvée et sans conflit

`main` est protégée : on n'y pousse jamais directement.

## Nommer une branche

`type/numero-sujet`, en minuscules et avec des tirets. Exemples : `docs/7-inventaire-sources`, `feat/37-nettoyage-cog`, `test/48-tests-qualite-bdiff`.

| Type | Pour quoi |
|---|---|
| `docs` | documents : fiches, analyses, journal, README |
| `feat` | du code qui ajoute quelque chose (récupération, nettoyage, modèle) |
| `fix` | corriger un bug |
| `test` | ajouter ou modifier des tests |
| `chore` | le reste : `.gitignore`, dépendances, rangement |

## Écrire un message de commit

`type(portée): ce que fait le commit`, en français, court, au présent ou à l'infinitif.

```
docs(sources): ajouter la fiche de la BDIFF
feat(nettoyage): table des communes et passage des anciens codes (#37)
fix(recuperation): reprendre un téléchargement coupé
```

- la portée est le dossier ou le sujet : `sources`, `analyse`, `qualite`, `decisions`, `nettoyage`, `recuperation`, `kpi`...
- un changement par commit. Une fiche = un commit
- chacun commite depuis son propre compte. Les exercices individuels (analyse de la commande, fiches, partie A de l'exo 3, fiche KPI) sont commités par leur auteur, c'est ce qui est noté
- le message de la fusion : `Merge pull request #N : sujet en quelques mots`

## Relire une PR

Le relecteur :

- ouvre les fichiers, pas seulement le résumé. Les chiffres se revérifient dans les données quand c'est possible
- pour du code : lance `python -m unittest discover -s tests -t .` et la commande de la PR
- vérifie qu'aucune donnée ni clé ne part dans le commit
- écrit ce qui est bon et ce qui est à changer. Il approuve quand tout ce qui bloque est réglé, les petites remarques peuvent rester en commentaire

Le responsable d'un domaine relit les PR de son domaine (sources : Lawson, pipeline : Franck, qualité : Denis), même s'il ne les a pas faites.

## Ce qui ne part jamais sur GitHub

- les données (`data/raw/`, `data/processed/`) : chacun les retélécharge avec `python -m src.recuperation`
- les clés d'API : elles vont dans `.env`, qui est ignoré. Le dépôt contient seulement `.env.example`
- donc pas de `git add .` : on ajoute les fichiers un par un et on regarde `git status` avant de commiter

## Décisions

Toute décision du groupe, et tout changement de rôle, va dans le [journal des décisions](docs/decisions.md), la plus récente en haut, avec le modèle d'entrée du fichier.

## Qualité des données

Les règles sont dans [docs/qualite/regles.md](docs/qualite/regles.md). Une nouvelle source ou une nouvelle table propre arrive avec ses règles et ses tests.
