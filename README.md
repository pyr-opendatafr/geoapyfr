Geoapyfr Package Overview
=========================

[![Build Status](https://github.com/hadrilec/geoapyfr/actions/workflows/master.yml/badge.svg)](https://github.com/hadrilec/geoapyfr/actions)
[![Codecov test coverage](https://codecov.io/gh/hadrilec/geoapyfr/branch/master/graph/badge.svg)](https://codecov.io/gh/hadrilec/geoapyfr?branch=master)

The geoapyfr package contains tools to easily download data from
geo.api.gouv.fr API. Geoapyfr gives a quick access to a list of French
administrative areas, with their geographic limits, population and
surface area. Have a look at the detailed API page with the following
[link](https://geo.api.gouv.fr/). This package is a contribution to
reproducible research and public data transparency. It benefits from the
developments made by DINUM's teams working on APIs.

Installation
------------

```
# Get the development version from GitHub
# git clone https://github.com/hadrilec/geoapyfr.git
# cd geoapyfr
# pip install .
```

Data Search and Collection Advice
---------------------------------
To get all communes from one or several departements/regions, please do the following:
* First, use ```get_region``` to have a full list of French regions and their identifier code
* Then, use ```get_departement``` to get the list of departements in one or several regions
* Finally, use ```get_commune``` to get the communes
* NB : ```geometry=True``` will give the geographic limits of each commune, departement or region

``` python 
from geoapyfr.admin import get_commune, get_departement, get_region

reg = get_region()

dep = get_departement(region = ['93'], geometry = True)

commune = get_commune(departement = ['84'], geometry=True)

```

Population Density By Commune
-----------------------------

![image](https://raw.githubusercontent.com/hadrilec/geoapyfr/master/examples/population_density_by_commune.png)

``` python

from pandas.api.types import CategoricalDtype    
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import descartes  
import geopandas as gpd

from geoapyfr.admin.get_commune import get_commune  

communes = get_commune(geometry=True)                     
                                      
d = gpd.GeoDataFrame(communes, geometry='geometry')
d['density'] = 100 * d['population'] / d['surface']

d.loc[d.density < 40, 'range'] = "< 40"
d.loc[d.density >= 20000, 'range'] = "> 20 000"

density_ranges = [40, 100, 120, 160, 200, 240, 260, 410, 600, 1000, 5000, 20000]
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
    legend_kwds={'bbox_to_anchor': (1.1, 0.9),
                 'title':'density per km2'})
ax.set_axis_off()
ax.set(title='Distribution of population in France')
plt.show()

```

How to avoid proxy issues ?
---------------------------

``` python

```

Support
-------

Feel free to open an issue with any question about this package using
\<<https://github.com/hadrilec/geoapyfr/issues>\> Github repository.

Contributing
------------

All contributions, whatever their forms, are welcome. See
CONTRIBUTING.md
