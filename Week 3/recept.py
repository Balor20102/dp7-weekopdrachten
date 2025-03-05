class Recept:
    def __init__(self, naam, omschrijving, ingredienten_lijst, stappen_lijst, aantal_personen):
        self.naam  = str(naam)
        self.omschrijving = str(omschrijving)
        self.ingredienten_lijst = list(ingredienten_lijst)
        self.stappen_lijst = list(stappen_lijst)
        self.aantal_personen = aantal_personen


    def __str__(self):
        return f"{self.naam}"
    
    def voeg_ingredient_toe(self, ingredient):
        self.ingredienten_lijst.append(ingredient)

    def get_ingredienten(self):
        return self.ingredienten_lijst
    
    def get_naam (self):
        return self.naam

    def voeg_stap_toe(self, stap):
        self.stappen_lijst.append(stap)

    def get_aantal_personen(self): 
        return self.aantal_personen
    
    def set_aantal_personen(self, aantal_personen):
        self.aantal_personen = aantal_personen
        for ingredient in self.ingredienten_lijst:
            ingredient.set_hoeveelheid(aantal_personen)

    def get_plantaardig_recept(self):
        ingredienten_lijst_plantaardig = []
        for ingredient in self.ingredienten_lijst:
            ingredienten_lijst_plantaardig.append(ingredient.get_ingrediënt(True))

        return ingredienten_lijst_plantaardig