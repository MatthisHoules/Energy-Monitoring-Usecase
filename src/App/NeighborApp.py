# External Imports
import requests
import urllib.parse
from requests import Response


class NeighborApp(object) :
    """_summary_

    Args:
        object (_type_): _description_
    """
    
    
    
    def __init__(self, host : str, port : int) -> None :
        """_summary_

        Args:
            host (str): _description_
            port (int): _description_
        """
        
        self.__host : str = host
        self.__port : int = port
    # def __init__(self, host : str, port : int) -> None
    
    
    
    def __rule_url_encode(self, rule : str) -> str:
        """_summary_

        Args:
            rule (str): _description_
        """
        
        return urllib.parse.quote(rule)
    # def __rule_url_encode(self, rule : str) -> str


    
    def request(self, rule) -> Response:
        """_summary_

        Args:
            rule (_type_): _description_
        """
        
        response : Response = requests.get(
            f"{self.__host}:{self.__port}/energy_monitoring?rule={self.__rule_url_encode(rule)}"
        )
        
        print(response)
        return response
    # def request(self, rule) -> Response
    
# class NeighborApp(object)  
 