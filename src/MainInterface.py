import cmd
import src.display
import src.player as Player

player = Player.Player()


class CombatShell(cmd.Cmd):
    """
    Handles one instance of combat.
    """
    aliases = {}
    disp = src.display.Display(player)

    ###############################
    # Shell Setup                 #
    ###############################
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.aliases = {
            'd'   : self.do_damage,
            'e'   : self.do_exit,
            'q'   : self.do_exit,
            'quit': self.do_exit,
            'm'   : self.do_move,
            'st'  : self.do_status,
        }

    def preloop(self):
        """
        Preloop
        :return:
        """
        # player.load('result.json')
        print("The pre-loop setup entered successfully.")

    def postloop(self):
        """
        Postloop.
        :return:
        """
        # player.save()
        print("The postloop cleanup happened.")

    def default(self, line):
        """
        Handles aliasing.
        :param args:
        :return:
        """
        cmd, arg, line = self.parseline(line)
        if cmd in self.aliases:
            self.aliases[cmd](arg)
        else:
            print("*** Unknown syntax: %s" % line)

    #########################
    # Help Messages         #
    #########################

    def help_damage(self):
        print("Applies damage to the user. Usage: d/damage <amount_in_numbers>")

    ##############################
    # Methods for Commands       #
    ##############################

    def do_tempHP(self, args):
        """
        Adds temporary HP to the player.
        :param args: amount to add
        :return:
        """
        amount = 0
        try:
            amount = int(args)
        except ValueError:
            print("Usage: tempHP <tempHP_to_add>")

        player.playerTempHP = amount

    def do_heal(self, args):
        """
        Heals the player for a certain amount.
        :param args:
        :return:
        """
        args = args.split(" ")
        heal_amount = 0

        # try parsing the heal amount
        try:
            heal_amount = int(args[0])
        except ValueError:
            print("Usage: heal <amount>")
            return False

        # do the things
        player.heal(heal_amount)

    def do_damage(self, args):
        """
        Hurts the player.
        :param args: damage
        :return: True if valid.
        """
        # Check valid #
        args = args.split(" ")
        # print("Args: %s." % args)
        if len(args) == 0:
            print("Usage: d/damage <amount_in_numbers>")
            return False

        dmg = -1
        try:
            dmg = int(args[0])
        except ValueError:
            print("Usage: d/damage <amount_in_numbers>")
            return False

        # apply damage #
        alive = player.damage(dmg)
        print("You just took %d points of damage!" % dmg)

        if not alive:
            print("You just fell unconscious!")

    def do_spell(self, args):
        """
        Looks up a spell in the database and prints it out.
        :param args: SpellName to search for.
        :return:
        """
        spell = None
        # Todo searching and shit
        pass

    def do_move(self, args):
        """
        Moves the player specified amount.
        :param args: feet to move.
        :return:
        """
        amount = 0
        try:
            amount = int(args)
        except:
            print("Usage: move <amount in feet>")
            return
        player.move(amount)

    def do_status(self, args):
        print(self.disp.quickDisplay())

    def do_exit(self, args):
        """
        Exits the combat shell.
        :param args: arguments passed, irrelevant.
        :return: True.
        """
        return True


class MainShell(cmd.Cmd):
    """
    This is the main shell that the player interacts with. It enters into different modes like combat with an
    instance of the combat shell, etc.
    """
    combat_shell = None
    aliases = {}

    def __init__(self):
        """
        Initliazes object and superclass, as well as sets up a list of aliases.
        """
        # Call superclass ctor
        cmd.Cmd.__init__(self)

        # Create alias dict
        self.aliases = {
            'c'   : self.do_combat,
            'q'   : self.do_exit,
            'e'   : self.do_exit,
            'quit': self.do_exit

        }

    #####################################
    # Handle Console Stuff Here         #
    #####################################

    def preloop(self):
        """
        Executed before the main interface begins. Do introduction and player load/save here.
        :return:
        """
        # TODO load player object here
        print("Welcome to DnD Tool!")

    def postloop(self):
        """
        Exceuted when the shell loop finishes. Do autosave and exit message here.
        :return:
        """
        # TODO session statistics.
        # TODO Exit shell succesfully
        pass

    ####################################
    # Handle aliases here              #
    ####################################

    def default(self, line):
        """
        Handles aliases.
        :param line: lines to parse.
        :return: N/A
        """
        cmd, arg, line = self.parseline(line)
        if cmd in self.aliases:
            self.aliases[cmd](arg)
        else:
            print("*** Unknown syntax: %s" % line)

    ########################################
    # Handle Other Shell Interactions Here #
    ########################################

    def do_exit(self, args):
        """
        End session and save the data.
        :return: True.
        """
        # TODO Save player data
        # TODO Exit
        exit("Bye-bye!")
        pass

    def do_combat(self, args):
        """
        Enters the combat shell.
        :param args: Arguments to be passed in.
        :return: True.
        """
        self.combat_shell = CombatShell()
        self.combat_shell.prompt = "(Combat) >> "
        self.combat_shell.cmdloop("Welcome to the combat shell. Type ?  for help.")
        print("Youre out of combat!")
        return


cShell = MainShell()
cShell.prompt = '(Normal Shell) >> '
cShell.cmdloop("Let the combat begin!")
