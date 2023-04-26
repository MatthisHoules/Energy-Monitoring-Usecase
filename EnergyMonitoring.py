from joulehunter import Profiler, renderers

class EnergyMonitoring(object):
    """_summary_

    Args:
        object (_type_): _description_
    """
    
    def __init__(self, app, *args, **kwargs):
        """_summary_
        """
        
        self._app = app
        
        self._kwargs = kwargs
    # def __init__(self, *args, **kwargs)

    def __call__(self, obj):
        """__call__

        Args:
            obj (_type_): _description_
        """
        
        import itertools
        keys, values = zip(*self._kwargs.items())
        permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]

        for v in permutations_dicts : 
            for i in range(1) :
                
                print(v)
                with Profiler(interval=0.0001) as p:
                    obj(**v)

                # print(p.output(
                #     renderers.JSONRenderer(show_all=True)
                # ))
                del p
    # def __call__(self, obj)