#!/usr/bin/env python

"""
This solution uses a bound current line integral approximation, numerically integrated along the length of the cylinder to obtain a valid approximation of the B-field of the cylindrical ferromagnets at any point outside it.
"""

## MODULES
import numpy as np
from numba import njit, prange

# X AND Y ARE PLANAR DIRECTIONS, Z IS VERTICAL


@njit(cache=True)
def solution(
    position=np.array([0, 0, 1]),
    mradius=0.005,
    mheight=0.003,
    moment=1.0,
    accuracy=[10, 2],
):
    field = np.zeros(3)
    point = np.linspace(0, 2 * np.pi, accuracy[1])

    for h in np.linspace(-mheight / 2, mheight / 2, accuracy[0]):
        for rad in prange(1, accuracy[1]):
            v1 = np.array(
                [np.cos(point[rad - 1]) * mradius, np.sin(point[rad - 1]) * mradius, h]
            )
            v2 = np.array(
                [np.cos(point[rad]) * mradius, np.sin(point[rad]) * mradius, h]
            )

            r = position - (v1 + v2) / 2
            field += np.cross((v2 - v1), r) / (np.linalg.norm(r) ** 3)

    return (field * moment) / (accuracy[0] * 2 * np.pi * (mradius**2) * 1e7)


import ctypes
import os

import numpy as np

# Load shared library
_lib = ctypes.CDLL(os.path.abspath("./libbfield.so"))

# Define argument types
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


def bfield_compiled(
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
