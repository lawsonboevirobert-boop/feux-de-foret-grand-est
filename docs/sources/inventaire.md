# Inventaire des sources - Exercice 2

Auteur : Franck Kevin TAMBOU
Périmètre : Grand Est, questions de l'Exercice 1 (ressources humaines et financières ; prévisions des feux de forêt).
Statut : brouillon à relire par le responsable sources avant fusion.

## 1. Sources retenues

| Source | Fiche | Producteur | Période utile | Usage pour l'exercice |
|:-------|:------|:-----------|:--------------|:----------------------|
| Météo des forêts (archives annuelles) | `fiche-archives-meteo-des-forets.md` | Météo-France | 3 juin 2024 à 5 octobre 2026 | Niveaux de danger par département (J+1, J+2) |
| Comptes des SDIS (OFGL) | `fiche-comptes-sdis.md` | OFGL | 2012 à 2025 | Dépenses et personnel des SDIS |
| Interventions des SIS (DGSCGC) | `fiche-interventions-sdis.md` | DGSCGC, ministère de l'Intérieur | 2008 à 2024, sauf 2019 | Nombre d'interventions par département, feux de végétations |
| BDIFF (MASA / IGN) | `fiche-bdiff.md` | MASA / IGN | Extrait Grand Est, 736 incidents | Feux de forêt individuels (date, surface, cause) |

## 2. Sources écartées

| Source | Raison |
|:-------|:-------|
| Pyro-SDIS 2024 | Écartée. Son contenu n'a pas été vérifié contre un fichier. |
| SIM Météo-France | Hors de la liste officielle retenue pour l'exercice. |
| Justificatifs de dépenses (PDF, XLSX) | Ne sont pas des sources officielles et concernent des dépenses individuelles identifiables : non utilisés. |

## 3. Questions sans réponse

1. **Interventions 2019 et 2025** : non reçues. La série du Grand Est a donc un trou sur ces deux années.
2. **Rupture du Bas-Rhin en 2013** (69 755 à 96 802, soit +39 %, porté par le secours à victime) : cause non vérifiée (changement de méthode ou de déclaration ?).
3. **Météo des forêts 2024** : tout le Grand Est est au niveau 1 sur toute l'année. Anomalie à confirmer auprès de Météo-France.
4. **BDIFF, Bas-Rhin 2012 à 2019** : aucune donnée pour cette période. À demander au SDIS du Bas-Rhin.
5. **BDIFF, cause renseignée** : seulement environ 13 % des feux ont une cause. Les analyses par cause restent limitées.
6. **Comptes des SDIS, licence** : non relevée dans le fichier ni sur la page.
7. **Comptes 2025 vs interventions** : le chiffre d'interventions 2025 du fichier OFGL (66 976 pour le Bas-Rhin) ne correspond pas à la série DGSCGC. Définition à confirmer avant toute jointure.

## 4. Surprises

- Le Bas-Rhin fait deux sauts de +39 % dans les interventions (2008-2009 et 2012-2013), alors que le reste du Grand Est progresse plus lentement.
- Les niveaux de danger de la Météo des forêts ne prennent jamais les niveaux 3 et 4 en 2024 pour tout le Grand Est : la saison 2024 n'est pas comparable aux saisons suivantes.
- Le libellé des comptes passe de « SDIS » à « SIS » en 2024 pour le Bas-Rhin et le Haut-Rhin : une jointure sur le libellé casse la série sans filtre adapté.
- Le fichier BDIFF ne couvre pas le Bas-Rhin entre 2012 et 2019.

## 5. Utiles mais inexploitables

- **API temps réel Météo-France** : données de danger plus récentes que les archives, mais accès authentifié. Hors de portée de l'exercice ; les archives annuelles suffisent.
- **Feux de végétations dans les interventions** : utiles pour Q4 et Q5, mais absentes en 2010-2013 et en 2019. Inexploitables seules pour une série continue.
- **Justificatifs de dépenses** : donnent le détail des dépenses individuelles mais ne sont pas une source publique exploitable pour l'exercice.
