from functools import reduce

class LocalEnergyData(object):
    """Caching of latest recorded consumption for a single endpoint
    """

    def __init__(self) -> None :
        """__init__
        """
        
        self.__args_costs : dict[str, list[int]] = dict()
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
    
    
    
    def get_avg_costs(self) -> dict[str, int] :
        """_summary_

        Returns:
            dict[str, float]: _description_
        """
        
        result_dict : dict[str, int] = dict()
        
        for arg_combination in self.__args_costs.keys() :
            result_dict[arg_combination] = self.get_avg_cost_by_args(arg_combination)
        
        return result_dict
    # def get_avg_costs(self) -> dict[str, int]
    
    
    
    def get_avg_cost_by_args(self, key : str) -> int:
        """get_avg_cost
        """
        
        costs = self.__args_costs.get(key, None)
        
        if costs is None :
            return 0
        
        return int(round(reduce(lambda x, y : x + y, costs) / len(costs), 0))
    # def get_avg_cost_by_args(self, key : str) -> int
    
    
    
    def add_arg_cost(self, key : str, cost : int) -> None :
        """_summary_

        Args:
            key (str): _description_
        """
        
        if self.contains_args(key) :
            self.__args_costs[key].append(cost)
        else :
            self.__args_costs[key] = [cost]
    # def add_arg_cost(self, key : str, cost : float) -> None
# class LocalEnergyData