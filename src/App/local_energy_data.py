from functools import reduce
class LocalEnergyData:

    _args_costs : dict[str, list[float]] = dict()
    """ the latest recorded consumption of a function and its called arguments. the callee is mapped by his arguments """

    def contains_args(self, tuple) -> bool:
        return tuple in self._args_costs
    
    def get_avg_cost(self, tuple) -> float:
        costs = self._args_costs.get(tuple, [])
        
        if not len(costs):
            return 0.0
        
        return reduce(lambda x, y : x + y, costs) / len(costs)