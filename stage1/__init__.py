from otree.api import *
import json
import random

doc = """
Stage 1 of save invest experiment
"""


class C(BaseConstants):
    NAME_IN_URL = 'mplApp'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3

    ORDER_MAX = 42 #number of unique rounds in stage1-1

    # randomize order of rounds
    ROUND_ORDER = list(range(1, ORDER_MAX, 1)) #round order is range from 1 to 43 (or number of unique rounds)

    # print("Original: ", ROUND_ORDER)
    random.shuffle(ROUND_ORDER)
    # print("1 shuffle: ", ROUND_ORDER)

    # repeating the fixed ENDOWMENT (10) the total number of unique comparisons + 1 since we are never in round 0
    ENDOWMENT = [10] * 43

    # populating probability A
    PROBA = [0, 1, 0.1,  0.55, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 0.95, 0.8, 0.3, 0.6, 0.5, 0.95,
    0.2, 0.7, 0.4, 0.5, 0.05, 0.8, 0.3, 0.6, 0.5, 0.95,
    0.2, 0.7, 0.4, 0.5, 0.05, 0.8, 0.3, 0.6, 0.5, 0.95, 
    0.2, 0.7, 0.4, 0.5]

    # populating probability B
    PROBB = [round(1 - p, 2) for p in PROBA]

    # populating return to A
    RETURNA = [0, 2.1,1.9, 2.7, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 
    1.6, 1.7, 1.8, 1.9, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7,
    1.7, 1.7, 1.7, 1.7, 2.4, 2.4, 2.4, 2.4, 2.4, 2.4,
    2.4, 2.4, 2.4, 2.4, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2,
    2.2, 2.2, 2.2, 2.2]

    # populating return to B
    RETURNB = [0, -1, 2.3, 1.6, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5,
    2.5, 2.5, 2.5, 2.5, 2.5, 1.8, 1.8, 1.8, 1.8, 1.8,
    1.8, 1.8, 1.8, 1.8, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2]


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

    #Round Parameters
    counter = models.IntegerField()
    round_order = models.IntegerField()
    round_endowment = models.CurrencyField()
    round_probA = models.FloatField()
    round_probB = models.FloatField()
    round_returnA = models.FloatField()
    round_returnB = models.FloatField()

    #Round Choices
    savings = models.CurrencyField(min = 0, max = 10)
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
        
    #Payoffs
    paying_asset = models.StringField()
    payoff_today = models.CurrencyField()
    payoff_oneMonth = models.CurrencyField()
    make_changes = models.BooleanField()
    

#Error Messages for incorrect user inputs
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
        participant.round_order = C.ROUND_ORDER.copy()



class ComprehensionStageOne1(Page):
    def is_displayed(player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['comp_instant', 'comp_oneMonthA','comp_oneMonthB']

class ComprehensionStageOne2(Page):
    def is_displayed(player):
        return player.round_number == 1

    form_model = 'player'
    form_fields = ['comp_prob1', 'comp_prob2']

class SaveToday(Page):
    def is_displayed(player: Player):
        if (player.round_number == 1):
            player.session.vars['order'] = 0
            return True

        prev_player = player.in_round(player.round_number - 1)

        if (prev_player.make_changes == False and prev_player.counter == C.ORDER_MAX):
            player.make_changes = False
            player.counter = C.ORDER_MAX
            player.round_order = 0
            player.round_endowment = 0
            player.round_probA = 0
            player.round_probB = 0
            player.round_returnA = 0
            player.round_returnB = 0
            return False
        return True

    form_model = 'player'
    form_fields = ['savings']

    @staticmethod
    def vars_for_template(player: Player):
        #set the counter
        if (player.round_number > 1):
            prev_player = player.in_round(player.round_number-1)

            #if player is altering preferences, counter set to previous round counter
            if (prev_player.make_changes == True):
                player.counter = prev_player.counter

            #if new round, counter set to previous round counter +1
            else:
                player.counter = prev_player.counter + 1
        #if first round, counter set to 0
        else:
            player.counter = 0

        order = C.ROUND_ORDER[player.counter] # if (player.counter <C.ORDER_MAX+1) else 0
        endowment = C.ENDOWMENT[order]
        probA = C.PROBA[order]
        returnA = C.RETURNA[order]
        probB = C.PROBB[order]
        returnB = C.RETURNB[order]

        return dict(
            endowment_display=endowment,
            probA_display=probA,
            returnA_display=returnA,
            probB_display=probB,
            returnB_display=returnB if returnB>0 else "N/A",
            roundNo_display=player.counter+1
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        #writing to memory after clicking submit
        player.round_order = C.ROUND_ORDER[player.counter]
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
        if (prev_player.make_changes == False and prev_player.counter == C.ORDER_MAX):
            return False
        return True

    form_model = 'player'
    form_fields = ['investA']

    @staticmethod
    def vars_for_template(player):
        order = C.ROUND_ORDER[player.counter]
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
            returnB_display=returnB if returnB>0 else "N/A",
            max_investA_display=max_investA,
            roundNo_display=player.counter+1
        )

class Confirm(Page):
    def is_displayed(player):
        if (player.round_number == 1):
            return True

        prev_player = player.in_round(player.round_number - 1)
        if (prev_player.make_changes == False and prev_player.counter == C.ORDER_MAX):
            return False
        return True

    form_model = 'player'
    form_fields = ['make_changes']

    @staticmethod
    def vars_for_template(player):
        #writes choices for use in pages
        order = C.ROUND_ORDER[player.counter]
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
            returnB_display=returnB if returnB>0 else "N/A",
            max_investA_display=max_investA,
            investB_display=investB,
            money_today_display=money_today,
            money_onemonthA_display=money_onemonthA,
            money_onemonthB_display=money_onemonthB,
            roundNo_display = player.counter+1
        )

    #for the barchart
    def js_vars(player):
        order = C.ROUND_ORDER[player.counter]
        money_today = player.savings
        money_onemonthA = C.RETURNA[order] * player.investA
        money_onemonthB = max(0,C.RETURNB[order] * (C.ENDOWMENT[order] - player.savings - player.investA))
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

        # write investB to data
        player.investB = player.round_endowment - player.savings - player.investA

        if player.round_number == 1:
            # initialize participant lists if first round
            participant.monthA = []
            participant.monthB = []
            participant.probA = []
            participant.probB = []
            participant.savings = []

        else:

            order = C.ROUND_ORDER[player.counter]
            participant.monthA.append(C.RETURNA[order] * player.investA)
            participant.monthB.append(max(0, C.RETURNB[order] * (C.ENDOWMENT[order] - player.savings - player.investA)))
            participant.probA.append(player.round_probA)
            participant.probB.append(player.round_probB)
            participant.savings.append(player.savings)
            
        #stage 2 will now play if it is the last stage 1 round
        # DELETE THIS SINCE WE WILL WRITE THIS AS A SEPARATE APP
        if (player.make_changes == False and player.counter == C.ORDER_MAX):
            subsession.order = 1

        # CHECK IF THIS IS THE LAST ROUND AND THERE WERE NO CHANGES 
        if player.counter == C.ORDER_MAX and player.make_changes == False:

    

            # then define the paying round
            paying_round = random.randint(0,C.ORDER_MAX)
            participant.paying_round = paying_round


            #draw number between 0 and 1 that will determine paying asset
            paying_asset_number = random.uniform(0,1) # if less than probA in the paying round then A pays, else B
            participant.paying_asset_number = paying_asset_number

            participant.paying_round_order = participant.paying_round


            # need to call the probability of A that was in the paying round
            player_in_paying_round = player.in_round(paying_round)

            if participant.paying_asset_number <= player_in_paying_round.round_probA:
                participant.paying_asset = "A"

            else:
                participant.paying_asset = "B"

            #set the player's payoffs today and one month from today
            participant.payoff_today = player_in_paying_round.savings

            if participant.paying_asset == "A":
                player_in_paying_round.payoff_oneMonth = player_in_paying_round.investA * player_in_paying_round.round_returnA
            if player.session['paying_asset'] == "B":
                player_in_paying_round.payoff_oneMonth = max(0, player_in_paying_round.investB * player_in_paying_round.round_returnB)

###

page_sequence = [
    InstructionsStageOne,
    ComprehensionStageOne1,
    ComprehensionStageOne2,
    SaveToday,
    InvestA,
    Confirm
]
