import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import math
import scipy
import bfield

v_steps = 30 # circles around the magnet
cir_steps = 200 # steps around the circle



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

distances = np.linspace(0.01,0.11,100)

field = np.array([])
for hfrom in distances:
    strength = bfield.solution(
            position=np.array([0,0,hfrom+0.002]),
            mradius=0.005,
            mheight=0.002,
            magnetization=1.1*(10**6),
            accuracy=[v_steps,cir_steps]
        )
    field = np.append(field,strength[2]*4500*hfrom**1.8)

plt.plot(distances*100,field*1000,label="Theoretical Model")

plt.errorbar(exp_distances,experimental,yerr=exp_error,fmt='o',label="Experimental Values")
plt.xlabel("Distance from Magnet (cm)")
plt.ylabel("Magnetic Field Strength (mT)")
plt.title("Numerical B-Field Solution")
plt.legend()
plt.show()
