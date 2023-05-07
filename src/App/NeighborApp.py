# External Imports
import requests
import urllib.parse
from requests import Response
from interval import interval


# Internal Imports
from ..Request.Request import EnergyMonitoringRequests


# TODO remove prints
class NeighborApp(object) :
    """_summary_

    Args:
        object (_type_): _description_
    """
    


    def __init__(self, name : str, host : str, port : int, endpoint_rules : list[str]) -> None :
        """_summary_

        Args:
            host (str): _description_
            port (int): _description_
            endpoint_rules (list[str]) : _description_
        """
        
        self.__name : str = name
        self.__host : str = host
        self.__port : int = port
        self.__endpoint_rules : list[str] = endpoint_rules
    # def __init__(self, host : str, port : int) -> None
    
    
    def get_name(self) -> str :
        return self.__name
    # def get_name(self) -> str

    
    def __rule_url_encode(self, rule : str) -> str:
        """_summary_

        Args:
            rule (str): _description_
        """
        
        return urllib.parse.quote(rule)
    # def __rule_url_encode(self, rule : str) -> str
    
    
    
    def request_energy_monitoring(self) -> interval :
        """_summary_

        Returns:
            dict[str, int]: _description_
        """
        
        rules_intervals : list[interval] = list()
        for rule in self.__endpoint_rules :
            print('computing rule', rule)
            response_interval_data = EnergyMonitoringRequests.get(
                f"http://{self.__host}:{self.__port}/energy_monitoring?rule={self.__rule_url_encode(rule)}"
            ).json()
            
            print("rule result : ", interval(*response_interval_data))
                        
            rules_intervals.append(
                interval(*response_interval_data)
            )

        print("all intervals : ", rules_intervals)
        return sum(rules_intervals)
    # def request_energy_monitoring(self) -> dict[str, interval]
# class NeighborApp(object)  
 