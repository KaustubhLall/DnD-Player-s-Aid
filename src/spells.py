import src.constants as CONST
import json
from pprint import pprint


class SpellBook:
    """Defines a spellbook that a player can maintain."""

    # stores all the known spells in a spell object
    spellList = {}

    def __init__(self):
        """
        Sets up an object of this class.
        """
        self.spellList = self.populateSpellList(CONST.PATH_TO_SPELL_LIST)

    def searchList(self, s):
        """
        Searches the known spellist for spells that might match s and returns
        a list of all possible hits.
        :param s: Spell to search for.
        :return: list of spells found with the name.
        """
        s = str(s)
        s = s.title()

        # TODO

    def populateSpellList(self, fname):
        """
        Populates the spell list from the given file.
        :param fname: file to populate from.
        :return: spellList
        """
        # the spells is added with the following pattern:
        # "spellname" : correspondingSpellObject (see __init__ method for the
        #  Spell class) @Ahan TODO

        spells = {}
        f = open(fname, encoding="utf8")
        stringData = ""

        for line in f:
            stringData += line

        data = json.loads(stringData)
        for key in sorted(data):
            print(key)

        return spells


class Spell:
    """Stores information about one spell."""
    # spell fields
    name = ""
    castingTime = ""
    components = ""
    description = ""
    range = ""
    duration = ""
    school = ""
    level = "0"

    def __init__(self, name, level, castingTime, components, description,
                 range, duration, school):
        """
        Constructor for the class.
        :param name: name of the spell.
        :param level: spell level.
        :param castingTime: Time taked to case the spell.
        :param components: V, S, M (... ) components of the spell.
        :param description: Spell description.
        :param range: Range that the spell works for.
        :param duration: Duration of the spell.
        :param school: School that the spell belongs to.
        """
        # parse name
        self.name = str(name).title()

        # parse level
        level = int(level)
        if level == 0:
            self.level = "Cantrip"
        elif level == 1:
            self.level = "1st Level"
        elif level == 2:
            self.level = "2nd Level"
        else:
            self.level = str(level) + "th Level"

        # parse casting time
        self.castingTime = castingTime

        self.components = components

        self.description = description

        self.range = range

        self.duration = duration

        self.school = school

    def __repr__(self):
        """String representation of the spell"""
        s = ""
        s += self.name.title() + "\n"
        s += self.castingTime + " " + self.level + "\n"
        s += "Casting time: %s\n" % self.castingTime
        s += "Range: %s\n" % self.range
        s += "Duration: %s\n" % self.duration
        s += self.description

        return s


s = SpellBook()
