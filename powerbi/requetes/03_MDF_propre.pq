// Requête intermédiaire (clic droit > décocher "Activer le chargement").
// Météo des forêts 2024-2026, Grand Est : une ligne = un jour concerné x un département.
let
    GrandEst = {"08", "10", "51", "52", "54", "55", "57", "67", "68", "88"},
    // un fichier par année, compressé ; séparateur "," en 2024-2025 et ";" en 2026 (règle M1)
    Lire = (annee as number, separateur as text) as table =>
        let
            Contenu = Binary.Decompress(
                File.Contents(DossierProjet & "data\raw\meteo_des_forets\mdf_" & Text.From(annee) & ".csv.gz"),
                Compression.GZip
            ),
            Csv = Csv.Document(Contenu, [Delimiter = separateur, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
            EnTetes = Table.PromoteHeaders(Csv, [PromoteAllScalars = true])
        in
            Table.SelectColumns(EnTetes, {"date", "num_dep", "niveau_j1"}),
    Empiler = Table.Combine({Lire(2024, ","), Lire(2025, ","), Lire(2026, ";")}),
    // règle M5 : "niveau_j1" vaut pour le lendemain de la diffusion. Les bulletins partent
    // entre 14h et 16h UTC, donc le jour UTC est aussi le jour à Paris
    AjoutDate = Table.AddColumn(Empiler, "Date", each Date.AddDays(
        #date(Number.From(Text.Start([date], 4)), Number.From(Text.Range([date], 5, 2)), Number.From(Text.Range([date], 8, 2))),
        1), type date),
    // règle M2 : le département est "8" en 2024-2025, "08" en 2026
    AjoutDepartement = Table.AddColumn(AjoutDate, "Code département", each Text.PadStart([num_dep], 2, "0"), type text),
    AjoutNiveau = Table.AddColumn(AjoutDepartement, "Niveau", each Number.From([niveau_j1]), Int64.Type),
    SeulementGrandEst = Table.SelectRows(AjoutNiveau, each List.Contains(GrandEst, [Code département])),
    Final = Table.SelectColumns(SeulementGrandEst, {"Date", "Code département", "Niveau"})
in
    Final
