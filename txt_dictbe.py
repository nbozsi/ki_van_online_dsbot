import re
import json


def txt2dict(file_nev, nev, json_paros="paros_het.json", json_paratlan="paratlan_het.json"):
    with open(file_nev, 'r', encoding="utf-8") as file:
        egesz = file.read()
    sorok = egesz.split("\n")

    # sorok=file.readlines()
    # d={Boldi:{  Hetfo:  {(480,600) ,  (720,840)}  , Kedd:{(vmi,vmi),(vmi,vmi)} } ,  Erik:{ Hetfo:  ((vmi,vmi),(vmi,vmi)) , Kedd: ((vmi,vmi)...)}  }
    # Hétfő - 8:00 - 10:00    Óra    Komplex függvénytanE-a (kompft1a0_m17ea) - 1 () Minden hét (Sigray István) (0-820 Hunfalvy János terem (LD-0-820))    0-820 Hunfalvy János terem (LD-0-820)

    # paratlan és paros dictionary elkészítése

    d_paratlan = {"Hétfő": {}, "Kedd": {},
                  "Szerda": {}, "Csütörtök": {}, "Péntek": {}}
    d_paros = {"Hétfő": {}, "Kedd": {},
               "Szerda": {}, "Csütörtök": {}, "Péntek": {}}

    # !Ha nincs órája aznap

    napok = {"Hétfő": 0, "Kedd": 1, "Szerda": 2, "Csütörtök": 3, "Péntek": 4}
    napok2 = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"]

    paratlan_het = [[], [], [], [], []]
    paros_het = [[], [], [], [], []]

    for i in range(1, len(sorok)):

        paritas = re.search("(Páratlan|Páros|Minden) hét",
                            sorok[i])  # milyen héten

        szetszedett = sorok[i].split("\t")

        nap = szetszedett[0]  # melyik nap

        kezdet = szetszedett[2]
        veg = szetszedett[4]
        kezdet_szet = kezdet.split(":")
        veg_szet = veg.split(":")

        # óra kezdete (óra*60)+perc
        kezdetido = int(kezdet_szet[0])*60+int(kezdet_szet[1])
        vegido = int(veg_szet[0])*60+int(veg_szet[1])  # óra vége (óra*60)+perc

        idopont = (kezdetido, vegido)  # óra időpontja
        if paritas == "Páratlan" or paritas == "Minden":
            paratlan_het[napok[nap].append(idopont)]
        if paritas == "Páros" or paritas == "Minden":
            # paros_het=[[(400,800),(600,900)],[(300,500),(1000,1200)], [] , [] , [] ]
            paros_het[napok[nap].append(idopont)]

    for nap in napok2:
        betolt_set_paratlan = set(paratlan_het[i])
        betolt_set_paros = set(paros_het[i])

        d_paratlan[nap] = betolt_set_paratlan
        d_paros[nap] = betolt_set_paros
    print(d_paratlan, d_paros)


###  d1={nev : d_paratlan}
###  d2={nev : d_paros}
if __name__ == "__main__":  # ez csak akkor fut ha önmagában ezt a scriptet futtatod, ha a másik hívja meg, akkor nem
    txt2dict("nbozsi4#2098.txt", "nbozsi4#2098")
