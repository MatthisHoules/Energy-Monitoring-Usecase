# External Imports
import itertools
from joulehunter import Profiler
from interval import interval
from flask import request
import logging
from pandas.io.json._normalize import nested_to_record    
from functools import reduce



# Internal Imports
from .LocalEnergyData import LocalEnergyData
from .NeighborApp import NeighborApp
from . import mckp, interval_helper
      



class EnergyMonitorRoute(object) :
    """EnergyMonitorRoute

        Energy monitored route and args tuned EnergyMonitorApp endpoints
    """
    
    
    def __init__(self, rule : str, monitored_params : dict, depends_on : list[NeighborApp] = [], threshold : int = 50) :
        """__init__

        ### params :
            rule (str): endpoint rule
            monitored_params (dict): monitored params with their ranges
        """
        
        self.rule : str = rule
        self.monitored_params : dict = monitored_params
        self.__threshold : int = threshold
        self.__local_energy_data : LocalEnergyData = LocalEnergyData(self.__threshold, len(monitored_params), monitored_params.keys())        
        self.__depends_on : list[NeighborApp] = depends_on
    # def __init__(self, endpoint : str, rule : str, monitored_params : dict)
    
    
    
    def parse_rule_with_args(self, **kwargs) :
        """parse_rule_with_args

        Returns:
            **kwargs: route args with their values
        """

        split_rule : list = self.rule.split('/')

        parsed_rule : list = []
        for s in split_rule :
            if len(s) == 0 : continue

            if s[0] == '<' :
                param_name : str = s[1:-1]
                type_sep_pos : int = param_name.find(':')

                if type_sep_pos != -1 :
                    param_name = param_name[type_sep_pos+1:]
                
                parsed_rule.append(str(kwargs.get(param_name)))    
            else :
                parsed_rule.append(s)
        
        return '/'.join(parsed_rule)
    # def parse_rule_with_args(self, **args)
    
    
    
    def get_params_combinations(self) :
        """get_params_combinations

        Returns:
            Endpoints args combinations (ranges ext)
        """
        
        keys, values = zip(*self.monitored_params.items())
        return [dict(zip(keys, v)) for v in itertools.product(*values)]
    # def get_params_combinations(self)
    
    
    
    def monitor_function_call(self, function, **args):
        """monitor_function_call

        Args:
            function (function): endpoint function to monitor

        Returns:
            response: response of the monitored endpoint function
        """
        
        profiler : Profiler = Profiler(interval=.0001)
        profiler.start()

        response = function(**args)

        profiler.stop()
        
        cost : float  = profiler._get_last_session_or_fail().root_frame()
        if cost:
            cost = cost.time()
        else:
            cost = 0.0
        
        self.__local_energy_data.add_arg_cost(str(args), round(cost*1000, 0))
        
        return response
    # def monitor_function_call(self, function, **args)  
    
    
    
    def get_route_cost(self) -> interval :
        local_cost : interval = self.get_local_energy_data().get_cost_interval()
        # neighbor
        if self.is_route_dependent() :
            neigbors_costs : dict[str, interval] = nested_to_record(self.get_neighbouring_endpoints_consumption(), sep='_')
            total_cost : interval = local_cost + sum(neigbors_costs.values())
            return total_cost
        
        return local_cost
    # def get_route_cost(self) -> interval
    
    
    
    def process_arguments(self, objective : float, available : int | None) -> tuple[dict[str, int], list[float]]:
        """process_arguments

        Args:
            objective (float): user consumtion energy consumtion
            available (int) : available consumtion
        """

        if objective < 0:
            logging.warn(f"{self.rule} has not objective defined.")
            
        print(f"{self.rule} has an objective of {objective}, with an availability of {available}")

        endpoints = nested_to_record(self.get_neighbouring_endpoints_consumption(), sep='_')
        endpoints[self.rule] = self.__local_energy_data.get_cost_interval()

        distributed = self.distribute_objective(objective / 100, endpoints, available)

        return (distributed, self.__local_energy_data.predict_args_from_cost(distributed[self.rule]))
    # def process_arguments(self, objective : float, arguments: list[float])



    def distribute_objective(self, objective : float, endpoints_costs : dict[str, interval], target : int | None) -> dict[str, int]:
        """distribute_objective

            Args:
                objective : user objectibe
                endpoints_costs : dict[str, interval] : cost of local & neighbors endpoints
                target : int : target cost defined by parent endpoint
        """

        (min_cost, max_cost) = interval_helper.intervals_bounds(endpoints_costs.values())

        if target is None:
            target = round(max_cost * objective)
            
        if target <= min_cost:
            return {k: interval_helper.interval_min(v) for k, v in endpoints_costs.items()}

        surplus = target - min_cost
        given_costs = {}
        for endpoint_name, costs in endpoints_costs.items():
            given = interval_helper.interval_min(costs) + surplus * interval_helper.interval_max(costs) / max_cost
            given_costs[endpoint_name] = int(given)
        return given_costs
    # def distribute_objective(self, objective : float, endpoints_costs : dict[str, interval], target : int | None) -> dict[str, int]
    


    def distribute_objective_mckp(self, objective : int, endpoints_costs : dict[str, interval]) -> dict[str, int]:
        """
            mckp function (TBD)
        """
        minimal_costs = mckp.closest_path(endpoints_costs, objective)
        
        remaining = objective - sum(minimal_costs.values())

        shares = len(minimal_costs)
        for endpoint_name, cost in minimal_costs.items():
            share_amount = remaining / shares
        
        return minimal_costs
    # def distribute_objective_mckp(self, objective : int, endpoints_costs : dict[str, interval]) -> dict[str, int]



    def get_neighbouring_endpoints_consumption(self) -> dict[str, dict[str, interval]] :
        """Returns a map containing the consumption of all neighbouring endpoints, keyed by their rule 

        Returns:
            dict[str, interval]: a map { rule -> consumption interval }
        """
        
        result_dict : dict[str, dict[str, interval]] = dict()
        for neighbor in self.__depends_on :
            result_dict[neighbor.get_name()] = neighbor.request_energy_monitoring()
            
        return result_dict
    # def get_neighbouring_endpoints_consumption(self) -> dict[str, dict[str, interval]] 
    
    
    
    def get_threshold(self) -> float :
        """get_treshold

        Returns:
            float: treshold value
        """
        return self.__threshold
    # def get_treshold(self) -> float
    
    
    
    def is_route_dependent(self) -> bool :
        """is_route_dependent

            Returns True if the endpoint is dependent. Returns False instead
        """
        return len(self.__depends_on) > 0
    # def is_route_dependent(self) -> bool
    
    
    
    def get_local_energy_data(self) -> LocalEnergyData :
        """get_local_energy_data

            Getter of __local_energy_data attribute
        """
        return self.__local_energy_data
    # def get_local_energy_data(self) -> LocalEnergyData
# class EnergyMonitorRoute(object)