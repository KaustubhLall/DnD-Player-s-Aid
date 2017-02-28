# this dict stores a list of all known items with their name as the key
itemManifest = {}


class Player:
    """
    This class is the main class that defines a player and tracks their
    progress.
    """
    # Player Constants Go Here #
    ############################
    # Note about alignments: -1 = unlawful/evil, 0 = neutral, 1 = lawful/good
    name = ""  # actual name of player
    playerName = ""  # name of character in game
    playerAlignment = (None, None)
    playerRace = ""
    playerClass = ""
    # these will be implemented later TODO
    personalityTraits = ""
    playerBonds = ""
    playerIdeals = ""
    playerFlaws = ""
    playerBackground = ""

    # Player Variables Go After Here #
    ##################################

    attributes = {
        "STR": 0,
        "DEX": 0,
        "CON": 0,
        "INT": 0,
        "WIS": 0,
        "CHA": 0,
    }

    attributeModifiers = {
        "STR": 0,
        "DEX": 0,
        "CON": 0,
        "INT": 0,
        "WIS": 0,
        "CHA": 0,
    }

    # Player proficiencies and expertise.
    # Dict format: "skill": (parentStat, isProficient, isExpert)
    # Note: All skills are lowercase
    skills = {
        "athletics"      : ("STR", False, False),
        "acrobatics"     : ("DEX", False, False),
        "sleight of hand": ("DEX", False, False),
        "stealth"        : ("DEX", False, False),
        "animal handling": ("WIS", False, False),
        "insight"        : ("WIS", False, False),
        "medicine"       : ("WIS", False, False),
        "perception"     : ("WIS", False, False),
        "survival"       : ("WIS", False, False),
        "arcana"         : ("INT", False, False),
        "history"        : ("INT", False, False),
        "investigation"  : ("INT", False, False),
        "nature"         : ("INT", False, False),
        "religion"       : ("INT", False, False),
        "deception"      : ("CHA", False, False),
        "intimidation"   : ("CHA", False, False),
        "performance"    : ("CHA", False, False),
        "persuasion"     : ("CHA", False, False),
    }

    playerInspiration = False
    playerAC = 0
    playerInitiative = 0
    playerSpeed = 0
    playerPassivePerception = 0
    playerHP = 0
    playerMaxHP = 0
    playerTempHP = 0
    playerHitDieType = 0
    playerHitDieTotal = 0
    playerHitDieRemaining = 0
    playerUnconscious = False
    playerDeathFails = 0
    playerDeathSuccesses = 0
    playerStable = True

    # setter/getter methods for constants
    def setActualPlayerName(self, name):
        self.name = name

    def setCharacterName(self, charName):
        self.playerName = charName

    def setPlayerAlignment(self, alignment):
        if len(alignment) != 2 or not isinstance(alignment, tuple):
            raise InvalidArgument("Alignment should be a tuple (law, moral)")
        self.playerAlignment = alignment

    def setPlayerRace(self, race):
        # TODO change attributes
        # TODO throw exception if race not found
        self.playerRace = race

    def setPlayerClass(self, playerClass):
        # TODO Throw exception if player class not found
        self.playerClass = playerClass

    def initializePlayer(self):
        """This method initializes the player from scratch and loads all
        relevant information"""
        affirmative = ["yes", "y"]
        affirmation = "y"  # this character tracks the user's input.
        response = ""

        o = PlayerInterface()
        o.out("Halt! Who goes there ... ? Identify yourself!")
        response = o.readRaw("I said, identify yourself! Enter name: ")
        affirmation = o.read("%s you said, did I hear that right? (y/n) "
                             % response)

        while affirmation not in affirmative:
            response = o.read(
                "No? What is it then. Out with it! Enter name: ")
            affirmation = o.read("%s, did I hear you right this time? ("
                                 "y/n)" % response)

        o.out("Well, I must say, it's a pleasure to make your acquaintance.")
        o.out("Who am I, you ask? Well. Nobody really knows who I am. If you "
              "must know, I have been hired to aid the young adventurer who "
              "goes by the name of %s.")


class PlayerInterface:
    """This class serves as an interface between the player and the program."""

    def out(self, message):
        print(message)

    def read(self, message):
        """
        Prompts the user for input with the given message and returns the
        string as lowercase.
        :param message: prompt message.
        :return: Player input as lowercase.
        """
        userResponse = input(message)

        if len(userResponse) == 0:
            userResponse = input(message)

        return userResponse.lower()

    def readRaw(self, message):
        """
        Prompts the user for input with the given message and returns the
        string as-is.
        :param message: prompt message.
        :return: Player input.
        """
        userResponse = input(message)
        if len(userResponse) == 0:
            userResponse = input(message)
        return userResponse


class Item:
    """Defines an item object. The item typically will have a name, value,
    weight and possibly a list of tags or related info."""

    itemName = ""
    itemValue = ""
    itemWeight = 0
    itemInfo = []

    def __init__(self, itemName, itemValue, itemWeight, itemInfo):
        """Constructor for the class.

        :param itemName: Name of the item.
        :param itemValue: String that contains the numeric value of an item
        followed by its denomination. Ex: 5g is 5 gold, or 20s is 20 silver.
        :param itemWeight: Float that contains the item value in lb.
        :param itemInfo: List of associated tags of the item, usually empty.
        """
        self.itemName = itemName
        self.itemInfo = itemInfo
        self.itemValue = itemValue
        self.itemWeight = itemWeight

    def __repr__(self):
        """
        Streing representation of the object.
        :return: String s that contains all the object data.
        """
        s = ""
        s += "This is (a) %s worth %s. The %s weighs %0.1f lb." % \
             (self.itemName, self.itemValue, self.itemName, self.itemWeight)

        if (self.itemInfo != []):
            s += "Also, the item has the following special properties: " + \
                 str(self.itemInfo)

        return s

    @staticmethod
    def loadItemManifest(fname):
        """
        Loads the items and information from the manifest into a dict.
        :param fname: File containing information about different objects.
        :return: Dictionary with key-value store of itemName and item.
        """
        manifest = {}
        file = open(fname)

        for line in file:
            line = line.strip()
            itemName = ""
            itemValue = ""
            itemWeight = 0
            itemInfo = []

            # skip the line if it is empty or starts with #
            if not line.startswith("#"):
                args = line.split(" ")
                # check that atleast 3 arguments are passed in, else skip the
                # line
                if len(args) > 2:
                    # parse iteminfo for spaces
                    # DEBUG: possible bug if "_" character isnt removed.
                    itemName = args[0]
                    itemName = " ".join(itemName.split("_"))

                    # parse itemValue to see if the denomination is specified
                    itemValue = args[1]
                    if itemValue[-1] not in ['g', 's', 'c']:
                        itemValue += 'g'

                    # parse itemWeight
                    itemWeight = float(args[2])

                    # if there is any item info associated, add it.
                    if len(args) > 3:
                        itemInfo = args[3:]
                        for elem in itemInfo:
                            elem = " ".join(elem.split("_"))

                    # finally, make a new item object and store it in the
                    # item manifest with its name as key and item object as
                    # value

                    item = Item(itemName, itemValue, itemWeight, itemInfo)
                    manifest[itemName] = item

        # Close file when its no longer needed
        file.close()
        return manifest


class InvalidArgument(Exception):
    """Raises an exception if an invalid input is supplied"""

    def __init__(self, message):
        self.message = message


# test code
# itemManifest = Item.loadItemManifest("ItemList")
# print(itemManifest)

player = Player()
player.initializePlayer()
