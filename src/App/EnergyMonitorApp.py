# External Imports
from flask import request
import eventlet
from eventlet import wsgi
from flask import Flask, g
import httpx
from flask import json
from functools import wraps
import urllib.parse
import requests

# Internal Imports
from .EnergyMonitorRoute import EnergyMonitorRoute

energy_monitoring_service = ()

class EnergyMonitorApp(object) :
    """_summary_

    """
    
    
    def __init__(self, host : str, port : int, name : str) -> None:
        """_summary_
        """
        
        self.__host : str = host
        self.__port : int = port
        self.__name : str = name
        self.app = Flask(self.__name)
        self.monitored_routes : dict[str, EnergyMonitorRoute] = dict()
        
        self.monitoring_endpoint()
    # def __init__(self, host : str, port : int, name : str) -> None
    
    
    
    def get_app(self) :
        """_summary_
        """
        
        return self.app
    # def get_app(self)



    def monitoring_endpoint(self) -> None :
        """_summary_
        """
        
        
        @self.app.route("/energy_monitoring")
        def retreive_monitored_endpoint() :
            """_summary_
            """
            
            rule = request.args.get('rule', default=None)
            print("RULE : ", rule)
            
            route : EnergyMonitorRoute = self.monitored_routes.get(rule, None)
            
            if route is None : 
                response = self.app.response_class(
                    response=json.dumps(f"No route {rule}"),
                    status=404,
                    mimetype='application/json'
                )
                return response
            
            
            route_energy_monitor : dict[str, float] = route.get_local_energy_data().get_avg_costs()
            
            
            response = self.app.response_class(
                response=json.dumps(route_energy_monitor),
                status=200,
                mimetype='application/json'
            )
            
            return response
        # def retreive_monitored_endpoint(rule : str)
    # def monitoring_endpoint(self)

    
    
    def route(self, rule, **options) :
        """_summary_

        Args:
            rule (str): _description_
        """
        
        def register_route_in_app(f):
            """_summary_

            Args:
                f (_type_): _description_

            Returns:
                _type_: _description_
            """
            
            # Reserved rule for peer to peer energy consumption
            assert rule != "/energy_monitoring"
            
            endpoint = options.pop("endpoint", None)
            
            monitored_params = options.pop("monitored_params", None)
            if monitored_params is None :           
                self.app.add_url_rule(rule, endpoint, f, **options)
                return f
            
            depends_on_endpoints : dict[str, list[str]] = options.pop("depends_on", None)
            
            
            self.__add_monitoring_route(EnergyMonitorRoute(
                rule,
                monitored_params,
                depends_on_endpoints
            ))
            
            @wraps(f)
            def route_function_wrapper(**endpoint_function_args):
                
                response = f(**endpoint_function_args)
                # response = self.monitored_routes[rule].monitor_function_call(f, **endpoint_function_args)

                return response

            self.app.add_url_rule(rule, endpoint, route_function_wrapper, **options)
            return route_function_wrapper

        return register_route_in_app
    # def route(self, rule, **options)
    
    
    
    def __add_monitoring_route(self, energy_monitored_route : EnergyMonitorRoute) :
        """_summary_

        Args:
            energy_monitored_route (EnergyMonitorRoute): _description_
        """
        
        self.monitored_routes[energy_monitored_route.url] = energy_monitored_route
    # def __add_monitoring_route(self, energy_monitored_route : EnergyMonitorRoute)



    def monitor_energy_routes(self) :
        """_summary_
        """
        
        c = httpx.Client(app=self.app, base_url="http://monitoring_routes")
        
        with c :
            for _, route in self.monitored_routes.items() :
                for args in route.get_params_combinations() :
                    for _ in range(route.get_treshold()) :
                        c.get(route.parse_url_with_args(**args))
    # def monitor_energy_routes(self)
    
    

    def run(self) -> None:
        """_summary_
        """
    
        self.monitor_energy_routes()

        eventlet.wsgi.server(
            eventlet.listen(
                (self.__host, self.__port)
            ), self.app
        )
    # def run(self) -> None    
# class App(object)
