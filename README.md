# Cylindrical Magnet B-Field Solution

## About
This code calculates the B-field of a cylindrical magnet at any point in 3D space given magnetization, radius, and height.

I use a bound-current approximation, discretized into rings. I discretize these rings into arcs, and solve for the B-field at any given point using Biot-Savart and the superposition principle.
It's of course quite flexible, and can be extended for use as a current-ring, solenoid, or hemholtz coil field simulation.

i wrote it for IYPT so if u end up using it for some YPT around the world pls let me know and we can chat a bit!

## Organization
uhh bfield and threaded_bfield are single worker and multi-worker (multithreaded) versions of the same thing.
It actually takes quite a bit of latency to spawn so many workers, so if u can use bfield and make ur calls threaded. bfield_threaded discretizes the current rings into chunks which is faster once u have approximately 80 or more discretizations

also like the code isnt very fast, i would write in rust but i like to import it easily into other python scripts /shrug

u can look at draw_field or other scripts as examples of how to use

```python
import bfield
# OR
import threaded_bfield as bfield

bfield.solution(np.array([0,0,2]),magnetization=1e5,mradius=0.02,mheight=0.01,accuracy=[80,80])
```
## Dependencies
```
# Python Packages
numpy
matplotlib
scipy

numba (optional, use no_numba or threaded bfield module if u don't want numba)
```


## Showcase
![high_res](https://github.com/user-attachments/assets/0909a81f-3f80-4827-82ce-33d3d0b28551)



srry for teh messy code, this is just some stuff i used for iypt that it hought id publish ya :P

also i wrote this in like 2 hours on the 高铁从from kunming到深圳 so like there may be issues no guarantees :pensive:


## Discretization Error
![image](https://github.com/user-attachments/assets/8a0b093c-5b56-4044-a915-937d18978707)

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


