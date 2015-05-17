[![Code Climate](https://codeclimate.com/github/scienceopen/msise00/badges/gpa.svg)](https://codeclimate.com/github/scienceopen/msise00)

# msise-00
NRL MSISE-00 atmospheric model

The plot immediately below shows a slice at 200km on a world-wide grid. The yellow ball represents the sun footprint on Earth.

![msis global at 200km](http://blogs.bu.edu/mhirsch/files/2015/04/demo200km1.gif)

Installation:
-------------
```
git clone --depth 1 --recursive https://github.com/scienceopen/msise00
pip install -r requirements.txt 
make -f Makefile.f2py
```

Example Usage:
--------------
```
python demo_msis.py
```

#### Reference
Original fortran code from
http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/

[>1200 citations 2002 paper](http://onlinelibrary.wiley.com/doi/10.1029/2002JA009430/pdf)

If you don't have make (which you should have) you can manually compile by:
```
f2py -m gtd7 -c nrlmsise00_sub.for 
```
