import pandas
import xarray
import numpy
from openalea.weatherdata.ipm import WeatherDataHub, WeatherDataSource

wdh= WeatherDataHub()
source = 'no.met.locationforecast'
norway = wdh.get_ressource(source)

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)

def testDataStationMetNorway():
    '''
    Test Met_Norway data function

    Params:
    -------
        latitude:(list) [67.2828]
        longitude: (list) [14.3711]
        altitude:(list) [70]
    '''
    
    # Met Norway Locationforecast resource
    ## test ds format
    rep_ds=norway.data(latitude=[67.2828],longitude=[14.3711],altitude=[70], parameters=[1001, 3001, 2001, 4002],display="ds")
    assert type(rep_ds) is xarray.Dataset
    
    ### test coords
    assert list(rep_ds.coords)==['time', 'location', 'lat', 'lon']
    assert rep_ds.coords['time'].dtype=='<M8[ns]'
    assert rep_ds.coords['time'].attrs=={}
    assert rep_ds.coords['location'].dtype=='<U18'
    assert rep_ds.coords['location'].values=='[67.2828, 14.3711]'
    #assert rep_ds.coords['location'].attrs=={'name': '[latitude,longitude]'}
    assert rep_ds.coords['lat'].dtype=='float64'
    assert rep_ds.coords['lat'].attrs=={'name': 'latitude', 'unit': 'degrees_north'}
    assert rep_ds.coords['lat'].values==[67.2828]
    assert rep_ds.coords['lon'].dtype=='float64'
    assert rep_ds.coords['lon'].attrs=={'name': 'longitude', 'unit': 'degrees_east'}
    assert rep_ds.coords['lon'].values==[14.3711]

    
    ### test data variable
    assert list(rep_ds.data_vars) == ['1001', '3001', '2001', '4002']
    assert rep_ds.data_vars['1001'].dtype == 'float64'
    assert rep_ds.data_vars['1001'].attrs == {'id': 1001, 'name': 'Instantaneous temperature at 2m', 'description': None, 'unit': 'Celcius','aggregationType': 'AVG'}    
    assert rep_ds.data_vars['3001'].dtype == 'float64'
    assert rep_ds.data_vars['3001'].attrs == {'id': 3001, 'name': 'Instantaneous RH at 2m (%)', 'description': None, 'unit': '%', 'aggregationType': 'AVG'}    
    assert rep_ds.data_vars['2001'].dtype == 'float64'
    assert rep_ds.data_vars['2001'].attrs == {'id': 2001, 'name': 'Precipitation', 'description': None, 'unit': 'mm', 'aggregationType': 'SUM'}
    assert rep_ds.data_vars['4002'].dtype == 'float64'
    assert rep_ds.data_vars['4002'].attrs == {'id': 4002, 'name': 'Instantaneous wind speed at 2m', 'description': None, 'unit': 'm/s','aggregationType': 'AVG'}

    ### test ds attribute
    assert type(rep_ds.attrs) is dict
    assert keys_exists(rep_ds.attrs,('weatherRessource','timeStart','timeEnd','parameters'))
    assert rep_ds.attrs['weatherRessource']==source
    #assert rep_ds.attrs['timeStart']=='2022-05-23T09:00:00.000000000'
    #assert rep_ds.attrs['timeEnd']=='2022-06-01T18:00:00.000000000'
    assert rep_ds.attrs['parameters']==['1001', '3001', '2001', '4002']

    ###test conversion dataframe
    assert rep_ds.to_dataframe().shape[1]==6
    assert rep_ds.to_dataframe().index.names==['time', 'location']

"""
def testDataStationsMetNorway():
    '''
    Test Met_Norway data function

    Params:
    -------
        latitude:(list) [67.2828, 68.3737]
        longitude: (list) [14.3711, 10.1515]
        altitude:(list) [70, 0]
    '''
    
    # Met Norway Locationforecast resource
    ## test ds format
    rep_ds=norway.data(latitude=[67.2828, 68.3737],longitude=[14.3711, 10.1515],altitude=[70, 0],
                       parameters=[1001, 3001, 2001, 4002],display="ds")
    assert type(rep_ds) is xarray.Dataset
    assert keys_exists(dict(rep_ds.dims),('alt','lat','location','lon','time'))
    
    ### test coords
    assert list(rep_ds.coords)==['alt', 'lat', 'location', 'time', 'lon']
    assert rep_ds.coords['time'].dtype=='<M8[ns]'
    assert rep_ds.coords['time'].attrs=={}
    assert rep_ds.coords['location'].dtype=='<U18'
    assert numpy.all(rep_ds.coords['location'].values==['[67.2828, 14.3711]','[68.3737, 10.1515]'])
    assert rep_ds.coords['location'].attrs=={'name': '[latitude,longitude]'}
    assert rep_ds.coords['lat'].dtype=='float64'
    assert rep_ds.coords['lat'].attrs=={'name': 'latitude', 'unit': 'degrees_north'}
    assert numpy.all(rep_ds.coords['lat'].values==[67.2828,68.3737])
    assert rep_ds.coords['lon'].dtype=='float64'
    assert rep_ds.coords['lon'].attrs=={'name': 'longitude', 'unit': 'degrees_east'}
    assert numpy.all(rep_ds.coords['lon'].values==[10.1515,14.3711])
    assert rep_ds.coords['alt'].dtype=='float64'
    assert rep_ds.coords['alt'].attrs=={'name': 'altitude', 'unit': 'meters'}
    assert numpy.all(rep_ds.coords['alt'].values==[0.,70])
    
    ### test data variable
    assert list(rep_ds.data_vars) == ['1001', '3001', '2001', '4002']
    assert rep_ds.data_vars['1001'].dtype == 'float64'
    assert rep_ds.data_vars['1001'].attrs == {'id': 1001, 'name': 'Instantaneous temperature at 2m', 'description': None, 'unit': 'Celcius'}    
    assert rep_ds.data_vars['3001'].dtype == 'float64'
    assert rep_ds.data_vars['3001'].attrs == {'id': 3001, 'name': 'Instantaneous RH at 2m (%)', 'description': None, 'unit': '%'}    
    assert rep_ds.data_vars['2001'].dtype == 'float64'
    assert rep_ds.data_vars['2001'].attrs == {'id': 2001, 'name': 'Precipitation', 'description': None, 'unit': 'mm'}
    assert rep_ds.data_vars['4002'].dtype == 'float64'
    assert rep_ds.data_vars['4002'].attrs == {'id': 4002, 'name': 'Instantaneous wind speed at 2m', 'description': None, 'unit': 'm/s'}

    ### test ds attribute
    assert type(rep_ds.attrs) is dict
    assert keys_exists(rep_ds.attrs,('weatherRessource','longitude','latitude','timeStart','timeEnd','parameters'))
    assert rep_ds.attrs['weatherRessource']==source
    assert rep_ds.attrs['longitude']==[10.1515,14.3711]
    assert rep_ds.attrs['latitude']==[67.2828,68.3737]
    assert rep_ds.attrs['parameters']==['1001', '3001', '2001', '4002']

    ###test conversion dataframe
    assert rep_ds.to_dataframe().shape[1]==4
    assert rep_ds.to_dataframe().index.names==['alt', 'lat', 'location', 'lon', 'time']

    # format= json
    rep_json=norway.data(latitude=[67.2828, 68.3737],longitude=[14.3711, 10.1515],altitude=[70,0.],display="json")

    assert type(rep_json) is list
    for el in range(len(rep_json)):
        assert(type(rep_json[el]) is  dict)
        assert keys_exists(rep_json[0],('timeStart', 'timeEnd', 'interval', 'weatherParameters', 'locationWeatherData'))
        assert rep_json[el]['weatherParameters']==[1001, 3001, 2001, 4002]
        assert rep_json[el]['locationWeatherData'][0]['longitude'] in [14.3711, 10.1515]
        assert rep_json[el]['locationWeatherData'][0]['latitude'] in [67.2828, 68.3737]
        assert rep_json[el]['locationWeatherData'][0]['altitude'] in [70,0.]
"""
