# -*- coding: utf-8 -*-

import pandas as pd
from functools import lru_cache
from shapely.ops import cascaded_union

from geoapyfr.admin._get_region_list import _get_region_list
from geoapyfr.admin.get_commune import get_commune

@lru_cache(maxsize=None)
def get_region(geometry=False, geo='france-zoom-overseas'):
    
    list_geo = [ 
        'france-all',
        'france-metropolitan', 
        'france-zoom-overseas'] 
    
    if geo not in list_geo:
        raise ValueError('!!! geo should be in : {} !!!'.format(' '.join(list_geo)))
    
    reg = _get_region_list()
    list_col = ['region_nom', 'region_code']
    reg.columns = list_col
    reg_list = reg.region_code.to_list()
    
    if geometry is True:
        communes = get_commune(region=reg_list,
                               geometry=geometry,
                               geo=geo)
                
        list_reg_with_geom = []
        
        for r in reg_list:
            df = communes[communes['region_code'] == r]
            polygons = df['geometry'].to_list()
            population = sum(df['population'])
            surface = sum(df['surface'])
            df = df[list_col].drop_duplicates()
            df['geometry'] =  [cascaded_union(polygons)]
            df['population'] = population
            df['surface'] = surface
            list_reg_with_geom.append(df)
        
        reg = pd.concat(list_reg_with_geom)   
    
    return(reg)
    
    
    
    