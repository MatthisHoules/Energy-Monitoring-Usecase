from joulehunter import Profiler, renderers
import env
import pymongo
mongo_client = pymongo.MongoClient(env.get("MONGO_ADDRESS")

mongo_db = mongo_client["energy_monitoring"]
monitoring_col = mongo_db["energy"]

class EnergyMonitoring(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
    
    def __init__(self, endpoint_name : str, endpoint_url : str, n_run_endpoint : int = 10, *args, **kwargs):
        """_summary_
        """

        self._endpoint_name : str = endpoint_name
        self._endpoint_url : str = endpoint_url   
        self._n_run_endpoint : int = n_run_endpoint 
        self._args = args
        self._kwargs = kwargs
    # def __init__(self, endpoint_name : str, endpoint_url : str, *args, **kwargs)

    def __call__(self, obj):
        """_summary_

        Args:
            obj (_type_): _description_
        """
        
        import itertools
        keys, values = zip(*self._kwargs.items())
        permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]

        for v in permutations_dicts:
            mean_joules : float = 0.0
            
            for _ in range(self._n_run_endpoint) :
                with Profiler(interval=0.0001) as p:
                    obj(**v)
                    
                frame = p._get_last_session_or_fail().root_frame()
                if frame:
                    mean_joules += frame.time()
                else:
                    mean_joules += 0.0
                
                del p
                
            mean_joules /= self._n_run_endpoint
            print("\n"*5, self._endpoint_name, mean_joules, "\n"*5)
                
            monitoring_col.insert_one(
                {
                    "endpoint_name" : self._endpoint_name,
                    "endpoint_url" : self._endpoint_url,
                    "joules": mean_joules,
                    **v
                }
            )
    # def __call__(self, obj)
# class EnergyMonitoring(object)