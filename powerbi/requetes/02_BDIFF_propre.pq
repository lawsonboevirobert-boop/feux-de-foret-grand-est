// Requête intermédiaire (clic droit > décocher "Activer le chargement").
// La BDIFF du Grand Est, 2006-2025, nettoyée : une ligne = un feu.
let
    Source = Csv.Document(
        File.Contents(DossierProjet & "data\raw\bdiff\bdiff_grand_est_2006_2025\Incendies.csv"),
        [Delimiter = ";", Columns = 24, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    // les 3 premières lignes du fichier sont un texte d'avertissement, pas des données
    SansAvertissement = Table.Skip(Source, 3),
    EnTetes = Table.PromoteHeaders(SansAvertissement, [PromoteAllScalars = true]),
    // minimisation (regles.md, partie 4) : pas de nom de commune, pas de décès ni de bâtiments
    ColonnesUtiles = Table.SelectColumns(EnTetes, {
        "Année", "Département", "Code INSEE", "Date de première alerte",
        "Surface parcourue (m2)", "Surface forêt (m2)", "Nature"
    }),
    Types = Table.TransformColumnTypes(ColonnesUtiles, {
        {"Année", Int64.Type}, {"Département", type text}, {"Code INSEE", type text},
        {"Date de première alerte", type datetime},
        {"Surface parcourue (m2)", type number}, {"Surface forêt (m2)", type number},
        {"Nature", type text}
    }, "en-US"),
    // règle B3 : doublon probable (même commune, même date et heure, même surface), Haguenau le 13/08/2025
    SansDoublon = Table.Distinct(Types, {"Code INSEE", "Date de première alerte", "Surface parcourue (m2)"}),
    // l'heure ne sort pas du pipeline (regles.md) : on garde seulement le jour
    AjoutDate = Table.AddColumn(SansDoublon, "Date", each DateTime.Date([Date de première alerte]), type date),
    AjoutDepartement = Table.AddColumn(AjoutDate, "Code département", each Text.PadStart([Département], 2, "0"), type text),
    AjoutSurface = Table.AddColumn(AjoutDepartement, "Surface (ha)", each [#"Surface parcourue (m2)"] / 10000, type number),
    AjoutSurfaceForet = Table.AddColumn(AjoutSurface, "Surface forêt (ha)", each [#"Surface forêt (m2)"] / 10000, type number),
    // règle B9 : 87 % des causes sont vides, on les garde en "Non renseignée"
    AjoutCause = Table.AddColumn(AjoutSurfaceForet, "Cause", each if [Nature] = null or [Nature] = "" then "Non renseignée" else [Nature], type text),
    Renommer = Table.RenameColumns(AjoutCause, {{"Code INSEE", "Code commune"}}),
    Final = Table.SelectColumns(Renommer, {
        "Année", "Date", "Code département", "Code commune", "Surface (ha)", "Surface forêt (ha)", "Cause"
    })
in
    Final
