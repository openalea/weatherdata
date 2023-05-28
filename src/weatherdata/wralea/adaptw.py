from openalea.core import *
from weatherdata import WeatherDataHub


def WeatherHub():
    """ Return WeatherDataHub that list all the resources available. """
    return WeatherDataHub(),

def resources(hub):
    return hub.list_resources,

class WeatherStations(Node):
    """ List all the weather stations From IPM platform."""
    stations = None
    def __init__(self):
        Node.__init__(self)

        hub = WeatherDataHub()
        rs = hub.list_resources
        if self.stations is None:
            self.stations = dict((v,k) for k, v in dict(rs.name).items())
        v, k = next(iter(self.stations.items()))
        print('init station : ', v,k)

        inputs=[ {'interface': None, 'name': 'WeatherHub', 'value': v}, 
                {'interface': IEnumStr(self.stations.keys()), 'name': 'stations', 'value': ''}, 
                ]
        [self.add_input(**kwds) for kwds in inputs]
        self.add_output(name='WeatherStations')

    def __call__(self, inputs):
        hub, station = inputs 
        print(hub, station)
        station_id = self.stations[station]
        fmi = hub.get_ressource(name=station_id)
        return fmi
