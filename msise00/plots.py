from pathlib import Path
from pytz import UTC
from numpy import atleast_1d
from datetime import datetime
from astropy.time import Time
from astropy.coordinates import get_sun,EarthLocation, AltAz
from matplotlib.pyplot import figure,subplots, close
from matplotlib.ticker import ScalarFormatter
#
from pymap3d import aer2geodetic

def plotgtd(dens,temp,dtime,altkm, ap, f107,glat,glon,rodir=None):
#
    if rodir:
        rodir = Path(rodir).expanduser()

    dtime = atleast_1d(dtime)
    sfmt = ScalarFormatter(useMathText=True) #for 10^3 instead of 1e3
    sfmt.set_powerlimits((-2, 2))
    sfmt.set_scientific(True)
    sfmt.set_useOffset(False)

    if dens.ndim==2: #altitude 1-D
        plot1d(dens,temp,glat,glon,ap,f107)
    elif dens.ndim==4: #lat/lon grid
#%% sun lat/lon
        ttime = Time(dtime)
        obs = EarthLocation(0,0) # geodetic lat,lon = 0,0 arbitrary
        sun = get_sun(time=ttime)
        aaf = AltAz(obstime=ttime,location=obs)
        sloc = sun.transform_to(aaf)
        slat,slon = aer2geodetic(sloc.az.value, sloc.alt.value, sloc.distance.value,0,0,0)[:2]
#%%
        #iterate over time
        for k,d in enumerate(dens): #dens is a 4-D array  time x species x lat x lon
            fg,ax = subplots(4,2,sharex=True, figsize=(8,8))
            fg.suptitle(datetime.fromtimestamp(d.time.item()/1e9, tz=UTC).strftime('%Y-%m-%dT%H:%M') +
                        f' alt.(km) {altkm}\nAp={ap[0]}  F10.7={f107}')
            ax=ax.ravel(); i = 0 #don't use enumerate b/c of skip

            #iterate over species
            for s in d:
                thisspecies = s.species.values
                if thisspecies != 'Total':
                    a = ax[i]

                    hi = a.imshow(s.values, aspect='auto', interpolation='none',cmap='viridis',
                             extent=(glon[0,0],glon[0,-1],glat[0,0],glat[-1,0]))
                    fg.colorbar(hi,ax=a, format=sfmt)

                    a.plot(slon[k],slat[k],linestyle='none',
                                        marker='o',markersize=5,color='w')

                    a.set_title(f'Density: {thisspecies}')
                    a.set_xlim(-180,180)
                    a.set_ylim(-90,90)
                    a.autoscale(False)
                    i+=1
            for i in range(0,6+2,2):
                ax[i].set_ylabel('latitude (deg)')
            for i in (6,7):
                ax[i].set_xlabel('longitude (deg)')

            if rodir:
                thisofn = rodir / '{:.1f}_{:03d}.png'.format(altkm[0],k)
                print(f'writing {thisofn}')
                fg.savefig(str(thisofn),dpi=100,bbox_inches='tight')
                close()
    else:
        print(f'densities  {dens}')
        print(f'temperatures {temp}')

def plot1d(dens,temp,glat,glon,ap,f107):
    ap = atleast_1d(ap)
    footer = '\n({},{})  Ap {}  F10.7 {}'.format(glat,glon,ap[0],f107)

    z=dens.altkm.values
    ax = figure().gca()
    for s in dens.T:
        thisspecies = s.species.values
        if thisspecies != 'Total':
            ax.semilogx(s, z, label=thisspecies)
    ax.legend(loc='best')
    ax.set_xlim(left=1e3)
    ax.set_ylabel('altitude [km]')
    ax.set_xlabel('density [m$^{-3}$]')
    ax.grid(True)
    ax.set_title('Number Density from MSISE-00' + footer)

    ax = figure().gca()
    ax.semilogx(dens.loc[:,'Total'], z)
    ax.set_xlabel('Total Mass Density [kg m$^{-3}$]')
    ax.set_ylabel('altitude [km]')
    ax.grid(True)
    ax.set_title('Total Mass Density from MSISE-00'+footer)

    ax = figure().gca()
    ax.plot(temp.loc[:,'Tn'], z)
    ax.set_xlabel('Temperature')
    ax.set_ylabel('altitude [km]')
    ax.grid(True)
    ax.set_title('Temperature from MSISE-00' + footer)
