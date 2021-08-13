# -*- coding: utf-8 -*-

import pandas as pd
from shapely.ops import cascaded_union

from geoapyfr.admin.get_commune import get_commune
from geoapyfr.admin._get_departement_list import _get_departement_list

def get_departement(region=None, geometry=False, geo='france-zoom-overseas-paris'):
    
    deps = _get_departement_list(region=region)
    deps.columns = list_col = ['departement_nom', 'departement_code', 'region_code']
    
    if geometry is True:
        communes = get_commune(region=region,
                               geometry=geometry,
                               geo=geo)
        
        dep_list = communes.departement_code.unique()
        
        list_dep_with_geom = []
        
        for d in dep_list:
            df = communes[communes['departement_code'] == d]
            polygons = df['geometry'].to_list()
            population = sum(df['population'])
            surface = sum(df['surface'])
            df = df[list_col].drop_duplicates()
            new_poly = cascaded_union(polygons)
            if len(new_poly) <= 1:
                df['geometry'] =  new_poly
            else:
                df['geometry'] =  [new_poly]
            df['population'] = population
            df['surface'] = surface
            list_dep_with_geom.append(df)
        
        deps = pd.concat(list_dep_with_geom)   
        
    deps = deps.reset_index(drop=True)
    
    return(deps)
