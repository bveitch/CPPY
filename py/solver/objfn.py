from abc import ABC, abstractmethod
import math
import numpy as np
import numpy.typing as npt
import matrix_operator_cpp

class L2ObjectiveFn:

    def __init__(self, 
                 op, 
                 data: npt.NDArray | None = None):
        self.op = op
        self.d = data

    @classmethod
    def from_arr2d(cls, 
                arr2d : npt.NDArray, 
                data: npt.NDArray | None = None,
                nthreads: int = 4):
        op = matrix_operator_cpp.MatrixOp(arr2d, nthreads)
        assert data.size == op.shape[0], f"{data.size=} not equal to {op.shape[0]}"
        return cls(op, data)
    
    @classmethod
    def from_sparse_values(cls, 
                nrow : int,
                ncol : int,
                locs : npt.NDArray,
                values : npt.NDArray, 
                data: npt.NDArray | None = None,
                nthreads: int = 4):
        assert data.size == nrow, f"{data.size=} not equal to {nrow}"
        op = matrix_operator_cpp.SparseOp(nrow, ncol, tuple(locs[0]), tuple(locs[1]), tuple(values), nthreads)
        return cls(op, data)
        

    @property
    def data(self):
        return self.d
    
    @property
    def xsize(self):
        return self.op.shape[1]
    
    def _eval(self, x):
        if self.op is not None:
            fx = np.zeros(self.d.shape)
            fx = self.op.forward(x)
        else:
            fx = x
        if self.d is not None:
            return fx - self.d
        else:
            return fx

    def value(self, x):
        r = self._eval(x)
        return 0.5*np.sum(r**2)
    
    def gradient(self, x):
        r = self._eval(x)
        if self.op is not None:
            return self.op.adjoint(r)
        else:
            return r
        
    def __call__(self, x: npt.NDArray):
        return self.value(x)

def check_objective(objective: L2ObjectiveFn, x:npt.NDArray, eps=1.0e-6):
    dx = np.random.random(x.shape)
    fpx=objective(x+eps*dx)
    fmx=objective(x-eps*dx)
    df = (fpx-fmx)*(0.5/eps)
    gx=objective.gradient(x)
    dfdx = np.dot(gx.ravel(), dx.ravel())
    np.testing.assert_allclose(df, dfdx, atol=1.0e-6, rtol=eps*eps*dx.dot(dx))