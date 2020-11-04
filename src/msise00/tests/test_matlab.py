from pathlib import Path
import subprocess
import pytest
import shutil

R = Path(__file__).parent
Rcode = R.parents[2]

MATLAB = shutil.which("matlab")


@pytest.mark.skipif(not MATLAB, reason="Matlab not available")
def test_matlab_api():
    subprocess.check_call([MATLAB, "-batch", "assertSuccess(runtests('msise00'))"], cwd=Rcode, timeout=60)
