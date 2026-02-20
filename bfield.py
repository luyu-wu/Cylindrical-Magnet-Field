import ctypes
import os

import numpy as np

_lib = ctypes.CDLL(os.path.abspath("./libbfield.so"))
_lib.bfield.argtypes = [
    ctypes.c_double,  # px
    ctypes.c_double,  # py
    ctypes.c_double,  # pz
    ctypes.c_double,  # mradius
    ctypes.c_double,  # mheight
    ctypes.c_double,  # moment
    ctypes.c_int,  # h_acc
    ctypes.c_int,  # r_acc
    ctypes.POINTER(ctypes.c_double),  # output array
]
_lib.bfield.restype = None


def solution(
    position=np.array([0.0, 0.0, 0.01]),
    mradius=0.005,
    mheight=0.003,
    moment=1.0,
    accuracy=(100, 200),
):
    """
    Fast shared-library magnetic field computation.
    """

    px, py, pz = map(float, position)
    h_acc, r_acc = accuracy

    out = np.zeros(3, dtype=np.float64)

    _lib.bfield(
        px,
        py,
        pz,
        mradius,
        mheight,
        moment,
        int(h_acc),
        int(r_acc),
        out.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
    )

    return out
