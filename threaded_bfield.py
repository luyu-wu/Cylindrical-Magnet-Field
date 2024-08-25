#!/usr/bin/env python

'''
Written by Luyu as a general solution to a cylindrical magnet's b-field.
This solution uses a bound current line integral approximation, numerically integrated along the length of the cylinder to obtain a valid approximation of the B-field of the cylindrical ferromagnets at any point outside it.
'''

## MODULES
import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import multiprocessing as mp
import math
import scipy

# X AND Y ARE PLANAR DIRECTIONS, Z IS VERTICAL (i cant do y is vertical anymore these days)
threads = mp.cpu_count()

current = 0
cir_step = 0
circle = 0
v_steps = 0
cir_steps = 0
g_mradius = 0
g_mheight = 0
g_position = 0

def worker(chunk):
    re_var = np.zeros(3)
    for height in chunk: #[int(v_steps*(thread_num/threads)):int(v_steps*((thread_num+1)/threads))-1]: # split into threads
        for rad in circle:
            v1,v2 = np.array([np.cos(rad)*g_mradius,np.sin(rad)*g_mradius,height]),np.array([np.cos(rad+cir_step)*g_mradius,np.sin(rad+cir_step)*g_mradius,height])
                        
            r = g_position - (v1+v2)/2
            re_var += np.cross(current*(v2-v1), r) * (10**-7) / (la.norm(r)**3)
    return re_var

def solution(position=np.zeros(3),mradius=0,mheight=0,magnetization=0,accuracy=[70,30]): # position (v3d coordinates), magnet (radius, height, magnetization)
    global current,cir_step,circle,v_steps,cir_steps,circle,g_mradius,g_mheight, g_position
    g_mradius,g_mheight,g_position = mradius, mheight, position
    v_steps,cir_steps = accuracy[0],accuracy[1]
    current = magnetization*mheight/v_steps
    cir_step = np.pi*2 / cir_steps
    circle = np.linspace(0,2*np.pi,cir_steps)

    pool = mp.Pool(processes=threads)

    arr = np.linspace(-(1/2)* mheight, (1/2) * mheight,v_steps)
    
    chunk_size = int(arr.shape[0] / threads) 
    if chunk_size == 0:
        chunk_size = 1
    chunks = [arr[i:i + chunk_size] for i in range(0, arr.shape[0], chunk_size)] 
    
    return np.sum(pool.map(worker,chunks),axis=0) # v3d with magnitude being in tesla
