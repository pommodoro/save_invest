from os import environ

SESSION_CONFIGS = [
    dict(
        name='save_invest',
        app_sequence=[
        'stage1',
        'stage2'],
        num_demo_participants=1,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'order',
    'round_order',
    'paying_round', 
	'paying_asset_number',
	'paying_order_s2',
	'paying_choice_number_s2',
	'paying_asset_s2',
	'paying_round_order',
	'paying_asset',
    'payoff_one_month_s1',
    'payoff_today_s1',
    'payoff_one_month_s2',
    'payoff_today_s2',
    'monthA',
    'monthB',
    'probA',
    'probB',
    'savings',
    's2probA',
    's2probB',
    's2savings',
    's2monthA',
    's2monthB',
    'paying_round_stage_2',
    'paying_row',
    'rts_invest',
    'rts_mpl',
    'rts_save'
    ]
	
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
    dict(
        name='CELSS_lab',
        display_name='CELSS Lab',
        participant_label_file='_rooms/test_participant_file.txt',
        use_secure_urls=False
    ),
]
ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5455770345824'
