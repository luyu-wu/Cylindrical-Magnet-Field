## MODULES
import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import bfield
import math
import scipy
from time import perf_counter

v_steps = 10 # circles around the magnet
cir_steps = 20 # steps around the circle

a = 0.00636  # radius of the magnet in meters
b = 0.0063  # length of the magnet in meters
m = 0.564

grid = 100
grid_size = 0.1
x = np.linspace(-grid_size/2, grid_size/2, grid)
z = np.linspace(-grid_size/2, grid_size/2, grid)

X, Z = np.meshgrid(x, z)

Bx,Bz = np.meshgrid(np.zeros(grid),np.zeros(grid))

print("Solving Biot-Savart Array")
t1_start = perf_counter() 

for i in range(grid):
    print(100*i/grid,"% Completion")
    for y in range(grid):
        xd = bfield.solution(np.array([x[i],0,z[y]]),mradius=a,mheight=b,accuracy=[v_steps,cir_steps],moment=m)
        Bx[y,i],Bz[y,i] = xd[0],xd[2]

t1_stop = perf_counter()
 
print("Elapsed time:", (t1_stop-t1_start),"s")

B_mag = np.log10(np.sqrt(Bx**2 + Bz**2))

# Plot the results
fig, ax = plt.subplots(figsize=(10, 10))


# Plot the B-field
print("Rendering Stream Plot")
stream = ax.streamplot(X, Z, Bx, Bz, density=2, color=B_mag, cmap='viridis', 
                       linewidth=1, arrowsize=0.8, broken_streamlines=True)

# Plot the magnet
ax.add_patch(plt.Rectangle((-a, -b/2), 2*a, b, fill=True, facecolor='grey', edgecolor='black'))

# Add colorbar
cbar = fig.colorbar(stream.lines)
cbar.set_label('Magnetic field strength ($log_{10}[T]$)')

ax.set_xlabel('x (m)')
ax.set_ylabel('z (m)')
ax.set_title('B-field ($log_{10}$) Around a Cylindrical Magnet')
ax.set_aspect('equal')
ax.set_xlim(-grid_size/2, grid_size/2)
ax.set_ylim(-grid_size/2, grid_size/2)

#plt.tight_layout()
print("Finished")
plt.show()
