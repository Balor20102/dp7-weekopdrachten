class Ingredient:
    def __init__(self, naam, hoeveelheid, eenheid):
        self.naam = str(naam)
        self.hoeveelheid = float(hoeveelheid)
        self.eenheid = str(eenheid)

    def __str__(self):
        return self.naam

    