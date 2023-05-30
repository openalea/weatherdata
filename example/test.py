from weatherdata import WeatherDataHub
hub = WeatherDataHub()
lmt = hub.get_ressource(name='no.nibio.lmt')
stations = lmt.stations
sids = stations.index.to_list()
data = lmt.data(parameters=[2001],stationId=[143], timeStart='2022-01-01', timeEnd='2022-12-30', display='ds')
lmt.plot(ds=data, varname='2001')