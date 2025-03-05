from ingredient import Ingredient

stappen_lijst = [
                    ["meng bakmeel met zout in een kom, maak een kuiltje in het midden", "voeg een zakje vanillesuiker toe"],
                    ["breek hier in het ei, en schenk er de helft van de melk bij.", ""],
                    ["roer van het midden uit, een glad beslag van en verdun dit al roerend met de rest van de melk", ""],
                    ["verhit een klonktje boter in een koekenpan", ""],
                    ["schenk met een pollepel zoveel beslag in de pan dat de bodem net bedekt is", ""],
                    ["bak de pannekoek tot dat de boven kant droog is", ""],
                    ["keer de pannekoek met behulp van een pannekoekenmes om en bak ook de andere kant goudbruin", ""],
                    ["leg de pannekoek op een voor verwarmt bord", ""],
                    ["bak vervolgens de volgende pannekoek en stapel ze op elkaar", ""]
                    ]

lijst_ingredient = (
                        ("zelfrijzend bakmeel", 250, "gram", 855, None),
                        ("zout", 1, "theelepel", 0, None),
                        ("ei", 1, "", 64, Ingredient('applemoes', 60 , "mililiter", 48, None)),
                        ("melk", 4.5, "deciliter", 300, Ingredient('sojamelk', 4.5, "deciliter", 144, None)),
                        ("boter", 50, "gram", 56, Ingredient('veganboter', 50, "gram", 177, None)),
                        )


stappen_lijst_recept_2 = [
    ["meng bloem, bakpoeder en zout in een kom", "voeg suiker en vanillesuiker toe"],
    ["klop de eieren los en voeg deze samen met de melk toe aan het bloemmengsel", ""],
    ["roer goed door en voeg gesmolten boter toe", ""],
    ["verhit een wafelijzer en vet het licht in met boter", ""],
    ["schep een lepel beslag in het ijzer en sluit het deksel", ""],
    ["bak de wafels goudbruin in ongeveer 3-5 minuten", ""],
    ["haal de wafel uit het ijzer en laat afkoelen op een rooster", ""],
    ["herhaal met de rest van het beslag", ""]
]

lijst_ingredient_recept_2 = (
    ("bloem", 250, "gram", 915, None),
    ("bakpoeder", 1, "theelepel", 0, None),
    ("zout", 1, "snufje", 0, None),
    ("suiker", 2, "eetlepels", 120, None),
    ("vanillesuiker", 1, "zakje", 30, None),
    ("ei", 2, "", 128, Ingredient('appelmoes', 120, "gram", 96, None)),
    ("melk", 3, "deciliter", 210, Ingredient('amandelmelk', 3, "deciliter", 90, None)),
    ("boter", 75, "gram", 540, Ingredient('margarine', 75, "gram", 270, None)),
)

stappen_lijst_recept_3 = [
    ["pureer de spinazie met de melk in een blender", ""],
    ["meng bloem en zout in een kom en maak een kuiltje in het midden", ""],
    ["voeg het ei toe en schenk de helft van het spinaziemengsel erbij", ""],
    ["roer tot een glad beslag en voeg al roerend de rest van het spinaziemengsel toe", ""],
    ["verhit een beetje olie in een koekenpan", ""],
    ["schep een lepel beslag in de pan en bak de pannenkoek tot de bovenkant droog is", ""],
    ["keer de pannenkoek om en bak de andere kant goudbruin", ""],
    ["herhaal met de rest van het beslag en stapel de pannenkoeken op", ""]
]

lijst_ingredient_recept_3 = (
    ("bloem", 200, "gram", 730, None),
    ("zout", 1, "snufje", 0, None),
    ("ei", 1, "", 64, Ingredient('chiazaad', 1, "eetlepel", 58, None)),
    ("melk", 3, "deciliter", 210, Ingredient('havermelk', 3, "deciliter", 90, None)),
    ("verse spinazie", 100, "gram", 23, None),
    ("olie", 20, "milliliter", 177, Ingredient('kokosolie', 20, "milliliter", 177, None)),
)