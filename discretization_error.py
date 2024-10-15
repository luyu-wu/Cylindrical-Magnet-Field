import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import linalg as la
import bfield

size_c = 40  # Grid size
size_v = 20
# Reference value calculation
print("Compiling...")
reference = la.norm(bfield.solution(
    position=np.array([0, 0, 0]),
    mradius=0.01,
    mheight=0.03,
    magnetization=1e7,
    accuracy=[1000, 40]
))
print("Found reference")

# Define accuracy ranges
accuracies_v = np.linspace(1, 40, size_v).astype(int)
accuracies_c = np.linspace(3, 150, size_c).astype(int)
relative_acc = np.zeros((size_c, size_v))

# Calculate relative accuracy for different discretizations

for v_s in range(size_v):
    for c_s in range(size_c):
        current_solution = la.norm(bfield.solution(
            position=np.array([0, 0, 0]),
            mradius=0.01,
            mheight=0.03,
            magnetization=1e7,
            accuracy=[accuracies_v[v_s], accuracies_c[c_s]]
        ))
        relative_acc[c_s, v_s] = abs((reference - current_solution) / reference) * 100
print("Finished search")

# Create the 3D plot
X, Y = np.meshgrid(accuracies_v, accuracies_c)
Z = relative_acc

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis')

# Set axis labels
ax.set_xlabel('Vertical Discretizations')
ax.set_ylabel('Circular Discretizations')
ax.set_zlabel('Relative Error (%)')

# Show plot
plt.show()
