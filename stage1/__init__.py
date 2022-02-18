from otree.api import *
import json
import random

doc = """
Stage 1 of save invest experiment
"""


class Constants(BaseConstants):
    name_in_url = 'mplApp'
    players_per_group = None
    num_rounds = 1

    order_max = 42 #number of unique rounds in stage1-1

    # randomize order of rounds
    round_order = list(range(1, order_max, 1)) #round order is range from 1 to 43 (or number of unique rounds)

    # print("Original: ", round_order)
    random.shuffle(round_order)
    # print("1 shuffle: ", round_order)

    # repeating the fixed endowment (10) the total number of unique comparisons + 1 since we are never in round 0
    endowment = [10] * 43

    # populating probability A
    probA = [0, 1, 0.1,  0.55, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 0.95, 0.8, 0.3, 0.6, 0.5, 0.95,
    0.2, 0.7, 0.4, 0.5, 0.05, 0.8, 0.3, 0.6, 0.5, 0.95,
    0.2, 0.7, 0.4, 0.5, 0.05, 0.8, 0.3, 0.6, 0.5, 0.95, 
    0.2, 0.7, 0.4, 0.5]

    # populating probability B
    probB = [round(1 - p, 2) for p in probA]

    # populating return to A
    returnA = [0, 2.1,1.9, 2.7, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 
    1.6, 1.7, 1.8, 1.9, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7,
    1.7, 1.7, 1.7, 1.7, 2.4, 2.4, 2.4, 2.4, 2.4, 2.4,
    2.4, 2.4, 2.4, 2.4, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2,
    2.2, 2.2, 2.2, 2.2]

    # populating return to B
    returnB = [0, -1, 2.3, 1.6, -1, -1, -1, -1, -1, -1,
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

    # set min value for input in investA
    def investA_min(player):
        if (player.round_probB == 0):
            return player.round_endowment - player.savings
        return 0

    # set max value for input in investA
    def investA_max(player):
        return player.round_endowment - player.savings

    investB = models.CurrencyField()

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

# PAGES
class InstructionsStageOne(Page):
    def is_displayed(player):
        return player.round_number == 1

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

        if (prev_player.make_changes == False and prev_player.counter == Constants.order_max):
            player.make_changes = False
            player.counter = Constants.order_max
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

        order = Constants.round_order[player.counter] # if (player.counter <Constants.order_max+1) else 0
        endowment = Constants.endowment[order]
        probA = Constants.probA[order]
        returnA = Constants.returnA[order]
        probB = Constants.probB[order]
        returnB = Constants.returnB[order]

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
        player.round_order = Constants.round_order[player.counter]
        player.round_endowment = Constants.endowment[player.round_order]
        player.round_probA = Constants.probA[player.round_order]
        player.round_returnA = Constants.returnA[player.round_order]
        player.round_probB = Constants.probB[player.round_order]
        player.round_returnB = Constants.returnB[player.round_order]


class InvestA(Page):
    def is_displayed(player):
        if (player.round_returnB == -1):
            player.investA = player.round_endowment - player.savings
            return False
        if (player.round_number == 1):
            return True
        prev_player = player.in_round(player.round_number - 1)
        if (prev_player.make_changes == False and prev_player.counter == Constants.order_max):
            return False
        return True

    form_model = 'player'
    form_fields = ['investA']

    @staticmethod
    def vars_for_template(player):
        order = Constants.round_order[player.counter]
        endowment = Constants.endowment[order]
        probA = Constants.probA[order]
        returnA = Constants.returnA[order]
        probB = Constants.probB[order]
        returnB = Constants.returnB[order]
        max_investA = Constants.endowment[order] - player.savings

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
        if (prev_player.make_changes == False and prev_player.counter == Constants.order_max):
            return False

        return True

    form_model = 'player'
    form_fields = ['make_changes']

    @staticmethod
    def vars_for_template(player):
        #writes choices for use in pages

        order = Constants.round_order[player.counter]
        endowment = Constants.endowment[order]
        probA = Constants.probA[order]
        returnA = Constants.returnA[order]
        probB = Constants.probB[order]
        returnB = Constants.returnB[order]
        max_investA = Constants.endowment[order] - player.savings
        investB = Constants.endowment[order] - player.savings - player.investA
        money_today = player.savings
        money_onemonthA = Constants.returnA[order] * player.investA
        money_onemonthB = max(0, Constants.returnB[order] * (
                        Constants.endowment[order] - player.savings - player.investA))

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
        order = Constants.round_order[player.counter]
        money_today = player.savings
        money_onemonthA = Constants.returnA[order] * player.investA
        money_onemonthB = max(0,Constants.returnB[order] * (Constants.endowment[order] - player.savings - player.investA))
        chart_series = [money_today, money_onemonthA, money_onemonthB]

        return dict(
            money_today_chart=money_today,
            money_onemonthA_chart=money_onemonthA,
            money_onemonthB_chart=money_onemonthB,
            chart_series=chart_series
        )


    @staticmethod
    def before_next_page(player, timeout_happened):
        # write investB to data
        player.investB = player.round_endowment - player.savings - player.investA

        #stage 2 will now play if it is the last stage 1 round
        # DELETE THIS SINCE WE WILL WRITE THIS AS A SEPARATE APP
        if (player.make_changes == False and player.counter == Constants.order_max):
            subsession.order = 1

        # CHECK IF THIS IS THE LAST ROUND AND THERE WERE NO CHANGES 
        if player.counter == Constants.order_max and player.make_changes == False:

            # point to the participant attribute
            participant = player.participant

            # then define the paying round
            paying_round = random.randint(0,Constants.order_max)
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

# MUST MOVE THESE TO MPL APP
class InstructionsStageTwo(Page):
    def is_displayed(player: Player):
        return False

class MplPage(Page):
    def is_displayed(player: Player):
        return False

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
        return False

    @staticmethod
    def vars_for_template(player: Player):
        list_of_choices = json.loads(player.options_chosen)
        return {
            "list_of_choices": list_of_choices,
        }
###

page_sequence = [
    InstructionsStageOne,
    ComprehensionStageOne1,
    ComprehensionStageOne2,
    SaveToday,
    InvestA,
    Confirm
]
