# -*- coding: utf-8 -*-

import pandas as pd
from shapely.ops import cascaded_union

from geoapyfr.admin.get_commune import get_commune
from geoapyfr.admin._get_departement_list import _get_departement_list

def get_departement(region=None, departement=None,
                    geometry=False, geo='france-zoom-overseas-paris'):
    """Get a list of communes

    Args:
        region (list, optional): A list of region codes to narrow down the search.
         Defaults to None, all departements will be delivered.
        departement (list, optional): A list of departement codes to narrow down the search.
         Defaults to None, all departements will be delivered.
        geometry (bool, optional): If True it provides geographic limits, if False only the center point is rendred. Defaults to False.
        geo (str, optional): To better display French territory, by default several geographic locations are modified.
         Overseas territory are artificial located close to French shores and a zoom on parisian departements is rendered.
         Available options are:
         geo='france-all' (geographic limits are provided as is)
         geo='france-metropolitan' (overseas departements are excluded)
         geo='france-zoom-paris' (overseas departements are excluded and a zoom on Paris is rendered)
         geo='france-zoom-overseas' (overseas departements are included in a zoom)
         geo='france-zoom-overseas-paris' (the zoom includes overseas departements and Paris)
         Defaults to 'france-zoom-overseas-paris'.

    Raises:
        ValueError: geo should be in above-mentioned list 
    """    
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
