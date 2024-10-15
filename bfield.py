#!/usr/bin/env python

'''
Written by Luyu as a general solution to a cylindrical magnet's b-field.
This solution uses a bound current line integral approximation, numerically integrated along the length of the cylinder to obtain a valid approximation of the B-field of the cylindrical ferromagnets at any point outside it.
'''

## MODULES
from numba import njit, prange
import numpy as np
# X AND Y ARE PLANAR DIRECTIONS, Z IS VERTICAL (i cant do y is vertical anymore these days)

@njit
def solution(position=np.ones(3),mradius=.0,mheight=.0,magnetization=.0,accuracy=np.ones(2)):
    field = np.zeros(3)
    point = np.linspace(0,2*np.pi,accuracy[1])
    
    for height in np.linspace(-mheight/2, mheight/2,accuracy[0]):
        for rad in prange(1,accuracy[1]):
            v1 = np.array([np.cos(point[rad-1])*mradius,np.sin(point[rad-1])*mradius,height])
            v2 = np.array([np.cos(point[ rad ])*mradius,np.sin(point[ rad ])*mradius,height])
            
            r = position - v1
            field += np.cross((v2-v1), r) / (np.linalg.norm(r)**3)

    return field * 2*np.pi*mradius * magnetization * 1e-7 / accuracy[0] # v3d with magnitude being in tesla
