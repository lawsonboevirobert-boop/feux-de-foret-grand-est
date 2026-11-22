// Dimension (chargée) : les causes de la BDIFF, une ligne par cause.
let
    Source = Table.Distinct(Table.SelectColumns(BDIFF_propre, {"Cause"})),
    AjoutConnue = Table.AddColumn(Source, "Cause connue", each [Cause] <> "Non renseignée", type logical),
    AjoutFamille = Table.AddColumn(AjoutConnue, "Famille", each
        if Text.StartsWith([Cause], "Involontaire") then "Involontaire"
        else if [Cause] = "Non renseignée" then "Non renseignée"
        else [Cause], type text)
in
    AjoutFamille
