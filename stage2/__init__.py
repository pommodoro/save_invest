from otree.api import *
import json
import random
import numpy as np

doc = """
Stage 2 (MPL) of save invest experiment
"""


class Constants(BaseConstants):
    name_in_url = 'stage2'
    players_per_group = None
    num_rounds = 32

    # round order will not be randomized

    # if the variable below is True, then the variable part of the MPL is displayed on the right, 
    # otherwise it is displayed on the left
    display_variable_right = True

    # # Initialize the format of the fixed option
    # list_of_fixed_options = [
    #     "Option A",
    # ]

    # list_of_fixed_options = list_of_fixed_options*32

    # The list below should contain 1 entry per round
    # It should contain the text of the variable part for a given round
    # {placeholder} will be replace with the items of the array
    list_of_variable_option_texts = [
        "Today:{today} , One Month: ${one_month} for sure"
    ]*32
    # the list below contains one sublist per round
    # each sublist contains the options displayed in this round
    list_of_variable_options = [
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

    @staticmethod
    def vars_for_template(player):
    #CREATING THE LISTS FOR DISPLAY
        monthA = player.participant.monthA
        monthB = player.participant.monthB
        savings = player.participant.savings
        probA = player.participant.probA
        probB = player.participant.probB
        order = player.participant.round_order

    
        return dict(
            monthA_display=monthA,
            monthB_display=monthB,
            savings_display=savings,
            probA_display=probA,
            probB_display=probB,
            order_display=order
        )

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
        probA = player.participant.probA[player.round_number - 1]

        # probability of asset B being picked
        probB = player.participant.probB[player.round_number - 1]


        # RHS range of future payoffs from $0 to $30 for sure
        variable_range = Constants.list_of_variable_options.copy()

        # RHS text
        variable_options_text_this_round = Constants.list_of_variable_option_texts[player.round_number - 1]

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

class Results(Page):
    def is_displayed(player: Player):
        return True

    @staticmethod
    def vars_for_template(player: Player):
        list_of_choices = json.loads(player.options_chosen)
        return {
            "list_of_choices": list_of_choices,
        }

page_sequence = [
    InstructionsStageTwo,
    MplPage,
    Results
]
