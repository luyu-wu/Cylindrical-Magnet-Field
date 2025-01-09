import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import math
import scipy
import bfield

moment = 0.8


'''
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
'''
experimental = [
    175,
    110,
    62,
    50,
    40,
    34,
    25,
    22,
    20,
    19,
    18
]


exp_distances = np.linspace(0.5,3,len(experimental))

distances = np.linspace(0.001,0.10,200)

field = np.array([])
field_dipole = np.array([])
for hfrom in distances:
    position = np.array([0,0,hfrom])
    position_unit = np.array([1,0,0])
    strength = bfield.solution(
            position=position,
            mradius=0.01,
            mheight=0,
            moment=moment,
            accuracy=[1,40]
        )
    field = np.append(field,la.norm(strength))

    dipole = (1e-7/la.norm(position)**3) * (3*position_unit*(np.dot(np.array([0,0,moment]), position_unit))- np.array([0,0,moment]))
    field_dipole = np.append(field_dipole,la.norm(dipole))

plt.plot(distances*100,np.log10(field*1000),label="Current Cylinder Model")
plt.plot(distances*100,np.log10(field_dipole*1000),label="Dipole Model")

#plt.scatter(exp_distances,experimental,label="Experimental Values")
plt.xlabel("Distance from Magnet (cm)")
plt.ylabel("Log Magnetic Field $[log_{10}(mT)]$")
plt.title("Numerical B-Field Solution")
plt.legend()
plt.show()
