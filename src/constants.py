import os

TERMINAL_LENGTH = 120  # 120 col terminal
PATH_TO_SPELL_LIST = os.path.expanduser("../assets/spells.json")
PATH_TO_ITEM_LIST = os.path.expanduser("../assets/ItemList")

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

SUBSHELL_COMBAT_MESSAGES = {
    "shell_enter": "You're in combat!"
}

KNOWN_COMMANDS = ["buy", "sell", ""]

COMBAT_COMMANDS = ["help", "h", "?",
                   "spell", "s",
                   "move", "m",
                   "st",
                   "d",
                   ]

COMBAT_HELP = "The commands possible are:\nhelp/h : get help\nspell/s <spell " \
              "name> : looks up the spell in the known spellbase and prints " \
              "it. If no argument is specified, prints known spells.\nmove/m " \
              "<movement distance> : subtracts the distance from your total " \
              "movement speed.\nd <amount> : take <amount> damage.\nst <STAT> " \
              ": make a savin throw for a given stat.\n"


def getPlayerClasses():
    return PLAYER_CLASSES


def getPlayerRacesVanilla():
    return PLAYER_RACES_VANILLA


def getPlayerRacesUnearthedArcana():
    return PLAYER_RACES_UNEARTHED_ARCANA


def getAllRaces():
    return PLAYER_RACES_VANILLA + PLAYER_RACES_UNEARTHED_ARCANA
