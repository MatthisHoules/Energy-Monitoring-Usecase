# External Imports
from flask import Flask, g, json, jsonify, make_response, request, Response
import requests
import eventlet
from eventlet import wsgi
import httpx
from functools import wraps
from interval import interval

# Internal Imports
from .EnergyMonitorRoute import EnergyMonitorRoute
from .NeighborApp import NeighborApp



class EnergyMonitorApp(object) :
    """  ## EnergyMonitorApp
        
        Wrapper of Flask App object :
            Add a route "/energy_monitoring" that can communicate cost of their energy monitored endpoints
            Intercept calls in order to adjust endpoints parameters to respect user energy consumption objective
    """
    
    def __init__(self, host : str, port : int, name : str, depends_microservices_config_env_filepath : str) -> None:
        """ ## __init__

            ### params :
                host : str : host on which the flask api will run
                port : int : port on which the flask api will run
                name : str : name of the flask api
                depends_microservices_config_env_filepath : str : path of the configuration file of depending microservices
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
        """get_app

            ### return :
                Flask app object
        """
        
        return self.app
    # def get_app(self)



    def __add_monitoring_endpoint(self) -> None :
        """__add_monitoring_endpoint
    
            This function allows to add the energy_monitoring route that returns the energy consumption of a given endpoint
        """
        
        @self.app.route("/energy_monitoring")
        def retreive_monitored_endpoint() :
            """retreive_monitored_endpoint
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
        """route

        Args:
            rule (str): rule pattern to add in the app
        """
        
        def register_route_in_app(f):
            """register_route_in_app

            Args:
                f (function): endpoint function

            Returns:
                function: function wrap with energy monitoring & args tuning components
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
                # get user energy objective
                user_cost_target : int | None = self.__get_user_energy_objective()
                args = endpoint_function_args
                
                if user_cost_target is not None :
                    available = request.headers.get('x-user-energy-available', None)
                    if available is not None:
                        available = int(available)

                    (endpoints_costs, args) = self.monitored_routes[rule].process_arguments(user_cost_target, available)
                    
                    g.endpoints = endpoints_costs.copy()
                 
                response = self.monitored_routes[rule].monitor_function_call(f, **args)

                return response

            self.app.add_url_rule(rule, endpoint, route_function_wrapper, **options)
            return route_function_wrapper

        return register_route_in_app
    # def route(self, rule, **options)
    
    
    
    def __add_monitoring_route(self, energy_monitored_route : EnergyMonitorRoute) :
        """__add_monitoring_route

        Args:
            energy_monitored_route (EnergyMonitorRoute): monitored route
        """
        
        self.monitored_routes[energy_monitored_route.rule] = energy_monitored_route
    # def __add_monitoring_route(self, energy_monitored_route : EnergyMonitorRoute)



    def monitor_energy_routes(self) :
        """monitor_energy_routes

            Get energy consumption informations of each interval in order to avoid cold starts 
        """

        c = httpx.Client(app=self.app, base_url="http://monitoring_routes")
        
        with c :
            for _, route in self.monitored_routes.items() :
                for args in route.get_params_combinations() :
                    for _ in range(route.get_threshold()) :
                        c.get(route.parse_rule_with_args(**args))
    # def monitor_energy_routes(self)
    
    
    
    def __retreive_route_neighbors_endpoints(self, depends_on_endpoints : dict[str, list[str]]) -> list[NeighborApp] :
        """__retreive_route_neighbors_endpoints

        Args:
            depends_on_endpoints (dict[str, list[str]]): endpoints that depents of a route

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
        """run

            Run the Flask app wiht a wsgi server
        """

        self.monitor_energy_routes()

        wsgi.server(
            eventlet.listen(
                (self.__host, self.__port)
            ), self.app
        )
    # def run(self) -> None
    
    
    
    def __get_user_energy_objective(self) -> int | None: 
        user_cost_target : int | None = request.headers.get('x-user-energy-objective', None)
        
        if user_cost_target is None : 
            return None
        
        user_cost_target = int(user_cost_target)
        if user_cost_target < 10 :
            user_cost_target = 10
        elif user_cost_target > 100 : 
            user_cost_target = 100
        elif type(user_cost_target) is float :
            user_cost_target = int(user_cost_target)
        
        return user_cost_target
    # def __get_user_energy_objective(self) -> int        
# class App(object)