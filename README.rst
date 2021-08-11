.. role:: raw-html-m2r(raw)
   :format: html

Geoapyfr Package Overview
=========================

**Work in progress**

.. image:: https://github.com/InseeFrLab/Py-Insee-Data/actions/workflows/master.yml/badge.svg
   :target: https://github.com/InseeFrLab/Py-Insee-Data/actions
   :alt: Build Status

.. image:: https://codecov.io/gh/InseeFrLab/Py-Insee-Data/branch/master/graph/badge.svg?token=TO96FMWRHK
   :target: https://codecov.io/gh/InseeFrLab/Py-Insee-Data?branch=master
   :alt: Codecov test coverage

.. image:: https://readthedocs.org/projects/pynsee/badge/?version=latest
   :target: https://pynsee.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

The geoapyfr package contains tools to easily download data from geo.api.gouv.fr API.
Geoapyfr gives a quick access to a list of French administrative areas, with their geographic limits, population and surface area. 
Have a look at the detailed API page with the following `link <https://geo.api.gouv.fr/>`_.
This package is a contribution to reproducible research and public data transparency. 
It benefits from the developments made by DINUM's teams working on APIs.

Installation
------------

.. code-block:: python
 
   # Get the development version from GitHub
   # git clone https://github.com/hadrilec/geoapyfr.git
   # cd geoapyfr
   # pip install .

Population Density By Commune
-----------------------------

.. image:: https://raw.githubusercontent.com/InseeFrLab/Py-Insee-Data/master/docs/examples/pictures/example_gdp_picture.png?token=AP32AXOVNXK5LWKM4OJ5THDAZRHZK

.. literalinclude:: population_density_by_commune.py
   

How to avoid proxy issues ?
---------------------------

.. code-block:: python

   # Use the proxy_server argument of the init_conn function to change the proxy server address   
   from pynsee.utils.init_conn import init_conn
   init_conn(insee_key="my_insee_key",
             insee_secret="my_insee_secret",
             proxy_server="http://my_proxy_server:port")

   # Beware : any change to the keys should be tested after having cleared the cache
   # Please do : from pynsee.utils import *; clear_all_cache()

Support
-------

Feel free to open an issue with any question about this package using <https://github.com/hadrilec/Geoapyfr/issues> Github repository.

Contributing
------------

All contributions, whatever their forms, are welcome. See CONTRIBUTING.md