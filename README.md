# Cylindrical Magnet B-Field Solution

## About
This code calculates the B-field of a cylindrical magnet at any point in 3D space given magnetic moment, radius, and height.

I use a bound-current approximation, discretized into rings. I discretize these rings into arcs, and solve for the B-field at any given point using Biot-Savart and the superposition principle.
It's of course quite flexible, and can be extended for use as a current-ring, solenoid, or hemholtz coil field simulation.

i wrote it for IYPT so if u end up using it for some YPT around the world pls let me know and we can chat a bit!

## Organization
uhh bfield and threaded_bfield are single worker and multi-worker (multithreaded) versions of the same thing. (removed now cause jit was just faster)
It actually takes quite a bit of latency to spawn so many workers, so if u can use bfield and make ur calls threaded. bfield_threaded discretizes the current rings into chunks which is faster once u have approximately 80 or more discretizations

```python
import bfield
# OR
import threaded_bfield as bfield

bfield.solution(np.array([0,0,2]),moment=0.8,mradius=0.02,mheight=0.01,accuracy=[80,80])
```
## Dependencies
```
# Python Packages
numpy
matplotlib
numba
```

## Showcase
![multifield](https://github.com/user-attachments/assets/be06950f-b90f-424a-9de5-34decc347970)

![CorrectLogField](https://github.com/user-attachments/assets/d1c530a0-9e9f-4dfb-a72f-bae5d5d1f85c)

![compared_todipolemodel](https://github.com/user-attachments/assets/4994ccfa-a336-4dd1-aad9-381a84ffd8df)


srry for teh messy code, this is just some stuff i used for iypt that it hought id publish ya :P

also i wrote this in like 2 hours on the 高铁从from kunming到深圳 so like there may be issues no guarantees :pensive:


## Discretization Error

![image](https://github.com/user-attachments/assets/c40fb930-aedd-479b-812d-a39719faa26b)
(NEW ALGORITHM)
![image](https://github.com/user-attachments/assets/8a0b093c-5b56-4044-a915-937d18978707)
(OLD ALGORITHM)
(Relative to a high-fidelity simulation)


## Benchmarking
```
## Parameters
# 100 VT-DISC, 100 CIR-DISC, Averaged 100 Runs
# 4c8t system, Tiger Lake

Numba JIT-Based Solution
	First Call: 1188 ms # Needs JIT compilation
	Discrete Call Time: 2706 us
	Segment Call Time: 270 ns

Multi-threaded Solution
	First Call: 89 ms
	Discrete Call Time: 94074 us
	Segment Call Time: 9407 ns

Single-threaded Solution
	First call: 246 ms
	Discrete Call Time: 260706 us
	Segment Call Time: 26070 ns

# Note: Scaling is roughly linear with discretizations, with 10x10 disc. I get a 32us call time (roughy 30,657 calls/sec!).
```
![benchmark](https://github.com/user-attachments/assets/14023b21-19c9-43b3-a56e-288eff619c9c)
## Citations
Griffiths, D. J. (2024). Introduction to Electrodynamics (5 ed.). Cambridge 	University. doi:10.1017/9781009397735. ISBN 978-1-009-39773-5.​
