import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import math
import scipy
from scipy.interpolate import make_interp_spline, BSpline
import threaded_bfield as bfield

v_steps = 100 # circles around the magnet
cir_steps = 50 # steps around the circle

'''
accuracies = np.linspace(5,100,5)
for acc in accuracies:
    v_steps = int(acc)
    
    distances = np.linspace(0,0.06,30)
    field = np.array([])
    for hfrom in distances:
        field = np.append(field,la.norm(bfield.solution(
            position=np.array([0,0,hfrom]),
            mradius=0.005,
            mheight=0.01,
            magnetization=4.2*(10**5),
            accuracy=[v_steps,cir_steps]
        )))

    xnew = np.linspace(distances.min(), distances.max(), 100)  
        
    spl = make_interp_spline(distances, field, k=3)
    power_smooth = spl(xnew)
    
    plt.plot(xnew*100,power_smooth*1000,label="Accuracy: "+str(v_steps)+" Circular Approximations")

plt.xlabel("Distance from Magnet (cm)")
plt.ylabel("Magnetic Field Strength (mT)")
plt.title("Numerical B-Field Solution")
plt.legend()
plt.show()
'''

accuracies = np.linspace(3,100,50)
fields = np.array([])
for acc in accuracies:
    cir_steps = int(acc)
    
    fields = np.append(fields,la.norm(bfield.solution(
            position=np.array([0,0,0]),
            mradius=0.005,
            mheight=0.01,
            magnetization=4.2*(10**5),
            accuracy=[v_steps,cir_steps]
        )))
    

plt.plot(accuracies,fields,label="Accuracy: "+str(cir_steps)+" Circular Approximations")

plt.xlabel("Accuracies (Vertical Approximations)")
plt.ylabel("Magnetic Field Strength (mT)")
plt.title("Numerical B-Field Solution")
plt.legend()
plt.show()
