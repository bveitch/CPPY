import pytest
import numpy as np
from pylops import LinearOperator
import matrix_operator_cpp

m2d_3x3 = np.array([[1.,2.,0], [-1.,1.,1.], [3.,0.,1.]])
m2d_3x5 = np.array([[1.,2.,0], [-1.,1.,1.], [3.,0.,1.], [0,1.,1.0],[-1,0,10]])
m2d_large =  np.ones((100,1000), dtype=np.float64)
ARRAYS = [m2d_3x3, m2d_3x5, m2d_large]
class CPPMatrixMult(LinearOperator):
    def __init__(self, m2d):
        self.m_op = matrix_operator_cpp.MatrixOp(m2d, 1)
        super().__init__(
            dtype=m2d.dtype,
            shape=m2d.shape,
            explicit=True,
        )

    def _matvec(self, x):
        return self.m_op.forward(x)

    def _rmatvec(self, x):
        return self.m_op.adjoint(x)

@pytest.mark.parametrize("arr2d", ARRAYS)
def test_dotproduct(arr2d):
    nrow, ncol = arr2d.shape
    rng = np.random.default_rng(seed=1000)
    x = rng.random(ncol)
    y = rng.random(nrow)
    MOp = CPPMatrixMult(arr2d)
    Mx = MOp @ x
    yTMx = np.dot(y,Mx)
    MTy = MOp.H @ y
    xTMTy = np.dot(x,MTy)
    np.testing.assert_allclose(yTMx, xTMTy,rtol=1.0e-4)
