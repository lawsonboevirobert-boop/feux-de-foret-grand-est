// Table de paramètre (chargée, reliée à rien) : le niveau de la Météo des forêts
// à partir duquel on lance le dispositif renforcé. Elle sert au segment de la page Décision.
#table(
    type table [Niveau = Int64.Type, #"Niveau de déclenchement" = text],
    {{1, "1 - faible"}, {2, "2 - modéré"}, {3, "3 - élevé"}, {4, "4 - très élevé"}}
)
