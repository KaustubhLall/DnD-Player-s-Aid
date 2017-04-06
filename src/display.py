# This module formats text that contains player data to display well


class Display():
    player = None

    def __init__(self, player):
        """
        Sets up the display object to display the information for the given player object.
        :param player: player to fetch data from
        """
        self.player = player

    def displaySkills(self):
        """
        Shows skills with proficiency, bonus and expertise.
        :return: string of data
        """
        pass

    def quickDisplay(self):
        """
        Shows HP out of max, movement speed, temporary hitpoints, AC.
        :return: String of the data.
        """
        maxHP = self.player.playerMaxHP
        curHp = self.player.playerHP
        ac = self.player.playerAC
        tempHP = self.player.playerTempHP
        movement = self.player.movementSpeed

        formatter = curHp, tempHP, maxHP, ac, movement

        return "You status is:\n\tHP: %d (+%d) / %d\n\tAC: %d\n\tMovement: %d" % formatter
