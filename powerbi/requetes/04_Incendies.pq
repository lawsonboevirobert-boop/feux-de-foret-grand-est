// Table de faits (chargée) : une ligne = un feu.
// On ajoute le niveau de la Météo des forêts du jour du feu, dans son département
// (vide si le feu est parti hors de la période de publication, ou avant juin 2024).
let
    // Table.Buffer : chaque fichier est lu une seule fois
    Source = Table.Buffer(BDIFF_propre),
    MdF = Table.Buffer(MDF_propre),
    Fusion = Table.NestedJoin(Source, {"Date", "Code département"}, MdF, {"Date", "Code département"}, "MdF", JoinKind.LeftOuter),
    AjoutNiveau = Table.ExpandTableColumn(Fusion, "MdF", {"Niveau"}, {"Niveau Météo des forêts"}),
    Types = Table.TransformColumnTypes(AjoutNiveau, {{"Niveau Météo des forêts", Int64.Type}}),
    // le même niveau en libellé, pour les graphiques
    Libelles = {"1 - faible", "2 - modéré", "3 - élevé", "4 - très élevé"},
    AjoutLibelle = Table.AddColumn(Types, "Niveau du jour", each
        if [Niveau Météo des forêts] = null then "Pas de bulletin" else Libelles{[Niveau Météo des forêts] - 1},
        type text)
in
    AjoutLibelle
