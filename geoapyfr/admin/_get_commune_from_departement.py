# -*- coding: utf-8 -*-

import appdirs
import os
import requests
import pandas as pd
from shapely.geometry import MultiPolygon, Polygon, shape

def _get_commune_from_departement(d, update, geometry):
    
    local_appdata_folder = appdirs.user_cache_dir()
    geoapyfr_folder = local_appdata_folder + '/geoapyfr'

    # create  folder
    if not os.path.exists(geoapyfr_folder):
        os.mkdir(geoapyfr_folder)
    link_file = geoapyfr_folder + '/communes' + '_' + d
    
    if (not os.path.exists(link_file)) | (update):
        
        apigeo_link = 'https://geo.api.gouv.fr/'
    
        req_fields = '?fields=nom,code,codesPostaux,centre,surface,contour,codeDepartement,departement,codeRegion,region,population&format=geojson'
        if geometry is True:
            req_fields += '&geometry=contour'
        
        link = apigeo_link + 'departements/{}/communes'.format(d) + req_fields
        results = requests.get(link)
        data = results.json()['features']
        
        coms = []
        
        for c in range(len(data)): 
               
            df = data[c]['properties']
            
            com = {}
            
            for o in df.keys():
                if type(df[o]) == dict:
                    for k in df[o].keys():
                        com[str(o) + '_' + str(k)] = df[o][k]
                elif type(df[o]) == list:
                    com[o] = ','.join(df[o])
                else:
                    com[o] = df[o]
            
            geom = data[c]['geometry']['coordinates']
            
            d = pd.DataFrame(com, index=[0])
                        
            # commune area is one plain polygon without hole
            if len(geom) == 1:
                g = Polygon(geom[0])
                d['geometry'] = g
            else:
                # commune area splitted in several polygons
                
                if all([len(geom[i]) == 1 for i in range(len(geom))]):
                    # commune area with several plain polygons without hole
                   
                    list_g = [[geom[i][0] for i in range(len(geom))]]
                    d['geometry'] = shape({"type":"MultiPolygon",
                                           "coordinates": list_g})
                
                else:
                    polygon_len_test = [len(geom[i]) == 1 for i in range(len(geom))]
                    if any(polygon_len_test):
                        # commune area with several polygons and some have holes inside
                        # eg Bouloc-en-Quercy  j=80 c=20   
                        list_polygon = []
                        for i in range(len(geom)):
                           if len(geom[i]) == 1:
                               polygon = Polygon(geom[i][0])                         
                           else:
                               polygon = Polygon(geom[i][0], [geom[i][j] for j in range(1, len(geom[i]))])
                           list_polygon.append(polygon)
                        multi_poly = MultiPolygon(list_polygon)
                        d['geometry'] = [multi_poly]
                                             
                    else:
                        # commune area in one polygon with holes inside
                        # eg Beauvernois j=24 c=27
                        g = Polygon(geom[0], [geom[i] for i in range(1, len(geom))])
                        d['geometry'] = g
                        
            coms.append(d)
            
            communes = pd.concat(coms).reset_index(drop=True)
            communes.to_pickle(link_file)
            
    else:
        
        try:
            communes = pd.read_pickle(link_file)
        except:
            os.remove(link_file)
            communes = _get_commune_from_departement(d=d, update=True)       
    
    return(communes)
                