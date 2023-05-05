# External Imports
import itertools
from bloompy import CountingBloomFilter
from joulehunter import Profiler
from interval import interval
import logging

# Internal Imports
from .local_energy_data import LocalEnergyData
      


class EnergyMonitorRoute(object) :
    """_summary_

    Args:
        object (_type_): _description_
    """
    
    filter : CountingBloomFilter = CountingBloomFilter
    
    
    
    def __init__(self, url : str, monitored_params : dict, depends_on : dict[str, list[str]], threshold : int = 10) :
        """_summary_

        Args:
            endpoint (str): _description_
            url (str): _description_
            monitored_params (dict): _description_
        """
        
        self.url : str = url
        self.monitored_params : dict = monitored_params
        self.__treshold : int = threshold
        self.__local_energy_data : LocalEnergyData = LocalEnergyData()
        """ counting bloom filter to assess whether to evaluate using the MCKP or not """
        
        self.__depends_on : dict[str, list[str]] = depends_on
    # def __init__(self, endpoint : str, url : str, monitored_params : dict)
    
    
    
    def parse_url_with_args(self, **args) :
        """_summary_

        Returns:
            _type_: _description_
        """
                
        split_url : list = self.url.split('/')

        parsed_url : list = []
        for s in split_url :
            if len(s) == 0 : continue

            if s[0] == '<' :
                param_name : str = s[1:-1]
                type_sep_pos : int = param_name.find(':')

                if type_sep_pos != -1 :
                    param_name = param_name[type_sep_pos+1:]
                
                parsed_url.append(str(args.get(param_name)))    
            else :
                parsed_url.append(s)
        
        return '/'.join(parsed_url)
    # def parse_url_with_args(self, **args)
    
    
    
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
        
        response = function(**args)

        profiler.stop()
        
        cost : float  = profiler._get_last_session_or_fail().root_frame()
        if cost:
            cost = cost.time()
        else:
            cost = 0.0
        
        self.__local_energy_data.add_arg_cost(str(args), round(cost, 3))
        
        return response
    # def monitor_function_call(self, function, **args)  
    
    
    
    def process_arguments(self, objective : float, arguments : list[float]):
        """process_arguments

        Args:
            objective (float): _description_
            arguments (list[float]): _description_
        """
        
        if objective < 0:
            logging.warn(f"{self._name} has not objective defined.")
            pass
        logging.info(f"{self._name} has an objective of {objective}")

        endpoints = self.get_neighbouring_enpoints_consumption() # TODO : coder
        
        if self._filter.count > self._threshold :
            pass
        else:
            pass
    # def process_arguments(self, objective : float, arguments: list[float])



    def distribute_objective(objective : float, endpoints_costs : dict[str, interval]):
        # TODO
        pass
    # def distribute_objective(objective : float, endpoints_costs : dict[str, interval])



    def get_neighbouring_enpoints_consumption() -> dict[str, interval]:
        """Returns a map containing the consumption of all neighbouring endpoints, keyed by their URL 

        Returns:
            dict[str, interval]: a map { URL -> consumption interval }
        """
        # TODO
        pass
    # def get_neighbouring_enpoints_consumption() -> dict[str, interval]
    
    
    
    def get_treshold(self) -> float :
        """get_treshold

        Returns:
            float: _description_
        """
        return self.__treshold
    # def get_treshold(self) -> float
    
    
    
    def get_local_energy_data(self) -> LocalEnergyData :
        return self.__local_energy_data
    # def get_local_energy_data(self) -> LocalEnergyData
# class EnergyMonitorRoute(object)