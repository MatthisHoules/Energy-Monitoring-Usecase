import logging
from bloompy import CountingBloomFilter
from interval import interval
from joulehunter import Profiler

class EndpointMonitoringService:

    _name : str
    """ name of the functions for logging purposes """

    _local_functions_consumption : dict[tuple, list[float]] = {}
    """ the latest recorded consumption of a function and its called arguments. the callee is mapped by his arguments """

    _filter : CountingBloomFilter
    """ counting bloom filter to assess whether to evaluate using the MCKP or not """

    def __init__(self, name, threshold = 10) -> None:
        self._name = name
        self._filter = CountingBloomFilter
        self._threshold = threshold
        self._local_energy_consumption = -1


    def monitor_function_call(self, objective : float, **args) -> tuple(float, object):
        profiler = Profiler()
        profiler.start()

        frame = profiler._get_last_session_or_fail().root_frame()
        if frame:
            frame = frame.time()
        else:
            frame = 0.0
                        
        pass

    def get_objectives(self, objective, **arguments) -> tuple[dict[str, str], list[float]]:
        if objective < 0:
            logging.warn(f"{self._functions_name[function]} has not objective defined.")
            pass
        logging.info(f"{self._functions_name[function]} has an objective of {objective}")


        endpoints = get_neighbouring_enpoints_consumption() 

        if self._filter.count > self._threshold:
            pass
        else:
            pass

    def get_neighbouring_enpoints_consumption() -> dict[str, interval]:
        pass