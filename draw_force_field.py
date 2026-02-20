## MODULES
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as la
from tqdm import tqdm

import bfield
import lorentz

v_steps = 16  # circles around the magnet
cir_steps = 16  # steps around the circle

orient_magnet = False

a = 0.00636  # radius of the magnet in meters
b = 0.00315  # length of the magnet in meters
m = 0.276  # moment in Am**2

grid = 100
grid_size = 0.15
x = np.linspace(-grid_size / 2, grid_size / 2, grid)
z = np.linspace(-grid_size / 2, grid_size / 2, grid)

X, Z = np.meshgrid(x, z)
Fx, Fz = np.meshgrid(np.zeros(grid), np.zeros(grid))

Bx, Bz = np.meshgrid(np.zeros(grid), np.zeros(grid))

print("Solving Lorentz Array")
t1_start = perf_counter()

for i in tqdm(range(grid)):
    for y in range(grid):
        rent = np.array([0, 0, 1])
        position = np.array([x[i], 0, z[y]])

        field = bfield.solution(
            position=position,
            mradius=a,
            mheight=b,
            moment=m,
            accuracy=[v_steps, cir_steps],
        )
        field /= la.norm(field)
        Bx[y, i], Bz[y, i] = field[0], field[2]
        if not orient_magnet:
            field = np.array([0, 0, 1])
        xd = lorentz.solution(
            position,
            moment=m,
            mradius=a,
            mheight=b,
            accuracy=[v_steps, cir_steps],
            orientation=field,
        )
        Fx[y, i], Fz[y, i] = xd[0], xd[2]

t1_stop = perf_counter()

print("Elapsed time:", (t1_stop - t1_start), "s")

F_mag = np.log10(np.sqrt(Fx**2 + Fz**2))
# Plot the results
fig, ax = plt.subplots(figsize=(10, 10))


# Plot the B-field
print("Rendering Stream Plot")


stream = ax.streamplot(
    X,
    Z,
    Fx,
    Fz,
    density=3,
    color=F_mag,
    cmap="viridis",
    linewidth=1,
    arrowsize=1,
    broken_streamlines=True,
)


# Plot the magnet
ax.add_patch(
    plt.Rectangle(
        (-a, -0.0025), 2 * a, 0.005, fill=True, facecolor="grey", edgecolor="black"
    )
)

# Add colorbar
cbar = fig.colorbar(stream.lines)
cbar.set_label("Magnetic Force ($log_{10}(N)$)")

ax.set_xlabel("x (m)")
ax.set_ylabel("z (m)")
ax.set_title("Force on Cylindrical Magnet around a Cylindrical Magnet")
ax.set_aspect("equal")
ax.set_xlim(-grid_size / 2, grid_size / 2)
ax.set_ylim(-grid_size / 2, grid_size / 2)

# plt.tight_layout()
print("Finished")
plt.show()
