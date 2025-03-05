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

if __name__ == "__main__":
    # Maak een lijst van recepten
    lijst_recepten = [
        maak_recept('pannenkoeken', 'voor ca. 8 stuks', lijst_ingredient, stappen_lijst),
        maak_recept('wafels', 'voor ca. 8 stuks', lijst_ingredient_recept_2, stappen_lijst_recept_2),
        maak_recept('spinaziepannenkoeken', 'voor ca. 8 stuks', lijst_ingredient_recept_3, stappen_lijst_recept_3)
    ]

    # Print een lijst van beschikbare recepten
    print("\nBeschikbare recepten:")
    for recept in lijst_recepten:
        print(f"- {recept.get_naam()}")

    # Gebruiker kiest een recept
    input_user = input("\nSelecteer je recept: ").strip().lower()
    geselecteerd_recept = next((r for r in lijst_recepten if r.get_naam().lower() == input_user), None)

    if not geselecteerd_recept:
        print("❌ Recept niet gevonden! Probeer opnieuw.")
    else:
        # Gebruiker kiest aantal personen (foutafhandeling toegevoegd)
        while True:
            try:
                input_personen = int(input("Voor hoeveel personen? "))
                if input_personen > 0:
                    break
                else:
                    print("Aantal personen moet minimaal 1 zijn.")
            except ValueError:
                print("⚠️ Voer een geldig getal in.")

        geselecteerd_recept.set_aantal_personen(input_personen)

        # Gebruiker kiest of ze een vegan variant willen
        input_vegan = input("Wil je de vegan variant? (ja/nee) ").strip().lower() == "ja"

        # Print recept informatie
        print(f"\n🍽️ Recept: {geselecteerd_recept.get_naam()}")
        print(f"📖 Omschrijving: {geselecteerd_recept.omschrijving}")

        # Print ingrediënten met kcal-berekening
        totaal_kcal = 0
        print("\n🛒 Ingrediënten:")
        for ingredient in geselecteerd_recept.ingredienten_lijst:
            gekozen_ingredient = ingredient.alternatief if (input_vegan and ingredient.alternatief) else ingredient
            totaal_kcal += gekozen_ingredient.kcal * input_personen
            print(f"• {gekozen_ingredient.hoeveelheid * input_personen} {gekozen_ingredient.eenheid} {gekozen_ingredient.naam}")

        print(f"\n🔥 Totale kcal: {totaal_kcal} voor {input_personen} personen")

        # Print stappen met tips
        print("\n👨‍🍳 Bereidingsstappen:")
        for index, stap in enumerate(geselecteerd_recept.stappen_lijst, 1):
            print(f"{index}. {stap.stap} {'(💡 ' + stap.tip + ')' if stap.tip else ''}")