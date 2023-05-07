# External Imports
from flask import Flask, g, json, jsonify, make_response, request

import eventlet
from eventlet import wsgi

import httpx

from functools import wraps

from interval import interval



# Internal Imports
from .EnergyMonitorRoute import EnergyMonitorRoute
from .NeighborApp import NeighborApp



class EnergyMonitorApp(object) :
    """_summary_

    """
    
    
    def __init__(self, host : str, port : int, name : str, depends_microservices_config_env_filepath : str) -> None:
        """_summary_
        """
        
        self.__host : str = host
        self.__port : int = port
        self.__name : str = name
        self.app = Flask(self.__name)
        self.monitored_routes : dict[str, EnergyMonitorRoute] = dict()
    
        with open(depends_microservices_config_env_filepath) as f:
            self.__neighbors_app_config : dict = json.load(f).get("neighbor_apps")

        self.__add_monitoring_endpoint()
    # def __init__(self, host : str, port : int, name : str) -> None
    
    
    
    def get_app(self) :
        """_summary_
        """
        
        return self.app
    # def get_app(self)



    def __add_monitoring_endpoint(self) -> None :
        """_summary_
        """
        
        @self.app.route("/energy_monitoring")
        def retreive_monitored_endpoint() :
            """_summary_
            """
            
            rule = request.args.get('rule', default=None)
            route : EnergyMonitorRoute = self.monitored_routes.get(rule, None)
            
            if route is None : 
                response = self.app.response_class(
                    response=json.dumps(f"No route {rule}"),
                    status=404,
                    mimetype='application/json'
                )
                return response
            
            # here total_cost is only local cost
            total_cost : interval = route.get_route_cost()
            
            response = make_response(jsonify(list(total_cost)), 200)
            return response
        # def retreive_monitored_endpoint(rule : str)
    # def __add_monitoring_endpoint(self) -> None

    
    
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
            
            # This rule is reserved for peer to peer energy consumption communication
            assert rule != "/energy_monitoring"
            
            endpoint = options.pop("endpoint", None)
            
            monitored_params = options.pop("monitored_params", None)
            if monitored_params is None :           
                self.app.add_url_rule(rule, endpoint, f, **options)
                return f
            
            depends_on_endpoints : dict[str, list[str]] = options.pop("depends_on", {})
                 
            self.__add_monitoring_route(EnergyMonitorRoute(
                rule,
                monitored_params,
                self.__retreive_route_neighbors_endpoints(depends_on_endpoints)
            ))
            
            @wraps(f)
            def route_function_wrapper(**endpoint_function_args):
                # get monitoring header
                user_cost_target : int = request.headers.get('x-user-energy-objective', None)
                
                if user_cost_target is None :
                    response = f(**endpoint_function_args)
                    return response
                
                # TODO MAIN
                self.monitored_routes[rule].get_route_cost()
                 
                response = self.monitored_routes[rule].monitor_function_call(f, **endpoint_function_args)

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
        
        self.monitored_routes[energy_monitored_route.rule] = energy_monitored_route
    # def __add_monitoring_route(self, energy_monitored_route : EnergyMonitorRoute)



    def monitor_energy_routes(self) :
        """_summary_
        """
        # TODO IGNORE DEPENDS_ON CALLS
        c = httpx.Client(app=self.app, base_url="http://monitoring_routes")
        
        with c :
            for _, route in self.monitored_routes.items() :
                for args in route.get_params_combinations() :
                    for _ in range(route.get_treshold()) :
                        c.get(route.parse_rule_with_args(**args))
    # def monitor_energy_routes(self)
    
    
    
    def __retreive_route_neighbors_endpoints(self, depends_on_endpoints : dict[str, list[str]]) -> list[NeighborApp] :
        """_summary_

        Args:
            depends_on_endpoints (dict[str, list[str]]): _description_

        Returns:
            list[NeighborApp]: _description_
        """
        if depends_on_endpoints == {} : return list()
        
        route_neighbors_apps : list[NeighborApp] = list()
        for neighbor_app_name, neighbor_app_routes in depends_on_endpoints.items() :
            neighbor_app_config = self.__neighbors_app_config.get(neighbor_app_name)
            print("neighbor route creation : ", neighbor_app_routes)
            route_neighbors_apps.append(
                NeighborApp(
                    neighbor_app_name,
                    neighbor_app_config.get("host"),
                    neighbor_app_config.get("port"),
                    neighbor_app_routes
                )
            )

        return route_neighbors_apps
    # def __retreive_route_neighbors_endpoints(self, depends_on_endpoints : dict[str, list[str]]) -> list[NeighborApp]
    
    

    def run(self) -> None:
        """_summary_
        """

        self.monitor_energy_routes()

        wsgi.server(
            eventlet.listen(
                (self.__host, self.__port)
            ), self.app
        )
    # def run(self) -> None
# class App(object)
