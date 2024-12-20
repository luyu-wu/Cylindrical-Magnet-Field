import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import math
import scipy
import bfield

v_steps = 10 # circles around the magnet
cir_steps = 20 # steps around the circle
moment = 0.278


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
field_dipole = np.array([])
for hfrom in distances:
    position = np.array([0,0,hfrom])
    position_unit = np.array([0,0,1])
    strength = bfield.solution(
            position=position,
            mradius=0.005,
            mheight=0.002,
            moment=moment,
            accuracy=[v_steps,cir_steps]
        )
    field = np.append(field,la.norm(strength))

    dipole = (1e-7/la.norm(position)**3) * (3*position_unit*(np.dot(np.array([0,0,moment]), position_unit))- np.array([0,0,moment]))
    field_dipole = np.append(field_dipole,la.norm(dipole))

plt.plot(distances*100,field*1000,label="Current Cylinder Model")
plt.plot(distances*100,field_dipole*1000,label="Dipole Model")

plt.errorbar(exp_distances,experimental,yerr=exp_error,fmt='o',label="Experimental Values")
plt.xlabel("Distance from Magnet (cm)")
plt.ylabel("Magnetic Field Strength (mT)")
plt.title("Numerical B-Field Solution")
plt.legend()
plt.show()
