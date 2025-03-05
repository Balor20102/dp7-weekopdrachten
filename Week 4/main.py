import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from stap import Stap
from ingredient import Ingredient
from recept import Recept
from gegevens import (stappen_lijst, lijst_ingredient, 
                      stappen_lijst_recept_2, lijst_ingredient_recept_2, 
                      stappen_lijst_recept_3, lijst_ingredient_recept_3)

DB_NAME = "receptenboek.sqlite"

# ------------------ DATABASE FUNCTIES ------------------

def setup_database():
    """Maakt de database en tabellen als deze nog niet bestaan."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recepten (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        naam TEXT UNIQUE,
        omschrijving TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredienten (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recept_id INTEGER,
        naam TEXT,
        hoeveelheid REAL,
        eenheid TEXT,
        kcal INTEGER,
        FOREIGN KEY (recept_id) REFERENCES recepten(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stappen (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recept_id INTEGER,
        beschrijving TEXT,
        tip TEXT,
        FOREIGN KEY (recept_id) REFERENCES recepten(id)
    )
    """)

    conn.commit()
    conn.close()

def voeg_recept_toe_db(recept):
    """Voegt een recept toe aan de database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO recepten (naam, omschrijving) VALUES (?, ?)", (recept.naam, recept.omschrijving))
    recept_id = cursor.lastrowid

    for ingredient in recept.ingredienten_lijst:
        cursor.execute("INSERT INTO ingredienten (recept_id, naam, hoeveelheid, eenheid, kcal) VALUES (?, ?, ?, ?, ?)",
                       (recept_id, ingredient.naam, ingredient.hoeveelheid, ingredient.eenheid, ingredient.kcal))

    for stap in recept.stappen_lijst:
        cursor.execute("INSERT INTO stappen (recept_id, beschrijving, tip) VALUES (?, ?, ?)",
                       (recept_id, stap.stap, stap.tip))

    conn.commit()
    conn.close()

def verwijder_recept_db(recept_naam):
    """Verwijdert een recept uit de database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ingredienten WHERE recept_id IN (SELECT id FROM recepten WHERE naam = ?)", (recept_naam,))
    cursor.execute("DELETE FROM stappen WHERE recept_id IN (SELECT id FROM recepten WHERE naam = ?)", (recept_naam,))
    cursor.execute("DELETE FROM recepten WHERE naam = ?", (recept_naam,))

    conn.commit()
    conn.close()

# ------------------ PDF GENERATIE ------------------

def exporteer_als_pdf(recept):
    """Exporteert een recept naar een goed opgemaakte PDF."""

    bestandsnaam = f"{recept.naam}.pdf"
    c = canvas.Canvas(bestandsnaam, pagesize=letter)
    width, height = letter
    marge_links = 100
    y = height - 50  # Startpositie bovenaan de pagina
    regelafstand = 20

    def nieuwe_pagina():
        """Voegt een nieuwe pagina toe en reset de y-positie."""
        nonlocal y
        c.showPage()
        y = height - 50  # Reset naar bovenaan nieuwe pagina

    def schrijf_tekst(tekst, x, y, max_breedte=400):
        """Schrijft tekst met automatische woordafbreking."""
        regels = simpleSplit(tekst, c._fontname, c._fontsize, max_breedte)
        for regel in regels:
            if y < 50:  # Controleer of we een nieuwe pagina nodig hebben
                nieuwe_pagina()
            c.drawString(x, y, regel)
            y -= regelafstand
        return y  # Geef de nieuwe y-positie terug

    # Titel en omschrijving
    c.setFont("Helvetica-Bold", 14)
    y = schrijf_tekst(f"Recept: {recept.naam}", marge_links, y)
    
    c.setFont("Helvetica", 12)
    y -= regelafstand
    y = schrijf_tekst(f"Omschrijving: {recept.omschrijving}", marge_links, y)

    # Ingrediënten-sectie
    if recept.ingredienten_lijst:
        c.setFont("Helvetica-Bold", 12)
        y -= regelafstand
        y = schrijf_tekst("Ingrediënten:", marge_links, y)

        c.setFont("Helvetica", 11)
        for ingredient in recept.ingredienten_lijst:
            y -= regelafstand
            y = schrijf_tekst(
                f"- {ingredient.hoeveelheid} {ingredient.eenheid} {ingredient.naam} ({ingredient.kcal} kcal)",
                marge_links, y
            )
    else:
        y -= regelafstand
        y = schrijf_tekst("Geen ingrediënten beschikbaar.", marge_links, y)

    # Bereidingsstappen-sectie
    if recept.stappen_lijst:
        c.setFont("Helvetica-Bold", 12)
        y -= 2 * regelafstand
        y = schrijf_tekst("Bereidingsstappen:", marge_links, y)

        c.setFont("Helvetica", 11)
        for index, stap in enumerate(recept.stappen_lijst, 1):
            y -= regelafstand
            y = schrijf_tekst(f"{index}. {stap.stap}", marge_links, y)
            if stap.tip:
                y -= regelafstand
                y = schrijf_tekst(f"   Tip: {stap.tip}", marge_links + 20, y)
    else:
        y -= regelafstand
        y = schrijf_tekst("Geen bereidingsstappen beschikbaar.", marge_links, y)

    # PDF opslaan
    c.save()
    print(f"📄 PDF '{bestandsnaam}' succesvol gegenereerd!")



def haal_recepten_op():
    """Haalt alle recepten op en vult deze met ingrediënten en stappen."""
    recepten = []

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Stap 1: Haal alle recepten op
        cursor.execute("SELECT id, naam, omschrijving FROM recepten")
        recepten_rows = cursor.fetchall()

        for recept_id, naam, omschrijving in recepten_rows:
            # Stap 2: Haal ingrediënten op voor dit recept
            cursor.execute("SELECT naam, hoeveelheid, eenheid, kcal FROM ingredienten WHERE recept_id = ?", (recept_id,))
            ingredienten_rows = cursor.fetchall()
            ingredienten = [Ingredient(naam, hoeveelheid, eenheid, kcal, None) for naam, hoeveelheid, eenheid, kcal in ingredienten_rows]

            # Stap 3: Haal stappen op voor dit recept
            cursor.execute("SELECT beschrijving, tip FROM stappen WHERE recept_id = ?", (recept_id,))
            stappen_rows = cursor.fetchall()
            stappen = [Stap(beschrijving, tip) for beschrijving, tip in stappen_rows]

            # Stap 4: Maak het Recept-object en voeg het toe aan de lijst
            recept = Recept(naam, omschrijving, ingredienten, stappen, recept_id)
            recepten.append(recept)

    return recepten

def toon_recepten():
    """Toont een lijst van alle beschikbare recepten."""
    lijst_recepten = haal_recepten_op()
    if not lijst_recepten:
        print("📭 Geen recepten gevonden.")
        return
    
    print("\n📜 Beschikbare recepten:")
    for index, recept in enumerate(lijst_recepten, 1):
        print(f"{index}. {recept.naam}")

def toon_recept(lijst_recepten):
    """Toont een lijst met recepten en laat de gebruiker een recept kiezen om details te zien."""
    if not lijst_recepten:
        print("📭 Geen recepten gevonden.")
        return
    
    print("\n📜 Beschikbare recepten:")
    for index, recept in enumerate(lijst_recepten, 1):
        print(f"{index}. {recept.naam}")
    
    keuze = input("\nSelecteer een receptnummer: ").strip()
    if not keuze.isdigit() or int(keuze) < 1 or int(keuze) > len(lijst_recepten):
        print("❌ Ongeldige keuze.")
        return
    

    recept = lijst_recepten[int(keuze) - 1]
    print(f"\n📖 Recept: {recept.naam}\nOmschrijving: {recept.omschrijving}\n\nIngrediënten:")

    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM recepten WHERE naam = ?", (recept.naam,))
        recept_id = cursor.fetchone()[0]
        cursor.execute("SELECT naam, hoeveelheid, eenheid, kcal FROM ingredienten WHERE recept_id = ?", (recept_id,))
        ingredienten = cursor.fetchall()
    
    for naam, hoeveelheid, eenheid, kcal in ingredienten:
        print(f"- {hoeveelheid} {eenheid} {naam} ({kcal} kcal)")
    
    print("\nBereidingsstappen:")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM recepten WHERE naam = ?", (recept.naam,))
        recept_id = cursor.fetchone()[0]
        cursor.execute("SELECT beschrijving, tip FROM stappen WHERE recept_id = ?", (recept_id,))
        stappen = cursor.fetchall()
    
    for index, (beschrijving, tip) in enumerate(stappen, 1):
        print(f"{index}. {beschrijving}")
        if tip:
            print(f"   Tip: {tip}")

def voeg_recept_toe():
    """Voegt een nieuw recept toe aan de database."""
    naam = input("Naam van het recept: ").strip()
    omschrijving = input("Korte omschrijving: ").strip()
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recepten (naam, omschrijving) VALUES (?, ?)", (naam, omschrijving))
        recept_id = cursor.lastrowid
    
    ingredienten = []
    while True:
        naam_ing = input("Ingrediënt naam (of enter om te stoppen): ").strip()
        if not naam_ing:
            break
        hoeveelheid = input("Hoeveelheid: ").strip()
        eenheid = input("Eenheid: ").strip()
        kcal = input("Kcal: ").strip()
        
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ingredienten (recept_id, naam, hoeveelheid, eenheid, kcal) VALUES (?, ?, ?, ?, ?)",
                           (recept_id, naam_ing, hoeveelheid, eenheid, kcal))
    
    stappen = []
    while True:
        beschrijving = input("Stap beschrijving (of enter om te stoppen): ").strip()
        if not beschrijving:
            break
        tip = input("Optionele tip: ").strip()
        
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO stappen (recept_id, beschrijving, tip) VALUES (?, ?, ?)",
                           (recept_id, beschrijving, tip))
    
    print(f"✅ Recept '{naam}' toegevoegd!")

def verwijder_recept():
    """Verwijdert een recept uit de database."""
    lijst_recepten = haal_recepten_op()
    toon_recept(lijst_recepten)
    
    keuze = input("\nWelk recept wil je verwijderen? Voer de naam in: ").strip()
    
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ingredienten WHERE recept_id IN (SELECT id FROM recepten WHERE naam = ?)", (keuze,))
        cursor.execute("DELETE FROM stappen WHERE recept_id IN (SELECT id FROM recepten WHERE naam = ?)", (keuze,))
        cursor.execute("DELETE FROM recepten WHERE naam = ?", (keuze,))
        
        if cursor.rowcount:
            print(f"🗑️ Recept '{keuze}' is verwijderd.")
        else:
            print("❌ Recept niet gevonden.")



def voeg_recept_toe_db(recept_naam, omschrijving, ingredienten_lijst, stappen_lijst):
    """Voegt een recept toe aan de database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recepten (naam, omschrijving) VALUES (?, ?)", (recept_naam, omschrijving))
        recept_id = cursor.lastrowid
        
        for naam, hoeveelheid, eenheid, kcal, alternatief in ingredienten_lijst:
            cursor.execute("INSERT INTO ingredienten (recept_id, naam, hoeveelheid, eenheid, kcal) VALUES (?, ?, ?, ?, ?)",
                           (recept_id, naam, hoeveelheid, eenheid, kcal))
        
        for beschrijving, tip in stappen_lijst:
            cursor.execute("INSERT INTO stappen (recept_id, beschrijving, tip) VALUES (?, ?, ?)",
                           (recept_id, beschrijving, tip))
        
        conn.commit()
        print(f"✅ Recept '{recept_naam}' toegevoegd!")

if __name__ == "__main__":

    setup_database()


    # print("📥 Bezig met het toevoegen van recepten aan de database...")
    
    # voeg_recept_toe_db("Pannenkoeken", "Voor ca. 8 stuks", lijst_ingredient, stappen_lijst)
    # voeg_recept_toe_db("Wafels", "Voor ca. 8 stuks", lijst_ingredient_recept_2, stappen_lijst_recept_2)
    # voeg_recept_toe_db("Spinaziepannenkoeken", "Voor ca. 8 stuks", lijst_ingredient_recept_3, stappen_lijst_recept_3)
    
    # print("✅ Alle recepten succesvol toegevoegd!")

    lijst_recepten = haal_recepten_op()
    
    while True:
        print("\n📌 Wat wil je doen?")
        print("1️⃣ Recept bekijken")
        print("2️⃣ Recept toevoegen")
        print("3️⃣ Recept verwijderen")
        print("4️⃣ Exporteren als PDF")
        print("5️⃣ Afsluiten")
        
        keuze = input("Kies een optie: ").strip()
        
        if keuze == "1":
            toon_recept(lijst_recepten)
        elif keuze == "2":
            voeg_recept_toe()
        elif keuze == "3":
            verwijder_recept()
        elif keuze == "4":
            if not lijst_recepten:
                print("📭 Geen recepten gevonden.")
                continue
            else:
                toon_recepten()  # Display recipes to the user
                keuze = input("\nSelecteer een receptnummer: ").strip()

                # Validate user input
                if not keuze.isdigit() or int(keuze) < 1 or int(keuze) > len(lijst_recepten):
                    print("❌ Ongeldige keuze.")
                    continue
                else:
                    # Select the recipe
                    recept = lijst_recepten[int(keuze) - 1]
                    
                    exporteer_als_pdf(recept)
        elif keuze == "5":
            print("👋 Programma afgesloten.")
            break
        else:
            print("⚠️ Ongeldige invoer, probeer opnieuw.")