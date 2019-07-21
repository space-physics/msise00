#!/usr/bin/env python
r"""
On Windows with Octave >= 5, you may need to add to PATH like:
    C:\Octave\Octave-5.1.0.0\mingw64\bin
to get at octave.exe instead of octave.vbs
"""
from pathlib import Path
import subprocess
import pytest
import shutil

R = Path(__file__).parent
Rcode = R.parent / 'matlab'

OCTAVE = shutil.which('octave-cli')
MATLAB = shutil.which('matlab')


@pytest.mark.skipif(not OCTAVE, reason="GNU Octave not available")
@pytest.mark.parametrize('build_sys', ['cmake', 'meson'])
def test_octave_build(build_sys, tmp_path):
    subprocess.check_call([OCTAVE, '--eval',
                           f"build('{build_sys}', '{R.parent}', '{tmp_path}')"],
                          cwd=Rcode, timeout=120)


@pytest.mark.skipif(not MATLAB, reason="Matlab not available")
@pytest.mark.parametrize('build_sys', ['cmake', 'meson'])
def test_matlab_build(build_sys, tmp_path):
    subprocess.check_call([MATLAB, '-batch',
                           f"build('{build_sys}', '{R.parent}', '{tmp_path}')"],
                          cwd=Rcode, timeout=120)


@pytest.mark.skipif(not MATLAB, reason="Matlab not available")
def test_matlab_api():
    subprocess.check_call([MATLAB, '-batch', 'runtests'],
                          cwd=R, timeout=60)


@pytest.mark.skipif(not OCTAVE, reason='octave not found')
def test_octave_api():
    subprocess.check_call([OCTAVE, 'test_mod.m'],
                          cwd=R, timeout=60)


if __name__ == '__main__':
    pytest.main(['-r', 'a', '-v', '-s', __file__])
