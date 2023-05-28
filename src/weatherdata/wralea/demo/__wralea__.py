
# This file has been generated at Tue May 23 15:26:16 2023

from openalea.core import *


__name__ = 'ipmdecisions.weatherdata.demo'

__editable__ = True
__version__ = '1.1.0'
__license__ = 'CECILL-C'
__authors__ = 'Marc Labadie, Christian Fournier, Christophe Pradal'
__institutes__ = 'INRAE/CIRAD'
__description__ = 'WeatherData from IPM'
__url__ = 'https://github.com/H2020-IPM-openalea/weatherdata'
__icon__ = ''
__alias__ = ['']


__all__ = [  'weather']

weather = CompositeNodeFactory(name='weather',
                             description='Application using weather data',
                             category='weather',
                             doc='',
                             inputs=[],
                             outputs=[],
                             elt_factory={  2: ('ipmdecisions.weatherdata', 'WeatherHub'),
   3: ('ipmdecisions.weatherdata', 'WeatherStations'),
   4: ('ipmdecisions.weatherdata', 'resources'),
   5: ('openalea.python method', 'print')},
                             elt_connections={4329367824: (2, 0, 3, 0), 4329367856: (2, 0, 4, 0), 4329367888: (4, 0, 5, 0)},
                             elt_data={  2: {  'block': False,
         'caption': 'WeatherHub',
         'delay': 0,
         'hide': True,
         'id': 2,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 25.866983372921613,
         'posy': 14.422802850356295,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   3: {  'block': False,
         'caption': 'WeatherStations',
         'delay': 0,
         'hide': True,
         'id': 3,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -3.083501513959944,
         'posy': 49.336024223359104,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   4: {  'block': False,
         'caption': 'resources',
         'delay': 0,
         'hide': True,
         'id': 4,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -118.59621207538245,
         'posy': 37.00201816751934,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   5: {  'block': False,
         'caption': 'print',
         'delay': 0,
         'hide': True,
         'id': 5,
         'lazy': False,
         'port_hide_changed': set(),
         'posx': -103.65308935388428,
         'posy': 69.02299542787263,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   '__in__': {  'block': False,
                'caption': 'In',
                'delay': 0,
                'hide': True,
                'id': 0,
                'lazy': True,
                'port_hide_changed': set(),
                'posx': 0,
                'posy': 0,
                'priority': 0,
                'use_user_color': True,
                'user_application': None,
                'user_color': None},
   '__out__': {  'block': False,
                 'caption': 'Out',
                 'delay': 0,
                 'hide': True,
                 'id': 1,
                 'lazy': True,
                 'port_hide_changed': set(),
                 'posx': 0,
                 'posy': 0,
                 'priority': 0,
                 'use_user_color': True,
                 'user_application': None,
                 'user_color': None}},
                             elt_value={  2: [],
   3: [(1, "'Landbruksmeteorologisk tjeneste'")],
   4: [],
   5: [],
   '__in__': [],
   '__out__': []},
                             elt_ad_hoc={  2: {'position': [25.866983372921613, 14.422802850356295], 'userColor': None, 'useUserColor': False},
   3: {'position': [-3.083501513959944, 49.336024223359104], 'userColor': None, 'useUserColor': False},
   4: {'position': [-118.59621207538245, 37.00201816751934], 'userColor': None, 'useUserColor': False},
   5: {'position': [-103.65308935388428, 69.02299542787263], 'userColor': None, 'useUserColor': False},
   '__in__': {'position': [0, 0], 'userColor': None, 'useUserColor': True},
   '__out__': {'position': [0, 0], 'userColor': None, 'useUserColor': True}},
                             lazy=True,
                             eval_algo='LambdaEvaluation',
                             )




