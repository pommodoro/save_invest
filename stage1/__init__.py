from otree.api import *
import json
import random
import numpy as np
import time

doc = """
Stage 1 of save invest experiment
"""


class C(BaseConstants):
    NAME_IN_URL = 'mplApp'
    PLAYERS_PER_GROUP = None

    # this lets each person make at most 24 changes
    NUM_ROUNDS = 512

    # number of unique rounds -1. Setting this to 1 gives two unique rounds.
    # There are 42 total comparisons, so this should be set to 41.
    ORDER_MAX = 41

    # ORDER RANDOMIZATION SHOULD NOT BE DONE IN THE BASE CONSTANTS
    # randomize order of rounds
    # round order is range from 0 to 42 (or number of unique rounds)
    # recall this will be a list of length 42 because it starts at zero and does not include the upper endpoint.
    ROUND_ORDER = list(range(0, 42, 1))

    # print("Original: ", ROUND_ORDER)
    # random.shuffle(ROUND_ORDER)
    # print("1 shuffle: ", ROUND_ORDER)

    # repeating the fixed ENDOWMENT (10) the total number of unique comparisons + 1 since we are never in round 0
    ENDOWMENT = [10] * 42

    # populating probability A

    PROBA = [1, 1, 1, 1, 1, 
             1, 1, 1, 1, 1,
             0.2, 0.2, 0.2, 0.2, 0.2,
             0.2, 0.2, 0.2, 0.3, 0.3,
             0.3, 0.3, 0.3, 0.3, 0.3,
             0.3, 0.4, 0.4, 0.4, 0.4,
             0.4, 0.4, 0.4, 0.4, 0.5,
             0.5, 0.5, 0.5, 0.5, 0.5,
             0.5, 0.5]

    # populating probability B
    PROBB = [round(1 - p, 2) for p in PROBA]

    # populating return to A
    RETURNA = [1, 1.1, 1.2, 1.3, 1.4,
               1.5, 1.6, 1.7, 1.8, 1.9,
               5, 4.5, 6, 5.5, 7,
               6, 7.5, 7, 3.5, 3,
               4, 3.5, 4.5, 4, 5,
               4.5, 2.5, 2, 3, 2.5,
               3.5, 2.5, 3.5, 3, 2.5,
               1.5, 2.5, 1.5, 2.5, 2,
               2.5, 2]

    # populating return to B
    RETURNB = [-1, -1, -1, -1, -1,
               -1, -1, -1, -1, -1,
               1.2, 1.2, 1.4, 1.4, 1.6,
               1.6, 1.8, 1.8, 1.4, 1.4,
               1.6, 1.6, 1.8, 1.8, 2,
               2, 1.6, 1.6, 1.8, 1.8,
               2, 2, 2.2, 2.2, 1.8, 
               1.8, 2, 2, 2.2, 2.2, 
               2.4, 2.4]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # Comprehension Question Fields
    comp_instant = models.FloatField()
    comp_oneMonthA = models.FloatField()
    comp_oneMonthB = models.FloatField()
    comp_prob1 = models.FloatField()
    comp_prob2 = models.FloatField()

    # Round Parameters
    counter = models.IntegerField()
    round_order = models.IntegerField()
    round_endowment = models.CurrencyField()
    round_probA = models.FloatField()
    round_probB = models.FloatField()
    round_returnA = models.FloatField()
    round_returnB = models.FloatField()

    # Round Choices
    savings = models.CurrencyField(min=0, max=10)
    investA = models.CurrencyField()
    investB = models.CurrencyField()

    # set min value for input in investA
    def investA_min(player):
        if (player.round_probB == 0):
            return player.round_endowment - player.savings
        return 0

    # set max value for input in investA
    def investA_max(player):
        return player.round_endowment - player.savings

    # Payoffs
    paying_asset = models.StringField()
    payoff_today = models.CurrencyField()
    payoff_oneMonth = models.CurrencyField()
    make_changes = models.BooleanField()

    # Final counter round indicator
    is_done = models.BooleanField(initial=False)

    # Reaction times
    start_time = models.FloatField()
    reaction_time = models.FloatField()

# Error Messages for incorrect user inputs


def comp_instant_error_message(player, value):
    if value != 10:
        return 'Incorrect. Try Again.'


def comp_oneMonthA_error_message(player, value):
    if value != 11:
        return 'Incorrect. Try Again.'


def comp_oneMonthB_error_message(player, value):
    if value != 5:
        return 'Incorrect. Try Again.'


def comp_prob1_error_message(player, value):
    if value != 60:
        return 'Incorrect. Try Again.'


def comp_prob2_error_message(player, value):
    if value != 40:
        return 'Incorrect. Try Again.'


def investA_error_message(player, value):
    if value > (player.round_endowment - player.savings):
        return 'Cannot invest more than is available after savings'
    if value < 0:
        return 'Investment must be zero or greater'

# PAGES


class InstructionsStageOne(Page):
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        # point to the participant attribute
        participant = player.participant

        # write the order to data
        round_order = C.ROUND_ORDER.copy()
        participant.round_order = random.sample(round_order, len(round_order))


class ComprehensionStageOne1(Page):
    def is_displayed(player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['comp_instant', 'comp_oneMonthA', 'comp_oneMonthB']


class ComprehensionStageOne2(Page):
    def is_displayed(player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['comp_prob1', 'comp_prob2']


class ComprehensionComplete(Page):
    def is_displayed(player):
        return player.round_number == 1
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.rts_save = []
        participant.rts_invest = []


class SaveToday(Page):
    def is_displayed(player: Player):
        if player.is_done == True:
            return False
        return True

    form_model = 'player'
    form_fields = ['savings']

    @staticmethod
    def vars_for_template(player: Player):
        # time start to compute reaction time
        player.start_time = time.time()

        # set the counter
        # if first round intialize at 0
        if (player.round_number == 1):
            player.counter = 0

        # for other rounds do
        if (player.round_number > 1):

            # define the previous player
            prev_player = player.in_round(player.round_number-1)

            # if player is altering preferences, counter set to previous round counter
            if (prev_player.make_changes == True):
                player.counter = prev_player.counter

            # if new round, counter set to previous round counter +1
            else:
                player.counter = prev_player.counter + 1
        # if first round, counter set to 0
        else:
            player.counter = 0

        # test to see if this is the last round
        # important because player.counter could be out of round_order range
        # if (player.counter < C.ORDER_MAX):
        participant = player.participant
        order = participant.round_order[player.counter]
        endowment = C.ENDOWMENT[order]
        probA = C.PROBA[order]
        returnA = C.RETURNA[order]
        probB = C.PROBB[order]
        returnB = C.RETURNB[order]

        # order = C.ROUND_ORDER[player.counter] if (player.counter <C.ORDER_MAX) else 0
        # endowment = C.ENDOWMENT[order]
        # probA = C.PROBA[order]
        # returnA = C.RETURNA[order]
        # probB = C.PROBB[order]
        # returnB = C.RETURNB[order]

        return dict(
            order_display=order,
            endowment_display=endowment,
            probA_display=probA,
            returnA_display=returnA,
            probB_display=probB,
            returnB_display=returnB if returnB > 0 else "N/A",
            roundNo_display=player.counter+1
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        # store reaction times
        player.reaction_time = time.time() - player.start_time
        player.participant.rts_save.append(player.reaction_time)

        # writing to memory after clicking submit
        participant = player.participant
        player.round_order = participant.round_order[player.counter]
        player.round_endowment = C.ENDOWMENT[player.round_order]
        player.round_probA = C.PROBA[player.round_order]
        player.round_returnA = C.RETURNA[player.round_order]
        player.round_probB = C.PROBB[player.round_order]
        player.round_returnB = C.RETURNB[player.round_order]


class InvestA(Page):
    def is_displayed(player):
        if (player.round_returnB == -1):
            player.investA = player.round_endowment - player.savings
            return False
        if (player.round_number == 1):
            return True
        prev_player = player.in_round(player.round_number - 1)
        # if (prev_player.make_changes == False and prev_player.counter == C.ORDER_MAX):
        if (player.is_done == True):
            return False
        return True

    form_model = 'player'
    form_fields = ['investA']

    @staticmethod
    def vars_for_template(player):
        # time start to compute reaction time
        player.start_time = time.time()
        
        order = player.participant.round_order[player.counter]
        endowment = C.ENDOWMENT[order]
        probA = C.PROBA[order]
        returnA = C.RETURNA[order]
        probB = C.PROBB[order]
        returnB = C.RETURNB[order]
        max_investA = C.ENDOWMENT[order] - player.savings

        return dict(
            endowment_display=endowment,
            probA_display=probA,
            returnA_display=returnA,
            probB_display=probB,
            returnB_display=returnB if returnB > 0 else "N/A",
            max_investA_display=max_investA,
            roundNo_display=player.counter+1
        )
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        # store reaction times
        player.reaction_time = time.time() - player.start_time
        player.participant.rts_invest.append(player.reaction_time)


class Confirm(Page):
    def is_displayed(player):
        if (player.round_number == 1):
            return True

        prev_player = player.in_round(player.round_number - 1)
        
        if (player.is_done == True):
            return False
        return True

    form_model = 'player'
    form_fields = ['make_changes']

    @staticmethod
    def vars_for_template(player):
        # writes choices for use in pages
        order = player.participant.round_order[player.counter]
        endowment = C.ENDOWMENT[order]
        probA = C.PROBA[order]
        returnA = C.RETURNA[order]
        probB = C.PROBB[order]
        returnB = C.RETURNB[order]
        max_investA = C.ENDOWMENT[order] - player.savings
        investB = C.ENDOWMENT[order] - player.savings - player.investA
        money_today = player.savings
        money_onemonthA = C.RETURNA[order] * player.investA
        money_onemonthB = max(0, C.RETURNB[order] * (
            C.ENDOWMENT[order] - player.savings - player.investA))

        return dict(
            endowment_display=endowment,
            probA_display=probA,
            returnA_display=returnA,
            probB_display=probB,
            returnB_display=returnB if returnB > 0 else "N/A",
            max_investA_display=max_investA,
            investB_display=investB,
            money_today_display=money_today,
            money_onemonthA_display=money_onemonthA,
            money_onemonthB_display=money_onemonthB,
            roundNo_display=player.counter+1
        )

    # for the barchart
    def js_vars(player):
        order = player.participant.round_order[player.counter]
        money_today = player.savings
        money_onemonthA = C.RETURNA[order] * player.investA
        money_onemonthB = max(
            0, C.RETURNB[order] * (C.ENDOWMENT[order] - player.savings - player.investA))
        chart_series = [money_today, money_onemonthA, money_onemonthB]

        return dict(
            money_today_chart=money_today,
            money_onemonthA_chart=money_onemonthA,
            money_onemonthB_chart=money_onemonthB,
            chart_series=chart_series
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        # point to the participant attribute
        participant = player.participant

        if player.round_number == 1 :
            # initialize participant lists if first round
            participant.monthA = []
            participant.monthB = []
            participant.probA = []
            participant.probB = []
            participant.savings = []

        if player.make_changes == False:
            # write investB to data
            player.investB = player.round_endowment - player.savings - player.investA

            order = player.participant.round_order[player.counter]
            participant.monthA.append(C.RETURNA[order] * player.investA)
            participant.monthB.append(
                max(0, C.RETURNB[order] * (C.ENDOWMENT[order] - player.savings - player.investA)))
            participant.probA.append(player.round_probA)
            participant.probB.append(player.round_probB)
            participant.savings.append(player.savings)

        if player.counter == C.ORDER_MAX and player.make_changes == False:
            player.is_done = True

            # select the paying round
            participant = player.participant

            # select a random UNIQUE round number
            random_round = random.randint(0, C.ORDER_MAX - 1)
            participant.paying_round = random_round + 1

            # payoff today
            participant.payoff_today_s1 = participant.savings[random_round]

            # check if there was no asset B
            if participant.probA[random_round] == 1:

                # payoff in a month
                participant.payoff_one_month_s1 = participant.monthA[random_round]
                participant.paying_asset = "A"

            # if there is an asset B, sample assets with weights
            else:
                # sample with weights
                assets = ["A", "B"]
                weights = [participant.probA[random_round],
                           participant.probB[random_round]]
                chosen_asset = random.choices(assets, weights=weights, k=1)[0]

                participant.paying_asset = chosen_asset

                if chosen_asset == "A":
                    participant.payoff_one_month_s1 = participant.monthA[random_round]

                if chosen_asset == "B":
                    participant.payoff_one_month_s1 = participant.monthB[random_round]


class EndOf(Page):
    @staticmethod
    def is_displayed(player):
        if(player.is_done == True):
            return(True)
        else:
            return(False)

    # DEBUG
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return dict(
            payoff_today_s1=participant.payoff_today_s1,
            paying_round=participant.paying_round,
            paying_asset=participant.paying_asset,
            payoff_one_month_s1=participant.payoff_one_month_s1
        )

    # create participant variables to be used in stage 2
    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant

        # get the index numbers where the probability of getting asset A is not 1
        # and converting to a list
        idx_np1 = np.where(np.array(participant.probA) != 1)[0].tolist()

        # subsetting values only for when probA 
        participant.s2savings = np.array(participant.savings)[idx_np1].tolist()
        participant.s2probA = np.array(participant.probA)[idx_np1].tolist()
        participant.s2probB = np.array(participant.probB)[idx_np1].tolist()
        participant.s2monthA = np.array(participant.monthA)[idx_np1].tolist()
        participant.s2monthB = np.array(participant.monthB)[idx_np1].tolist()



    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return upcoming_apps[0]


page_sequence = [
    InstructionsStageOne,
    ComprehensionStageOne1,
    ComprehensionStageOne2,
    ComprehensionComplete,
    SaveToday,
    InvestA,
    Confirm,
    EndOf
]
