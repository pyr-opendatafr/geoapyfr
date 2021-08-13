# -*- coding: utf-8 -*-

from unittest import TestCase
import pandas as pd
import geopandas as gpd
import sys

from geoapyfr.admin.get_commune import get_commune
from geoapyfr.admin.get_departement import get_departement
from geoapyfr.admin.get_region import get_region

class TestFunction(TestCase):

    def test_all(self):

        list_geo = [ 
        'france-all',
        'france-metropolitan', 
        'france-zoom-overseas',
        'france-zoom-paris', 
        'france-zoom-overseas-paris'] 

        test = True

        for geo in list_geo:
            for bool in [True, False]:             
                df = get_commune(geometry=bool, geo=geo)
                test = test & isinstance(df, pd.DataFrame)

                df = get_region(geometry=bool, geo=geo)
                test = test & isinstance(df, pd.DataFrame)
                
                df = get_departement(geometry=bool, geo=geo)
                test = test & isinstance(df, pd.DataFrame)
        
        df = get_commune(geometry=True, geo='france-zoom-overseas-paris')
        df = test & isinstance(df, pd.DataFrame)

        self.assertTrue(test)

        def get_commune_crash():
            return(get_commune(geo='test'))

        self.assertRaises(ValueError, get_commune_crash)
