import os
import time
from functools import wraps
import matplotlib.pyplot as plt
import numpy as np
import array_norm_cpp

SHAPE = (200000)
NREPEAT=1000

def repeat(nrepeat):
    def timing_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time() # Record start time
            for _ in range(nrepeat):
                _ = func(*args, **kwargs) # Execute the function
            end_time = time.time() # Record end time
            return end_time - start_time
        return wrapper
    return timing_decorator

@repeat(nrepeat=NREPEAT)
def numpy_norm(arr):
    return np.sum(arr**2)

@repeat(nrepeat=NREPEAT)
def omp_norm(arr):
    return array_norm_cpp.l2_norm_omp(arr)

if __name__== "__main__": 
    max_threads = 40
    rng = np.random.default_rng(seed=1000)
    arr = rng.random(SHAPE)
    runtime_numpy = numpy_norm(arr)  
    speedup = {}
    for nthreads in range(1,max_threads):
        os.environ["OMP_NUM_THREADS"]=str(nthreads)
        runtime_omp = omp_norm(arr) 
        speedup[nthreads] = runtime_numpy/runtime_omp
    plt.plot(speedup.keys(), speedup.values())
    plt.ylabel("speedup")
    plt.xlabel("nthreads")
    plt.title("omp norm versus numpy baseline")
    plt.savefig("speedup_omp")


    