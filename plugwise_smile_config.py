import json
import io


class PlugwiseSmileConfig(): 
    # This function read the logfiles in the folder /Logs and return 
    # a dictionary with the JSON data
    
    @classmethod
    def load_config_data(self):
        _plugwise_smile_config = {}
        try:
            with io.open("plugwise_smile.conf", 'r', encoding='utf-8') as f:
                _plugwise_smile_config = json.load(f)
            return _plugwise_smile_config
        except Exception:
            print("The config file could (plugwise_smile.config) not be read. Is it in the main folder?")
        finally:
            f.close()
