# -*- coding: utf-8 -*-

import requests
import pandas as pd

from ._get_region_list import _get_region_list

def _get_departement_list(region=None):
    
    apigeo_link = 'https://geo.api.gouv.fr/'
    
    dep_list = []
    
    if region is None:
        reg = _get_region_list()    
        region = reg.code.to_list()
    
    for r in region:
        results = requests.get(apigeo_link + 'regions/{}/departements'.format(r))
        data = results.json()
        dep = pd.DataFrame(data)
        dep_list.append(dep)
    
    deps = pd.concat(dep_list).reset_index(drop=True)
    
    return(deps)
    
    