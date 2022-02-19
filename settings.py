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
    'round_order',
    'paying_round', 
	'paying_asset_number',
	'paying_order_s2',
	'paying_choice_number_s2',
	'paying_asset_s2',
	'paying_round_order',
	'paying_asset',
    'monthA',
    'monthB',
    'probA',
    'probB',
    'savings' 
    ]
	
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5455770345824'
