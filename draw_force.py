#!/usr/bin/env python


"""Statement
Attach one or two magnets to a non-magnetic and non-conductive base such that they attract a magnet suspended from a string. Investigate how the motion of the moving magnet depends on relevant parameters.
"""

import time

import bfield
import lorentz
import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as la

pi = np.pi
## Variables

print(
    "\n\033[1mWelcome to Magnetic Assist Force Solution\033[0m\nKindly wait while the simulation is run!\n"
)


drawOrientation = False
# Geometry
height = 0.06  # height of magnet above lower magnet in cm (lowest point)
length = 0.24  # length of string in cm
magnet_pos = np.array([0])
moment = 1
# swinging magnet stuff
magnet_radius = 0.00636
magnet_height = 0  # 0.00315
force_segmentations = 100
resolution = 120
theta_range = np.linspace(-0.4, 0.4, resolution)

# Integration step function

# Precompile
t0 = time.perf_counter()
print("Compiling B-Field..")
bfield.solution(
    position=np.array([0, 0, 0]), mradius=1, mheight=1, moment=1, accuracy=[1, 1]
)
print("Precompiled B-Field:", int(1e3 * (time.perf_counter() - t0)), "ms\n")
t0 = time.perf_counter()
if not drawOrientation:
    print("Compiling Lorentz..")
    lorentz.solution(
        position=np.array([0, 0, 0]), mradius=1, mheight=1, moment=1, accuracy=[1, 1]
    )
    print("Precompiled Lorentz:", int(1e3 * (time.perf_counter() - t0)), "ms\n")

solve_x = np.zeros(resolution)
solve_y = np.zeros(resolution)
solve_z = np.zeros(resolution)


t0 = time.perf_counter()
print("Calculating  ..")

for counter, theta in enumerate(theta_range):
    r_position = np.array(
        [np.sin(theta) * length, 0, length + height - np.cos(theta) * length]
    )  # relative positioning

    field = bfield.solution(
        position=r_position,
        mradius=magnet_radius,
        mheight=magnet_height,
        moment=moment,
        accuracy=[2, force_segmentations],
    )

    if drawOrientation:
        (solve_x[counter], solve_y[counter], solve_z[counter]) = field / la.norm(field)
    else:
        solution = lorentz.solution(
            position=r_position,
            orientation=field / la.norm(field),
            mradius=magnet_radius,
            mheight=0,
            moment=moment,
            accuracy=[2, force_segmentations],
        )
        (solve_x[counter], solve_y[counter], solve_z[counter]) = solution

print("Finished computing:", int(1e3 * (time.perf_counter() - t0)), "ms\n")


print("Drawing force graph...")
plt.xlabel("Theta (rads)")
if drawOrientation:
    plt.ylabel("Orientation")
else:
    plt.ylabel("Magnetic Force (N)")

plt.plot(theta_range, solve_x, label="X Vector")
plt.plot(theta_range, solve_y, label="Y Vector")
plt.plot(theta_range, solve_z, label="Z Vector")

plt.fill_between(theta_range, solve_x, 0, alpha=0.3, facecolor="#089FFF")
plt.fill_between(theta_range, solve_y, 0, alpha=0.3, facecolor="#FF8419")
plt.fill_between(theta_range, solve_z, 0, alpha=0.3, facecolor="#65BC85")


plt.legend()
plt.grid()
plt.show()
