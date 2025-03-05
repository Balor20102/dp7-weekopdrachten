class Recept:
    def __init__(self, naam, omschrijving, ingredienten_lijst, stappen_lijst):
        self.naam  = str(naam)
        self.omschrijving = str(omschrijving)
        self.ingredienten_lijst = list(ingredienten_lijst)
        self.stappen_lijst = list(stappen_lijst)

    def voeg_ingredient_toe(self, ingredient):
        self.ingredienten_lijst.append(ingredient)

    def get_ingredienten(self):
        return self.ingredienten_lijst
    
    def get_naam (self):
        return self.naam

    def voeg_stap_toe(self, stap):
        self.stappen_lijst.append(stap)

    def __str__(self):
        return f"{self.naam}"