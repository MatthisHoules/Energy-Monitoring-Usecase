# External Imports
from functools import reduce
from interval import interval
from sklearn.neighbors import KNeighborsRegressor
import yaml
import numpy as np
import pandas as pd


# TODO SKLEARN KNN --> retrain to test, predict TODO
# TODO Refacto : LocalEnergyData in EnergyMonitoringRoute ?
# TODO remove prints
# TODO Documentation
class LocalEnergyData(object):
    """Caching of latest recorded consumption for a single endpoint
    """

    def __init__(self, treshold : int, n_monitored_args : int, monitored_args_name : list[str]) -> None :
        """__init__
        """
        
        self.__args_costs : dict[str, list[int]] = dict()
        """the latest recorded consumption of a function and its called arguments. the callee is mapped by his arguments"""

        self.__monitored_args_name = monitored_args_name
        self.__error_cost : int = 20
        self.__treshold : int = treshold
        self.__cost_to_args : list[tuple[int, dict[str, int]]] = list()
        self.__n_monitored_args : int = n_monitored_args
        self.__knn_model : KNeighborsRegressor = KNeighborsRegressor(weights="distance")
    # def __init__(self) -> None
 


    def contains_args(self, key : str) -> bool :
        """_summary_

        Args:
            tuple (_type_): _description_

        Returns:
            bool: _description_
        """
        
        return key in self.__args_costs.keys()
    # def contains_args(self, tuple) -> bool
    
    
    
    def get_cost_interval(self) -> interval :
        """_summary_

        Returns:
            dict[str, float]: _description_
        """
        
        intervals : list[interval] = []
        
        for arg_combination in self.__args_costs.keys() :
            avg_cost = self.get_avg_cost_by_args(arg_combination)
            
            intervals.append(
                interval([
                    avg_cost - self.__error_cost if avg_cost - self.__error_cost >= 0 else 1,
                    avg_cost + self.__error_cost
                ])
            )

        return interval.union(intervals)
    # def get_cost_interval(self) -> dict[str, int]
    
    
    
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
            if len(self.__args_costs[key]) == self.__treshold :
                key_dict : dict = yaml.load(key, Loader=yaml.FullLoader)
                self.__cost_to_args.append(
                    (cost, key_dict)
                )
                self.__retrain_knn_model()
        else :
            self.__args_costs[key] = [cost]
    # def add_arg_cost(self, key : str, cost : float) -> None
    
    
    
    def __retrain_knn_model(self) -> None :
        """_summary_
        """
        
        cost, args = zip(*self.__cost_to_args)
        

        self.__knn_model = KNeighborsRegressor(n_neighbors=self.__n_monitored_args, weights="distance")
        self.__knn_model.fit(
            np.array(cost).reshape(-1, 1),
            pd.DataFrame(args)
        )
    # def __retrain_knn_model(self) -> None
    
    
    
    def predict_args_from_cost(self, cost : int) -> dict[str, int] :
        # TODO : DISTANCE WITH POINT (if cost already in --> return params) else predict
        
        predictions : tuple = self.__knn_model.predict([[cost]])[0]
        # TODO Verify good type for predictions var
        # TODO predictions to dict[str, int]
        return dict(zip(self.__monitored_args_name, map(round, predictions)))
    # def predict_args_from_cost(self, cost : int) -> dict[str, int] 
# class LocalEnergyData(object)