import json
import os


class Inventory:
    def __init__(self, dateiname='inventar.json'):
        self.dateiname = dateiname
        self.lade_inventar()

    def lade_inventar(self):
        if os.path.exists(self.dateiname):
            with open(self.dateiname, 'r') as datei:
                self.inventar = json.load(datei)
        else:
            self.inventar = {
                "kategorien": {},
                "lagerorte": {},
                "lieferanten": {},
                "kunden": {},
                "auftraege": {}
            }

    def speichere_inventar(self):
        with open(self.dateiname, 'w') as datei:
            json.dump(self.inventar, datei, indent=4, ensure_ascii=False)

    def fuege_kategorie_hinzu(self, kategorie):
        if kategorie not in self.inventar["kategorien"]:
            self.inventar["kategorien"][kategorie] = {}
            print(f"Kategorie '{kategorie}' hinzugefügt.")
        else:
            print(f"Kategorie '{kategorie}' gibt's schon.")

    def fuege_lagerort_hinzu(self, lagerort):
        if lagerort not in self.inventar["lagerorte"]:
            self.inventar["lagerorte"][lagerort] = {}
            print(f"Lagerort '{lagerort}' hinzugefügt.")
        else:
            print(f"Lagerort '{lagerort}' gibt's schon.")

    def fuege_lieferant_hinzu(self, lieferant):
        if lieferant not in self.inventar["lieferanten"]:
            self.inventar["lieferanten"][lieferant] = []
            print(f"Lieferant '{lieferant}' hinzugefügt.")
        else:
            print(f"Lieferant '{lieferant}' gibt's schon.")

    def fuege_kunde_hinzu(self, kunde):
        if kunde not in self.inventar["kunden"]:
            self.inventar["kunden"][kunde] = []
            print(f"Kunde '{kunde}' hinzugefügt.")
        else:
            print(f"Kunde '{kunde}' gibt's schon.")

    def fuege_artikel_hinzu(self, kategorie, lagerort, name, menge, lieferant):
        if kategorie not in self.inventar["kategorien"]:
            print(f"Kategorie '{kategorie}' gibt's nicht.")
            return
        if lagerort not in self.inventar["lagerorte"]:
            print(f"Lagerort '{lagerort}' gibt's nicht.")
            return
        if lieferant not in self.inventar["lieferanten"]:
            print(f"Lieferant '{lieferant}' gibt's nicht.")
            return

        if lagerort not in self.inventar["kategorien"][kategorie]:
            self.inventar["kategorien"][kategorie][lagerort] = {}

        if name in self.inventar["kategorien"][kategorie][lagerort]:
            self.inventar["kategorien"][kategorie][lagerort][name] += menge
        else:
            self.inventar["kategorien"][kategorie][lagerort][name] = menge

        self.inventar["lieferanten"][lieferant].append(name)
        print(f"{menge} {name}(s) hinzugefügt in {kategorie} bei {lagerort} von {lieferant}.")
        self.speichere_inventar()

    def entferne_artikel(self, kategorie, lagerort, name, menge):
        if kategorie not in self.inventar["kategorien"]:
            print(f"Kategorie '{kategorie}' gibt's nicht.")
            return
        if lagerort not in self.inventar["kategorien"][kategorie]:
            print(f"Lagerort '{lagerort}' gibt's nicht.")
            return

        if name in self.inventar["kategorien"][kategorie][lagerort]:
            if self.inventar["kategorien"][kategorie][lagerort][name] >= menge:
                self.inventar["kategorien"][kategorie][lagerort][name] -= menge
                if self.inventar["kategorien"][kategorie][lagerort][name] == 0:
                    del self.inventar["kategorien"][kategorie][lagerort][name]
                    if not self.inventar["kategorien"][kategorie][lagerort]:
                        del self.inventar["kategorien"][kategorie][lagerort]
                print(f"{menge} {name}(s) entfernt aus {kategorie} bei {lagerort}.")
            else:
                print(f"Nicht genug {name} in {kategorie} bei {lagerort}.")
        else:
            print(f"{name} nicht gefunden in {kategorie} bei {lagerort}.")
        self.speichere_inventar()

    def wareneingang(self, kategorie, lagerort, name, menge, lieferant):
        self.fuege_artikel_hinzu(kategorie, lagerort, name, menge, lieferant)

    def warenausgang(self, kategorie, lagerort, name, menge, kunde):
        if kategorie not in self.inventar["kategorien"]:
            print(f"Kategorie '{kategorie}' gibt's nicht.")
            return
        if lagerort not in self.inventar["kategorien"][kategorie]:
            print(f"Lagerort '{lagerort}' gibt's nicht.")
            return
        if kunde not in self.inventar["kunden"]:
            print(f"Kunde '{kunde}' gibt's nicht.")
            return

        if name in self.inventar["kategorien"][kategorie][lagerort]:
            if self.inventar["kategorien"][kategorie][lagerort][name] >= menge:
                self.inventar["kategorien"][kategorie][lagerort][name] -= menge
                if self.inventar["kategorien"][kategorie][lagerort][name] == 0:
                    del self.inventar["kategorien"][kategorie][lagerort][name]
                    if not self.inventar["kategorien"][kategorie][lagerort]:
                        del self.inventar["kategorien"][kategorie][lagerort]
                self.inventar["kunden"][kunde].append(name)
                print(f"{menge} {name}(s) an {kunde} ausgegeben aus {kategorie} bei {lagerort}.")
            else:
                print(f"Nicht genug {name} in {kategorie} bei {lagerort}.")
        else:
            print(f"{name} nicht gefunden in {kategorie} bei {lagerort}.")
        self.speichere_inventar()

    def liste_inventar_auf(self):
        if not self.inventar["kategorien"]:
            print("Inventar ist leer.")
            return

        print("Inventar:")
        for kategorie, lagerorte in self.inventar["kategorien"].items():
            print(f"Kategorie: {kategorie}")
            for lagerort, artikel in lagerorte.items():
                print(f"  Lagerort: {lagerort}")
                for name, menge in artikel.items():
                    print(f"    {name}: {menge}")
        print("Lieferanten:")
        for lieferant in self.inventar["lieferanten"]:
            print(f"  {lieferant}: {', '.join(self.inventar['lieferanten'][lieferant])}")
        print("Kunden:")
        for kunde in self.inventar["kunden"]:
            print(f"  {kunde}: {', '.join(self.inventar['kunden'][kunde])}")


class Auftragsverwaltung:
    def __init__(self, inventar):
        self.inventar = inventar

    def erstelle_auftrag(self, auftragsnummer, kunde, artikel, menge):
        if kunde not in self.inventar.inventar["kunden"]:
            print(f"Kunde '{kunde}' gibt's nicht.")
            return
        if not self.pruefe_lagerbestand(artikel, menge):
            print(f"Nicht genug {artikel} auf Lager.")
            return

        if auftragsnummer not in self.inventar.inventar["auftraege"]:
            self.inventar.inventar["auftraege"][auftragsnummer] = {
                "kunde": kunde,
                "artikel": {},
                "status": "Offen"
            }

        if artikel in self.inventar.inventar["auftraege"][auftragsnummer]["artikel"]:
            self.inventar.inventar["auftraege"][auftragsnummer]["artikel"][artikel] += menge
        else:
            self.inventar.inventar["auftraege"][auftragsnummer]["artikel"][artikel] = menge

        print(f"Auftrag {auftragsnummer} erstellt für {kunde} mit {menge} {artikel}.")
        self.inventar.speichere_inventar()

    def pruefe_lagerbestand(self, artikel, menge):
        for kategorie in self.inventar.inventar["kategorien"].values():
            for lagerort in kategorie.values():
                if artikel in lagerort:
                    if lagerort[artikel] >= menge:
                        return True
        return False

    def liste_auftraege_auf(self):
        if not self.inventar.inventar["auftraege"]:
            print("Keine Aufträge vorhanden.")
            return

        print("Aufträge:")
        for auftragsnummer, details in self.inventar.inventar["auftraege"].items():
            print(f"Auftragsnummer: {auftragsnummer}")
            print(f"  Kunde: {details['kunde']}")
            print(f"  Status: {details['status']}")
            print(f"  Artikel:")
            for artikel, menge in details["artikel"].items():
                print(f"    {artikel}: {menge}")


def main():
    inventar = Inventory()
    auftragsverwaltung = Auftragsverwaltung(inventar)

    while True:
        print("\nInventarverwaltungssystem")
        print("1. Kategorie hinzufügen")
        print("2. Lagerort hinzufügen")
        print("3. Lieferant hinzufügen")
        print("4. Kunde hinzufügen")
        print("5. Artikel hinzufügen (Waren-Eingang)")
        print("6. Artikel entfernen (Waren-Ausgang)")
        print("7. Inventar auflisten")
        print("8. Auftrag erstellen")
        print("9. Aufträge auflisten")
        print("10. Beenden")
        wahl = input("Wähle eine Option (1-10): ")

        if wahl == '1':
            kategorie = input("Kategorie: ")
            inventar.fuege_kategorie_hinzu(kategorie)
        elif wahl == '2':
            lagerort = input("Lagerort: ")
            inventar.fuege_lagerort_hinzu(lagerort)
        elif wahl == '3':
            lieferant = input("Lieferant: ")
            inventar.fuege_lieferant_hinzu(lieferant)
        elif wahl == '4':
            kunde = input("Kunde: ")
            inventar.fuege_kunde_hinzu(kunde)
        elif wahl == '5':
            kategorie = input("Kategorie: ")
            lagerort = input("Lagerort: ")
            name = input("Artikel: ")
            menge = int(input("Menge: "))
            lieferant = input("Lieferant: ")
            inventar.wareneingang(kategorie, lagerort, name, menge, lieferant)
        elif wahl == '6':
            kategorie = input("Kategorie: ")
            lagerort = input("Lagerort: ")
            name = input("Artikel: ")
            menge = int(input("Menge: "))
            kunde = input("Kunde: ")
            inventar.warenausgang(kategorie, lagerort, name, menge, kunde)
        elif wahl == '7':
            inventar.liste_inventar_auf()
        elif wahl == '8':
            auftragsnummer = input("Auftragsnummer: ")
            kunde = input("Kunde: ")
            artikel = input("Artikel: ")
            menge = int(input("Menge: "))
            auftragsverwaltung.erstelle_auftrag(auftragsnummer, kunde, artikel, menge)
        elif wahl == '9':
            auftragsverwaltung.liste_auftraege_auf()
        elif wahl == '10':
            print("Programm wird beendet...")
            break
        else:
            print("Ungültige Wahl. Bitte eine Zahl zwischen 1 und 10 eingeben.")


if __name__ == "__main__":
    main()
