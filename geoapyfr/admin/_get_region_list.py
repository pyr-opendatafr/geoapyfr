# -*- coding: utf-8 -*-

import requests
import pandas as pd
from functools import lru_cache

@lru_cache(maxsize=None)
def _get_region_list():
    
    apigeo_link = 'https://geo.api.gouv.fr/'
            
    results = requests.get(apigeo_link + 'regions')
    
    data = results.json()
    
    reg = pd.DataFrame(data)
    
    reg.columns = 'region_' + reg.columns
    
    return(reg)
    