# External Imports
from flask import request, Response
import requests

# TODO Documentation
class EnergyMonitoringRequests(object) :
    """_summary_

    Args:
        object (_type_): _description_
    """
    
    
    
    def get(url, headers : dict[str, str]= {}) -> Response :
        """_summary_

        Args:
            url (_type_): _description_

        Returns:
            Response: _description_
        """
        headers = headers.copy()
        objective = request.g.objectives.get(url)
        if objective is not None:
            headers['x-user-energy-objective'] = objective
        response = requests.get(url, headers=headers)
        
        return response
    # def request(self, url) -> Response
# class EnergyMonitoringRequests(object)