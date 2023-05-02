import itertools
      
class EnergyMonitorRoute(object) :
    """_summary_

    Args:
        object (_type_): _description_
    """
    
    
    
    def __init__(self, url : str, monitored_params : dict):
        """_summary_

        Args:
            endpoint (str): _description_
            url (str): _description_
            monitored_params (dict): _description_
        """
        
        self.url : str = url
        self.monitored_params : dict = monitored_params
    # def __init__(self, endpoint : str, url : str, monitored_params : dict)
    
    
    
    def parse_url_with_params(self, **params) :
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
                
                parsed_url.append(str(params.get(param_name)))    
            else :
                parsed_url.append(s)
        
        return '/'.join(parsed_url)
    # def parse_url_with_params(self, **params)
    
    
    
    def get_params_combinations(self) :
        """_summary_

        Returns:
            _type_: _description_
        """
        
        keys, values = zip(*self.monitored_params.items())
        return [dict(zip(keys, v)) for v in itertools.product(*values)]
    # def get_params_combinations(self)
# class EnergyMonitorRoute(object)