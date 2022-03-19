import re
import json
import datetime
import os
from os.path import dirname, abspath

data_dirname = os.path.join(dirname(dirname(abspath(__file__))), 'data')


def txt2dict(file_nev, nev, json_paros="paros_het.json", json_paratlan="paratlan_het.json"):
    with open(file_nev, 'r', encoding="utf-8") as file:
        egesz = file.read()
    sorok = egesz.split("\n")

    with open(os.path.join(data_dirname, json_paros), 'r') as f:  # json beolvasása d_paros-ba
        d_paros = json.load(f)
    with open(os.path.join(data_dirname, json_paratlan), 'r') as f:  # json beolvasás d_paratlan-ba
        d_paratlan = json.load(f)
    # sorok=file.readlines()
    # d={Boldi:{  Hetfo:  {(480,600) ,  (720,840)}  , Kedd:{(vmi,vmi),(vmi,vmi)} } ,  Erik:{ Hetfo:  ((vmi,vmi),(vmi,vmi)) , Kedd: ((vmi,vmi)...)}  }
    # Hétfő - 8:00 - 10:00    Óra    Komplex függvénytanE-a (kompft1a0_m17ea) - 1 () Minden hét (Sigray István) (0-820 Hunfalvy János terem (LD-0-820))    0-820 Hunfalvy János terem (LD-0-820)
    napok = {"Hétfő": 0, "Kedd": 1, "Szerda": 2, "Csütörtök": 3,
             "Péntek": 4, "Szombat": 5, "Vasárnap": 6}
    d_paratlan[nev] = {nap: [] for nap in range(7)}  # H=0, K=1, .... V=6
    d_paros[nev] = {nap: [] for nap in range(7)}
    for sor in sorok[1:]:
        data = re.search(
            '(Hétfő|Kedd|Szerda|Csütörtök|Péntek) - (\d{1,2}):(\d\d) - (\d{1,2}):(\d\d).*(Minden|Páratlan|Páros) hét', sor).groups()
        match data[5]:
            case "Minden":
                d_paratlan[nev][napok[data[0]]].append(
                    (int(data[1])*60+int(data[2]), int(data[3])*60+int(data[4])))
                d_paros[nev][napok[data[0]]].append(
                    (int(data[1])*60+int(data[2]), int(data[3])*60+int(data[4])))
            case "Páratlan":
                d_paratlan[nev][napok[data[0]]].append(
                    (int(data[1])*60+int(data[2]), int(data[3])*60+int(data[4])))
            case "Páros":
                d_paros[nev][napok[data[0]]].append(
                    (int(data[1])*60+int(data[2]), int(data[3])*60+int(data[4])))
    with open(os.path.join(data_dirname, json_paros), 'w') as f:  # JSON-ben minden kulcs STRING!!!
        json.dump(d_paros, f)
    with open(os.path.join(data_dirname, json_paratlan), 'w') as f:
        json.dump(d_paratlan, f)
    print("adatok sikeresn hozzáadva")


def kategoriak(tagok, json_paros="paros_het.json", json_paratlan="paratlan_het.json"):
    most = datetime.datetime.now()  # vasárnaptól kezdi a számozást a datetime
    ma = str((int(most.strftime("%w"))-1) % 7)
    perc = most.hour*60+most.minute
    p = []
    s = []
    z = []
    if int(most.strftime("%W")) % 2 == 0:
        with open(os.path.join(data_dirname, json_paros), 'r') as f:
            d = json.load(f)
    else:
        with open(os.path.join(data_dirname, json_paratlan), 'r') as f:
            d = json.load(f)
    for tag in tagok:
        nick = f"{tag.name}#{tag.discriminator}"
        foglalt, oraja_lesz = False, False
        if nick in d:
            for kezdes, veg in d[nick][ma]:
                if kezdes < perc and perc < veg:
                    p.append(tag.name)
                    foglalt = True
                elif kezdes < perc+60 and perc < veg:
                    oraja_lesz = True
            if (not foglalt) and oraja_lesz:
                s.append(tag.name)
            elif (not foglalt) and (not oraja_lesz):
                z.append(tag.name)
    return (z, s, p)
