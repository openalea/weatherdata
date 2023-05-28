import pandas
import xarray
import numpy
from weatherdata.ipm import WeatherDataHub, WeatherDataSource

wdh= WeatherDataHub()
source = 'fi.fmi.observation.station'
fmi = wdh.get_ressource(source)

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)

def testDataStationFMI():
    '''
    Test 'Finnish Meteorological Institute measured data' data function for one parameter by argument

    Params:
    -------
        stationId= [101104]
        parameters = [1002,3002]
        timeStart = '2020-06-12'
        timeEnd = '2020-07-03'
        timeZone = 'UTC'

    '''
    
    ## test ds format
    rep_ds=fmi.data(
        stationId=[101104],
        parameters=[1002,3002],
        timeStart = '2020-06-12',
        timeEnd = '2020-07-03',
        timeZone='UTC',
        display="ds")
    assert type(rep_ds) is xarray.Dataset
    assert keys_exists(dict(rep_ds.dims),('location','time'))

    ### test coords
    assert list(rep_ds.coords)==['time', 'location', 'lat', 'lon']
    assert rep_ds.coords['time'].dtype=='<M8[ns]'
    assert rep_ds.coords['time'].attrs=={'name': 'time'}
    assert rep_ds.coords['location'].dtype in ['int32', 'int64']
    assert rep_ds.coords['location'].values==[101104]
    assert rep_ds.coords['lat'].dtype=='float64'
    assert rep_ds.coords['lat'].attrs=={'name': 'latitude', 'unit': 'degrees_north'}
    assert rep_ds.coords['lat'].values==[60.81397]
    assert rep_ds.coords['lon'].dtype=='float64'
    assert rep_ds.coords['lon'].attrs=={'name': 'longitude', 'unit': 'degrees_east'}
    assert rep_ds.coords['lon'].values==[23.49825]

    
    ### test data variable
    assert list(rep_ds.data_vars) == ['1002', '3002']
    assert rep_ds.data_vars['1002'].dtype == 'float64'
    assert rep_ds.data_vars['1002'].attrs == {'id': 1002, 'name': 'Mean air temperature at 2m', 'description': None, 'unit': 'Celcius', 'aggregationType': 'AVG'}    
    assert rep_ds.data_vars['3002'].dtype == 'float64'
    assert rep_ds.data_vars['3002'].attrs == {'id': 3002, 'name': 'Mean RH at 2m', 'description': None, 'unit': '%', 'aggregationType': 'AVG'}    

    ### test ds attribute
    assert type(rep_ds.attrs) is dict
    assert keys_exists(rep_ds.attrs,('weatherRessource','timeStart','timeEnd','parameters'))
    assert rep_ds.attrs['weatherRessource']==source
    assert rep_ds.attrs['timeStart']=='2020-06-12T00:00:00.000000000'
    assert rep_ds.attrs['timeEnd']=='2020-07-03T00:00:00.000000000'
    assert rep_ds.attrs['parameters']==['1002', '3002']

    ###test conversion dataframe
    assert rep_ds.to_dataframe().shape[1]==4
    assert rep_ds.to_dataframe().index.names==['time', 'location']

    # format= json
    rep_json=fmi.data(
        stationId=[101104],
        parameters=[1002,3002],
        timeStart = '2020-06-12',
        timeEnd = '2020-07-03',
        timeZone='UTC',
        display="json")
    assert type(rep_json[0]) is dict
    assert keys_exists(rep_json[0],('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
    assert rep_json[0]['weatherParameters']==[1002, 3002]
    assert rep_json[0]['locationWeatherData'][0]['longitude']==23.49825
    assert rep_json[0]['locationWeatherData'][0]['latitude']==60.81397
    assert rep_json[0]['locationWeatherData'][0]['altitude']==0.0
    


def testDataStationsFMI():
    '''
    Test 'Finnish Meteorological Institute measured data' data function for several parameter by argument

    Params:
    -------
        stationId= [101104,101533]
        parameters = [1002,3002]
        timeStart = '2020-06-12'
        timeEnd = '2020-07-03'
        timeZone = 'UTC'

    '''
    
    ## test ds format
    rep_ds=fmi.data(
        stationId=[101104,101533],
        parameters=[1002,3002],
        timeStart = '2020-06-12',
        timeEnd = '2020-07-03',
        timeZone='UTC',
        display="ds")
    assert type(rep_ds) is xarray.Dataset
    assert keys_exists(dict(rep_ds.dims),('location','time'))

    ### test coords
    assert all(k in list(rep_ds.coords) for k in ['location', 'time', 'lat', 'lon'])
    assert rep_ds.coords['time'].dtype=='<M8[ns]'
    assert rep_ds.coords['time'].attrs=={'name': 'time'}
    assert numpy.all(rep_ds.coords['location'].values==[101104, 101533])
    assert rep_ds.coords['lat'].attrs=={'name': 'latitude', 'unit': 'degrees_north'}
    assert numpy.all(rep_ds.coords['lat'].values==[60.81397, 63.08898])
    assert rep_ds.coords['lon'].attrs=={'name': 'longitude', 'unit': 'degrees_east'}
    assert numpy.all(rep_ds.coords['lon'].values==[23.49825, 24.26084])

    
    ### test data variable
    assert list(rep_ds.data_vars) == ['1002', '3002']
    assert rep_ds.data_vars['1002'].attrs == {'id': 1002, 'name': 'Mean air temperature at 2m', 'description': None, 'unit': 'Celcius', 'aggregationType': 'AVG'}
    assert rep_ds.data_vars['3002'].attrs == {'id': 3002, 'name': 'Mean RH at 2m', 'description': None, 'unit': '%', 'aggregationType': 'AVG'}    

    ### test ds attribute
    assert type(rep_ds.attrs) is dict
    assert keys_exists(rep_ds.attrs,('weatherRessource','timeStart','timeEnd','parameters'))
    assert rep_ds.attrs['weatherRessource']==source
    assert rep_ds.attrs['timeStart']=='2020-06-12T00:00:00.000000000'
    assert rep_ds.attrs['timeEnd']=='2020-07-03T00:00:00.000000000'
    assert rep_ds.attrs['parameters']==['1002', '3002']

    ###test conversion dataframe
    assert rep_ds.to_dataframe().shape[1]==4
    assert all(k in rep_ds.to_dataframe().index.names for k in ['location', 'time'])

    # format= json
    rep_json=fmi.data(
        stationId=[101104,101533],
        parameters=[1002,3002],
        timeStart = '2020-06-12',
        timeEnd = '2020-07-03',
        timeZone='UTC',
        display="json")
    
    assert type(rep_json) is list
    for el in range(len(rep_json)):
        assert type(rep_json[el]) is dict
        assert keys_exists(rep_json[el],('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
        assert rep_json[el]['weatherParameters']==[1002, 3002]
        assert rep_json[el]['locationWeatherData'][0]['longitude'] in [23.49825, 24.26084]
        assert rep_json[el]['locationWeatherData'][0]['latitude'] in [60.81397, 63.08898]
        assert rep_json[0]['locationWeatherData'][0]['altitude']==0.0
