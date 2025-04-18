import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import bfield

print(
    "\n\033[1mCylindrical B-Field Benchmark\033[0m\nPlease wait while the benchmark is run!\n"
)

v_steps = 10  # circles around the magnet
cir_steps = 20  # steps around the circle
length = 50000

t0 = time.perf_counter()

bfield.solution(
    position=np.array([0, 0, 0.1]),
    mradius=0.005,
    mheight=0.002,
    moment=1,
    accuracy=[v_steps, cir_steps],
)

print("Compilation:", int(1e3 * (time.perf_counter() - t0)), "ms")

t0 = time.perf_counter()

for _ in range(length):
    bfield.solution(
        position=np.array([0, 0, 0.1]),
        mradius=0.005,
        mheight=0.002,
        moment=1,
        accuracy=[v_steps, cir_steps],
    )

calls_st = int(1 / ((time.perf_counter() - t0) / (length * v_steps * cir_steps)))

print(
    "Arc Call Time:",
    int(1e9 * (time.perf_counter() - t0) / (length * v_steps * cir_steps)),
    "ns",
)


print(
    "\nSpeed:",
    calls_st,
    "Calls/s",
)

print("\n\033[1mMultithreaded B-Field Benchmark\033[0m\n")


def worker_function(args):
    iterations, v_steps, cir_steps = args
    for _ in range(iterations):
        bfield.solution(
            position=np.array([0, 0, 0.1]),
            mradius=0.005,
            mheight=0.002,
            moment=1,
            accuracy=[v_steps, cir_steps],
        )
    return iterations * v_steps * cir_steps


num_cpus = mp.cpu_count()
print(f"Using {num_cpus} CPU cores")

# Split the work
iterations_per_process = length
total_work = 0

t0 = time.perf_counter()

with ProcessPoolExecutor(max_workers=num_cpus) as executor:
    args = [(iterations_per_process, v_steps, cir_steps) for _ in range(num_cpus)]
    results = list(executor.map(worker_function, args))
    total_work = sum(results)

total_time = time.perf_counter() - t0


calls_mt = int(total_work / total_time)
print(
    "Multithreaded Speed:",
    calls_mt,
    "Calls/s",
)

print("\n\nSpeedup (MT/ST)", calls_mt / calls_st, "X")
