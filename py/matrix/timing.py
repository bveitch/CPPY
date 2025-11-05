import time
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import matrix_operator_cpp

class TimedOperator:

    class NumpyOp:

        def __init__(self, arr2d):
            self.array = arr2d

        def forward(self, x):
            return np.dot(self.array,x)
            
        def adjoint(self, x):
            return np.dot(self.array.T,x)
        
    def __init__(self, arr2d, operator: str, nthreads =1):
        self.rng = np.random.default_rng(seed=1000)
        self.ncol = arr2d.shape[0]
        self.nrow = arr2d.shape[1]
        if operator == "Numpy":
           self.mop = TimedOperator.NumpyOp(arr2d)
        else:
            self.mop = None
            if operator == "Sparse":
                nrow, ncol = arr2d.shape
                locs = np.nonzero(arr2d)
                values = arr2d[locs]
                self.mop =  matrix_operator_cpp.SparseOp(nrow, ncol, tuple(locs[0]), tuple(locs[1]), tuple(values))
            elif operator == "ParBlk":
                self.mop= matrix_operator_cpp.MatrixOpParBlk(arr2d, nthreads)
            elif operator == "ParCol":
                self.mop = matrix_operator_cpp.MatrixOpParCol(arr2d, nthreads)
            elif operator == "ParRow":
                self.mop = matrix_operator_cpp.MatrixOpParRow(arr2d, nthreads)
            else:
                self.mop = matrix_operator_cpp.MatrixOp(arr2d, nthreads)

        
    def __call__(self, nrepeat: int) -> float:
        runtime = 0.
        for _ in range(nrepeat):
            x = self.rng.random(self.nrow)
            start_time = time.time()
            self.mop.forward(x)
            end_time = time.time()
            runtime += end_time - start_time
        return runtime/nrepeat

TESTS =  {"ParRow", "ParCol", "ParBlock"}
SHAPE = (10000,100000)
NREPEAT=10
if __name__== "__main__": 
    max_threads = 41
    rng = np.random.default_rng(seed=1000)
    arr2d = rng.random(SHAPE)
    numpy_op = TimedOperator(arr2d, "Numpy")
    runtime_numpy = numpy_op(nrepeat=NREPEAT)  
    for test_name in TESTS :
        speedup = {}
        for nthreads in range(1,max_threads):
            print(f"{test_name}: {nthreads}")
            timed_op = TimedOperator(arr2d, test_name, nthreads)
            runtime = timed_op(nrepeat=NREPEAT) 
            speedup[nthreads] = runtime_numpy/runtime
        plt.plot(speedup.keys(), speedup.values(), label = test_name)
    plt.ylabel(f"speedup")
    plt.xlabel("nthreads")
    plt.title(f"shape = {SHAPE}")
    plt.legend()
    plt.savefig("speedup_matrixops")


    