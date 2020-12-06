import json
import io
import logging
from datetime import datetime

class PlugwiseSmileConfig(): 
    # This function read the logfiles in the folder /Logs and return 
    # a dictionary with the JSON data
    
    @classmethod
    def load_config_data(self):
        _plugwise_smile_config = {}
        try:
            with io.open("/home/evdillen/P1Monitor/plugwise_smile.conf", 'r', encoding='utf-8') as f:
                _plugwise_smile_config = json.load(f)
            return _plugwise_smile_config
        except Exception:
            logging.error("%s >>The config file could (plugwise_smile.config) not be read. Is it in the main folder?", datetime.now())
        finally:
            logging.info("%s >>Configuration information hase been read succesfull.", datetime.now())
            f.close()
