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
Rcode = R.parents[2] / "matlab"

OCTAVE = shutil.which("octave-cli")
MATLAB = shutil.which("matlab")


@pytest.mark.skipif(not MATLAB, reason="Matlab not available")
def test_matlab_api():
    subprocess.check_call([MATLAB, "-batch", "test_mod"], cwd=Rcode, timeout=60)


@pytest.mark.skipif(not OCTAVE, reason="octave not found")
def test_octave_api():
    subprocess.check_call([OCTAVE, "test_mod.m"], cwd=Rcode, timeout=60)
