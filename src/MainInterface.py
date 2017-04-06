import cmd, src.player as Player

player = Player.Player()


class CombatShell(cmd.Cmd):
    """
    Handles one instance of combat.
    """
    aliases = {}

    ###############################
    # Shell Setup                 #
    ###############################
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.aliases = {
            'd': self.do_damage,
        }

    def preloop(self):
        """
        Preloop
        :return:
        """
        print("The pre-loop setup entered successfully.")

    def postloop(self):
        """
        Postloop.
        :return:
        """
        print("The postloop cleanup happened.")

    #########################
    # Help Messages         #
    #########################

    def help_damage(self):
        print("Applies damage to the user. Usage: d/damage <amount_in_numbers>")

    ##############################
    # Methods for Commands       #
    ##############################

    def do_heal(self, args):
        args = args.split(" ")

    def do_damage(self, args):
        """
        Hurts the player.
        :param args: damage
        :return: True if valid.
        """
        # Check valid #
        args = args.split(" ")
        if len(args) == 0:
            print("Usage: d/damage <amount_in_numbers>")
            return False

        dmg = -1
        try:
            dmg = int(args[1])
        except ValueError:
            print("Usage: d/damage <amount_in_numbers>")
            return False

        # apply damage #
        alive = player.damage(dmg)
        print("You just took %d points of damage!")

        if not alive:
            print("You just fell unconscious!")
        return True


class MainShell(cmd.Cmd):
    combat_shell = None
    aliases = {}

    def __init__(self):
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
        # TODO load player object here
        print("Welcome to DnD Tool!")

    def postloop(self):
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
