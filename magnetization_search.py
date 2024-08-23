import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import math
import scipy
from scipy.interpolate import make_interp_spline, BSpline
import threaded_bfield as bfield

v_steps = 25 # circles around the magnet
cir_steps = 100 # steps around the circle


distances = np.linspace(0.01,0.12,30)
field = np.array([])
for hfrom in distances:
    strength = bfield.solution(
            position=np.array([0,0,hfrom]),
            mradius=0.005,
            mheight=0.002,
            magnetization=8.2*(10**6),
            accuracy=[v_steps,cir_steps]
        )
    field = np.append(field,strength[2]/la.norm(strength))

plt.plot(distances*100,field,label="Field (mT) vs. Distance (cm)")

plt.xlabel("Distance from Magnet (cm)")
plt.ylabel("Magnetic Field Strength (mT)")
plt.title("Numerical B-Field Solution")
plt.legend()
plt.show()
