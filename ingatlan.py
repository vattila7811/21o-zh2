# Feladat: Írj programot ingatlanhirdetések kezelésére!

# A hirdetések adatai az 'ingatlanok.json' fájlban vannak tárolva.
# Egy ingatlanhoz az alábbi adatok tartoznak:
# településnév (city)
# cím (address)
# ár - MFt (price)
# alapterület (area)
# szobaszám (rooms)

# A program indításkor kérdezze meg a felhasználótól, hogy új hirdetést
# szeretne feladni vagy keresni szeretne.

# Új hirdetés feladásánál kérje be az adatait és mentse bele a fájlba.
# (A megadott adatok formátumát nem kell ellenőrizni.)

# Ingatlankeresésnél kínáljon fel szűrési lehetőségeket.
# A szűrések a main()-ben vannak részletezve.
# Minden szűrés után írja ki, hány hirdetés felel meg a feltételeknek.
# Végül, a megmaradt hirdetések közül írja ki az adatait annak, amelyiknek
# a legalacsonyabb a négyzetméterenkénti ára.
# Vagy azt, hogy "Nincs a szűréseknek megfelelő hirdetés."

# A fájlból olvasás, szűrések, és a legjobb kiválasztása legyenek külön
# függvényekben implementálva. Ezt a vizsgáztató helyben fogja ellenőrizni.

import json

INGATLAN = dict[str, str | int | float ]
INGATLANOK = list[INGATLAN]

DBNEV = 'ingatlanok.json'

def load_ingatlanok() -> INGATLANOK:
    ingatlanok : INGATLANOK = []
    with open(DBNEV, "r", encoding="utf-8") as jsoinfile:
        ingatlanok =  json.load(jsoinfile)
    return ingatlanok


def save_ingatlanok(ingatlanok: INGATLANOK):
    with open(DBNEV, "w", encoding="utf-8") as jsonfile:
            json.dump(ingatlanok, jsonfile, indent=4, ensure_ascii=False)


def uj_hirdetes(ingatlanok: INGATLANOK):
    ujingatlan : INGATLAN = {}
    ujingatlan['city'] = input("Település neve: ")
    ujingatlan['address'] = input("Utca, házszám: ")
    ujingatlan['price'] = float(input("Eladási ár (MFt): "))
    ujingatlan['area'] = float(input("Alapterület: "))
    ujingatlan['rooms'] = int(input("Szobák száma: "))
    ingatlanok.append(ujingatlan)
    save_ingatlanok(ingatlanok)
    

def szurt_darab_kiir (ingatlanok: INGATLANOK):
    if len(ingatlanok) > 0:
        print(len(ingatlanok), "hirdetés felel meg a szűrési feltételeknek")
    else:
        print("Nincs a szűréseknek megfelelő hirdetés.")        


def hirdetesek_szurese(ingatlanok: INGATLANOK) -> INGATLANOK:
    szurt_ingatlanok = ingatlanok
    print(len(szurt_ingatlanok), "hirdetés van az adatbázisban")
    
    city = input("Adja meg a kívánt település nevét, vagy nyomjon Enter-t ezen szűrés kihagyásához: ")    
    if city != "":
        szurt_ingatlanok = [ingatlan for ingatlan in szurt_ingatlanok if ingatlan['city'] == city]
    szurt_darab_kiir(szurt_ingatlanok)

    if len(szurt_ingatlanok) > 0:
        minroom = input("Adja meg a kívánt minimális szobaszámot, vagy nyomjon Enter-t ezen szűrés kihagyásához: ")
        if minroom != "":
            szurt_ingatlanok = [ingatlan for ingatlan in szurt_ingatlanok if ingatlan['rooms'] >= int(minroom) ]
        szurt_darab_kiir(szurt_ingatlanok)

    if len(szurt_ingatlanok) > 0:
        maxroom = input("Adja meg a kívánt maximális szobaszámot, vagy nyomjon Enter-t ezen szűrés kihagyásához: ")
        if maxroom != "":
            szurt_ingatlanok = [ingatlan for ingatlan in szurt_ingatlanok if ingatlan['rooms'] <= int(maxroom) ]
        szurt_darab_kiir(szurt_ingatlanok)

    return szurt_ingatlanok


def keres_legjobb(ingatlanok: INGATLANOK)-> int:
    legjobb_index = -1 
    legjobb = 0.
    for i, ingatlan in enumerate(ingatlanok):
        arpernm = float(ingatlan['price'])/float(ingatlan['area'])
        if legjobb == 0. or arpernm < legjobb:
            legjobb_index = i
            legjobb = arpernm
    return legjobb_index


def kiir_legjobb(ingatlanok: INGATLANOK, legjobb_index: int):
    if legjobb_index >=0 and legjobb_index < len(ingatlanok):
        ingatlan = ingatlanok[legjobb_index]
        print("A legjobb négyzetméterenkénti árú ingatlan:")        
        print(f"Település neve: {ingatlan['city']}")
        print(f"Utca, házszám: {ingatlan['address']}")
        print(f"Eladási ár (MFt): {ingatlan['price']}")
        print(f"Alapterület: {ingatlan['area']}")
        print(f"Szobák száma: {ingatlan['rooms']}")


def menu(ingatlanok: INGATLANOK):
     while True:
        try:
            print("0: Kilépés")
            print("1: Új hirdetés feladása")
            print("2: Hirdetések szűrése")

            choice = int(input("Válasszon egy menüpontot: "))
            match choice:
                case 0:
                    break
                case 1:
                    uj_hirdetes(ingatlanok)
                case 2: 
                    szurt_ingatlanok = hirdetesek_szurese(ingatlanok)
                    legjobb_index = keres_legjobb(szurt_ingatlanok)
                    kiir_legjobb(szurt_ingatlanok, legjobb_index)
        except ValueError:
            pass


def main():
    ingatlanok = load_ingatlanok()
    menu(ingatlanok)
    

main()
