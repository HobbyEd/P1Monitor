import plugwise_smile_API
import time
import json
from influxdb import InfluxDBClient

class PersistTimeSeriesForPlugwiseSmile(): 
    def __init__(self, influxdb_host, influxdb_database, influxdb_user, influxdb_password, plugwise_smile_host, plugwise_smile_password): 
        self.client = InfluxDBClient(host=influxdb_host, port=8086, database=influxdb_database, username=influxdb_user, password=influxdb_password)
        self.p1 = plugwise_smile_API.Smile(plugwise_smile_host, plugwise_smile_password)

    def persist_plugwise_smile_actueel(self): 
        self.p1.update_data()
        self.__persist_point(self.p1.get_actueel_verbruikt())
        self.__persist_point(self.p1.get_actueel_opgewekt())
                    
    def persist_plugwise_smile_cumulatief(self): 
        self.p1.update_data()
        self.__persist_point(self.p1.get_cumulatief_opgewekt_hoog_tarief())
        self.__persist_point(self.p1.get_cumulatief_opgewekt_laag_tarief())
        self.__persist_point(self.p1.get_cumulatief_verbuikt_hoog_tarief())
        self.__persist_point(self.p1.get_cumulatief_verbuikt_laag_tarief())

    def __persist_point(self, meetwaarde): 
        json_body = self.__get_point(meetwaarde)
        self.client.write_points(json_body)

    def __get_point(self, meetwaarde): 
        json_body = [
            {
                "measurement": meetwaarde['meeting_type'],
                "time": meetwaarde['time_stamp'],
                "fields": {
                    "waarde": meetwaarde['waarde'],
                    "eenheid": meetwaarde['eenheid']
                }
            }
        ]
        return json_body
