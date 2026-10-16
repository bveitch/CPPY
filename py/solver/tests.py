import numpy as np
from objfn import L2ObjectiveFn
from solver import SciPySolver, direct_solve
     
def test_solve_l2():
    A = np.diag([5.,3.,4.,1.])
    b = np.array([1,1,1,1])
    Aobjfn = L2ObjectiveFn(arr2d= A, data = b)
    ans = SciPySolver(Aobjfn).solve()
    exp = np.linalg.inv(A) @ b
    np.testing.assert_allclose(ans, exp, rtol=1.0e-8)

def test_solve2_l2():
    A = np.zeros((4, 10))
    A[:, :4] += np.diag([5.,3.,4.,1.])
    A[1, 9] = 1
    l = 0.01
    y=np.zeros(A.shape[1])
    b = np.array([1,1,1,1])
    T = np.sqrt(l)*np.eye(y.size)
    arr2d = np.concatenate([A,T], axis=0)
    assert arr2d.shape == (A.shape[0] + T.shape[0], T.shape[1])
    data = np.concatenate([b,y],axis=0)
    Aobjfn = L2ObjectiveFn(arr2d= arr2d, data = data)
    ans = SciPySolver(Aobjfn).solve()
    exp = direct_solve(A,b, l=l, y=y)
    np.testing.assert_allclose(ans, exp, rtol=1.0e-5)