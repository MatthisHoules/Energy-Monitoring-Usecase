import logging
from bloompy import CountingBloomFilter
from interval import interval
from joulehunter import Profiler

from .local_energy_data import LocalEnergyData

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


        
        frame = profiler._get_last_session_or_fail().root_frame()
        if frame:
            frame = frame.time()
        else:
            frame = 0.0

    def process_arguments(self, objective : float, arguments: list[float]):
        if objective < 0:
            logging.warn(f"{self._name} has not objective defined.")
            pass
        logging.info(f"{self._name} has an objective of {objective}")


        endpoints = get_neighbouring_enpoints_consumption() # TODO : coder
        

        if self._filter.count > self._threshold:
            pass
        else:
            pass

    def distribute_objective(objective : float, endpoints_costs : dict[str, interval]):
        pass

    def get_neighbouring_enpoints_consumption() -> dict[str, interval]:
        """Returns a map containing the consumption of all neighbouring endpoints, keyed by their URL 

        Returns:
            dict[str, interval]: a map { URL -> consumption interval }
        """
        pass
