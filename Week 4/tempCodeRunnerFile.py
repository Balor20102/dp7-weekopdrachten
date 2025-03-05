keuze = input("\nSelecteer een receptnummer: ").strip()
                if not keuze.isdigit() or int(keuze) < 1 or int(keuze) > len(lijst_recepten):
                    print("❌ Ongeldige keuze.")
                    continue
                else:
                    recept = lijst_recepten[int(keuze) - 1]
                    exporteer_als_pdf(recept)