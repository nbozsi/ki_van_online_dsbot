import re
import json


def txt2dict(file_nev, nev, json_paros="paros_het.json", json_paratlan="paratlan_het.json"):
    with open(file_nev, 'r', encoding="utf-8") as file:
        egesz = file.read()
    sorok = egesz.split("\n")

    with open(json_paros, 'r') as f:  # json beolvasása d_paros-ba
        d_paros = json.load(f)
    with open(json_paratlan, 'r') as f:  # json beolvasás d_paratlan-ba
        d_paratlan = json.load(f)
    # sorok=file.readlines()
    # d={Boldi:{  Hetfo:  {(480,600) ,  (720,840)}  , Kedd:{(vmi,vmi),(vmi,vmi)} } ,  Erik:{ Hetfo:  ((vmi,vmi),(vmi,vmi)) , Kedd: ((vmi,vmi)...)}  }
    # Hétfő - 8:00 - 10:00    Óra    Komplex függvénytanE-a (kompft1a0_m17ea) - 1 () Minden hét (Sigray István) (0-820 Hunfalvy János terem (LD-0-820))    0-820 Hunfalvy János terem (LD-0-820)
    napok2 = ["Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek"]
    d_paratlan[nev] = {nap: [] for nap in napok2}
    d_paros[nev] = {nap: [] for nap in napok2}
    for sor in sorok[1:]:
        data = re.search(
            '(Hétfő|Kedd|Szerda|Csütörtök|Péntek) - (\d{1,2}):(\d\d) - (\d{1,2}):(\d\d).*(Minden|Páratlan|Páros) hét', sor).groups()
        match data[5]:
            case "Minden":
                d_paratlan[nev][data[0]].append(
                    (int(data[1])*60+int(data[2]), int(data[3])*60+int(data[4])))
                d_paros[nev][data[0]].append(
                    (int(data[1])*60+int(data[2]), int(data[3])*60+int(data[4])))
            case "Páratlan":
                d_paratlan[nev][data[0]].append(
                    (int(data[1])*60+int(data[2]), int(data[3])*60+int(data[4])))
            case "Páros":
                d_paros[nev][data[0]].append(
                    (int(data[1])*60+int(data[2]), int(data[3])*60+int(data[4])))
    print(d_paratlan, d_paros)
    with open(json_paros, 'w') as f:
        json.dump(d_paros, f)
    with open(json_paratlan, 'w') as f:
        json.dump(d_paratlan, f)
    print("adatok sikeresn hozzáadva")


if __name__ == "__main__":  # ez csak akkor fut ha önmagában ezt a scriptet futtatod, ha a másik hívja meg, akkor nem
    txt2dict("nbozsi4#2098.txt", "nbozsi4#2098")
