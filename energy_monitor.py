import plugwise_smile_config as config
import persist_time_series_for_plugwise_smile as plugwise_persistor
import time
import sys
import logging  
from datetime import date
from datetime import datetime

# haal alle configuratie data op!
config_data = config.PlugwiseSmileConfig().load_config_data()
influxdb_host = config_data['influxdb']['host']
influxdb_user =  config_data['influxdb']['user']
influxdb_password = config_data['influxdb']['password']
influxdb_database = config_data['influxdb']['database']
plugwise_smile_host = config_data['plugwise_smile']['host']
plugwise_smile_password = config_data['plugwise_smile']['password']

def actueel_data(): 
    logging.basicConfig(filename='energy_monitor_actueel.log', level=logging.INFO)
    logging.info("%s >>Actuele data ophalen gestart.", datetime.now())
    persistor = plugwise_persistor.PersistTimeSeriesForPlugwiseSmile(influxdb_host,influxdb_database, influxdb_user,influxdb_password,plugwise_smile_host,plugwise_smile_password)
    
    while True: 
        persistor.persist_plugwise_smile_actueel()
        time.sleep(2)

def cumulatief_data(): 
    logging.basicConfig(filename='energy_monitor_cumulatief.log', level=logging.INFO)
    logging.info("%s >>Cumulatief data ophalen gestart.", datetime.now())
    persistor = plugwise_persistor.PersistTimeSeriesForPlugwiseSmile(influxdb_host,influxdb_database, influxdb_user,influxdb_password,plugwise_smile_host,plugwise_smile_password)
    while True: 
        persistor.persist_plugwise_smile_cumulatief()
        time.sleep(1800)

if __name__ == "__main__":
    #clear the log handlers list
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    parameter =sys.argv
    #check whether there is added a parameter to the script. If not plot the chart offline
    if (len(parameter) == 1):
        print (" Paramater required: values --actueel-- or --cumulatief-- ")
    elif (str.upper(parameter[1]) == "ACTUEEL"): 
        actueel_data()
    elif (str.upper(parameter[1])=="CUMULATIEF"):
        cumulatief_data()