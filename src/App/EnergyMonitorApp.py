# External Imports
import flask
from joulehunter import Profiler
import eventlet
from eventlet import wsgi
from flask import Flask, g, make_response
import httpx
import itertools
from flask import json
from functools import wraps

# Internal Imports
from .EnergyMonitorRoute import EnergyMonitorRoute



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

        self.monitored_routes : dict = dict()
    # def __init__(self) -> None
    
    
    
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
        
        def decorator(f):
            """_summary_

            Args:
                f (_type_): _description_

            Returns:
                _type_: _description_
            """
            
            endpoint = options.pop("endpoint", None)
            
            if options.get("monitored_params", None) is None :           
                self.app.add_url_rule(rule, endpoint, f, **options)
                return f
            
            self.__add_monitoring_route(EnergyMonitorRoute(
                rule,
                options.pop("monitored_params")
            ))
            
            @wraps(f)
            def test(**t) :
                print(t)
                g.profiler = Profiler()
                g.profiler.start()
                
                # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
                # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
                # monitor & tuning
                #   Si <= monitoring
                #       Prendre 100%, produit en croix, calcul knn puis monitoring, enregistrer résultat param
                #       MCKP Paulopolpogba

                response =  f(**t)
                print("response : ", response)
            
                g.profiler.stop()
                    
                frame = g.profiler._get_last_session_or_fail().root_frame()
                if frame:
                    frame = frame.time()
                else:
                    frame = 0.0
                    
                print(frame)
                return response
                
            self.app.add_url_rule(rule, endpoint, test, **options)
            return test

        return decorator
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
                for a in route.get_params_combinations() :
                    for _ in range(10) :
                        c.get(route.parse_url_with_params(**a))
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
