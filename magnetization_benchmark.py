import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import math
import scipy
from scipy.interpolate import make_interp_spline, BSpline
import bfield
import time

t0 = time.perf_counter()
v_steps = 200 # circles around the magnet
cir_steps = 60 # steps around the circle

experimental = [
234.5
,172.716666666667
,135.3
,99.525
,82
,60.32
,45.64
,36.5
,28.625
,23.35
,17.55
]
exp_error = [
    6.10327780786685
    ,11.296521096731
    ,5.48707572391707
    ,3.95750868602964
    ,4.80582979307424
    ,4.06024629794795
    ,0.909065454189081
    ,2.56645020732269
    ,1.98667435680838
    ,3.85519130524025
    ,0.824115687671741
    
]
exp_distances = np.linspace(1,11,11)

distances = np.linspace(0.01,0.11,30)

field = np.array([])
for hfrom in distances:
    strength = bfield.solution(
            position=np.array([0,0,hfrom]),
            mradius=0.005,
            mheight=0.002,
            magnetization=1.1*(10**7),
            accuracy=[v_steps,cir_steps]
        )
    field = np.append(field,strength[2])

print("Time Taken:",time.perf_counter()-t0,"s")
