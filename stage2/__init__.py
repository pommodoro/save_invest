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

    # total rounds is 32
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

    # Determining the paying round and row for stage 2. Done here so that refreshing the final page does not change results.
    @staticmethod
    def before_next_page(player, timeout_happened):
        # define participant in name space
        participant = player.participant

        # determine the paying round in stage 2
        participant.paying_round_stage_2 = random.randint(1, 32)

        # determine the paying ROW in the round, there a 62 rows but we
        # want to sample from 0 to 61 for indexing
        participant.paying_row = random.randint(0, 61)

class MplPage(Page):
    def is_displayed(player: Player):
        return True

    form_model = "player"
    form_fields = ["options_chosen"]

    @staticmethod
    def vars_for_template(player: Player):
        # savings selected in the round number
        payment_today = player.participant.s2savings[player.round_number - 1]

        # returns from invested amount in A and rate
        monthA = player.participant.s2monthA[player.round_number - 1]

        # returns from invested amount in B and rate
        monthB = player.participant.s2monthB[player.round_number - 1]

        # probability of asset A being picked ROUND to whole numbers
        probA = round(player.participant.s2probA[player.round_number - 1] * 100)


        # probability of asset B being picked ROUND to whole numbers
        probB = round(player.participant.s2probB[player.round_number - 1] * 100)

        # RHS range of future payoffs from $0 to $30 for sure
        variable_range = C.LIST_OF_VARIABLE_OPTIONS.copy()

        # RHS text
        variable_options_text_this_round = C.LIST_OF_VARIABLE_OPTION_TEXTS[
            player.round_number - 1]

        # Intialize empty lists
        list_of_fixed_options = []
        list_of_variable_options = []

        for i, variable in enumerate(variable_range):
            id_text_pair_variable = [
                "v"+str(i), variable_options_text_this_round.format(today=payment_today, one_month=variable)]
            id_text_pair_fixed = ["f"+str(i), "Today: "+str(payment_today)+", One Month: Lottery A "]
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
        if(player.round_number == C.NUM_ROUNDS):
            return True

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant

        # get the player for the paying round
        paying_player = player.in_round(participant.paying_round_stage_2)

        # get the fixed or variable
        choice = paying_player.options_chosen[participant.paying_row]

        # get the payoff today
        participant.payoff_today_s2 = participant.s2savings[participant.paying_round_stage_2 - 1]

        # gets stage 1 results
        paying_round1 = player.participant.paying_round
        payoff_today_s1 = player.participant.payoff_today_s1
        paying_asset_s1 = player.participant.paying_asset
        payoff_one_month_s1 = player.participant.payoff_one_month_s1

        if choice == "f":

            # get the payoff in one month
            if participant.s2probA[paying_round_stage_2 - 1] == 1:
                participant.payoff_one_month_s2 = participant.s2monthA[paying_round_stage_2 - 1]

            else:
                # sample with weights
                assets = ["A", "B"]
                weights = [participant.s2probA[paying_round_stage_2 - 1], participant.s2probB[paying_round_stage_2 - 1]]
                chosen_asset = random.choices(assets, weights = weights, k = 1)[0]

                if chosen_asset == "A":
                    participant.payoff_one_month_s2 = participant.s2monthA[paying_round_stage_2 - 1]

                if chosen_asset == "B":
                    participant.payoff_one_month_s2 = participant.s2monthB[paying_round_stage_2 - 1]

        else:
            participant.payoff_one_month_s2 = C.LIST_OF_VARIABLE_OPTIONS[participant.paying_row]

        return dict(
            payoff_today_s1 = participant.payoff_today_s1,
            payoff_one_month_s1 = participant.payoff_one_month_s1,
            payoff_today_s2 = participant.payoff_today_s2,
            payoff_one_month_s2 = participant.payoff_one_month_s2)

page_sequence = [
    InstructionsStageTwo,
    MplPage,
    Results
]
