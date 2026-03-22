import pandas
import xarray
import numpy
from openalea.weatherdata.ipm import WeatherDataHub, WeatherDataSource

wdh= WeatherDataHub()
list_resources = wdh.__resources__.keys()
observation_source = 'no.nibio.lmt'
forecast_source = 'no.met.locationforecast'

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)

def testListRessource():
    '''
    Test list_ressource function
    '''
    rep= wdh.list_resources
    assert type(rep) is pandas.DataFrame, rep
    assert list(rep.columns) == ['name', 'description', 'parameters']
    assert observation_source in rep.index
    assert forecast_source in rep.index


def testGetRessource():
    '''
    Test get resource functoin for all ressources
    '''

    rep=wdh.get_ressource(observation_source)
    assert isinstance(rep,WeatherDataSource)
    rep=wdh.get_ressource(forecast_source)
    assert isinstance(rep,WeatherDataSource)


def testStationId():
    '''
    Test station_id function
    '''

    # Finnish Meteorological Institute measured data resource
    stations = wdh.get_ressource('fi.fmi.observation.station').stations
    assert type(stations) is pandas.DataFrame
    assert len(stations) > 10
    assert all(col in stations.columns for col in ['name', 'latitude','longitude'])
    # Landbruksmeteorologisk tjeneste resource
    stations = wdh.get_ressource('no.nibio.lmt').stations
    assert type(stations) is pandas.DataFrame
    assert len(stations) > 10
    assert all(col in stations.columns for col in ['name', 'latitude','longitude'])
   # MeteoBot API resource
    stations = wdh.get_ressource('com.meteobot').stations
    assert type(stations) is pandas.DataFrame
    assert len(stations) > 10
    assert all(col in stations.columns for col in ['name', 'latitude','longitude'])


def testParameters():
    '''
    Test parameters function for all resources
    '''
    parameters = wdh.get_ressource(forecast_source).parameter
    assert type(parameters) is pandas.DataFrame
    assert list(parameters.id) == [1001, 2001, 3001, 4002]


def testCheckForcast():
    '''
    Test check_forcast function for all ressources
    '''
    assert wdh.get_ressource(forecast_source).forecast
    assert not wdh.get_ressource(observation_source).forecast
