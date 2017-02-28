PLAYER_RACES_VANILLA = [
    "Dragonborn",
    "Dwarf",
    "Elf",
    "Gnome",
    "Half Elf",
    "Half Orc",
    "Halfling",
    "Human",
    "Tiefling",
]

PLAYER_RACES_UNEARTHED_ARCANA = [
    ""
]

PLAYER_CLASSES = ["Paladin",
                  "Druid",
                  "Monk",
                  "Rogue",
                  "Bard",
                  "Warlock",
                  "Wizard",
                  "Sorcerer",
                  "Fighter",
                  "Ranger",
                  "Barbarian",
                  "Cleric",
                  ]


def getPlayerClasses():
    return PLAYER_CLASSES


def getPlayerRacesVanilla():
    return PLAYER_RACES_VANILLA


def getPlayerRacesUnearthedArcana():
    return PLAYER_RACES_UNEARTHED_ARCANA


def getAllRaces():
    return PLAYER_RACES_VANILLA + PLAYER_RACES_UNEARTHED_ARCANA
