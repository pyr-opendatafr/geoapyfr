# -*- coding: utf-8 -*-

import pandas as pd
from functools import lru_cache
from shapely.ops import cascaded_union

from ._get_region_list import _get_region_list
from .get_commune import get_commune

@lru_cache(maxsize=None)
def get_region(geometry=False, geo='france-zoom-overseas-paris'):
        
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
            df = df[list_col].drop_duplicates()
            df['geometry'] =  cascaded_union(polygons)
            list_reg_with_geom.append(df)
        
        reg = pd.concat(list_reg_with_geom)   
    
    return(reg)
    
    
    
    