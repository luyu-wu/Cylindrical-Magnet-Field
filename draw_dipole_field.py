#!/usr/bin/python

## MODULES
import numpy as np 
import matplotlib.pyplot as plt
from numpy import linalg as la
import bfield
import math
import scipy
from time import perf_counter

magnet_pos = np.array([[0,0]])
magnet_ori = np.array([1])
grid = 100
grid_size = 0.2
x = np.linspace(-grid_size/2, grid_size/2, grid)
z = np.linspace(-grid_size/2, grid_size/2, grid)

X, Z = np.meshgrid(x, z)

Bx,Bz = np.meshgrid(np.zeros(grid),np.zeros(grid))


for (mag_num,mpos) in enumerate(magnet_pos):
    for i in range(grid):
        for y in range(grid):
            position = np.array([x[i]-mpos[0],0,z[y]])
            position_unit = position/la.norm(position)
            xd = (1e-7/la.norm(position)**3) * (3*position_unit*(np.dot(np.array([0,0,1]), position_unit))- np.array([0,0,1]))
            Bx[y,i] += xd[0]
            Bz[y,i] += xd[2]

t1_stop = perf_counter()
 

B_mag = np.log(np.sqrt(Bx**2 + Bz**2))

# Plot the results
fig, ax = plt.subplots(figsize=(10, 10))


# Plot the B-field
print("Rendering Stream Plot")
stream = ax.streamplot(X, Z, Bx, Bz, density=2, color=B_mag, cmap='viridis', 
                       linewidth=1, arrowsize=0.8, broken_streamlines=True)

# Add colorbar
cbar = fig.colorbar(stream.lines)
cbar.set_label('Log Magnetic field strength (T)')

ax.set_xlabel('x (m)')
ax.set_ylabel('z (m)')
ax.set_title('B-field (log) Around a Cylindrical Magnet')
ax.set_aspect('equal')
ax.set_xlim(-grid_size/2, grid_size/2)
ax.set_ylim(-grid_size/2, grid_size/2)

#plt.tight_layout()
print("Finished")
plt.show()
