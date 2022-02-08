from otree.api import *
import json
import random
import numpy as np

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'stage2'
    players_per_group = None
    num_rounds = 150

    order_max = 2 #number of unique rounds in stage 2

    # randomize order of rounds
    round_order = list(range(1, order_max, 1)) #round order is range from 1 to 43 (or number of unique rounds)

    # print("Original: ", round_order)
    random.shuffle(round_order)
    # print("1 shuffle: ", round_order)

    # if the variable below is True, then the variable part of the MPL is displayed on the right, 
    # otherwise it is displayed on the left
    display_variable_right = True

    # the list below should contain 1 entry per round
    list_of_fixed_options = [
        "A payoff of $4 for sure",
        "A payoff of $4 for sure",
        "A payoff of $8 for sure",
    ]
    # The list below should contain 1 entry per round
    # It should contain the text of the variable part for a given round
    # {placeholder} will be replace with the items of the array
    list_of_variable_option_texts = [
        "${placeholder} with a probability of 20%",
        "$7 with a probability of {placeholder}%",
        "$10 with a probability of {placeholder}%",
    ]
    # the list below contains one sublist per round
    # each sublist contains the options displayed in this round
    list_of_lists_of_variable_options = [
        [4 + x for x in np.arange(0, 10.25, 0.25).tolist()],
        [10, 60],
        [65, 75, 85, 95],
    ]


class Subsession(BaseSubsession):
    pass 

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # MOVE THIS TO MPL APP

    # the field contains one record per choice that is either f for fixed or v for variable
    # since we cannot store lists in the database we store the information as a string.
    # If it is needed as a list again (e.g. for payoff calculation) it can be converted 
    # back into a list by importing the json module and using using json.loads()
    options_chosen = models.StringField()

# # FUNCTIONS
# def creating_session(subsession: Subsession):
#         if subsession.round_number == 1:

#             for p in subsession.get_players():

#                 # TEMPORARY STAGE 2 PAYING ASSET WILL MOVE TO MPL APP
#                 paying_order_s2 = random.randint(0, Constants.order_max_s2-1)
#                 p.paying_order_s2 = paying_order_s2

#                 paying_choice_number_s2 = random.randint(0, 19)
#                 p.paying_choice_number_s2 = paying_choice_number_s2

#                 paying_asset_s2 = random.uniform(0,1)
#                 p.paying_asset_number_s2 = paying_asset_s2

# PAGES

class InstructionsStageTwo(Page):
    def is_displayed(player: Player):
        return True

    @staticmethod
    def vars_for_template(player):
    #DELETE THIS ONLY A TESTER
        investA = player.participant.investA
        investB = player.participant.investB
        savings = player.participant.savings
        make_changes = player.participant.make_changes
    
        return dict(
            max_investA_display=investA,
            investB_display=investB,
            savings_display=savings,
            make_changes_display=make_changes,
        )

class MplPage(Page):
    def is_displayed(player: Player):
        return True

    form_model = "player"
    form_fields = ["options_chosen"]

    @staticmethod
    def vars_for_template(player: Player):
        fixed_option_this_round = Constants.list_of_fixed_options[player.round_number - 1]
        variables_this_round = Constants.list_of_lists_of_variable_options[player.round_number - 1]
        variable_options_text_this_round = Constants.list_of_variable_option_texts[player.round_number - 1]
        list_of_variable_options = []
        list_of_fixed_options = []
        for i, variable in enumerate(variables_this_round):
            id_text_pair_variable = ["v"+str(i), variable_options_text_this_round.format(placeholder=variable)]
            id_text_pair_fixed = ["f"+str(i), fixed_option_this_round]
            list_of_fixed_options.append(id_text_pair_fixed)
            list_of_variable_options.append(id_text_pair_variable)
        number_of_options = len(list_of_fixed_options)
        return {
            "number_of_options": number_of_options,
            "list_of_fixed_options": list_of_fixed_options,
            "list_of_variable_options": list_of_variable_options,
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
