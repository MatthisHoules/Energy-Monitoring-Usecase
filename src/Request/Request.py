# External Imports
from flask import request, Response
import requests


class EnergyMonitoringRequests(object) :
    
    def get(url) -> Response :        
        headers = request.headers
        response = requests.get(url, headers=headers)
        
        return response
    # def request(self, url) -> Response