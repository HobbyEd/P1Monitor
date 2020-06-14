import plugwise_smile_config as config
import persist_time_series_for_plugwise_smile as plugwise_persistor
import time
import sys

# haal alle configuratie data op!
config_data = config.PlugwiseSmileConfig().load_config_data()
influxdb_host = config_data['influxdb']['host']
influxdb_user =  config_data['influxdb']['user']
influxdb_password = config_data['influxdb']['password']
influxdb_database = config_data['influxdb']['database']
plugwise_smile_host = config_data['plugwise_smile']['host']
plugwise_smile_password = config_data['plugwise_smile']['password']

persistor = plugwise_persistor.PersistTimeSeriesForPlugwiseSmile(influxdb_host,influxdb_database, influxdb_user,influxdb_password,plugwise_smile_host,plugwise_smile_password)

def actueel_data(): 
    while True: 
        persistor.persist_plugwise_smile_actueel()
        time.sleep(2)

def cumulatief_data(): 
    while True: 
        persistor.persist_plugwise_smile_cumulatief()
        time.sleep(1800)

if __name__ == "actueel":
    actueel_data()
elif __name__ == "cumulatief": 
    cumulatief_data()