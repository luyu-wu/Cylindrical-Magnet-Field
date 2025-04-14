import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as la
import bfield
from tqdm import tqdm

experimental = np.array([3450.5, 2332, 1603.5, 1012.5, 714, 552.5, 397.5, 307.5])

exp_error = np.array(
    [
        21.920310216783,
        36.7695526217005,
        2.12132034355964,
        3.53553390593274,
        14.142135623731,
        3.53553390593274,
        13.4350288425444,
        10.6066017177982,
    ]
)
exp_distances = np.linspace(0.02, 0.055, len(experimental))

least = 1e10
m_moment = 0
m_disp = 0
for moment in tqdm(np.linspace(0.975, 1, 30), desc="Minimizing moment"):
    for disp in np.linspace(0.0099, 0.01, 30):
        ls = 0
        for ind, hfrom in enumerate((exp_distances + disp)):
            position = np.array([0, 0, hfrom])
            strength = bfield.solution(
                position=position,
                mradius=0.00636,
                mheight=0.0063,
                moment=moment,
                accuracy=[10, 40],
            )
            ls += (experimental[ind] / 1000000 - la.norm(strength)) ** 2
        if ls < least:
            m_moment = moment
            m_disp = disp
            least = ls

print("minimum of moment:", m_moment, "displa:", m_disp)

exp_distances += m_disp
moment = m_moment

distances = np.linspace(exp_distances[0], exp_distances[-1], 100)

field = np.array([])
# field_dipole = np.array([])
for hfrom in distances:
    position = np.array([0, 0, hfrom])
    strength = bfield.solution(
        position=position,
        mradius=0.00636,
        mheight=0.0063,
        moment=moment,
        accuracy=[10, 40],
    )
    field = np.append(field, la.norm(strength))

    # dipole = (1e-7/la.norm(position)**3) * (3*position_unit*(np.dot(np.array([0,0,moment]), position_unit))- np.array([0,0,moment]))
    # field_dipole = np.append(field_dipole,la.norm(dipole))

plt.plot(distances * 100, field * 1000, label="Current Cylinder Model")
# plt.plot(distances*100,np.log10(field_dipole*1000),label="Dipole Model")
plt.errorbar(
    exp_distances * 100,
    experimental / 1000,
    yerr=exp_error / 1000,
    xerr=0.05,
    label="Experimental Values",
    capsize=4,
    fmt=".",
)

plt.xlabel("Distance from Magnet (cm)")
plt.ylabel("Magnetic Field $(mT)$")
plt.title("Numerical B-Field Solution")
plt.legend()
plt.show()
