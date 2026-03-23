from openalea.core import *
from openalea.weatherdata import WeatherDataHub


def WeatherHub():
    """ Return WeatherDataHub that list all the resources available. """
    return WeatherDataHub(),

def resources(hub):
    return hub.list_resources,

class WeatherSources(Node):
    """ List all the weather sources From IPM platform."""
    sources = None
    def __init__(self):
        Node.__init__(self)

        hub = WeatherDataHub()
        rs = hub.list_resources
        if self.sources is None:
            self.sources = dict((v,k) for k, v in dict(rs.name).items())
        v, k = next(iter(self.sources.items()))
        
        print('init source : ', v,k)

        inputs=[ {'interface': None, 'name': 'WeatherHub', 'value': None}, 
                {'interface': IEnumStr(self.sources.keys()), 'name': 'sources', 'value': v}, 
                ]
        [self.add_input(**kwds) for kwds in inputs]
        self.add_output(name='WeatherSources')

    def __call__(self, inputs):
        hub, source = inputs 
        #print(hub, source)
        source_id = self.sources[source]
        fmi = hub.get_ressource(name=source_id)
        return fmi

class WeatherStations(Node):
    """ List all the weather Stations From IPM platform."""
    def __init__(self):
        Node.__init__(self)

        inputs=[ {'interface': None, 'name': 'WeatherSource', 'value': None}, 
                ]
        [self.add_input(**kwds) for kwds in inputs]
        self.add_output(name='WeatherStations', interface='ISequence')

    def __call__(self, inputs):
        source = inputs[0]
        stations = []
        try:
            stations = source.stations.index.to_list()
        except:
            stations = [143]
        return stations,

def weather_data(source, stations=[143], parameters=[2001], timeStart='2022-01-01', timeEnd='2022-12-30', timezone='UTC'):
    """ Return Weather data as an xarray.

    Parameters:
        - source : weather data provider
        - stations (list) : list of station identifiers
        - parameters (list): list of weather parameters requested 
        - timeStart : the fist date of the time serie
        - timeEnd : the end date of the time serie
        - timezone (str): the time zone (eg Europe/Paris)

    Returns:
        - weather data (xarray)
    """
    return source.data(parameters=parameters,stationId=stations, 
                       timeStart=timeStart, timeEnd=timeEnd, 
                       display='ds'),

def plot(source, data, varname='2001'):
    """ Plot Weather data as an xarray.

    Parameters:
        - source : weather data provider
        - stations (list) : list of station identifiers
        - parameters (list): list of weather parameters requested 
        - timeStart : the fist date of the time serie
        - timeEnd : the end date of the time serie
        - timezone (str): the time zone (eg Europe/Paris)

    Returns:
        - weather data (xarray)
    """
    res = source.plot(ds=data, varname=varname)
    return res,

