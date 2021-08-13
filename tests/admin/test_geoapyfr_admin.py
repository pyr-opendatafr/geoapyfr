# -*- coding: utf-8 -*-

from unittest import TestCase
import pandas as pd
import geopandas as gpd
import sys

from geoapyfr.admin.get_commune import get_commune

class TestFunction(TestCase):

    def test_get_commune(self):

        list_geo = [ 
        'france-all',
        'france-metropolitan', 
        'france-zoom-overseas',
        'france-zoom-paris', 
        'france-zoom-overseas-paris'] 

        test = True

        for geo in list_geo:
            df = get_commune(geometry=True, geo=geo)
            test = test & isinstance(df, pd.DataFrame)

        self.assertTrue(test)

        def get_commune_crash():
            return(get_commune(geo='test'))

        self.assertRaises(ValueError, get_commune_crash)
