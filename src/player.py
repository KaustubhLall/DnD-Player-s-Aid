# this dict stores a list of all known items with their name as the key
import os
import platform
import subprocess
from datetime import time
import json

itemManifest = {}
import src.constants as CONST
from src.playerinterface import *


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

    # Stores saving throws in the format KEY = (value, isProficient, isExpert)
    savingThrows = {
        "STR": [0, False],
        "DEX": [0, False],
        "CON": [0, False],
        "WIS": [0, False],
        "INT": [0, False],
        "CHA": [0, False],
    }

    # Player proficiencies and expertise.
    # Dict format: "skill": (value, parentStat, isProficient, isExpert)
    # Note: All skills are lowercase
    skills = {
        "athletics"      : [0, "STR", False, False],
        "acrobatics"     : [0, "DEX", False, False],
        "sleight of hand": [0, "DEX", False, False],
        "stealth"        : [0, "DEX", False, False],
        "animal handling": [0, "WIS", False, False],
        "insight"        : [0, "WIS", False, False],
        "medicine"       : [0, "WIS", False, False],
        "perception"     : [0, "WIS", False, False],
        "survival"       : [0, "WIS", False, False],
        "arcana"         : [0, "INT", False, False],
        "history"        : [0, "INT", False, False],
        "investigation"  : [0, "INT", False, False],
        "nature"         : [0, "INT", False, False],
        "religion"       : [0, "INT", False, False],
        "deception"      : [0, "CHA", False, False],
        "intimidation"   : [0, "CHA", False, False],
        "performance"    : [0, "CHA", False, False],
        "persuasion"     : [0, "CHA", False, False],
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

    def calculateAttributeModifiers(self):
        """Recalculates attribute modifiers based on attributes."""
        for mod in self.attributeModifiers:
            self.attributeModifiers[mod] = int((self.attributes[mod]) - 10) / 2

    def calculateSkills(self):
        """Calculates skills based on attributes, proficiencies and
        expertise"""
        for skill in self.skills:
            ability = self.skills[skill][1]

            if self.skills[skill][3]:
                self.skills[skill][0] = self.attributeModifiers[ability] + 4

            elif self.skills[skill][2]:
                self.skills[skill][0] = self.attributeModifiers[ability] + 2

            else:
                self.skills[skill][0] = self.attributeModifiers[ability]

    def calculateSavingThrows(self):
        """Calculates saving throws based on attributes, proficiencies and
        expertise"""
        for st in self.savingThrows:
            mod = 0
            if self.savingThrows[st][1]:
                mod = 2
            self.savingThrows[st][0] = self.attributeModifiers[st] + mod

    def initializePlayer(self):
        """This method initializes the player from scratch and loads all
        relevant information"""
        affirmatives = ["yes", "y"]
        affirmation = "y"  # this character tracks the user's input.
        response = ""

        o = PlayerInterface()
        # start basic introduction
        o.next("Introduction")

        o.out("Halt! Who goes there ... ? Identify yourself!")
        response = o.readRaw("I said, identify yourself! Enter name: ")
        affirmation = o.read("%s you said, did I hear that right? (y/n) "
                             % response)

        while affirmation not in affirmatives:
            response = o.readRaw(
                "No? What is it then. Out with it! Enter name: ")
            affirmation = o.read("%s, did I hear you right this time? ("
                                 "y/n) : " % response)
        self.setCharacterName(response)
        response = ""

        o.out("Well, I must say, it's a pleasure to make your acquaintance.")
        o.out("Who am I, you ask? Well. Nobody really knows who I am. If you "
              "must know, I have been hired to aid the young adventurer who "
              "goes by the name of %s." % self.playerName)

        o.out("In order to help you, I must pick up a few things about you. "
              "Im afraid i wasn't briefed all that well.")
        response = o.read("In this day and age, it isn't proper to assume "
                          "one's race, now is it? So tell me, what race is it "
                          "that you identify with? Enter race: ")
        response = str(response).title().replace("-", " ")
        while response not in CONST.getAllRaces():
            response = o.read(
                "Now there, don't toy with me. %s is clearly not a recognized "
                "race, tell me your real race. Enter race: " % response)
            response = str(response).title().replace("-", " ")

        affirmation = o.read("So then, you're sure you're a %s? (y/n)" %
                             response)

        while affirmation not in affirmatives:
            response = o.read("Well, out with it. What race are you? Enter "
                              "race: ")
            response = str(response).title().replace("-", " ")

            while response not in CONST.getAllRaces():
                response = o.read("Well, out with it. What race are you? Enter "
                                  "race: ")
                response = str(response).title().replace("-", " ")

            affirmation = o.read("So then, you're sure you're a %s? (y/n)" %
                                 response)

        self.playerRace = response

        while response not in CONST.getPlayerClasses():
            response = o.read("Be more specific, you're a %s, but what class? "
                              "Enter class (do not indicate specialized "
                              "classes): " % self.playerRace)
            response = str(response).capitalize()
        self.playerClass = response

        # calculate proficiency bonus
        o.next("Attributes")
        response = o.read("Oh my, a %s %s. You must be very proficient. What "
                          "is your "
                          "proficiency bonus? Enter proficiency bonus: " % (
                              self.playerRace, self.playerClass))
        while True:
            try:
                prof = int(response)
                o.out("Great! Your proficiency bonus is: %+d" % prof)
                break
            except:
                response = o.read("Enter a valid bonus please: ")

        o.out("Oh my. Thats mighty proficient of you!")

        o.out("So, tell me more about your stats.")
        for stat in self.attributes:
            response = o.read(
                "Tell me about your " + stat + ". Enter your " +
                stat + ": ")
            while True:
                try:
                    value = int(response)
                    while value > 20 or value < 1:
                        response = o.read("Come, then, be realistic. What is "
                                          "your %s? Enter stat: " % stat)
                        value = int(response)

                    self.attributes[stat] = value
                    o.out("Great, your %s is %s!" % (stat, value))
                    break

                except:
                    response = o.read("Your " + stat + ". What is it? Enter "
                                                       "stat: ")

        # Calculate modifiers
        for mod in self.attributeModifiers:
            self.attributeModifiers[mod] = int((self.attributes[mod]) - 10) / 2

        o.next("Player Attributes")
        o.out("Great, so your attributes are: ")
        for att in self.attributes:
            o.out("  + %s : %2d (%+d)" % (att, self.attributes[att],
                                          self.attributeModifiers[att]))

        o.out("")

        # ask for saving throw proficiencies
        response = o.read("So, what saving throws are you proficient in? "
                          "Enter proficient saving throws (ex: STR, CON): ")

        # Process proficiencies and expertise
        response = str(response).split(",")
        for word in response:
            ban = ""  # any banned word is stored here
            # Format word
            word = word.strip().upper()
            if len(word) > 3:
                word = word[:3]
            # check against dictionary
            while word not in self.savingThrows:
                word = o.read("Looks like %s isn't a valid saving "
                              "throw. Try again (enter n to cancel): "
                              "" % word)
                word = word.upper().strip()
                if word == "N" or word == "n":
                    ban = word
                    break
            if word != ban:
                self.savingThrows[word][1] = True

        # Calculate the player's saving throws
        self.calculateSavingThrows()

        # display the saving throws
        o.out("\nYour saving throws are:")
        for throw in self.savingThrows:
            ch = "_"
            mod = 0
            if self.savingThrows[throw][1]:
                ch = "p"
                mod = 2
            o.out("%+d (%s) : %s" % (self.savingThrows[throw][0], ch, throw))

        # move into skills
        o.next("Skills")
        affirmation = o.read("Do you have expertise in any skills? (y/n)")
        if affirmation in affirmatives:
            # handle expertise for skills
            response = o.read(
                "So what skills do you have expertise in? Enter skills as "
                "acrobatics, athletics, persuasion ... :")
            response = str(response).split(",")
            ban = ""
            for word in response:
                # parse the responses
                word = word.strip()
                while word not in self.skills:
                    word = o.read("Sorry, I couldn't quite understand which "
                                  "skill you meant by %s. Could you tell me "
                                  "once more (enter n if wrong output is "
                                  "shown): " % word)
                    if word == "n":
                        ban = word
                        break

                    word = word.strip()
                if word != ban:
                    self.skills[word][3] = True

        affirmation = o.read("\nDo you have proficiencies in any skills? (y/n)")
        if affirmation in affirmatives:
            # handle proficiencies for skills
            response = o.read(
                "So what skills do you have proficiency in? Enter skills as "
                "acrobatics, athletics, persuasion ... :")
            response = str(response).split(",")
            ban = ""
            for word in response:
                word = word.strip()
                # parse the responses
                while word not in self.skills:
                    word = o.read("Sorry, I couldn't quite understand which "
                                  "skill you meant by %s. Could you tell me "
                                  "once more (enter n if wrong output is "
                                  "shown): " % word)
                    if word == "n":
                        ban = word
                        break

                    word = word.strip()
                if word != ban:
                    self.skills[word][2] = True

        # Calculate the player's skill checks
        self.calculateSkills()
        o.out("\nYour skills are: ")
        for skill in sorted(self.skills):
            ch = "_"  # no proficiency or expertise
            if self.skills[skill][3]:
                ch = "e"  # expertise
            if self.skills[skill][2]:
                ch = "p"  # proficiency
            o.out(" %+d (%s) : %s (%s)" % (self.skills[skill][0], ch,
                                           str(skill).title(),
                                           self.skills[skill][1]))

        o.next("HP and hit dice.")

    def save(self):
        """Saves player information as json file"""
        d = {}
        for attr in dir(self):
            if not attr.startswith('__') and not callable(getattr(self, attr)):
                d[attr] = getattr(self, attr)

        print(d)
        with open('result.json', 'w') as fp:
            json.dump(d, fp)

    def printStatus(self):
        """
        Prints the current status of the player.
        :return: status string
        """
        return "Implementing player status."

    @staticmethod
    def load(filename):
        json_file = open(filename)
        json_str = json_file.read()
        d = json.loads(json_str)
        return d

    def startNewRound(self):
        print("New Round Started.")

    def damage(self, dmg):
        """
        Subtracts from playerHP.
        :param dmg: amount to substract.
        :return: True if player is alive, False if unconscious.
        """
        self.playerHP -= dmg

        return self.playerHP > 0


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
def test():
    player = Player()
    player.initializePlayer()
    player.save()
    print(Player.load("result.json"))
