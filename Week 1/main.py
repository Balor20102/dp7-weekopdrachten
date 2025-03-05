from stap import Stap
from ingredient import Ingredient
from recept import Recept
from gegevens import (stappen_lijst, lijst_ingredient, 
                      stappen_lijst_recept_2, lijst_ingredient_recept_2, 
                      stappen_lijst_recept_3, lijst_ingredient_recept_3)

def maak_recept(naam, omschrijving, lijst_ingredienten, lijst_stappen):
    """Maakt een Recept-object en vult het met ingrediënten en stappen."""
    recept = Recept(naam, omschrijving, [], [])
    for ingredient in lijst_ingredienten:
        naam, hoeveelheid, eenheid = ingredient
        recept.voeg_ingredient_toe(Ingredient(naam, hoeveelheid, eenheid))
    
    for stap in lijst_stappen:
        recept.voeg_stap_toe(Stap(stap[0]))
    
    return recept

if __name__ == "__main__":
    # Maak een lijst van recepten
    lijst_recepten = [
        maak_recept('pannenkoeken', 'voor ca. 8 stuks', lijst_ingredient, stappen_lijst),
        maak_recept('wafels', 'voor ca. 8 stuks', lijst_ingredient_recept_2, stappen_lijst_recept_2),
        maak_recept('spinaziepannenkoeken', 'voor ca. 8 stuks', lijst_ingredient_recept_3, stappen_lijst_recept_3)
    ]

    # Print een overzicht van recepten
    print("\nBeschikbare recepten:")
    for recept in lijst_recepten:
        print(f"- {recept.get_naam()}")

    # Gebruiker selecteert een recept
    gekozen_recept = input("\nSelecteer je recept: ").strip().lower()

    # Zoek naar het recept in de lijst
    recept_gevonden = next((r for r in lijst_recepten if r.get_naam().lower() == gekozen_recept), None)

    if not recept_gevonden:
        print("❌ Recept niet gevonden! Probeer opnieuw.")
    else:
        # Print receptgegevens
        print(f"\n🍽️ Recept: {recept_gevonden.get_naam()}")
        print(f"📖 Omschrijving: {recept_gevonden.omschrijving}")

        # Print ingrediënten
        print("\n🛒 Ingrediënten:")
        for ingredient in recept_gevonden.ingredienten_lijst:
            print(f"• {ingredient.naam} {ingredient.hoeveelheid} {ingredient.eenheid}")

        # Print bereidingsstappen
        print("\n👨‍🍳 Bereidingsstappen:")
        for index, stap in enumerate(recept_gevonden.stappen_lijst, 1):
            print(f"{index}. {stap.stap}")

