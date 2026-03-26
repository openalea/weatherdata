"""Converters between elaborated python object and basic dicts"""

import xarray as xr
import pandas
import numpy as np

def weather_data_as_xarray(weather_data):
    times = pandas.date_range(start=weather_data["timeStart"],
                              end=weather_data["timeEnd"],
                              freq=str(weather_data["interval"]) + "s",
                              name="time")

    datas = [np.array(weather_data['locationWeatherData'][0]['data']).astype("float")]

    dats = [[data[:, i].reshape(data.shape[0], 1) for i in range(data.shape[1])] for data in datas]

    # construction of dict for dataset variable
    responses = [weather_data]
    data_vars = [{str(response['weatherParameters'][i]): (['time', 'location'], dat[i]) for i in
                  range(len(response['weatherParameters']))} for response in responses for dat in dats]


    coords = [{'time': times.values,
               'location': ([str([responses[el]['locationWeatherData'][0]['latitude'],
                                  responses[el]['locationWeatherData'][0]['longitude']])]),
               'lat': ('location', [responses[el]['locationWeatherData'][0]['latitude']]),
               'lon': ('location', [responses[el]['locationWeatherData'][0]['longitude']]),
               # 'alt':[float(responses[el]['locationWeatherData'][0]['altitude'])]
               } for el in range(len(responses))]

    # list de ds
    list_ds = [xr.Dataset(data_vars[el], coords=coords[el]) for el in range(len(responses))]

    # merge ds
    ds = xr.merge(list_ds)