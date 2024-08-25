from numba import jit
import numpy as np 
import matplotlib.pyplot as plt
import numpy.linalg as la
import scipy

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


@jit
def biot_savart(v1,v2,position,current): # input 2 points (line) and current
    r = position - (v1+v2)/2
    return np.cross(current*(v2-v1), r) * (10**-7) / (la.norm(r)**3) # biot savart equation

@jit
def solution(position=np.zeros(3),mradius=0,mheight=0,magnetization=0,accuracy=[70,30]): # position (v3d coordinates), magnet (radius, height, magnetization)
    v_steps,cir_steps = accuracy[0],accuracy[1]
    field = np.zeros(3)
    current = magnetization*mheight/v_steps
    cir_step = np.pi*2 / cir_steps

    circle = np.linspace(0,2*np.pi,cir_steps)
    
    for height in np.linspace(-(1/2)* mheight, (1/2) * mheight,v_steps):
        for rad in circle:
            field += biot_savart(np.array([np.cos(rad)*mradius,np.sin(rad)*mradius,height]),np.array([np.cos(rad+cir_step)*mradius,np.sin(rad+cir_step)*mradius,height]),position,current)
    
    return field * 1000 # v3d with magnitude being in tesla


distances = np.linspace(0.01,0.11,30)

field = np.array([])

for hfrom in distances:
    strength = solution(
            position=np.array([0,0,hfrom]),
            mradius=0.005,
            mheight=0.002,
            magnetization=1.1*(10**7),
            accuracy=[v_steps,cir_steps]
        )
    field = np.append(field,strength[2])
