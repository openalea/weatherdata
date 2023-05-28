from openalea.core import *

__name__ = "ipmdecisions.weatherdata"
__version__ = '1.1.0'
__license__ = 'CECILL-C'
__authors__ = 'Marc Labadie, Christophe Pradal, Christian Fournier'
__institutes__ = 'INRAE/CIRAD'
__description__ = 'Intercropping for pest management'
__url__ = 'https://github.com/H2020-IPM-openalea/weatherdata'

__editable__ = 'True'
__icon__ = 'icon_cloud.png'
__alias__ = [""] # Aliases for compatibitity

__all__ = """
WeatherHub
resources
WeatherStations
""".split()

WeatherHub = Factory(name='WeatherHub',
                 description='WeatherDataHub that list all the resources available',
                 category='Weather',
                 nodemodule='weatherdata.wralea.adaptw',
                 nodeclass='WeatherHub',
                 )
resources =  Factory(name='resources',
                 description='List of resources with their description',
                 category='Weather',
                 nodemodule='weatherdata.wralea.adaptw',
                 nodeclass='resources',
                 )

WeatherStations =  Factory(name='WeatherStations',
                 description='Select a weather provider',
                 category='Weather',
                 nodemodule='weatherdata.wralea.adaptw',
                 nodeclass='WeatherStations',
                 )