# this script will run the main shell that interacts with the user.
# by default, the shell runs in this state.
# however, subshells may be called by this shell.
# for example, when a  player enters combat, the control is transferred to the
# combat subshell. These will be defined as methods inside this package,
# or within other .py files.
import src.playerinterface as interface
import src.constants as CONST
from src.spells import SpellBook as spells

shell = interface.PlayerInterface()


def combatSubshell(player):
    """
    Runs the combat subshell.
    :param player: data of the current player as a player object.
    :return:
    """

    with CONST.SUBSHELL_COMBAT_MESSAGES as messages:
        # enter into combat subshell
        shell.next(messages["Enter"])
        endCombat = False
        combatRound = 0
        while not endCombat:
            # start a new round
            shell.next("You are in round %d of combat." % combatRound)
            player.startNewRound()

            ##### parse commands #####
            response = shell.read("Enter a command. Press h for help.")
            workingCommand = tokenizeCommand(response, CONST.COMBAT_COMMANDS)

            # check for invalid commands
            if workingCommand[0] == None:
                response = tokenizeCommand(shell.read(
                    "Type help/h/? for a list of all commands. End/e/q to end "
                    "combat."),
                    CONST.COMBAT_COMMANDS)

            # check for end shell
            if workingCommand[0] in ["e", "end"]:
                shell.out("Combat ended.")
                shell.out(player.printStatus())
                return

            # check for help command
            if workingCommand[0] in ["h", "help", "?"]:
                shell.out(CONST.COMBAT_HELP)

            ##### deliver valid commands #####
            # check for damage command

            if workingCommand[0] == "d":
                amount = 0
                if len(workingCommand) > 1:
                    try:
                        amount = int(workingCommand[1])
                    except ValueError:
                        shell.out("Invalid damage entered.")
                player.damage(amount)
                shell.out("Player took %d damage." % amount)

            # check for move command
            if workingCommand[0] in ["m", "move"]:
                amount = 0
                if len(workingCommand) > 1:
                    try:
                        amount = int(workingCommand[1])
                    except ValueError:
                        shell.out("Distance not valid.")

                player.move(amount)
                shell.out("Moved player %2dft." % amount)

            # check for spell
            if workingCommand[0] in ["s", "spell"]:
                if len(workingCommand) == 1:
                    shell.out(player.printSpells())
                else:
                    spell = workingCommand[1]
                    if spells.searchList(spell) != []:
                        shell.out(spells.print(spell))
                    else:
                        shell.out("Spell %s doesnt exist in database." % spell)


def inventorySubshell(player):
    """
    Does inventory interactions with the player. Money-interactions will
    likely jsut be implemented into the main subshell.
    :param player: player whose data is to be manipulated.
    :return:
    """


def helpSubShell(player):
    """
    Experimental subshell that might be implemented to have useful context/help
    for items.
    :param player: probably not relevant
    :return:
    """


def tokenizeCommand(s, commandSublist=CONST.KNOWN_COMMANDS):
    """
    Parses the command and tokenizes it.
    :param s: string of command passed in.
    :param commandSublist: a list of known commands, defaults to all known
    if not specified.
    :return: tuple (command, args)
    """
    # first, strip down the command and parse it
    s = str(s).lower().strip()

    # if command is empty, exit
    if len(s) == 0:
        return [None]

    # else, we will try and parse it
    args = s.split(" ")

    for command in args:
        if command in commandSublist:
            sliceAt = args.index(command)
            return command, args[sliceAt + 1:]

    return (None, args)
