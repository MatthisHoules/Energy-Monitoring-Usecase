import logging
from bloompy import CountingBloomFilter
from interval import interval
from joulehunter import Profiler
import requests
from interval import interval
from .local_energy_data import LocalEnergyData

def get_neighbour(url: str) -> tuple(str, interval):
    res = requests.get(url).json()
    return (url, interval([res.get("lower"), res.get("upper")]))
    
class EndpointMonitoringService:
    """Service monitoring the energy consumption of a single endpoint. 
    It also provides the tuning of given arguments
    """

    def __init__(self, name, neighbours = [], threshold = 10) -> None:
        self._name : str = name
        """ name of the functions for logging purposes """

        self._filter : CountingBloomFilter = CountingBloomFilter
        """ counting bloom filter to assess whether to evaluate using the MCKP or not """

        self._threshold : float = threshold

        self._local_energy_data : LocalEnergyData = LocalEnergyData
        self._neighbours : list[str] = neighbours
        """ urls of the neighbouring endpoints """

    def monitor_function_call(self, objective : float, **args):
        profiler = Profiler()
        profiler.start()
        
        # TODO : Call function and mo

        frame = profiler._get_last_session_or_fail().root_frame()
        consumption = 0.0
        if frame:
            consumption = frame.time() # time is the consumption in joules. JouleHunter did not modify this name

        

    def process_arguments(self, objective : float, arguments: list[float]) -> list[float]:
        if objective < 0:
            logging.warn(f"{self._name} has not objective defined.")
            pass
        logging.info(f"{self._name} has an objective of {objective}")


        endpoints = self.get_neighbouring_enpoints_consumption() # TODO : coder
        

        if self._filter.count > self._threshold:
            endpoints[self._name] = self._local_energy_data.get_avg_cost(arguments)
        else:
            # TODO : Retirer objectif calculé depuis KNN ou plus cout le plus proche ? 
            pass

        self.distribute_objective(objective, endpoints)

    def distribute_objective(objective : float, endpoints_costs : dict[str, interval]):
        pass

    def get_neighbouring_enpoints_consumption(self) -> dict[str, interval]:
        """Returns a map containing the consumption of all neighbouring endpoints, keyed by their URL 

        Returns:
            dict[str, interval]: a map { URL -> consumption interval }
        """
        dict(map(get_neighbour, self._neighbours))