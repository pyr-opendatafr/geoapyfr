# -*- coding: utf-8 -*-

from pandas.api.types import CategoricalDtype    
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import descartes  
import geopandas as gpd

from geoapyfr.admin.get_commune import get_commune  

communes = get_commune()                     
                                      
d = gpd.GeoDataFrame(communes, geometry='geometry')
d['density'] = 100 * d['population'] / d['surface']

d.loc[d.density < 40, 'range'] = "< 40"
d.loc[d.density >= 20000, 'range'] = "> 20 000"

density_ranges = [40, 50, 70, 100, 120, 160, 200, 240, 260, 410, 600, 1000, 5000, 20000]
list_ranges = []
list_ranges.append( "< 40")

for i in range(len(density_ranges)-1):
    min = density_ranges[i]
    max = density_ranges[i+1]
    range_string = "[{}, {}[".format(min, max)
    d.loc[(d.density >= min) & (d.density < max), 'range'] = range_string
    list_ranges.append(range_string)

list_ranges.append("> 20 000")

d['range'] = d['range'].astype(CategoricalDtype(categories=list_ranges, ordered=True))

fig, ax = plt.subplots(1,1,figsize=[10,10])
d.plot(column='range', cmap=cm.viridis,
    legend=True, ax=ax,
    legend_kwds={'bbox_to_anchor': (1.1, 0.8),
                 'title':'density per km2'})
ax.set_axis_off()
ax.set(title='Distribution of population in metropolitan France')
plt.show()
