"""
A generic, clean way to build C/C++/Fortran code "build on run"

Michael Hirsch, Ph.D.
https://www.scivision.dev
"""
import shutil
from pathlib import Path
import subprocess
import typing
import sys
import argparse
import logging

R = Path(__file__).resolve().parent
SRCDIR = R
BINDIR = SRCDIR / "build"


def build(build_sys: str, src_dir: Path = SRCDIR, bin_dir: Path = BINDIR):
    """
    attempts build with Meson or CMake
    """
    if build_sys == "meson":
        meson_setup(src_dir, bin_dir)
    elif build_sys == "cmake":
        cmake_setup(src_dir)
    else:
        raise ValueError("Unknown build system {}".format(build_sys))


def cmake_setup(src_dir: Path):
    """
    attempt to build using CMake
    """
    exe = shutil.which("ctest")
    if not exe:
        raise FileNotFoundError("CMake not available")

    subprocess.check_call([exe, "-S", str(src_dir / "setup.cmake"), "-VV"])


def meson_setup(src_dir: Path, bin_dir: Path):
    """
    attempt to build with Meson + Ninja
    """
    args: typing.List[str] = []
    meson_exe = shutil.which("meson")
    if not meson_exe:
        raise FileNotFoundError("Meson not available")

    if (bin_dir / "build.ninja").is_file():
        args += ["--wipe"]

    cmd = [meson_exe, "setup", str(bin_dir), str(src_dir)] + args
    logging.debug(cmd)
    subprocess.check_call(cmd)

    subprocess.check_call([meson_exe, "test", "-C", str(bin_dir)])


def get_libpath(bin_dir: Path, stem: str) -> Path:
    if sys.platform in ("win32", "cygwin"):
        dllfn = bin_dir / ("lib" + stem + ".dll")
    elif sys.platform == "linux":
        dllfn = bin_dir / ("lib" + stem + ".so")
    elif sys.platform == "darwin":
        dllfn = bin_dir / ("lib" + stem + ".dylib")

    if not dllfn.is_file():
        dllfn = None

    return dllfn


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("buildsys", choices=["meson", "cmake"])
    P = p.parse_args()

    build(P.buildsys)
