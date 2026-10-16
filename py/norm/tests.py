import os
import numpy as np
import array_norm_cpp

def test():

    n=2*3*4
    arr = np.arange(n)
    arr = np.reshape(arr,(4,3,2))
    norm =array_norm_cpp.l2_norm(arr)
    sum = (n-1)*(n)*(2*n-1)/6
    assert norm == sum, f"{norm =} != {sum=}"

def test_omp():
    os.environ["OMP_NUM_THREADS"]=str(4)
    n=5*6*7*9
    arr = np.arange(n)
    arr = np.reshape(arr,(7,6,5, 9))
    norm =array_norm_cpp.l2_norm_omp(arr)
    sum = (n-1)*(n)*(2*n-1)/6
    assert norm == sum, f"{norm =} != {sum=}"

def test_func():
    n=4*5*6*7
    arr = np.arange(n)
    arr = np.reshape(arr,(7,6,5,4))
    def f(a,b):
        return a+b**3
    norm = array_norm_cpp.func_norm(arr, f)
    sum = (n-1)*(n)/2
    sum*=sum
    assert norm == sum, f"{norm =} != {sum=}"

def test_random():
    n = 1000
    arr = np.random.rand(n)
    norm =array_norm_cpp.l2_norm_omp(arr)
    np_norm = np.sum(arr**2)
    np.testing.assert_allclose(norm , np_norm, rtol=1.0e-8)
