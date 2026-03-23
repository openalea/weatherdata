# -*- python -*-
# -*- coding:utf-8 -*-
#
#       Copyright 2020 INRAE-CIRAD
#       Distributed under the Cecill-C License.
#       See https://cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
# ==============================================================================


from unicodedata import name
import pandas
import datetime
import xarray as xr
import numpy as np
import os
import json
import logging
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfea

from openalea.agroservices.ipm.ipm import IPM
import openalea.agroservices.ipm.fakers as fakers

from .settings import pathCache

logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.INFO)

class WeatherDataHub:    
    """
        Allows to access at IPM weather resources 
        give the list of weather adapter (resources) available on IPM and allows access to weather data source
        
        ..doctest::
        >>> wsh = WeatherDataHub()
        >>> resources = wsh.list_resources()
        >>> wsh.get_resource(name = resources.name.iat[0])

    """

    def __init__(self):
        """
            Give an access to IPM interface from agroservice
        """
        self.ipm = IPM()
        self.sources = None
        self.local_sources={}
    
    @property
    def __resources__(self):
        
        if self.sources is None:
            self.sources= self.ipm.get_weatherdatasource()
            
        if len(self.local_sources)>0:
            self.sources.update(self.local_sources)
        
        return self.sources
    
    @property
    def list_resources(self):
        """ display a dataframe of list of resources with their description 

        Returns
        -------
        pandas.DataFrame
            name and description of available weatherdatasource on IPM service
        """  
        # if local:
        #     return list(self.local_sources)
            
        # else: 
        df= pandas.DataFrame(self.__resources__).T
        return df.loc[:,["name","description","parameters"]]
    
    @property                 
    def parameters(self):
        ipm_parameter=self.ipm.get_parameter()
        return pandas.DataFrame.from_records(ipm_parameter)

    def __forecast__(self):
        return {key:bool(value["temporal"]["forecast"])for key,value in self.__resources__.items()}
    
    def __endpoint__(self):
        return {key: value["endpoint"] for key, value in self.__resources__.items()}
    
        
    def get_ressource(self, name:str):
        """ Get ressource from WeatherDataSource

        Parameters
        ----------
        name : str
             name of weatherdatasource (available in list ressource)

        Returns
        -------
        WeatherDataSource
           weatherdatasource with the name of resource

        Raises
        ------
        NotImplementedError
            the resource is unknown or the name of the resource is misspelled
        """        
        if name in self.local_sources:
            return WeatherDataSource(name=name,forecast=None,endpoint=None,df=self.local_sources[name]["endpoint"])
        else:
            keys = [item for item in self.__resources__]
            if name in keys:
                return WeatherDataSource(name,forecast=self.__forecast__()[name],endpoint=self.__endpoint__()[name])
            else:
                raise NotImplementedError("the resource is unknown or the name of the resource is misspelled")
            
        
    def add_local_ressource(self,
                            name,
                            data, 
                            longitude=3.87,
                            latitude=43.61,
                            altitude=0,
                            timezone="Europe/Paris",
                            interval=3600,
                            convert_name={
                                'temperature_air': 1002,
                                "relative_humidity": 3001,
                                "rain": 2001,
                                "wind_speed": 4005,
                                "global_radiation": 5001}):
        
        data = data.rename(columns=convert_name)
        
        data.attrs={"longitude":longitude,
                    "latitude":latitude,
                    "altitude":altitude,
                    "timezone":timezone,
                    "interval":interval}
        
        d={"personal_data":{
            "id":"personal data",
           "name": name,
           "description": "personal data",
           "public_URL": None,
           "endpoint":data,
           "authentication_type":None,
           "needs_data_control":False,
           "access_type":'location',
           "priority":0,
           "temporal" : {"forecast" : None,
                         "historic" : {"start": data.index.tolist()[0].strftime('%Y-%m-%d'),
                                       "end": data.index.tolist()[-1].strftime('%Y-%m-%d'),
                                       "interval" : [interval]}
                          },
           "parameters" : {'common': data.columns.tolist(), 'optional': None},
           "spatial" : None,
           "organization" : None}
        }
        
        self.local_sources.update(d)
        return data
        
    def __data_reader__(self,path=r'C:\Users\mlabadie\Documents\GitHub\weatherdata\example\Boigneville_2012_2013_h.csv',sep=';',column_name=['date', 'h', 'temperature_air',
                                             'relative_humidity', 'rain',
                                             'wind_speed', 'global_radiation'],skiprows=2,dec=","):
        r""" Reader for my data boignonville

        Parameters
        ----------
        path : regexp, optional
            file path, by default r'C:\Users\mlabadie\Documents\GitHub\weatherdata\example\Boigneville_2012_2013_h.csv'
        sep : str, optional
            type of separator in my data, by default ';'
        column_name : list, optional
            column_name of data, by default ['date', 'h', 'temperature_air', 'relative_humidity', 'rain', 'wind_speed', 'global_radiation']
        skiprows : int, optional
        line of data begin, by default 2
        dec : str, optional
            type of decimal used in my file, by default ","
        """
        data=pandas.read_csv(path, names=column_name,
                            sep=';', skiprows=skiprows, decimal=dec,encoding='latin-1')
        data.index = pandas.to_datetime(data['date'].map(str) + ' ' + data['h'],
                                        dayfirst=True)
        data['date'] = data.index
        
        # convert Rg J/cm2 -> J.m-2.s-1
        data['global_radiation'] *= (10000. / 3600)
        
        # convert Global radiation to PPFD -> µmol.m-2.s-1
        #data["Par"]=data["global_radiation"]*0.48*4.6
        
        # convert wind km/h -> m.s-1
        data['wind_speed'] *= (1000. / 3600)
        data=data.drop(columns=["date", "h"])
        
        return data    
            

class WeatherDataSource(object):
    def __init__(self, name, forecast,endpoint,df=None):
        self.name = name
        self.forecast=forecast
        self.endpoint=endpoint
        self.sources=WeatherDataHub().__resources__
        self.ipm = IPM()
        self.df= df 
    
        # WeatherDataHub.__init__(self)   
  
    @property
    def __source__(self):
        
        # if self.sources is None:
        #     self.sources=self.__resources__
            
        source= self.sources[self.name]
        return source
          
    
    @property               
    def parameter(self):
        df= WeatherDataHub().parameters
        list_parameters= self.__source__["parameters"]["common"]
        
        if self.__source__["parameters"]["optional"]:
            list_parameters.append(list_parameters)
            
        
        return df[df["id"].isin(list_parameters)]
    
    
    @property
    def stations(self):
        stations = {}
        if "features" in self.__source__["spatial"]["geoJSON"]:
            features = self.__source__["spatial"]["geoJSON"]['features']
            def _get_id(feature):
                if 'id' in feature:
                    return int(feature['id'])
                else:
                    return int(feature['properties']['id'])
            def _get_properties(feature):
                properties = feature["properties"]
                coord = feature['geometry']['coordinates']
                properties.update(dict(latitude=float(coord[0]), longitude=float(coord[1])))
                return properties
                #recupère les infos stations dans une properties
            stations={_get_id(feature): _get_properties(feature) for feature in features}
        df = pandas.DataFrame(stations).T
        return df

    def data(self,
             parameters =None,
             stationId =None,
             timeStart = '2020-06-12',
             timeEnd = '2020-07-03',
             timeZone = "UTC",
             altitude = [70.0],
             longitude = [14.3711],
             latitude = [67.2828],
             credentials = None,
             interval = 3600,
             display ='ds',
             varname = 'id',
             usecache =False,
            savecache =False):
        
        responses=[]

        times = pandas.date_range(timeStart, timeEnd, freq=str(interval) + 's', tz=timeZone)
        # time transformation for query format
        timeStart = datetime.datetime.isoformat(times[0])
        timeEnd = datetime.datetime.isoformat(times[-1])
        interval = pandas.Timedelta(times.freq).seconds

        param_list = []
        path_list = []

        if self.forecast== False:
            for station in stationId:
                params = fakers.weather_adapter_params(self.__source__,
                                                        station_id=station,
                                                        time_start=timeStart,
                                                        time_end=timeEnd,
                                                        interval=interval,
                                                        parameters=parameters)
                path=os.path.join(pathCache(),str(station)+'_'+str(parameters)+"_"+timeStart.split("T")[0]+"_"+timeEnd.split("T")[0]+'.json')

                param_list.append(params)
                path_list.append(path)
        else:
            stationId = None # controls the behaviour of response parsing to xarray
            for el in range(len(latitude)):
                path = os.path.join(pathCache(),
                                    str(altitude[el]) + '_' + str(latitude[el]) + "_" + str(longitude[el]) + '.json')
                params = fakers.weather_adapter_params(self.__source__,
                                                        latitude=latitude[el],
                                                        longitude=longitude[el],
                                                        time_start=timeStart,
                                                        time_end=timeEnd,
                                                        interval=interval,
                                                        parameters=parameters)
                param_list.append(params)
                path_list.append(path)

        for params, path in zip(param_list, path_list):
            if self.forecast == False:
                logging.info('start connecting to station %s' % station)

            if usecache and os.path.exists(path):
                with open(path) as f:
                    data=json.load(f)
            else:
                data = self.ipm.get_weatheradapter(self.__source__,
                                params,
                                credentials=credentials)

            if type(data) is dict:
                responses.append(data)
            elif type(data) is int:
                logging.warning('HTTPError: %s for %s' %(data,station))

            if savecache and type(data) is dict:
                with open(path,'w') as f:
                    json.dump(data, f)

        if display=="ds":
            return self.__convert_xarray_dataset__(responses,stationId,varname,display)
        else:
            return responses
    
    def __convert_xarray_dataset__(self, responses,stationId,varname,display):
        
        if display != "ds":
            return responses
        else:          
            times=pandas.date_range(start=responses[0]["timeStart"],
                                    end=responses[0]["timeEnd"],
                                    freq=str(responses[0]["interval"])+"S",
                                    name="time")
            
            #times.strftime('%Y-%m-%dT%H:%M:%S')
            
            datas= [np.array(response['locationWeatherData'][0]['data']).astype("float") for response in responses]
            
            dats = [[data[:,i].reshape(data.shape[0],1) for i in range(data.shape[1])] for data in datas]
            

            # construction of dict for dataset variable
            data_vars=[{str(response['weatherParameters'][i]):(['time','location'],dat[i]) for i in range(len(response['weatherParameters']))} for response in responses for dat in dats]

            # construction dictionnaire coordonnée
            if stationId:
                coords=[{'time':times.values,
                'location':([stationId[el]]),
                'lat':("location",[float(responses[el]['locationWeatherData'][0]['latitude'])]),
                'lon':("location",[float(responses[el]['locationWeatherData'][0]['longitude'])]),
                #'alt':[float(responses[el]['locationWeatherData'][0]['altitude'])]
                } 
                for el in range(len(responses))]
                
            else:
                coords=[{'time':times.values,
                        'location':([str([responses[el]['locationWeatherData'][0]['latitude'],responses[el]['locationWeatherData'][0]['longitude']])]),
                        'lat':('location',[responses[el]['locationWeatherData'][0]['latitude']]),
                        'lon':('location',[responses[el]['locationWeatherData'][0]['longitude']]),
            #'alt':[float(responses[el]['locationWeatherData'][0]['altitude'])]
            } for el in range(len(responses))]
                
                    
            # list de ds
            list_ds=[xr.Dataset(data_vars[el], coords=coords[el]) for el in range(len(responses))]
            
            #merge ds
            ds=xr.merge(list_ds)
            
            #add coordinates attributes
            if stationId:
                ds.coords['time'].attrs["name"]="time"
                ds.coords['location'].attrs['name']= 'WeatherStationId'
                ds.coords['lat'].attrs['name']='latitude'
                ds.coords['lat'].attrs['unit']='degrees_north'
                ds.coords['lon'].attrs['name']='longitude'
                ds.coords['lon'].attrs['unit']='degrees_east'
            else:
                #ds.coords['location'].attrs['name']='[latitude,longitude]'
                ds.coords['lat'].attrs['name']='latitude'
                ds.coords['lat'].attrs['unit']='degrees_north'
                ds.coords['lon'].attrs['name']='longitude'
                ds.coords['lon'].attrs['unit']='degrees_east'
            
            # add data variable  attributes
            param = self.ipm.get_parameter()
            p={str(item['id']): item for item in param if item['id'] in responses[0]['weatherParameters']}
                    
                
            for el in list(ds.data_vars):
                try:
                    ds.data_vars[el].attrs=p[str(el)]
                except KeyError as e:
                    logging.exception("The weatherParameter not implemented; key error: %s".format(e))
            
            # Attribute of dataset
            if stationId:
                ds.attrs['weatherRessource']=self.name
                #ds.attrs['weatherStationId']=stationId
                ds.attrs['timeStart']=str(ds.coords['time'].values[0])
                ds.attrs['timeEnd']=str(ds.coords['time'].values[-1])
                ds.attrs['parameters']=list(ds.data_vars)
            else:
                ds.attrs['weatherRessource']=self.name
                ds.attrs['timeStart']=str(ds.coords['time'].values[0])
                ds.attrs['timeEnd']=str(ds.coords['time'].values[-1])
                ds.attrs['parameters']=list(ds.data_vars)
            
            if varname=="name":
                ds= ds.rename_vars(name_dict={str(ds[el].attrs['id']):ds[el].attrs['name'] for el in list(ds.keys())}) 
                
        return ds
    
    def __dataset_to_ipm__(self,ds:xr.Dataset):
        """Parser from dataset to weather ouput IPM format

        Parameters
        ----------
        ds : xr.Dataset
            weatherdata in xarray dataset format

        Returns
        -------
        dict
            IPM weather data from IPM weatherdata format
        """
        
        timeStart=pandas.to_datetime(ds.time.values[0])
        timesecondDate= pandas.to_datetime(ds.time.values[1])
        timeEnd=pandas.to_datetime(ds.time.values[-1])
        
        interval= timesecondDate-timeStart
        interval=interval.seconds
        
        timeStart=timeStart.strftime("%Y-%m-%dT%H:%M")+"Z"
        timeEnd=timeEnd.strftime("%Y-%m-%dT%H:%M")+"Z"
        
        # parser ipm format
        d={"timeStart":timeStart,
        "timeEnd":timeEnd,
        "interval":interval,
        'weatherParameters':[int(el) for el in list(ds.data_vars)],
        "locationWeatherData":[{"longitude":float(ds.lon.values),
                                "latitude":float(ds.lat.values),
                                "altitude":0,
                                "amalgamation":list(np.repeat(0,len(ds.data_vars))),
                                "data":ds.to_dataframe().drop(columns=['lat','lon']).to_numpy().tolist(),
                                "qc":list(np.repeat(0,len(ds.data_vars))),
                                "width":len(ds.data_vars),
                                "length":len(ds.time)}]}
        return [d]
    
    def to_ipm(self,
                       display="json"):
        """Convert weather dataframe into IPM weather output schema

        Parameters
        ----------
        longitude : float, optional
            longitudinal coordinate in degree of the weather dataframe, by default 3.87
        latitude : float, optional
            latitude coordinate in degree of the weather dataframe  , by default 43.61
        altitude : float, optional
            altitude coordinate in degree of the weather dataframe, by default 0.0
        timezone : str, optional
            time zone of dataframe eg. Europe/Paris if weatherdata is in france, by default "Europe/Paris"
        interval : int, optional
            interval time between index in second eg 3600 if weather data is in hour , by default 3600
        convert_name : dict, optional
            dict of conversion between weather dataframe and ipm parameters, by default {'temperature_air':1002, "relative_humidity":3001, "rain":2001, "wind_speed":4005, "global_radiation":5001}
        display : str, optional
            choose the type of data according json schema ipm or ds in xarray.dataset , by default "json"

        Returns
        -------
        json or xarray.dataset
            return data in weatherdata according to ipm input (json) or in xarray.dataset (ds)
        """
        
        
        data=self.endpoint
        if data is None:
            data = self.df

        time=pandas.date_range(start=data.index.tolist()[0],
                               end=data.index.tolist()[-1],
                               tz=data.attrs["timezone"],
                               freq=str(data.attrs["interval"])+"s").tz_convert("UTC").strftime('%Y-%m-%dT%H:%M:%S')+"Z"
        
        weather_ipm_schema={}
        weather_ipm_schema["timeStart"]=time.tolist()[0]
        weather_ipm_schema["timeEnd"]=time.tolist()[-1]
        weather_ipm_schema["interval"]=data.attrs["interval"]
        weather_ipm_schema['weatherParameters']=data.columns.to_list()
        weather_ipm_schema["locationWeatherData"]=[
            {"longitude":data.attrs["longitude"],
            "latitude":data.attrs["latitude"],
            "altitude":data.attrs["altitude"],
            "amalgamation":np.repeat(0,data.shape[1]).tolist(),
            "data":np.array(data).tolist(),
            "qc":np.repeat(0,data.shape[1]).tolist(),
            "width":data.shape[1],
            "length":data.shape[0]}
        ]
        
        if display=="ds":
            return self.__convert_xarray_dataset__([weather_ipm_schema],stationId=None,varname="id",display="ds")
        else:
            responses=weather_ipm_schema
        return [responses]
    
    def station_plot(self,ds=None,varname=None,time=None,resample=None):
        """_summary_

        Parameters
        ----------
        ds : xarray.Dataset
            xarray.dataset from weather ressources
        varname : str, optional
        variable name to plot, if None plot station localisation by default None
        time : int, optional
            index of time, by default None
        resample : str, optional
            frequency that data can be resampling. resampling calculate is mean function according ds.time eg d for days, by default None
        """
        ext_lat_min=int(ds.lat.values.min()-1)
        ext_lat_max=int(ds.lat.values.max()+1)
        ext_lon_min=int(ds.lon.values.min()-1)
        ext_lon_max=int(ds.lon.values.max()+1)
        
        if resample:
            ds = ds.resample(time=resample).mean()
        else:
            ds = ds
            
        df=ds.to_dataframe()
        fig = plt.figure(figsize=(12,8))
        ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
        ax.add_feature(cfea.LAKES, zorder=3)
        ax.add_feature(cfea.OCEAN, zorder=1)
        ax.add_feature(cfea.COASTLINE, zorder=2)
        ax.add_feature(cfea.LAND, zorder=1)
        ax.add_feature(cfea.BORDERS, zorder=4)
        ax.set_extent([ext_lon_min,ext_lon_max,ext_lat_min,ext_lat_max])
        gl=ax.gridlines(draw_labels=True, zorder = 5)
        gl.right_labels = False
        gl.top_labels = False
        
        if (varname and time) is None:
            ax.scatter(x=df["lon"].values,y=df["lat"].values,transform=ccrs.PlateCarree(),color='k',s=10)
        else:
            ds.isel(time=time).plot.scatter(x='lon',y='lat',hue=varname,
                                ax=ax,cmap='inferno',vmin=int(ds[varname].min()),vmax=int(ds[varname].max()),
                                transform=ccrs.PlateCarree(),marker='s',s=50 ,zorder=6)
        #ax.text(x=df["lon"].values,y=df["lat"].values,s=df.index.get_level_values("location"),color="k")
        # ax.text(x=float(ds.isel(time=0).lon.values)-0.5,y=float(ds.isel(time=0).lat.values),s=float(ds['1002'].isel(time=0).values),color="red")
        # ax.text(x=float(ds.isel(time=0).lon.values)-0.5,y=float(ds.isel(time=0).lat.values)-0.2,s=float(ds['3002'].isel(time=0).values),color="blue")
        
    def plot(self,ds=None,varname=None, location=None,resample=None,date=None):
        
        mpl_res = None
        if resample:
            data=ds[varname].resample(time=resample).mean()
            
        else:
            data=ds[varname]
            
        if location is not None:  
            data_loc= data.sel(location=location)
            mpl_res = data_loc.plot.line(x="time")
        else:
            mpl_res = data.plot.line(x="time")
        
        # if date is not None:
        #     data_time = data.sel(time=date)
        #     plt.bar(x=data_time.location.astype("str"), height=data_time.values) 
        return mpl_res
    