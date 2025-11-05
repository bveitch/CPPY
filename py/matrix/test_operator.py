import pytest
import itertools
import numpy as np
import numpy.typing as npt
import matrix_operator_cpp

m2d_3x3 = np.array([[1.,2.,0], [-1.,1.,1.], [3.,0.,1.]])
m2d_3x5 = np.array([[1.,2.,0], [-1.,1.,1.], [3.,0.,1.], [0,1.,1.0],[-1,0,10]])
m2d_large =  np.ones((100,1000), dtype=np.float64)
ARRAYS = [m2d_3x3, m2d_3x5, m2d_large]
TESTS = ["Matrix", "Sparse", "ParBlk", "ParCol", "ParRow"]

@pytest.mark.parametrize("arr2d,operator", list(itertools.product(ARRAYS,TESTS)))
class TestOperator:

    nthreads =4
    mop = None
    rng = np.random.default_rng(seed=1000)

    def create_operator(self, arr2d: npt.NDArray, operator: str):
        print(self.nthreads)
        if operator == "Sparse":
            nrow, ncol = arr2d.shape
            locs = np.nonzero(arr2d)
            values = arr2d[locs]
            self.mop =  matrix_operator_cpp.SparseOp(nrow, ncol, tuple(locs[0]), tuple(locs[1]), tuple(values), self.nthreads)
        elif operator == "ParBlk":
            self.mop= matrix_operator_cpp.MatrixOpParBlk(arr2d, self.nthreads)
        elif operator == "ParCol":
            self.mop = matrix_operator_cpp.MatrixOpParCol(arr2d, self.nthreads)
        elif operator == "ParRow":
            self.mop = matrix_operator_cpp.MatrixOpParRow(arr2d, self.nthreads)
        else:
            self.mop = matrix_operator_cpp.MatrixOp(arr2d, self.nthreads)
        
    def test_operator_shape(self, arr2d: npt.NDArray,  operator: str):
        self.create_operator(arr2d, operator)
        assert self.mop.shape == arr2d.shape, f"{self.mop.shape=} != {arr2d.shape=}"

    def test_nthreads_shape(self, arr2d: npt.NDArray,  operator: str):
        self.create_operator(arr2d, operator)
        assert self.mop.nthreads == self.nthreads, f"{self.mop.nthreads=} != {self.nthreads=}"

    def test_forward_size(self, arr2d: npt.NDArray,  operator: str):
        self.create_operator(arr2d, operator)
        nrow, ncol = arr2d.shape
        x = self.rng.random(ncol)
        y=self.mop.forward(x)
        assert f"forward size = {y.size} != {nrow}"

    def test_adjoint_size(self, arr2d: npt.NDArray,  operator: str):
        self.create_operator(arr2d, operator)
        nrow, ncol = arr2d.shape
        x = self.rng.random(nrow)
        y=self.mop.adjoint(x)
        assert f"adjoint size = {y.size} != {ncol}"

    def test_bad_forward_size(self, arr2d: npt.NDArray,  operator: str):
        self.create_operator(arr2d, operator)
        _, ncol = arr2d.shape
        badsize = ncol+1
        x = self.rng.random(badsize)
        with pytest.raises(RuntimeError) as excinfo:
            self.mop.forward(x)
        assert f"input size = {badsize} != {ncol}" in str(excinfo.value)

    def test_bad_adjoint_size(self, arr2d: npt.NDArray,  operator: str):
        self.create_operator(arr2d, operator)
        nrow, _ = arr2d.shape
        badsize = nrow-1
        y = self.rng.random(badsize)
        with pytest.raises(RuntimeError) as excinfo:
            self.mop.adjoint(y)
        assert f"input size = {badsize} != {nrow}" in str(excinfo.value)      

    def test_operator_forward(self, arr2d: npt.NDArray,  operator: str):
        _, nrow = arr2d.shape
        x = self.rng.random(nrow)
        y=np.dot(arr2d,x)
        self.create_operator(arr2d, operator)
        y_cpp = self.mop.forward(x)
        np.testing.assert_allclose(y, y_cpp, rtol=1.0e-4)

    def test_operator_adjoint(self, arr2d: npt.NDArray,  operator: str):
        ncol, _ = arr2d.shape
        y = self.rng.random(ncol)
        xT=np.dot(arr2d.T,y)
        self.create_operator(arr2d, operator) 
        xT_cpp = self.mop.adjoint(y)
        np.testing.assert_allclose(xT, xT_cpp, rtol=1.0e-4)

    def test_operator_dotproduct(self, arr2d: npt.NDArray,  operator: str):
        nrow, ncol = arr2d.shape
        x = self.rng.random(ncol)
        y = self.rng.random(nrow)
        self.create_operator(arr2d, operator)
        mx = self.mop.forward(x)
        yTmx = np.dot(y,mx)
        mTy = self.mop.adjoint(y)
        xTmTy = np.dot(x,mTy)
        np.testing.assert_allclose(yTmx, xTmTy,rtol=1.0e-4)

    