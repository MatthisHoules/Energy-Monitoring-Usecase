# External Imports
from flask import request
from joulehunter import Profiler
import eventlet
from eventlet import wsgi
from flask import Flask, g
import httpx
from interval import interval
from flask import json
from functools import wraps

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
    # def __init__(self, host : str, port : int, name : str) -> None
    
    
    
    def get_app(self) :
        """_summary_
        """
        
        return self.app
    # def get_app(self)


    
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
            
            endpoint = options.pop("endpoint", None)
            
            monitored_params = options.pop("monitored_params", None)
            if monitored_params is None :           
                self.app.add_url_rule(rule, endpoint, f, **options)
                return f
            
            depends_on_endpoints : list[str] = list(options.pop("depends_on", []))
            
            
            self.__add_monitoring_route(EnergyMonitorRoute(
                rule,
                monitored_params,
                depends_on_endpoints
            ))
            
            @wraps(f)
            def route_function_wrapper(**endpoint_function_args):
                
                print("RULE : ", rule)
                response = self.monitored_routes[rule].monitor_function_call(f, **endpoint_function_args)
        

                return response
                # g.profiler = Profiler()
                # g.profiler.start()
                # # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
                # # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
                # # monitor & tuning
                # #   Si <= monitoring
                # #       Prendre 100%, produit en croix, calcul knn puis monitoring, enregistrer résultat param
                # #       MCKP Paulopolpogba


                # response =  f(**t)
                # print("response : ", response)
            
                # g.profiler.stop()
                    
                # frame = g.profiler._get_last_session_or_fail().root_frame()
                # if frame:
                #     frame = frame.time()
                # else:
                #     frame = 0.0
                    
                # print(frame)
                # return response
                
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
    
    

    def run(self) :
        """_summary_
        """
    
        self.monitor_energy_routes()

        eventlet.wsgi.server(
            eventlet.listen(
                (self.__host, self.__port)
            ), self.app
        )
    # def run(self)    
# class App(object)
