# External Imports
from flask import g, Response
import requests

# TODO Documentation
class EnergyMonitoringRequests(object) :
    """EnergyMonitoringRequests
    """
    
    def get(url) -> Response :
        """get

        Args:
            url (str): url to request

        Returns:
            Response: the response of the get url HTTP request
        """
        headers = {}
        if g is not None and hasattr(g, 'endpoints'):
            headers = g.endpoints.get(url, {})
        
        response = requests.get(url, headers=headers)
        
        return response
    # def request(self, url) -> Response
# class EnergyMonitoringRequests(object)