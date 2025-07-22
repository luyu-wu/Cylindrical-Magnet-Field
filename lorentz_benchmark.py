import numpy as np
import lorentz

# import bfield_no_numba as bfield
# import bfield_threaded as bfield
import time

print(
    "\n\033[1mLorentz Force Benchmark\033[0m\nPlease wait while the benchmark is run!\n"
)

v_steps = 1  # circles around the magnet
cir_steps = 8  # steps around the circle
length = 5000

t0 = time.perf_counter()

lorentz.solution(
    position=np.array([0, 0, 0.1]),
    mradius=0.005,
    mheight=0.002,
    moment=1,
    accuracy=[v_steps, cir_steps],
)

print("Compilation:", int(1e3 * (time.perf_counter() - t0)), "ms")

t0 = time.perf_counter()

for _ in range(length):
    lorentz.solution(
        position=np.array([0, 0, 0.1]),
        mradius=0.005,
        mheight=0.002,
        moment=1,
        accuracy=[v_steps, cir_steps],
    )

print("Call Time:", int(1e6 * (time.perf_counter() - t0) / (length)), "uS")


print("\nSpeed:", int(1 / ((time.perf_counter() - t0) / (length))), "Calls/s")
