"""
A generic, clean way to build C/C++/Fortran code from setup.py or manually

Michael Hirsch, Ph.D.
https://www.scivision.dev
"""
import shutil
from pathlib import Path
import subprocess
import os

R = Path(__file__).resolve().parents[1]
BINDIR = R / 'build'
SRCDIR = R / 'src'


def build():
    """
    attempts build with Meson or CMake
    """
    try:
        meson_setup()
    except (FileNotFoundError, RuntimeError):
        cmake_setup()


def cmake_setup():
    """
    attempt to build using CMake >= 3
    """
    cmake_exe = shutil.which('cmake')
    if not cmake_exe:
        raise FileNotFoundError('CMake not available')

    wopts = ['-G', 'MinGW Makefiles', '-DCMAKE_SH="CMAKE_SH-NOTFOUND'] if os.name == 'nt' else []

    subprocess.check_call([cmake_exe] + wopts + [str(SRCDIR)],
                          cwd=BINDIR)

    ret = subprocess.run([cmake_exe, '--build', str(BINDIR)],
                         stderr=subprocess.PIPE,
                         universal_newlines=True)

    result(ret)


def meson_setup():
    """
    attempt to build with Meson + Ninja
    """
    meson_exe = shutil.which('meson')
    ninja_exe = shutil.which('ninja')

    if not meson_exe or not ninja_exe:
        raise FileNotFoundError('Meson or Ninja not available')

    if not (BINDIR / 'build.ninja').is_file():
        subprocess.check_call([meson_exe, str(SRCDIR)], cwd=BINDIR)

    ret = subprocess.run(ninja_exe, cwd=BINDIR, stderr=subprocess.PIPE,
                         universal_newlines=True)

    result(ret)


def result(ret: subprocess.CompletedProcess):
    if not ret.returncode:
        print('\nBuild Complete!')
    else:
        raise RuntimeError(ret.stderr)
