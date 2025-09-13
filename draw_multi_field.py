#!/usr/bin/python

## MODULES
import numpy as np
import matplotlib.pyplot as plt
import bfield
from time import perf_counter

v_steps = 12  # circles around the magnet
cir_steps = 24  # steps around the circle

a = 0.02  # radius of the magnet in meters
b = 0.005  # length of the magnet in meters
m = 1  # magnetization in Am^2

magnet_pos = np.array([[0, -0.02], [0, 0.02]])
magnet_ori = np.array([1, -1])
grid = 100
grid_size = 0.064
x = np.linspace(-grid_size / 2, grid_size / 2, grid)
z = np.linspace(-grid_size / 2, grid_size / 2, grid)

X, Z = np.meshgrid(x, z)

Bx, Bz = np.meshgrid(np.zeros(grid), np.zeros(grid))

print("Solving Biot-Savart Array")
t1_start = perf_counter()

for mag_num, mpos in enumerate(magnet_pos):
    for i in range(grid):
        print(100 * ((mag_num / len(magnet_pos)) + (i / (grid * len(magnet_pos)))), "%")
        for y in range(grid):
            xd = magnet_ori[mag_num] * bfield.solution(
                np.array([x[i] - mpos[0], 0, z[y] - mpos[1]]),
                moment=m,
                mradius=a,
                mheight=b,
                accuracy=[v_steps, cir_steps],
            )
            Bx[y, i] += xd[0]
            Bz[y, i] += xd[2]

t1_stop = perf_counter()

print("Elapsed time:", (t1_stop - t1_start), "s")

B_mag = np.log10(np.sqrt(Bx**2 + Bz**2))

# Plot the results
fig, ax = plt.subplots(figsize=(10, 10))


# Plot the B-field
print("Rendering Stream Plot")
stream = ax.streamplot(
    X,
    Z,
    Bx,
    Bz,
    density=2,
    color=B_mag,
    cmap="viridis",
    linewidth=1,
    arrowsize=0.8,
    broken_streamlines=True,
)

# Plot the magnet
for magnet_p in magnet_pos:
    ax.add_patch(
        plt.Rectangle(
            (magnet_p[0] - a, magnet_p[1] - b / 2),
            2 * a,
            b,
            fill=True,
            facecolor="grey",
            edgecolor="black",
        )
    )

# Add colorbar
cbar = fig.colorbar(stream.lines)
cbar.set_label("Log Magnetic field strength (T)")

ax.set_xlabel("x (m)")
ax.set_ylabel("z (m)")
ax.set_title("B-field (log) Around a Cylindrical Magnet")
ax.set_aspect("equal")
ax.set_xlim(-grid_size / 2, grid_size / 2)
ax.set_ylim(-grid_size / 2, grid_size / 2)

# plt.tight_layout()
print("Finished")
plt.show()
