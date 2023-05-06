# External Imports
import requests
import urllib.parse
from requests import Response
from interval import interval



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
    
    
    
    def __rule_url_encode(self, rule : str) -> str:
        """_summary_

        Args:
            rule (str): _description_
        """
        
        return urllib.parse.quote(rule)
    # def __rule_url_encode(self, rule : str) -> str


    
    def __request_energy_interval_rule(self, rule) -> Response:
        """_summary_

        Args:
            rule (_type_): _description_
        """
        
        response : Response = requests.get(
            f"http://{self.__host}:{self.__port}/energy_monitoring?rule={self.__rule_url_encode(rule)}"
        )
        
        return response
    # def __request_energy_monitoring_rule(self, rule) -> Response
    
    
    
    def request_energy_monitoring(self) -> dict[str, interval] :
        """_summary_

        Returns:
            dict[str, int]: _description_
        """
        
        
        r_dict : dict = dict()
        for rule in self.__endpoint_rules :
            r = self.__request_energy_interval_rule(rule).json()
            assert len(r) == 2
            
            r_dict[rule] = interval([r[0], r[1]])
        
        return r_dict
    # def request_energy_monitoring(self) -> dict[str, interval]
# class NeighborApp(object)  
 