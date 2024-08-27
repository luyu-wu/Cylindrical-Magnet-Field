#!/usr/bin/env python

'''
Written by Luyu as a general solution to a cylindrical magnet's b-field.
This solution uses a bound current line integral approximation, numerically integrated along the length of the cylinder to obtain a valid approximation of the B-field of the cylindrical ferromagnets at any point outside it.
'''

## MODULES
from numba import jit
import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import scipy


# X AND Y ARE PLANAR DIRECTIONS, Z IS VERTICAL (i cant do y is vertical anymore these days)

@jit
def solution(position=np.zeros(3),mradius=0,mheight=0,magnetization=0,accuracy=[70,30]): # position (v3d coordinates), magnet (radius, height, magnetization)
    v_steps,cir_steps = accuracy[0],accuracy[1]
    field = np.zeros(3)
    current = magnetization*mheight/v_steps
    cir_step = np.pi*2 / cir_steps

    circle = np.linspace(0,2*np.pi,cir_steps)
    
    for height in np.linspace(-(1/2)* mheight, (1/2) * mheight,v_steps):
        for rad in circle:
            v1,v2 = np.array([np.cos(rad)*mradius,np.sin(rad)*mradius,height]),np.array([np.cos(rad+cir_step)*mradius,np.sin(rad+cir_step)*mradius,height])
            
            r = position - (v1+v2)/2
            field += np.cross(current*(v2-v1), r) * (10**-7) / (la.norm(r)**3)
                        
    return field # v3d with magnitude being in tesla

