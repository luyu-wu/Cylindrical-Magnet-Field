import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import math
import scipy
from scipy.interpolate import make_interp_spline, BSpline
import bfield

v_steps = 1 # circles around the magnet
cir_steps = 4 # steps around the circle


distances = np.linspace(0,1,100)
field = np.array([])
for hfrom in distances:
    strength = bfield.solution(
            position=np.array([0,0,hfrom]),
            mradius=0.005,
            mheight=0,
            magnetization=8.2*(10**6),
            accuracy=[v_steps,cir_steps]
        )
    field = np.append(field,strength[2]/la.norm(strength))

plt.ylim(0,1)
plt.plot(distances*100,field,label="Z-Vector/Magnitude")

plt.fill_between(distances*100, field, 0,alpha=0.3, facecolor='#089FFF')

plt.xlim(0,100)
plt.xlabel("Distance from Magnet (cm)")
plt.ylabel("Vertical Uniformity (a.u.)")
plt.title("Numerical B-Field Solution")
plt.legend()
plt.show()
