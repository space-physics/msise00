.. image:: https://zenodo.org/badge/32971905.svg
   :target: https://zenodo.org/badge/latestdoi/32971905
.. image:: https://travis-ci.org/scivision/msise00.svg
    :target: https://travis-ci.org/scivision/msise00
.. image:: https://coveralls.io/repos/scivision/msise00/badge.svg?branch=master&service=github 
   :target: https://coveralls.io/github/scivision/msise00?branch=master 

==========
msise-00
==========
NRL MSISE-00 atmospheric model.  Said to be valid from altitude z = 0 - 1000 km.

The plot immediately below shows a slice at 200km on a world-wide grid.
The yellow ball represents the sun footprint on Earth.

.. image:: tests/msise00_demo.gif

Installation
-------------
::

  python setup.py install

Example Usage:
--------------
This outputs a series of PNGs to your temp directory::

  python DemoMSIS.py

Reference
---------
`Original fortran code <http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/>`_

`1200+ citations 2002 paper <http://onlinelibrary.wiley.com/doi/10.1029/2002JA009430/pdf>`_
