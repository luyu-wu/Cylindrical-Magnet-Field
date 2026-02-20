import bfield
import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as la
from tqdm import tqdm

experimental = np.array(
    [
        41.43,
        39.4,
        36.83,
        33.45,
        30.0,
        25.4,
        22.73,
        19.63,
        16.87,
        14.57,
        12.9,
        11.0,
        9.95,
        8.9,
        7.9,
        6.85,
        6.1,
        5.35,
        4.6,
        4.15,
    ]
)

exp_error = np.array(
    [
        2.702,
        2.586,
        2.1,
        1.775,
        1.745,
        1.179,
        1.531,
        0.833,
        0.603,
        1.002,
        0.173,
        0.1,
        0.212,
        0.283,
        0.424,
        0.212,
        0.0,
        0.071,
        0.0,
        0.071,
    ]
)
exp_distances = np.linspace(0, 0.02, len(experimental))
least = 1e10
m_moment = 0
m_disp = 0
m_rad = 0
# minimum of moment: 0.7666666666666667 displa: 0.0074444444444444445 m_rad 0.010052631578947369

for moment in tqdm(np.linspace(0.75, 0.78, 10), desc="Minimizing moment"):
    for disp in np.linspace(0.006, 0.008, 10):
        for rad in np.linspace(0.0098,0.0105,20):
            ls = 0
            for ind, hfrom in enumerate((exp_distances + disp)):
                position = np.array([0, 0, hfrom])
                strength = bfield.solution(
                    position=position,
                    mradius=rad,
                    mheight=0.02,
                    moment=moment,
                    accuracy=[10, 40],
                )
                ls += (experimental[ind] / 1000 - la.norm(strength)) ** 2
            if ls < least:
                m_moment = moment
                m_disp = disp
                m_rad = rad
                least = ls

print("minimum of moment:", m_moment, "displa:", m_disp, "m_rad",m_rad)

exp_distances += m_disp

distances = np.linspace(exp_distances[0], exp_distances[-1], 30)

field = np.array([])
for hfrom in distances:
    position = np.array([0, 0, hfrom])
    strength = bfield.solution(
        position=position,
        mradius=m_rad,
        mheight=0.02,
        moment=m_moment,
        accuracy=[10, 40],
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
