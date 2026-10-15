import numpy as np
from objfn import L2ObjectiveFn
from solver import GeneralSolver

def solve_l2(A, b):
    Aobjfn = L2ObjectiveFn(arr2d= A, data = b)
    return GeneralSolver(Aobjfn).solve()
    
A = np.diag([5.,3.,4.,1.])
b = np.array([1,1,1,1])

ans = solve_l2(A,b)
exp = np.linalg.inv(A) @ b
print(f"{ans=}, {exp=}")