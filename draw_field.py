## MODULES
import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import bfield
import math
import scipy
from time import perf_counter

v_steps = 1 # circles around the magnet
cir_steps = 10 # steps around the circle

a = 0.00636  # radius of the magnet in meters
b = 1e-9  # length of the magnet in meters
M = 1e5  # magnetization in A/m

grid = 100
grid_size = 0.1
angle = np.pi
x = np.linspace(-grid_size/2, grid_size/2, grid)
z = np.linspace(-grid_size/2, grid_size/2, grid)

X, Z = np.meshgrid(x, z)

Bx,Bz = np.meshgrid(np.zeros(grid),np.zeros(grid))

print("Solving Biot-Savart Array")
t1_start = perf_counter() 

for i in range(grid):
    print(100*i/grid,"% Completion")
    for y in range(grid):
        xd = 1000*bfield.solution(np.array([x[i]*np.cos(angle),x[i]*np.sin(angle),z[y]]),magnetization=M,mradius=a,mheight=b,accuracy=[v_steps,cir_steps])
        Bx[y,i],Bz[y,i] = np.cos(angle)*xd[0] + np.sin(angle)*xd[1],xd[2]

t1_stop = perf_counter()
 
print("Elapsed time:", (t1_stop-t1_start),"s")

B_mag = np.log(np.sqrt(Bx**2 + Bz**2))

# Plot the results
fig, ax = plt.subplots(figsize=(10, 10))


# Plot the B-field
print("Rendering Stream Plot")
stream = ax.streamplot(X, Z, Bx, Bz, density=3, color=B_mag, cmap='viridis', 
                       linewidth=1, arrowsize=0, norm=plt.Normalize(vmin=0, vmax=B_mag.max(),),broken_streamlines=True)

# Plot the magnet
ax.add_patch(plt.Rectangle((-a, -b/2), 2*a, b, fill=True, facecolor='grey', edgecolor='black'))

# Add colorbar
cbar = fig.colorbar(stream.lines)
cbar.set_label('Log Magnetic field strength (mT)')

ax.set_xlabel('x (m)')
ax.set_ylabel('z (m)')
ax.set_title('B-field (log) Around a Cylindrical Magnet')
ax.set_aspect('equal')
ax.set_xlim(-grid_size/2, grid_size/2)
ax.set_ylim(-grid_size/2, grid_size/2)

#plt.tight_layout()
print("Finished")
plt.show()
