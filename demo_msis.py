#!/usr/bin/env python3
"""
NOTE: The performance of this demo has not been checked at all.
Please do basic sanity checks of output.
Quick demo of calling NRL MSISE-00 using f2py3 from Python
Michael Hirsch
bostonmicrowave.com

Original fortran code from
http://nssdcftp.gsfc.nasa.gov/models/atmospheric/msis/nrlmsise00/
"""
from __future__ import division
from pandas import Series, DataFrame
from numpy import arange
from matplotlib.pyplot import figure,show
#
import gtd7

def testgtd7(ip,ap,altkm):
    stl = ip['sec']/3600 + ip['glon']/15

    dens = []; temp=[]
    for a in altkm:
        d,t = gtd7.gtd7(ip['iyd'],ip['sec'],a,ip['glat'],ip['glon'],stl,
                    ip['f107a'],ip['f107'], ap,ip['mass'])
        dens.append(d)
        temp.append(t)

    densdf = DataFrame(dens, index=altkm,
                       columns=['He','O','N2','O2','Ar','Total','H','N','AnomalousO'])
    tempdf = DataFrame(temp, index=altkm, columns=['exotemp','heretemp'])

    return densdf,tempdf

def plotgtd(dens,temp):
    ax = figure().gca()
    for g in dens.columns:
        if g != 'Total':
            ax.semilogx(dens[g], dens.index, label=g)
    ax.legend(loc='best')
    ax.set_xlim(left=1e3)
    ax.set_ylabel('altitude [km]')
    ax.set_xlabel('density [cm$^{-3}$]')
    ax.grid(True)
    ax.set_title('Number Density from MSISE-00')

    ax = figure().gca()
    ax.semilogx(dens['Total'],dens.index)
    ax.set_xlabel('Total Mass Density [gm/cm^-3]')
    ax.set_ylabel('altitude [km]')
    ax.grid(True)
    ax.set_title('Total Mass Density from MSISE-00')

    ax = figure().gca()
    ax.plot(temp['heretemp'],temp.index)
    ax.set_xlabel('Temperature')
    ax.set_ylabel('altitude [km]')
    ax.grid(True)
    ax.set_title('Temperature from MSISE-00')

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='calls MSISE-00 from Python, a basic demo')
    p.add_argument('iyd',help='day of year [0-366]',type=int,nargs='?',default=172)
    p.add_argument('utsec',help='utc second from midnight [0-86400]',type=float,nargs='?',default=29000)
    p.add_argument('altkm',help='altitude (km) (start,stop,step)',type=float,nargs='?',default=(60,1000,5))
    p.add_argument('glat',help='geodetic latitude (deg)',type=float,nargs='?',default=60)
    p.add_argument('glon',help='geodetic longitude (deg)',type=float,nargs='?',default=-70)
    p.add_argument('F107a',help=' 81 day AVERAGE OF F10.7 FLUX (centered on day DDD)',type=float,nargs='?',default=150)
    p.add_argument('F107',help='DAILY F10.7 FLUX FOR PREVIOUS DAY',type=float,nargs='?',default=150)
    p.add_argument('AP',help='daily ap, 0-3hr, 3-6hr, 6-9hr, 9-12hr,12-33hr, 36-57hr',type=float,nargs='?',default=[4,4,4,4,4,4,4])
    p.add_argument('mass',help=('MASS NUMBER (ONLY DENSITY FOR SELECTED GAS IS ' +
                    'CALCULATED.  MASS 0 IS TEMPERATURE.  MASS 48 FOR ALL. '+
                    'MASS 17 IS Anomalous O ONLY.'),nargs='?',default=48)
    p = p.parse_args()

    inp = Series({'iyd':p.iyd, 'sec':p.utsec, 'glat':p.glat, 'glon':p.glon,
                  'f107a':p.F107a, 'f107':p.F107, 'mass':p.mass})

    altkm = arange(p.altkm[0],p.altkm[1],p.altkm[2])

    dens,temp = testgtd7(inp,p.AP,altkm)

    plotgtd(dens,temp)
    show()