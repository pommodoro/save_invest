from otree.api import *
import json
import random

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mplApp'
    players_per_group = None
    num_rounds = 10

    # if the variable below is True, then the variable part of the MPL is displayed on the right, otherwise it is displayed on the left
    display_variable_right = True

    # the list below should contain 1 entry per round
    list_of_fixed_options = [
        "A payoff of $1 for sure",
        "A payoff of $4 for sure",
        "A payoff of $8 for sure",
    ]
    # The list below should contain 1 entry per round
    # It should contain the text of the variable part for a given round
    # {placeholder} will be replace with the items of the array
    list_of_variable_option_texts = [
        "$3 with a probability of {placeholder}%",
        "$7 with a probability of {placeholder}%",
        "$10 with a probability of {placeholder}%",
    ]
    # the list below contains one sublist per round
    # each sublist contains the options displayed in this round
    list_of_lists_of_variable_options = [
        [20, 40, 60],
        [10, 60],
        [65, 75, 85, 95],
    ]

    order_max = 2 #number of unique rounds in stage1-1
    order_max_s2 = 2 #number of unique rounds in stage 2

    # randomize order of rounds
    round_order = list(range(1, order_max+2, 1)) #round order is range from 1 to 43 (or number of unique rounds)
    # print("Original: ", round_order)
    random.shuffle(round_order)
    # print("1 shuffle: ", round_order)


    # input the round parameters
    endowment = [0]
    probA = [0]
    probB = [0]
    returnA = [0]
    returnB = [0]

    endowment.insert(1, 10)
    probA.insert(1, 1)
    probB.insert(1, 0)
    returnA.insert(1, 2.1)
    returnB.insert(1, -1)

    endowment.insert(2, 10)
    probA.insert(2, 0.1)
    probB.insert(2, 0.9)
    returnA.insert(2, 1.9)
    returnB.insert(2, 2.3)

    endowment.insert(3, 10)
    probA.insert(3, 0.55)
    probB.insert(3, 0.45)
    returnA.insert(3, 2.7)
    returnB.insert(3, 1.6)


class Subsession(BaseSubsession):
    def creating_session(player):
        if player.round_number == 1:
            #determine paying round order (between 0 and max round order)
            paying_round = random.randint(0,Constants.order_max)
            player.session.vars['paying_round'] = paying_round

            #draw number between 0 and 1 that will determine paying asset
            paying_asset_number = random.uniform(0,1) # if less than probA in the paying round then A pays, else B
            player.session.vars['paying_asset_number'] = paying_asset_number

            #map from paying_asset_number to the asset letter
            #compare paying_asset_number to the return probability of asset A in the paying round
            #if paying_asset_number <= Constants.probA[Constants.round_order[self.round_number]]:
            #    paying_asset = "A"
            #else: paying_asset = "B"
            #self.session.vars['paying_asset'] = paying_asset


            paying_order_s2 = random.randint(0, Constants.order_max_s2-1)
            player.session. vars['paying_order_s2'] = paying_order_s2

            paying_choice_number_s2 = random.randint(0, 19)
            player.session.vars['paying_choice_number_s2'] = paying_choice_number_s2

            paying_asset_s2 = random.uniform(0,1)
            player.session.vars['paying_asset_number_s2'] = paying_asset_s2

    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # the field contains one record per choice that is either f for fixed or v for variable
    # since we cannot store lists in the database we store the information as a string.
    # If it is needed as a list again (e.g. for payoff calculation) it can be converted 
    # back into a list by importing the json module and using using json.loads()
    options_chosen = models.StringField()

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

    stage1_round = models.IntegerField()
    choice1 = models.IntegerField(
        choices = [
            [1, ''],
            [2, ''],
        ],
        widget = widgets.RadioSelectHorizontal
    )
    choice2 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget = widgets.RadioSelectHorizontal
    )
    choice3 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget = widgets.RadioSelectHorizontal
    )
    choice4 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget = widgets.RadioSelectHorizontal
    )
    choice5 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice6 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget = widgets.RadioSelectHorizontal
    )
    choice7 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice8 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice9 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice10 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice11 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice12 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice13 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget = widgets.RadioSelectHorizontal
    )
    choice14 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice15 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice16 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice17 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice18 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )
    choice19 = models.IntegerField(
        choices=[
            [1, ''],
            [2, ''],
        ],
        widget=widgets.RadioSelectHorizontal
    )


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
    def is_displayed(player):
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
    def vars_for_template(player):
        #set the counter
        if (player.round_number > 1):
            prev_player = player.in_round(player.round_number-1)
            #if player is altering preferences, counter set to previous round counter
            if (prev_player.make_changes == True):
                player.counter = prev_player.counter
            #if new round, counter set to previous round counter +1
            else:
                player.counter = prev_player.counter +1
        #if first round, counter set to 0
        else:
            player.counter = 0

            order = Constants.round_order[player.counter] if (player.counter <Constants.order_max+1) else 0
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

    def before_next_page(player):
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


    def before_next_page(player):
        # write investB to data
        player.investB = player.round_endowment - player.savings - player.investA

        #stage 2 will now play if it is the last stage 1 round
        if (player.make_changes == False and player.counter == Constants.order_max):
            session.vars['order'] = 1

        # if the round was payoff-determinative, determine the paying asset and assign the values to variables
        if player.counter == session.vars['paying_round'] and player.make_changes == False:
            session.vars['paying_round_order'] = player.round_number

            if session.vars['paying_asset_number'] <= player.round_probA:
                session.vars['paying_asset'] = "A"
            else:
                session.vars['paying_asset'] = "B"

            #set the player's payoffs today and one month from today
            player.payoff_today = player.savings
            if session.vars['paying_asset'] == "A":
                player.payoff_oneMonth = player.investA * player.round_returnA
            if session.vars['paying_asset'] == "B":
                player.payoff_oneMonth = max(0, player.investB * player.round_returnB)

class InstructionsStageTwo(Page):
     pass

class MplPage(Page):
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
    @staticmethod
    def vars_for_template(player: Player):
        list_of_choices = json.loads(player.options_chosen)
        return {
            "list_of_choices": list_of_choices,
        }

page_sequence = [
    InstructionsStageOne,
    ComprehensionStageOne1,
    ComprehensionStageOne2,
    SaveToday,
    InvestA,
    Confirm,
    InstructionsStageTwo,
    MplPage,
    Results,
]
