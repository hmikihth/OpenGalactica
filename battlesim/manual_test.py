#!/usr/bin/env python3

from .ship import Ship
from .fleet import Fleet
from .battle import Battle

# Ship definitions
laser_torony = Ship("Lézer lövegtorony", "Khaduuii", "Na", "Va Na All", "pvr", 20, 25, 18, 72, 12, 270, 2000, 3000, 1000)
plasma_torony = Ship("Plazma lövegtorony", "Khaduuii", "Fr", "Na Fr All", "pvr", 40, 15, 30, 63, 23, 660, 4000, 6000, 2000)
tera = Ship("Tera", "Digitrox", "Ro", "Ro Cir Csh", "standard", 650, 10, 27, 51, 34, 1872, 16500, 10500, 1800)
trojan = Ship("Trojan", "Digitrox", "Ro", "- - -", "resourcer", 1010, 0, 5, 0, 0, 1750, 10200, 10800, 1200)
haramia = Ship("Haramia", "Piraati", "Fr", "Fr - -", "thief", 420, 17, 14, 56, 29, 667, 5200, 5800, 1000)
bandita = Ship("Bandita", "Piraati", "Ro", "Ro - -", "thief", 570, 10, 41, 48, 27, 1560, 11400, 11000, 1600)
hoher = Ship("Hoher", "Piraati", "Cir", "Cir - -", "thief", 720, 5, 100, 41, 33, 3528, 25000, 20000, 3000)
argon = Ship("Argon", "Extra", "Fr", "Fr Ro All", "standard", 430, 17, 10, 58, 27, 587, 5200, 4000, 400)
kripton = Ship("Kripton", "Extra", "Ro", "Ro Cir All", "standard", 580, 10, 37, 56, 20, 1373, 10400, 8000, 800)
apaly = Ship("Apály", "Khaduii", "Na", "Na Fr -", "blocker", 285, 25, 12, 57, 34, 278, 2100, 3500, 400)
dagaly = Ship("Dagály", "Khaduii", "Na", "Fr Va All", "standard", 360, 25, 12, 61, 8, 306, 3200, 2200, 600)
villam = Ship("Villám", "Khaduii", "Fr", "Fr Ro All", "blocker", 410, 17, 15, 58, 68, 712, 3600, 6800, 1600)
cunami = Ship("Cunami", "Khaduii", "Ro", "Ro Cir All", "blocker", 560, 10, 25, 64, 94, 1657, 9400, 12200, 2400)
orveny = Ship("Örvény", "Khaduii", "Na", "- - -", "resourcer", 1050, 25, 1, 0, 0, 223, 3800, 1900, 300)
tolvaj = Ship("Tolvaj", "Piraati", "Va", "Va - -", "thief", 130, 40, 5, 74, 9, 95, 1000, 1800, 200)
zsivany = Ship("Zsivány", "Piraati", "Na", "Na - -", "thief", 320, 25, 10, 69, 13, 278, 2400, 3200, 400)
xenon = Ship("Xenon", "Extra", "Cir", "Cir Csh All", "standard", 730, 5, 53, 54, 38, 3105, 20800, 16000, 1600)
radon = Ship("Radon", "Extra", "Csh", "Csh Va All", "standard", 900, 0, 105, 61, 43, 6822, 41600, 32000, 3200)

# Fleet definitions
#vedo_flotta = Fleet("Védő Játékos 1", "wedge", 2)
vedo_flotta = Fleet("Védő Játékos 1", "wall",2)
#vedo_flotta = Fleet("Védő Játékos 1", "sphere",2)
vedo_flotta.add_ship(apaly, 219)
vedo_flotta.add_ship(dagaly, 399)
vedo_flotta.add_ship(villam, 450)
vedo_flotta.add_ship(cunami, 1247)
vedo_flotta.add_ship(kripton, 17)
vedo_flotta.add_ship(xenon, 9)
vedo_flotta.add_ship(radon, 6)

#vedo_flotta2 = Fleet("Védő Játékos 1", "wedge",3)
#vedo_flotta2 = Fleet("Védő Játékos 1", "wall",3)
vedo_flotta2 = Fleet("Védő Játékos 1", "sphere")
vedo_flotta2.add_ship(tolvaj, 1000)
vedo_flotta2.add_ship(zsivany, 2000)

#vedo_flotta.add_ship(bandita, 100)


#tamado_flotta = Fleet("Támadó Játékos 1", "wedge")
tamado_flotta = Fleet("Támadó Játékos 1", "wall")
#tamado_flotta = Fleet("Támadó Játékos 1", "sphere")
tamado_flotta.add_ship(apaly, 800)
tamado_flotta.add_ship(dagaly, 800)
tamado_flotta.add_ship(villam, 542)
tamado_flotta.add_ship(orveny, 400)

#tamado_flotta2 = Fleet("Támadó Játékos 1", "wedge")
#tamado_flotta2 = Fleet("Támadó Játékos 1", "wall")
tamado_flotta2 = Fleet("Támadó Játékos 1", "sphere")
tamado_flotta2.add_ship(tera, 43)
tamado_flotta2.add_ship(trojan, 46)

#tamado_flotta.add_ship(bandita, 100)


# Battle
battle = Battle([tamado_flotta, tamado_flotta2], [vedo_flotta, vedo_flotta2])
battle.battle()
battle.print_battle_report()
