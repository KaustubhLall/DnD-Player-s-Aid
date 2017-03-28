import os
import src.constants as CONST


class PlayerInterface:
    """This class serves as an interface between the player and the program."""

    def out(self, message):
        """
        Sends a message to the player.
        :param message: message to send.
        :return: None.
        """
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

    def next(self, message="", ch=" "):
        """
        Enters the next interaction with the user.
        :param message: optional message to display.
        :return: None
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        if message != "":
            message = "+" + message + "+"
            padding = CONST.TERMINAL_LENGTH - len(message)
            padding /= 2
            padding = int(padding)
            out = message + (padding * ch)
            print(out + "\n")

    def confirm(self, s):
        """
        Prompts the user to confirm an action with the given input string.
        :param s: string to prompt for.
        :return: true if user is affirmative, else false.
        """
        AFFIRMATIVES = ["y", "yes"]
        NEGATIVES = ["n", "no"]
        response = self.read(s + "(y/n) : ")

        if response in AFFIRMATIVES:
            return True
        elif response in NEGATIVES:
            return False
        else:
            return self.confirm(s)
