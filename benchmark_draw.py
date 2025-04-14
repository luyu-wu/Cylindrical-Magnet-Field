import numpy as np
import bfield
import time
import matplotlib.pyplot as plt

length = 100
batches = 30
step_size = 10

comp_time = time.perf_counter()
print("Compiling B-Field..")
bfield.solution(
    position=np.array([0, 0, 0.1]),
    mradius=0.005,
    mheight=0.002,
    moment=1,
    accuracy=[2, 2],
)
print("Precompiled B-Field:", int(1e3 * (time.perf_counter() - comp_time)), "ms\n")


# Circular discretizations benchmark
v_steps = 2  # circles around the magnet
cir_steps = 10  # steps around the circle
v_init, cir_ini = v_steps, cir_steps

data_raw = np.zeros((length, batches))
for leng in range(length):
    for num in range(batches):
        t0 = time.perf_counter()
        bfield.solution(
            position=np.array([0, 0, 0.1]),
            mradius=0.005,
            mheight=0.002,
            moment=1,
            accuracy=[v_steps, cir_steps],
        )
        data_raw[leng, num] = 1e6 * (time.perf_counter() - t0)
    cir_steps += step_size

avs = np.zeros(length)
st_devs = np.zeros(length)

for i in range(length):
    avs[i] = np.average(data_raw[i])
    st_devs[i] = np.std(data_raw[i])

x_axis = np.linspace(v_init * cir_ini, v_steps * cir_steps, length)

# scatter stuff
x_scatter = np.zeros(length * batches)
recursor = 0
for i in x_axis:
    for d in range(batches):
        x_scatter[recursor] = i
        recursor += 1

plt.scatter(x_scatter, data_raw.flatten(), alpha=0.05, color="#FF9848")
plt.plot(
    x_axis, avs, linestyle="dashdot", color="#CC4F1B", label="Circular Discretizations"
)
plt.fill_between(
    x_axis,
    avs - st_devs,
    avs + st_devs,
    alpha=0.5,
    edgecolor="#CC4F1B",
    facecolor="#FF9848",
)


## VERTICAL STUFF
v_steps = 10  # circles around the magnet
cir_steps = 2  # steps around the circle
v_init, cir_ini = v_steps, cir_steps


data_raw = np.zeros((length, batches))
for leng in range(length):
    for num in range(batches):
        t0 = time.perf_counter()
        bfield.solution(
            position=np.array([0, 0, 0.1]),
            mradius=0.005,
            mheight=0.002,
            moment=1,
            accuracy=[v_steps, cir_steps],
        )
        data_raw[leng, num] = 1e6 * (time.perf_counter() - t0)
    v_steps += step_size

avs = np.zeros(length)
st_devs = np.zeros(length)

for i in range(length):
    avs[i] = np.average(data_raw[i])
    st_devs[i] = np.std(data_raw[i])

x_axis = np.linspace(v_init * cir_ini, v_steps * cir_steps, length)

# scatter stuff
x_scatter = np.zeros(length * batches)
recursor = 0
for i in x_axis:
    for d in range(batches):
        x_scatter[recursor] = i
        recursor += 1

plt.scatter(x_scatter, data_raw.flatten(), alpha=0.05, color="#1B2ACC")
plt.plot(
    x_axis, avs, linestyle="dashdot", color="#1B2ACC", label="Vertical Discretizations"
)
plt.fill_between(
    x_axis,
    avs - st_devs,
    avs + st_devs,
    alpha=0.5,
    edgecolor="#CC4F1B",
    facecolor="#089FFF",
)


plt.grid()
plt.ylabel("Solution Time (uS)")
plt.xlabel("Total Discretizations (arb.)")
plt.title("Computation Time vs. Discretizations")
plt.legend()
plt.show()
