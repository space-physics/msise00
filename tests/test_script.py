#!/usr/bin/env python
from pathlib import Path
import tempfile
import os
import subprocess
import pytest

CI = bool(os.environ['CI']) if 'CI' in os.environ else False
if not CI:
    import imageio
    from matplotlib.pyplot import figure, show


def test_blank():
    """current time, gridded over world, one altitude
       specified -gs 90 90 just to speed up on CI
    """
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(['msis00', '-o', str(d), '-gs', '90', '90'])
        olist = list(Path(d).glob('*.png'))
        fcount = len(olist)
        assert fcount == 1

        if not CI:
            for f in olist:
                ax = figure().gca()
                ax.imshow(imageio.imread(f))
                ax.axis('off')

            show()


def test_one_time():
    """ same as test_blank """
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(['msis00', '-o', str(d), '-gs', '90', '90',
                               '-t', '2017-03-21T12'])
        olist = list(Path(d).glob('*.png'))
        fcount = len(olist)
        assert fcount == 1

        if not CI:
            for f in olist:
                ax = figure().gca()
                ax.imshow(imageio.imread(f))
                ax.axis('off')

            show()


def test_one_alt():
    """ same as test_blank """
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(['msis00', '-o', str(d), '-gs', '90', '90',
                               '-a', '200'])
        olist = list(Path(d).glob('*.png'))
        fcount = len(olist)
        assert fcount == 1

        if not CI:
            for f in olist:
                ax = figure().gca()
                ax.imshow(imageio.imread(f))
                ax.axis('off')

            show()


def test_one_alt_one_time():
    """ same as test_blank """
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(['msis00', '-o', str(d), '-a', '200', '-t', '2017-03-01T12'])
        olist = list(Path(d).glob('*.png'))
        fcount = len(olist)
        assert fcount == 1

        if not CI:
            for f in olist:
                ax = figure().gca()
                ax.imshow(imageio.imread(f))
                ax.axis('off')

            show()


def test_time_range():
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(['msis00', '-o', str(d), '-gs', '90', '90',
                               '-t', '2017-03-01T12', '2017-03-01T14'])
        olist = sorted(Path(d).glob('*.png'))
        fcount = len(olist)
        assert fcount == 2

        if not CI:
            for f in olist:
                ax = figure().gca()
                ax.imshow(imageio.imread(f))
                ax.axis('off')

            show()


def test_one_loc():
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(['msis00', '-o', str(d),
                               '-c', '65', '-148'])
        olist = list(Path(d).glob('*.png'))
        fcount = len(olist)
        assert fcount == 0


def test_one_loc_one_time():
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(['msis00', '-o', str(d),
                               '-t', '2017-03-01T12', '-c', '65', '-148'])
        olist = list(Path(d).glob('*.png'))
        fcount = len(olist)
        assert fcount == 0


def test_one_alt_one_time_one_loc():
    with tempfile.TemporaryDirectory() as d:
        subprocess.check_call(['msis00', '-o', str(d),
                               '-a', '100', '-t', '2017-03-01T12', '-c', '65', '-148'])
        olist = list(Path(d).glob('*.png'))
        fcount = len(olist)
        assert fcount == 0


if __name__ == '__main__':
    pytest.main()
