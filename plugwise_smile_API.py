import requests 
from requests.auth import HTTPBasicAuth
import xmltodict  
from enum import Enum

class meeting_type(Enum): 
    ACTUEEL_VERBRUIKT = 'actueel_verbuikt'
    ACTUEEL_OPGEWEKT = 'actueel_terug_geleverd'
    CUMULATIEF_OPGEWEKT_LAAG_TARIEF = 'cumulatief_terug_geleverd_laag_tarief'
    CUMULATIEF_OPGEWEKT_HOOG_TARIEF = 'cumulatief_terug_geleverd_tarief'
    CUMULATIEF_VERBRUIKT_LAAG_TARIEF = 'cumulatief_verbuikt_laag_tarief'
    CUMULATIEF_VERBRUIKT_HOOG_TARIEF = 'cumulatief_verbuikt_hoog_tarief'

class Smile: 
    def __init__(
        self,
        host,
        password,
        username="smile",
        port=80,
        ):
        self._endpoint = f"http://{host}:{str(port)}/core/domain_objects"
        self._password = password 
        self._username = username 
        self._actueel_opgewekt = {}
        self._actueel_verbruikt = {}
        self._cumulatief_opgewekt_laag_tarief = {}
        self._cumulatief_opgewekt_hoog_tarief = {}
        self._cumulatief_verbuikt_laag_tarief = {}
        self._cumulatief_verbuikt_hoog_tarief = {}

    def get_actueel_opgewekt(self): 
        return self._actueel_opgewekt

    def get_actueel_verbruikt(self):
        return self._actueel_verbruikt

    def get_cumulatief_verbuikt_hoog_tarief(self): 
        return self._cumulatief_verbuikt_hoog_tarief
    
    def get_cumulatief_verbuikt_laag_tarief(self): 
        return self._cumulatief_verbuikt_laag_tarief

    def get_cumulatief_opgewekt_hoog_tarief(self): 
        return self._cumulatief_opgewekt_hoog_tarief

    def get_cumulatief_opgewekt_laag_tarief(self): 
        return self._cumulatief_opgewekt_laag_tarief

    def update_data(self):
        resp = requests.get(self._endpoint, auth=HTTPBasicAuth(self._username, self._password) )
        resp_dict = xmltodict.parse(resp.content)

        # Zet alle actuele waarden.        
        for verbruik in resp_dict['domain_objects']['module']['services']['electricity_point_meter']['measurement']:
            if verbruik['@directionality'] == 'consumed': 
                self._actueel_verbruikt = {'meeting_type': meeting_type.ACTUEEL_VERBRUIKT.value, 'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}
            elif verbruik['@directionality'] == 'produced':
                self._actueel_opgewekt = {'meeting_type': meeting_type.ACTUEEL_OPGEWEKT.value, 'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}
        
        #Zet alle cumulatieve waarden. 
        for verbruik in resp_dict['domain_objects']['module']['services']['electricity_cumulative_meter']['measurement']:
            if verbruik['@directionality'] == 'consumed': 
                if verbruik['@tariff_indicator'] == 'nl_peak':
                    self._cumulatief_verbuikt_hoog_tarief = {'meeting_type': meeting_type.CUMULATIEF_VERBRUIKT_HOOG_TARIEF.value, 'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}
                elif verbruik['@tariff_indicator'] == 'nl_offpeak':
                    self._cumulatief_verbuikt_laag_tarief = {'meeting_type': meeting_type.CUMULATIEF_VERBRUIKT_LAAG_TARIEF.value, 'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}
            elif verbruik['@directionality'] == 'produced':
                if verbruik['@tariff_indicator'] == 'nl_peak':
                    self._cumulatief_opgewekt_hoog_tarief = {'meeting_type': meeting_type.CUMULATIEF_OPGEWEKT_HOOG_TARIEF.value, 'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}
                elif verbruik['@tariff_indicator'] == 'nl_offpeak':
                    self._cumulatief_opgewekt_laag_tarief = {'meeting_type': meeting_type.CUMULATIEF_OPGEWEKT_LAAG_TARIEF.value, 'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}


