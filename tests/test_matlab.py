#!/usr/bin/env python
from pathlib import Path
import subprocess
import pytest
import shutil

R = Path(__file__).parent


@pytest.mark.skipif(not bool(shutil.which('matlab')), reason="Matlab not available")
def test_matlab_api():
    subprocess.check_call(['matlab', '-nojvm', '-r',
                           'r=runtests(); exit(any([r.Failed]))'],
                          cwd=R, timeout=60)


if __name__ == '__main__':
    pytest.main(['-xrsv', __file__])
