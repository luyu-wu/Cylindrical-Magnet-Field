import numpy as np
import bfield
#import bfield_no_numba as bfield
#import bfield_threaded as bfield
import time

print("\n\033[1mCylindrical B-Field Benchmark\033[0m\nPlease wait while the benchmark is run!\n")

v_steps = 10 # circles around the magnet
cir_steps = 10 # steps around the circle
length = 1000

t0 = time.perf_counter()

bfield.solution(
        position=np.array([0,0,0.1]),
        mradius=0.005,
        mheight=0.002,
        magnetization=1.1*(10**7),
        accuracy=[v_steps,cir_steps]
    )

print("Compilation:",int(1e3* (time.perf_counter()-t0) ),"ms")

t0 = time.perf_counter()

for _ in range(length):
    bfield.solution(
        position=np.array([0,0,0.1]),
        mradius=0.005,
        mheight=0.002,
        magnetization=1.1*(10**7),
        accuracy=[v_steps,cir_steps]
    )

print("Arc Call Time:",int(1e9*(time.perf_counter()-t0)/(length*v_steps*cir_steps)),"ns")


print("\nSpeed:",int(1/((time.perf_counter()-t0)/(length*v_steps*cir_steps))),"Calls/s")
