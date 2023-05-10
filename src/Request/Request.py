# External Imports
from flask import g, Response
import requests

# TODO Documentation
class EnergyMonitoringRequests(object) :
    """_summary_

    Args:
        object (_type_): _description_
    """
    
    
    
    def get(url) -> Response :
        """_summary_

        Args:
            url (_type_): _description_

        Returns:
            Response: _description_
        """
        headers = {}
        if g is not None and g.endpoints is not None:
            headers = g.endpoints.get(url, {})
        
        response = requests.get(url, headers=headers)
        
        return response
    # def request(self, url) -> Response
# class EnergyMonitoringRequests(object)