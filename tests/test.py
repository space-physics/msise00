#!/usr/bin/env python
from numpy.testing import assert_allclose
from datetime import datetime
from pytz import UTC
from numpy import array
from numpy.testing import run_module_suite
#
from msise00.runmsis import rungtd1d

def test_gtd1d():
    t=datetime(2013,3,31,12,tzinfo=UTC)
    altkm=150.
    glat=65.; glon=-148.
    f107a=100; f107=100; ap=4; mass=48.
    tselecopts = array([1,1,1,1,1,1,1,1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],float)

    dens,temp = rungtd1d(t,altkm,glat,glon,f107a,f107,ap,mass,tselecopts)

    assert_allclose(dens.values[0,:-1],[1.19930062e+13, 1.25792119e+16, 2.92461331e+16,
                                 2.75184702e+15, 6.24779497e+13,1.84406768e-09,
                                 8.54530523e+11, 8.42101896e+12])
    assert (dens.species.values == ['He', 'O', 'N2', 'O2', 'Ar', 'Total', 'H', 'N', 'AnomalousO']).all()

    assert_allclose(temp.values[0,:],[ 848.71148682,  645.71972656])

if __name__ == '__main__':
    run_module_suite()
