import numpy as np
import bfield
#import bfield_no_numba as bfield
#import bfield_threaded as bfield
import time

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

print("First Call:",int(1e3* (time.perf_counter()-t0) ),"ms")

t0 = time.perf_counter()

for i in range(length):
    bfield.solution(
        position=np.array([0,0,0.1]),
        mradius=0.005,
        mheight=0.002,
        magnetization=1.1*(10**7),
        accuracy=[v_steps,cir_steps]
    )

#print("Total Time Taken:",int(1e3* (time.perf_counter()-t0) ),"ms")
print("Discrete Call Time:",int(1e6*((time.perf_counter()-t0)/length) ),"us")
print("Segment Call Time:",int(1e9*(time.perf_counter()-t0)/(length*v_steps*cir_steps)),"ns")


print("\nSpeed:",int(1/((time.perf_counter()-t0)/length)),"Calls/s")
