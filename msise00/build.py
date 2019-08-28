#!/usr/bin/env python3
import subprocess
import shutil
from pathlib import Path
from typing import List

R = Path(__file__).parent
RS = R / "fortran"

SOURCES = list(map(str, [RS / "nrlmsise00_sub.for", RS / "msise00_driver.f90"]))
EXE = R / "msise00_driver"
EXE_OPT = ["-o", str(EXE)]


def build(sources: List[str] = SOURCES, compiler: str = "gfortran", exe_opt: List[str] = EXE_OPT) -> str:
    """
    Attempt to compile code instead of using setup.py
    """
    if isinstance(sources, (str, Path)):
        sources = [sources]

    fc = shutil.which(compiler)
    if not fc:
        raise FileNotFoundError(fc)

    for s in SOURCES:
        if not Path(s).is_file():
            raise FileNotFoundError(s)

    sources = list(map(str, sources))

    subprocess.check_call([str(fc)] + sources + EXE_OPT)

    return shutil.which(EXE.name, path=str(R))


if __name__ == "__main__":
    exe = build()
    print("compiled", exe)
