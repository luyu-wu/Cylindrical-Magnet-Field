import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import linalg as la
import threaded_bfield as bfield

size = 10  # Grid size

# Reference value calculation
reference = la.norm(bfield.solution(
    position=np.array([0, 0, 0]),
    mradius=0.005,
    mheight=0.002,
    magnetization=4.2e5,
    accuracy=[200, 200]
))
print("Found reference")

# Define accuracy ranges
accuracies_v = np.linspace(1, 50, size)
accuracies_c = np.linspace(1, 50, size)
relative_acc = np.zeros((size, size), dtype=float)

# Calculate relative accuracy for different accuracies
for v_s in range(size):
    v_steps = int(accuracies_v[v_s])

    for c_s in range(size):
        cir_steps = int(accuracies_c[c_s])
        current_solution = la.norm(bfield.solution(
            position=np.array([0, 0, 0]),
            mradius=0.005,
            mheight=0.002,
            magnetization=4.2e5,
            accuracy=[v_steps, cir_steps]
        ))
        relative_acc[v_s, c_s] = 100 * abs((reference - current_solution) / reference)

print("Finished search")

# Create the 3D plot
X, Y = np.meshgrid(accuracies_v, accuracies_c)
Z = relative_acc

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis')

# Set axis labels
ax.set_xlabel('Accuracies V')
ax.set_ylabel('Accuracies C')
ax.set_zlabel('Relative Accuracy (%)')

# Show plot
plt.show()
