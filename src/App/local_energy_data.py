from functools import reduce

class LocalEnergyData:
    """Caching of latest recorded consumption for a single endpoint
    """

    def __init__(self) -> None :
        """__init__
        """
        
        self.__args_costs : dict[str, list[float]] = dict()
        """the latest recorded consumption of a function and its called arguments. the callee is mapped by his arguments"""
    # def __init__(self) -> None



    def contains_args(self, key : str) -> bool:
        """_summary_

        Args:
            tuple (_type_): _description_

        Returns:
            bool: _description_
        """
        
        return key in self.__args_costs.keys()
    # def contains_args(self, tuple) -> bool
    
    
    
    def get_args_avg_cost(self, key : str) -> float:
        """get_avg_cost
            TODO
        """
        
        costs = self._args_costs.get(key, None)
        
        if costs is None :
            return 0.0
        
        return reduce(lambda x, y : x + y, costs) / len(costs)
    # def get_args_avg_cost(self, key : str) -> float
    
    
    
    def add_arg_cost(self, key : str, cost : float) -> None :
        """_summary_

        Args:
            key (str): _description_
        """
        
        if self.contains_args(key) :
            self.__args_costs[key].append(cost)
        else :
            self.__args_costs[key] = [cost]
            
        print(f"New cost added : {self.__args_costs}", self.__args_costs[key])
    # def add_arg_cost(self, key : str, cost : float) -> None
# class LocalEnergyData