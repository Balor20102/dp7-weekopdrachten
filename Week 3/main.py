from stap import Stap
from ingredient import Ingredient
from recept import Recept
from gegevens import (stappen_lijst, lijst_ingredient, 
                      stappen_lijst_recept_2, lijst_ingredient_recept_2, 
                      stappen_lijst_recept_3, lijst_ingredient_recept_3)

def maak_recept(naam, omschrijving, lijst_ingredienten, lijst_stappen):
    """Maakt een Recept-object en vult het met ingrediënten en stappen."""
    recept = Recept(naam, omschrijving, [], [], 1)
    for ingredient in lijst_ingredienten:
        naam, hoeveelheid, eenheid, kcal, alternatief = ingredient
        recept.voeg_ingredient_toe(Ingredient(naam, hoeveelheid, eenheid, kcal, alternatief))
    
    for stap in lijst_stappen:
        recept.voeg_stap_toe(Stap(stap[0], stap[1]))
    
    return recept

def toon_recepten(lijst_recepten):
    """Toont een overzicht van beschikbare recepten."""
    print("\n📜 Beschikbare recepten:")
    for recept in lijst_recepten:
        print(f"- {recept.get_naam()}")

def toon_recept(lijst_recepten):
    """Laat de gebruiker een recept selecteren en toont de details."""
    toon_recepten(lijst_recepten)
    gekozen_recept = input("\nSelecteer je recept: ").strip().lower()
    
    recept_gevonden = next((r for r in lijst_recepten if r.get_naam().lower() == gekozen_recept), None)
    
    if not recept_gevonden:
        print(" Recept niet gevonden! Probeer opnieuw.")
    else:
        while True:
            try:
                input_personen = int(input("Voor hoeveel personen? "))
                if input_personen > 0:
                    break
                else:
                    print("Aantal personen moet minimaal 1 zijn.")
            except ValueError:
                print(" Voer een geldig getal in.")

        recept_gevonden.set_aantal_personen(input_personen)

        input_vegan = input("Wil je de vegan variant? (ja/nee) ").strip().lower() == "ja"

        print(f"\n Recept: {recept_gevonden.get_naam()}")
        print(f" Omschrijving: {recept_gevonden.omschrijving}")

        totaal_kcal = 0
        print("\n Ingrediënten:")
        for ingredient in recept_gevonden.ingredienten_lijst:
            gekozen_ingredient = ingredient.alternatief if (input_vegan and ingredient.alternatief) else ingredient
            totaal_kcal += gekozen_ingredient.kcal * input_personen
            print(f"• {gekozen_ingredient.hoeveelheid * input_personen} {gekozen_ingredient.eenheid} {gekozen_ingredient.naam}")

        print(f"\n Totale kcal: {totaal_kcal} voor {input_personen} personen")

        print("\n Bereidingsstappen:")
        for index, stap in enumerate(recept_gevonden.stappen_lijst, 1):
            print(f"{index}. {stap.stap} {'(💡 ' + stap.tip + ')' if stap.tip else ''}")

def voeg_recept_toe(lijst_recepten):
    """Laat de gebruiker een nieuw recept toevoegen."""
    print("\n Nieuw recept toevoegen:")
    naam = input("Naam van het recept: ").strip()
    omschrijving = input("Omschrijving: ").strip()
    
    nieuw_recept = Recept(naam, omschrijving, [], [], 1)

    while True:
        naam = input("\nIngrediënt naam (of 'stop' om te beëindigen): ").strip()
        if naam.lower() == 'stop':
            break
        hoeveelheid = float(input("Hoeveelheid: ").strip())
        eenheid = input("Eenheid (gram, ml, etc.): ").strip()
        kcal = int(input("Aantal kcal: ").strip())
        alternatief = None  # Dit kan later uitgebreid worden
        nieuw_recept.voeg_ingredient_toe(Ingredient(naam, hoeveelheid, eenheid, kcal, alternatief))

    while True:
        stap_beschrijving = input("\nBereidingsstap (of 'stop' om te beëindigen): ").strip()
        if stap_beschrijving.lower() == 'stop':
            break
        tip = input("Tip (optioneel, druk Enter als je geen tip hebt): ").strip() or None
        nieuw_recept.voeg_stap_toe(Stap(stap_beschrijving, tip))

    lijst_recepten.append(nieuw_recept)
    print(f"\n Recept '{naam}' toegevoegd!")

def verwijder_recept(lijst_recepten):
    """Laat de gebruiker een recept verwijderen."""
    toon_recepten(lijst_recepten)
    gekozen_recept = input("\nWelk recept wil je verwijderen? ").strip().lower()
    
    for recept in lijst_recepten:
        if recept.get_naam().lower() == gekozen_recept:
            lijst_recepten.remove(recept)
            print(f" Recept '{recept.get_naam()}' verwijderd!")
            return
    
    print(" Recept niet gevonden.")

if __name__ == "__main__":
    lijst_recepten = [
        maak_recept('pannenkoeken', 'voor ca. 8 stuks', lijst_ingredient, stappen_lijst),
        maak_recept('wafels', 'voor ca. 8 stuks', lijst_ingredient_recept_2, stappen_lijst_recept_2),
        maak_recept('spinaziepannenkoeken', 'voor ca. 8 stuks', lijst_ingredient_recept_3, stappen_lijst_recept_3)
    ]

    while True:
        print("\n📌 Wat wil je doen?")
        print("1️ Recept bekijken")
        print("2️ Recept toevoegen")
        print("3️ Recept verwijderen")
        print("4️ Afsluiten")

        keuze = input("Kies een optie: ").strip()

        if keuze == "1":
            toon_recept(lijst_recepten)
        elif keuze == "2":
            voeg_recept_toe(lijst_recepten)
        elif keuze == "3":
            verwijder_recept(lijst_recepten)
        elif keuze == "4":
            print("Programma afgesloten.")
            break
        else:
            print("Ongeldige invoer, probeer opnieuw.")
