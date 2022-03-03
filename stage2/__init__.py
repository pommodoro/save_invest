from otree.api import *
import json
import random
import numpy as np

doc = """
Stage 2 (MPL) of save invest experiment
"""


class C(BaseConstants):
    NAME_IN_URL = 'stage2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 32

    # round order will not be randomized

    # if the variable below is True, then the variable part of the MPL is displayed on the right, 
    # otherwise it is displayed on the left
    DISPLAY_VARIABLE_RIGHT = True

    # # Initialize the format of the fixed option
    # list_of_fixed_options = [
    #     "Option A",
    # ]

    # list_of_fixed_options = list_of_fixed_options*32

    # The list below should contain 1 entry per round
    # It should contain the text of the variable part for a given round
    # {placeholder} will be replace with the items of the array
    LIST_OF_VARIABLE_OPTION_TEXTS = [
        "Today: {today}, One Month: ${one_month} for sure"
    ]*32
    # the list below contains one sublist per round
    # each sublist contains the options displayed in this round
    LIST_OF_VARIABLE_OPTIONS = [
        x for x in np.arange(0, 31, 0.50).tolist()
    ]


class Subsession(BaseSubsession):
    pass 

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # the field contains one record per choice that is either f for fixed or v for variable
    # since we cannot store lists in the database we store the information as a string.
    # If it is needed as a list again (e.g. for payoff calculation) it can be converted 
    # back into a list by importing the json module and using using json.loads()
    options_chosen = models.StringField()

# PAGES

class InstructionsStageTwo(Page):
    def is_displayed(player: Player):
        return player.round_number == 1


class MplPage(Page):
    def is_displayed(player: Player):
        return True

    form_model = "player"
    form_fields = ["options_chosen"]

    @staticmethod
    def vars_for_template(player: Player):
        # savings selected in the round number
        payment_today = player.participant.savings[player.round_number - 1]

        # returns from invested amount in A and rate
        monthA = player.participant.monthA[player.round_number - 1]

        # returns from invested amount in B and rate
        monthB = player.participant.monthB[player.round_number - 1]

        # probability of asset A being picked
        probA = player.participant.probA[player.round_number - 1] * 100

        # probability of asset B being picked
        probB = player.participant.probB[player.round_number - 1] * 100


        # RHS range of future payoffs from $0 to $30 for sure
        variable_range = C.LIST_OF_VARIABLE_OPTIONS.copy()

        # RHS text
        variable_options_text_this_round = C.LIST_OF_VARIABLE_OPTION_TEXTS[player.round_number - 1]

        # Intialize empty lists
        list_of_fixed_options = []
        list_of_variable_options = []

        for i, variable in enumerate(variable_range):
            id_text_pair_variable = ["v"+str(i), variable_options_text_this_round.format(today=payment_today, one_month=variable)]
            id_text_pair_fixed = ["f"+str(i), "Option A"]
            list_of_fixed_options.append(id_text_pair_fixed)
            list_of_variable_options.append(id_text_pair_variable)
        number_of_options = len(list_of_fixed_options)


        return {
            "number_of_options": number_of_options,
            "list_of_fixed_options": list_of_fixed_options,
            "list_of_variable_options": list_of_variable_options,
            "monthA_display": monthA,
            "monthB_display": monthB,
            "savings_display": payment_today,
            "probA_display": probA,
            "probB_display": probB
        }

        #Create a page that checks if round number is last round, then go to final confirmation page of finishing


page_sequence = [
    InstructionsStageTwo,
    MplPage
]
