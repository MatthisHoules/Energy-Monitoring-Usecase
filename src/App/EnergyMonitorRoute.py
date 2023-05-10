# External Imports
import itertools
from bloompy import CountingBloomFilter
from joulehunter import Profiler
from interval import interval
from flask import request
import logging

# Internal Imports
from .LocalEnergyData import LocalEnergyData
from .NeighborApp import NeighborApp
from . import mckp
      

# TODO Documentation
# TODO remove prints
class EnergyMonitorRoute(object) :
    """_summary_

    Args:
        object (_type_): _description_
    """
    
    
    def __init__(self, rule : str, monitored_params : dict, depends_on : list[NeighborApp] = [], threshold : int = 10) :
        """_summary_

        Args:
            endpoint (str): _description_
            rule (str): _description_
            monitored_params (dict): _description_
        """
        
        self.rule : str = rule
        self.monitored_params : dict = monitored_params
        self.__threshold : int = threshold
        self.__local_energy_data : LocalEnergyData = LocalEnergyData(self.__threshold, len(monitored_params))        
        self.__depends_on : list[NeighborApp] = depends_on
        self.__filter : CountingBloomFilter = CountingBloomFilter

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
        print("\n"*5, "RULE : ", self.rule)
        local_cost : interval = self.get_local_energy_data().get_cost_interval()
        print("local cost : ", local_cost)
        # neighbor
        if self.is_route_dependent() :
            neigbors_costs : dict[str, interval] = self.get_neighbouring_endpoints_consumption()
            print("neighbors costs : ", neigbors_costs)
            total_cost : interval = local_cost + sum(neigbors_costs.values()) # TODO : Average ??
            print("total cost : ", total_cost)
            return total_cost
        
        return local_cost
    # def get_route_cost(self) -> interval
    
    
    
    def process_arguments(self, objective : float) -> tuple[dict[str, int], list[float]]:
        """process_arguments

        Args:
            objective (float): _description_
            arguments (list[float]): _description_
        """

        if objective < 0:
            logging.warn(f"{self.rule} has not objective defined.")
            pass
        logging.info(f"{self.rule} has an objective of {objective}")

        endpoints = self.get_neighbouring_endpoints_consumption() # TODO : coder
        endpoints[self.rule] = self.__local_energy_data.get_cost_interval()
        costs = self.distribute_objective(objective, endpoints)
        print(costs)
        return (endpoints, self.__local_energy_data.predict_args_from_cost(costs[self.rule]))
    # def process_arguments(self, objective : float, arguments: list[float])



    def distribute_objective(self, objective : int, endpoints_costs : dict[str, interval]) -> dict[str, int]:
        print(f"obj : {objective}, costs : {endpoints_costs}")
        minimal_costs = mckp.closest_path(endpoints_costs, objective)
        distributed = sum(minimal_costs.values())
        print(f"distributed {distributed} out of {objective}")
        return minimal_costs
    # def distribute_objective(objective : float, endpoints_costs : dict[str, interval])



    def get_neighbouring_endpoints_consumption(self) -> dict[str, interval] :
        """Returns a map containing the consumption of all neighbouring endpoints, keyed by their rule 

        Returns:
            dict[str, interval]: a map { rule -> consumption interval }
        """
        return {
            neighbor.get_name() : neighbor.request_energy_monitoring() for neighbor in self.__depends_on
        }
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