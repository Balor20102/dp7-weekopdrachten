class Ingredient:
    def __init__(self, naam, hoeveelheid, eenheid, kcal, alternatief_ingredient):
        self.naam = str(naam)
        self.hoeveelheid = float(hoeveelheid)
        self.eenheid = str(eenheid)
        self.kcal = int(kcal)
        self.alternatief = alternatief_ingredient
        
    def __str__(self):
        return self.naam
    
    def set_hoeveelheid(self, aantal_personen):
        self.hoeveelheid = self.hoeveelheid * aantal_personen

    def get_hoeveelheid(self):
        return self.hoeveelheid

    def get_kcal(self):
        return self.kcal

    def set_plantaardig_alternatief(self, alternatief_ingredient):
        self.alternatief = alternatief_ingredient

    def get_ingredient(self, plantaardig=False):
        """Retourneert of het normale of plantaardige ingrediënt gebruikt wordt."""
        if plantaardig and self.plantaardig_alternatief:
            return self.plantaardig_alternatief
        return self
        


    