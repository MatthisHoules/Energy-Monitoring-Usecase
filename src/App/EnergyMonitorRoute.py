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
import pprint
# TODO Documentation
# TODO remove prints
class EnergyMonitorRoute(object) :
    """_summary_

    Args:
        object (_type_): _description_
    """
    
    
    def __init__(self, rule : str, monitored_params : dict, depends_on : list[NeighborApp] = [], threshold : int = 20) :
        """_summary_

        Args:
            endpoint (str): _description_
            rule (str): _description_
            monitored_params (dict): _description_
        """
        
        self.rule : str = rule
        self.monitored_params : dict = monitored_params
        self.__threshold : int = threshold
        self.__local_energy_data : LocalEnergyData = LocalEnergyData(self.__threshold, len(monitored_params), monitored_params.keys())        
        self.__depends_on : list[NeighborApp] = depends_on
    # def __init__(self, endpoint : str, rule : str, monitored_params : dict)
    
    
    
    def parse_rule_with_args(self, **args) :
        """_summary_

        Returns:
            _type_: _description_
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
                
                parsed_rule.append(str(args.get(param_name)))    
            else :
                parsed_rule.append(s)
        
        return '/'.join(parsed_rule)
    # def parse_rule_with_args(self, **args)
    
    
    
    def get_params_combinations(self) :
        """_summary_

        Returns:
            _type_: _description_
        """
        
        keys, values = zip(*self.monitored_params.items())
        return [dict(zip(keys, v)) for v in itertools.product(*values)]
    # def get_params_combinations(self)
    
    
    
    def monitor_function_call(self, function, **args):
        """_summary_

        Args:
            function (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        profiler : Profiler = Profiler(interval=.0001)
        profiler.start()

        # TODO : Process arguments
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
    
    
    
    def process_arguments(self, objective : float | None, available : int | None) -> tuple[dict[str, int], list[float]]:
        """process_arguments

        Args:
            objective (float): _description_
            arguments (list[float]): _description_
        """
        assert objective is not None or available is not None
        endpoints = nested_to_record(self.get_neighbouring_endpoints_consumption(), sep='_')
        endpoints[self.rule] = self.__local_energy_data.get_cost_interval()

        distributed = self.distribute_objective(objective, endpoints, available)

        return (distributed, self.__local_energy_data.predict_args_from_cost(distributed[self.rule]))
    # def process_arguments(self, objective : float, arguments: list[float])


    def distribute_objective(self, objective : float | None, endpoints_costs : dict[str, interval], target : int | None) -> dict[str, int]:
        (min_cost, max_cost) = interval_helper.intervals_bounds(endpoints_costs.values())

        if target is None:
            target = round(max_cost * objective / 100)
            
        if target <= min_cost:
            return {k: interval_helper.interval_min(v) for k, v in endpoints_costs.items()}

        surplus = target - min_cost
        given_costs = {}
        for endpoint_name, costs in endpoints_costs.items():
            given = interval_helper.interval_min(costs) + surplus * interval_helper.interval_max(costs) / max_cost
            given_costs[endpoint_name] = int(given)
            
        print(f"endpoints costs ", pprint.pformat(endpoints_costs))
        print(f"distributed available energy to neighbouring endpoints : {pprint.pformat(given_costs)}, \n sum = {sum(given_costs.values())}, \n target = {target}")
        return given_costs
    
    def distribute_objective_mckp(self, objective : int, endpoints_costs : dict[str, interval]) -> dict[str, int]:
        
        minimal_costs = mckp.closest_path(endpoints_costs, objective)
        
        remaining = objective - sum(minimal_costs.values())

        shares = len(minimal_costs)
        for endpoint_name, cost in minimal_costs.items():
            share_amount = remaining / shares
        
        return minimal_costs
    # def distribute_objective(objective : float, endpoints_costs : dict[str, interval])



    def get_neighbouring_endpoints_consumption(self) -> dict[str, dict[str, interval]] :
        """Returns a map containing the consumption of all neighbouring endpoints, keyed by their rule 

        Returns:
            dict[str, interval]: a map { rule -> consumption interval }
        """
        
        result_dict : dict[str, dict[str, interval]] = dict()
        for neighbor in self.__depends_on :
            result_dict[neighbor.get_name()] = neighbor.request_energy_monitoring()
            
        return result_dict
    # def get_neighbouring_enpoints_consumption() -> dict[str, interval]
    
    
    
    def get_threshold(self) -> float :
        """get_treshold

        Returns:
            float: _description_
        """
        return self.__threshold
    # def get_treshold(self) -> float
    
    
    
    def is_route_dependent(self) -> bool :
        return len(self.__depends_on) > 0
    # def is_route_dependent(self) -> bool
    
    
    
    def get_local_energy_data(self) -> LocalEnergyData :
        return self.__local_energy_data
    # def get_local_energy_data(self) -> LocalEnergyData
# class EnergyMonitorRoute(object)