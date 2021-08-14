# -*- coding: utf-8 -*-

import os
import appdirs
import pandas as pd
from tqdm import trange
from shapely.affinity import translate

from geoapyfr.admin._get_commune_from_departement import _get_commune_from_departement
from geoapyfr.admin._get_departement_list import _get_departement_list
from geoapyfr.admin._get_region_list import _get_region_list
from geoapyfr.admin._extract_bounds import _extract_bounds
from geoapyfr.admin._rescale_geom import _rescale_geom

def get_commune(region=None, departement=None, update=False,
                geometry=False, geo = 'france-zoom-overseas-paris'):
    """Get a list of communes

    Args:
        region (list, optional): A list of region codes to narrow down the search.
         Defaults to None, all communes will be delivered.
        departement (list, optional): A list of departement codes to narrow down the search.
         Defaults to None, all communes will be delivered.
        update (bool, optional): Data are stored on locally on the machine, their are used later on.
         To force the data update, set update=True. Defaults to False.
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
    list_geo = [ 
        'france-all',
        'france-metropolitan', 
        'france-zoom-overseas',
        'france-zoom-paris', 
        'france-zoom-overseas-paris'] 
    
    if (region is not None) | (departement is not None):
        geo = 'france-all'
    
    if geo not in list_geo:
        raise ValueError('!!! geo should be in : {} !!!'.format(' '.join(list_geo)))
    
    local_appdata_folder = appdirs.user_cache_dir()
    geoapyfr_folder = local_appdata_folder + '/geoapyfr'

    # create  folder
    if not os.path.exists(geoapyfr_folder):
        os.mkdir(geoapyfr_folder)
        
    link_file = geoapyfr_folder + '/communes'
    if geometry is False:
        link_file += '_centre'  

    link_file_geo = link_file + '_' + geo

    if ((not os.path.exists(link_file_geo)) | (update)):  
    
        if ((not os.path.exists(link_file)) | (update)):
            
            reg = _get_region_list()
            
            reg_list = reg.region_code.to_list()
            
            if region is not None:
                reg_list = [reg for reg in reg_list if reg in region]
            
            deps = _get_departement_list(region=reg_list)
            
            deps_list = deps.code.to_list()
            
            if departement is not None:
                deps_list = [dep for dep in deps_list if dep in departement]
            
            coms = []
            
            for j in trange(len(deps_list)):
                
                df = _get_commune_from_departement(d=deps_list[j],
                                                update=update,
                                                geometry=geometry)       
                        
                coms.append(df)
            
            communes = pd.concat(coms).reset_index(drop=True)
            if region is None:
                if departement is None:                
                    communes.to_pickle(link_file)
        else:
            try:
                communes = pd.read_pickle(link_file)
            except:
                os.remove(link_file)
                communes = get_commune(region=region,
                                    departement=departement,
                                    geometry=geometry,
                                    geo=geo,
                                    update=True)
            
    #
    # Translate and zoom on overseas departements and Paris
    #
    

        communes['geometry'] = communes['geometry'].to_list()
        list_ovdep = ['971', '972', '973', '974', '976']
        fm = communes[~communes['departement_code'].isin(list_ovdep)]
        fm = fm.reset_index(drop=True)
        
        if geo == 'france-metropolitan':
            communes = fm        
        
        if (geo not in ['france-all', 'france-metropolitan']) & (geometry is True):
            
            list_dept_available = communes['departement_code'].unique()
            
            if all([dpt in list_dept_available for dpt in list_ovdep + ['29']]):
        
                dep29 =  communes[communes['departement_code'].isin(['29'])]
                dep29 = dep29.reset_index(drop=True)
                minx = min(_extract_bounds(geom=dep29['geometry'], var='minx'))
                miny = min(_extract_bounds(geom=dep29['geometry'], var='miny')) + 3
                
                list_new_dep = []         
                    
                for d in range(len(list_ovdep)):
                    ovdep = communes[communes['departement_code'].isin([list_ovdep[d]])]
                    ovdep = ovdep.reset_index(drop=True)
                    if list_ovdep[d] == '973':
                        # area divided by 4 for Guyane
                        ovdep = _rescale_geom(df=ovdep, factor = 0.25)
                    
                    maxxdep = max(_extract_bounds(geom=ovdep['geometry'], var='maxx'))
                    maxydep = max(_extract_bounds(geom=ovdep['geometry'], var='maxy'))
                    xoff = minx - maxxdep - 2.5
                    yoff = miny - maxydep
                    ovdep['geometry'] = ovdep['geometry'].apply(lambda x: translate(x, xoff=xoff, yoff=yoff))
                    
                    
                    miny = min(_extract_bounds(geom=ovdep['geometry'], var='miny')) - 1.5
                    list_new_dep.append(ovdep)
                
                # PARIS
                paris = communes[communes['departement_code'].isin(['75','92', '93','94'])]
                paris = paris.reset_index(drop=True)
                paris = _rescale_geom(df = paris, factor = 4)
                
                dep29 =  communes[communes['departement_code'].isin(['29'])]
                dep29 = dep29.reset_index(drop=True)
                minx = min(_extract_bounds(geom=dep29['geometry'], var= 'minx'))
                miny = min(_extract_bounds(geom=dep29['geometry'], var= 'miny')) + 3
                
                maxxdep = max(_extract_bounds(geom=paris['geometry'], var= 'maxx'))
                maxydep = max(_extract_bounds(geom=paris['geometry'], var= 'maxy'))
                xoff = minx - maxxdep + 1
                yoff = miny - maxydep - 5
                paris['geometry'] = paris['geometry'].apply(lambda x: translate(x, xoff=xoff, yoff=yoff))
                
                
                if geo == 'france-zoom-overseas-paris':        
                    communes = pd.concat(list_new_dep + [fm] + [paris])
                elif geo == 'france-zoom-paris':
                    communes = pd.concat([fm] + [paris])
                elif geo == 'france-zoom-overseas':
                    communes = pd.concat(list_new_dep + [fm])

                if region is None:
                    if departement is None:  
                        communes.to_pickle(link_file_geo)
    else:
        try:
            communes = pd.read_pickle(link_file_geo)
        except:
            os.remove(link_file_geo)
            communes = get_commune(region=region,
                                   departement=departement,
                                   geometry=geometry,
                                   geo=geo,
                                   update=True)

    if region is not None:
        communes = communes[communes['region_code'].isin(region)]
    if departement is not None:
        communes = communes[communes['departement_code'].isin(departement)]

    communes = communes.reset_index(drop=True)   
     
    return(communes)
            
   
            
