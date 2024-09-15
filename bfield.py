#!/usr/bin/env python

'''
Written by Luyu as a general solution to a cylindrical magnet's b-field.
This solution uses a bound current line integral approximation
numerically integrated along the length of the cylinder to obtain a valid
approximation of the B-field of the cylindrical ferromagnets
at any point outside it.
'''

# MODULES
from numba import njit
import numpy as np
# X AND Y ARE PLANAR DIRECTIONS, Z IS VERTICAL


@njit
def solution(position=0, mradius=.0, mheight=.0, magnetization=.0, accuracy=[1, 20]):
    field = np.zeros(3)
    cirStep = np.pi*2 / accuracy[1]
    for height in np.linspace(-mheight/2, mheight/2, accuracy[0]):
        for rad in np.linspace(0,2*np.pi, accuracy[1]):
            v1 = np.array([np.cos(rad)*mradius, np.sin(rad)*mradius, height])
            v2 = np.array([np.cos(rad+cirStep)*mradius, np.sin(rad+cirStep)*mradius, height])
            r = position - (v1+v2)/2  # Displacement vector
            field += np.cross((v2-v1), r) / (np.linalg.norm(r)**3)
    return field * 2*np.pi*mradius * magnetization * 1e-7 / accuracy[0]
