#!/usr/bin/env python


import ctypes
import os

import numpy as np
_lib = ctypes.CDLL(os.path.abspath("./liblorentz.so"))

_lib.lorentz_force.argtypes = [
    ctypes.POINTER(ctypes.c_double),  # position[3]
    ctypes.POINTER(ctypes.c_double),  # orientation[3]
    ctypes.c_double,  # mradius
    ctypes.c_double,  # mheight
    ctypes.c_double,  # moment
    ctypes.c_double,  # moment2
    ctypes.c_double,  # mradius2
    ctypes.c_int,  # h_acc
    ctypes.c_int,  # r_acc
    ctypes.POINTER(ctypes.c_double),  # out[3]
]
_lib.lorentz_force.restype = None


def solution(
    position=np.array([0.0, 0.0, 1.0]),
    orientation=np.array([0.0, 0.0, 1.0]),
    mradius=0.005,
    mheight=0.003,
    moment=1.0,
    moment2=None,
    mradius2=None,
    accuracy=(2, 100),
):
    if moment2 is None:
        moment2 = moment
    if mradius2 is None:
        mradius2 = mradius

    position = np.asarray(position, dtype=np.float64)
    orientation = np.asarray(orientation, dtype=np.float64)
    orientation = orientation / np.linalg.norm(orientation)

    h_acc, r_acc = int(accuracy[0]), int(accuracy[1])

    out = np.zeros(3, dtype=np.float64)

    _lib.lorentz_force(
        position.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        orientation.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        float(mradius),
        float(mheight),
        float(moment),
        float(moment2),
        float(mradius2),
        h_acc,
        r_acc,
        out.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
    )
    return out
