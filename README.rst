.. image:: https://codeclimate.com/github/scienceopen/msise00/badges/gpa.svg
   :target: https://codeclimate.com/github/scienceopen/msise00
   :alt: Code Climate

==========
msise-00
==========
NRL MSISE-00 atmospheric model

The plot immediately below shows a slice at 200km on a world-wide grid.
The yellow ball represents the sun footprint on Earth.

`msis global at 200km <http://blogs.bu.edu/mhirsch/files/2015/04/demo200km1.gif>`_

Installation
-------------
from Terminal::

  git clone --depth 1 https://github.com/scienceopen/msise00
  conda install -r requirements.txt
  python setup.py install


Example Usage:
--------------
from Terminal::

  python demo_msis.py


Reference
---------
`Original fortran code <http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/>`_

`1200+ citations 2002 paper <http://onlinelibrary.wiley.com/doi/10.1029/2002JA009430/pdf>`_
