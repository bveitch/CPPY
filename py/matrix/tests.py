import pytest
import itertools
import numpy as np
import numpy.typing as npt
import matrix_operator_cpp
from pylops import LinearOperator
from pylops.utils import dottest as pylops_dottest

m2d_3x3 = np.array([[1.,2.,0], [-1.,1.,1.], [3.,0.,1.]])
m2d_3x5 = np.array([[1.,2.,0], [-1.,1.,1.], [3.,0.,1.], [0,1.,1.0],[-1,0,10]])
m2d_large =  np.ones((100,1000), dtype=np.float64)
ARRAYS = [m2d_3x3, m2d_3x5, m2d_large]
OPERATORS = ["Matrix", "Sparse", "ParBlk", "ParCol", "ParRow"]

NTHREADS = 4
rng = np.random.default_rng(seed=1000)

def create_operator(arr2d: npt.NDArray, operator: str):
    if operator == "Sparse":
        nrow, ncol = arr2d.shape
        locs = np.nonzero(arr2d)
        values = arr2d[locs]
        return  matrix_operator_cpp.SparseOp(nrow, ncol, tuple(locs[0]), tuple(locs[1]), tuple(values), NTHREADS)
    elif operator == "ParBlk":
        return matrix_operator_cpp.MatrixOpParBlk(arr2d, NTHREADS)
    elif operator == "ParCol":
        return matrix_operator_cpp.MatrixOpParCol(arr2d, NTHREADS)
    elif operator == "ParRow":
        return matrix_operator_cpp.MatrixOpParRow(arr2d, NTHREADS)
    else:
        return matrix_operator_cpp.MatrixOp(arr2d, NTHREADS)

pytestmark = pytest.mark.parametrize("arr2d,operator", list(itertools.product(ARRAYS,OPERATORS)))     

def test_operator_shape(arr2d: npt.NDArray,  operator: str):
    op = create_operator(arr2d, operator)
    assert op.shape == arr2d.shape, f"{op.shape=} != {arr2d.shape=}"

def test_nthreads_shape(arr2d: npt.NDArray,  operator: str):
    op = create_operator(arr2d, operator)
    assert op.nthreads == NTHREADS, f"{op.nthreads=} != {NTHREADS=}"

def test_forward_size(arr2d: npt.NDArray,  operator: str):
    op = create_operator(arr2d, operator)
    nrow, ncol = arr2d.shape
    x = rng.random(ncol)
    y=op.forward(x)
    assert f"forward size = {y.size} != {nrow}"

def test_adjoint_size(arr2d: npt.NDArray,  operator: str):
    op = create_operator(arr2d, operator)
    nrow, ncol = arr2d.shape
    x = rng.random(nrow)
    y=op.adjoint(x)
    assert f"adjoint size = {y.size} != {ncol}"

def test_operator_forward(arr2d: npt.NDArray,  operator: str):
    _, nrow = arr2d.shape
    rng = np.random.default_rng(seed=1000)
    x = rng.random(nrow)
    y=np.dot(arr2d,x)
    op = create_operator(arr2d, operator)
    y_cpp = op.forward(x)
    np.testing.assert_allclose(y, y_cpp, rtol=1.0e-4)

def test_operator_adjoint(arr2d: npt.NDArray,  operator: str):
    ncol, _ = arr2d.shape
    y = rng.random(ncol)
    xT=np.dot(arr2d.T,y)
    op = create_operator(arr2d, operator) 
    xT_cpp = op.adjoint(y)
    np.testing.assert_allclose(xT, xT_cpp, rtol=1.0e-4)

def test_operator_dotproduct(arr2d: npt.NDArray,  operator: str):
    nrow, ncol = arr2d.shape
    x = rng.random(ncol)
    y = rng.random(nrow)
    op = create_operator(arr2d, operator)
    mx = op.forward(x)
    yTmx = np.dot(y,mx)
    mTy = op.adjoint(y)
    xTmTy = np.dot(x,mTy)
    np.testing.assert_allclose(yTmx, xTmTy,rtol=1.0e-4)

class CPPMatrixMult(LinearOperator):
    def __init__(self, m2d, operator_name):
        self.m_op = create_operator(m2d, operator_name)
        super().__init__(
            dtype=m2d.dtype,
            shape=m2d.shape,
            explicit=True,
        )

    def _matvec(self, x):
        return self.m_op.forward(x)

    def _rmatvec(self, x):
        return self.m_op.adjoint(x)

def test_pylops_dotproduct(arr2d: npt.NDArray,  operator: str):
    MOp = CPPMatrixMult(arr2d, operator)
    pylops_dottest(MOp)