# Glossaire

Les termes inconnus de la commande et ceux des trois analyses individuelles, alignés sur l'[analyse globale](analyse/analyse-globale.md). Doublons fusionnés.

Statuts :

- **vérifié** : définition confirmée par une source officielle (voir « Sources » en bas) ;
- **définition du groupe** : convention que nous fixons pour nos calculs, à faire valider par le SDIS ;
- **à vérifier** : définition provisoire, la question ouverte est indiquée.

## Acteurs et dispositif

| Terme | Définition | Vient de | Statut |
|---|---|---|---|
| SDIS | Service départemental d'incendie et de secours : les sapeurs-pompiers du département. Ici le SDIS 67 (Bas-Rhin), auteur de la commande. | mail SDIS 67 | vérifié |
| CIS / chef de centre | Centre d'incendie et de secours, c'est-à-dire une caserne. Le chef de centre la dirige ; ce sont eux qui signalent que le seuil actuel fonctionne mal. | mail SDIS 67, analyses Denis + Franck | vérifié |
| dispositif renforcé | Moyens supplémentaires activés quand le danger est jugé élevé : patrouilles, guet, etc. Son contenu exact dans le Bas-Rhin et son coût par jour sont inconnus. | mail SDIS 67, toutes les analyses | à vérifier (demander au SDIS 67) |
| guet | Surveillance visuelle pour repérer un départ de feu le plus tôt possible (tours de guet, postes en hauteur). | mail SDIS 67 | à vérifier (existe-t-il des tours de guet dans le 67 ?) |
| patrouille | Équipe mobile qui circule dans les zones à risque pour détecter les départs tôt et intervenir vite. | mail SDIS 67 | à vérifier (composition dans le 67) |
| jour-secteur | Unité de coût du dispositif renforcé : un jour d'activation sur un secteur donné. Permet de compter combien d'activations le budget finance. | analyse Franck, analyse globale | définition du groupe |
| DFCI | Défense des forêts contre l'incendie : aménagements de prévention et de lutte (pistes, points d'eau, débroussaillement). | analyse Lawson | vérifié |

## Indice de danger

| Terme | Définition | Vient de | Statut |
|---|---|---|---|
| Météo des forêts | Carte de danger de feu de forêt publiée par Météo-France depuis juin 2023, chaque jour en saison vers 17 h, par département, pour le lendemain et le surlendemain. Elle est calculée à partir de l'IFM. Franck l'appelle « indice Météo-Forêt » : c'est la même chose. | mail SDIS 67, toutes les analyses | vérifié |
| niveau de danger | Les 4 niveaux de la Météo des forêts : faible (vert), modéré (jaune), élevé (orange), très élevé (rouge). Un niveau faible ne veut pas dire risque nul. | mail SDIS 67, analyses Denis + Lawson | vérifié |
| seuil | Niveau de danger à partir duquel le SDIS déclenche le dispositif renforcé. Le seuil actuel du 67 n'est pas connu. | mail SDIS 67, analyse Lawson | à vérifier (seuil actuel à demander au SDIS 67) |
| IFM (indice forêt météo) | Indice calculé par Météo-France, adapté de l'indice canadien (Fire Weather Index), à partir de la température, de l'humidité de l'air, du vent et des pluies. Il estime la probabilité qu'un feu éclose et son potentiel de propagation. Il existe sur une période plus longue que la Météo des forêts. | analyses Denis + Lawson | vérifié (calcul détaillé et historique disponible à vérifier) |

## Feux

| Terme | Définition | Vient de | Statut |
|---|---|---|---|
| départ de feu | Début d'un incendie, détecté ou non. À distinguer du feu de forêt qui figure dans les bases. Question : compte-t-on tous les départs ou seulement ceux qui deviennent des feux de forêt ? | mail SDIS 67, analyse Franck | à vérifier |
| feu de forêt | Incendie qui atteint une forêt (et selon les sources, landes ou broussailles). La surface minimale pour qu'un feu soit compté varie selon les sources. | analyse Denis | à vérifier (définition exacte de la BDIFF) |
| surface brûlée | Surface touchée par un feu, en hectares. | analyse Denis | vérifié |
| saison feux | Période où le risque est le plus élevé, surtout l'été. Pour nos calculs : mars à octobre. Météo-France ne publie la Météo des forêts qu'en saison. | mail SDIS 67, analyses Lawson + Franck | définition du groupe |
| interface habitat-forêt | Zones où les habitations touchent la forêt : un feu y est plus dangereux pour les personnes et les biens. | analyse Lawson | vérifié |

## Évaluation du seuil

| Terme | Définition | Vient de | Statut |
|---|---|---|---|
| jour avec feu | Jour où au moins un feu de forêt a démarré dans la zone étudiée (département ou secteur). | analyse globale | définition du groupe |
| fausse alerte (faux positif) | Jour où le niveau prévu la veille est au-dessus du seuil, sans aucun feu ce jour-là. | mail SDIS 67, analyses Lawson + Franck | définition du groupe |
| feu manqué (faux négatif) | Jour où le niveau prévu la veille est sous le seuil et où un feu se déclare quand même. | mail SDIS 67, analyses Lawson + Franck | définition du groupe |
| taux de base | Part des jours avec feu sur la période, tous niveaux confondus. Sert de référence pour juger si l'indice apporte quelque chose. | analyse Lawson | définition du groupe |
| taux de feux couverts | Part des feux survenus un jour où le dispositif aurait été activé avec un seuil donné. | analyse Lawson | définition du groupe |

## Sources de données

| Terme | Définition | Vient de | Statut |
|---|---|---|---|
| BDIFF | Base de données sur les incendies de forêt en France : liste des feux depuis 2006, à l'échelle de la commune, gérée par l'IGN pour le ministère de l'Agriculture. | analyses Denis + Lawson | vérifié (champs disponibles, dont la cause, à vérifier) |
| Prométhée | Base des incendies de forêt de la zone méditerranéenne, plus ancienne que la BDIFF (depuis 1973). Ne couvre pas le Grand Est. | analyse globale | vérifié |
| EFFIS | European Forest Fire Information System : système européen d'information sur les feux de forêt (Copernicus), avec surfaces brûlées et indices de danger. | analyse Lawson | à vérifier (données utiles pour le Grand Est) |
| CORINE Land Cover | Inventaire européen de l'occupation du sol, utile pour connaître la surface et le type de forêt. | analyse Lawson | vérifié |
| COG | Code officiel géographique de l'INSEE : codes des communes. Il change chaque année (fusions de communes), donc il faut savoir de quel millésime est chaque code. | analyse Denis, cours | vérifié |

## Vocabulaire de la donnée

| Terme | Définition | Vient de | Statut |
|---|---|---|---|
| grain | Niveau de détail d'une donnée : ce que représente une ligne (un feu, un jour × un département, une commune). | analyse Franck, consigne | vérifié |
| période | Intervalle de temps couvert par la donnée. | consigne | vérifié |
| fraîcheur | Délai entre l'événement et la disponibilité de la donnée, ou fréquence de mise à jour. | analyse Franck, consigne | vérifié |
| emprise | Périmètre géographique couvert par la donnée (Bas-Rhin, Grand Est, France). | analyse Franck, consigne | vérifié |

## Sources

- Météo-France et ONF, Météo des forêts : [feuxdeforet.fr](https://www.feuxdeforet.fr/moyens-de-lutte/surveillance-et-prevention/meteo-des-forets/), [préfecture de la Lozère](https://www.lozere.gouv.fr/index.php/contenu/telechargement/29657/259507/file/CP%20-%20M%C3%A9t%C3%A9o%20des%20For%C3%AAts%20-Incendies.pdf)
- Ministère de la Transition écologique, [feux de forêt et de végétation](https://www.ecologie.gouv.fr/feux-foret-et-vegetation)
- BDIFF : [bdiff.agriculture.gouv.fr](https://bdiff.agriculture.gouv.fr), [data.gouv.fr](https://www.data.gouv.fr/reuses/indicateur-territorial-des-incendies-de-foret)
