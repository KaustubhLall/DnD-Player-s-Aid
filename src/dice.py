# This module does simple random dice rolling jobs.

import random


def roll(die):
    """
    Rolls a given die
    :param die:
    :return: (totalRoll, inDividualRollsAsList)
    """
    die = parseDie(die)
    return rollDice(die[0], die[1])


def rollDice(n, m):
    """
    Rolls a dice of size m n times.
    :param n: times to roll the die.
    :param m: size of the die.
    :return: (totalRoll, individualRollsAsList)
    """
    rolls = []
    roll = 0
    neg = False
    if m < 0:
        neg = True
        m = -1 * m

    for i in range(n):
        rolls.append(random.randrange(1, m))

    if neg:
        roll = -(sum(rolls))
        rolls = [-x for x in rolls]

    else:
        roll = sum(rolls)

    return roll, rolls


def rollWithReroll(die, timesToReroll, threshold=-1):
    """
    Same as roll but takes the best roll of timesToReroll.
    You can use threshold, so that a reroll will only be made if the roll is
    under a certain roll.
    :param die: die to roll.
    :param timesToReroll: times to reroll a roll.
    :param threshold: threshold. If roll > threshold it is not rerolled.
    :return: roll of the die.
    """
    # todo


def rollAboveK(die, k, times=-1):
    """
    Rerolls the die if it is less than k.
    :param die: die to roll.
    :param k: threshold to roll again above.
    :param times: number of times the die should be rerolled.
    :return: totalRoll, individualRolls
    """
    # todo


def parseExpression(expr):
    """
    Parses the roll of many die rolls.
    ex: d6+2d4+1 or d6-1 or d4+1 ...
    :return: result of the rolls.
    """
    expr = expr.lower().strip()
    tokens = expr.split("+")
    rolls = []
    total = 0
    indivRolls = []

    for token in tokens:
        # handle constants
        if 'd' not in token:
            try:
                total += int(token)
            except:
                # probably a glitch in split
                pass

        # roll and add to rolls
        else:
            rolls.append(roll(token))

    for entry in rolls:
        total += entry[0]
        indivRolls.append(entry[1])

    return total, indivRolls


def parseDie(die):
    """
    Parses a single die.
    :param die: input die to parse.
    :return: (num_times_to_roll_die, die_size)
    """
    # implicitly add a 1 to the die. Ex d20 becomes 1d20.
    if die[0] == 'd':
        die = '1' + die

    args = die.split("d")

    n = int(args[0])
    m = int(args[1])

    return n, m


def test():
    """
    Simple tester for die rolls.
    :return:
    """
    roll1 = roll('5d20')
    print("Rolling 5d20:\n\tTotal: %d.\n\tIndividual rolls: %s" % (
        roll1[0], roll1[1]))

    roll2 = parseExpression("2d4+2d10")
    print("\nRolling 2d4+2d10:\n\tTotal: %d\n\tIndividual rolls: %s." % (
        roll2[0], roll2[1]))
