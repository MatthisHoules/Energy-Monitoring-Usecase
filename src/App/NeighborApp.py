# External Imports
import requests
import urllib.parse
from requests import Response
from interval import interval

# Internal Imports
from ..Request.Request import EnergyMonitoringRequests



class NeighborApp(object) :
    """NeighborApp

        Neighbor app of a EnergyMonitorRoute
    """

    def __init__(self, name : str, host : str, port : int, endpoint_rules : list[str]) -> None :
        """__init__

        Args:
            name (str): name of the neighbor app
            host (str): host of the neighbor app
            port (int): port of the neighbor app
            endpoint_rules (list[str]) : rules of the neighbor app
        """
        
        self.__name : str = name
        self.__host : str = host
        self.__port : int = port
        self.__endpoint_rules : list[str] = endpoint_rules
    # def __init__(self, host : str, port : int) -> None
    
    
    
    def get_name(self) -> str :
        """get_name

            Getter of the neighbor app name attribute
        """
        
        return self.__name
    # def get_name(self) -> str


    
    def __rule_url_encode(self, rule : str) -> str:
        """__rule_url_encode

            Getter of the rule but url encoded
        """
        
        return urllib.parse.quote(rule)
    # def __rule_url_encode(self, rule : str) -> str
    
    
    
    def request_energy_monitoring(self) -> dict[str, interval] :
        """request_energy_monitoring

            Request the energy consumtion of the neighbor app endpoints
        """
        
        rules_intervals : dict[str, interval] = dict()
        for rule in self.__endpoint_rules :
            print(f'computing {self.__host}:{self.__port}{rule}')
            response_interval_data = EnergyMonitoringRequests.get(
                f"http://{self.__host}:{self.__port}/energy_monitoring?rule={self.__rule_url_encode(rule)}"
            ).json()
            
            rules_intervals[rule] = interval(*response_interval_data)
            
        return rules_intervals
    # def request_energy_monitoring(self) -> dict[str, interval]
# class NeighborApp(object)  
 