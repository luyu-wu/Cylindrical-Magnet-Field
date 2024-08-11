## MODULES
import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import threaded_bfield as bfield
#import bfield as bfield
import math
import scipy
from time import perf_counter

v_steps = 80 # circles around the magnet
cir_steps = 60 # steps around the circle

a = 0.005  # radius of the magnet in meters
b = 0.001  # half-length of the magnet in meters
M = 1e5  # magnetization in A/m

grid = 80
x = np.linspace(-0.02, 0.02, grid)
z = np.linspace(-0.02, 0.02, grid)

X, Z = np.meshgrid(x, z)

Bx,Bz = np.meshgrid(np.zeros(grid),np.zeros(grid))

print("Solving Biot-Savart Array")
t1_start = perf_counter() 

for i in range(grid):
    print(100*i/grid,"% Completion")
    for y in range(grid):
        xd = 1000*bfield.solution(np.array([x[i],0,z[y]]),magnetization=M,mradius=a,mheight=b*2,accuracy=[v_steps,cir_steps])
        Bx[i,y],Bz[y,i] = xd[0],xd[2]

t1_stop = perf_counter()
 
print("Elapsed time:", (t1_stop-t1_start),"s")

B_mag = np.log(np.sqrt(Bx**2 + Bz**2))

# Plot the results
fig, ax = plt.subplots(figsize=(10, 10))


# Plot the B-field
print("Rendering Stream Plot")
stream = ax.streamplot(X, Z, Bx, Bz, density=10, color=B_mag, cmap='viridis', 
                       linewidth=1, arrowsize=1, norm=plt.Normalize(vmin=0, vmax=B_mag.max(),),broken_streamlines=True)

# Plot the magnet
ax.add_patch(plt.Rectangle((-a, -b), 2*a, 2*b, fill=True, facecolor='grey', edgecolor='black'))

# Add colorbar
cbar = fig.colorbar(stream.lines)
cbar.set_label('Log Magnetic field strength (mT)')

ax.set_xlabel('x (m)')
ax.set_ylabel('z (m)')
ax.set_title('B-field (log) Around a Cylindrical Magnet')
ax.set_aspect('equal')
ax.set_xlim(-0.02, 0.02)
ax.set_ylim(-0.02, 0.02)

#plt.tight_layout()
print("Finished")
plt.show()