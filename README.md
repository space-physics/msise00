# msise-00
NRL MSISE-00 atmospheric model

The plot immediately below shows a slice at 200km on a world-wide grid. The yellow ball represents the sun footprint on Earth.

![msis global at 200km](http://blogs.bu.edu/mhirsch/files/2015/04/demo200km1.gif)

All credit to original authors, I slightly modified the Fortran 77 
code so it could compile in a modern compiler. 

Installation:
-------------
```
git clone --recursive https://github.com/scienceopen/msise00

pip install -r requirements.txt 

f2py -m gtd7 -c nrlmsise00_sub.for 
```
plot by:
```
python demo_msis.py
```

#### Reference
Original fortran code from
http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/

[>1200 citations 2002 paper](http://onlinelibrary.wiley.com/doi/10.1029/2002JA009430/pdf)


