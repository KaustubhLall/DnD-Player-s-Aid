# this script will run the main shell that interacts with the user.
# by default, the shell runs in this state.
# however, subshells may be called by this shell.
# for example, when a  player enters combat, the control is transferred to the
# combat subshell. These will be defined as methods inside this package,
# or within other .py files.
shell =
def combatSubshell(player):
    """
    Runs the combat subshell.
    :param player: data of the current player as a player object.
    :return:
    """


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