# -*- coding: utf-8 -*-

from shapely.affinity import scale

def _rescale_geom(df, factor):
    df_bounds = df['geometry'].bounds
    maxxdf = df_bounds.maxx.max()
    minxdf = df_bounds.minx.min()
    maxydf = df_bounds.maxy.max()
    minydf = df_bounds.miny.min()
    center = ((maxxdf + minxdf) / 2, (maxydf + minydf) / 2)
    df['geometry'] =  df['geometry'].scale(xfact=factor,
                                           yfact=factor,
                                           zfact=1.0, origin=center)
    
    return(df) 