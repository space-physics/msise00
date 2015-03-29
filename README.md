# msise-00
NRL MSISE-00 atmospheric model

All credit to original authors, I slightly modified the Fortran 77 
code so it could compile in a modern compiler. 

```
f2py3 -m gtd7 -c nrlmsise00_sub.for 
```
plot by:
```
python demo_msis.py
```

Prereqs:
--------
``` pip install -r requirements.txt ```

#### Reference
Original fortran code from
http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/


