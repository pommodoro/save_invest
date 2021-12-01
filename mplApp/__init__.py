from otree.api import *
import json

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mplApp'
    players_per_group = None
    num_rounds = 3
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
class InstructionsStageOne(Page):
    def is_displayed(player):
        return player.round_number == 1

# class ComprehensionStageOne1(Page):
#     def is_displayed(player):
#         return player.round_number == 1

#     form_model = 'player'
#     form_fields = ['comp_instant', 'comp_oneMonthA','comp_oneMonthB']

# class ComprehensionStageOne2(Page):
#     def is_displayed(player):
#         return player.round_number == 1

#     form_model = 'player'
#     form_fields = ['comp_instant', 'comp_oneMonthA','comp_oneMonthB']

# class SaveToday(Page):
#     def is_displayed(player):
#         if (player.round_number == 1):
#             player.session.vars['order'] = 0
#             return True

#         prev_player = player.in_round(player.round_number - 1)

#         if (prev_player.make_changes == False and prev_player.counter ==Constants.order_max):
#             player.make_changes = False
#             player.counter = Constants.order_max
#             player.round_order = 0
#             player.round_endowment = 0
#             player.round_probA = 0
#             player.round_probB = 0
#             player.round_returnA = 0
#             player.round_returnB = 0
#             return False
#         return True

#     form_model = 'player'
#     form_fields = ['savings']

# class InvestA(Page):
#     def is_displayed(player):
#         if (player.round_returnB == -1):
#             player.investA = player.round_endowment - player.savings
#             return False
#         if (player.round_number == 1):
#             return True
#         prev_player = player.in_round(player.round_number - 1)
#         if (prev_player.make_changes == False and prev_player.counter == Constants.order_max):
#             return False
#         return True

#     form_model = 'player'
#     form_fields = ['investA']

#     def vars_for_template(player):
#         order = Constants.round_order[player.counter]
#         endowment = Constants.endowment[order]
#         probA = Constants.probA[order]
#         returnA = Constants.returnA[order]
#         probB = Constants.probB[order]
#         returnB = Constants.returnB[order]
#         max_investA = Constants.endowment[order] - player.savings

#         return dict(
#             endowment_display=endowment,
#             probA_display=probA,
#             returnA_display=returnA,
#             probB_display=probB,
#             returnB_display=returnB if returnB>0 else "N/A",
#             max_investA_display=max_investA,
#             roundNo_display = player.counter+1
#         )

# class Confirm(Page):
#     def is_displayed(player):
#         if (player.round_number == 1):
#             return True
#         prev_player = player.in_round(player.round_number - 1)
#         if (prev_player.make_changes == False and prev_player.counter == Constants.order_max):
#             return False
#         return True
#     form_model = 'player'
#     form_fields = ['make_changes']

#     def vars_for_template(player):
#         #writes choices for use in pages

#         order = Constants.round_order[player.counter]
#         endowment = Constants.endowment[order]
#         probA = Constants.probA[order]
#         returnA = Constants.returnA[order]
#         probB = Constants.probB[order]
#         returnB = Constants.returnB[order]
#         max_investA = Constants.endowment[order] - player.savings
#         investB = Constants.endowment[order] - player.savings - player.investA
#         money_today = player.savings
#         money_onemonthA = Constants.returnA[order] * player.investA
#         money_onemonthB = max(0, Constants.returnB[order] * (
#                         Constants.endowment[order] - player.savings - player.investA))

#         return dict(
#             endowment_display=endowment,
#             probA_display=probA,
#             returnA_display=returnA,
#             probB_display=probB,
#             returnB_display=returnB if returnB>0 else "N/A",
#             max_investA_display=max_investA,
#             investB_display=investB,
#             money_today_display=money_today,
#             money_onemonthA_display=money_onemonthA,
#             money_onemonthB_display=money_onemonthB,
#             roundNo_display = self.player.counter+1
#         )

#     #for the barchart
#     def js_vars(player):
#         order = Constants.round_order[self.player.counter]
#         money_today = player.savings
#         money_onemonthA = Constants.returnA[order] * player.investA
#         money_onemonthB = max(0,Constants.returnB[order] * (Constants.endowment[order] - player.savings - player.investA))
#         chart_series = [money_today, money_onemonthA, money_onemonthB]

#         return dict(
#             money_today_chart=money_today,
#             money_onemonthA_chart=money_onemonthA,
#             money_onemonthB_chart=money_onemonthB,
#             chart_series=chart_series
#         )


#     def before_next_page(player):
#         # write investB to data
#         player.investB = player.round_endowment - player.savings - player.investA

#         #stage 2 will now play if it is the last stage 1 round
#         if (player.make_changes == False and player.counter == Constants.order_max):
#             session.vars['order'] = 1

#         # if the round was payoff-determinative, determine the paying asset and assign the values to variables
#         if player.counter == session.vars['paying_round'] and player.make_changes == False:
#             session.vars['paying_round_order'] = player.round_number

#             if session.vars['paying_asset_number'] <= player.round_probA:
#                 session.vars['paying_asset'] = "A"
#             else:
#                 session.vars['paying_asset'] = "B"

#             #set the player's payoffs today and one month from today
#             player.payoff_today = player.savings
#             if session.vars['paying_asset'] == "A":
#                 player.payoff_oneMonth = player.investA * player.round_returnA
#             if session.vars['paying_asset'] == "B":
#                 player.payoff_oneMonth = max(0, player.investB * player.round_returnB)

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
    #ComprehensionStageOne1,
    #ComprehensionStageOne2.
    #SaveToday,
    #InvestA,
    #Confirm,
    InstructionsStageTwo,
    MplPage,
    Results,
]
