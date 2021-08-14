# -*- coding: utf-8 -*-

import pandas as pd
from shapely.ops import cascaded_union

from geoapyfr.admin.get_commune import get_commune
from geoapyfr.admin._get_departement_list import _get_departement_list

def get_departement(region=None, departement=None,
                    geometry=False, geo='france-zoom-overseas-paris'):
    
    deps = _get_departement_list(region=region)
    deps.columns = list_col = ['departement_nom', 'departement_code', 'region_code']
    
    
    if geometry is True:
        communes = get_commune(region=region,
                               geometry=geometry,
                               geo=geo)
        
        dep_list = communes.departement_code.unique()
        
        if departement is not None:
            dep_list = [dep for dep in dep_list if dep in departement]
            
        list_dep_with_geom = []
        
        for d in dep_list:
            df = communes[communes['departement_code'] == d]
            polygons = df['geometry'].to_list()
            population = sum(df['population'])
            surface = sum(df['surface'])
            df = df[list_col].drop_duplicates()
            new_poly = cascaded_union(polygons)
            try:
                df['geometry'] =  new_poly
            except:
                df['geometry'] =  [new_poly]
            df['population'] = population
            df['surface'] = surface
            list_dep_with_geom.append(df)
        
        deps = pd.concat(list_dep_with_geom)  
    
    if departement is not None:
        deps = deps[deps['departement_code'].isin(departement)]
        
    deps = deps.reset_index(drop=True)
    
    return(deps)
