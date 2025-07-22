import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as la
from scipy import optimize

import bfield

experimental = np.array(
    [
        19.55,
        16.8,
        15.35,
        13.85,
        12.7,
        11.15,
        10.3,
        9.7,
        8.55,
        7.7,
        6.7,
        5.7,
        5.2,
        4.4,
        3.9,
        3.5,
        3.1,
        2.75,
        2.5,
        2.35,
        2.25,
        1.05,
        0.6,
    ]
)

exp_error = np.array(
    [
        0.4949747468,
        0.2828427125,
        0.2121320344,
        0.3535533906,
        0.5656854249,
        0.07071067812,
        0.1414213562,
        0.1414213562,
        0.2121320344,
        0.2828427125,
        0.1414213562,
        0.2828427125,
        0.1414213562,
        0.1414213562,
        0.1414213562,
        0.1414213562,
        0.1414213562,
        0.07071067812,
        0.1414213562,
        0.07071067812,
        0.07071067812,
        0.07071067812,
        0.0,
    ]
)
exp_distances = (
    np.array(
        [
            0.0,
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
            0.6,
            0.7,
            0.8,
            0.9,
            1.0,
            1.1,
            1.2,
            1.3,
            1.4,
            1.5,
            1.6,
            1.7,
            1.8,
            1.9,
            2.0,
            3.0,
            4.0,
        ]
    )
    / 100
)


def objective(params):
    moment, rad, disp = params
    ls = 0
    for ind, hfrom in enumerate(exp_distances + disp):
        position = np.array([0, 0, hfrom])
        strength = bfield.solution(
            position=position,
            mradius=rad,
            mheight=0,
            moment=float(moment),
            accuracy=[1, 8],
        )
        strength *= 1000
        ls += (experimental[ind] - la.norm(strength)) ** 2
    return ls


initial_guess = [1.85, 0.0045, 0.025]
bounds = ((1, 4.0), (0.001, 0.005), (0.01, 0.04))
result = optimize.minimize(objective, initial_guess, bounds=bounds, method="L-BFGS-B")

m_moment, m_rad, m_disp = result.x
print("minimum of moment:", m_moment, "m_rad", m_rad, "m_disp", m_disp)

exp_distances += m_disp
distances = np.linspace(exp_distances[0], exp_distances[-1], 30)

field = np.array([])
for hfrom in distances:
    position = np.array([0, 0, hfrom])
    strength = bfield.solution(
        position=position,
        mradius=m_rad,
        mheight=0,
        moment=float(m_moment),
        accuracy=[1, 8],
    )
    field = np.append(field, la.norm(strength) * 1000)

plt.plot(distances * 100, field, label="Current Cylinder")
plt.errorbar(
    exp_distances * 100,
    experimental,
    yerr=exp_error,
    xerr=0.025,
    label="Experimental Data",
    capsize=4,
    fmt=".",
)

plt.xlabel("Distance from Magnet (cm)")
plt.ylabel("Magnetic Field $(mT)$")
plt.title("Numerical B-Field Solution")
plt.legend()
plt.show()
